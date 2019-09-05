from tree import Tree
import pandas

class Cyk(object):

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

    def parse0(self, s):

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

    def parse(self, s):

        words = s.split(' ')
        n = len(words)
        table = pandas.DataFrame(index = range(n), columns = words)
        table.fillna('', inplace=True)

        print(table)

        term1 = ''
        term2 = ''

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

            # J IS ROW
            for j in range(i, 0, -1):
                # K IS COLUMN
                for k in range(i, 0, -1):
                    if table.iloc[j-1, k] == '':
                        # LOOKING TO PUT LHS
                        table.iloc[j-1, k] = str(j-1) + ', ' + str(k)

                        # RHS: TERM 1
                        nt_prev = table.iloc[j, j]
                        term1 = nt_prev
                        term2 = nt[0]

                        # RHS: TERM 1 + TERM 2
                        #rhs = tuple([nt_prev, nt[0]])
                        rhs = tuple([term1, term2])

                        # LHS: lookup using rhs
                        lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]
                        if len(lhs) > 0:
                            table.iloc[j, k] = lhs[0]
                            nt = lhs


                    print("######################################")
                    print(f"term 1: {term1}")
                    print(f"term 2: {term2}")
                    print(f"rhs: {rhs}")
                    print(f"i: {i}")
                    print(f"j: {j}")
                    print(f"k: {k}")
                    print(table)

        print(table)

        print("Hello!")
