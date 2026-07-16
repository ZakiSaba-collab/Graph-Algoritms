import sys

def create_empty_graph(n):
    graph = []
    for _ in range(n + 1):
        graph.append([])
    return graph

def read_first_line(st_0):
    n = int(st_0[:-1])
    is_directed = st_0[-1] == "d"
    return n, is_directed
# Если граф ориент-ый, то is_directed становится True


# 1. Ввод списком рёбер
def read_edges(filename):
    file = open(filename, "r", encoding="utf-8")

    st_0 = file.readline().strip()
    n, is_directed = read_first_line(st_0)
    graph = create_empty_graph(n)

    for line in file:
        line = line.strip()

        if line == "":
            continue

        parts = line.split()

        x = int(parts[0])
        y = int(parts[1])

        if len(parts) == 3:
            w = int(parts[2])
        else:
            w = 1

        if is_directed:
            graph[x].append((y, w))
        else:
            if x < y:
                graph[x].append((y, w))
                graph[y].append((x, w))



    file.close()
    return graph, is_directed


# 2. Ввод списком смежности
def read_adjacency_list(filename):
    file = open(filename, "r", encoding="utf-8")
    st_0 = file.readline().strip()
    n, is_directed = read_first_line(st_0)
    graph = create_empty_graph(n)
    for x in range(1, n + 1):
        line = file.readline().strip()
        if line == "":
            continue
        parts = line.split()
        # если в начале строки есть номер вершины
        if ":" not in parts[0]:
            vertex = int(parts[0])
            elems = parts[1:]

        else:
            vertex = x
            elems = parts
        for elem in elems:
            y, w = elem.split(":")
            y = int(y)
            w = int(w)
            graph[vertex].append((y, w))
    file.close()
    return graph, is_directed

# 3. Ввод матрицей смежности
def read_adjacency_matrix(filename):
    file = open(filename, "r", encoding="utf-8")

    st_0 = file.readline().strip()
    n, is_directed = read_first_line(st_0)
    graph = create_empty_graph(n)

    for i in range(1, n + 1):
        row = list(map(int, file.readline().split()))

        for j in range(1, n + 1):
            w = row[j - 1]

            if w != 0:
                if is_directed:
                    graph[i].append((j, w))
                else:
                    if i < j:
                        graph[i].append((j, w))
                        graph[j].append((i, w))

    file.close()
    return graph, is_directed


#1
'''
Функция degrees(graph, is_directed) считает степени вершин графа. Граф передаётся в функцию в виде списка смежности.
Пример: graph = [[], [(2,1), (3,1)], [(3,1)], [(1,1)]]
Каждый элемент списка — список соседей вершины. Например: graph[1] = [(2,1), (3,1)] означает: из вершины 1 есть дуга в 2; из вершины 1 есть дуга в 3.
Сначала функция определяет количество вершин: n = len(graph) - 1 Из длины списка вычитается 1, так как graph[0] не используется.

Если граф ориентированный (is_directed = True), то вычисляются: полустепени исхода; полустепени захода.
Полустепень исхода показывает, сколько дуг выходит из вершины.
Она вычисляется как количество элементов в списке смежности вершины: len(graph[x])
Например: graph[1] = [(2,1), (3,1)] В списке 2 элемента, значит из вершины 1 выходят 2 дуги.

Полустепень захода показывает, сколько дуг входит в вершину. Для её вычисления программа двойным циклом
проходит по всем спискам смежности и проверяет, сколько раз рассматриваемая вершина встречается как конец дуги.
Например, для вершины 3 программа ищет пары: (3, w) во всех списках смежности.

Если граф неориентированный (is_directed = False), то вычисляется обычная степень вершины. это количество её соседей.
'''
def degrees(graph, is_directed):
    n = len(graph) - 1

    if is_directed:
        out_degree = []
        in_degree = []

        for x in range(1, n + 1):
            out_degree.append(len(graph[x]))

        for x in range(1, n + 1):
            count = 0

            for row in graph:
                for y, w in row:
                    if y == x:
                        count += 1

            in_degree.append(count)

        print("Полустепени исхода:")
        print(out_degree)

        print("Полустепени захода:")
        print(in_degree)

    else:
        degree = []
        for x in range(1, n + 1):
            degree.append(len(graph[x]))
        print("Вектор степеней:")
        print(degree)


