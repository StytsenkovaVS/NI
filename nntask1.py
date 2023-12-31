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


def write_to_json(graph, out):
    vertex = []
    for i in range(len(graph)):
        vertex.append(i + 1)
    edges = []
    for i in graph:
        if i != []:
            for j in i:
                edges.append({'from': graph.index(i) + 1, 'to': j + 1, 'order': i.index(j) + 1})
    ans = {'vertices': vertex, 'edges': edges}
    with open(out, 'w') as outfile:
        json.dump(ans, outfile, indent=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inp', default='graph.txt')
    parser.add_argument('-out', default='graph.json')
    args = parser.parse_args()
    values = write_to_json(read_graph(args.inp), args.out)
    print("Программа выполнена успешно")

main()

