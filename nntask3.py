import argparse
import json
import math
import warnings

warnings.filterwarnings("ignore")

def read_graph(inp):
    try:
        input_graph = open(inp, 'r')
        line = input_graph.read()
    except Exception:
        print("Файл не найден")
        exit()
    text = ''
    for i in line.split():
        text += i
    tmp = text[1:-1].split('),(')
    edges = []
    for i in tmp:
        edges.append(list(map(int, i.split(','))))
    maximum = 0
    for i in range(len(edges)):
        maximum = max(maximum, edges[i][0], edges[i][1])
    graph = [[] for _ in range(maximum)]
    count = [0 for _ in range(maximum)]
    x = 0
    for i in edges:
        try:
            graph[i[1] - 1].find(i[0] - 1)
            print("Такое ребро уже существует", "Ошибка в строке", x + 1)
            exit()
        except Exception:
            graph[i[1] - 1].append(i[0] - 1)
        if count[i[1] - 1] == i[2] - 1:
            count[i[1] - 1] += 1
        else:
            print("Нарушен порядок перечисления рёбер", "Ошибка в строке", x + 1)
            exit()
    return graph

def dfs(graph, v, marks):
    marks[v] = 1
    for i in graph[v]:
        if marks[i] == 0:
            marks = dfs(graph, i, marks)
        if marks[i] == 1:
            print("В графе есть циклы")
            exit()
    marks[v] = 2
    return marks

def source_list(v, graph):
    ans = [v]
    for i in range(len(graph)):
        for j in graph[i]:
            if j == v:
                l = source_list(i, graph)
                if l != []:
                    ans.append(l)
    return ans

def list_to_string(l):
    ans = ''
    for i in range(len(l)):
        if type(l[i]) == int:
            f = False
            for j in range(i + 1, len(l)):
                if type(l[j]) == list:
                    f = True
            if f:
                ans += str(l[i] + 1) + '('
                for j in range(i + 1, len(l)):
                    ans += list_to_string(l[j])
                    if j != len(l) - 1:
                        ans += ', '
                ans += ')'
            else:
                for j in range(i, len(l)):
                    ans += str(l[j] + 1)
                    if j != len(l) - 1:
                        ans += ', '
    return ans

def to_string(inp):
    graph = read_graph(inp)
    marks = []
    for _ in graph:
        marks.append(0)
    v = 0
    while True:
        if v == len(marks):
            break
        if marks[v] == 0:
            marks = dfs(graph, v, marks)
        v += 1
    f = []
    for i in range(len(graph)):
        if graph[i] == []:
            f.append(i)
    ans = []
    for i in f:
        ans.append(list_to_string(source_list(i, graph)))
    return ans

def my_exp(x):
    return math.exp(x)

def my_sum(*args):
    ans = 0
    for i in args:
        ans += i
    return ans

def my_mult(*args):
    ans = 1
    for i in args:
        ans *= i
    return ans

def caluculate(inp1, inp2, out):
    string = to_string(inp1)
    calc_string = []
    try:
        operations = open(inp2, 'r')
        old_line = operations.read().split('\n')
        line = []
        for i in old_line:
            line.append(i.split(':'))
    except Exception:
        print("Файл не найден")
        exit()
    while True:
        for i in range(len(line)):
            if line[i] == ['']:
                break
        if i != len(line) - 1 or (i == len(line) - 1 and line[i] == ['']):
            line.pop(i)
        else:
            break
    for i in range(len(string)):
        for j in line:
            try:
                index = 0
                while True:
                    index = string[i].find(j[0], index)
                    if index == -1:
                        break
                    if index == 0:
                        string[i] = string[i].replace(j[0], '_' + j[1])
                    elif string[i][index - 1] != '_' and index != -1:
                        string[i] = string[i].replace(string[i][index - 1] + j[0], string[i][index - 1] + '_' + j[1])
                    index += 1
            except Exception:
                do_nothing = 0
        index = 0
        while True:
            index = string[i].find('_')
            if index != -1:
                string[i] = string[i][:index] + string[i][index + 1:]
            else:
                break
        calc_string.append(string[i])
        index = 0
        while True:
            index = calc_string[i].find('*', index)
            if index == 0:
                calc_string[i] = calc_string[i].replace('*', 'my_mult')
            elif calc_string[i][index - 1] != '_' and index != -1:
                calc_string[i] = calc_string[i].replace(calc_string[i][index - 1] + '*',
                                                        calc_string[i][index - 1] + 'my_mult')
            else:
                break
            index += 1
        index = 0
        while True:
            index = calc_string[i].find('+', index)
            if index == 0:
                calc_string[i] = calc_string[i].replace('+', 'my_sum')
            elif calc_string[i][index - 1] != '_' and index != -1:
                calc_string[i] = calc_string[i].replace(calc_string[i][index - 1] + '+',
                                                        calc_string[i][index - 1] + 'my_sum')
            else:
                break
            index += 1
        index = 0
        while True:
            index = calc_string[i].find('exp', index)
            if index == 0:
                calc_string[i] = calc_string[i].replace('exp', 'my_exp')
            elif calc_string[i][index - 1] != '_' and index != -1:
                calc_string[i] = calc_string[i].replace(calc_string[i][index - 1] + 'exp',
                                                        calc_string[i][index - 1] + 'my_exp')
            else:
                break
            index += 1
    ans = []
    for i in calc_string:
        try:
            ans.append(eval(i))
        except Exception:
            ans.append('Ошибка')
    with open(out, 'w') as calculated_functions:
        for i in range(len(calc_string)):
            calculated_functions.write(string[i] + ' = ' + str(ans[i]) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inp1', default='graph.txt')
    parser.add_argument('-inp2', default='operation.txt')
    parser.add_argument('-out', default='result.txt')
    args = parser.parse_args()
    values = caluculate(args.inp1, args.inp2, args.out)
    print("Программа выполнена успешно")

main()
