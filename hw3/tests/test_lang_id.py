import nose
import torch
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from nose.tools import eq_, assert_almost_equals, assert_in, assert_greater, assert_less
from hw3_utils import vocab
from hw3_utils import lang_id

def setup_module():
    global bi_text, bi_text_train, bi_text_test, bt_c2i, bt_i2c, bt_l2i, bt_i2l
    
    bi_text = pd.read_csv("./data/sentences_bilingual.csv")
    bt_c2i, bt_i2c = vocab.build_vocab(bi_text.sentence.values)
    bt_l2i, bt_i2l = vocab.build_label_vocab(bi_text.lang.values)
    bi_text_train, bi_text_test = train_test_split(bi_text, test_size=0.2)
    
def test_d2_1_forward():    
    global bt_c2i
    
    li = lang_id.LangID(
        input_vocab_n=len(bt_c2i), 
        embedding_dims=10,
        hidden_dims=20,
        lstm_layers=1,
        output_class_n=2
    )
    
    out = li(vocab.sentence_to_tensor("this is a sentence", bt_c2i))
    
    eq_(out.shape[0], 2)
    
def test_d2_2_predict_one():
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
    
def test_d2_3_eval_acc():
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
    
    
    