from  hw2_utils import constants 
import numpy as np

# deliverable 4.1
def get_token_type_ratio(counts):
    """
    Compute the ratio of tokens to types
    
    :param counts: bag of words feature for a song
    :returns: ratio of tokens to types
    :rtype float
    """
    raise NotImplementedError

# deliverable 4.2
def concat_ttr_binned_features(data):
    """
    Add binned token-type ratio features to the observation represented by data
    
    :param data: Bag of words
    :returns: Bag of words, plus binned ttr features
    :rtype: dict
    """
    raise NotImplementedError

