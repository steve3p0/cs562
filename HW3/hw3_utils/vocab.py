from collections import defaultdict
from itertools import count
import numpy as np
import torch

BOS_SYM = '<BOS>'
EOS_SYM = '<EOS>'

def build_vocab(corpus):
    """
    Build an exhaustive character inventory for the corpus, and return dictionaries
    that can be used to map characters to indicies and vice-versa.
    
    Make sure to include BOS_SYM and EOS_SYM!
    
    :param corpus: a corpus, represented as an iterable of strings
    :returns: two dictionaries, one mapping characters to vocab indicies and another mapping idicies to characters.
    :rtype: dict-like object, dict-like object
    """

    s = set(''.join(corpus))

    i2c_dict = dict(enumerate(s))

    last, _ = list(i2c_dict.items())[-1]
    last += 1
    i2c_dict[last] = BOS_SYM
    last += 1
    i2c_dict[last] = EOS_SYM

    c2i_dict = dict((v,k) for k,v in i2c_dict.items())

    return c2i_dict, i2c_dict

def sentence_to_vector(s, vocab, pad_with_bos=False):
    """
    Turn a string, s, into a list of indicies in from `vocab`. 
    
    :param s: A string to turn into a vector
    :param vocab: the mapping from characters to indicies
    :param pad_with_bos: Pad the sentence with BOS_SYM/EOS_SYM markers
    :returns: a list of the character indicies found in `s`
    :rtype: list
    """

    chr_indices = list()

    for c in s:
        chr_indices.append(vocab[c])

    if pad_with_bos:
        chr_indices.insert(0, vocab[BOS_SYM])
        chr_indices.append(vocab[EOS_SYM])

    return chr_indices
    
def sentence_to_tensor(s, vocab, pad_with_bos=False):
    """
    :param s: A string to turn into a tensor
    :param vocab: the mapping from characters to indicies
    :param pad_with_bos: Pad the sentence with BOS_SYM/EOS_SYM markers
    :returns: (1, n) tensor where n=len(s) and the values are character indicies
    :rtype: torch.Tensor
    """

    list_indices = sentence_to_vector(s, vocab, pad_with_bos)

    #arry_indices = np.asarray(list_indices, dtype=int)
    #arry_indices = np.asarray(list_indices, dtype=np.long)
    arry_indices = np.asarray(list_indices, dtype=np.int_)
    arry_indices = np.asarray(list_indices, dtype=np.longlong)

    #t = torch.Tensor(list_indices, dbtype=int).unsqueeze(0)
    t = torch.from_numpy(arry_indices).unsqueeze(0)
    #t.dbtype = torch.int64

    return t
    
def build_label_vocab(labels):
    """
    Similar to build_vocab()- take a list of observed labels and return a pair of mappings to go from label to numeric index and back.
    
    The number of label indicies should be equal to the number of *distinct* labels that we see in our dataset.
    
    :param labels: a list of observed labels ("y" values)
    :returns: two dictionaries, one mapping label to indicies and the other mapping indicies to label
    :rtype: dict-like object, dict-like object
    """

    i2l_dict = dict(enumerate(set(labels)))
    l2i_dict = dict((v,k) for k,v in i2l_dict.items())

    return l2i_dict, i2l_dict
