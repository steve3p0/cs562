from hw2_utils.constants import OFFSET
from hw2_utils import clf_base, evaluation

import numpy as np
from collections import defaultdict, Counter
from itertools import chain
import math

from hw2_utils import preproc
from hw2_utils import clf_base

# deliverable 3.1
def get_corpus_counts(x,y,label):
    """
    Compute corpus counts of words for all documents with a given label.

    :param x: list of counts, one per instance
    :param y: list of labels, one per instance
    :param label: desired label for corpus counts
    :returns: defaultdict of corpus counts
    :rtype: defaultdict

    """

    label_docs = list(Counter())

    for lyrics, lbl in zip(x, y):
        if lbl == label:
            label_docs.append(lyrics)

    counts = sum(label_docs, Counter())

    return counts

def estimate_pxy(x,y,label,smoothing,vocab):
    """
    Compute smoothed log-probability P(word | label) for a given label. (eq. 2.30 in Eisenstein, 4.14 in J&M)

    :param x: list of counts, one per instance
    :param y: list of labels, one per instance
    :param label: desired label
    :param smoothing: additive smoothing amount
    :param vocab: list of words in vocabulary
    :returns: defaultdict of log probabilities per word
    :rtype: defaultdict of log probabilities per word

    """

    # Create references to parameters that match formula and algorithm in 4.14 in J&M
    # Yes, it violates python naming conventions, but understanding Naive Bayes is more important
    D = x
    C = y
    c = label
    V = vocab
    V[OFFSET] = 0.0
    # |V| = size of vocabulary, that took a while to figure out,
    #       I vaguely remember now it being mentioned in class
    V_size = len(vocab)

    counts = get_corpus_counts(D, C, c)
    counts[OFFSET] = 0.0
    sum_counts = sum(counts.values())

    loglikelihood = dict.fromkeys(list(V.keys()), 0.0)
    #loglikelihood[OFFSET] = 0.0

    for w in V:
        if w in counts:
            count_w = counts[w]
        else:
            count_w = 0

        # THE ABOVE MENTIONED BOOKS DO NOT TELL YOU:
        # When using a smoothing parameter, multiply V_size or |V| by the smoothing parameter
        # p_wi = (count_w + smoothing) / (sum_counts + V_size)
        p_wi = (count_w + smoothing) / (sum_counts + (smoothing * V_size))
        log_p_wi = np.log(p_wi)
        loglikelihood[w] = log_p_wi
    return loglikelihood

# # deliverable 3.2
# def estimate_pxy(x,y,label,smoothing,vocab):
#     """
#     Compute smoothed log-probability P(word | label) for a given label. (eq. 2.30 in Eisenstein, 4.14 in J&M)
#
#     :param x: list of counts, one per instance
#     :param y: list of labels, one per instance
#     :param label: desired label
#     :param smoothing: additive smoothing amount
#     :param vocab: list of words in vocabulary
#     :returns: defaultdict of log probabilities per word
#     :rtype: defaultdict of log probabilities per word
#
#     """
#
#     # Create references to parameters that match formula and algorithm in 4.14 in J&M
#     # Yes, it violates python naming conventions, but understanding Naive Bayes is more important
#     D = x
#     C = y
#     c = label
#     V = vocab
#     # |V| = size of vocabulary, that took a while to figure out,
#     #       I vaguely remember now it being mentioned in class
#     V_size = len(vocab)
#
#     counts = get_corpus_counts(D, C, c)
#     #counts[OFFSET] = 0
#     sum_counts = sum(counts.values())
#
#     Ndoc = len(D)
#     Nc = len(counts)
#
#     loglikelihood = dict.fromkeys(list(V.keys()), 0.0)
#
#     for w in V:
#         if w in counts:
#             count_w = counts[w]
#         else:
#             count_w = 0
#         # THE ABOVE MENTIONED BOOKS DO NOT TELL YOU:
#         # When using a smoothing parameter, multiply V_size or |V| by the smoothing parameter
#         #p_wi = (count_w + smoothing) / (sum_counts + V_size)
#         p_wi = (count_w + smoothing) / (sum_counts + (smoothing * V_size))
#         #p_wi = (count_w + smoothing) / (sum_counts + (smoothing))
#         log_p_wi = np.log(p_wi)
#         #loglikelihood[w] = log_p_wi
#
#     #loglikelihood[OFFSET] = np.log(Nc / Ndoc)
#     #loglikelihood[OFFSET] = 1
#     #loglikelihood[OFFSET] = 0.0
#     #loglikelihood[OFFSET] = smoothing
#
#     return loglikelihood

# deliverable 3.3
def estimate_nb(x,y,smoothing):
    """
    Estimate a naive bayes model

    :param x: list of dictionaries of base feature counts
    :param y: list of labels
    :param smoothing: smoothing constant
    :returns: weights, as a default dict where the keys are (label, word) tuples and values are smoothed log-probs of P(word|label)
    :rtype: defaultdict 

    """
    
    labels = set(y)
    counts = defaultdict(float)
    doc_counts = defaultdict(float)

    # Create references to parameters that match formula and algorithm in 4.14 in J&M
    # Yes, it violates python naming conventions, but understanding Naive Bayes is more important
    D = x           # all documents
    C = labels           # Labels or class as it is known in 4.14 in J&M
    V = Counter()   # Vocabulary counter
    V_size = 0     # |V| = size of vocabulary, initialize to 0

    weights = defaultdict()
    for c in C:
        V = preproc.aggregate_counts(D)

        p_xy = estimate_pxy(D, C, c, smoothing, V)
        weights.update(clf_base.make_feature_vector(p_xy, c))

        # for w, p in p_xy.items():
        #     key = (c, w)
        #     weights[key] = p

        # Don't really understand how the OFFSET is related to Naive Bayes,
        #key = (c, OFFSET)
        #weights[key] = smoothing

    return weights

# deliverable 3.4
def find_best_smoother(x_tr,y_tr,x_dv,y_dv,smoothers):
    """
    Find the smoothing value that gives the best accuracy on the dev data

    :param x_tr: training instances
    :param y_tr: training labels
    :param x_dv: dev instances
    :param y_dv: dev labels
    :param smoothers: list of smoothing values
    :returns: best smoothing value, scores
    :rtype: float, dict mapping smoothing value to score
    """

    raise NotImplementedError
    