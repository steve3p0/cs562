#!/usr/bin/env python -O
# tree.py: n-ary branching tree, reading trees from text, and transforms
# Kyle Gorman <gormanky@ohsu.edu>

from re import escape, finditer
from collections import namedtuple

# left and delimiters on trees
LDEL = '('
RDEL = ')'
LDELE = escape(LDEL)
RDELE = escape(RDEL)
DELIMITERS = r'({})|({})'.format(LDELE, RDELE)

# labels are a sequence of non-whitespace, non-delimiter characters used
# both for terminals and non-terminals
LABEL = r'[^\s{}{}]+'.format(LDELE, RDELE)

# a "token" consists of:
# * a left delimiter
# * possibly some whitespace (though not usually)
# * one of:
#   - a label for a head (possibly null)
#   - a right delimiter
#   - a label for a terminal
TOKEN = r'({0})\s*({2})?|({1})|({2})'.format(LDELE, RDELE, LABEL)

# characters for naming heads introduced by tree transformation; should
# not overlap LDEL or RDEL if you are writing to text files
CU_JOIN_CHAR = '+'
MARKOVIZE_CHAR = '|'
CNF_JOIN_CHAR = '&'
CNF_LEFT_DELIMITER = '<'
CNF_RIGHT_DELIMITER = '>'


