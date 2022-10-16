class Clause:
    def __init__(self, list):
        self.literal_set = set(list)

    def get_literal_set(self):
        return self.literal_set

class Cnf:
    def __init__(self, list, var_num, literal_num):
        self.var_num = var_num
        self.literal_num = literal_num
        self.clause_list = []
        for i in range(len(list)):
            self.clause_list.append(Clause(list[i]))
    
    def get_var_num(self):
        return self.var_num

    def get_literal_num(self):
        return self.literal_num

    def __str__(self):
        result = ""
        for clause in self.clause_list:
            result += "("
            l = []
            for literal in clause.get_literal_set():
                s = ""
                if literal < 0:
                    s += "-"
                s += "x" + str(abs(literal))
                l.append(s)
            result += " + ".join(l)
            result += ")"
        return result