#2
'''
Функция создает список смежности для ориентированного графа, делая его
временно неориентированным для программы. Для каждой вершины в новый список смежности
добавляют ее соседа, а соседу добавляют ее как соседа.
'''
def make_undirected(graph):
    n = len(graph) - 1
    new_graph = []
    for _ in range(n + 1):
        new_graph.append([])
    for x in range(1, n + 1):
        for y, w in graph[x]:
            new_graph[x].append((y, w))
            new_graph[y].append((x, w))
    return new_graph

#функция_1 в поиске компонент связности
'''
Создается список очередь. В него будут добавляться вершины, кот-ые нужно обработать позже.
Создается список компонента. В него будут добавляться вершины текущей компоненты, т.е. вершины,  до которых можно дойти из стартовой вершины.
1. Стартовая вершина, номер которой передается в функцию, записывается в очередь, помечаетс посещенной в общем списке посещенных вершин.
2. Запускается цикл "пока в очереди есть вершины, кот-ые нужно обработать",
берется первая вершина очереди
удаляется из очереди
добавляется в компоненту связности
далее берется ее вершина-сосед и, если она еще не отмечена как посещенная, то она добавляется в конец очереди и помечается как посещенная.
'''
def bfs(start, graph, visited):
    queue = []
    component = []
    queue.append(start)
    visited[start] = True
    while len(queue) > 0:
        v = queue[0]
        queue.pop(0)
        component.append(v)
        for y, w in graph[v]:
            if visited[y] == False:
                queue.append(y)
                visited[y] = True
    return component

#функция_2 в поиске компонент связности
def connected_components(graph):
    n = len(graph) - 1
    visited = [False] * (n + 1)
    components = []

    for v in range(1, n + 1):
        if visited[v] == False:
            component = bfs(v, graph, visited)
            components.append(component)

    print("Компоненты связности:")

    for comp in components:
        print(comp)

#3
'''
Для поиска СЛАБОЙ:
1. Ориентированный граф с помощью функции делаем неор-ым
2. Запускаю обычный поиск компоненты связности, состоящий из функции обхода всех вершин и bfs.
'''
def weak_components(graph):
    undirected_graph = make_undirected(graph)
    connected_components(undirected_graph)

#4
def dfs_strong(v, graph, visited, component):
    visited[v] = True
    component.append(v)

    for y, w in graph[v]:
        if visited[y] == False:
            dfs_strong(y, graph, visited, component)


def transpose_graph(graph):
    n = len(graph) - 1
    new_graph = [[] for _ in range(n + 1)]

    for x in range(1, n + 1):
        for y, w in graph[x]:
            new_graph[y].append((x, w))

    return new_graph


def strong_components(graph):
    n = len(graph) - 1
    components = []

    reversed_graph = transpose_graph(graph)

    for v in range(1, n + 1):
        visited1 = [False] * (n + 1)
        comp1 = []
        dfs_strong(v, graph, visited1, comp1)

        visited2 = [False] * (n + 1)
        comp2 = []
        dfs_strong(v, reversed_graph, visited2, comp2)

        component = []

        for x in comp1:
            if x in comp2:
                component.append(x)

        component.sort()

        if component not in components:
            components.append(component)

    print("Компоненты сильной связности:")

    for comp in components:
        print(comp)

