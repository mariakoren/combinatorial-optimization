import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.graph = nx.Graph() if not directed else nx.DiGraph()

    def add_edge(self, u, v, weight=1):
        self.graph.add_edge(u, v, weight=weight)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines() 
                graph_type = lines[0].strip()
                self.directed = True if graph_type == 'S' else False
                self.graph = nx.DiGraph() if self.directed else nx.Graph()

                self.num_vertices = int(lines[1].strip())
                for line in lines[2:]:
                    u, v, weight = map(int, line.split())
                    self.add_edge(u, v, weight)
        except FileNotFoundError:
            print("Plik nie został znaleziony.")
        except ValueError as ve:
            print(f"Błąd w danych: {ve}")


# Sprawdzanie nierówności trójkąta
def verify_triangle_inequality(graph):
    for u, v, data in graph.edges(data=True):
        for w, _, data2 in graph.edges(data=True):
            if u != w and v != w:  # Unikamy sprawdzania w tych samych krawędziach
                if graph[u][w]['weight'] > data['weight'] + data2['weight']:
                    return False
    return True


# Algorytm Christofidesa
def christofides(graph):
    # Krok 1: Sprawdzenie nierówności trójkąta
    if not verify_triangle_inequality(graph):
        print("Graf nie spełnia nierówności trójkąta!")
        return None

    # Krok 2: Obliczanie minimalnego drzewa rozpinającego (MST)
    mst = nx.minimum_spanning_tree(graph)

    # Krok 3: Znalezienie wierzchołków o nieparzystym stopniu w MST
    odd_degree_nodes = [v for v, deg in mst.degree() if deg % 2 != 0]

    # Krok 4: Minimalne parowanie dla wierzchołków o nieparzystym stopniu
    # Zbuduj podgraf z wierzchołkami o nieparzystym stopniu
    subgraph = graph.subgraph(odd_degree_nodes)

    # Użycie funkcji max_weight_matching (minimalne parowanie)
    matching = nx.max_weight_matching(subgraph, maxcardinality=True, weight='weight')

    # Krok 5: Połączenie MST i parowania
    # Dodanie krawędzi z parowania do MST
    eulerian_graph = mst.copy()
    for u, v in matching:
        eulerian_graph.add_edge(u, v, weight=subgraph[u][v]['weight'])

    # Krok 6: Sprawdzanie, czy graf jest Eulera
    if not nx.is_connected(eulerian_graph) or any(deg % 2 != 0 for v, deg in eulerian_graph.degree()):
        print("Graf nie jest Eulera!")
        return None

    # Znalezienie cyklu Eulera
    eulerian_cycle = list(nx.eulerian_circuit(eulerian_graph))

    # Zwracamy wynik - cykl Eulera jako listę krawędzi
    return eulerian_cycle


# Rysowanie grafu
def draw_graph(graph, filename="graph"):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', font_weight='bold')
    plt.savefig(f"{filename}.png")
    plt.show()


# Przykład użycia
graph = Graph(directed=False)
graph.load_from_file("file.txt")  # Wczytaj graf z pliku

# Wykonanie algorytmu Christofidesa
eulerian_cycle = christofides(graph.graph)  # Zastosowanie algorytmu Christofidesa

if eulerian_cycle:
    print(f"Cykl Eulera: {eulerian_cycle}")

# Rysowanie grafu
draw_graph(graph.graph)
