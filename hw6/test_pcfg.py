# test_pcfg.py: pcfg unit tests for tree.py
# Author: Steve Braich

import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
import inspect
import os
from io import StringIO
import logging
from collections import defaultdict
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

# Chomsky Normal Form Unit Tests
class TestPcfg(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    # PCFG - Inline test #1
    def test_default_collections(self):

        data = [
                    ('TOP', ['NP', 'VP', '.']),
                    ('NP', ['DT', 'NN']),
                    ('DT', ['the']),
                    ('NN', ['teacher']),
                    ('VP', ['MD', 'VP']),
                    ('MD', ['will']),
                    ('VP', ['VB', 'NP']),
                    ('VB', ['lecture']),
                    ('NP', ['NN', 'PP']),
                    ('NN', ['today']),
                    ('PP', ['IN', 'NP']),
                    ('IN', ['in']),
                    ('NP', ['DT', 'NN', 'NN']),
                    ('DT', ['the']),
                    ('NN', ['lecture']),
                    ('NN', ['hall']),
                    ('.', ['.'])
                ]

        pcfg = defaultdict(dict)
        for nonterminal, rhs in data:
            try:
                pcfg[nonterminal]['rhs'].add(tuple(rhs))
                pcfg[nonterminal]['probability'] = 1 / len(pcfg[nonterminal]['rhs'])
            except:
                pcfg[nonterminal].setdefault('rhs', set()).add(tuple(rhs))
                pcfg[nonterminal].setdefault('probability', 1)

        print(dict(pcfg))

    def test_convert_to_pcfg_inline1(self):
        s = inspect.cleandoc("""
            (TOP
                (NP
                  (DT the)
                  (NN teacher)
                )
                (VP
                  (MD will)
                  (VP
                    (VB lecture)
                    (NP
                      (NN today)
                      (PP
                          (IN in)
                          (NP
                            (DT the)
                            (NN lecture)
                            (NN hall)
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

        # counts['NP'][('DT','NN')] / sum(counts['NP'].values())
        print('EXPECTED: *************************')


        # blah = {'TOP': {('NP', 'VP', '.'): 1}, 'NP': {('DT', 'NN'): 1, ('NN', 'PP'): 1, ('DT', 'NN', 'NN'): 1}, 'DT': {('the',): 1}, 'NN': {('teacher',): 1, ('today',): 1, ('lecture',): 1, ('hall',): 1}, 'VP': {('MD', 'VP'): 1, ('VB', 'NP'): 1}, 'MD': {('will',): 1}, 'VB': {('lecture',): 1}, 'PP': {('IN', 'NP'): 1}, 'IN': {('in',): 1}, '.': {('.',): 1}}
        # pcfg_expect = {
        #     'TOP': {
        #         ('NP', 'VP', '.'): 1.0
        #     },
        #     'NP': {
        #         ('DT', 'NN'): 0.3333333333333333,
        #         ('NN', 'PP'): 0.3333333333333333,
        #         ('DT', 'NN', 'NN'): 0.3333333333333333,
        #     },
        #     'DT': {
        #         ('the',): 1.0
        #     },
        #     'NN': {
        #         ('teacher',): 0.25,
        #         ('today',): 0.25,
        #         ('lecture',): 0.25,
        #         ('hall',): 0.25,
        #     },
        #     'VP': {
        #         ('MD', 'VP'): 0.5,
        #         ('VB', 'NP'): 0.5,
        #     },
        #     'MD': {
        #         ('will',): 1.0
        #     },
        #     'VB': {
        #         ('lecture',): 1.0
        #     },
        #     'PP': {
        #         ('IN', 'NP'): 1.0
        #     },
        #     'IN': {
        #         ('in',): 1.0
        #     },
        #     '.': {
        #         ('.',): 1.0
        #     }
        # }

        pcfg_expect = {
            ('TOP', ('NP', 'VP', '.')): 1.0,
            ('NP', ('DT', 'NN')): 0.3333333333333333,
            ('NP', ('NN', 'PP')): 0.3333333333333333,
            ('NP', ('DT', 'NN', 'NN')): 0.3333333333333333,
            ('DT', ('the',)): 1.0,
            ('NN', ('teacher',)): 0.25,
            ('NN', ('today',)): 0.25,
            ('NN', ('lecture',)): 0.25,
            ('NN', ('hall',)): 0.25,
            ('VP', ('MD', 'VP')): 0.5,
            ('VP', ('VB', 'NP')): 0.5,
            ('MD', ('will',)): 1.0,
            ('VB', ('lecture',)): 1.0,
            ('PP', ('IN', 'NP')): 1.0,
            ('IN', ('in',)): 1.0,
            ('.',  ('.',)): 1.0
        }

        expect = "defaultdict(<class 'dict'>, " + format(pcfg_expect) + ")"
        print(expect)

        print('ACTUAL *************************')
        rules = Tree.productions(t_before)
        pcfg_actual = Tree.convert_to_pcfg(rules)
        actual = format(pcfg_actual)
        print(actual)

        eq_(actual, expect)

    def test_pcfg_terminal_lookup1(self):

        pcfg = {
            ('TOP', ('NP', 'VP', '.')): 1.0,
            ('NP', ('DT', 'NN')): 0.3333333333333333,
            ('NP', ('NN', 'PP')): 0.3333333333333333,
            ('NP', ('DT', 'NN', 'NN')): 0.3333333333333333,
            ('DT', ('the',)): 1.0,
            ('NN', ('teacher',)): 0.25,
            ('NN', ('today',)): 0.25,
            ('NN', ('lecture',)): 0.25,
            ('NN', ('hall',)): 0.25,
            ('VP', ('MD', 'VP')): 0.5,
            ('VP', ('VB', 'NP')): 0.5,
            ('MD', ('will',)): 1.0,
            ('VB', ('lecture',)): 1.0,
            ('PP', ('IN', 'NP')): 1.0,
            ('IN', ('in',)): 1.0,
            ('.',  ('.',)): 1.0
        }

        sentence = "the teacher gave the lecture"
        words = sentence.split(' ')
        w = "the"

        print("List Comprehension: lhs")
        actual = [key[0] for key, value in pcfg.items() if w in key[1]]
        expect = ['DT']

        eq_(actual, expect)

    def test_pcfg_terminal_lookup2(self):

        pcfg = {
            ('TOP', ('NP', 'VP', '.')): 1.0,
            ('NP', ('DT', 'NN')): 0.3333333333333333,
            ('NP', ('NN', 'PP')): 0.3333333333333333,
            ('NP', ('DT', 'NN', 'NN')): 0.3333333333333333,
            ('DT', ('the',)): 1.0,
            ('NN', ('teacher',)): 0.25,
            ('NN', ('today',)): 0.25,
            ('NN', ('lecture',)): 0.25,
            ('NN', ('hall',)): 0.25,
            ('VP', ('MD', 'VP')): 0.5,
            ('VP', ('VB', 'NP')): 0.5,
            ('MD', ('will',)): 1.0,
            ('VB', ('lecture',)): 1.0,
            ('PP', ('IN', 'NP')): 1.0,
            ('IN', ('in',)): 1.0,
            ('.',  ('.',)): 1.0
        }

        # nonterminal = list(self.pcfg.keys())[list(self.pcfg.values()).index(tuple([words[i]]))]
        sentence = "the teacher gave the lecture"
        words = sentence.split(' ')
        w = "the"

        keys = pcfg.keys()
        vals = pcfg.values()

        lst_keys = list(keys)
        lst_vals = list(vals)

        #nonterminal = list(pcfg.keys())[list(pcfg.values()).index(tuple([w]))]

        search = {('the',): 1.0}

        print("List Comprehension: lhs")
        lhs = [key[0] for key, value in pcfg.items() if w in key[1]]
        print(lhs)

        #lhs = [key for key, value in pcfg.items() if w in value]
        lhs = [key for key, value in pcfg.items()]
        rhs = [value for key, value in pcfg.items()]
        #lhs = [key for key, value in pcfg.items() if search in value]
        print("List Comprehension: lhs")
        print(lhs)
        print("List Comprehension: rhs")
        print(rhs)


        for rule, probability in pcfg.items():
            #print("\nLHS: {} -----> rhs {}", lhs, rhs)
            print(f"LHS: {rule[0]} -----> rhs {rule[1]}: {probability}")

            # for key in rhs:
            #     print('rhs KEY: ' + str(key) + ':', rhs[key])


        #expect = format(pcgf_expect)
        expect = "defaultdict(<class 'dict'>, " + format(pcfg) + ")"
        print(expect)

        # print('ACTUAL *************************')
        # rules = Tree.productions(t_before)
        # pcfg_actual = Tree.convert_to_pcfg(rules)
        # actual = format(pcfg_actual)
        # print(actual)
        #
        # eq_(actual, expect)

    def test_pretty_pcfg_inline1(self):

        pcfg = {
            ('TOP', ('NP', 'VP', '.')): 1.0,
            ('NP', ('DT', 'NN')): 0.3333333333333333,
            ('NP', ('NN', 'PP')): 0.3333333333333333,
            ('NP', ('DT', 'NN', 'NN')): 0.3333333333333333,
            ('DT', ('the',)): 1.0,
            ('NN', ('teacher',)): 0.25,
            ('NN', ('today',)): 0.25,
            ('NN', ('lecture',)): 0.25,
            ('NN', ('hall',)): 0.25,
            ('VP', ('MD', 'VP')): 0.5,
            ('VP', ('VB', 'NP')): 0.5,
            ('MD', ('will',)): 1.0,
            ('VB', ('lecture',)): 1.0,
            ('PP', ('IN', 'NP')): 1.0,
            ('IN', ('in',)): 1.0,
            ('.',  ('.',)): 1.0
        }

        print('BEFORE: *************************')
        before = format(pcfg)
        print(before)

        # Expected Value
        expect = inspect.cleandoc("""     
            TOP                  -> NP VP . 1.0
            NP                   -> DT NN 0.3333333333333333
            NP                   -> NN PP 0.3333333333333333
            NP                   -> DT NN NN 0.3333333333333333
            DT                   -> the 1.0
            NN                   -> teacher 0.25
            NN                   -> today 0.25
            NN                   -> lecture 0.25
            NN                   -> hall 0.25
            VP                   -> MD VP 0.5
            VP                   -> VB NP 0.5
            MD                   -> will 1.0
            VB                   -> lecture 1.0
            PP                   -> IN NP 1.0
            IN                   -> in 1.0
            .                    -> . 1.0""")

        print('EXPECTED: *************************')
        expect = os.linesep.join([st for st in expect.splitlines() if st])
        print(expect)

        print('ACTUAL *************************')
        actual = Tree.pretty_pcgf(pcfg)
        print(actual)

        eq_(actual, expect)

    def test_INTEGRATION_pretty_pcfg_inline1(self):
        s = inspect.cleandoc("""
            (TOP
                (NP
                  (DT the)
                  (NN teacher)
                )
                (VP
                  (MD will)
                  (VP
                    (VB lecture)
                    (NP
                      (NN today)
                      (PP
                          (IN in)
                          (NP
                            (DT the)
                            (NN lecture)
                            (NN hall)
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
            TOP                  -> NP VP . 1.0
            NP                   -> DT NN 0.3333333333333333
            NP                   -> NN PP 0.3333333333333333
            NP                   -> DT NN NN 0.3333333333333333
            DT                   -> the 1.0
            NN                   -> teacher 0.25
            NN                   -> today 0.25
            NN                   -> lecture 0.25
            NN                   -> hall 0.25
            VP                   -> MD VP 0.5
            VP                   -> VB NP 0.5
            MD                   -> will 1.0
            VB                   -> lecture 1.0
            PP                   -> IN NP 1.0
            IN                   -> in 1.0
            .                    -> . 1.0""")

        print('EXPECTED: *************************')
        expect = os.linesep.join([st for st in expect.splitlines() if st])
        print(expect)

        print('ACTUAL *************************')
        rules = Tree.productions(t_before)
        pcfg = Tree.convert_to_pcfg(rules)
        actual = Tree.pretty_pcgf(pcfg)
        print(actual)

        eq_(actual, expect)

    def test_convert_to_pcfg_WSJ_small(self):
        #filename = "wsj-normalized.psd"
        filename = "wsj-test.psd"

        actual_rules = Tree.load_rules(filename)
        actual_rules_pretty = Tree.pretty_productions(actual_rules)

        print('ACTUAL *************************')
        pcfg = Tree.convert_to_pcfg(actual_rules)
        actual = Tree.pretty_pcgf(pcfg)
        print(actual)

    def test_convert_to_pcfg_bigger_treebank2(self):
        # filename = "wsj-normalized.psd"
        filename = "bigger_treebank_2.txt"

        actual_rules = Tree.load_rules(filename)
        #actual_rules_pretty = Tree.pretty_productions(actual_rules)

        print('ACTUAL *************************')
        pcfg = Tree.convert_to_pcfg(actual_rules)
        actual = Tree.pretty_pcgf(pcfg)
        print(actual)
        #eq_(actual, expect)