#5
def floyd(graph):
    n = len(graph) - 1
    INF = 10 ** 9

    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    next_vertex = [[-1] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dist[i][i] = 0
        next_vertex[i][i] = i

    for x in range(1, n + 1):
        for y, w in graph[x]:
            dist[x][y] = w
            next_vertex[x][y] = y

    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_vertex[i][j] = next_vertex[i][k]

    print("Матрица расстояний:")

    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if dist[i][j] == INF:
                row.append("∞")
            else:
                row.append(dist[i][j])
        print(row)

    eccentricity = []

    for i in range(1, n + 1):
        if INF in dist[i][1:]:
            eccentricity.append(INF)
        else:
            eccentricity.append(max(dist[i][1:]))

    diameter = max(eccentricity)
    radius = min(eccentricity)

    def show_value(x):
        if x == INF:
            return "+Infinity"
        return x

    central = []
    peripheral = []

    for i in range(len(eccentricity)):
        if eccentricity[i] == radius:
            central.append(i + 1)
        if eccentricity[i] == diameter:
            peripheral.append(i + 1)

    print("Эксцентриситет:", [show_value(x) for x in eccentricity])
    print("Диаметр:", show_value(diameter))
    print("Радиус:", show_value(radius))
    print("Центральные вершины:", central)
    print("Периферийные вершины:", peripheral)

    print("Кратчайшие пути:")

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and dist[i][j] != INF:
                path = [i]
                current = i

                while current != j:
                    current = next_vertex[current][j]
                    path.append(current)

                path_str = "-".join(map(str, path))
                print(dist[i][j], ":", path_str)
        print()
#6
def dijkstra(graph, start, finish):
    n = len(graph) - 1
    INF = 10 ** 9

    dist = [INF] * (n + 1)
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)

    dist[start] = 0

    for _ in range(1, n + 1):
        v = -1

        for i in range(1, n + 1):
            if visited[i] == False and (v == -1 or dist[i] < dist[v]):
                v = i

        if v == -1 or dist[v] == INF:
            break

        visited[v] = True

        for y, w in graph[v]:
            if dist[v] + w < dist[y]:
                dist[y] = dist[v] + w
                parent[y] = v

    if dist[finish] == INF:
        print("Пути нет")
        return

    path = []
    current = finish

    while current != -1:
        path.append(current)
        current = parent[current]

    path.reverse()

    print("Расстояние:", dist[finish])
    print("Кратчайший путь:", path)


#7
def prim(graph):
    n = len(graph) - 1
    used = [False] * (n + 1)

    used[1] = True

    mst = []
    total_weight = 0

    while len(mst) < n - 1:
        min_edge = None
        min_weight = 10 ** 9

        for v in range(1, n + 1):
            if used[v]:
                for to, w in graph[v]:
                    if not used[to]:
                        if w < min_weight:
                            min_weight = w
                            min_edg7e = (v, to, w)

        if min_edge is None:
            print("Граф несвязный")
            return

        v, to, w = min_edge

        mst.append((v, to, w))
        total_weight += w
        used[to] = True

    print("Минимальное остовное дерево:")

    for edge in mst:
        print(edge)

    print("Вес дерева:", total_weight)

def get_value(args, key):
    if key in args:
        index = args.index(key)

        if index + 1 < len(args):
            return args[index + 1]

    print("Ошибка: после", key, "нужно указать значение")
    exit()


args = sys.argv

if "-h" in args:
    print("Автор: твое имя, группа: твоя группа")
    print("-e файл — список рёбер")
    print("-m файл — матрица смежности")
    print("-l файл — список смежности")
    print("-o файл — вывод в файл")
    print("-n число — начальная вершина")
    print("-d число — конечная вершина")
    exit()


input_keys = ["-e", "-m", "-l"]
count = 0

for key in input_keys:
    if key in args:
        count += 1

if count != 1:
    print("Ошибка: нужно указать ровно один ключ ввода: -e, -m или -l")
    exit()

if "-e" in args:
    filename = get_value(args, "-e")
    graph, is_directed = read_edges(filename)

elif "-m" in args:
    filename = get_value(args, "-m")
    graph, is_directed = read_adjacency_matrix(filename)

elif "-l" in args:
    filename = get_value(args, "-l")
    graph, is_directed = read_adjacency_list(filename)


if "-o" in args:
    output_filename = get_value(args, "-o")
    sys.stdout = open(output_filename, "w", encoding="utf-8")
print(graph)

degrees(graph, is_directed)
if is_directed:
    weak_components(graph)
    strong_components(graph)
else:
    connected_components(graph)

#5
floyd(graph)

#6
if "-n" in args:
    start = int(get_value(args, "-n"))
else:
    start = 1

if "-d" in args:
    finish = int(get_value(args, "-d"))
else:
    finish = len(graph) - 1

#7
if is_directed:
    undirected_graph = make_undirected(graph)
    prim(undirected_graph)
else:
    prim(graph)