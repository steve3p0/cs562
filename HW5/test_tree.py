import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
import inspect
from tree import Tree
from io import StringIO

import logging


class TestTree(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    def test_kidnap_grandchild_simple(self):
        # Simple merge, with root and POS "distractors":
        s = '(TOP (S (VP (TO to) (VP (VB play)))))'
        t = Tree.from_string(s)
        col_tree = t.kidnap_grandchild()
        actual = col_tree.pretty()
        expected = inspect.cleandoc("""
            (TOP
                (S+VP
                    (TO to)
                    (VP
                        (VB play)
                    )
                )
            )""")

        eq_(actual, expected)

    def test_kidnap_grandchild_double(self):
        # Double merge, with both types of distractors:
        s = '(TOP (S (SBAR (VP (TO to) (VP (VB play))))))'
        t = Tree.from_string(s)
        col_tree = t.kidnap_grandchild()
        actual = col_tree.pretty()
        expected = inspect.cleandoc("""
            (TOP
                (S+SBAR+VP
                    (TO to)
                    (VP
                        (VB play)
                    )
                )
            )""")

        eq_(actual, expected)

    def test_kidnap_grandchild_long(self):
        # A long one:
        s = inspect.cleandoc("""
            (TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP
            (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's))
            (NN trading) (NN room))))) (, ,) (NP (DT the)
            (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP
            (RB little)) (ADJP (RB right)))) (. .)))""")

        t = Tree.from_string(s)
        col_tree = t.kidnap_grandchild()
        actual = col_tree.pretty()
        expected = inspect.cleandoc("""
            (TOP
                (S
                    (S+VP
                        (VBN Turned)
                        (ADVP
                            (RB loose)
                        )
                        (PP
                            (IN in)
                            (NP
                                (NP
                                    (NNP Shane)
                                    (NNP Longman)
                                    (POS 's)
                                )
                                (NN trading)
                                (NN room)
                            )
                        )
                    )
                    (, ,)
                    (NP
                        (DT the)
                        (NN yuppie)
                        (NNS dealers)
                    )
                    (VP
                        (AUX do)
                        (NP
                            (NP
                                (RB little)
                            )
                            (ADJP
                                (RB right)
                            )
                        )
                    )
                    (. .)
                )
            )""")

        eq_(actual, expected)

    def test_from_stream(self):
        s = '(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        source = StringIO(s.replace(' ', '\n\n\n') + s)
        (one, two) = Tree.from_stream(source)
        actual = str(one)
        expected = str(two)
        eq_(actual, expected)

    def test_from_stream_file(self):
        f = open("wsj-test.psd", "r", encoding="utf-8")
        obj = Tree.from_stream(f)
        for t in obj:
            before = Tree.pretty(t)
            print('////////////////////////////////////////////////////////////////////')
            print('BEFORE *************************')
            print(before)

            col_tree = t.kidnap_grandchild()
            after = Tree.pretty(col_tree)
            print('AFTER *************************')
            print(after)


    #@unittest.skip(("skip attribute")




