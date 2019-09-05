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

    def parse(self, s):

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

                # for j in range(i):
                #
                #     nt_prev = table.iloc[i - j, i - j]
                #     rhs = [nt_prev, nt[0]]
                #     rhs = [nt_prev, nt[0]]
                #     rhs = tuple([nt_prev, nt[0]])
                #
                #     key1 = [key[1] for key, value in self.pcfg.items()]
                #     lhs = [key[0] for key, value in self.pcfg.items() if rhs == key[1]]
                #
                #     if len(lhs) > 0:
                #         table.iloc[j - 1, j] = lhs[0]


        print(table)

        print("Hello!")

            #nonterminal = [key[0] for key, value in self.pcfg.items() if words[i] in key[1]]
            #lookup = {('the',): 1.0}
            #list(self.pcfg.values()).index({('the',): 1.0})
            #print(nonterminal)
            #nonterminal = self.pcfg[words[i]]
            #print(list(mydict.keys())[list(mydict.values()).index(16)])  #
            #print(table.loc[i, "Name"], table.loc[i, "Age"])
            #table.iloc[i,]

        #raise NotImplementedError

        #
        # for j in range(n):

        # let the input be a string I consisting of n characters: a1 ... an.
        # let the grammar contain r nonterminal symbols R1 ... Rr, with start symbol R1.
        # let P[n,n,r] be an array of real numbers. Initialize all elements of P to zero.
        # let back[n,n,r] be an array of backpointing triples.
        # for each s = 1 to n
        #   for each unit production Rv →as
        #     set P[1,s,v] = Pr(Rv →as)
        # for each l = 2 to n -- Length of span
        #   for each s = 1 to n-l+1 -- Start of span
        #     for each p = 1 to l-1 -- Partition of span
        #       for each production Ra → Rb Rc
        #         prob_splitting = Pr(Ra →Rb Rc) * P[p,s,b] * P[l-p,s+p,c]
        #         if P[p,s,b] > 0 and P[l-p,s+p,c] > 0 and P[l,s,a] <  prob_splitting then
        #           set P[l,s,a] = prob_splitting
        #           set back[l,s,a] = <p,b,c>





