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

    #counts['NP'][('DT','NN')] / sum(counts['NP'].values())
    def test_convert_to_pcfg_inline1_revised(self):
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


        blah = {'TOP': {('NP', 'VP', '.'): 1}, 'NP': {('DT', 'NN'): 1, ('NN', 'PP'): 1, ('DT', 'NN', 'NN'): 1}, 'DT': {('the',): 1}, 'NN': {('teacher',): 1, ('today',): 1, ('lecture',): 1, ('hall',): 1}, 'VP': {('MD', 'VP'): 1, ('VB', 'NP'): 1}, 'MD': {('will',): 1}, 'VB': {('lecture',): 1}, 'PP': {('IN', 'NP'): 1}, 'IN': {('in',): 1}, '.': {('.',): 1}}
        pcfg_expect = {
            'TOP': {
                ('NP', 'VP', '.'): 1
            },
            'NP': {
                ('DT', 'NN'): 0.3333333333333333,
                ('NN', 'PP'): 0.3333333333333333,
                ('DT', 'NN', 'NN'): 0.3333333333333333,
            },
            'DT': {
                ('the'): 1.0
            },
            'NN': {
                ('teacher'): 0.25,
                ('today'): 0.25,
                ('lecture'): 0.25,
                ('hall'): 0.25,
            },
            'VP': {
                ('MD', 'VP'): 0.5,
                ('VB', 'NP'): 0.5,
            },
            'MD': {
                ('will'): 1
            },
            'VB': {
                ('lecture'): 1
            },
            'PP': {
                ('IN', 'NP'): 1
            },
            'IN': {
                ('in'): 1
            },
            '.': {
                ('.'): 1
            }
        }
        #expect = format(pcgf_expect)
        expect = "defaultdict(<class 'dict'>, " + format(pcfg_expect) + ")"
        print(expect)

        print('ACTUAL *************************')
        pcfg_actual =  t_before.convert_to_pcfg()
        actual = format(pcfg_actual)
        print(actual)

        eq_(actual, expect)

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

        print('EXPECTED: *************************')
        pcfg_expect = {
            'TOP': {
                'rhs': {
                    ('NP', 'VP', '.')
                },
                'probability': 1
            },
            'NP': {
                'rhs': {
                    ('DT', 'NN'),
                    ('NN', 'PP'),
                    ('DT', 'NN', 'NN')
                },
                'probability': 0.3333333333333333
            },
            'DT': {
                'rhs': {
                    ('the',)
                },
                'probability': 1.0
            },
            'NN': {
                'rhs': {
                    ('teacher',),
                    ('today',),
                    ('lecture',),
                    ('hall',)
                },
                'probability': 0.25
            },
            'VP': {
                'rhs': {
                    ('MD', 'VP'),
                    ('VB', 'NP')
                },
                'probability': 0.5
            },
            'MD': {
                'rhs': {
                    ('will',)
                },
                'probability': 1
            },
            'VB': {
                'rhs': {
                    ('lecture',)
                },
                'probability': 1
            },
            'PP': {
                'rhs': {
                    ('IN', 'NP')
                },
                'probability': 1
            },
            'IN': {
                'rhs': {
                    ('in',)
                },
                'probability': 1
            },
            '.': {
                'rhs': {
                    ('.',)
                },
                'probability': 1
            }
        }
        #expect = format(pcgf_expect)
        expect = "defaultdict(<class 'dict'>, " + format(pcfg_expect) + ")"
        print(expect)

        print('ACTUAL *************************')
        pcfg_actual =  t_before.convert_to_pcfg()
        actual = format(pcfg_actual)
        print(actual)

        eq_(actual, expect)

    def test_pretty_pcfg_inline1(self):
        pcfg = {
            'TOP': {
                'rhs': {
                    ('NP', 'VP', '.')
                },
                'probability': 1
            },
            'NP': {
                'rhs': {
                    ('DT', 'NN'),
                    ('NN', 'PP'),
                    ('DT', 'NN', 'NN')
                },
                'probability': 0.3333333333333333
            },
            'DT': {
                'rhs': {
                    ('the',)
                },
                'probability': 1.0
            },
            'NN': {
                'rhs': {
                    ('teacher',),
                    ('today',),
                    ('lecture',),
                    ('hall',)
                },
                'probability': 0.25
            },
            'VP': {
                'rhs': {
                    ('MD', 'VP'),
                    ('VB', 'NP')
                },
                'probability': 0.5
            },
            'MD': {
                'rhs': {
                    ('will',)
                },
                'probability': 1
            },
            'VB': {
                'rhs': {
                    ('lecture',)
                },
                'probability': 1
            },
            'PP': {
                'rhs': {
                    ('IN', 'NP')
                },
                'probability': 1
            },
            'IN': {
                'rhs': {
                    ('in',)
                },
                'probability': 1
            },
            '.': {
                'rhs': {
                    ('.',)
                },
                'probability': 1
            }
        }

        for nonterminal, productions in pcfg.items():
            probability = productions['probability']
            list_rhs = productions['rhs']
            for rhs in list_rhs:
                print('{: <20} -> {} {}'.format(nonterminal, ' '.join(rhs), probability))

            # for label, rhs in productions.items():
            #     for terms in rhs:
            #         print('{: <20} -> {} {}'.format(nonterminal, ' '.join(terms)), str('FUCK YOU'))
            #         #print('{: <20} -> {} {}'.format(nonterminal), str(probability))

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

    def test_convert_to_pcfg_JMpg5(self):
        s = inspect.cleandoc("""
            (TOP
                (S 
                    (VP
                        (VB book)
                        (NP
                            (DT	the)
                            (NN
                                (N	dinner)
                                (N	flight)
                            )
                        )
                    )
                
                    (VP
                        (VB book)
                        (NP
                            (DT	the)
                            (NN
                                (N	dinner)
                            )
                        )
                        (NP
                            (NN
                                (N	flight)
                            )
                        )			
                    )
                )
            )""")

        t_before = Tree.from_string(s)

        print('BEFORE: *************************')
        before = t_before.pretty()
        print(before)

        print('EXPECTED: *************************')
        pcfg_expect = {
            'TOP': {
                'rhs': {
                    ('S'), 1
                },

            },
            'S': {
                'rhs': {
                    ('VP')
                },
                'probability': 1
            },
            'VP': {
                'rhs': {
                    ('V'),
                },

            },
            'DT': {
                'rhs': {
                    ('the',)
                },
                'probability': 1.0
            },
            'NN': {
                'rhs': {
                    ('teacher',),
                    ('today',),
                    ('lecture',),
                    ('hall',)
                },
                'probability': 0.25
            },
            'VP': {
                'rhs': {
                    ('MD', 'VP'),
                    ('VB', 'NP')
                },
                'probability': 0.5
            },
            'MD': {
                'rhs': {
                    ('will',)
                },
                'probability': 1
            },
            'VB': {
                'rhs': {
                    ('lecture',)
                },
                'probability': 1
            },
            'PP': {
                'rhs': {
                    ('IN', 'NP')
                },
                'probability': 1
            },
            'IN': {
                'rhs': {
                    ('in',)
                },
                'probability': 1
            },
            '.': {
                'rhs': {
                    ('.',)
                },
                'probability': 1
            }
        }
        #expect = format(pcgf_expect)
        expect = "defaultdict(<class 'dict'>, " + format(pcfg_expect) + ")"
        print(expect)

        print('ACTUAL *************************')
        pcfg_actual =  t_before.convert_to_pcfg()
        actual = format(pcfg_actual)
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
        pcfg = Tree.convert_to_pcfg(t_before)
        actual = Tree.pretty_pcgf(pcfg)
        print(actual)

        eq_(actual, expect)


    ### Convert to PCFG - Regression Tests ######################################################

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