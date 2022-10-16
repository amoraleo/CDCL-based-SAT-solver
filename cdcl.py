import cnf_realisation

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
        for index, node in enumerate(self.node_list):
            result += "x" + str(node.var_num) + "=" + str(node.value) + ":" + str(node.level) + "(" + str(index) + ")" + "\n" + str(node.prev_list) + "\n" + str(node.next_list) + "\n\n"
        return result


class VarValues:
    def __init__(self, var_num):
        self.list = []
        for _ in range(var_num):
            self.list.append(None)

    def change_var_value(self, var_num, value):
        self.list[var_num-1] = value

    def are_all_assigned(self):
        return None not in self.list

    def __str__(self):
        return str(self.list)
                

def pick_branching_variable(var_values:VarValues):
    for index, var_value in enumerate(var_values.list):
        if var_value == None:
            return index + 1, 1
            

def use_sing_disj_rule_and_check_impossible_clause(clause:cnf_realisation.Clause, var_values:VarValues):
    unassigned_cntr = 0
    for literal in clause.literal_set:
        if var_values.list[abs(literal)-1] == None:
            unassigned_cntr += 1
            unassigned_literal = literal
            gener_literals = [literal for literal in clause.literal_set if literal != unassigned_literal]
        elif (var_values.list[abs(literal)-1] == True and literal > 0) or (var_values.list[abs(literal)-1] == False and literal < 0):
            return False, None, None
    if unassigned_cntr == 0:
        return True, None, None
    if unassigned_cntr == 1:
        return False, unassigned_literal, gener_literals
    return False, None, None


def unit_propagation_conflict(cnf:cnf_realisation.Cnf, var_values:VarValues, graph:Graph, level:int):
    for clause in cnf.clause_list:
        is_impossible, unassigned_literal, gener_literals = use_sing_disj_rule_and_check_impossible_clause(clause, var_values)
        if is_impossible:
            return True
        elif unassigned_literal != None:
            value = True if unassigned_literal > 0 else False
            var_values.change_var_value(abs(unassigned_literal), value)
            node_num = graph.add_node(Node(abs(unassigned_literal), value, level))
            for literal in gener_literals:
                prev_node_num = graph.get_node_num(abs(literal))
                graph.node_list[prev_node_num].add_next_link(node_num)
                graph.node_list[node_num].add_prev_link(prev_node_num)
            return unit_propagation_conflict(cnf, var_values, graph, level)
    return False


def conflict_analysis(cnf:cnf_realisation.Cnf, graph:Graph, level:int):
    if level == 0: return -1
    level_set = set()
    node_set = set()
    for node in graph.node_list[::-1]:
        if node.level == level and node.prev_list != []:
            for index in node.prev_list:
                if graph.node_list[index].level < level or (graph.node_list[index].level == level and graph.node_list[index].prev_list == []):
                    node_set.add(graph.node_list[index])
                    level_set.add(graph.node_list[index].level)
        if node.level == level and node.prev_list == []:
            node_set.add(node)
            level_set.add(node.level)
        if node.level < level:
            break
    literal_list = []
    for node in node_set:
        literal_list.append(-node.var_num if node.value else node.var_num)
    cnf.add_clause(literal_list)
    return min(level_set)

def backtrack(var_values:VarValues, graph:Graph, b:int):
    end = None
    for index in range(len(graph.node_list)):
        if graph.node_list[index].level < b:
            graph.node_list[index].next_list = [var_num for var_num in graph.node_list[index].next_list if graph.node_list[index].level < b]
            graph.node_list[index].prev_list = [var_num for var_num in graph.node_list[index].prev_list if graph.node_list[index].level < b]
        else:
            if end == None:
                end = index
            var_values.list[graph.node_list[index].var_num - 1] = None
    if end == 0:
        graph.node_list = []
    else:
        graph.node_list = graph.node_list[:end]

def cdcl_based_solver(cnf:cnf_realisation.Cnf, var_values:VarValues, impl_graph:Graph):
    level = 0
    was_conflict = False
    if unit_propagation_conflict(cnf, var_values, impl_graph, level):
            return False
    while not var_values.are_all_assigned():
        if was_conflict:
            if unit_propagation_conflict(cnf, var_values, impl_graph, level):
                return False
        var_num, var_val = pick_branching_variable(var_values)
        level += 1
        var_values.change_var_value(var_num, bool(var_val))
        impl_graph.add_node(Node(var_num, bool(var_val), level))
        #print("===============================================")
        #print(cnf)
        #print(var_values_list)
        #print(impl_graph)
        if was_conflict := unit_propagation_conflict(cnf, var_values, impl_graph, level):
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            #print(impl_graph)
            b = conflict_analysis(var_values, impl_graph, level)
            if b < 0:
                return False
            else:
                backtrack(cnf, var_values, impl_graph, b)
                level = b - 1
    return True