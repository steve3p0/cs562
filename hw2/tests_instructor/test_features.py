from nose.tools import eq_, assert_almost_equals, assert_greater_equal
from hw2_utils import preproc, clf_base, constants, hand_weights, evaluation, naive_bayes, features
import numpy as np

def setup_module():
    global vocab, label_set, x_tr_pruned

    y_tr,x_tr = preproc.read_data('lyrics-train.csv',preprocessor=preproc.bag_of_words)
    labels = set(y_tr)

    counts_tr = preproc.aggregate_counts(x_tr)

    x_tr_pruned, vocab = preproc.prune_vocabulary(counts_tr, x_tr, 10)

    label_set = sorted(list(set(y_tr)))

def test_d4_1_token_type_ratio():
    global x_tr_pruned
    
    ratios = [features.get_token_type_ratio(x_tr_pruned[i]) for i in range(5)]
    assert_almost_equals(ratios[0], 5.08333, places=2)
    assert_almost_equals(ratios[1], 2.6, places=2)
    assert_almost_equals(ratios[2], 1.91139, places=2)
    assert_almost_equals(ratios[3], 2.31884, places=2)
    assert_almost_equals(ratios[4], 6.18868, places=2)
    
    
def test_d4_2_discretize():
    global x_tr_pruned
    
    eq_(len(x_tr_pruned[0]), 60) # before adding the indicator features
    x_tr_new = [features.concat_ttr_binned_features(dict(x_i)) for x_i in x_tr_pruned]
    eq_(len(x_tr_new[0]), 67)
    eq_(x_tr_new[1][constants.TTR_TWO], 1)
    eq_(x_tr_new[2][constants.TTR_ONE], 1)
    eq_(x_tr_new[3][constants.TTR_TWO], 1)

