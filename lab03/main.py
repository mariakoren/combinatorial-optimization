import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from collections import defaultdict

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj_matrix = [] 
        self.weights_matrix = []  
        self.num_vertices = 0

    def add_vertex(self):
        self.num_vertices += 1
        for row in self.adj_matrix:
            row.append(0) 
        self.adj_matrix.append([0] * self.num_vertices)  
        # Dodajemy pustą listę dla wag
        self.weights_matrix.append([[] for _ in range(self.num_vertices)])

    def delete_vertex(self, v):
        if v < 1 or v > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return
        v -= 1
        self.adj_matrix.pop(v)
        self.weights_matrix.pop(v)
        for row in self.adj_matrix:
            row.pop(v)
        for row in self.weights_matrix:
            row.pop(v)
        self.num_vertices -= 1

    def add_edge(self, i, j, weight=1):
        if i < 1 or j < 1 or i > self.num_vertices or j > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return
        i -= 1
        j -= 1
        self.adj_matrix[i][j] += 1  
        self.weights_matrix[i][j].append(weight) 
        if not self.directed:
            self.adj_matrix[j][i] += 1
            self.weights_matrix[j][i].append(weight)

    def delete_edge(self, i, j, weight=None):
        if i < 1 or j < 1 or i > self.num_vertices or j > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return
        i -= 1
        j -= 1
        if self.adj_matrix[i][j] == 0:
            print("Krawędź nie istnieje.")
            return
        if weight is None: 
            self.adj_matrix[i][j] -= 1
            self.weights_matrix[i][j].pop()
            if not self.directed:
                self.adj_matrix[j][i] -= 1
                self.weights_matrix[j][i].pop()
        else: 
            if weight in self.weights_matrix[i][j]:
                self.weights_matrix[i][j].remove(weight)
                self.adj_matrix[i][j] -= 1
                if not self.directed:
                    self.weights_matrix[j][i].remove(weight)
                    self.adj_matrix[j][i] -= 1
            else:
                print("Nie znaleziono krawędzi o podanej wadze.")

    def vertex_degree(self, v):
        if v < 1 or v > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return 0
        v -= 1
        if self.directed:
            in_degree = sum(self.adj_matrix[i][v] for i in range(self.num_vertices))
            out_degree = sum(self.adj_matrix[v][i] for i in range(self.num_vertices))
            return in_degree, out_degree, in_degree + out_degree
        else:
            return sum(self.adj_matrix[v])

    def min_graph_degree(self):
        if self.num_vertices == 0:
            return 0
        if not self.directed:
            return min(self.vertex_degree(v+1) for v in range(self.num_vertices))
        else:
            return min(self.vertex_degree(v+1)[2] for v in range(self.num_vertices))

    def max_graph_degree(self):
        if self.num_vertices == 0:
            return 0
        if not self.directed:
            return max(self.vertex_degree(v+1) for v in range(self.num_vertices))
        else:
            return max(self.vertex_degree(v+1)[2] for v in range(self.num_vertices))

    def even_odd_degrees(self):
        even, odd = 0, 0
        for v in range(self.num_vertices):
            if not self.directed:
                if self.vertex_degree(v+1) % 2 == 0:
                    even += 1
                else:
                    odd += 1
            else:
                _, _, sum_degree = self.vertex_degree(v+1)
                if sum_degree % 2 == 0:
                    even += 1
                else: 
                    odd += 1                
        return even, odd

    def sorted_vertex_degrees(self):
        if not self.directed:
            degrees = [self.vertex_degree(v+1) for v in range(self.num_vertices)]
            return sorted(degrees, reverse=True)
        else:
            degrees = [self.vertex_degree(v+1)[2] for v in range(self.num_vertices)]
            return sorted(degrees, reverse=True)

    def draw_graph(self, filename):
        plt.clf()
        G = nx.MultiDiGraph() if self.directed else nx.MultiGraph()
        size = len(self.adj_matrix)

        for i in range(size):
            G.add_node(i + 1)
        for i in range(size):
            for j in range(size):
                k = self.adj_matrix[i][j]
                if k > 0:
                    for edge_idx in range(k):
                        weight = self.weights_matrix[i][j][edge_idx]
                        G.add_edge(i + 1, j + 1, weight=weight, key=edge_idx)

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
        nx.draw_networkx_labels(G, pos, font_weight='bold')
        edge_labels = {}
        for u, v, key, data in G.edges(data=True, keys=True):
            edge_labels[(u, v, key)] = data['weight']
        ax = plt.gca()
        for (u, v, key), label in edge_labels.items():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            if u == v:
                loop = FancyArrowPatch((x0, y0), (x0 + 0.1, y0 + 0.1),
                                       connectionstyle=f"arc3,rad={0.3 + 0.1 * key}",
                                       arrowstyle='-', color='black')
                ax.add_patch(loop)
                plt.text(x0 + 0.15, y0 + 0.15, str(label), fontsize=10, color='black')
            else:
                arc = FancyArrowPatch((x0, y0), (x1, y1),
                                      connectionstyle=f"arc3,rad={0.2 * (key - len(G[u][v]) // 2)}",
                                      arrowstyle='-', color='black')
                ax.add_patch(arc)
                mid_x = (x0 + x1) / 2 + 0.1 * key
                mid_y = (y0 + y1) / 2 + 0.1 * key
                plt.text(mid_x, mid_y, str(label), fontsize=10, ha='center', color='black')

        plt.savefig(f"{filename}.png")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines() 
                graph_type = lines[0].strip()
                if graph_type == 'S':
                    self.directed = True
                elif graph_type == 'N':
                    self.directed = False
                else:
                    raise ValueError("Nieprawidłowy typ grafu. Użyj 'S' dla skierowanego lub 'N' dla nieskierowanego.")    
                self.num_vertices = int(lines[1].strip())
                self.adj_matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
                self.weights_matrix = [[[] for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]
                for line in lines[2:]:
                    i, j, w = map(int, line.split())
                    self.add_edge(i, j, w)
        
        except FileNotFoundError:
            print("Plik nie został znaleziony.")
        except ValueError as ve:
            print(f"Błąd w danych: {ve}")

    def display_matrices(self):
        print("Macierz sąsiedztwa:")
        for row in self.adj_matrix:
            print(row)
        print("\nMacierz wag:")
        for row in self.weights_matrix:
            print(["; ".join(map(str, cell)) if cell else "[]" for cell in row])


    def perfect_matching(self):
        # Upewnij się, że liczba wierzchołków w pełnym grafie jest parzysta
        if self.num_vertices % 2 != 0:
            print("Nie można znaleźć dokładnego skojarzenia, ponieważ liczba wierzchołków jest nieparzysta.")
            return None

        # Używamy NetworkX do znalezienia maksymalnego skojarzenia wagowego
        matching = nx.max_weight_matching(self.to_networkx(), maxcardinality=True, weight='weight')

        # Sprawdzamy, czy skojarzenie jest dokładne
        if len(matching) == self.num_vertices // 2:
            print(f"Znaleziono dokładne skojarzenie: {matching}")
        else:
            print("Nie znaleziono dokładnego skojarzenia.")
            return None

        return matching
    def chineese_postman(self):
        # Zidentyfikuj wierszchołki nieparzystego stopnia w grafie G.
        W = []
        for v in range(self.num_vertices):
            if not self.directed:
                if self.vertex_degree(v+1) % 2 != 0:
                    W.append(v+1)
        print(f"Wierszchołki o nieparzystym stopniu to: {W}")

        # Skonstruuj pełny graf na podstawie wierzchołków W
        # oraz najkrótszych ścieżek między nimi w grafie G
        G_full = nx.Graph()


        for vertex in W:
            G_full.add_node(vertex)

        shortest_paths_list = [] # u, v, shortest_path
        for i in range(len(W)):
            for j in range(i + 1, len(W)):
                u, v = W[i], W[j]
                shortest_path = nx.shortest_path(self.to_networkx(), source=u, target=v, weight='weight')
                shortest_path_length = nx.shortest_path_length(self.to_networkx(), source=u, target=v, weight='weight')
                shortest_paths_list.append((u, v, shortest_path))
                G_full.add_edge(u, v, weight=shortest_path_length)


        plt.clf()
        pos = nx.spring_layout(G_full)
        nx.draw(G_full, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2000)
        edge_labels = nx.get_edge_attributes(G_full, 'weight')
        nx.draw_networkx_edge_labels(G_full, pos, edge_labels=edge_labels)
        plt.savefig("g_full")

        print("Zapisano pełny graf z wierszchołków o nieparzystym stopniu do pliku g_full.png")


        # Znajdź minimalne skojarzenie dokładne M w grafie G'
        matching = nx.algorithms.matching.min_weight_matching(G_full, weight='weight')
        print(f"Minimalne dokładne skojarzenie: {matching}")
        plt.clf()
        pos = nx.spring_layout(G_full)
        nx.draw(
            G_full, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2000
        )
        edge_labels = nx.get_edge_attributes(G_full, 'weight')
        nx.draw_networkx_edge_labels(G_full, pos, edge_labels=edge_labels)
        matching_edges = list(matching)
        nx.draw_networkx_edges(
            G_full, pos, edgelist=matching_edges, edge_color='purple', width=2.5
        )
        plt.savefig("g_full_matching.png")

        # Dla każdej krawędzi e z M dodaj krawędzie w grafie G, 
        # które odpowiadają najkrótszej ścieżce opdpowiadającej e

        for u, v in matching:
            for element in shortest_paths_list:
                if (element[0] == u and element[1] == v) or (element[0] == v and element[1] == u):
                    shortest_path = element[2]
                    print(f"Dodawanie krawędzi dla najkrótszej ścieżki {shortest_path} odpowiadającej {u}-{v}")
                    for i in range(len(shortest_path) - 1):
                        start = shortest_path[i]
                        end = shortest_path[i + 1]
                        weight = self.to_networkx().edges[start, end]['weight']
                        self.add_edge(start, end, weight=weight)
                        print(f"Dodano krawędź: {start} -> {end} o wadze {weight}")
        G_E = self.to_networkx()
        plt.clf()
        self.draw_graph("augmented_graph")
        print("Zapisano graf z dodatkowymi krawędziami do pliku augmented_graph.png")
        return self.adj_matrix, self.weights_matrix

    def to_networkx(self):
        G = nx.Graph()
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.adj_matrix[i][j] > 0:
                    weight = self.weights_matrix[i][j][0]
                    G.add_edge(i+1, j+1, weight=weight)
        return G



g = Graph()
g.load_from_file("file.txt")
g.draw_graph("basegraph")
adjMatrix, wMatrix = g.chineese_postman()


def find_eulerian_cycle(graph):
    G = nx.MultiGraph()
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if graph[i][j] > 0:
                for _ in range(graph[i][j]):
                    G.add_edge(i, j)

    if nx.is_eulerian(G):
        cycle = list(nx.eulerian_circuit(G))
        return cycle
    else:
        return None

cycle = find_eulerian_cycle(adjMatrix)
print("Cykl listonosza:")
if cycle:
    for u, v in cycle:
        print(f"({u+1}, {v+1})", end=" ")
    print()
else:
    print("Graf nie ma cyklu Eulera")


sumw= 0
for i, j in cycle:
    sumw += wMatrix[i][j][0]
    
print(f"Długość trasy: {sumw}")




    
