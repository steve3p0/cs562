import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
import inspect
from io import StringIO
import logging

from tree import Tree

# Helper function Unit Tests
class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    def print_kidnap_grandchild_collapse_WSJ_trees(self):
        # filename = "wsj-normalized.psd"
        filename = "wsj-test.psd"
        f = open(filename, "r", encoding="utf-8")
        trees_before = Tree.from_stream(f)
        f.close

        for t in trees_before:
            before = Tree.pretty(t)
            print('////////////////////////////////////////////////////////////////////')
            print('BEFORE *************************')
            print(before)

            tree_collapsed = t.kidnap_daughter()
            after = Tree.pretty(tree_collapsed)
            print('AFTER *************************')
            print(after)

    def test_from_stream(self):
        s = '(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        source = StringIO(s.replace(' ', '\n\n\n') + s)
        (one, two) = Tree.from_stream(source)
        actual = str(one)
        expected = str(two)
        eq_(actual, expected)

    #@unittest.skip(("skip attribute")

# Collapse Unary Unit Tests
class TestCollapseUnary(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    # Collapse Unary - Inline test #1
    def test_kidnap_grandchild_simple(self):
        # Simple merge, with root and POS "distractors":
        s = '(TOP (S (VP (TO to) (VP (VB play)))))'
        t = Tree.from_string(s)
        col_tree = t.kidnap_daughter()
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

    # Collapse Unary - Inline test #1
    def test_kidnap_grandchild_double(self):
        # Double merge, with both types of distractors:
        s = '(TOP (S (SBAR (VP (TO to) (VP (VB play))))))'
        t = Tree.from_string(s)
        col_tree = t.kidnap_daughter()
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

    # Collapse Unary - Inline test #1
    def test_kidnap_grandchild_long(self):
        # A long one:
        s = inspect.cleandoc("""
            (TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP
            (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's))
            (NN trading) (NN room))))) (, ,) (NP (DT the)
            (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP
            (RB little)) (ADJP (RB right)))) (. .)))""")

        t = Tree.from_string(s)
        col_tree = t.kidnap_daughter()
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

    ### Collapse Unary - Regression Tests ######################################################

    def test_kidnap_grandchild_collapse_small_WSJ_trees(self):
        # filename = "wsj-normalized.psd"
        filename = "wsj-test.psd" # small test file - only 2 trees
        f = open(filename, "r", encoding="utf-8")
        trees_before = Tree.from_stream(f)
        f.close

        index = 0
        for t in trees_before:
            index += 1
            before = Tree.pretty(t)
            print('////////////////////////////////////////////////////////////////////')
            print('TEST: ' + str(index) + '  ************************************')
            print(before)

            tree_collapsed = Tree.kidnap_daughter(t)
            actual = Tree.pretty(tree_collapsed)
            print('AFTER *************************')
            print(actual)

            expect = None
            if index == 1:
                expect = inspect.cleandoc("""
                    (TOP
                        (NP-SBJ
                            (NP
                                (NNP <NNP>)
                                (NNP <NNP>)
                            )
                            (, ,)
                            (ADJP
                                (NP
                                    (CD <CD>)
                                    (NNS years)
                                )
                                (JJ old)
                            )
                            (, ,)
                        )
                        (VP
                            (MD will)
                            (VP
                                (VB join)
                                (NP
                                    (DT the)
                                    (NN board)
                                )
                                (PP-CLR
                                    (IN as)
                                    (NP
                                        (DT a)
                                        (JJ nonexecutive)
                                        (NN director)
                                    )
                                )
                                (NP-TMP
                                    (NNP <NNP>)
                                    (CD <CD>)
                                )
                            )
                        )
                        (. .)
                    )""")
            elif index == 2:
                expect = inspect.cleandoc("""
                    (TOP
                        (NP-SBJ
                            (NNP <NNP>)
                            (NNP <NNP>)
                        )
                        (VP
                            (VBZ is)
                            (NP-PRD
                                (NP
                                    (NN chairman)
                                )
                                (PP
                                    (IN of)
                                    (NP
                                        (NP
                                            (NNP <NNP>)
                                            (NNP <NNP>)
                                        )
                                        (, ,)
                                        (NP
                                            (DT the)
                                            (NNP <NNP>)
                                            (VBG publishing)
                                            (NN group)
                                        )
                                    )
                                )
                            )
                        )
                        (. .)
                    )""")

            print('EXPECTED: *************************')
            print(expect)
            print('ACTUAL *************************')
            print(actual)

            eq_(expect, actual)

    def test_kidnap_grandchild_109(self):
        # A long one:
        s = inspect.cleandoc("""
            (TOP
                (PP
                    (IN by)
                    (NP
                        (JJS most)
                        (NNS measures)
                    )
                )
                (, ,)
                (NP-SBJ
                    (NP
                        (DT the)
                        (NN nation)
                        (POS 's)
                    )
                    (JJ industrial)
                    (NN sector)
                )
                (VP
                    (VBZ is)
                    (ADVP-TMP
                        (RB now)
                    )
                    (VP
                        (VBG growing)
                        (ADVP-MNR
                            (RB very)
                            (RB slowly)
                        )
                        (: --)
                        (SBAR-ADV
                            (IN if)
                            (FRAG
                                (ADVP
                                    (IN at)
                                    (DT all)
                                )
                            )
                        )
                    )
                )
                (. .)
            )""")

        t = Tree.from_string(s)

        # Expected Value
        expect = inspect.cleandoc("""
            (TOP
                (PP
                    (IN by)
                    (NP
                        (JJS most)
                        (NNS measures)
                    )
                )
                (, ,)
                (NP-SBJ
                    (NP
                        (DT the)
                        (NN nation)
                        (POS 's)
                    )
                    (JJ industrial)
                    (NN sector)
                )
                (VP
                    (VBZ is)
                    (ADVP-TMP
                        (RB now)
                    )
                    (VP
                        (VBG growing)
                        (ADVP-MNR
                            (RB very)
                            (RB slowly)
                        )
                        (: --)
                        (SBAR-ADV
                            (IN if)
                            (FRAG+ADVP
                                (IN at)
                                (DT all)
                            )
                        )
                    )
                )
                (. .)
            )""")
        print('EXPECTED: *************************')
        print(expect)

        col_tree = t.kidnap_daughter()
        actual = col_tree.pretty()
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

    def test_kidnap_grandchild_109a(self):
        # A long one:
        s = inspect.cleandoc("""
            (TOP
                (VP
                    (VP
                        (SBAR-ADV
                            (IN if)
                            (FRAG
                                (ADVP
                                    (IN at)
                                    (DT all)
                                )
                            )
                        )
                    )
                )
                (. .)
            )""")

        t = Tree.from_string(s)

        # Expected Value
        expect = inspect.cleandoc("""
            (TOP
                (VP+VP+SBAR-ADV
                    (IN if)
                    (FRAG+ADVP
                        (IN at)
                        (DT all)
                    )
                )
                (. .)
            )""")
        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        col_tree = t.kidnap_daughter()
        actual = Tree.pretty(col_tree)
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

    def test_kidnap_grandchild_109b(self):
        # A long one:
        s = inspect.cleandoc("""
            (TOP
                (SBAR-ADV
                    (IN if)
                    (FRAG
                        (ADVP
                            (IN at)
                            (DT all)
                        )
                    )
                )
            )""")

        t = Tree.from_string(s)

        # Expected Value
        expect = inspect.cleandoc("""
            (TOP
                (SBAR-ADV
                    (IN if)
                    (FRAG+ADVP
                        (IN at)
                        (DT all)
                    )
                )
            )""")
        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        col_tree = t.kidnap_daughter()
        actual = Tree.pretty(col_tree)
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

    def test_kidnap_grandchild_109c(self):
        # A long one:
        s = inspect.cleandoc("""
            (TOP
                (SBAR-ADV
                    (FRAG
                        (ADVP
                            (IN at)
                            (DT all)
                        )
                    )
                )
            )""")

        t = Tree.from_string(s)

        # Expected Value
        expect = inspect.cleandoc("""
            (TOP
                (SBAR-ADV+FRAG+ADVP
                    (IN at)
                    (DT all)
                )
            )""")
        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        col_tree = t.kidnap_daughter()
        actual = Tree.pretty(col_tree)
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

    def test_kidnap_grandchild_109d(self):
        # A long one:
        s = inspect.cleandoc("""
            (TOP
                (FRAG
                    (ADVP
                        (IN at)
                        (DT all)
                    )
                )
            )""")

        t = Tree.from_string(s)

        # Expected Value
        expect = inspect.cleandoc("""
            (TOP
                (FRAG+ADVP
                    (IN at)
                    (DT all)
                )
            )""")
        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        col_tree = t.kidnap_daughter()
        actual = Tree.pretty(col_tree)
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)
