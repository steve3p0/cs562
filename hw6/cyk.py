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

    def __init__(self, rules):
        self.tree = Tree
        self.rules = rules
        self.pcfg = self.tree.convert_to_pcfg(rules)

        self.table_rules = None
        self.table_probs = None
        self.root = None
        self.parse_tree = ''
        self.valid = False

    @staticmethod
    def load_rules_ap(filename):
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

    @staticmethod
    def load_rules_pa(filename):
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
            t_prd = Tree.productions(t_cnf)
            t_pcfg = Tree.convert_to_pcfg(t_prd)

            rules += t_pcfg

        return rules

    @staticmethod
    def load_rules_ap(filename):
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
        self.table_rules = pandas.DataFrame(index=range(n), columns=words)
        self.table_rules.fillna('', inplace=True)

        #self.pcfg = Tree.convert_to_pcfg(self.rules)
        self.root = Node(self.table_rules.iloc[0, n - 1])
        self.root.x = 0
        self.root.y = n - 1

        rhs_left = ''
        rhs_right = ''

        for y in range(n):
            for x in range(y, -1, -1):

                # RHS - Right
                rhs_right = [key[0] for key, value in self.pcfg.items() if words[y] in key[1]][0]
                self.table_rules.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and self.table_rules.iloc[x - 1, y] == '':
                        lhs_word = lhs[0]
                        self.table_rules.iloc[x - 1, y] = lhs[0]

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if self.table_rules.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = self.table_rules.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and self.table_rules.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            self.table_rules.iloc[x - x_offset, y] = lhs[0]

                            print(self.table_rules)

                rhs_left = rhs_right

        # Validate Sentence
        top_lhs = self.table_rules.iloc[0, n - 1]

        if top_lhs == start_symbol:
            self.valid = True

            root = Node(self.table_rules.iloc[0, n - 1])
            root.x = 0
            root.y = n - 1
            parse_tree = self.get_parse_tree(self.table_rules, root)

            self.parse_tree = self.print_parse_tree(root)
            self.parse_tree = os.linesep.join([st for st in self.parse_tree.splitlines() if st])

            actual_tree = Tree.from_string(self.parse_tree)
            self.parse_tree = actual_tree.pretty()

            return True
        else:
            return False

    def parse_pcfg(self, s):

        start_symbol = next(iter(self.rules))[0]
        words = s.split(' ')
        n = len(words)

        table_rules = pandas.DataFrame(index=range(n), columns=words)
        table_rules.fillna('', inplace=True)

        # temp probs
        table_probs_tmp = pandas.DataFrame(index=range(n), columns=words)
        table_probs_tmp.fillna(0.0, inplace=True)

        # final probs
        table_probs = pandas.DataFrame(index=range(n), columns=words)
        table_probs.fillna(0.0, inplace=True)

        #self.pcfg = Tree.convert_to_pcfg(self.rules)
        self.root = Node(table_rules.iloc[0, n-1])
        self.root.x = 0
        self.root.y = n - 1

        #lhs
        #lhs_word
        #rhs
        rhs_left_trm = ''
        rhs_right_trm = ''

        rule_prb = 0.0
        lhs_prb = 0.0
        rhs_left_prb = 0.0
        rhs_right_prb = 0.0

        for y in range(n):
            for x in range(y, -1, -1):

                # RHS - Right: Map right node of RHS of Rule to CYK Table
                rhs_right_trm = [key[0] for key, value in self.pcfg.items() if words[y] in key[1]][0]
                rhs_right_prb = [value for key, value in self.pcfg.items() if words[y] in key[1]][0]
                # TABLE - RHS RIGHT
                table_rules.iloc[y, y] = rhs_right_trm
                table_probs.iloc[y, y] = rhs_right_prb

                # FIND LHS
                if x > 0:
                    # FIND LHS: Given RHS-LEFT and RHS-RIGHT...
                    rhs = tuple([rhs_left_trm, rhs_right_trm])
                    lhs = [[key[0], value] for key, value in self.pcfg.items() if rhs == key[1]]

                    #if len(lhs) > 0 and table_rules.iloc[x - 1, y] == '':
                    for lhs_term, v in lhs:

                        #for key, value
                        lhs_prb = self.pcfg[lhs_term, rhs]
                        rule_prb = rhs_left_prb * rhs_right_prb * lhs_prb

                        # lHS: Map LHS of Rule to CYK Table
                        # TABLE - LHS
                        table_rules.iloc[x - 1, y] = lhs_term
                        table_probs.iloc[x - 1, y] = rule_prb

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right_trm = lhs_term
                                    rhs_right_prb = rule_prb

                                    # RHS - LEFT
                                    if table_rules.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left_trm = table_rules.iloc[x - x_offset, y - y_offset]
                                        rhs_left_prb = table_probs.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left_trm, rhs_right_trm])
                                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and table_rules.iloc[x - x_offset, y] == '':
                                            lhs_term = lhs[0]
                                            lhs_prb = self.pcfg[lhs_term, rhs]
                                            rule_prb = rhs_left_prb * rhs_right_prb * lhs_prb

                                            if rule_prb > table_probs.iloc[x - x_offset, y]:

                                                table_rules.iloc[x - x_offset, y] = lhs_term
                                                table_probs.iloc[x - x_offset, y] = rule_prb


                            print(table_rules)
                            print(table_probs)

                rhs_left_trm = rhs_right_trm
                rhs_left_prb = rhs_right_prb

        self.table_rules = table_rules
        self.table_probs = table_probs

        # Validate Sentence
        top_lhs = self.table_rules.iloc[0, n - 1]

        if top_lhs == start_symbol:
            self.valid = True

            root = Node(self.table_rules.iloc[0, n - 1])
            root.x = 0
            root.y = n - 1
            parse_tree = self.get_parse_tree(self.table_rules, root)

            self.parse_tree = self.print_parse_tree(root)
            self.parse_tree = os.linesep.join([st for st in self.parse_tree.splitlines() if st])

            actual_tree = Tree.from_string(self.parse_tree)
            self.parse_tree = actual_tree.pretty()

            return True
        else:
            return False

    def parse_pcfg1(self, s):

        start_symbol = next(iter(self.rules))[0]
        words = s.split(' ')
        n = len(words)

        table_rules = pandas.DataFrame(index=range(n), columns=words)
        table_rules.fillna('', inplace=True)
        table_probs = pandas.DataFrame(index=range(n), columns=words)
        table_probs.fillna(0.0, inplace=True)

        #self.pcfg = Tree.convert_to_pcfg(self.rules)
        self.root = Node(table_rules.iloc[0, n-1])
        self.root.x = 0
        self.root.y = n - 1

        #lhs
        #lhs_word
        #rhs
        rhs_left_trm = ''
        rhs_right_trm = ''

        rule_prb = 0.0
        lhs_prb = 0.0
        rhs_left_prb = 0.0
        rhs_right_prb = 0.0

        for y in range(n):
            for x in range(y, -1, -1):

                # RHS - Right: Map right node of RHS of Rule to CYK Table
                rhs_right_trm = [key[0] for key, value in self.pcfg.items() if words[y] in key[1]][0]
                rhs_right_prb = [value for key, value in self.pcfg.items() if words[y] in key[1]][0]
                # TABLE - RHS RIGHT
                table_rules.iloc[y, y] = rhs_right_trm
                table_probs.iloc[y, y] = rhs_right_prb

                # FIND LHS
                if x > 0:
                    # FIND LHS: Given RHS-LEFT and RHS-RIGHT...
                    rhs = tuple([rhs_left_trm, rhs_right_trm])
                    lhs = [[key[0], value] for key, value in self.pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and table_rules.iloc[x - 1, y] == '':

                        #for key, value
                        lhs_prb = self.pcfg[lhs[0], rhs]
                        rule_prb = rhs_left_prb * rhs_right_prb * lhs_prb

                        # lHS: Map LHS of Rule to CYK Table
                        lhs_word = lhs[0]
                        # TABLE - LHS
                        table_rules.iloc[x - 1, y] = lhs[0]
                        table_probs.iloc[x - 1, y] = rule_prb

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right_trm = lhs_word
                                    rhs_right_prb = rule_prb

                                    # RHS - LEFT
                                    if table_rules.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left_trm = table_rules.iloc[x - x_offset, y - y_offset]
                                        rhs_left_prb = table_probs.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left_trm, rhs_right_trm])
                                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and table_rules.iloc[x - x_offset, y] == '':
                                            lhs_prb = self.pcfg[lhs[0], rhs]
                                            rule_prb = rhs_left_prb * rhs_right_prb * lhs_prb

                                            lhs_word = lhs[0]
                                            table_rules.iloc[x - x_offset, y] = lhs[0]
                                            table_probs.iloc[x - x_offset, y] = rule_prb

                            print(table_rules)
                            print(table_probs)

                rhs_left_trm = rhs_right_trm
                rhs_left_prb = rhs_right_prb

        self.table_rules = table_rules
        self.table_probs = table_probs

        # Validate Sentence
        top_lhs = self.table_rules.iloc[0, n - 1]

        if top_lhs == start_symbol:
            self.valid = True

            root = Node(self.table_rules.iloc[0, n - 1])
            root.x = 0
            root.y = n - 1
            parse_tree = self.get_parse_tree(self.table_rules, root)

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
        self.table_rules = pandas.DataFrame(index=range(n), columns=words)
        self.table_rules.fillna('', inplace=True)

        self.pcfg = Tree.convert_to_pcfg(self.rules)
        self.root = Node(self.table_rules.iloc[0, n - 1])
        self.root.x = 0
        self.root.y = n - 1

        rhs_left = ''
        rhs_right = ''

        for y in range(n):
            for x in range(y, -1, -1):
                # RHS - Right
                rhs_right = [key[0] for key, value in self.pcfg.items() if words[y] in key[1]][0]
                self.table_rules.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and self.table_rules.iloc[x - 1, y] == '':
                        lhs_word = lhs[0]
                        self.table_rules.iloc[x - 1, y] = lhs[0]

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if self.table_rules.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = self.table_rules.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and self.table_rules.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            self.table_rules.iloc[x - x_offset, y] = lhs[0]

                            # print(table_rules)

                rhs_left = rhs_right

        # Validate Sentence
        top_lhs = self.table_rules.iloc[0, n - 1]

        if top_lhs == start_symbol:
            self.valid = True

            root = Node(self.table_rules.iloc[0, n - 1])
            root.x = 0
            root.y = n - 1
            parse_tree = self.get_parse_tree(self.table_rules, root)

            self.parse_tree = self.print_parse_tree(root)
            self.parse_tree = os.linesep.join([st for st in self.parse_tree.splitlines() if st])

            actual_tree = Tree.from_string(self.parse_tree)
            self.parse_tree = actual_tree.pretty()

            return True
        else:
            return False

    def parse2(self, s):

        start_symbol = next(iter(self.rules))[0]
        words = s.split(' ')
        n = len(words)
        self.table_rules = pandas.DataFrame(index=range(n), columns=words)
        self.table_rules.fillna('', inplace=True)

        #self.pcfg = Tree.convert_to_pcfg(self.rules)
        self.root = Node(self.table_rules.iloc[0, n - 1])
        self.root.x = 0
        self.root.y = n - 1

        rhs_left = ''
        rhs_right = ''
        done = False

        for y in range(n):

            if done == True:
                break

            for x in range(y, -1, -1):

                if done == True:
                    break

                # RHS - Right
                rhs_right = [key[0] for key, value in self.pcfg.items() if words[y] in key[1]][0]
                self.table_rules.iloc[y, y] = rhs_right

                # LHS
                if x > 0:
                    rhs = tuple([rhs_left, rhs_right])
                    lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                    if len(lhs) > 0 and self.table_rules.iloc[x - 1, y] == '':
                        lhs_word = lhs[0]
                        self.table_rules.iloc[x - 1, y] = lhs[0]

                        if done == True:
                            break

                        for x_offset in range(n):
                            for y_offset in range(n):

                                if x - x_offset > -1:

                                    # RHS - RIGHT
                                    rhs_right = lhs_word

                                    # RHS - LEFT
                                    if self.table_rules.iloc[x - x_offset, y - y_offset] != '':
                                        rhs_left = self.table_rules.iloc[x - x_offset, y - y_offset]

                                    # LHS
                                    if x > -1:
                                        rhs = tuple([rhs_left, rhs_right])
                                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                                        if len(lhs) > 0 and self.table_rules.iloc[x - x_offset, y] == '':
                                            lhs_word = lhs[0]
                                            self.table_rules.iloc[x - x_offset, y] = lhs[0]

                                        if x - x_offset == 0 and y == n -1:
                                            done = True

                            print(self.table_rules)

                rhs_left = rhs_right

        # Validate Sentence
        top_lhs = self.table_rules.iloc[0, n - 1]

        if top_lhs == start_symbol:
            self.valid = True

            root = Node(self.table_rules.iloc[0, n - 1])
            root.x = 0
            root.y = n - 1
            parse_tree = self.get_parse_tree(self.table_rules, root)

            self.parse_tree = self.print_parse_tree(root)
            self.parse_tree = os.linesep.join([st for st in self.parse_tree.splitlines() if st])

            actual_tree = Tree.from_string(self.parse_tree)
            self.parse_tree = actual_tree.pretty()

            return True
        else:
            return False