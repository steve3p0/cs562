# test_cyk.py: pcfg unit tests for tree.py
# Author: Steve Braich

import unittest
from nose.tools import eq_, assert_almost_equals, assert_greater_equal
import inspect
import pandas
import os
from io import StringIO
import logging
from collections import defaultdict
from cyk import Cyk, Node
from tree import Tree

# Chomsky Normal Form Unit Tests
class TestCyk(unittest.TestCase):

    def setUp(self):
        # This is where you.. set up things...
        #logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)

    def test_convert_to_pcfg_inline1(self):
        cyk = Cyk()

        #cyk.rules = cyk.load_rules('')
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

        t_before = cyk.tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

        # counts['NP'][('DT','NN')] / sum(counts['NP'].values())
        print('EXPECTED: *************************')

        # blah = {'TOP': {('NP', 'VP', '.'): 1}, 'NP': {('DT', 'NN'): 1, ('NN', 'PP'): 1, ('DT', 'NN', 'NN'): 1}, 'DT': {('the',): 1}, 'NN': {('teacher',): 1, ('today',): 1, ('lecture',): 1, ('hall',): 1}, 'VP': {('MD', 'VP'): 1, ('VB', 'NP'): 1}, 'MD': {('will',): 1}, 'VB': {('lecture',): 1}, 'PP': {('IN', 'NP'): 1}, 'IN': {('in',): 1}, '.': {('.',): 1}}
        pcfg_expect = {
            'TOP': {
                ('NP', 'VP', '.'): 1.0
            },
            'NP': {
                ('DT', 'NN'): 0.3333333333333333,
                ('NN', 'PP'): 0.3333333333333333,
                ('DT', 'NN', 'NN'): 0.3333333333333333,
            },
            'DT': {
                ('the',): 1.0
            },
            'NN': {
                ('teacher',): 0.25,
                ('today',): 0.25,
                ('lecture',): 0.25,
                ('hall',): 0.25,
            },
            'VP': {
                ('MD', 'VP'): 0.5,
                ('VB', 'NP'): 0.5,
            },
            'MD': {
                ('will',): 1.0
            },
            'VB': {
                ('lecture',): 1.0
            },
            'PP': {
                ('IN', 'NP'): 1.0
            },
            'IN': {
                ('in',): 1.0
            },
            '.': {
                ('.',): 1.0
            }
        }
        #expect = format(pcgf_expect)
        expect = "defaultdict(<class 'dict'>, " + format(pcfg_expect) + ")"
        print(expect)

        print('ACTUAL *************************')
        rules = cyk.tree.productions(t_before)
        pcfg_actual = cyk.tree.convert_to_pcfg(rules)
        actual = format(pcfg_actual)
        print(actual)

        eq_(actual, expect)

    def test_convert_to_pcfg_bigger_treebank2(self):
        cyk = Cyk()
        # filename = "wsj-normalized.psd"
        filename = "bigger_treebank_2.txt"

        actual_rules = cyk.tree.load_rules(filename)
        #actual_rules_pretty = Tree.pretty_productions(actual_rules)

        print('ACTUAL *************************')
        pcfg = cyk.tree.convert_to_pcfg(actual_rules)
        actual = cyk.tree.pretty_pcgf(pcfg)
        print(actual)
        #eq_(actual, expect)

    def test_cyk_parse_small(self):
        cyk = Cyk()

        # rules = [
        #     ('S', ['NP', 'VP', '.']),
        #     ('NP', ['DET', 'N']),
        #     ('NP', ['NP', 'PP']),
        #     ('PP', ['P', 'NP']),
        #     ('VP', ['VP', 'PP']),
        #     ('VP', ['saw']),
        #     ('DET', ['the']),
        #     ('NP', ['I']),
        #     ('N', ['man']),
        #     ('N', ['telescope']),
        #     ('P', ['with']),
        #     ('V', ['saw']),
        #     ('N', ['cat']),
        #     ('N', ['dog']),
        #     ('N', ['pig']),
        #     ('N', ['hill']),
        #     ('N', ['park']),
        #     ('N', ['roof']),
        #     ('P', ['from']),
        #     ('P', ['on']),
        #     ('P', ['in'])
        # ]

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]

        pcfg = cyk.tree.convert_to_pcfg(rules)
        cyk.rules = rules
        cyk.pcfg = pcfg
        pcfg_pretty = cyk.tree.pretty_pcgf(pcfg)
        #actual = format(pcfg)
        print(pcfg_pretty)

        #sentence = "I saw the man with the telescope on the hill"
        #sentence = "I saw"
        sentence = "the teacher gave the lecture"

        cyk.parse(sentence)

        #eq_(actual, expect)

    def test_cyk_parse_small_valid1(self):

        s = "the teacher gave the lecture"
        #s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]

        print("Expected Parse Tree: ")
        expect_parse_tree = inspect.cleandoc("""
            (S
                (NP
                    (DT the)
                    (NN teacher)
                )
                (VP
                    (VB gave)
                    (NP
                        (DT the)
                        (NN lecture)
                    )
                )
            )""")
        expect_parse_tree = os.linesep.join([st for st in expect_parse_tree.splitlines() if st])
        expect_tree = Tree.from_string(expect_parse_tree)
        expect_parse_tree = expect_tree.pretty()
        print(expect_parse_tree)

        cyk = Cyk()
        cyk.rules = rules
        cyk.parse(s)

        print("Actual Parse Tree: ")
        print(cyk.parse_tree)

        eq_(cyk.valid, True)
        eq_(cyk.parse_tree, expect_parse_tree)

    def test_cyk_parse_small_valid2(self):

        s = "the lecture gave the teacher"
        #s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]

        print("Expected Parse Tree: ")
        expect_parse_tree = inspect.cleandoc("""
            (S
                (NP
                    (DT the)
                    (NN lecture)
                )
                (VP
                    (VB gave)
                    (NP
                        (DT the)
                        (NN teacher)
                    )
                )
            )""")
        expect_parse_tree = os.linesep.join([st for st in expect_parse_tree.splitlines() if st])
        expect_tree = Tree.from_string(expect_parse_tree)
        expect_parse_tree = expect_tree.pretty()
        print(expect_parse_tree)

        cyk = Cyk()
        cyk.rules = rules
        cyk.parse(s)

        print("Actual Parse Tree: ")
        print(cyk.parse_tree)

        eq_(cyk.valid, True)
        eq_(cyk.parse_tree, expect_parse_tree)

    def test_cyk_parse_small_invalid1(self):

        #s = "the teacher gave the lecture"
        s = "gave lecture the teacher the"
        #s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]

        cyk = Cyk()
        cyk.rules = rules
        cyk.parse(s)

        eq_(cyk.valid, False)
        eq_(cyk.parse_tree, '')

    def test_cyk_parse_small_invalid2(self):

        #s = "the teacher gave the lecture"
        #s = "gave lecture the teacher the"
        s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]

        cyk = Cyk()
        cyk.rules = rules
        cyk.parse(s)

        eq_(cyk.valid, False)
        eq_(cyk.parse_tree, '')

    def test_cyk_parse_small_invalid3(self):

        #s = "the teacher gave the lecture"
        #s = "gave lecture the teacher the"
        #s = "the the teacher gave the lecture"
        s = "teacher the gave the lecture"

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]

        cyk = Cyk()
        cyk.rules = rules
        cyk.parse(s)

        eq_(cyk.valid, False)
        eq_(cyk.parse_tree, '')

    # CYK - with Probabilities
    def test_cyk_parse_small_valid1(self):

        s = "the teacher gave the lecture"
        #s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]

        print("Expected Parse Tree: ")
        expect_parse_tree = inspect.cleandoc("""
            (S
                (NP
                    (DT the)
                    (NN teacher)
                )
                (VP
                    (VB gave)
                    (NP
                        (DT the)
                        (NN lecture)
                    )
                )
            )""")
        expect_parse_tree = os.linesep.join([st for st in expect_parse_tree.splitlines() if st])
        expect_tree = Tree.from_string(expect_parse_tree)
        expect_parse_tree = expect_tree.pretty()
        print(expect_parse_tree)

        cyk = Cyk()
        cyk.rules = rules
        cyk.parse(s)

        print("Actual Parse Tree: ")
        print(cyk.parse_tree)

        eq_(cyk.valid, True)
        eq_(cyk.parse_tree, expect_parse_tree)