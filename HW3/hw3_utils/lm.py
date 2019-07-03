import torch
import torch.nn as nn
import random
import numpy as np
import matplotlib.pyplot as plt
import itertools
from hw3_utils import vocab

import torch.nn.functional as F

class NameGenerator(nn.Module):
    def __init__(self, input_vocab_size, n_embedding_dims, n_hidden_dims, n_lstm_layers, output_vocab_size):
        """
        Initialize our name generator, following the equations laid out in the assignment. In other words,
        we'll need an Embedding layer, an LSTM layer, a Linear layer, and LogSoftmax layer. 
        
        Note: Remember to set batch_first=True when initializing your LSTM layer!

        Also note: When you build your LogSoftmax layer, pay attention to the dimension that you're 
        telling it to run over!
        """
        super(NameGenerator, self).__init__()
        self.lstm_dims = n_hidden_dims
        self.lstm_layers = n_lstm_layers

        self.embed_dims = n_embedding_dims

        self.input_lookup = nn.Embedding(num_embeddings=input_vocab_size, embedding_dim=n_embedding_dims)
        self.lstm = nn.LSTM(input_size=n_embedding_dims, hidden_size=n_hidden_dims, num_layers=n_lstm_layers, batch_first=True)
        self.output = nn.Linear(in_features=n_hidden_dims, out_features=output_vocab_size)
        self.softmax = nn.LogSoftmax(dim=2)
        
    def forward(self, history_tensor, prev_hidden_state):
        """
        Given a history, and a previous timepoint's hidden state, predict the next character. 
        
        Note: Make sure to return the LSTM hidden state, so that we can use this for
        sampling/generation in a one-character-at-a-time pattern, as in Goldberg 9.5!
        """        
        e = self.input_lookup(history_tensor)
        x = e.view(e.shape[0], e.shape[1], e.shape[2])

        h, _ = self.lstm(x, self.init_hidden())

        o = self.output(h[-1])
        #y = self.softmax(o)
        y = F.log_softmax(o, dim=1)
        y = y.squeeze()[-1]

        return y


    def generate(self):
        max_length = 10
        last_character = ''
        last_history = init_hidden()
        for i in range(max_length)
            # call forward(last_char, last_hist), save output and history into last_char and last_hist
            # append output to the string that we're building up
            # repeat
        

    def init_hidden(self):
        """
        Generate a blank initial history value, for use when we start predicting over a fresh sequence.
        """
        h_0 = torch.randn(self.lstm_layers, 1, self.lstm_dims)
        c_0 = torch.randn(self.lstm_layers, 1, self.lstm_dims)

### Utility functions

def train(model, epochs, training_data, c2i):
    """
    Train model for the specified number of epochs, over the provided training data.
    
    Make sure to shuffle the training data at the beginning of each epoch!
    """
    raise NotImplementedError


def sample(model, c2i, i2c, max_seq_len=200):
    """
    Sample a new sequence from model.
    
    The length of the resulting sequence should be < max_seq_len, and the 
    new sequence should be stripped of <bos>/<eos> symbols if necessary.
    """
    raise NotImplementedError

    
def compute_prob(model, sentence, c2i):
    """
    Compute the negative log probability of p(sentence)
    
    Equivalent to equation 3.3 in Jurafsky & Martin.
    """
    
    nll = nn.NLLLoss(reduction='sum')
    
    with torch.no_grad():
        s_tens = vocab.sentence_to_tensor(sentence, c2i, True)
        x = s_tens[:,:-1]
        y = s_tens[:,1:]
        y_hat, _ = model(x, model.init_hidden())
        return nll(y_hat.squeeze(), y.squeeze()).item() # get rid of first dimension of each
