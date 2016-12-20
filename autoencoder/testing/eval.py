'''
Created on Dec, 2016

@author: hugo

'''
from __future__ import absolute_import

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from utils import *

def plot_tsne(doc_codes, doc_labels, classes_to_visual):
    markers = ["o", "v", "8", "s", "p", "*", "h", "H", "+", "x", "D"]

    C = len(classes_to_visual)
    while True:
        if C <= len(markers):
            break
        markers += markers

    class_ids = dict(zip(classes_to_visual, range(C)))

    classes_to_visual_set = set(classes_to_visual)
    codes, labels = zip(*[(code, doc_labels[doc]) for doc, code in doc_codes.items() if classes_to_visual_set.intersection(doc_labels[doc])])
    # codes, labels = zip(*[(code, doc_labels[doc]) for doc, code in doc_codes.items() if doc_labels[doc] in classes_to_visual and (doc_labels[doc] == 1 or np.random.uniform(0,1) > .8)])
    X = np.r_[list(codes)]
    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
    np.set_printoptions(suppress=True)
    X = tsne.fit_transform(X)

    plt.figure(figsize=(10, 10), facecolor='white')

    for c in classes_to_visual:
        # idx = np.array(labels) == c
        idx = get_indices(labels, c)
        plt.plot(X[idx, 0], X[idx, 1], linestyle='None', alpha=0.6, marker=markers[class_ids[c]],
                        markersize=6, label=c)
    legend = plt.legend(loc='upper center', shadow=True)
    plt.title("tsne")
    plt.savefig('tsne.png')
    plt.show()


def visualize_pca_2d(doc_codes, doc_labels, classes_to_visual):
    """
        Visualize the input data on a 2D PCA plot. Depending on the number of components,
        the plot will contain an X amount of subplots.
        @param doc_codes:
        @param number_of_components: The number of principal components for the PCA plot.
    """

    # markers = ["p", "s", "h", "H", "+", "x", "D"]
    markers = ["o", "v", "8", "s", "p", "*", "h", "H", "+", "x", "D"]

    C = len(classes_to_visual)
    while True:
        if C <= len(markers):
            break
        markers += markers

    class_ids = dict(zip(classes_to_visual, range(C)))

    classes_to_visual_set = set(classes_to_visual)
    codes, labels = zip(*[(code, doc_labels[doc]) for doc, code in doc_codes.items() if classes_to_visual_set.intersection(doc_labels[doc])])
    # codes, labels = zip(*[(code, doc_labels[doc]) for doc, code in doc_codes.items() if doc_labels[doc] in classes_to_visual and (doc_labels[doc] == 1 or np.random.uniform(0,1) > .8)])

    X = np.r_[list(codes)]
    X = PCA(n_components=3).fit_transform(X)
    plt.figure(figsize=(10, 10), facecolor='white')

    x_pc, y_pc = 1, 2

    for c in classes_to_visual:
        # idx = np.array(labels) == c
        idx = get_indices(labels, c)
        plt.plot(X[idx, x_pc], X[idx, y_pc], linestyle='None', alpha=0.6, marker=markers[class_ids[c]],
                        markersize=6, label=c)
        # plt.legend(c)
    plt.title('Projected on the first 2 PCs')
    plt.xlabel('PC %s' % x_pc)
    plt.ylabel('PC %s' % y_pc)
    legend = plt.legend(loc='upper center', shadow=True)
    plt.savefig('pca_2d.png')
    plt.show()

def get_indices(labels, c):
    idx = np.zeros(len(labels), dtype=bool)
    for i in range(len(labels)):
        tmp = [labels[i]] if not isinstance(labels[i], list) else labels[i]
        if c in tmp:
            idx[i] = True
    return idx

if __name__ == '__main__':
    # 20news
    # visualize_pca_2d(load_json(sys.argv[1]), load_json(sys.argv[2]), ["rec.sport.hockey", "comp.graphics", "sci.crypt",
                                                                # "soc.religion.christian", "talk.politics.mideast",
                                                                # "talk.politics.guns"])

    plot_tsne(load_json(sys.argv[1]), load_json(sys.argv[2]), ["rec.sport.hockey", "comp.graphics", "sci.crypt",
                                                                "soc.religion.christian", "talk.politics.mideast",
                                                                "talk.politics.guns"])

    # # 8k
    # plot_tsne(load_json(sys.argv[1]), load_json(sys.argv[2]), [0, 1])
    # plot_tsne(load_json(sys.argv[1]), load_json(sys.argv[2]), ['1143155', '889936', '1362719', '700733', '730708'])
    # visualize_pca_2d(load_json(sys.argv[1]), load_json(sys.argv[2]), ['2006', '2008', '2010', '2012'])

