import nltk
import logging
import re
import sys
import argparse
from nltk.probability import FreqDist
import matplotlib
import matplotlib.pyplot as plot
#from matplotlib.pyplot import plot, loglog, show

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
        logging.debug("WordMetric._parse_args(self, args)")
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

    def rank_frequency_plot(self, word_list):
        logging.debug("WordMetric.rank_frequency_plot(self, word_list)")
        fd = nltk.FreqDist()
        for word in word_list:
            fd[word] += 1

        freqs = [t[1] for t in fd.items()]
        ranks = range(len(freqs))
        plot.loglog(ranks, freqs)
        plot.xlabel('Frequency')
        plot.ylabel('Rank')
        plot.grid(True)
        plot.show()

    def most_common_words(self, n, word_list, stopwords, counts):
        logging.debug("WordMetric._most_common_words(self, n, word_list, stopwords)")

        if stopwords:
            from nltk.corpus import stopwords
            stops = set(stopwords.words("english"))
            ustops = [x.upper() for x in stops]
            word_list = [word for word in word_list if word not in ustops]
            print(str(n) + " Most Common (without stop words): ", end="")
        else:
            print(str(n) + " Most Common (with stop words): ", end="")

        from nltk import FreqDist
        fdist = FreqDist(word_list)
        nmc = fdist.most_common(n)

        if counts:
            print()
            for word in nmc:
                print(word[0] + ": " + str(word[1]))
            print()
        else:
            for word in nmc:
                #print(word[0] + ": " + str(word[1]))
                print(word[0] + ", ", end='')

    def pmi(self, text, n, threshold):
        logging.debug("WordMetric._pmi(self, text)")
        f = nltk.BigramCollocationFinder.from_documents([nltk.word_tokenize(x) for x in text.split('\n')])
        f.apply_freq_filter(threshold)
        print("return the 30 bigrams with the highest PMI")

        bm = nltk.collocations.BigramAssocMeasures()
        print(f.nbest(bm.pmi, n))

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

    # Twenty most common words (with stop words)
    wm.most_common_words(20, word_list, False, True)

    # Twenty most common words (without stop words)
    wm.most_common_words(20, word_list, True, False)

    #PMI: examine the 30 highest-PMI word pairs, along with their unigram and bigram frequencie
    wm.pmi("NEW YORK", 1, 0)
    wm.pmi(text, 30, 1000)
    wm.pmi(text, 10, 100)

    # Produce rank-frequency plot (Zipf's Law) for this corpus.
    wm.rank_frequency_plot(word_list)

if __name__ == '__main__':
    logging.debug("__main__")
    main()