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

    def _parse_args(self, args):
        logging.debug("Deserialization._parse_args(self, read_path, write_path)")
        arg_parser = argparse.ArgumentParser(description='description here')
        arg_parser.add_argument('read_file')
        arg_parser.add_argument('-o', '--outfile')
        return arg_parser.parse_args(args)

    def _process_file(self, read_path, outfile):
        logging.debug("Deserialization._process_file(self, read_path, outfile): " + read_path)

        with gzip.open(read_path, 'r') as fin:
            file_content = fin.read()

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.XML(file_content, parser=parser)
        text = tree.xpath('/GWENG/DOC[@type="story"]/TEXT/P/text()')

        if not outfile:
            for line in text:
                print(line.replace('\n', ' '))
        else:
            f = open(outfile, "a+")
            for line in text:
                f.write(line.replace('\n', ' ') + "\n")
            f.close()

    def deserialize(self, read_path, outfile):
        logging.debug("Deserialization.deserialize(self, read_path, outfile): " + read_path)
        files = glob.glob(read_path)

        for file in files:
            self._process_file(file, outfile)

def main():
    ds = Deserialization()
    arg_parser = ds._parse_args(sys.argv[1:])
    ds.deserialize(arg_parser.read_file, arg_parser.outfile)


if __name__ == '__main__':
    logging.debug("__main__")
    main()
