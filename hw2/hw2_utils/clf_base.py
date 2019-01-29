from hw2_utils.constants import OFFSET
import numpy as np
from hw2_utils import preproc
from collections import Counter

# HELPER FUNCTION
def argmax(score_dict):
    """
    Find the 
    :param score_dict: A dict whose keys are labels and values are scores
    :returns: Top-scoring label
    :rtype: string
    """
    items = list(score_dict.items())
    items.sort()
    return items[np.argmax([i[1] for i in items])][0]


# deliverable 2.1
def make_feature_vector(base_features, label):
    """
    Take a dict of bag-of-words features and a label; return a dict of features, corresponding to f(x,y)
    
    :param base_features: Counter of base features
    :param label: label string
    :returns dict of features, f(x,y)
    :rtype: dict
    """
    #start michaels nonsense
    # base_features[OFFSET] = 1
    # fv = {}
    # for f in base_features:
    #     t = (label, f)
    #     fv[t] = base_features[f]
    #
    # return fv
    #end michaels nonsense
    fv = {}
    for f in base_features:
        t = (label, f)
        fv[t]= base_features[f]

    t = (label, OFFSET)
    fv[t] = 1

    return fv

# deliverable 2.2
def predict(base_features, weights, labels):
    """
    Simple linear prediction function y_hat = argmax_y \theta^T f(x,y)

    :param base_features: a dictionary of base features and counts (base features, NOT a full feature vector)
    :param weights: a defaultdict of features and weights. Features are tuples (label, base_feature)
    :param labels: a list of candidate labels
    :returns: top-scoring label, plus the scores of all labels
    :rtype: string, dict
    """
    # scores = dict()
    # feature_vect = make_feature_vector(base_features, labels)
    # for key, value in weights.items():
    #     for key_1, values_1 in feature_vect:
    #         if key == key_1:
    #             scores[key] += value * values_1
    # return argmax(scores), scores

    scores = dict()

    for label in labels:
        scores[label] = 0
        for word in base_features:
            scores[label] += base_features[word] * weights[label, word]

    print(scores)
    return argmax(scores), scores

# # deliverable 2.2
# def predict(base_features, weights, labels):
#
#     bf_agg = preproc.aggregate_counts(base_features)
#     #bf_agg = sum(base_features, Counter())
#
#     for l in labels:
#         total = 0
#         for x, y in weights.items():
#             if x == l:
#
#
#                 # x is era, y is word, weights[x, y] is weight
#                 weight = weights[x,y]
#                 count = bf_agg[y]
#                 total += weight * y
#
#         print(l + ": " + str(total))
#
#         #     print(x)
#         #     print(y)
#         #     break
#
#         # important_words = dict()
#         # for f in base_features:
#         #     #asdf
#         # for key in
#         #     #counts_train = preproc.aggregate_counts(x_train)
#
#         fv = make_feature_vector(base_features, l)
#
#         #{('1980s', 'test'): 1, ('1980s', 'case'): 2, ('1980s', '**OFFSET**'): 1}


    # accum = dict()
    # for
    #         if key in accum +=1
    #     else
    #         accum[key] = value

    # for x, y in weights.items():
    #     print(x)
    #     print(y)
    #     break
    # for x, y in base_features.items():
    #     print(x)
    #     print(y)
    #     break

    
def predict_all(x, weights, labels):
    """
    Predict the label for all instances in a dataset. For bulk prediction.
    
    :param x: iterable of base instances
    :param weights: defaultdict of weights
    :param labels: a list of candidate labels
    :returns: predictions for each instance
    :rtype: numpy array
    """
    y_hat = np.array([predict(x_i, weights, labels)[0] for x_i in x])
    return y_hat
    