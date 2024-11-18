import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj_matrix = []  # Macierz sąsiedztwa
        self.weights_matrix = []  # Macierz wag krawędzi
        self.num_vertices = 0

    def add_vertex(self):
        self.num_vertices += 1
        for row in self.adj_matrix:
            row.append(0)  # Dodajemy kolumnę do macierzy sąsiedztwa
        self.adj_matrix.append([0] * self.num_vertices)  # Dodajemy nowy wiersz
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
        self.adj_matrix[i][j] += 1  # Dodajemy krawędź
        self.weights_matrix[i][j].append(weight)  # Dodajemy wagę krawędzi
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
        if weight is None:  # Usuń jedną krawędź
            self.adj_matrix[i][j] -= 1
            self.weights_matrix[i][j].pop()
            if not self.directed:
                self.adj_matrix[j][i] -= 1
                self.weights_matrix[j][i].pop()
        else:  # Usuń krawędź o określonej wadze
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
        
        # Use MultiGraph or MultiDiGraph to handle multiple edges
        G = nx.MultiDiGraph() if self.directed else nx.MultiGraph()
        size = len(self.adj_matrix)

        for i in range(size):
            G.add_node(i+1)

        # Add edges with their respective weights
        for i in range(size):
            for j in range(size):
                k = self.adj_matrix[i][j]
                if k > 0:
                    for edge_idx in range(k):
                        weight = self.weights_matrix[i][j][edge_idx]
                        G.add_edge(i+1, j+1, weight=weight)

        pos = nx.spring_layout(G)
        
        # Manually extract edge weights and associate them with the edge keys
        edge_labels = {}
        for u, v, key, data in G.edges(data=True, keys=True):
            edge_labels[(u, v, key)] = data['weight']

        # Draw the graph (nodes and edges)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2000)

        # Manually draw the edge labels for multi-edges
        for (u, v, key), label in edge_labels.items():
            x = (pos[u][0] + pos[v][0]) / 2
            y = (pos[u][1] + pos[v][1]) / 2
            plt.text(x, y, str(label), fontsize=12, ha='center', color='black')

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


# Example usage
g = Graph()
g.load_from_file("file.txt")
g.draw_graph("basegraph")
