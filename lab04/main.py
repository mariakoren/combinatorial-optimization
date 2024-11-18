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
    for u in graph.nodes():
        for v in graph.nodes():
            if u != v:
                for w in graph.nodes():
                    if u != w and v != w:
                        if graph.has_edge(u, v) and graph.has_edge(v, w) and graph.has_edge(w, u):
                            uv_weight = graph[u][v]['weight']
                            vw_weight = graph[v][w]['weight']
                            wu_weight = graph[w][u]['weight']
                            if uv_weight + vw_weight <= wu_weight or uv_weight + wu_weight <= vw_weight or vw_weight + wu_weight <= uv_weight:
                                return False
    return True


# Algorytm Christofidesa
def christofides(graph):
    print("Krok 1: Sprawdzenie nierówności trójkąta")
    if not verify_triangle_inequality(graph):
        print("Graf nie spełnia nierówności trójkąta!")
        return None
    print("Nierówność trójkąta spełniona")

    print("Krok 2: Obliczanie minimalnego drzewa rozpinającego (MST)")
    mst = nx.minimum_spanning_tree(graph)

    print("Krok 3: Znalezienie wierzchołków o nieparzystym stopniu w MST")
    odd_degree_nodes = [v for v, deg in mst.degree() if deg % 2 != 0]

    print("Krok 4: Minimalne skojarzenie dla wierzchołków o nieparzystym stopniu")
    subgraph = graph.subgraph(odd_degree_nodes)
    matching = nx.max_weight_matching(subgraph, maxcardinality=True, weight='weight')

    print("Krok 5: Połączenie MST i parowania")
    eulerian_graph = nx.MultiGraph(mst)
    for u, v in matching:
        eulerian_graph.add_edge(u, v, weight=subgraph[u][v]['weight'])

    print("Krok 6: Sprawdzanie, czy graf jest Eulera")
    if not nx.is_connected(eulerian_graph) or any(deg % 2 != 0 for v, deg in eulerian_graph.degree()):
        print("Graf nie jest Eulera!")
        return None

    eulerian_cycle = list(nx.eulerian_circuit(eulerian_graph))
    return mst, odd_degree_nodes, matching, eulerian_cycle



def draw_graph(graph, mst=None, matching=None, odd_degree_nodes=None, filename="graph"):
    pos = nx.spring_layout(graph)
    node_colors = ['lavender' if node in odd_degree_nodes else 'lightblue' for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, font_weight='bold', edge_color='gray')
    if mst is not None:
        nx.draw_networkx_edges(mst, pos, edge_color='purple', width=10)
    if matching is not None:
        matching_edges = list(matching)
        nx.draw_networkx_edges(graph, pos, edgelist=matching_edges, edge_color='skyblue', width=2)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, font_color='black')
    plt.savefig(f"{filename}.png")
    plt.close()


graph = Graph(directed=False)
graph.load_from_file("file.txt")
mst, odd_degree_nodes, matching, eulerian_cycle = christofides(graph.graph)

if eulerian_cycle:
    print(f"Cykl Eulera: {eulerian_cycle}")




draw_graph(graph.graph, mst=mst, matching=matching, odd_degree_nodes=odd_degree_nodes)
