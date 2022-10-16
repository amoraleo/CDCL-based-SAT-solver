import dimacs_parser
import cnf_realisation
import cdcl
import sys

if len (sys.argv) < 2:
    print("Wrong input")
    exit(1)

cl_list, vars_num, clauses_num = dimacs_parser.parse(sys.argv[1])
c = cnf_realisation.Cnf(cl_list, vars_num, clauses_num)
vars_values = cdcl.VarValues(vars_num)
impl_graph = cdcl.Graph()

if cdcl.cdcl_based_solver(c, vars_values, impl_graph):
    print("SAT")
    print([int(value) for value in vars_values.list])
else:
    print("UNSAT")