class Tree(object):
    """
    A n-ary branching tree with string(-like) objects as labels both on
    terminals and non-terminals. 

    For the purpose of variable names, X' is the "mother" of X, and X the 
    "daughter" of X', iff X' immediately dominates X. Furthermore, X and
    Y are "sisters" if they are immediately dominated by the same mother.

    We assume throughout that terminals are only daughters (i.e., have no
    sisters).
    """

    def __init__(self, label, daughters=None):
        self.label = label
        self.daughters = daughters if daughters else []

    ###################################################
    # construct trees from string and file objects

    @classmethod
    def from_string(cls, string):
        r"""
        Read a single Treebank-style tree from a string. Example:

        >>> s = '(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        >>> Tree.from_string(s)
        (ADVP
            (ADV widely)
            (CONJ and)
            (ADV friendly)
        )

        It doesn't break just because there are weird newlines, either:

        >>> str(Tree.from_string(s)) == \
        ... str(Tree.from_string(s.replace(' ', '\n')))
        True

        A few types of errors are known:

        >>> Tree.from_string(s[:-1])
        Traceback (most recent call last):
        ...
        ValueError: End-of-string, need /\)/
        >>> Tree.from_string(s[1:])
        Traceback (most recent call last):
        ...
        ValueError: Need /\(/
        >>> s_without_head = s[6:-1]
        >>> Tree.from_string(s_without_head)
        Traceback (most recent call last):
        ...
        ValueError: String contains 3 trees
        """
        # initialize stack to "empty"
        stack = [(None, [])]
        for m in finditer(TOKEN, string):
            token = m.group()
            if m.group(1):  # left delimiter
                stack.append((m.group(2), []))
            elif m.group(3):  # right delimiter
                # if stack is "empty", there is nothing in need of closure
                if len(stack) == 1:
                    raise ValueError('Need /{}/'.format(LDELE))
                (mother, children) = stack.pop()
                stack[-1][1].append(cls(mother, children))
            elif m.group(4):  # leaf
                stack[-1][1].append(m.group(4))
            else:
                raise ValueError('Parsing failure: {}'.format(m.groups()))
        # check to make sure the stack is "empty"
        if len(stack) > 1:
            raise ValueError('End-of-string, need /{}/'.format(RDELE))
        elif len(stack[0][1]) == 0:
            raise ValueError('End-of-string, need /{}/'.format(LDELE))
        elif len(stack[0][1]) > 1:
            raise ValueError('String contains {} trees'.format(
                len(stack[0][1])))
        return stack[0][1][0]

    @classmethod
    def from_stream(cls, handle):
        r"""
        Given a treebank-style data *.psd file, yield all its Trees, using
        `from_string` above

        Mock up a real file using cStringIO

        >>> from io import StringIO
        >>> s = '(ADVP (ADV widely) (CONJ and) (ADV friendly))'
        >>> source = StringIO(s.replace(' ', '\n\n\n') + s)
        >>> (one, two) = Tree.from_stream(source)
        >>> str(one) == str(two)
        True
        """
        # TODO I am deeply unhappy with this solution. It would be nicer
        # to use the cleverer logic found in Tree.from_string instead.
        stack = 0
        start = 0
        string = handle.read()
        for m in finditer(DELIMITERS, string):
            # left bracket
            if m.group(1):
                stack += 1
            # right bracket
            else:
                stack -= 1
                # if brackets match, parse it
                if stack == 0:
                    end = m.end()
                    yield Tree.from_string(string[start:end])
                    start = end

    ###################################################
    # magic methods for access, etc., all using self.daughters

    def __iter__(self):
        return iter(self.daughters)

    def __getitem__(self, i):
        return self.daughters[i]

    def __setitem__(self, i, value):
        self.daughters[i] = value

    def __len__(self):
        return len(self.daughters)

    def pop(self, i=None):
        return self.daughters.pop() if i is None else self.daughters.pop(i)

    def append(self, other):
        self.daughters.append(other)

    ###################################################
    # static methods for traversal (etc.)

    @staticmethod
    def terminal(obj):
        return not hasattr(obj, 'label')

    @staticmethod
    def unary(obj):
        return len(obj) == 1

    ###################################################
    # string representations

    def __repr__(self):
        return self.pretty()

    def pretty(self, indent=0, step=4):
        """
        Serialize tree into human-readable multiline string

        >>> s = '(TOP (S (VP (TO to) (VP (VB play)))))'
        >>> t = Tree.from_string(s)
        >>> t
        (TOP
            (S
                (VP
                    (TO to)
                    (VP
                        (VB play)
                    )
                )
            )
        )
        """
        string = LDEL + self.label
        i = indent + step
        is_tree = None
        for daughter in self:
            is_terminal = Tree.terminal(daughter)
            if is_terminal:
                string += ' ' + daughter
            else:
                # recursively print with increased indent
                string += '\n' + (' ' * i) + daughter.pretty(i)
        # add a newline and spaces after last non-terminal at this depth
        if not is_terminal:
            string += '\n' + (' ' * indent)
        string += RDEL
        return string

    ###################################################
    # tree transform instance methods

    def collapse_unary(self, join_char=CU_JOIN_CHAR):
        """
        Return a copy of the tree in which unary productions (i.e.,
        productions with one daughter) have been removed. 

        There are two classes of unary production that we do *not* want to collapse:
        
        * In Penn Treebank style, the root is often a unary production,
          but it is not collapsed. This allows for a special root label
          (e.g., "TOP") to be used to indicate successful parsing.
        * In Penn Treebank style, each POS tag node is an only child 
          produced by a "syntactic" mother. We do not want to collapse these nodes either, 
          since we want to be able to use them as inputs for chart parsing.

        A mother is therefore collapsible into its daughter if it is not 
        the root note, the daughter is an "only child", and the daughter
        is neither terminal nor "pre-terminal" (the mother of a terminal).

        Algorithmically, this is as follows:
        
        * For each head immediately below the root:
            - If head is terminal, continue
            - Recursively apply the function
            - If head is non-unary, continue
            - If head's only daughter is terminal, continue
            - If head's only granddaughter is unary and terminal, continue
            - Merge the only daughter's label and promote its daughters

        Some examples follow.

        Simple merge, with root and POS "distractors":

        to play
        >>> #s = '(TOP (S+VP (TO to) (VP (VB play))))'
        >>> s = '(TOP (S (VP (TO to) (VP (VB play)))))'
        >>> t = Tree.from_string(s)
        >>> t.collapse_unary()
        (TOP
            (S+VP
                (TO to)
                (VP
                    (VB play)
                )
            )
        )

        """

        print(self.label)

        #print(self.unary(self))
        #print(self.unary(self.daughters))
        #is_unary = self.unary(self)
        #print(is_unary)
        for daughter in self:
            is_unary = self.unary(daughter)
            if Tree.terminal(daughter):
                print("terminal: "  + daughter)
            elif daughter.label == 'POS':
                print('POS: Piece of of SHIT')
                daughter.collapse_unary()
            else:
                # Node is neither terminal nor POS
                # Now check if it is preterminal
                preterminal = False
                #for grandaughter in daughter.daughters:
                for grandaughter in daughter:
                    if Tree.terminal(grandaughter):
                        preterminal = True
                        break
                if preterminal:
                    print("pre-terminal: " + daughter.label)
                    daughter.collapse_unary()
                elif Tree.unary(daughter) == True:
                    print("UNARY collapse: " + daughter.label)
                    daughter.collapse_unary()
                else:
                    print("FUCKING ELSE: " + daughter.label)
                    #print(self.unary(self))
                    #print(self.unary(self.daughters))
                    daughter.collapse_unary()





if __name__ == '__main__':
    import doctest
    doctest.testmod()
