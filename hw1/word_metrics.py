import nltk
import logging
import re
import sys
import argparse
import os
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
        with open(os.path.realpath(filename), 'r') as f:
            text = f.read()
        return text

    def unique_types(self, word_set):
        logging.debug("WordMetric.unique_types(self, word_set)")
        return len(word_set)

    def unigram_tokens_count(self, word_list):
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
                print(word[0] + ", ", end='')

    def pmi(self, text, n, threshold):
        logging.debug("WordMetric._pmi(self, text)")
        f = nltk.BigramCollocationFinder.from_documents([nltk.word_tokenize(x) for x in text.split('\n')])
        f.apply_freq_filter(threshold)
        print("The " + str(n) + " bigrams with the highest PMI with threshold " + str(threshold))

        bm = nltk.collocations.BigramAssocMeasures()
        print(f.nbest(bm.pmi, n))

        #for i in f.score_ngrams(bm.pmi):
        #    print(i)

    def _unigram_probability(self, word, word_list, wordcount):
        fd = nltk.FreqDist(word_list)
        probability = fd[word] / wordcount
        return probability

    def _bigram_probability(self, word1, word2, word_list, wordcount):
        fd = nltk.FreqDist(word_list)
        bigrams = nltk.bigrams(word_list)
        cfd = nltk.ConditionalFreqDist(bigrams)

        if not word2 in cfd[word1]:
            #print('Backing Off to Unigram Probability for', second)
            unigram_prob = self._unigram_probability(word2, word_list, wordcount)
            return unigram_prob
        else:
            bigram_frequency = cfd[word1][word2]

        unigram_frequency = fd[word1]
        bigram_probability = bigram_frequency / unigram_frequency

        return bigram_probability

    def compute_unigram_probabilies(self, word_set, word_list, wordcount):
        for word in word_set:
            unigram_probs = self._unigram_probability(word, word_list, wordcount)
            print(word + ": " + str(unigram_probs))

    def compute_bigram_probabilies(self, word_set, word_list, wordcount):
        for word1 in word_set:
            for word2 in word_list:
                bigram_probs = self._bigram_probability(word1, word2, word_list, wordcount)
                print(word1 + " " + word2 + ": " + str(bigram_probs))

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
    wordcount = wm.unigram_tokens_count(word_list)
    print("Unigram Tokens: " + str(wordcount))

    # Twenty most common words (with stop words)
    wm.most_common_words(20, word_list, False, True)

    # Twenty most common words (without stop words)
    wm.most_common_words(20, word_list, True, False)

    #PMI: examine the 30 highest-PMI word pairs, along with their unigram and bigram frequencie
    wm.pmi("NEW YORK", 1, 0)
    wm.pmi(text, 30, 1000)
    wm.pmi(text, 10, 100)

    #compute unigram and bigram probabilities for all unigrams and bigrams in the corpus
    #wm.compute_unigram_probabilies(word_set, word_list, wordcount)
    #wm.compute_bigram_probabilies(word_set, word_list, wordcount)

if __name__ == '__main__':
    logging.debug("__main__")
    main()