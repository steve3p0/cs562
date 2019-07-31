import unittest
import nose
from nose.tools import eq_, assert_in
from hw3_utils import vocab
from collections import defaultdict

class TestVocab(unittest.TestCase):
    def setUp(self):
        global tiny_corpus
        tiny_corpus = ["This is a sentence.", "This is another sentence.", "Here is a third."]

    def test_d1_1_char_vocab(self):
        global tiny_corpus
        c2i, i2c = vocab.build_vocab(tiny_corpus)

        # are BOS_SYM and EOS_SYM in there?
        assert_in(vocab.BOS_SYM, c2i)
        assert_in(vocab.EOS_SYM, c2i)

        # does it map things correctly?

        t_idx = c2i["T"]
        eq_(i2c[t_idx], "T")

        # are they the same length?
        eq_(len(c2i), len(i2c))

        # is it exhaustive?
        all_seen = defaultdict(int)
        for doc in tiny_corpus:
            for c in list(doc):
                all_seen[c] = 1
        char_count = len(all_seen)

        # account for BOS_SYM and EOS_SYM
        char_count += 2

        eq_(char_count, len(c2i))

    def test_d1_2_sentence_vector(self):
        global tiny_corpus
        c2i, i2c = vocab.build_vocab(tiny_corpus)

        test_sentence = "Here is a sentence."

        sent_vec = vocab.sentence_to_vector(test_sentence, c2i)

        eq_(len(sent_vec), len(test_sentence))

        back_to_chars = [i2c[c] for c in sent_vec]
        eq_(test_sentence, ''.join(back_to_chars))

        # does the BOS/EOS padding work?
        with_padding = vocab.sentence_to_vector(test_sentence, c2i, True)
        eq_(len(with_padding), len(test_sentence) + 2)
        eq_(with_padding[0], c2i[vocab.BOS_SYM])
        eq_(with_padding[-1], c2i[vocab.EOS_SYM])

    def test_d1_3_sentence_tensor(self):
        global tiny_corpus
        c2i, i2c = vocab.build_vocab(tiny_corpus)

        s = "This is a sentence."
        s_tens = vocab.sentence_to_tensor(s, c2i)
        eq_(s_tens.shape[0], 1)
        eq_(s_tens.shape[1], len(s))
        eq_(len(s_tens.shape), 2)

        # does BOS/EOS padding work?
        with_padding = vocab.sentence_to_tensor(s, c2i, True)
        eq_(with_padding.shape[1], len(s) + 2)
        eq_(with_padding[0,0].item(), c2i[vocab.BOS_SYM])



    def test_d1_4_label_vocab(self):
        labels = ["eng","eng","spa","eng","deu"]
        l2i, i2l = vocab.build_label_vocab(labels)

        # does reversel lookup work?
        eng_idx = l2i["eng"]
        eq_(i2l[eng_idx], "eng")

        # are our regular and inverted mappings equally-sized?
        eq_(len(l2i), len(i2l))

        # are there the right number of entries in each?
        eq_(len(l2i), len(set(labels)))
        eq_(len(i2l), len(set(labels)))
    
