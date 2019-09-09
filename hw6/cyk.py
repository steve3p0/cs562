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

    def print_parse_tree1(self, node):
        if (node != None):
            print(str(node.nonterminal) + ' ')
            if node.terminal != '':
                print(str(node.terminal) + ' ')
            self.print_parse_tree(node.left)
            self.print_parse_tree(node.right)

    def print_parse_tree2(self, node, s):
        if (node != None):

            s += f"({node.nonterminal} "

            if node.terminal != '':
                s += f"{node.terminal}) "

            # print(str(node.nonterminal) + ' ')
            # if node.terminal != '':
            #     print(str(node.terminal) + ' ')
            s += self.print_parse_tree(node.left, s)
            s += self.print_parse_tree(node.right, s)

            s += f")"

            print(s)

        return s

    def parse1(self, s):

        words = s.split(' ')
        n = len(words)
        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        prev_left = ''

        for i in range(n):

            # initialize Uninary terminal cell
            nt = [key[0] for key, value in self.pcfg.items() if words[i] in key[1]]
            table.iloc[i, i] = nt[0]

            # Find rule with previous terminal
            nt_prev = table.iloc[i - 1, i - 1]
            rhs = tuple([ nt_prev, nt[0] ])
            lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

            if len(lhs) > 0:
                table.iloc[i - 1, i] = lhs[0]
                nt = lhs

            # Find rule
            # ј is the diagonal
            for j in range(i, 0, -1):
                for k in range(i, j, -1):
                    if table.iloc[j-1, k] == '':
                        table.iloc[j-1, k] = str(j)
                        nt_prev = table.iloc[j-1, k]
                        rhs = tuple([nt_prev, nt[0]])
                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                        if len(lhs) > 0:
                            table.iloc[j, k] = lhs[0]
                            nt = lhs

                print(table)

        print(table)

    def parse2(self, s):

        words = s.split(' ')
        n = len(words)
        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        prev_left = ''

        for i in range(n):

            # initialize Uninary terminal cell
            nt = [key[0] for key, value in self.pcfg.items() if words[i] in key[1]]
            table.iloc[i, i] = nt[0]

            # Find rule with previous terminal
            nt_prev = table.iloc[i - 1, i - 1]
            rhs = tuple([ nt_prev, nt[0] ])
            lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

            if len(lhs) > 0:
                table.iloc[i - 1, i] = lhs[0]
                nt = lhs

            # Find rule
            for j in range(i, 0, -1):
                x = i
                for k in range(x, 0, -1):
                    if table.iloc[j-1, k] == '':
                        table.iloc[j-1, k] = str(j)
                        nt_prev = table.iloc[j, j]
                        rhs = tuple([nt_prev, nt[0]])
                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

                        if len(lhs) > 0:
                            table.iloc[j, k] = lhs[0]
                            nt = lhs

                print(table)

        print(table)

    @staticmethod
    def strip_formating(s):

        if ':' in s:
            s = s.split(':')[1]

        s = s.strip()

        return s

    def parse3(self, s):

        words = s.split(' ')
        n = len(words)
        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        term1 = ''
        term2 = ''

        step = 0
        for i in range(n):

            step += 1
            # initialize Uninary terminal cell
            nt = [key[0] for key, value in self.pcfg.items() if words[i] in key[1]]
            table.iloc[i, i] = str(step) + ": " + nt[0]

            # Find rule with previous terminal
            nt_prev = self.strip_formating(table.iloc[i - 1, i - 1])
            rhs = tuple([ nt_prev, nt[0] ])
            lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]

            if len(lhs) > 0:
                table.iloc[i - 1, i] = str(step) + ": " + lhs[0]
                nt = lhs

            # Find rule

            # J IS ROW
            for j in range(i, -1, -1):
                # K IS COLUMN
                for k in range(i, -1, -1):
                    if table.iloc[j-1, k] == '':

                        #step += 1

                        # LOOKING TO PUT LHS
                        table.iloc[j-1, k] = str(step) + ": " + str(j-1) + ', ' + str(k)

                        # RHS: TERM 1
                        #nt_prev = table.iloc[j, j]
                        nt_prev = self.strip_formating(table.iloc[j, j])
                        term1 = nt_prev
                        term2 = nt[0]

                        # RHS: TERM 1 + TERM 2
                        #rhs = tuple([nt_prev, nt[0]])
                        rhs = tuple([term1, term2])

                        # LHS: lookup using rhs
                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]
                        if len(lhs) > 0:
                            table.iloc[j, k] = str(step) + ": " + lhs[0]
                            nt = lhs

                        print("######################################")
                        print(f"term 1: {term1}")
                        print(f"term 2: {term2}")
                        print(f"rhs: {rhs}")
                        print(f"i: {i}")
                        print(f"j: {j}")
                        print(f"k: {k}")
                        print(table)




        print()
        print()
        print("#### FINAL TABLE #####################################")
        print(table)

        print("Hello!")
