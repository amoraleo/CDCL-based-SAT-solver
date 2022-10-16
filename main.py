import dimacs_parser
import cnf_realisation
import cdcl

l, v_n, l_n = dimacs_parser.parse()
c = cnf_realisation.Cnf(l, v_n, l_n)
var_values_list = cdcl.VarValuesList(v_n)
graph = cdcl.Graph()
print(c)
#print(c.get_var_num())
#print(c.get_literal_num())
if cdcl.cdcl(c, var_values_list, graph):
    print("SAT")
    print([int(value) for value in var_values_list.var_values_list])
else:
    print("UNSAT")