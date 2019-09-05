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
from cyk import Cyk

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

    def test_python_ranges(self):

        s = "the teacher gave the lecture"
        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        step = 0
        for x in range(n):
            for y in range(x, -1, -1):
                step += 1
                #table.iloc[x - 1, y] = str(step) + ": " + str(x - 1) + ', ' + str(y)
                table.iloc[x, y] = str(step)
                #print(f"x,y: {x},{y}")

                print(table)


        # step = 0
        # for x in range(n):
        #     for y in range(x, -1, -1):
        #         step += 1
        #         #table.iloc[x - 1, y] = str(step) + ": " + str(x - 1) + ', ' + str(y)
        #         table.iloc[x, y] = str(step)
        #         #print(f"x,y: {x},{y}")
        #
        #         print(table)
