import gzip
import nltk
#import lxml
import wget
from lxml import etree
from os import listdir
from os.path import isfile, join
import re
import glob
import logging
import sys
import argparse
#
# sys.setdefaultencoding('utf8')

logging.basicConfig(#level=logging.DEBUG,  (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='word_metrics.log',
                    filemode='w')

#python your_deserialization_script.py cna_eng/*.xml.gz > deserialized.txt

class WordMetric:
    def __init__(self):
        logging.debug("WordMetric.__init__(self)")

    def _normalize(self, text):
        logging.debug("WordMetric._deserialize(self, text): text = " + text)

    def _tokenize(self, lang, text):
        logging.debug("WordMetric._tokenize(self, lang, text) lang, text = " + lang + ", " + text)

    def _unique_types(self, text):
        logging.debug("WordMetric._unique_types(self, text): text = " + text)

    def _unigram_tokens(self, text):
        logging.debug("WordMetric._unigram_tokens(self, text): text = " + text)

    def _rank_frequency_plot(self, text):
        logging.debug("WordMetric._rank_frequency_plot(self, text): text = " + text)

    def _most_common_words(self, text, stopwords):
        logging.debug("WordMetric._most_common_words(self, text, stopwords): text, stopwords = " + text + ", " + stopwords)

    def _pmi(self, word1, word2):
        logging.debug("WordMetric._pmi(self, word1, word2): word1, word2 = " + word1 + ", " + word2)

    def _compute_ngram(self, text, n, threshold):
        logging.debug("WordMetric._compute_ngram(self, text, n, threshold): " + text + ", " + n +", " + threshold)

def main():
    wm = WordMetric()

if __name__ == '__main__':
    logging.debug("__main__")
    main()