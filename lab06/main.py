from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx

class TaskScheduler:
    def __init__(self, edges, machines):
        self.graph = defaultdict(list)
        self.indegree = defaultdict(int)
        self.levels = defaultdict(int)
        self.tasks = set()
        self.machines = machines
        self.reverse_graph = defaultdict(list)  # For checking predecessors

        for u, v in edges:
            self.graph[u].append(v)
            self.reverse_graph[v].append(u)  # Store reverse edges for predecessor checking
            self.indegree[v] += 1
            self.tasks.add(u)
            self.tasks.add(v)

    def compute_levels(self):
        # Start with tasks that have no incoming edges
        root_nodes = [node for node in self.tasks if self.indegree[node] == 0]
        queue = deque(root_nodes)
        level = 1

        while queue:
            current = queue.popleft()
            self.levels[current] = level

            for neighbor in self.graph[current]:
                self.indegree[neighbor] -= 1  # Reduce indegree since we are processing `current`
                if self.indegree[neighbor] == 0:
                    queue.append(neighbor)

            level += 1

    def schedule_tasks(self):
        schedule = []
        time = 0
        completed_tasks = set()
        available_tasks = deque()

        # Add tasks with no predecessors (those with indegree 0)
        for task in self.tasks:
            if self.indegree[task] == 0:
                available_tasks.append(task)

        # Scheduling tasks
        while len(completed_tasks) < len(self.tasks):
            # Sort available tasks by level (higher level first)
            available_tasks = deque(sorted(available_tasks, key=lambda task: self.levels[task]))

            current_schedule = []
            for _ in range(min(self.machines, len(available_tasks))):
                task = available_tasks.popleft()
                current_schedule.append(task)
                completed_tasks.add(task)

                # Add new tasks to available_tasks if all their predecessors are completed
                for neighbor in self.graph[task]:
                    self.indegree[neighbor] -= 1
                    if self.indegree[neighbor] == 0 and neighbor not in completed_tasks:
                        available_tasks.append(neighbor)

            # Ensure that only tasks from the same or higher level are scheduled
            # Filter out tasks from a lower level than the highest level of the current tasks
            max_level = max([self.levels[task] for task in current_schedule])
            available_tasks = deque([task for task in available_tasks if self.levels[task] >= max_level])

            if current_schedule:
                schedule.append((time, current_schedule))
                time += 1

        return schedule

    def draw_gantt_chart(self, schedule):
        fig, ax = plt.subplots(figsize=(10, 6))

        for start_time, tasks in schedule:
            for machine_id, task in enumerate(tasks):
                ax.broken_barh([(start_time, 1)], (machine_id + 1, 0.8), facecolors=("tab:blue"))
                ax.text(start_time + 0.5, machine_id + 1.4, task, ha='center', va='center', color='white')

        ax.set_xlabel('Time')
        ax.set_ylabel('Machines')
        ax.set_yticks([i + 1 for i in range(self.machines)])
        ax.set_yticklabels([f'Machine {i + 1}' for i in range(self.machines)])
        ax.grid(True)
        plt.savefig("gantt_chart.png")

    def draw_task_graph(self):
        G = nx.DiGraph()
        for u in self.graph:
            for v in self.graph[u]:
                G.add_edge(u, v)

        # Ensure all tasks are included, even if they have no edges
        for task in self.tasks:
            if task not in G:
                G.add_node(task)

        # Draw the graph
        plt.figure(figsize=(10, 6))
        nx.draw(G, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)
        plt.title("Task Graph")
        plt.savefig("task_graph.png")

    def compute_cmax(self, schedule):
        return max(time for time, _ in schedule) + 1

# Example input
graph_edges = [
    ("z1", "z5"),
    ("z2", "z6"),
    ("z3", "z6"),
    ("z5", "z8"),
    ("z6", "z7"),
    ("z4", "z7"),
    ("z8", "z9"),
    ("z7", "z9")    
]
num_machines = 2

scheduler = TaskScheduler(graph_edges, num_machines)
scheduler.compute_levels()
schedule = scheduler.schedule_tasks()
scheduler.draw_gantt_chart(schedule)
scheduler.draw_task_graph()
cmax = scheduler.compute_cmax(schedule)

print("Cmax:", cmax)
