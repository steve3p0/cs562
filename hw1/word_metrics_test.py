import unittest
import logging
import os
#from mock import patch, MagicMock
import word_metrics

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test_translate.log',
                    filemode='w')

class TestWordMetrics(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(True, False)

    def test_tokenize(self):
        self.assertEqual(True, False)

    def test_unique_types(self):
        self.assertEqual(True, False)

    def test_unigram_tokens(self):
        self.assertEqual(True, False)

    def test_rank_frequency_plot(self):
        self.assertEqual(True, False)

    def test_most_common_words(self):
        self.assertEqual(True, False)

    def test_pmi(self):
        self.assertEqual(True, False)

    def test_compute_ngram(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
