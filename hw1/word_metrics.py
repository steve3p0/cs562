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
import re
from collections import Counter
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

class WordMetric:
    def __init__(self):
        logging.debug("WordMetric.__init__(self)")

    def _parse_args(self, args):
        logging.debug("WordMetric._parse_args(self, read_path, write_path)")
        arg_parser = argparse.ArgumentParser(description='description here')
        arg_parser.add_argument('read_file')
        arg_parser.add_argument('-o', '--outfile')
        return arg_parser.parse_args(args)

    def _read_tokenized(self, filename):
        logging.debug("WordMetric._read_tokenized(self, filename): " + filename)

        with open(filename, 'r') as f:
            text = f.read()
        return text

    def unique_types(self, word_set):
        logging.debug("WordMetric.unique_types(self, word_set)")
        return len(word_set)

    def unigram_tokens(self, word_list):
        logging.debug("WordMetric.unigram_tokens(self, word_list)")
        return len(word_list)

    def _rank_frequency_plot(self, text):
        logging.debug("WordMetric._rank_frequency_plot(self, text)")

    def most_common_words(self, n, word_list, stopwords):
        logging.debug("WordMetric._most_common_words(self, n, word_list, stopwords)")

        from nltk import FreqDist
        fdist = FreqDist(word_list)
        nmc = fdist.most_common(n)
        print(str(n) + " Most Common: ", end="")

        for word in nmc:
            #print(word[0] + ": " + str(word[1]))
            print(word[0] + ", ", end='')

    def _pmi(self, word1, word2):
        logging.debug("WordMetric._pmi(self, word1, word2): word1, word2 = " + word1 + ", " + word2)

    def _compute_ngram(self, text, n, threshold):
        logging.debug("WordMetric._compute_ngram(self, text, n, threshold): " + text + ", " + n +", " + threshold)

def main():
    wm = WordMetric()
    arg_parser = wm._parse_args(sys.argv[1:])
    text = wm._read_tokenized(arg_parser.read_file)

    word_list = re.sub("[^\w]", " ", text).split()
    word_set = set(word_list)

    # Unique Types
    unique = wm.unique_types(word_set)
    print("Unique Types: " + str(unique))

    # Unigram Tokens
    utokens = wm.unigram_tokens(word_list)
    print("Unigram Tokens: " + str(utokens))

    # Twenty most common words
    wm.most_common_words(20, word_list, False)


if __name__ == '__main__':
    logging.debug("__main__")
    main()