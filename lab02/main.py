import matplotlib.pyplot as plt
import networkx as nx
import random

class Graph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = len(matrix)
        self.edges = [(i, j) for i in range(self.size) for j in range(i+1, self.size) if self.matrix[i][j] > 0]
    
    def remove_edge(self, u, v):
        if self.matrix[u][v] > 0:
            self.matrix[u][v] -= 1
            self.matrix[v][u] -= 1
            self.edges = [(i, j) for (i, j) in self.edges if i != u and i != v and j != u and j != v]

    def has_edges(self):
        return len(self.edges) > 0
    
    

    def draw_graph(self, filename, cover_nodes=None, cover_edges=None):
        plt.clf()
        G = nx.Graph()

        for i in range(self.size):
            G.add_node(i+1)
        

        for i in range(self.size):
            for j in range(i+1, self.size):
                if self.matrix[i][j] > 0:
                    G.add_edge(i+1, j+1)
        
        pos = nx.spring_layout(G)
        

        node_colors = []
        for node in G.nodes():
            if cover_nodes and node in cover_nodes:
                node_colors.append('purple')
            else:
                node_colors.append('lightblue')

        edge_colors = []
        for edge in G.edges():
            if cover_edges and edge in cover_edges:
                edge_colors.append('red')
            else:
                edge_colors.append('black')

        nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, font_weight='bold')
        plt.savefig(f"{filename}.png")

def read_edges_from_file(filename):
    edges = []
    max_node = 0
    
    with open(filename, 'r') as file:
        for line in file:
            u, v = map(int, line.split())
            edges.append((u - 1, v - 1))
            max_node = max(max_node, u, v)

    matrix = [[0] * max_node for _ in range(max_node)]
    for u, v in edges:
        matrix[u][v] = 1
        matrix[v][u] = 1
    
    return matrix
def vertex_cover_2_approx(graph):
    cover = set()
    cover_edges = set()
    step = 1 

    print("\nEtapy działania algorytmu:")
    

    while graph.has_edges():
        u, v = random.choice(graph.edges)
        
        print(f"\nEtap {step}:")
        print(f"Wybieram krawędź: ({u+1}, {v+1})")

        cover.add(u + 1)
        cover.add(v + 1)
        cover_edges.add((u + 1, v + 1)) 
        print(f"Dodaję wierzchołki {u+1} i {v+1} do pokrycia")

        graph.draw_graph(f"graph_step_{step}_1", cover_nodes=cover, cover_edges=cover_edges)
        print(f"Zapisano graf po etapie {step} do pliku: graph_step_{step}_1.png")
        graph.remove_edge(u, v)

        for neighbor in range(graph.size):
            if graph.matrix[u][neighbor] > 0:
                graph.matrix[u][neighbor] = 0
                graph.matrix[neighbor][u] = 0
                graph.remove_edge(u, neighbor)
                print(f"Usuwam krawędź incydentną: ({u+1}, {neighbor+1})")
            if graph.matrix[v][neighbor] > 0:
                graph.matrix[v][neighbor] = 0
                graph.matrix[neighbor][v] = 0
                graph.remove_edge(v, neighbor)
                print(f"Usuwam krawędź incydentną: ({v+1}, {neighbor+1})")


        graph.draw_graph(f"graph_step_{step}_2", cover_nodes=cover, cover_edges=cover_edges)
        print(f"Zapisano graf po etapie {step} do pliku: graph_step_{step}_2.png")
        
        step += 1

    
    print(f"\nPokrycie wierzchołkowe: {cover}")
    print(f"Wykorzystano krawędzi: {cover_edges}")
    return cover, cover_edges


matrix = read_edges_from_file("file.txt")

g = Graph(matrix)
print("Graf przed rozpoczęciem algorytmu:")
g.draw_graph("initial_graph")


cover, cover_edges = vertex_cover_2_approx(g)

matrix1 = read_edges_from_file("file.txt")

g1 = Graph(matrix1)
g1.draw_graph("final", cover_edges=cover_edges, cover_nodes=cover)