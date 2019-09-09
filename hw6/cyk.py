from tree import Tree
import pandas


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
        self.root = None

    def __init__(self):
        self.tree = Tree
        self.rules = []
        self.pcfg = []

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

    def get_parse_tree(self, table, root):

        if root != None:
            root.left = self.search_left(table, root)
            root.right = self.search_right(table, root)
            self.get_parse_tree(table, root.left)
            self.get_parse_tree(table, root.right)
            #root.terminal = table.columns[root.y] #table.iloc[root.x, root.y]
            #self.get_parse_tree(table, root.right)
            #root.terminal = table.columns[root.y]


        # if root != None:
        #     root.left = self.search_left(table, root)
        #     self.get_parse_tree(table, root.left)
        #     root.terminal = table.columns[root.y] #table.iloc[root.x, root.y]
        #     root.right = self.search_right(table, root)
        #     self.get_parse_tree(table, root.right)
        #     root.terminal = table.columns[root.y]

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
                break

        return node

    def print_parse_tree(self, node):
        if (node != None):
            self.print_parse_tree(node.left)
            print(str(node.term) + ' ')
            self.print_parse_tree(node.right)


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

    def parse02(self, s):

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
