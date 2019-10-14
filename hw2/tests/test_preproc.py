import unittest
from nose.tools import eq_
import collections
# import logging
# import numpy
from hw2_utils import preproc

LYRICS_DEV_CSV = '../tests_instructor/lyrics-mini.csv'
LYRICS_TEST_CSV = '../tests_instructor/lyrics-test-hidden.csv'
LYRICS_TRAIN_CSV = '../tests_instructor/lyrics-train.csv'

class TestPreproc(unittest.TestCase):
    # def setUp(self):
    #     global x_train, y_train, x_dev, y_dev, counts_dev, counts_train
    #     y_train, x_train = preproc.read_data(LYRICS_TRAIN_CSV)
    #     y_dev, x_dev = preproc.read_data(LYRICS_DEV_CSV)
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
        eq_(len(x_train[1144]), 124)

    @unittest.skip("does't use setup")
    def test_d1_1_bow_steve(self):
        train_labels, train_lyrics = preproc.read_data(LYRICS_TRAIN_CSV)

        # x (data) and y (label) vectors should be the same length
        eq_(len(train_lyrics), len(train_labels))

        # spot-check some counts:
        eq_(train_lyrics[4]['all'], 5)
        eq_(train_lyrics[41]['angels'], 1)
        eq_(train_lyrics[410]['angels'], 0)

        train_at_1144 = train_lyrics[1144]
        len_train_at_1144 = len(train_lyrics[1144])

        eq_(len(train_lyrics[1144]), 124)

    # 1: you were laughing laughing Ì¢cause youre doin it to me laughing
    # 2; # you were laughing laughing Ì¢cause youre doin it to me laughing one two
    # you were laughing youre doin it to me
    # {'you': 1, 'were': laughing youre doin it to me
    #@unittest.skip("does't use setup")
    def test_d1_1_bow_steve_nonascii(self):
        nonascii_txt = 'you were laughing laughing Ì¢cause youre doin it to me laughing'
        nonascii_bag = preproc.bag_of_words(nonascii_txt)
        print(nonascii_bag)

    def test_d1_2_agg(self):
        global x_dev

        print(x_dev)
        eq_(counts_dev['you'], 5542)
        eq_(len(counts_dev), 9006)
        eq_(counts_dev['money'], 92)

    @unittest.skip("does't use setup")
    def test_d1_2_agg_steve(self):
        _, bow_list = preproc.read_data(LYRICS_DEV_CSV)
        counts = preproc.aggregate_counts(bow_list)

        print(counts)

        eq_(counts['you'], 5542)
        eq_(counts['money'], 92)
        eq_(len(counts), 9006)

    @unittest.skip("test for prediction")
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

    @unittest.skip("does't use setup")
    def test_d1_3_oov_steve(self):
        _, lyrics_dev   = preproc.read_data(LYRICS_DEV_CSV)
        _, lyrics_train = preproc.read_data(LYRICS_TRAIN_CSV)

        counts_dev   = preproc.aggregate_counts(lyrics_dev)
        counts_train = preproc.aggregate_counts(lyrics_train)

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

    #@unittest.skip("does't use setup")
    def test_d1_3_oov_nonascii(self):
        # 1: you were laughing laughing Ì¢cause youre doin it to me laughing
        # 2; # you were laughing laughing Ì¢cause youre doin it to me laughing one two

        nonascii_txt1 = 'you were laughing laughing Ì¢cause youre doin it to me laughing'
        nonascii_txt2 = 'you were laughing laughing Ì¢cause youre doin it to me laughing one two'
        nonascii_txt3 = 'you were laughing laughing Ì¢cause canÌ¢t youre doin it to me laughing one two three'
        nonascii_txt4 = 'you were laughing laughing Ì¢cause youre doin it to me laughing one two three four'

        nonascii_bag1 = preproc.bag_of_words(nonascii_txt1)
        nonascii_bag2 = preproc.bag_of_words(nonascii_txt2)
        nonascii_bag3 = preproc.bag_of_words(nonascii_txt3)
        nonascii_bag4 = preproc.bag_of_words(nonascii_txt4)

        nonascii_list1 = [nonascii_bag1, nonascii_bag2]
        nonascii_list2 = [nonascii_bag3, nonascii_bag4]

        counts1 = preproc.aggregate_counts(nonascii_list1)
        counts2 = preproc.aggregate_counts(nonascii_list2)

        oov1 = preproc.compute_oov(counts1, counts2)
        oov2 = preproc.compute_oov(counts2, counts1)

        print(oov1)
        print(oov2)

    def test_d1_4_prune(self):
        global x_dev, counts_train

        x_train_pruned, vocab = preproc.prune_vocabulary(counts_train, x_train, 3)
        x_dev_pruned, vocab2 = preproc.prune_vocabulary(counts_train, x_dev, 3)

        #eq_(len(vocab), len(vocab2))
        #eq_(len(vocab), 11824)
        eq_(len(x_dev[95].keys()) - len(x_dev_pruned[95].keys()), 8)

    def test_d1_4_prune_steve_train(self):
        _, train_lyrics = preproc.read_data(LYRICS_TRAIN_CSV)
        counts_train = preproc.aggregate_counts(train_lyrics)
        train_lyrics_pruned, vocab = preproc.prune_vocabulary(counts_train, train_lyrics, 3)

        eq_(len(vocab), 11820) # 11824 contains instrumental, NA and corrupted lyrics

    #@unittest.skip("comment out setup")
    def test_d1_4_prune_steve_dev(self):
        _, dev_lyrics = preproc.read_data(LYRICS_DEV_CSV)
        dev_counts = preproc.aggregate_counts(dev_lyrics)
        dev_lyrics_pruned, vocab = preproc.prune_vocabulary(dev_counts, dev_lyrics, 3)

        vocab_sorted = collections.OrderedDict(sorted(vocab.items(), key=lambda t: t[0]))

        # On the 95th line in the dev file, we have the following words that were removed
        # Because the total count for these words in the entire document was < 3
        # heyyeah: 1, stands: 1, disco: 1, wasdancin: 1, diei: 1, diegonna: 1, electified: 1
        # yeahhey: 1, changin: 1, shaky: 1, funking: 1, diethey: 1

        # heyyeah: 1, stands: 1, disco: 2, wasdancin: 1, diei: 1, diegonna: 1, electified: 1
        # yeahhey: 2, changin: 2, shaky: 1, funking: 1, diethey: 1
        eq_(len(dev_lyrics[95].keys()) - len(dev_lyrics_pruned[95].keys()), 13)

        # How did we get 13?
        eq_(len(dev_lyrics[95].keys()) - len(dev_lyrics_pruned[95].keys()), 8)

if __name__ == '__main__':
    unittest.main()
