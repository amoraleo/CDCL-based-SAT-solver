class Clause:
    def __init__(self, list):
        self.literal_set = set(list)

class Cnf:
    def __init__(self, list, var_num, clause_num):
        self.var_num = var_num
        self.clause_num = clause_num
        self.clause_list = []
        for i in range(len(list)):
            self.clause_list.append(Clause(list[i]))

    def add_clause(self, list):
        self.clause_list.append(Clause(list))

    def __str__(self):
        result = ""
        for clause in self.clause_list:
            result += "("
            l = []
            for literal in clause.literal_set:
                s = ""
                if literal < 0:
                    s += "-"
                s += "x" + str(abs(literal))
                l.append(s)
            result += " + ".join(l)
            result += ")"
        return result