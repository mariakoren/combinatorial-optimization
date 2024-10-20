import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.matrix = []
        self.num_vertices = 0

    def add_vertex(self):
        self.num_vertices += 1
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * self.num_vertices)

    def delete_vertex(self, v):
        if v < 1 or v > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return
        v -= 1
        self.matrix.pop(v)
        for row in self.matrix:
            row.pop(v)
        self.num_vertices -= 1

    def add_edge(self, i, j):
        if i < 1 or j < 1 or i > self.num_vertices or j > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return
        self.matrix[i-1][j-1] += 1
        if not self.directed:
            self.matrix[j-1][i-1] += 1

    def delete_edge(self, i, j):
        if i < 1 or j < 1 or i > self.num_vertices or j > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return
        if self.matrix[i-1][j-1] == 0:
            print("Krawędź nie istnieje.")
            return
        self.matrix[i-1][j-1] -= 1
        if not self.directed:
            self.matrix[j-1][i-1] -= 1

    def vertex_degree(self, v):
        if v < 1 or v > self.num_vertices:
            print("Wierzchołek nie istnieje.")
            return 0
        v -= 1
        if self.directed:
            in_degree = sum(self.matrix[i][v] for i in range(self.num_vertices))
            out_degree = sum(self.matrix[v][i] for i in range(self.num_vertices))
            return in_degree, out_degree, in_degree+out_degree
        else:
            return sum(self.matrix[v])

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
        G = nx.DiGraph() if self.directed else nx.Graph()
        size = len(self.matrix)
        for i in range(size):
            G.add_node(i+1)
        for i in range(size):
            for j in range(size):
                if self.matrix[i][j] > 0:
                    for _ in range(self.matrix[i][j]):
                        G.add_edge(i+1, j+1)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')
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
                self.matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
                for line in lines[2:]:
                    i, j = map(int, line.split())
                    self.add_edge(i, j)
        
        except FileNotFoundError:
            print("Plik nie został znaleziony.")
        except ValueError as ve:
            print(f"Błąd w danych: {ve}")
