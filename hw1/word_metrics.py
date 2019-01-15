import gzip
import nltk
#import lxml
import wget
from lxml import etree
import logging
# import sys
#
# sys.setdefaultencoding('utf8')

logging.basicConfig(#level=logging.DEBUG,  (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    level=logging.CRITICAL, # Basically turn Logging off
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='word_metrics.log',
                    filemode='w')

#python your_deserialization_script.py cna_eng/*.xml.gz > deserialized.txt

class WordMetric:
    def __init__(self):
        logging.debug("WordMetric.__init__(self)")

    def _read(self, path):
        logging.debug("WordMetric._read(self, path): path = " + path)

        with gzip.open(path, 'r') as fin:
            file_content = fin.read()
            # for line in fin:
            #     print('got line', line)
        #print(file_content)

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.XML(file_content, parser=parser)
        #  XPath query /GWENG/DOC[@type="story"]/TEXT
        #  div.xpath('normalize-space(.//p[@class="class-name"])').extract()
        #text = tree.xpath('normalize-space(/GWENG/DOC[@type="story"]/TEXT/P)')
        #text = tree.xpath('/GWENG/DOC[@type="story"]/TEXT/P')
        #sel.xpath('normalize-space(//div[label="Actions Taken"]/article/div/ul/li/text()[0])').extract()

        #// label[ // text()[normalize - space() = 'some label']]
        #text = tree.xpath('/GWENG/DOC[@type="story"]/TEXT/P/text()/normalize-space(.)')
        #text = tree.xpath('/GWENG/DOC[@type="story"]/TEXT/P/normalize-space(.)')
        #text = tree.xpath('/GWENG/DOC[@type="story"]/TEXT/P[normalize-space(.)]')
        # This gets each element without normalization
        text = tree.xpath('/GWENG/DOC[@type="story"]/TEXT/P/text()')

        for line in text:
             print("XXXXX: (" + line.replace('\n','') + ")")
        #print("XXXXX: (" + text + ")")
        # print("blah: (" + text[0].text + ")")

    def _deserialize(self, path):
        logging.debug("WordMetric._deserialize(self, path): path = " + path)

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

if __name__ == '__main__':
    logging.debug("__main__")
