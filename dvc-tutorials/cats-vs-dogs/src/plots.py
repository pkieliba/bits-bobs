import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve


plt.style.use('seaborn-whitegrid')


def plot_learning_curve(model_history, metrics, outPath, legend=['train', 'val']):

    __, axes = plt.subplots(1, 2, figsize=(20, 5))

    axes[0].set_xlabel("epochs")
    axes[0].set_ylabel(metrics[0])
    axes[0].grid()
    axes[0].plot(model_history.history[metrics[0]], color='b', label=legend[0])
    axes[0].plot(model_history.history[f'val_{metrics[0]}'], color='orange', label=legend[1])
    axes[0].legend(loc="best")

    axes[1].grid()
    axes[1].set_xlabel("epochs")
    axes[1].set_ylabel(metrics[1])
    axes[1].plot(model_history.history[metrics[1]], color='b', label=legend[0])
    axes[1].plot(model_history.history[f'val_{metrics[1]}'], color='orange', label=legend[1])
    axes[1].legend(loc="best")

    plt.savefig(outPath)


def plot_confusion_matrix(cm, outPath, normalize=False, cmap=plt.cm.YlOrRd):

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    __, ax = plt.subplots()
    ax.imshow(cm, interpolation='nearest', cmap=cmap)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() * 1.4 / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(j, i, format(cm[i, j], fmt),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
                size=20)
    tick_marks = np.arange(2)
    ax.set_xticks(tick_marks)
    ax.set_yticks(tick_marks)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)
    ax.set_ylabel('True class', fontsize=20)
    ax.set_xlabel('Predicted class', fontsize=20)
    ax.grid(None)

    plt.savefig(outPath)


def plot_roc(fpr, tpr, labels, outPath):

    __, ax = plt.subplots()

    nsProbs = np.zeros(len(labels), dtype='int8')
    ns_fpr, ns_tpr, _ = roc_curve(labels, nsProbs)

    ax.plot(ns_fpr, ns_tpr, linestyle='--', label="Random", color='grey')
    step_kwargs = ({'step': 'post'})
    ax.step(fpr, tpr, alpha=0.4, color='skyblue', where='post')
    ax.fill_between(fpr, tpr, alpha=0.4, color='skyblue', **step_kwargs)
    ax.set_xlabel('FP rate', fontsize=18)
    ax.set_ylabel('TP rate', fontsize=18)
    ax.set_ylim([0, 1.05])
    ax.set_xlim([0, 1])
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.legend(fontsize=14)
    ax.set_aspect('equal')



