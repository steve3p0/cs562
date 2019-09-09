from tree import Tree
import pandas
import os

class Node:
    def __init__(self, val):
        self.nonterminal = val
        self.terminal = ''
        self.x = None
        self.y = None

        self.left = None
        self.right = None

class Cyk(object):

    def __init__(self):
        self.rules = []
        self.table = None
        self.root = None
        self.tree = Tree
        self.pcfg = []
        self.valid = False
        self.parse_tree = ''

    def load_rules(self, filename):
        f = open(filename, "r", encoding="utf-8")
        trees = Tree.from_stream(f)
        f.close

        rules = []

        for t in trees:
            # Get a copy of the tree before unary collapse
            t_before = Tree.pretty(t)

            # Get actual tree after collapse from tree.py
            t_col = Tree.collapse_unary(t)
            t_cnf = Tree.chomsky_normal_form(t_col)
            rules += Tree.productions(t_cnf)

        return rules

    def parse(self, s):

        start_symbol = next(iter(self.rules))[0]
        words = s.split(' ')
        n = len(words)
        self.table = pandas.DataFrame(index=range(n), columns=words)
        self.table.fillna('', inplace=True)

        self.pcfg = Tree.convert_to_pcfg(self.rules)
        self.root = Node(self.table.iloc[0, n-1])
        self.root.x = 0
        self.root.y = n - 1

        rhs_left = ''
        rhs_right = ''

        for y in range(n):
            for x in range(y, -1, -1):
                # RHS - Right
                rhs_right = [key[0] for key, value in self.pcfg.items() if words[y] in key[1]][0]
                self.table.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and self.table.iloc[x - 1, y] == '':
                        lhs_word = lhs[0]
                        self.table.iloc[x - 1, y] = lhs[0]

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if self.table.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = self.table.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and self.table.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            self.table.iloc[x - x_offset, y] = lhs[0]

                            # print(table)

                rhs_left = rhs_right

        # Validate Sentence
        top_lhs = self.table.iloc[0, n - 1]

        if top_lhs == start_symbol:
            self.valid = True

            root = Node(self.table.iloc[0, n - 1])
            root.x = 0
            root.y = n - 1
            parse_tree = self.get_parse_tree(self.table, root)

            self.parse_tree = self.print_parse_tree(root)
            self.parse_tree = os.linesep.join([st for st in self.parse_tree.splitlines() if st])

            actual_tree = Tree.from_string(self.parse_tree)
            self.parse_tree = actual_tree.pretty()

            return True
        else:
            return False

    def get_parse_tree(self, table, root):

        if root != None:
            root.left = self.search_left(table, root)
            root.right = self.search_right(table, root)
            self.get_parse_tree(table, root.left)
            self.get_parse_tree(table, root.right)

        return root

    def search_left(self, table, n):

        node = None

        for i in range(n.y - 1, -1, -1):
            if table.iloc[n.x, i] == '':
                next
            else:
                node = Node(table.iloc[n.x, i])
                node.x = n.x
                node.y = i
                if i == n.x:
                    node.terminal = table.columns[i]
                break

        return node

    def search_right(self, table, n):

        node = None

        for i in range(n.x + 1, n.y + 1):
            if table.iloc[i, n.y] == '':
                next
            else:
                node = Node(table.iloc[i, n.y])
                node.x = i
                node.y = n.y
                if i == n.y:
                    node.terminal = table.columns[i]
                break

        return node

    def print_parse_tree(self, node):

        s = ''
        if (node != None):

            nonterminal = node.nonterminal
            if node.terminal != '':
                terminal = node.terminal

                s = f"({nonterminal} {terminal})"
            else:
                left = self.print_parse_tree(node.left)
                right = self.print_parse_tree(node.right)

                s = f"({nonterminal} {left} {right})"

            #print(s)

        return s

    def parse1(self, s):

        start_symbol = next(iter(self.rules))[0]
        words = s.split(' ')
        n = len(words)
        self.table = pandas.DataFrame(index=range(n), columns=words)
        self.table.fillna('', inplace=True)

        self.pcfg = Tree.convert_to_pcfg(self.rules)
        self.root = Node(self.table.iloc[0, n-1])
        self.root.x = 0
        self.root.y = n - 1

        rhs_left = ''
        rhs_right = ''

        for y in range(n):
            for x in range(y, -1, -1):
                # RHS - Right
                rhs_right = [key[0] for key, value in self.pcfg.items() if words[y] in key[1]][0]
                self.table.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and self.table.iloc[x - 1, y] == '':
                        lhs_word = lhs[0]
                        self.table.iloc[x - 1, y] = lhs[0]

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if self.table.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = self.table.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and self.table.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            self.table.iloc[x - x_offset, y] = lhs[0]

                            # print(table)

                rhs_left = rhs_right

        # Validate Sentence
        top_lhs = self.table.iloc[0, n - 1]

        if top_lhs == start_symbol:
            self.valid = True

            root = Node(self.table.iloc[0, n - 1])
            root.x = 0
            root.y = n - 1
            parse_tree = self.get_parse_tree(self.table, root)

            self.parse_tree = self.print_parse_tree(root)
            self.parse_tree = os.linesep.join([st for st in self.parse_tree.splitlines() if st])

            actual_tree = Tree.from_string(self.parse_tree)
            self.parse_tree = actual_tree.pretty()

            return True
        else:
            return False