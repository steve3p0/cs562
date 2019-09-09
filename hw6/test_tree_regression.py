# test_tree_regression.py: regression tests for tree.py
# Author: Steve Braich

import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
import logging
import inspect
import os

from itertools import chain

from tree import Tree
from tree_regression import Tree as ExpectedTree

VERBOSE = True

logger = logging.getLogger()
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(filename='./test_tree_regression.log', level=logging.DEBUG,
                   format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                   datefmt='%m-%d %H:%M')

class TestTreeRegression(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    # This tests unary_collapse with all 14,898 in the WSJ test file
    # Note: This takes about a minute
    def test_collapse_unary_WSJ(self):
        filename = "wsj-normalized.psd"
        #filename = "wsj-test.psd"
        f = open(filename, "r", encoding="utf-8")
        trees_expect = ExpectedTree.from_stream(f)
        f.close

        f = open(filename, "r", encoding="utf-8")
        trees_actual = Tree.from_stream(f)
        f.close

        counter = 0
        passed = 0
        failed = 0
        for t_expect, t_actual in zip(trees_expect, trees_actual):
            counter += 1
            print('Collapse Unary - TEST ' + str(counter) + ': ', end='')

            # Get a copy of the tree before unary collapse
            t_before = Tree.pretty(t_actual)

            # Get expected tree after collapse from solution
            col_tree_expect = ExpectedTree.collapse_unary(t_expect)
            expect = ExpectedTree.pretty(col_tree_expect)

            # Get actual tree after collapse from tree.py
            col_tree_actual = Tree.kidnap_daughter(t_actual)
            actual = Tree.pretty(col_tree_actual)

            # Compare results and print full report of any failed trees
            try:
                eq_(expect, actual)
                passed += 1
                print(" PASS")
                if VERBOSE:
                    print('////////////////////////////////////////////////////////////////////')
                    print('Collapse Unary - TEST: ' + str(counter) + ': PASS *********************************')
                    print(t_before)
                    print('EXPECTED: *************************')
                    print(expect)
                    print('ACTUAL *************************')
                    print(actual)

            except AssertionError:
                failed += 1
                print(" FAIL")
                if VERBOSE:
                    print('////////////////////////////////////////////////////////////////////')
                    print('Collapse Unary - TEST: ' + str(counter) + ': FAIL ************************************')
                    print(t_before)
                    print('EXPECTED: *************************')
                    print(expect)
                    print('ACTUAL *************************')
                    print(actual)

        print("Passed: " + str(passed))
        print("Failed: " + str(failed))
        if failed > 0:
            raise AssertionError

    # This tests  with all 14,898 in the WSJ test file
    # Note: This takes about a minute
    def test_convert_cnf_WSJ(self):
        filename = "wsj-normalized.psd"
        #filename = "wsj-test.psd"
        f = open(filename, "r", encoding="utf-8")
        trees_expect = ExpectedTree.from_stream(f)
        f.close

        f = open(filename, "r", encoding="utf-8")
        trees_actual = Tree.from_stream(f)
        f.close

        counter = 0
        passed = 0
        failed = 0
        for t_expect, t_actual in zip(trees_expect, trees_actual):
            counter += 1
            print('Convert CNF - TEST ' + str(counter) + ': ', end='')

            # Get a copy of the tree before unary collapse
            t_before = Tree.pretty(t_actual)

            # Get expected tree after collapse from solution
            col_tree = ExpectedTree.collapse_unary(t_expect)
            cnf_tree_expect = ExpectedTree.chomsky_normal_form(col_tree)
            expect = ExpectedTree.pretty(cnf_tree_expect)

            # Get actual tree after collapse from tree.py
            cnf_tree_actual = Tree.chomsky_normal_form(t_actual)
            actual = Tree.pretty(cnf_tree_actual)

            # Compare results and print full report of any failed trees
            try:
                eq_(expect, actual)
                passed += 1
                print(" PASS")
                if VERBOSE:
                    print('////////////////////////////////////////////////////////////////////')
                    print('Convert CNF - TEST: ' + str(counter) + '  ************************************')
                    print(t_before)
                    print('EXPECTED: *************************')
                    print(expect)
                    print('ACTUAL *************************')
                    print(actual)

            except AssertionError:
                failed += 1
                print(" FAIL")
                if VERBOSE:
                    print('////////////////////////////////////////////////////////////////////')
                    print('Convert CNF - TEST: ' + str(counter) + '  ************************************')
                    print(t_before)
                    print('EXPECTED: *************************')
                    print(expect)
                    print('ACTUAL *************************')
                    print(actual)
                    print('----')

        print("Passed: " + str(passed))
        print("Failed: " + str(failed))
        if failed > 0:
            raise AssertionError

    # This tests  with all 14,898 in the WSJ test file
    # Note: This takes about a minute
    def test_productions_WSJ(self):
        #filename = "wsj-normalized.psd"
        filename = "wsj-test.psd"
        f = open(filename, "r", encoding="utf-8")
        trees_expect = ExpectedTree.from_stream(f)
        f.close

        f = open(filename, "r", encoding="utf-8")
        trees_actual = Tree.from_stream(f)
        f.close

        counter = 0
        passed = 0
        failed = 0
        for t_expect, t_actual in zip(trees_expect, trees_actual):
            counter += 1
            print('Productions - TEST ' + str(counter) + ': ', end='')

            # Get a copy of the tree before unary collapse
            t_before = Tree.pretty(t_actual)

            # Get expected tree after collapse from solution
            t_expect_col = ExpectedTree.collapse_unary(t_expect)
            t_expect_cnf = ExpectedTree.chomsky_normal_form(t_expect_col)
            t_expect_pro = ExpectedTree.productions(t_expect_cnf)
            expect = ExpectedTree.pretty_productions(t_expect_pro)
            #expect = ExpectedTree.pretty(t_expect_cnf)

            # Get actual tree after collapse from tree.py
            t_actual_col = Tree.collapse_unary(t_actual)
            t_actual_cnf = Tree.chomsky_normal_form(t_actual_col)
            t_actual_pro = Tree.productions(t_actual_cnf)
            actual = Tree.pretty_productions(t_actual_pro)

            # Compare results and print full report of any failed trees
            try:
                eq_(expect, actual)
                passed += 1
                print(" PASS")
                if VERBOSE:
                    print('////////////////////////////////////////////////////////////////////')
                    print('Generate Productions - TEST: ' + str(counter) + '  ************************************')
                    print(t_before)
                    print('EXPECTED: *************************')
                    print(expect)
                    print('ACTUAL *************************')
                    print(actual)

            except AssertionError:
                failed += 1
                print(" FAIL")
                if VERBOSE:
                    print('////////////////////////////////////////////////////////////////////')
                    print('Generate Productions - TEST: ' + str(counter) + '  ************************************')
                    print(t_before)
                    print('EXPECTED: *************************')
                    print(expect)
                    print('ACTUAL *************************')
                    print(actual)
                    print('----')

        print("Passed: " + str(passed))
        print("Failed: " + str(failed))
        if failed > 0:
            raise AssertionError

    def get_before_and_expected_values_from_WSF(self, tree_index, actual):
        filename = "wsj-normalized.psd"
        #filename = "wsj-test.psd"
        f = open(filename, "r", encoding="utf-8")
        trees_expect = ExpectedTree.from_stream(f)
        f.close

        f = open(filename, "r", encoding="utf-8")
        trees_actual = Tree.from_stream(f)
        f.close

        counter = 0
        for t_expect, t_actual in zip(trees_expect, trees_actual):
            counter += 1

            if counter == tree_index:
                print('Convert CNF - TEST ' + str(counter) + ': ', end='')

                before = Tree.pretty(t_actual)

                # Get expected and tree after collapse from solution
                t_expect_unary = ExpectedTree.collapse_unary(t_expect)
                t_expect_cnf = ExpectedTree.chomsky_normal_form(t_expect_unary)
                t_expect_prod = ExpectedTree.productions(t_expect_cnf)

                expect_unary = ExpectedTree.pretty(t_expect_unary)
                expect_cnf = ExpectedTree.pretty(t_expect_cnf)
                expect_prod = ExpectedTree.pretty_productions(t_expect_prod)

                print('// BEFORE VALUE ////////////////////////////////////////////////////////////////////////')
                print('WSJ TREE (BEFORE) #' + str(counter) + '  ************************************')
                print(before)

                print('// EXPECTED VALUES ////////////////////////////////////////////////////////////////////////')
                print('EXPECTED UNARY COLLAPSE #' + str(counter) + '  ************************************')
                print(expect_unary)
                print('EXPECTED Convert CNF - TEST: ' + str(counter) + '  ************************************')
                print(expect_cnf)
                print('EXPECTED Generate Productions: ' + str(counter) + '  ************************************')
                print(expect_prod)

                if actual:
                    # The order fucks this up
                    t_actual_unary = Tree.collapse_unary(t_actual)
                    actual_unary = Tree.pretty(t_actual_unary)

                    t_actual_cnf = Tree.chomsky_normal_form(t_actual_unary)
                    actual_cnf = Tree.pretty(t_actual_cnf)

                    t_actual_prod = Tree.productions(t_actual_unary)
                    actual_prod = Tree.pretty_productions(t_actual_prod)

                    print('// ACTUAL /////////////////////////////////////////////////////////////////////////////////')
                    print('ACTUAL UNARY COLLAPSE #' + str(counter) + '  ************************************')
                    print(actual_unary)
                    print('ACTUAL Convert CNF - TEST: ' + str(counter) + '  ************************************')
                    print(actual_cnf)
                    print('ACTUAL Generate Productions: ' + str(counter) + '  ************************************')
                    print(actual_prod)

                    eq_(expect_unary, actual_unary)
                    eq_(expect_cnf, actual_cnf)
                    eq_(expect_prod, actual_prod)

                break

    def test_set_productions_WSJ(self):
        #filename = "wsj-normalized.psd"
        filename = "wsj-test.psd"
        f = open(filename, "r", encoding="utf-8")
        trees_expect = ExpectedTree.from_stream(f)
        f.close

        f = open(filename, "r", encoding="utf-8")
        trees_actual = Tree.from_stream(f)
        f.close

        counter = 0
        passed = 0
        failed = 0

        t_expect_pro = []
        t_actual_pro = []

        for t_expect, t_actual in zip(trees_expect, trees_actual):
            counter += 1
            #print('Productions SET - TEST ' + str(counter) + ': ', end='')

            # Get a copy of the tree before unary collapse
            t_before = Tree.pretty(t_actual)

            # Get expected tree after collapse from solution
            t_expect_col = ExpectedTree.collapse_unary(t_expect)
            t_expect_cnf = ExpectedTree.chomsky_normal_form(t_expect_col)
            t_expect_pro += ExpectedTree.productions(t_expect_cnf)

            #expect = ExpectedTree.pretty(t_expect_cnf)

            # Get actual tree after collapse from tree.py
            t_actual_col = Tree.collapse_unary(t_actual)
            t_actual_cnf = Tree.chomsky_normal_form(t_actual_col)
            t_actual_pro += Tree.productions(t_actual_cnf)

        expect = ExpectedTree.pretty_productions(t_expect_pro)
        actual = Tree.pretty_productions(t_actual_pro)

        # Compare results and print full report of any failed trees
        try:
            eq_(expect, actual)
            passed += 1
            print(" PASS")
            if VERBOSE:
                print('////////////////////////////////////////////////////////////////////')
                print('Productions SET - TEST: ' + str(counter) + '  ************************************')
                #print(t_before)
                print('EXPECTED: *************************')
                print(expect)
                print('ACTUAL *************************')
                print(actual)

        except AssertionError:
            failed += 1
            print(" FAIL")
            if VERBOSE:
                print('////////////////////////////////////////////////////////////////////')
                print('Productions SET - TEST: ' + str(counter) + '  ************************************')
                #print(t_before)
                print('EXPECTED: *************************')
                print(expect)
                print('ACTUAL *************************')
                print(actual)
                print('----')

        print("Passed: " + str(passed))
        print("Failed: " + str(failed))
        if failed > 0:
            raise AssertionError

    def test_load_rules_WSJ_small(self):
        #filename = "wsj-normalized.psd"
        filename = "wsj-test.psd"
        f = open(filename, "r", encoding="utf-8")
        trees_expect = ExpectedTree.from_stream(f)
        f.close

        counter = 0
        passed = 0
        failed = 0

        expect_rules = []
        t_actual_pro = []

        for t_expect in trees_expect:
            counter += 1
            #print('Productions SET - TEST ' + str(counter) + ': ', end='')

            # Get a copy of the tree before unary collapse
            #t_before = Tree.pretty(t_actual)

            # Get expected tree after collapse from solution
            t_expect_col = ExpectedTree.collapse_unary(t_expect)
            t_expect_cnf = ExpectedTree.chomsky_normal_form(t_expect_col)
            expect_rules += ExpectedTree.productions(t_expect_cnf)

        expect = ExpectedTree.pretty_productions(expect_rules)

        actual_rules = Tree.load_rules(filename)
        actual = Tree.pretty_productions(actual_rules)


        # Compare results and print full report of any failed trees
        try:
            eq_(expect, actual)
            passed += 1
            print(" PASS")
            if VERBOSE:
                print('////////////////////////////////////////////////////////////////////')
                print('Load Rules - TEST: ' + str(counter) + '  ************************************')
                #print(t_before)
                print('EXPECTED: *************************')
                print(expect)
                print('ACTUAL *************************')
                print(actual)

        except AssertionError:
            failed += 1
            print(" FAIL")
            if VERBOSE:
                print('////////////////////////////////////////////////////////////////////')
                print('Load Rules - TEST: ' + str(counter) + '  ************************************')
                #print(t_before)
                print('EXPECTED: *************************')
                print(expect)
                print('ACTUAL *************************')
                print(actual)
                print('----')

        print("Passed: " + str(passed))
        print("Failed: " + str(failed))
        if failed > 0:
            raise AssertionError

class TestProductionsRegression(unittest.TestCase):

    def pretty_productions_cnf(self, cnf):
        rules = ''
        for (mother, daughters) in cnf.productions():
            #print('{: <20} -> {}'.format(mother, ' '.join(daughters)))
            rules += format('{: <20} -> {}\n'.format(mother, ' '.join(daughters)))

        rules = os.linesep.join([st for st in rules.splitlines() if st])
        return rules

    def pretty_productions(self, t_prod):
        rules = ''
        for (mother, daughters) in t_prod:
            rules += format('{: <20} -> {}\n'.format(mother, ' '.join(daughters)))

        rules = os.linesep.join([st for st in rules.splitlines() if st])
        return rules

    def test_productions_inline1_EXPECT(self):
        s = inspect.cleandoc("""
            (TOP (S (S (VP (VBN Turned) (ADVP (RB loose)) (PP
            (IN in) (NP (NP (NNP Shane) (NNP Longman) (POS 's))
            (NN trading) (NN room))))) (, ,) (NP (DT the)
            (NN yuppie) (NNS dealers)) (VP (AUX do) (NP (NP
            (RB little)) (ADJP (RB right)))) (. .)))""")

        #t_before = Tree.from_string(s)
        t_before = ExpectedTree.from_string(s)

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
        expect = os.linesep.join([st for st in expect.splitlines() if st])

        print('EXPECTED: *************************')
        print(expect)

        # Actual Value
        t_col = t_before.collapse_unary()
        t_cnf = t_col.chomsky_normal_form()
        t_pro = t_cnf.productions()

        print('ACTUAL *************************')
        # #t = ExpectedTree.from_string(s).collapse_unary().chomsky_normal_form()
        # t = t_cnf
        #
        # actual = ''
        # for (mother, daughters) in t.productions():
        #     #print('{: <20} -> {}'.format(mother, ' '.join(daughters)))
        #     actual += format('{: <20} -> {}\n'.format(mother, ' '.join(daughters)))
        #
        # actual = os.linesep.join([st for st in actual.splitlines() if st])

        actual = self.pretty_productions(t_pro)

        print(actual)

        eq_(expect, actual)

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

        t_before = ExpectedTree.from_string(s)

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
        t_prod = t_cnf.productions()

        print('ACTUAL *************************')
        #actual = self.pretty_productions(t_prod)
        actual = ExpectedTree.pretty_productions(t_prod)
        print(actual)

        eq_(actual, expect)

class TestBuildRegressionTools(unittest.TestCase):

    def test_get_before_and_expected_values_from_WSF(self):
        TestTreeRegression.get_before_and_expected_values_from_WSF(self, 94, True)

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
