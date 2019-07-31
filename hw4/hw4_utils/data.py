# Based on bits and pieces from DetectorMorse: https://github.com/cslu-nlp/DetectorMorse

import re
from collections import namedtuple
from .ptbtokenizer import word_tokenize

def file_as_string(fname, encoding="utf-8"):
    """
    Given a filename `fname`, read the whole thing into a single huge string.
    """
    with open(fname, encoding=encoding) as source:
        return source.read()
    
# This namedtuple is meant to store everything we need to know about the environment around a candidate sentence break.
#
# The fields here are:
# left_context: The token to the _left_ of the matching punctuation mark
# left_raw: BUFSIZE raw characters to the left, no tokenization performed, but newlines removed
# punctuation_mark: The punctuation mark itself
# right_context: The token to the _right_ of the matching punctuation mark
# right_raw: BUFSIZE raw characters to the right, no tokenization performed, but newlines removed
# is_true_break: Whether this punctuation mark is actually a sentence boundary. For use ONLY during training, and NOT as an input feature to the classifier!!
# end_offset: The offset within the original training data of the matching punctuation mark
# orig_obs: The original punctuation mark in context, no tokenization, just newline removal
#
# Note that left_raw and right_raw may include newline characters!

Observation = namedtuple("Observation", ["left_token", "left_raw", "punctuation_mark", "right_token", "right_raw", "is_true_break", "end_offset", "orig_obs"])

# parameters:
BUFSIZE = 32 # how much left or right context to consider?

# regexes for candidate extraction:
PUNCT = r"((\.+)|([!?]))" # look for one or more periods, or a question mark, or an exclamation point
TARGET = PUNCT + r"(['`\")}\]]*)(\s+)" # deal with quotation marks, etc.

LTOKEN = r"(\S+)\s*$"
RTOKEN = r"^\s*(\S+)"
NEWLINE = r"^\s*[\r\n]+\s*$"

QUOTE = r"^['`\"]+$"

def load_candidates(s):
    """
    Returns an iterator of Observations for each matching candidate sentence boundary in `s`
    """
    for matching_punct in re.finditer(TARGET, s):
        
        # get the mark itself:
        punct_mark = matching_punct.group(1)
        
        # is it a boundary (for ground-truth at training time)
        is_boundary = bool(re.match(NEWLINE, matching_punct.group(5)))
        
        # get left and right context:
        start = matching_punct.start()
        end = matching_punct.end()
        
        raw_obs = s[max(0, start - BUFSIZE):end+BUFSIZE]
        clean_obs = re.sub(r"[\r\n]", " ", raw_obs)
        
        raw_left_context = s[max(0, start - BUFSIZE):start]
        clean_left_context = re.sub(r"[\r\n]", " ", raw_left_context)
        
        left_match = re.search(LTOKEN, raw_left_context) # look to the left as close to BUFSIZE as we can

        left_token = word_tokenize(" " + left_match.group(1))[-1]

        if not left_match: # special case for when a line begins with a "."
            continue
        
        raw_right_context = s[end:end + BUFSIZE]
        
        # replace newlines, so they don't sneak into training data
        clean_right_context = re.sub(r"[\r\n]", " ", raw_right_context)
        
        right_match = re.search(RTOKEN, raw_right_context)
        if not right_match: # special case for end of file
            continue
            
        right_token = word_tokenize(right_match.group(1) + " ")[0]
        
        yield Observation(punctuation_mark=punct_mark, is_true_break=is_boundary, left_token = left_token, left_raw=clean_left_context, right_token = right_token, right_raw=clean_right_context, end_offset = end, orig_obs=clean_obs)