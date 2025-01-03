from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx
from string import ascii_uppercase
import matplotlib.colors as mcolors


class CriticalPathMethod:
    def __init__(self, tasks):
        self.tasks = tasks
        self.graph = defaultdict(list)
        self.graph_mapping = defaultdict(list)
        self.weights = {}
        self.weights_mapping = {}
        self.order = []
        self.order_mapping = []
        self.ES = {}
        self.LS = {}
        self.critical_path = []
        self.edge_task_mapping = {}
        self.edge_task_mapping_new = {}
        self.topo_mapping = {}

    def build_graph(self):
        for start, end, duration in self.tasks:
            self.graph[start].append(end)
            self.weights[(start, end)] = duration

        G = nx.DiGraph()
        for (start, end), duration in self.weights.items():
            G.add_edge(start, end, task=f"z{len(G.edges) + 1}", duration=duration)
            self.edge_task_mapping[(start, end)] = f"z{len(G.edges)}"
        pos = nx.spring_layout(G)
        edge_labels = {edge: f"{G.edges[edge]['task']} ({G.edges[edge]['duration']})" for edge in G.edges}
        self.draw_graph(G, edge_labels, pos, "Graf wejściowy", "graf_wejsciowy.png", node_color="#9932CC")

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


        self.topo_mapping = {node: ascii_uppercase[i] for i, node in enumerate(self.order)}

        G_t = nx.DiGraph()
        for (start, end), duration in self.weights.items():
            mapped_start = self.topo_mapping[start]
            mapped_end = self.topo_mapping[end]
            G_t.add_edge(mapped_start, mapped_end, task=self.edge_task_mapping[(start, end)], duration=duration)
        pos_t = nx.spring_layout(G_t)
        edge_labels_topo = {edge: f"{G_t.edges[edge]['task']} ({G_t.edges[edge]['duration']})" for edge in G_t.edges}
        self.draw_graph(G_t, edge_labels_topo, pos_t, "Graf topologiczny", "graf_topologiczny.png", node_color="#9370DB")


        new_graph = defaultdict(list)
        for node, neighbors in self.graph.items():
            mapped_node = self.topo_mapping[node]
            for neighbor in neighbors:
                mapped_neighbor = self.topo_mapping[neighbor]
                new_graph[mapped_node].append(mapped_neighbor)
        self.graph_mapping = new_graph


        mapped_order = [self.topo_mapping[node] for node in self.order]
        self.order_mapping = mapped_order

        new_weights = {}
        for (start, end), duration in self.weights.items():
            mapped_start = self.topo_mapping[start]
            mapped_end = self.topo_mapping[end]
            new_weights[(mapped_start, mapped_end)] = duration
        self.weights_mapping = new_weights

        edge_task_mapping_new = {}
        for (start, end), edge in self.edge_task_mapping.items():
            mapped_start = self.topo_mapping[start]
            mapped_end = self.topo_mapping[end]
            edge_task_mapping_new[(mapped_start, mapped_end)] = edge
        self.edge_task_mapping_new = edge_task_mapping_new

        print("Topological Order:", [self.topo_mapping[node] for node in self.order])


    def calculate_ES(self):
        self.ES = {node: 0 for node in self.order_mapping}
        for node in self.order_mapping:
            for neighbor in self.graph_mapping[node]:
                self.ES[neighbor] = max(self.ES[neighbor], self.ES[node] + self.weights_mapping[(node, neighbor)])

        cmax = 0
        for task in self.ES.items():
            if task[1] > cmax:
                cmax = task[1]
       
        
        print("Earliest Start Times (ES):", self.ES)
        print("Długość uszeregowania (według ES) wynosi: ", cmax)


    def calculate_LS(self):
        max_time = max(self.ES.values())
        self.LS = {node: max_time for node in self.order_mapping[::-1]}

        for node in reversed(self.order_mapping):
            for neighbor in self.graph_mapping[node]:
                self.LS[node] = min(self.LS[node], self.LS[neighbor] - self.weights_mapping[(node, neighbor)])
        print("Latest Start Times (LS):", self.LS)
        

    def find_critical_path(self):
        self.critical_path = []
        current_node = self.order_mapping[0]
        while current_node != self.order_mapping[-1]:
            for neighbor in self.graph_mapping[current_node]:
                if self.ES[neighbor] == self.LS[neighbor]:
                    self.critical_path.append((current_node, neighbor))
                    current_node = neighbor
                    break

        print("Critical Path:", [self.edge_task_mapping_new[edge] for edge in self.critical_path])


        

    def draw_gantt_chart(self):
        plt.figure(figsize=(12, 8))
        machine_usage = defaultdict(list)
        task_colors = {}
        # available_colors = list(mcolors.TABLEAU_COLORS.values())
        available_colors = [
            "#8A2BE2",  
            "#BA55D3",  
            "#4B0082", 
            "#6A5ACD",  
            "#9932CC",  
            "#7B68EE",  
            "#9370DB", 
            "#9400D3",  
            "#6495ED",  
            "#8B008B",  
        ]

        for i, (start, end) in enumerate(self.weights_mapping):
            task_colors[(start, end)] = available_colors[i % len(available_colors)]

        for start, end in self.weights_mapping:
            start_time = self.ES[start]
            end_time = start_time + self.weights_mapping[(start, end)]
            for machine in range(len(machine_usage) + 1):
                if not any(start_time < m_end and end_time > m_start for m_start, m_end in machine_usage[machine]):
                    machine_usage[machine].append((start_time, end_time))
                    plt.plot(
                        [start_time, end_time],
                        [machine, machine],
                        linewidth=6,
                        color=task_colors[(start, end)],
                        label=self.edge_task_mapping_new[(start, end)] if machine == 0 else None
                    )
                    break

        legend_handles = [
            plt.Line2D([0], [0], color=color, linewidth=6, label=self.edge_task_mapping_new[(start, end)])
            for (start, end), color in task_colors.items()
        ]
        plt.legend(handles=legend_handles, title="Zadania", loc="upper right")

        plt.yticks(range(len(machine_usage)), [f"Machine {i + 1}" for i in range(len(machine_usage))])
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
        self.draw_gantt_chart()

tasks = [
    ("w1", "w2", 4),
    ("w1", "w3", 2),
    ("w2", "w4", 4),
    ("w3", "w4", 6)
]

# tasks = [
#     ('w2', 'w4', 2),
#     ('w2', 'w1', 3),
#     ('w1', 'w3', 2),
#     ('w4', 'w3', 1),
#     ('w3', 'w5', 4),
# ]

# tasks = [
#     ("w2", "w1", 3),
#     ("w1", "w3", 4),
#     ("w2", "w3", 2),
#     ("w1", "w4", 1),
#     ("w3", "w4", 2),
#     ("w3", "w5", 3),
#     ("w4", "w6", 2),
#     ("w5", "w6", 4)
# ]


cpm = CriticalPathMethod(tasks)
cpm.execute()
