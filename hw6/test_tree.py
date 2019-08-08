# test_tree.py: unit tests for tree.py
# Author: Steve Braich

import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
import inspect
import os
from io import StringIO
import logging

from tree import Tree

# Helper function Unit Tests
class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    def print_before_and_after_collapse_WSJ_trees(self):
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

    #@unittest.skip("skip attribute")

# Collapse Unary Unit Tests
class TestCollapseUnary(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    # Collapse Unary - Inline test #1
    def test_kidnap_daughter_simple(self):
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
    def test_kkidnap_daughter_double(self):
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
    def test_kidnap_daughter_long(self):
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

    def test_kidnap_daughter_collapse_small_WSJ_trees(self):
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

    def test_kidnap_daughter_109(self):
        # The 109th tree in the WSJ tree examples
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

    def test_kidnap_daughter_109a(self):
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

    def test_kidnap_daughter_109b(self):
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

    def test_kidnap_daughter_109c(self):
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

    def test_kidnap_daughter_109d(self):
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

# Chomsky Normal Form Unit Tests
class TestChomskyNormalForm(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    # Convert to CNF - Inline test #1
    def test_convert_to_cnf_long(self):
        s = inspect.cleandoc("""
            (TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP
            (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's))
            (NN trading) (NN room))))) (, ,) (NP (DT the)
            (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP
            (RB little)) (ADJP (RB right)))) (. .)))""")

        t = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t.pretty()
        print(before)

        # Expected Value
        expect = inspect.cleandoc("""
            (TOP
                (S
                    (S+VP
                        (VBN Turned)
                        (S+VP|<ADVP&PP>
                            (ADVP
                                (RB loose)
                            )
                            (PP
                                (IN in)
                                (NP
                                    (NP
                                        (NNP Shane)
                                        (NP|<NNP&POS>
                                            (NNP Longman)
                                            (POS 's)
                                        )
                                    )
                                    (NP|<NN&NN>
                                        (NN trading)
                                        (NN room)
                                    )
                                )
                            )
                        )
                    )
                    (S|<,&NP>
                        (, ,)
                        (S|<NP&VP>
                            (NP
                                (DT the)
                                (NP|<NN&NNS>
                                    (NN yuppie)
                                    (NNS dealers)
                                )
                            )
                            (S|<VP&.>
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
                        )
                    )
                )
            )""")
        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        col_tree = t.collapse_unary()
        cnf_tree = col_tree.convert_to_cnf()
        actual = cnf_tree.pretty()
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

    # Convert to CNF - Test from assignment description
    def test_convert_to_cnf_short(self):
        s = inspect.cleandoc("""
            (TOP
                (NP 
                    (NNP Shane) 
                    (NNP Longman) 
                    (POS 's)
                )
            )""")

        t = Tree.from_string(s)

        # Expected Value
        expect = inspect.cleandoc("""
            (TOP
                (NP
                    (NNP Shane)
                    (NP|<NNP&POS>
                        (NNP Longman)
                        (POS 's)
                    )
                )
            )""")
        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        cnf_tree = t.convert_to_cnf()
        actual = cnf_tree.pretty()
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

    ### onvert to CNF - Regression Tests ######################################################

    def test_convert_to_cnf_94(self):
        # The 94th tree in the WSJ tree examples
        s = inspect.cleandoc("""
            (TOP
                (NP-SBJ
                    (DT these)
                    (NNS funds)
                )
                (ADVP-TMP
                    (RB now)
                )
                (VP
                    (VBP account)
                    (PP-CLR
                        (IN for)
                        (NP
                            (NP
                                (NP
                                    (QP
                                        (JJ several)
                                        (NNS billions)
                                    )
                                )
                                (PP
                                    (IN of)
                                    (NP
                                        (NNS dollars)
                                    )
                                )
                            )
                            (PP
                                (IN in)
                                (NP
                                    (NNS assets)
                                )
                            )
                        )
                    )
                )
                (. .)
            )""")

        t = Tree.from_string(s)
        before = Tree.pretty(t)
        print('BEFORE: *************************')
        print(before)

        expect = inspect.cleandoc("""
            (TOP
                (NP-SBJ
                    (DT these)
                    (NNS funds)
                )
                (TOP|<ADVP-TMP&VP>
                    (ADVP-TMP
                        (RB now)
                    )
                    (TOP|<VP&.>
                        (VP
                            (VBP account)
                            (PP-CLR
                                (IN for)
                                (NP
                                    (NP
                                        (NP+QP
                                            (JJ several)
                                            (NNS billions)
                                        )
                                        (PP
                                            (IN of)
                                            (NP
                                                (NNS dollars)
                                            )
                                        )
                                    )
                                    (PP
                                        (IN in)
                                        (NP
                                            (NNS assets)
                                        )
                                    )
                                )
                            )
                        )
                        (. .)
                    )
                )
            )""")
        print('EXPECTED: *************************')
        print(expect)

        col_tree = t.kidnap_daughter()
        cnf_tree_actual = Tree.chomsky_normal_form(col_tree)

        actual = cnf_tree_actual.pretty()
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

    def test_convert_to_cnf_109(self):
        # The 94th tree in the WSJ tree examples
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
        before = Tree.pretty(t)
        print('BEFORE: *************************')
        print(before)

        expect = inspect.cleandoc("""
            (TOP
                (PP
                    (IN by)
                    (NP
                        (JJS most)
                        (NNS measures)
                    )
                )
                (TOP|<,&NP-SBJ>
                    (, ,)
                    (TOP|<NP-SBJ&VP>
                        (NP-SBJ
                            (NP
                                (DT the)
                                (NP|<NN&POS>
                                    (NN nation)
                                    (POS 's)
                                )
                            )
                            (NP-SBJ|<JJ&NN>
                                (JJ industrial)
                                (NN sector)
                            )
                        )
                        (TOP|<VP&.>
                            (VP
                                (VBZ is)
                                (VP|<ADVP-TMP&VP>
                                    (ADVP-TMP
                                        (RB now)
                                    )
                                    (VP
                                        (VBG growing)
                                        (VP|<ADVP-MNR&:>
                                            (ADVP-MNR
                                                (RB very)
                                                (RB slowly)
                                            )
                                            (VP|<:&SBAR-ADV>
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
                                    )
                                )
                            )
                            (. .)
                        )
                    )
                )
            )""")
        print('EXPECTED: *************************')
        print(expect)

        col_tree = t.kidnap_daughter()
        cnf_tree_actual = Tree.chomsky_normal_form(col_tree)

        actual = cnf_tree_actual.pretty()
        print('ACTUAL *************************')
        print(actual)

        eq_(actual, expect)

# Chomsky Normal Form Unit Tests
class TestProductions(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    # Generate Productions - Inline test #1
    def test_productions_inline1(self):
        s = inspect.cleandoc("""
            (TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP
            (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's))
            (NN trading) (NN room))))) (, ,) (NP (DT the)
            (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP
            (RB little)) (ADJP (RB right)))) (. .)))""")

        t_before = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

        # Expected Value
        expect = inspect.cleandoc("""
            TOP                  -> S
            S                    -> S+VP S|<,&NP>
            S+VP                 -> VBN S+VP|<ADVP&PP>
            VBN                  -> Turned
            S+VP|<ADVP&PP>       -> ADVP PP
            ADVP                 -> RB
            RB                   -> loose
            PP                   -> IN NP
            IN                   -> in
            NP                   -> NP NP|<NN&NN>
            NP                   -> NNP NP|<NNP&POS>
            NNP                  -> Shane
            NP|<NNP&POS>         -> NNP POS
            NNP                  -> Longman
            POS                  -> 's
            NP|<NN&NN>           -> NN NN
            NN                   -> trading
            NN                   -> room
            S|<,&NP>             -> , S|<NP&VP>
            ,                    -> ,
            S|<NP&VP>            -> NP S|<VP&.>
            NP                   -> DT NP|<NN&NNS>
            DT                   -> the
            NP|<NN&NNS>          -> NN NNS
            NN                   -> yuppie
            NNS                  -> dealers
            S|<VP&.>             -> VP .
            VP                   -> AUX NP
            AUX                  -> do
            NP                   -> NP ADJP
            NP                   -> RB
            RB                   -> little
            ADJP                 -> RB
            RB                   -> right
            .                    -> .""")

        print('EXPECTED: *************************')
        expect = os.linesep.join([st for st in expect.splitlines() if st])
        print(expect)

        # Actual Value
        t_col = t_before.collapse_unary()
        t_cnf = t_col.chomsky_normal_form()
        t_prod = t_cnf.productions()

        print('ACTUAL *************************')
        actual = Tree.pretty_productions(t_prod)
        print(actual)

        eq_(actual, expect)

    def test_productions_fromAssignment(self):
        s = inspect.cleandoc("""
            (TOP
                (S
                    (VP
                        (TO to)
                        (VP
                            (VB play)
                        )
                    )
                )
            )""")

        t_before = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

        expect = inspect.cleandoc("""
            TOP                  -> S+VP
            S+VP                 -> TO VP
            TO                   -> to
            VP                   -> VB
            VB                   -> play""")
        expect = os.linesep.join([st for st in expect.splitlines() if st])

        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        t_col = t_before.collapse_unary()
        t_cnf = t_col.chomsky_normal_form()

        print('CNF: *************************')
        cnf = t_cnf.pretty()
        print(cnf)

        #t_prod = t_cnf.create_tree_productions()
        t_prod = t_cnf.productions()
        #t_prod = os.linesep.join([st for st in t_prod.splitlines() if st])
        #t_prod = t_cnf.productions()

        print('ACTUAL *************************')
        #actual = self.pretty_productions(t_prod)
        actual = Tree.pretty_productions(t_prod)
        #actual = t_prod
        print(actual)

        eq_(actual, expect)

    ### Generate Productions - Regression Tests ######################################################

    def test_productions_wsj_94(self):
        s = inspect.cleandoc("""
            (TOP
                (NP-SBJ
                    (DT these)
                    (NNS funds)
                )
                (ADVP-TMP
                    (RB now)
                )
                (VP
                    (VBP account)
                    (PP-CLR
                        (IN for)
                        (NP
                            (NP
                                (NP
                                    (QP
                                        (JJ several)
                                        (NNS billions)
                                    )
                                )
                                (PP
                                    (IN of)
                                    (NP
                                        (NNS dollars)
                                    )
                                )
                            )
                            (PP
                                (IN in)
                                (NP
                                    (NNS assets)
                                )
                            )
                        )
                    )
                )
                (. .)
            )""")

        t_before = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

        # Expected Value
        expect = inspect.cleandoc("""
            TOP                  -> NP-SBJ TOP|<ADVP-TMP&VP>
            NP-SBJ               -> DT NNS
            DT                   -> these
            NNS                  -> funds
            TOP|<ADVP-TMP&VP>    -> ADVP-TMP TOP|<VP&.>
            ADVP-TMP             -> RB
            RB                   -> now
            TOP|<VP&.>           -> VP .
            VP                   -> VBP PP-CLR
            VBP                  -> account
            PP-CLR               -> IN NP
            IN                   -> for
            NP                   -> NP PP
            NP                   -> NP+QP PP
            NP+QP                -> JJ NNS
            JJ                   -> several
            NNS                  -> billions
            PP                   -> IN NP
            IN                   -> of
            NP                   -> NNS
            NNS                  -> dollars
            PP                   -> IN NP
            IN                   -> in
            NP                   -> NNS
            NNS                  -> assets
            .                    -> .""")

        print('EXPECTED: *************************')
        expect = os.linesep.join([st for st in expect.splitlines() if st])
        print(expect)

        # Actual Value
        t_col = t_before.collapse_unary()
        t_cnf = t_col.chomsky_normal_form()
        t_prod = t_cnf.productions()

        print('ACTUAL *************************')
        actual = Tree.pretty_productions(t_prod)
        print(actual)

        eq_(actual, expect)

    def test_productions_wsj_109(self):
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

        t_before = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

        # Expected Value
        expect = inspect.cleandoc("""
            TOP                  -> PP TOP|<,&NP-SBJ>
            PP                   -> IN NP
            IN                   -> by
            NP                   -> JJS NNS
            JJS                  -> most
            NNS                  -> measures
            TOP|<,&NP-SBJ>       -> , TOP|<NP-SBJ&VP>
            ,                    -> ,
            TOP|<NP-SBJ&VP>      -> NP-SBJ TOP|<VP&.>
            NP-SBJ               -> NP NP-SBJ|<JJ&NN>
            NP                   -> DT NP|<NN&POS>
            DT                   -> the
            NP|<NN&POS>          -> NN POS
            NN                   -> nation
            POS                  -> 's
            NP-SBJ|<JJ&NN>       -> JJ NN
            JJ                   -> industrial
            NN                   -> sector
            TOP|<VP&.>           -> VP .
            VP                   -> VBZ VP|<ADVP-TMP&VP>
            VBZ                  -> is
            VP|<ADVP-TMP&VP>     -> ADVP-TMP VP
            ADVP-TMP             -> RB
            RB                   -> now
            VP                   -> VBG VP|<ADVP-MNR&:>
            VBG                  -> growing
            VP|<ADVP-MNR&:>      -> ADVP-MNR VP|<:&SBAR-ADV>
            ADVP-MNR             -> RB RB
            RB                   -> very
            RB                   -> slowly
            VP|<:&SBAR-ADV>      -> : SBAR-ADV
            :                    -> --
            SBAR-ADV             -> IN FRAG+ADVP
            IN                   -> if
            FRAG+ADVP            -> IN DT
            IN                   -> at
            DT                   -> all
            .                    -> .""")

        print('EXPECTED: *************************')
        expect = os.linesep.join([st for st in expect.splitlines() if st])
        print(expect)

        # Actual Value
        t_col = t_before.collapse_unary()
        t_cnf = t_col.chomsky_normal_form()
        t_prod = t_cnf.productions()

        print('ACTUAL *************************')
        actual = Tree.pretty_productions(t_prod)
        print(actual)

        eq_(actual, expect)