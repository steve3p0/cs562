import unittest
import nose
import torch
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from nose.tools import eq_, assert_almost_equals, assert_in, assert_greater, assert_less
from hw3_utils import vocab
from hw3_utils import lang_id

class TestLangID(unittest.TestCase):
    def setUp(self):
        global bi_text, bi_text_train, bi_text_test, bt_c2i, bt_i2c, bt_l2i, bt_i2l

        bi_text = pd.read_csv("../../data/sentences_bilingual.csv")
        bt_c2i, bt_i2c = vocab.build_vocab(bi_text.sentence.values)
        bt_l2i, bt_i2l = vocab.build_label_vocab(bi_text.lang.values)
        bi_text_train, bi_text_test = train_test_split(bi_text, test_size=0.2)

    def test_d2_1_forward(self):
        global bt_c2i

        li = lang_id.LangID(
            input_vocab_n=len(bt_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        #out = li(vocab.sentence_to_tensor("this is a sentence", bt_c2i))
        t = vocab.sentence_to_tensor("this is a sentence", bt_c2i)
        out = li(t)

        eq_(out.shape[0], 2)

    def test_d2_2_predict_one(self):
        global bg_c2i, bt_i2l

        li = lang_id.LangID(
            input_vocab_n=len(bt_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        out = lang_id.predict_one(li, "this is a sentence", bt_c2i, bt_i2l)

        assert_in(out, bt_i2l.values())

    def test_d2_3_eval_acc(self):
        global bi_text_test, bt_c2i, bt_i2c, bt_l2i, bt_i2l

        untrained = lang_id.LangID(
            input_vocab_n=len(bt_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        # should be ≈50% accuracy
        acc_untrained, y_hat_untrained = lang_id.eval_acc(untrained, bi_text_test, bt_c2i, bt_i2c, bt_l2i, bt_i2l)
        assert_greater(acc_untrained, 0.4)
        assert_less(acc_untrained, 0.6)

        eq_(len(y_hat_untrained), len(bi_text_test))

    def test_train_model(self):

        _bi_text = pd.read_csv("../../data/sentences_bilingual.csv")
        _c2i, _i2c = vocab.build_vocab(bi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(bi_text.lang.values)

        _li = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        trained_model = lang_id.train_model(
            model=_li,
            n_epochs=1,
            training_data=bi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        )

        trained_model(vocab.sentence_to_tensor("this is a sentence", _c2i))
        trained_model(vocab.sentence_to_tensor("quien estas", _c2i))

        _acc, _y_hat = lang_id.eval_acc(trained_model, bi_text_test, _c2i, _i2c, _l2i, _i2l)
        print(f"Trained Accuracy: {_acc}")

        _untrained = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        _acc_untrained, _y_hat_untrained = lang_id.eval_acc(_untrained, bi_text_test, _c2i, _i2c, _l2i, _i2l)
        print(f"Untrained Accuracy: {_acc_untrained}")

        assert_greater(_acc, 0.89)
