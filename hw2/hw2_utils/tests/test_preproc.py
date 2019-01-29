import unittest
from nose.tools import eq_
import logging
import numpy
from hw2_utils import preproc

class TestPreproc(unittest.TestCase):
    # def setUp(self):
    #     global x_train, y_train, x_dev, y_dev, counts_dev, counts_train
    #     y_train, x_train = preproc.read_data('lyrics-train.csv')
    #     y_dev, x_dev = preproc.read_data('lyrics-dev.csv')
    #
    #     counts_train = preproc.aggregate_counts(x_train)
    #     counts_dev = preproc.aggregate_counts(x_dev)

    def test_d1_1_bow(self):
        global x_train, y_train
        # x (data) and y (label) vectors should be the same length
        eq_(len(x_train), len(y_train))

        # spot-check some counts:
        eq_(x_train[4]['all'], 5)
        eq_(x_train[41]['angels'], 1)
        eq_(x_train[410]['angels'], 0)

        train_at_1144 = x_train[1144]
        len_train_at_1144 = len(x_train[1144])

        for ind, bag in enumerate(x_train):
            if len(bag) == 124:
                print(ind, end="")
                print(": ", end="")
                print(bag)

        eq_(len(x_train[1144]), 124)

    def test_d1_2_agg(self):
        global x_dev

        print(x_dev)
        eq_(counts_dev['you'], 5542)
        eq_(len(counts_dev), 9006)
        eq_(counts_dev['money'], 92)

    @unittest.skip("does't use setup")
    def test_d1_2_agg_steve(self):
        _, bow_list = preproc.read_data('lyrics-dev_steve.csv')
        counts = preproc.aggregate_counts(bow_list)

        print(counts)

        eq_(counts['you'], 5542)
        eq_(counts['money'], 92)
        eq_(len(counts), 9006)

    def test_for_predict(self):
        global x_dev

        print('Count of money: ' + str(counts_dev['money']))
        print('Count of name: ' + str(counts_dev['name']))
        print('Count of tonight: ' + str(counts_dev['tonight']))
        print('Count of man: ' + str(counts_dev['man']))
        print('Count of fly: ' + str(counts_dev['fly']))

    def test_d1_3_oov(self):
        global counts_train, counts_dev
        eq_(len(preproc.compute_oov(counts_dev, counts_train)), 2677)
        eq_(len(preproc.compute_oov(counts_train, counts_dev)), 30459) # ) 30442  17

    def test_d1_3_oov_steve(self):
        global x_train, y_train, x_dev, y_dev, counts_dev, counts_train
        _, x_dev   = preproc.read_data('lyrics-dev.csv')
        _, x_train = preproc.read_data('lyrics-train.csv')

        counts_dev   = preproc.aggregate_counts(x_dev)
        counts_train = preproc.aggregate_counts(x_train)

        oov_dev   = preproc.compute_oov(counts_dev,   counts_train)
        oov_train = preproc.compute_oov(counts_train, counts_dev)

        #oov_dev.remove(None)
        #oov_train.remove(None)

        list_oov_dev   = list(oov_dev)
        list_oov_train = list(oov_train)

        list_oov_dev.sort()
        list_oov_train.sort()

        set_oov_dev = set(list_oov_dev)
        set_oov_train = set(list_oov_train)

        oov_diff_dev_wo_train = set_oov_dev - set_oov_train
        oov_diff_train_wo_dev = set_oov_train - set_oov_dev
        # print(oov_diff)

        eq_(len(oov_dev), 2677)
        eq_(len(oov_train), 30459) # ) 30442

    def test_d1_4_prune(self):
        global x_dev, counts_train

        x_train_pruned, vocab = preproc.prune_vocabulary(counts_train, x_train, 3)
        x_dev_pruned, vocab2 = preproc.prune_vocabulary(counts_train, x_dev, 3)

        eq_(len(vocab), len(vocab2))
        eq_(len(vocab), 11824)
        eq_(len(x_dev[95].keys()) - len(x_dev_pruned[95].keys()), 8)

    @unittest.skip("does't use setup")
    def test_d1_4_prune_steve(self):
        _, x_train = preproc.read_data('lyrics-train.csv')
        counts_train = preproc.aggregate_counts(x_train)
        x_train_pruned, vocab = preproc.prune_vocabulary(counts_train, x_train, 3)

        f = open("vocab.txt", "w")
        f.write(str(vocab))
        f.close()

        # f = open("prune_3.txt", "w")
        # f.write(str(x_train_pruned))
        # f.close()

        #eq_(len(vocab), len(vocab2))
        eq_(len(vocab), 11824)
        #eq_(len(x_dev[95].keys()) - len(x_dev_pruned[95].keys()), 8)

if __name__ == '__main__':
    unittest.main()
