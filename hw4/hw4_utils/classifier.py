import string
from .data import Observation
import nltk.data

PUNKT_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')

def baseline_classifier(obs):
    """
    Baseline: Always say it's a sentence break
    """
    return True
    

def next_tok_capitalized_baseline(obs):
    """
    True if the right token is caplitalized
    """
    return obs.right_token[0] in string.ascii_uppercase

def punkt_baseline(obs):
    """
    Use the NLTK pre-trained Punkt classifier to try and decide if our candidate is a sentence break.
    
    This is not _exactly_ fair to Punkt, as it is not designed to work on fragments like this, but it's OK.
    """
    return len(PUNKT_DETECTOR.sentences_from_text(obs.orig_obs)) > 1