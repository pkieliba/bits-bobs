import sys
import yaml
import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.callbacks import EarlyStopping, CSVLogger, Callback

from plots import plot_learning_curve

tfds.disable_progress_bar()
params = yaml.safe_load(open(sys.argv[1]))["train"]

batch_size = params['batch_size']
random_rot = params['random_rotation']
dropout = params['dropout']
epochs = params['epochs']
epochs_ft = params['epochs_finetuning']
optimizer = params['optimizer']
optimizer_ft = params['optimizer_finetuning']
loss_fun = params['loss_fun']
metrics = params['metrics']

train_split = 40
val_split = 10
im_size = (150, 150)
model_out = 'models/model.h5'

train_ds, valid_ds = tfds.load("cats_vs_dogs",
                               split=[f"train[:{train_split}%]",
                                      f"train[{train_split}%:{train_split + val_split}%]"],
                               as_supervised=True)

# Resize images
train_ds = train_ds.map(lambda x, y: (tf.image.resize(x, im_size), y))
valid_ds = valid_ds.map(lambda x, y: (tf.image.resize(x, im_size), y))

# Batch and prefetch
train_ds = train_ds.cache().batch(batch_size).prefetch(buffer_size=10)
valid_ds = valid_ds.cache().batch(batch_size).prefetch(buffer_size=10)

# Data augmentation
data_augmentation = keras.Sequential([layers.RandomFlip("horizontal"),
                                      layers.RandomRotation(random_rot)])

# Pre-trained Xception weights requires that input be scaled
# from (0, 255) to a range of (-1., +1.), the rescaling layer
scale_layer = keras.layers.Rescaling(scale=1 / 127.5, offset=-1)

# Build model
base_model = keras.applications.Xception(
    weights="imagenet",
    input_shape=(150, 150, 3),
    include_top=False)
base_model.trainable = False

inputs = keras.Input(shape=(150, 150, 3))
x = data_augmentation(inputs)
x = scale_layer(x)
x = base_model(x, training=False)  # keep in inference mode, so that batchnorm weights do not update
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(dropout)(x)
outputs = keras.layers.Dense(1, activation='sigmoid')(x)
model = keras.Model(inputs, outputs)

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)
csv_logger = CSVLogger('reports/metrics/metrics_frozen.csv', append=False)
csv_logger_ft = CSVLogger('reports/metrics/metrics_finetune.csv', append=False)


class LogStageLR(Callback):

    def __init__(self, stage):
        self.stage = stage

    def on_epoch_end(self, epoch, logs):
        logs["lr"] = float(tf.keras.backend.get_value(self.model.optimizer.learning_rate))
        logs["training_stage"] = self.stage


# Train top-layers
model.compile(
    optimizer=keras.optimizers.deserialize(optimizer),
    loss=keras.losses.deserialize(loss_fun),
    metrics=metrics)
history = model.fit(train_ds, epochs=epochs, validation_data=valid_ds,
                    callbacks=[early_stopping, LogStageLR(0), csv_logger])

# Fine tuning
base_model.trainable = True
model.compile(
    optimizer=keras.optimizers.deserialize(optimizer_ft),
    loss=keras.losses.deserialize(loss_fun),
    metrics=metrics)
history_ft = model.fit(train_ds, epochs=epochs_ft, validation_data=valid_ds,
                       callbacks=[early_stopping, LogStageLR(1), csv_logger_ft])

model.save(model_out)

# Learning curve plots
plot_learning_curve(history, ['loss', 'binary_accuracy'], 'reports/figures/training_frozen.png')
plot_learning_curve(history_ft, ['loss', 'binary_accuracy'], 'reports/figures/training_finetune.png')





