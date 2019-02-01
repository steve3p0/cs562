import collections
from collections import Counter

import pandas as pd
import numpy as np
import re
import nltk

# deliverable 1.1
def bag_of_words(text):
    """
    Count the number of word occurrences for a given document
    
    :param text: a document, as a single string
    :returns: a Counter representing a single document's word counts
    :rtype: Counter
    """

    txt = text.strip()
    txt = text.replace("Ì¢", '')
    #empty_lyrics = []
    empty_lyrics = ['instrumental', 'NA', '']
    if txt in empty_lyrics:
        return collections.Counter()
    bag = collections.Counter(re.findall(r'\w+', txt))

    return bag

# deliverable 1.2
def aggregate_counts(bags_of_words):
    """
    Aggregate bag-of-words word counts across an Iterable of documents into a single bag-of-words.
    
    :param bags_of_words: an iterable of bags of words, produced from the bag_of_words() function above
    :returns: an aggregated bag of words for the whole corpus
    :rtype: Counter
    """
    return sum(bags_of_words, Counter())

# deliverable 1.3
def compute_oov(bow1, bow2):
    """
    Return a set of words that appears in bow1, but not bow2

    :param bow1: a bag of words
    :param bow2: a bag of words
    :returns: the set of words in bow1, but not in bow2
    :rtype: set
    """

    oov = set()
    for key in bow1.keys():
        if key not in bow2:
            oov.add(key)

    return oov

# deliverable 1.4 - BY REFERENCE VERSION
# This one is suprisingly fast
def prune_vocabulary(training_counts, target_data, min_counts):
    """
    Prune target_data to only include words that occur at least min_counts times in training_counts

    :param training_counts: aggregated Counter for the training data
    :param target_data: list of Counters containing dev bow's
    :returns: new list of Counters, with pruned vocabulary
    :returns: list of words in pruned vocabulary
    :rtype list of Counters, set
    """

    import copy

    pruned_counts = copy.deepcopy(training_counts)
    pruned_data   = copy.deepcopy(target_data)

    pruned_counts = {k: v for k, v in pruned_counts.items() if v >= (min_counts + 1)}

    for c in pruned_data:
        for word in list(c):
            if word not in pruned_counts:
                #print(c)
                #print("deleting word: " + word)
                del c[word]
                #print(c)
                #print()

    return pruned_data, pruned_counts

# # deliverable 1.4
# def prune_vocabulary(training_counts, target_data, min_counts):
#     """
#     Prune target_data to only include words that occur at least min_counts times in training_counts
#
#     :param training_counts: aggregated Counter for the training data
#     :param target_data: list of Counters containing dev bow's
#     :returns: new list of Counters, with pruned vocabulary
#     :returns: list of words in pruned vocabulary
#     :rtype list of Counters, set
#     """
#
#     import copy
#     pruned_word_list = []
#     pruned_cntr_list = copy.deepcopy(target_data)
#
#     for word in training_counts:
#         if training_counts[word] >= min_counts:
#             pruned_word_list.append(word)
#
#     for c in pruned_cntr_list:
#         for word in list(c):
#             if word not in pruned_word_list:
#                 del c[word]
#
#     return pruned_cntr_list, pruned_word_list
    

# Helper functions

def read_data(fname, label='Era', preprocessor=bag_of_words):
    df = pd.read_csv(fname)
    return (df[label].values, [preprocessor(string) for string in df['Lyrics'].values])
    
def oov_rate(bow1, bow2):
    return len(compute_oov(bow1, bow2)) / len(bow1.keys())