import unittest
import logging
import os
#from mock import patch, MagicMock
import deserialize

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='deserialize_test.log',
                    filemode='w')

class TestDeserialization(unittest.TestCase):
    def test__parse_args(self):
        expected_read_file = "data\\GW-cna_eng_small\\*.xml.gz"
        expected_write_file = "data\\GW-cna_eng_small\\APPEND_TO_FILE.txt"
        ds = deserialize.Deserialization()
        aparser = ds._parse_args([expected_read_file, '-o', expected_write_file])
        actual_writefile = aparser.outfile
        self.assertEqual(aparser.read_file, expected_read_file)
        self.assertEqual(expected_write_file, actual_writefile)

    def test__process_file(self):
        expected_lc = 6948
        ds = deserialize.Deserialization()
        read_file = "data\\GW-cna_eng_small\\cna_eng_199710.xml.gz"
        write_file = "data\\GW-cna_eng_small\\test_read.txt"
        if os.path.exists(write_file):
            os.remove(write_file)
        ds._process_file(read_file, write_file)

        with open(write_file) as f:
            for i, l in enumerate(f):
                pass
        actual_lc = i + 1
        self.assertEqual(expected_lc, actual_lc)

    def test_deserialize(self):
        # zgrep "</P>" *.xml.gz | wc - l
        expected_lc = 41261
        ds = deserialize.Deserialization()
        read_file = "data\\GW-cna_eng_small\\*.xml.gz"
        write_file = "data\\GW-cna_eng_small\\test_deserialize_all.txt"
        if os.path.exists(write_file):
            os.remove(write_file)
        ds.deserialize(read_file, write_file)

        with open(write_file) as f:
            for i, l in enumerate(f):
                pass
        actual_lc = i + 1
        self.assertEqual(expected_lc, actual_lc)

    def test_deserialize_allfiles(self):
        # zgrep "</P>" *.xml.gz | wc - l
        expected_lc = 489212
        ds = deserialize.Deserialization()
        read_file = "data\\GW-cna_eng\\*.xml.gz"
        write_file = "data\\GW-cna_eng\\test_deserialize_all.txt"
        if os.path.exists(write_file):
            os.remove(write_file)
        ds.deserialize(read_file, write_file)

        with open(write_file) as f:
            for i, l in enumerate(f):
                pass
        actual_lc = i + 1
        self.assertEqual(expected_lc, actual_lc)

if __name__ == '__main__':
    unittest.main()
