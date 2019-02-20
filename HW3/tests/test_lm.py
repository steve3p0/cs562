import nose
import torch
import os
from nose.tools import eq_, assert_almost_equals, assert_in, assert_true, assert_false, assert_greater, assert_less
from hw3_utils import vocab
from hw3_utils import lm

def setup_module():
    global corpus, c2i, i2c
    corpus = [l.strip() for l in open('data/towns_clean.txt')]
    c2i, i2c = vocab.build_vocab(corpus)

def test_d3_1_setup():
    global c2i, i2c
    
    mod = lm.NameGenerator(
        input_vocab_size=len(c2i),
        n_embedding_dims=25,
        n_hidden_dims=50,
        n_lstm_layers=1,
        output_vocab_size=len(c2i)
    )
    
    x = vocab.sentence_to_tensor("hello there", c2i, True)
    
    y_hat, hidden_state = mod(x, mod.init_hidden())
    
    # is the output the proper size?
    eq_(torch.Size([1,13,len(c2i)]), y_hat.shape) # counting <bos> and <eos>
    
    # do things add up to 1?
    sum_of_probs_at_first_pos = y_hat.squeeze()[0].exp().sum().item()
    assert_almost_equals(sum_of_probs_at_first_pos, 1.0, places=3)
    
def test_d3_2_training():
    global corpus, c2i
    
    model_fname = "deliverable_3.2.mod"
    
    # does the file exist?
    assert_true(os.path.exists(model_fname))
    
    # try loading saved model
    trained_model = torch.load(model_fname)
    
    # was it made correctly (as per the assignment's instructions)?
    eq_(trained_model.input_lookup.num_embeddings, len(c2i))
    eq_(trained_model.input_lookup.embedding_dim, 25)
    eq_(trained_model.lstm.num_layers, 1)
    eq_(trained_model.lstm.hidden_size, 50)
    
    # ask it for gibberish prob, make sure that's lower than actual town name prob
    gibberish_string = "asdflkjiopqutepoiuqrfm"
    good_fake_string = "Little Brockton-upon-Thyme"
    
    p_gibberish = lm.compute_prob(trained_model, gibberish_string, c2i)
    p_good = lm.compute_prob(trained_model, good_fake_string, c2i)
    
    p_gibberish_norm = p_gibberish / len(gibberish_string)
    p_good_norm = p_good / len(good_fake_string)
    
    # p_gibberish should be larger than p_good, since we're in negative log space
    assert_greater(p_gibberish_norm, p_good_norm)
    
def test_d3_3_sample():
    global c2i, i2c
    
    model_fname = "deliverable_3.2.mod"
    
    # does the file exist?
    assert_true(os.path.exists(model_fname))
    
    # try loading saved model
    trained_model = torch.load(model_fname)
    
    # try making a new town:
    new_town = lm.sample(trained_model, c2i, i2c)
    
    # verify that it's not too long:
    assert_less(len(new_town), 200)
    
    # make sure that it doesn't start with BOS_SYM
    assert_false(new_town[0] == vocab.BOS_SYM)
    
    # verify that its probability is lower than gibberish:
    gibberish_string = "asdflkjiopqutepoiuqrfm"
    p_gibberish = lm.compute_prob(trained_model, gibberish_string, c2i) / len(gibberish_string)
    p_good = lm.compute_prob(trained_model, new_town, c2i) / len(new_town)
    
    # negative log probs, so bigger is smaller
    assert_greater(p_gibberish, p_good)