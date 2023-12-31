import argparse
import json

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

def write_func(inp, out):
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
    output_graph = open(out, 'w')
    for i in ans:
        output_graph.write(i + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inp', default='graph.txt')
    parser.add_argument('-out', default='functions.txt')
    args = parser.parse_args()
    values = write_func(args.inp, args.out)
    print("Программа выполнена успешно")

main()
