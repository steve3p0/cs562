from nose.tools import eq_

from hw2_utils import preproc

import nose

def setup_module():
    global x_train, y_train, x_dev, y_dev, counts_dev, counts_train
    y_train, x_train = preproc.read_data('lyrics-train.csv')
    y_dev, x_dev = preproc.read_data('lyrics-dev.csv')
    
    counts_train = preproc.aggregate_counts(x_train)
    counts_dev = preproc.aggregate_counts(x_dev)
    
    
def test_d1_1_bow():
    global x_train, y_train
    # x (data) and y (label) vectors should be the same length
    eq_(len(x_train), len(y_train))
    
    # spot-check some counts:
    eq_(x_train[4]['all'], 5)
    eq_(x_train[41]['angels'], 1)
    eq_(x_train[410]['angels'], 0)
    eq_(len(x_train[1144]), 124)
    
def test_d1_2_agg():
    global x_dev

    eq_(counts_dev['you'],5542)
    eq_(len(counts_dev),9006)
    eq_(counts_dev['money'],92)

def test_d1_3_oov():
    global counts_train, counts_dev
    eq_(len(preproc.compute_oov(counts_dev,counts_train)),2677)
    eq_(len(preproc.compute_oov(counts_train,counts_dev)),30459)

def test_d1_4_prune():
    global x_dev, counts_train

    x_train_pruned, vocab = preproc.prune_vocabulary(counts_train,x_train,3)
    x_dev_pruned, vocab2 = preproc.prune_vocabulary(counts_train,x_dev,3)

    eq_(len(vocab),len(vocab2))
    eq_(len(vocab),11824)
    eq_(len(x_dev[95].keys())-len(x_dev_pruned[95].keys()),8)
