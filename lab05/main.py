from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx
from string import ascii_uppercase
import matplotlib.colors as mcolors


class CriticalPathMethod:
    def __init__(self, tasks):
        self.tasks = tasks
        self.graph = defaultdict(list)
        self.weights = {}
        self.order = []
        self.ES = {}
        self.LS = {}
        self.critical_path = []
        self.node_mapping={}
        self.tasks_mapping =[]

    def build_graph(self):
        for start, end, duration in self.tasks:
            self.graph[start].append(end)
            self.weights[(start, end)] = duration

    def topological_sort(self):
        in_degree = defaultdict(int)
        for start, ends in self.graph.items():
            for end in ends:
                in_degree[end] += 1

        queue = deque([node for node in self.graph if in_degree[node] == 0])
        self.order = []

        while queue:
            current = queue.popleft()
            self.order.append(current)
            for neighbor in self.graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        self.node_mapping = {node: ascii_uppercase[i] for i, node in enumerate(self.order)}

        mapped_order = [self.node_mapping[node] for node in self.order]
        self.order = mapped_order



        new_weights = {}
        for (start, end), duration in self.weights.items():
            mapped_start = self.node_mapping[start]
            mapped_end = self.node_mapping[end]
            new_weights[(mapped_start, mapped_end)] = duration
        self.weights = new_weights


        new_graph = defaultdict(list)
        for node, neighbors in self.graph.items():
            mapped_node = self.node_mapping[node]
            for neighbor in neighbors:
                mapped_neighbor = self.node_mapping[neighbor]
                new_graph[mapped_node].append(mapped_neighbor)
        self.graph = new_graph

        self.tasks_mapping = [(self.node_mapping[start], self.node_mapping[end], duration)for start, end, duration in self.tasks]


            

    def calculate_ES(self):
        self.ES = {node: 0 for node in self.order}
        for node in self.order:
            for neighbor in self.graph[node]:
                self.ES[neighbor] = max(self.ES[neighbor], self.ES[node] + self.weights[(node, neighbor)])
        

    def calculate_LS(self):
        max_time = max(self.ES.values())
        self.LS = {node: max_time for node in self.order[::-1]}

        for node in reversed(self.order):
            for neighbor in self.graph[node]:
                self.LS[node] = min(self.LS[node], self.LS[neighbor] - self.weights[(node, neighbor)])

    def find_critical_path(self):
        self.critical_path = []
        for start, end in self.weights:
            if self.ES[start] == self.LS[start] and self.ES[end] == self.LS[end]:
                self.critical_path.append((start, end))

    def draw_gantt_chart(self):
        plt.figure(figsize=(12, 8))
        machine_usage = defaultdict(list)
        task_colors = {}  # Słownik dla kolorów zadań
        available_colors = list(mcolors.TABLEAU_COLORS.values())  # Lista dostępnych kolorów

        # Przypisanie kolorów do zadań
        for i, task in enumerate(self.tasks_mapping):
            task_colors[task] = available_colors[i % len(available_colors)]  # Wybieranie kolorów cyklicznie

        # Rysowanie zadań na diagramie Gantta
        for start, end, duration in self.tasks_mapping:
            start_time = self.ES[start]
            end_time = start_time + duration
            for machine in range(len(machine_usage) + 1):
                if not any(start_time < m_end and end_time > m_start for m_start, m_end in machine_usage[machine]):
                    machine_usage[machine].append((start_time, end_time))
                    plt.plot(
                        [start_time, end_time],
                        [machine, machine],
                        linewidth=6,
                        color=task_colors[(start, end, duration)],
                        label=f"{start}->{end}" if machine == 0 else None  # Label tylko raz
                    )
                    break

        # Dodanie legendy z opisem kolorów
        legend_handles = [
            plt.Line2D([0], [0], color=color, linewidth=6, label=f"{start}->{end}")
            for (start, end, duration), color in task_colors.items()
        ]
        plt.legend(handles=legend_handles, title="Zadania", loc="upper right")

        # Konfiguracja osi i tytułu
        plt.yticks(range(len(machine_usage)), [f"Machine {i+1}" for i in range(len(machine_usage))])
        plt.xlabel("Time")
        plt.ylabel("Machines")
        plt.title("Diagram Gantta z kolorami zadań")
        plt.grid(axis="x")
        plt.savefig("diagram_gantta.png")
        plt.close()

    def draw_graph(self, graph, edge_labels, pos, title, filename, node_color="lightblue"):
        plt.figure(figsize=(8, 6))
        nx.draw(graph, pos, with_labels=True, node_size=2000, node_color=node_color, font_size=10, font_weight="bold")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
        plt.title(title)
        plt.savefig(filename)
        plt.close()

    def execute(self):
        self.build_graph()
        self.topological_sort()
        self.calculate_ES()
        self.calculate_LS()
        self.find_critical_path()

        # # Graf wejściowy
        G = nx.DiGraph()
        for start, end, duration in self.tasks:
            G.add_edge(start, end, task=f"z{len(G.edges) + 1}", duration=duration)
        pos = nx.spring_layout(G)
        edge_labels_input = {edge: f"{G.edges[edge]['task']} ({G.edges[edge]['duration']})" for edge in G.edges}
        self.draw_graph(G, edge_labels_input, pos, "Graf wejściowy", "graf_wejsciowy.png", node_color="purple")


        G_t = nx.DiGraph()
        for start, end, duration in self.tasks_mapping:
            G_t.add_edge(start, end, task=f"z{len(G.edges) + 1}", duration=duration)
        pos = nx.spring_layout(G_t)
        edge_labels_input_t = {edge: f"{G_t.edges[edge]['task']} ({G_t.edges[edge]['duration']})" for edge in G_t.edges}
        self.draw_graph(G_t, edge_labels_input_t, pos, "Graf topologiczny", "graf_topologiczny.png", node_color="lavender")

        print("Topological Order:", self.order)
        print("Earliest Start Times (ES):", self.ES)
        print("Latest Start Times (LS):", self.LS)
        print("Critical Path:", self.critical_path)
        self.draw_gantt_chart()

        print(f"graf: {self.graph.edges}")


# Przykład użycia
tasks = [
    # ('w2', 'w1', 3),
    ('w2', 'w4', 2),
    ('w2', 'w1', 3),
    ('w1', 'w3', 2),
    ('w4', 'w3', 1),
    ('w3', 'w5', 4),
]

cpm = CriticalPathMethod(tasks)
cpm.execute()
