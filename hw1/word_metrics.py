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
from nltk.tokenize import TweetTokenizer, sent_tokenize
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

    def _parse_args(self, args):
        logging.debug("WordMetric._parse_args(self, read_path, write_path)")
        arg_parser = argparse.ArgumentParser(description='description here')
        arg_parser.add_argument('read_file')
        arg_parser.add_argument('-o', '--outfile')
        return arg_parser.parse_args(args)

    def _read_deserialized(self, filename):
        logging.debug("WordMetric._read_deserialized(self, filename): " + filename)

        with open(filename, 'r') as f:
            text = f.read()

        ' '.join(text.split())
        return text.upper()
        #return text

    def _tokenize(self, text):
        logging.debug("WordMetric._tokenize(self, text)")
        sentences = nltk.sent_tokenize(text)

        import string
        punct_set = set(string.punctuation)
        # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        punct_set.add("'s")
        punct_set.add('``')
        punct_set.add("''")
        punct_set.add('--')
        #print(punct_set)

        for s in sentences:
            tokens = nltk.word_tokenize(s)
            no_punct_toks = [t for t in tokens if t not in punct_set]
            print(no_punct_toks)

        #return no_punct_toks

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
    arg_parser = wm._parse_args(sys.argv[1:])
    text = wm._read_deserialized(arg_parser.read_file)
    tokens = wm._tokenize(text)
    print(tokens)

if __name__ == '__main__':
    logging.debug("__main__")
    main()