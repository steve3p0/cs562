import unittest
import nose
import torch
import pandas as pd
import numpy as np
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

    # Put all the lang_id model code here to test.
    # Jupyter keeps producing the following error:
    #   RuntimeError: Trying to backward through the graph a second time,
    #   but the buffers have already been freed.
    #   Specify retain_graph=True when calling backward the first time.
    #
    # This error is NOT reproduced here in the unittest.
    #
    # This error in not guaranteed to be raised, as per discussion here.
    #   https://discuss.pytorch.org/t/understanding-graphs-and-state/224/2?u=kharshit
    # I tried implementing some of the workarounds to no avail, but the same code works here
    #
    # Futhermore, the multinomial test code in the Jupyter notebook does not raise this error.
    def test_train_model(self):

        # Adding prefix _ to local variables
        # Noticed some variation in the scores every time I run it.
        # Don't want to pollute my variables with globals when running all tests
        _bi_text = pd.read_csv("../../data/sentences_bilingual.csv")
        _bi_text_train, _bi_text_test = train_test_split(_bi_text, test_size=0.2)
        _c2i, _i2c = vocab.build_vocab(bi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(bi_text.lang.values)

        _li = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        _trained_model = lang_id.train_model(
            model=_li,
            n_epochs=1,
            training_data=_bi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        )

        _trained_model(vocab.sentence_to_tensor("this is a sentence", _c2i))
        _trained_model(vocab.sentence_to_tensor("quien estas", _c2i))

        _acc, _y_hat = lang_id.eval_acc(_trained_model, _bi_text_test, _c2i, _i2c, _l2i, _i2l)
        print(f"Trained Accuracy: {_acc}")

        _untrained = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        _acc_untrained, _y_hat_untrained = lang_id.eval_acc(_untrained, _bi_text_test, _c2i, _i2c, _l2i, _i2l)
        print(f"Untrained Accuracy: {_acc_untrained}")

        assert_greater(_acc, 0.89)

    def test_untrained_model(self):
        # Adding prefix _ to local variables
        # Noticed some variation in the scores every time I run it.
        # Don't want to pollute my variables with globals when running all tests
        _bi_text = pd.read_csv("../../data/sentences_bilingual.csv")
        _bi_text_train, _bi_text_test = train_test_split(_bi_text, test_size=0.2)

        _c2i, _i2c = vocab.build_vocab(_bi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(_bi_text.lang.values)

        _untrained = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=2
        )

        _acc_untrained, _y_hat_untrained = lang_id.eval_acc(_untrained, _bi_text_test, _c2i, _i2c, _l2i, _i2l)
        print(f"Untrained Accuracy: {_acc_untrained}")

        pred_label_list = np.asarray(_y_hat_untrained)
        pd.options.mode.chained_assignment = None
        _bi_text_test["predicted"] = pred_label_list
        _bi_text_test = _bi_text_test[["sentence", "lang", "predicted"]]
        _bi_text_test.to_csv("../../data/deliverable_2.4_untrained.csv", index=False)

        assert_greater(_acc_untrained, 0.4)
        assert_less(_acc_untrained, 0.6)

    def test_train_model_untrained_multi(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        _untrained_multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=5
        )

        acc_untrained_multi, y_hat_untrained_multi = lang_id.eval_acc(_untrained_multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)
        print(f"Untrained Multi Accuracy: {acc_untrained_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_untrained_multi))

        cm = confusion_matrix(y_multi, y_hat_untrained_multi)
        cm

        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])

        assert_greater(acc_untrained_multi, 0.4)
        assert_less(acc_untrained_multi, 0.6)

    #BASELINE
    def test_train_model_multi_baseline(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=1,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        #reload(lang_id);
        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])

        assert_greater(acc_multi, 0.60)

    #2 Modifed Params

    def test_train_model_multi_lstm2(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=2,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=1,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        # reload(lang_id);
        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])
        assert_greater(acc_multi, 0.60)

    def test_train_model_multi_lstm5(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=5,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=1,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        # reload(lang_id);
        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])
        assert_greater(acc_multi, 0.60)

    def test_train_model_multi_epoch5(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=1,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=5,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])
        assert_greater(acc_multi, 0.60)

    def test_train_model_embed2_hidden2(self):

        # Adding prefix _ to local variables
        # Noticed some variation in the scores every time I run it.
        # Don't want to pollute my variables with globals when running all tests
        _bi_text = pd.read_csv("../../data/sentences_bilingual.csv")
        _bi_text_train, _bi_text_test = train_test_split(_bi_text, test_size=0.2)
        _c2i, _i2c = vocab.build_vocab(bi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(bi_text.lang.values)

        _li = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=2,
            hidden_dims=2,
            lstm_layers=1,
            output_class_n=2
        )

        _trained_model = lang_id.train_model(
            model=_li,
            n_epochs=1,
            training_data=_bi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        )

        _trained_model(vocab.sentence_to_tensor("this is a sentence", _c2i))
        _trained_model(vocab.sentence_to_tensor("quien estas", _c2i))

        _acc, _y_hat = lang_id.eval_acc(_trained_model, _bi_text_test, _c2i, _i2c, _l2i, _i2l)
        print(f"Trained Accuracy: {_acc}")

        pred_label_list = np.asarray(_y_hat)
        pd.options.mode.chained_assignment = None

        pred_label_list = np.asarray(_y_hat)
        pd.options.mode.chained_assignment = None
        _bi_text_test["predicted"] = pred_label_list
        _bi_text_test = _bi_text_test[["sentence", "lang", "predicted"]]
        _bi_text_test.to_csv("../../data/deliverable_2.4.csv", index=False)

        assert_greater(_acc, 0.89)

    def test_train_model_multi_lstm5_epoch5(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=10,
            hidden_dims=20,
            lstm_layers=5,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=5,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")
        assert_greater(acc_multi, 0.60)

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        # reload(lang_id);
        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])

    def test_train_model_multi_embed20_hidden20_lstm5_epoch5(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=20,
            hidden_dims=20,
            lstm_layers=5,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=5,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")
        assert_greater(acc_multi, 0.60)

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        # reload(lang_id);
        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])

    def test_train_model_multi_embed20_hidden40(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=20,
            hidden_dims=40,
            lstm_layers=1,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=1,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        #reload(lang_id);
        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])

        assert_greater(acc_multi, 0.60)

    def test_train_model_multi_embed200_hidden200_epoch5(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=200,
            hidden_dims=200,
            lstm_layers=1,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=5,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])
        assert_greater(acc_multi, 0.95)

    def test_train_model_multi_embed200_hidden200_lstm2_epoch5(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=200,
            hidden_dims=200,
            lstm_layers=2,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=5,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])
        assert_greater(acc_multi, 0.95)


    def test_train_model_multi_embed100_hidden100_lstm4_epoch5(self):
        multi_text = pd.read_csv("../../data/sentences_multilingual.csv")
        multi_text_train, multi_text_test = train_test_split(multi_text, test_size=0.2)

        multi_text.groupby('lang').count()
        multi_text_train.groupby('lang').count()

        _c2i, _i2c = vocab.build_vocab(multi_text.sentence.values)
        _l2i, _i2l = vocab.build_label_vocab(multi_text.lang.values)

        multi_class = lang_id.LangID(
            input_vocab_n=len(_c2i),
            embedding_dims=100,
            hidden_dims=100,
            lstm_layers=4,
            output_class_n=5
        )

        lang_id.train_model(
            model=multi_class,
            n_epochs=5,
            training_data=multi_text_train,
            c2i=_c2i, i2c=_i2c,
            l2i=_l2i, i2l=_i2l
        );
        print("done")

        acc_multi, y_hat_multi = lang_id.eval_acc(multi_class, multi_text_test, _c2i, _i2c, _l2i, _i2l)

        # Jupyter reported Accuracy: 0.6954
        # Run 1: Accuracy: 0.6954
        print(f"Accuracy: {acc_multi}")

        from sklearn.metrics import classification_report, confusion_matrix
        y_multi = multi_text_test.lang.values
        print(classification_report(y_multi, y_hat_multi))

        cm = confusion_matrix(y_multi, y_hat_multi)
        cm

        lang_id.pretty_conf_matrix(cm, ['deu', 'eng', 'fra', 'ita', 'spa'])
        assert_greater(acc_multi, 0.95)
