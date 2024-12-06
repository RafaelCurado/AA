import numpy as np
import networkx as nx
import random
import time
import csv
from itertools import combinations, product

# Set the random seed for reproducibility
studentN = 103199
random.seed(studentN)

def generate_unique_points(num_points, min_distance=10):
    points = set()
    while len(points) < num_points:
        x = random.randint(1, 1000)
        y = random.randint(1, 1000)
        point = (x, y)
        
        # Ensure points are unique and not too close to each other
        if all(np.linalg.norm(np.array(point) - np.array(p)) >= min_distance for p in points):
            points.add(point)

    return list(points)

def generate_random_graph(num_vertices, edge_percentage):
    points = generate_unique_points(num_vertices)
    G = nx.Graph()
    for i, point in enumerate(points):
        G.add_node(i, pos=point)

    max_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = int(max_edges * edge_percentage)
    possible_edges = list(combinations(range(num_vertices), 2))
    random_edges = random.sample(possible_edges, num_edges)
    G.add_edges_from(random_edges)
    return G

# Exhaustive Search with tracking of operations and configurations tested
def is_valid_coloring(graph, coloring):
    basic_operations = 0
    for u, v in graph.edges():
        basic_operations += 1
        if coloring[u] == coloring[v]:
            return False, basic_operations
    return True, basic_operations

def exhaustive_chromatic_number(graph):
    n = len(graph.nodes())
    basic_operations = 0
    configurations_tested = 0

    for num_colors in range(1, n + 1):
        for coloring in product(range(num_colors), repeat=n):
            configurations_tested += 1
            is_valid, edge_operations = is_valid_coloring(graph, coloring)  # Check if valid and get edge operations
            basic_operations += edge_operations    
            if is_valid:                            # If the coloring is valid
                return num_colors, basic_operations, configurations_tested
    return n, basic_operations, configurations_tested  # Worst case

# Greedy Heuristic (Top) with tracking of operations and configurations tested
def greedy_chromatic_number_top(graph):
    n = len(graph.nodes())
    coloring = {}
    basic_operations = 0
    configurations_tested = 0

    vertices = sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)
    
    for vertex in vertices:
        neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}
        color = 0
        while color in neighbor_colors:
            color += 1
            basic_operations += 1  # Checking if color is in neighbor_colors is a basic operation

        coloring[vertex] = color
        configurations_tested += 1  # Each assignment is considered a configuration
    
    chromatic_number = max(coloring.values()) + 1
    return chromatic_number, basic_operations, configurations_tested

# Main experiment function to log data to separate CSVs
def main():
    edges = [12.5, 25, 50, 75]
    trials = 3
    maxVertices = 15

    with open('metrics/greedy_results.csv', mode='w', newline='') as greedy_file, \
         open('metrics/exhaustive_results.csv', mode='w', newline='') as exhaustive_file:
        
        greedy_writer = csv.writer(greedy_file)
        exhaustive_writer = csv.writer(exhaustive_file)

        # CSV headers
        headers = ['Vertices', 'Edge %', 'Chromatic Number', 'Avg Time (ms)', 
                   'Basic Operations', 'Configurations Tested', 'Precision']
        greedy_writer.writerow(headers)
        exhaustive_writer.writerow(headers[:-1])  # Exhaustive doesn't need precision

        for num_vertices in range(4, maxVertices + 1):
            print("Vertices: "+str(num_vertices))
            for edge_percentage in edges:
                G = generate_random_graph(num_vertices, edge_percentage / 100)
                num_edges = G.number_of_edges()  # Get the number of edges
                edges_formatted = f"{num_edges} ({edge_percentage}%)"

                # Greedy Heuristic (Top)
                greedy_times = []
                greedy_basic_ops = 0
                greedy_configs = 0
                chromatic_num_greedy = None
                
                for _ in range(trials):
                    start = time.time()
                    chromatic_num_greedy, basic_ops_greedy, configs_greedy = greedy_chromatic_number_top(G)
                    end = time.time()
                    greedy_times.append((end - start) * 10**3)
                    greedy_basic_ops += basic_ops_greedy
                    greedy_configs += configs_greedy
                
                avg_greedy_time = sum(greedy_times) / trials
                avg_greedy_ops = greedy_basic_ops // trials
                avg_greedy_configs = greedy_configs // trials

                # Exhaustive Search (only for smaller instances)
                if num_vertices <= 11:
                    exhaustive_times = []
                    exhaustive_basic_ops = 0
                    exhaustive_configs = 0
                    chromatic_num_exhaustive = None

                    for _ in range(trials):
                        start = time.time()
                        chromatic_num_exhaustive, basic_ops_exhaustive, configs_exhaustive = exhaustive_chromatic_number(G)
                        end = time.time()
                        exhaustive_times.append((end - start) * 10**3)
                        exhaustive_basic_ops += basic_ops_exhaustive
                        exhaustive_configs += configs_exhaustive

                    avg_exhaustive_time = sum(exhaustive_times) / trials
                    avg_exhaustive_ops = exhaustive_basic_ops // trials
                    avg_exhaustive_configs = exhaustive_configs // trials
                    exhaustive_writer.writerow([num_vertices, edges_formatted, chromatic_num_exhaustive, 
                                                f"{avg_exhaustive_time:.4f}", avg_exhaustive_ops, avg_exhaustive_configs])

                    # Calculate precision
                    precision = abs(chromatic_num_exhaustive - chromatic_num_greedy)
                else:
                    precision = None  # Precision not applicable when exhaustive not run

                # Write greedy heuristic results with precision
                greedy_writer.writerow([num_vertices, edges_formatted, chromatic_num_greedy, f"{avg_greedy_time:.4f}", avg_greedy_ops, avg_greedy_configs, precision])

if __name__ == "__main__":
    main()
