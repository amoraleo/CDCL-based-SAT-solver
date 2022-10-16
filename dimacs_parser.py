def parse(filename):
    clause_list = []
    with open(filename, "r") as file:
        for index, line in enumerate(file):
            if index == 1:
                l = line.split()
                var_num, clause_num = int(l[2]), int(l[3])
            if index > 1:
                clause_list.append([int(num.strip()) for num in line.split()[:-1]])

    return clause_list, var_num, clause_num
