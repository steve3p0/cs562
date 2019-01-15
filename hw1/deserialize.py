import gzip
from lxml import etree
import glob
import logging
import sys
import argparse

logging.basicConfig(#level=logging.DEBUG,  (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='deserialization.log',
                    filemode='w')

#python your_deserialization_script.py cna_eng/*.xml.gz > deserialized.txt

class Deserialization:
    def __init__(self):
        logging.debug("Deserialization.__init__(self)")

    def _read(self, read_path, write_path):
        logging.debug("Deserialization._read(self, read_path, write_path): " + read_path + ", " + write_path)

        with gzip.open(read_path, 'r') as fin:
            file_content = fin.read()

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.XML(file_content, parser=parser)
        text = tree.xpath('/GWENG/DOC[@type="story"]/TEXT/P/text()')

        f = open(write_path, "a+")
        for line in text:
            f.write(line.replace('\n',' ') + "\n")
        f.close()

    def parse_args(self, args):
        logging.debug("Deserialization.parse_args(self, read_path, write_path)")
        arg_parser = argparse.ArgumentParser(description='description here')
        arg_parser.add_argument('read_file')
        arg_parser.add_argument('write_file', type=argparse.FileType('a'))
        return arg_parser.parse_args(args)

    def deserialize(self, read_path, write_path):
        logging.debug("Deserialization.deserialize(self, read_path, write_path): " + read_path + ", " + write_path)
        files = glob.glob(read_path)

        for file in files:
            self._read(file, write_path)

def main():
    ds = Deserialization()
    arg_parser = ds.parse_args(sys.argv[1:])
    ds.deserialize(arg_parser.read_file, arg_parser.write_file.name)

if __name__ == '__main__':
    logging.debug("__main__")
    main()