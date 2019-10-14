import unittest
import logging
#from mock import patch, MagicMock
import word_metrics

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test_translate.log',
                    filemode='w')

class TestWordMetrics(unittest.TestCase):
    def test__parse_args(self):
        expected_read_file = "data\\GW-cna_eng_small\\*.xml.gz"
        expected_write_file = "data\\GW-cna_eng_small\\APPEND_TO_FILE.txt"
        wm = word_metrics.WordMetric()
        aparser = wm._parse_args([expected_read_file, '-o', expected_write_file])
        actual_writefile = aparser.outfile
        self.assertEqual(aparser.read_file, expected_read_file)
        self.assertEqual(expected_write_file, actual_writefile)

    def test_read_deserialized(self):
        expected_lc = 41261
        wm = word_metrics.WordMetric()
        read_file = "data\\GW-cna_eng_small\\test_deserialize_small.txt"
        text = wm._read_tokenized(read_file)
        lines = text.splitlines()

        actual_lc = 0
        for l in lines:
            actual_lc += 1
        self.assertEqual(expected_lc, actual_lc)

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
