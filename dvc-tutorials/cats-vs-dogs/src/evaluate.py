import sys
import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow import keras
from sklearn import metrics
import numpy as np
import json

from plots import *

tfds.disable_progress_bar()

model_file = sys.argv[1]
eval_file = 'reports/metrics/evaluation.json'
roc_cm_file = 'reports/metrics/roc_cm.json'

train_split = 40
val_split = 10
test_split = 10
im_size = (150, 150)

train_ds, valid_ds, test_ds = tfds.load("cats_vs_dogs",
                                        split=[f"train[:{train_split}%]",
                                               f"train[{train_split}%:{train_split + val_split}%]",
                                               f"train[{train_split + val_split}%:{train_split + val_split + test_split}%]"],
                                        as_supervised=True)

# Resize images
train_ds = train_ds.map(lambda x, y: (tf.image.resize(x, im_size), y))
valid_ds = valid_ds.map(lambda x, y: (tf.image.resize(x, im_size), y))
test_ds = test_ds.map(lambda x, y: (tf.image.resize(x, im_size), y))

# Batch and prefetch
train_ds = train_ds.cache().batch(32).prefetch(buffer_size=10)
valid_ds = valid_ds.cache().batch(32).prefetch(buffer_size=10)
test_ds = test_ds.cache().batch(32).prefetch(buffer_size=10)

# Load in model
model = keras.models.load_model(model_file)

train_pred = np.squeeze(model.predict(train_ds))
valid_pred = np.squeeze(model.predict(valid_ds))
test_pred = np.squeeze(model.predict(test_ds))

# Threshold predictions to obtain class labels
train_pred_thr = (train_pred > 0.5).astype(int)
valid_pred_thr = (valid_pred > 0.5).astype(int)
test_pred_thr = (test_pred > 0.5).astype(int)

# Extract labels
train_labels = np.concatenate([y for x, y in train_ds])
valid_labels = np.concatenate([y for x, y in valid_ds])
test_labels = np.concatenate([y for x, y in test_ds])

# Compute accuracy and loss
train_acc = tf.keras.metrics.binary_accuracy(train_labels, train_pred_thr).numpy()
valid_acc = tf.keras.metrics.binary_accuracy(valid_labels, valid_pred_thr).numpy()
test_acc = tf.keras.metrics.binary_accuracy(test_labels, test_pred_thr).numpy()

train_loss = tf.keras.metrics.binary_crossentropy(train_labels, train_pred).numpy()
valid_loss = tf.keras.metrics.binary_crossentropy(valid_labels, valid_pred).numpy()
test_loss = tf.keras.metrics.binary_crossentropy(test_labels, test_pred).numpy()

# ROC, CM
train_fpr, train_tpr, train_thresholds = metrics.roc_curve(train_labels, train_pred, drop_intermediate=True)
valid_fpr, valid_tpr, valid_thresholds = metrics.roc_curve(valid_labels, valid_pred, drop_intermediate=True)
test_fpr, test_tpr, test_thresholds = metrics.roc_curve(test_labels, test_pred, drop_intermediate=True)

train_cm = tf.math.confusion_matrix(train_labels, train_pred_thr, num_classes=2)
valid_cm = tf.math.confusion_matrix(valid_labels, valid_pred_thr, num_classes=2)
test_cm = tf.math.confusion_matrix(test_labels, test_pred_thr, num_classes=2)

# Save metric files
with open(eval_file, "w") as fd:
    json.dump({
        "train_binary_accuracy": float(train_acc),
        "validation_binary_accuracy": float(valid_acc),
        "test_binary_accuracy": float(test_acc),
        "train_loss": float(train_loss),
        "validation_loss": float(valid_loss),
        "test_loss": float(test_loss),
    }, fd, indent=4)

with open(roc_cm_file, "w") as fd:
    json.dump(
        {
            "train_roc": [{"fpr": fp, "tpr": tp, "threshold": t} for fp, tp, t in
                          zip(train_fpr, train_tpr, train_thresholds.astype(float))],
            "validation_roc": [{"fpr": fp, "tpr": tp, "threshold": t} for fp, tp, t in
                          zip(valid_fpr, valid_tpr, valid_thresholds.astype(float))],
            "test_roc": [{"fpr": fp, "tpr": tp, "threshold": t} for fp, tp, t in
                          zip(test_fpr, test_tpr, test_thresholds.astype(float))],
            "train_cm": train_cm.numpy().tolist(),
            "validation_cm": valid_cm.numpy().tolist(),
            "test_cm": test_cm.numpy().tolist(),
        }, fd, indent=4)

# Plots
plot_confusion_matrix(train_cm.numpy(), 'reports/figures/train_cm.jpg')
plot_confusion_matrix(valid_cm.numpy(), 'reports/figures/val_cm.jpg')
plot_confusion_matrix(test_cm.numpy(), 'reports/figures/test_cm.jpg')


