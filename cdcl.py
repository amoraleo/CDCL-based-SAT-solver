import random


class Node:
    def __init__(self, var_num, value, level):
        self.prev_list = []
        self.next_list = []
        self.var_num = var_num
        self.value = value
        self.level = level

    def add_prev_link(self, node_num):
        self.prev_list.append(node_num)

    def add_next_link(self, node_num):
        self.next_list.append(node_num)

class Graph:
    def __init__(self):
        self.node_list = []

    def add_node(self, node):
        self.node_list.append(node)
        return len(self.node_list) - 1

    def get_node_num(self, var_num):
        for index, node in enumerate(self.node_list):
            if node.var_num == var_num:
                return index

    def __str__(self):
        result = ""
        for node in self.node_list:
            result += "x" + str(node.var_num) + "=" + str(node.value) + ":" + str(node.level) + "\n" + str(node.prev_list) + "\n" + str(node.next_list) + "\n\n"
        return result


class VarValuesList:
    def __init__(self, var_num):
        self.var_values_list = []
        for _ in range(var_num):
            self.var_values_list.append(None)

    def change_var_value(self, var_num, value):
        self.var_values_list[var_num-1] = value

    def are_all_assigned(self):
        return None not in self.var_values_list

    def __str__(self):
        return str(self.var_values_list)


def pick_branching_variable(cnf, var_values_list):
    for index, var_value in enumerate(var_values_list.var_values_list):
        if var_value == None:
            return index + 1, random.randrange(0,2)


def use_sing_disj_rule_and_check_impossible_clause(clause, var_values_list):
    unassigned_cntr = 0
    for literal in clause.literal_set:
        if var_values_list.var_values_list[abs(literal)-1] == None:
            unassigned_cntr += 1
            unassigned_literal = literal
        elif (var_values_list.var_values_list[abs(literal)-1] == True and literal > 0) or (var_values_list.var_values_list[abs(literal)-1] == False and literal < 0):
            return False, None
    if unassigned_cntr == 0:
        return True, None
    if unassigned_cntr == 1:
        #var_values_list.change_var_value(unassigned_var, True)
        return False, unassigned_literal
    return False, None


def unit_propagation_conflict(cnf, var_values_list, last_node_num, graph, level):
    for clause in cnf.clause_list:
        is_impossible, literal = use_sing_disj_rule_and_check_impossible_clause(clause, var_values_list)
        if is_impossible:
            return True
        elif literal != None:
            value = True if literal > 0 else False
            var_values_list.change_var_value(abs(literal), value)
            node_num = graph.add_node(Node(abs(literal), value, level))
            graph.node_list[last_node_num].add_next_link(node_num)
            graph.node_list[node_num].add_prev_link(last_node_num)
            #if unit_propagation_conflict(cnf, var_values_list, node_num, graph, level):
                #return True
            #else:
                #return False
    return False


def conflict_analysis(cnf, var_values_list, level):
    return level

def backtrack(cnf, var_values_list, b):
    pass

def cdcl(cnf, var_values_list, impl_graph):
    level = 0
    while not var_values_list.are_all_assigned():
        print(var_values_list)
        var_num, var_val = pick_branching_variable(cnf, var_values_list)
        level += 1
        var_values_list.change_var_value(var_num, bool(var_val))
        node_num = impl_graph.add_node(Node(var_num, bool(var_val), level))
        if unit_propagation_conflict(cnf, var_values_list, node_num, impl_graph, level):
            b = conflict_analysis(cnf, var_values_list, level)
            if b < 0:
                return False
            else:
                backtrack(cnf, var_values_list, b)
                level = b
    #print(var_values_list)
    #print(impl_graph)
    return True
