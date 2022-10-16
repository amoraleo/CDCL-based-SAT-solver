def parse():
    s = input()
    s = input()
    l = s.split()
    var_num, literal_num = int(l[2]), int(l[3])
    cnf_list = []
    
    try:
        while True:
            s = input()
            cnf_list.append([int(num) for num in s.split()[:-1]])
    except EOFError:
        pass

    return cnf_list, var_num, literal_num
