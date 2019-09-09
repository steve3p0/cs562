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

    def test_cyk_parse(self):

        cyk = Cyk()

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]
        start_symbol = next(iter(rules))[0]

        pcfg = cyk.tree.convert_to_pcfg(rules)
        cyk.rules = rules
        cyk.pcfg = pcfg
        pcfg_pretty = cyk.tree.pretty_pcgf(pcfg)
        #actual = format(pcfg)
        print(pcfg_pretty)

        s = "the teacher gave the lecture"
        #s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        rhs_left = ''
        rhs_right = ''

        for y in range(n):
            for x in range(y, -1, -1):
                # RHS - Right
                rhs_right = [key[0] for key, value in pcfg.items() if words[y] in key[1]][0]
                table.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and table.iloc[x-1, y] == '':
                        lhs_word = lhs[0]
                        table.iloc[x-1, y] = lhs[0]

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x  - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if table.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = table.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and table.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            table.iloc[x - x_offset, y] = lhs[0]

                            #print(table)

                rhs_left = rhs_right

                #print(table)

        print(table)
        #expect = 'S'
        expect_start_symbol = start_symbol
        actual_start_symbol = table.iloc[0, n - 1]
        eq_(actual_start_symbol, expect_start_symbol)

        # Generate Parse Tree
        #parse_tree = table.iloc[0, n - 1] + '\n'

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

        root = Node(table.iloc[0, n-1])
        root.x = 0
        root.y = n - 1
        parse_tree = cyk.get_parse_tree(table, root)

        s_parse_tree = ''
        s_parse_tree = cyk.print_parse_tree(root, s_parse_tree)

        parse_tree = os.linesep.join([st for st in s_parse_tree.splitlines() if st])

        actual_tree = Tree.from_string(parse_tree)
        actual_parse_tree = actual_tree.pretty()

        print("Actual Parse Tree: ")
        print(actual_parse_tree)

        eq_(actual_parse_tree, expect_parse_tree)


    def test_cyk_parse1(self):

        cyk = Cyk()

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
        # actual = format(pcfg)
        print(pcfg_pretty)

        s = "the teacher gave the lecture"
        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index=range(n), columns=words)
        table.fillna('', inplace=True)

        print(table)

        step = 0
        for x in range(n):
            for y in range(x, -1, -1):
                step += 1

                nt = [key[0] for key, value in pcfg.items() if words[x] in key[1]]
                nt = nt[0]
                table.iloc[x, x] = nt
                nt_prev = table.iloc[x - 1, y]
                rhs = tuple([nt_prev, nt])
                lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                if len(lhs) > 0:
                    table.iloc[x, x - 1] = lhs[0]
                    nt = lhs[0]

                # else:
                #     table.iloc[x, x - 1] = str(step)

                # # Find rule with previous terminal
                # #nt_prev = self.strip_formating(table.iloc[x - 1, x - 1])
                # nt_prev = table.iloc[x + 1, + 1]
                # rhs = tuple([nt_prev, nt[0]])
                # lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]
                #
                # if len(lhs) > 0:
                #     table.iloc[x - 1, x] = str(step) + ": " + lhs[0]
                #     nt = lhs

                # table.iloc[x - 1, y] = str(step) + ": " + str(x - 1) + ', ' + str(y)
                # table.iloc[x, y] = str(step)
                # print(f"x,y: {x},{y}")

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

    def test_cyk_parse2(self):

        cyk = Cyk()

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

        s = "the teacher gave the lecture"
        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        step = 0
        nt_loc = ''
        nt_prev = ''
        nt_prev_loc = ''
        lhs_term = ''
        lhs_loc = ''
        # for x in range(n):
        #for y in range(x, -1, -1):
        for y in range(n):
            for z in range(y, -1, -1):
                step += 1
                #table.iloc[y, z] = str(step)

                nt = [key[0] for key, value in pcfg.items() if words[y] in key[1]]
                nt = nt[0]

                rhs = tuple([nt_prev, nt])
                lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                # Set terminal cell
                if table.iloc[y, y] == '':
                    table.iloc[y, y] = nt
                    nt_loc = format(f"{y}, {y}")

                # Set LHS of Rule
                if len(lhs) > 0:
                    lhs_term = lhs[0]
                    table.iloc[y, y - 1] = lhs[0]
                    lhs_loc = format(f"{y}, {y - 1}")

                print("######################################")
                print(f"    lhs[{lhs_loc}]: {lhs_term}")
                print(f"nt_prev[{nt_prev_loc}]: {nt_prev}")
                print(f"     nt[{nt_loc}]: {nt}")
                print(f"rhs: {rhs}")
                # print(f"i: {i}")
                # print(f"j: {j}")
                # print(f"k: {k}")
                print(f"y: {y}")
                print(f"z: {z}")
                print(table)

                if len(lhs) > 0:
                    nt_loc = format(f"{y}, {y - 1}")
                    nt = lhs[0]
                # else:

                # Find nt_previous
                nt_prev = table.iloc[y - 1, z]
                nt_prev_loc = format(f"{y - 1}, {z}")
                # nt_prev = table.iloc[y, z - 1]
                # nt_prev_loc = format(f"{y}, {z - 1}")


        # step = 0
        # for x in range(n):
        #     for y in range(x, -1, -1):
        #         step += 1
        #         #table.iloc[x - 1, y] = str(step) + ": " + str(x - 1) + ', ' + str(y)
        #         table.iloc[x, y] = str(step)
        #         #print(f"x,y: {x},{y}")
        #
        #         print(table)

    def test_cyk_parse3(self):

        cyk = Cyk()

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

        s = "the teacher gave the lecture"
        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        step = 0
        nt_loc = ''
        nt_prev = ''
        nt_prev_loc = ''
        lhs_term = ''
        lhs_loc = ''
        red_term_left = ''
        # for x in range(n):
        #for y in range(x, -1, -1):

        lhs_x = 0
        lhs_y = 0
        rhs_left_x = 0
        rhs_left_y = 0
        rhs_right_x = 0
        rhs_right_y = 0

        step = 0
        for y in range(n):
            for x in range(y, -1, -1):
                step += 1
                red_term_right = format(f"R-R:{str(step)}")
                table.iloc[x, y] = red_term_right
                rhs2_ptr = table.iloc[x, y]
                rhs_right_x = x
                rhs_right_y = y

                if x > 0:
                    step += 1
                    green_lhs = format(f"G:{str(step)}")
                    table.iloc[x-1, y] = green_lhs
                    lhs_ptr = table.iloc[x-1, y]
                    lhs_x = x - 1
                    lhs_y = y

                red_term_left = format(f"R-L:{str(step)}")
                table.iloc[x, y] = red_term_left
                rh1_ptr = table.iloc[x, y]
                rhs_left_x = x
                rhs_left_y = y

                print(table)

                for z in range (y, x, -1):
                    #if x > 0:
                    step += 1
                    green_lhs = format(f"G:{str(step)}")
                    table.iloc[x, z] = green_lhs
                    lhs_ptr = table.iloc[x, z]
                    lhs_x = x
                    lhs_y = z

                    print(table)




        # for y in range(n):
        #     for z in range(y, -1, -1):
        #         step += 1
        #         #table.iloc[y, z] = str(step)
        #
        #         nt = [key[0] for key, value in pcfg.items() if words[y] in key[1]]
        #         nt = nt[0]
        #
        #         rhs = tuple([nt_prev, nt])
        #         lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]
        #
        #         # Set terminal cell
        #         if table.iloc[y, y] == '':
        #             table.iloc[y, y] = nt
        #             nt_loc = format(f"{y}, {y}")
        #
        #         # Set LHS of Rule
        #         if len(lhs) > 0:
        #             lhs_term = lhs[0]
        #             table.iloc[y, y - 1] = lhs[0]
        #             lhs_loc = format(f"{y}, {y - 1}")
        #
        #         print("######################################")
        #         print(f"    lhs[{lhs_loc}]: {lhs_term}")
        #         print(f"nt_prev[{nt_prev_loc}]: {nt_prev}")
        #         print(f"     nt[{nt_loc}]: {nt}")
        #         print(f"rhs: {rhs}")
        #         # print(f"i: {i}")
        #         # print(f"j: {j}")
        #         # print(f"k: {k}")
        #         print(f"y: {y}")
        #         print(f"z: {z}")
        #         print(table)
        #
        #         if len(lhs) > 0:
        #             nt_loc = format(f"{y}, {y - 1}")
        #             nt = lhs[0]
        #         # else:
        #
        #         # Find nt_previous
        #         nt_prev = table.iloc[y - 1, z]
        #         nt_prev_loc = format(f"{y - 1}, {z}")
        #         # nt_prev = table.iloc[y, z - 1]
        #         # nt_prev_loc = format(f"{y}, {z - 1}")


        # step = 0
        # for x in range(n):
        #     for y in range(x, -1, -1):
        #         step += 1
        #         #table.iloc[x - 1, y] = str(step) + ": " + str(x - 1) + ', ' + str(y)
        #         table.iloc[x, y] = str(step)
        #         #print(f"x,y: {x},{y}")
        #
        #         print(table)

    def test_cyk_parse4(self):

        cyk = Cyk()

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

        #s = "the teacher gave the lecture"
        #s = "the the teacher gave the lecture"
        s = "teacher the gave the lecture"

        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        step = 0
        nt_loc = ''
        nt_prev = ''
        nt_prev_loc = ''
        lhs_term = ''
        lhs_loc = ''
        red_term_left = ''
        # for x in range(n):
        #for y in range(x, -1, -1):

        rhs_left = ''
        rhs_right = ''

        lhs_x = 0
        lhs_y = 0
        rhs_left_x = 0
        rhs_left_y = 0
        rhs_right_x = 0
        rhs_right_y = 0

        step = 0
        for y in range(n):
            for x in range(y, -1, -1):
            #for x in range(n):
                step += 1

                # RHS - Right

                rhs_right = [key[0] for key, value in pcfg.items() if words[y] in key[1]][0]
                rhs_right_debug = format(f"R-R:{str(step)}")
                #table.iloc[x, y] = rhs_right_debug
                table.iloc[y, y] = rhs_right
                rhs_right_ptr = table.iloc[y, y]
                rhs_right_x = y
                rhs_right_y = y

                # LHS
                if x > 0:
                    step += 1

                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and table.iloc[x-1, y] == '':

                        #lhs_debug = format(f"G:{str(step)}")
                        #table.iloc[x-1, y] = lhs_debug
                        lhs_word = lhs[0]
                        table.iloc[x-1, y] = lhs[0]
                        lhs_ptr = table.iloc[x-1, y]
                        lhs_x = x - 1
                        lhs_y = y

                        ######## for

                        # for z in range (y, x, -1):
                        #     if x > 0:
                        #
                        #         step += 1
                        #
                        #         rhs = tuple([rhs_left, rhs_right])
                        #         lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]
                        #
                        #         if len(lhs) > 0 and table.iloc[x-1, y] == '':
                        #             #lhs_debug = format(f"G:{str(step)}")
                        #             #table.iloc[x, z] = lhs_debug
                        #             table.iloc[x - 1, y] = lhs[0]
                        #             lhs_ptr = table.iloc[x, z]
                        #             lhs_x = x
                        #             lhs_y = z

                        #if x > 0:
                        for x_offset in range(n):
                            for y_offset in range(n):

                                # # we need a x offset
                                # # we need a y offset
                                # offset_x = z
                                # offset_y = z
                                #
                                # #if len()

                                #offset = z
                                if x  - x_offset > -1:
                                    #offset = 1

                                    # RHS - RIGHT
                                    rhs_right = lhs_word
                                    rhs_right_debug = format(f"R-R:{str(step)}")
                                    # table.iloc[x, y] = rhs_right_debug
                                    #table.iloc[x - offset, y] = rhs_right
                                    #table.iloc[x - offset, y] = rhs_right
                                    rhs_right_ptr = table.iloc[x - x_offset, y - y_offset]
                                    rhs_right_x = x - x_offset
                                    rhs_right_y = y - y_offset

                                    #offset += 1

                                    # RHS - LEFT
                                    #rhs_left = [key[0] for key, value in pcfg.items() if words[y] in key[1]][0]
                                    rhs_left_debug = format(f"R-L:{str(step)}")
                                    # table.iloc[x, y] = rhs_left_debug
                                    if table.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = table.iloc[x - x_offset, y - y_offset]
                                        rhs_left_ptr = table.iloc[x - x_offset, y - y_offset]
                                        rhs_left_x = y - x_offset
                                        rhs_left_y = y - y_offset

                                    # LHS
                                    if x > -1:
                                        step += 1

                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                                        #offset += 1

                                        if len(lhs) > 0 and table.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            # lhs_debug = format(f"G:{str(step)}")
                                            # table.iloc[x-1, y] = lhs_debug
                                            table.iloc[x - x_offset, y] = lhs[0]
                                            lhs_ptr = table.iloc[x - x_offset, y]
                                            lhs_x = x - x_offset
                                            lhs_y = y
                                        # else:
                                        #     #offset -= 1
                                        #     #offset -= 1
                                        #     y += 1
                                        # #    x -= 1



                            print(table)

                rhs_left = rhs_right
                rhs_left_debug = format(f"R-L:{str(step)}")
                #table.iloc[x, y] = rhs_left_debug
                #table.iloc[x, y] = rhs_left
                rhs_left_ptr = table.iloc[x, y]
                rhs_left_x = x
                rhs_left_y = y

                print(table)


        # for y in range(n):
        #     for z in range(y, -1, -1):
        #         step += 1
        #         #table.iloc[y, z] = str(step)
        #
        #         nt = [key[0] for key, value in pcfg.items() if words[y] in key[1]]
        #         nt = nt[0]
        #
        #         rhs = tuple([nt_prev, nt])
        #         lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]
        #
        #         # Set terminal cell
        #         if table.iloc[y, y] == '':
        #             table.iloc[y, y] = nt
        #             nt_loc = format(f"{y}, {y}")
        #
        #         # Set LHS of Rule
        #         if len(lhs) > 0:
        #             lhs_term = lhs[0]
        #             table.iloc[y, y - 1] = lhs[0]
        #             lhs_loc = format(f"{y}, {y - 1}")
        #
        #         print("######################################")
        #         print(f"    lhs[{lhs_loc}]: {lhs_term}")
        #         print(f"nt_prev[{nt_prev_loc}]: {nt_prev}")
        #         print(f"     nt[{nt_loc}]: {nt}")
        #         print(f"rhs: {rhs}")
        #         # print(f"i: {i}")
        #         # print(f"j: {j}")
        #         # print(f"k: {k}")
        #         print(f"y: {y}")
        #         print(f"z: {z}")
        #         print(table)
        #
        #         if len(lhs) > 0:
        #             nt_loc = format(f"{y}, {y - 1}")
        #             nt = lhs[0]
        #         # else:
        #
        #         # Find nt_previous
        #         nt_prev = table.iloc[y - 1, z]
        #         nt_prev_loc = format(f"{y - 1}, {z}")
        #         # nt_prev = table.iloc[y, z - 1]
        #         # nt_prev_loc = format(f"{y}, {z - 1}")


        # step = 0
        # for x in range(n):
        #     for y in range(x, -1, -1):
        #         step += 1
        #         #table.iloc[x - 1, y] = str(step) + ": " + str(x - 1) + ', ' + str(y)
        #         table.iloc[x, y] = str(step)
        #         #print(f"x,y: {x},{y}")
        #
        #         print(table)

    def test_cyk_parse5(self):

        cyk = Cyk()

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]
        start_symbol = next(iter(rules))[0]

        pcfg = cyk.tree.convert_to_pcfg(rules)
        cyk.rules = rules
        cyk.pcfg = pcfg
        pcfg_pretty = cyk.tree.pretty_pcgf(pcfg)
        #actual = format(pcfg)
        print(pcfg_pretty)

        s = "the teacher gave the lecture"
        #s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        rhs_left = ''
        rhs_right = ''

        for y in range(n):
            for x in range(y, -1, -1):
                # RHS - Right
                rhs_right = [key[0] for key, value in pcfg.items() if words[y] in key[1]][0]
                table.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and table.iloc[x-1, y] == '':
                        lhs_word = lhs[0]
                        table.iloc[x-1, y] = lhs[0]

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x  - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if table.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = table.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and table.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            table.iloc[x - x_offset, y] = lhs[0]

                            #print(table)

                rhs_left = rhs_right

                #print(table)

        print(table)

        #expect = 'S'
        expect = start_symbol
        actual = table.iloc[0, n - 1]
        eq_(actual, expect)

    def test_cyk_parse6(self):

        cyk = Cyk()

        rules = [
            ('S', ['NP', 'VP']),
            ('NP', ['DT', 'NN']),
            ('VP', ['VB', 'NP']),
            ('DT', ['the']),
            ('NN', ['teacher']),
            ('NN', ['lecture']),
            ('VB', ['gave']),
        ]
        start_symbol = next(iter(rules))[0]

        pcfg = cyk.tree.convert_to_pcfg(rules)
        cyk.rules = rules
        cyk.pcfg = pcfg
        pcfg_pretty = cyk.tree.pretty_pcgf(pcfg)
        #actual = format(pcfg)
        print(pcfg_pretty)

        s = "the teacher gave the lecture"
        #s = "the the teacher gave the lecture"
        #s = "teacher the gave the lecture"

        words = s.split(' ')
        n = len(words)

        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        rhs_left = ''
        rhs_right = ''

        for y in range(n):
            for x in range(y, -1, -1):
                # RHS - Right
                rhs_right = [key[0] for key, value in pcfg.items() if words[y] in key[1]][0]
                table.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and table.iloc[x-1, y] == '':
                        lhs_word = lhs[0]
                        table.iloc[x-1, y] = lhs[0]

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x  - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if table.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = table.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and table.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            table.iloc[x - x_offset, y] = lhs[0]

                            #print(table)

                rhs_left = rhs_right

                #print(table)

        print(table)
        #expect = 'S'
        expect_start_symbol = start_symbol
        actual_start_symbol = table.iloc[0, n - 1]
        eq_(actual_start_symbol, expect_start_symbol)

        # Generate Parse Tree
        #parse_tree = table.iloc[0, n - 1] + '\n'

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


        #(S
        parse_tree = f"({table.iloc[0, n-1]}\n"
        #   (NP
        parse_tree += f"\t({table.iloc[0, 1]}\n"
        #       (DT the)
        parse_tree += f"\t\t({table.iloc[0, 0]} {table.columns[0]})\n"
        #       (NN teacher)
        parse_tree += f"\t\t({table.iloc[1, 1]} {table.columns[1]})\n"
        #   )
        parse_tree += f"\t)\n"
        #   (VP
        parse_tree += f"\t({table.iloc[2, n-1]}\n"
        #       (VB gave)
        parse_tree += f"\t\t({table.iloc[2, 2]} {table.columns[2]})\n"
        #       (NP
        parse_tree += f"\t\t({table.iloc[3, n-1]}\n"
        #           (DT the)
        parse_tree += f"\t\t\t({table.iloc[3, 3]} {table.columns[3]})\n"
        #           (NN lecture)
        parse_tree += f"\t\t\t({table.iloc[4, 4]} {table.columns[4]})\n"
        #       )
        parse_tree += f"\t\t)\n"
        #   )
        parse_tree += f"\t)\n"
        #}
        parse_tree += f")"

        #print(parse_tree)

        root = Node(table.iloc[0, n-1])
        root.x = 0
        root.y = n - 1
        parse_tree = cyk.get_parse_tree(table, root)

        s_parse_tree = ''
        s_parse_tree = cyk.print_parse_tree(root, s_parse_tree)

        parse_tree = os.linesep.join([st for st in s_parse_tree.splitlines() if st])

        actual_tree = Tree.from_string(parse_tree)
        actual_parse_tree = actual_tree.pretty()

        print("Actual Parse Tree: ")
        print(actual_parse_tree)

        eq_(actual_parse_tree, expect_parse_tree)