import os
import random
import time
import csv
import networkx as nx
from itertools import product
from graph_utils import load_webgraph

# EXHAUSTIVE SEARCH with tracking of operations and configurations tested
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


# GREEDY HEURISTIC with tracking of operations and configurations tested
def greedy_chromatic_number(graph):
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


# RANDOM GREEDY with tracking of operations and configurations tested
def random_greedy_chromatic_number(graph, trials):
    basic_operations = 0
    configurations_tested = 0
    
    best_chromatic_number = float('inf')  # Initialize with a large value
    tested_orders = set()  # To store unique vertex orders
    vertices = list(graph.nodes())

    for _ in range(trials):
        # Generate a new unique vertex order
        while True:
            random.shuffle(vertices)
            vertex_order = tuple(vertices)  # Convert list to tuple for set operations
            if vertex_order not in tested_orders:
                tested_orders.add(vertex_order)
                break  # Found a new unique order

        # Perform greedy coloring on the randomized order
        coloring = {}
        for vertex in vertices:
            neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}
            color = 0
            while color in neighbor_colors:
                color += 1
                basic_operations += 1

            coloring[vertex] = color
            configurations_tested += 1  # Each assignment is considered a configuration
            

        # Compute chromatic number for this trial
        chromatic_number = max(coloring.values()) + 1
        best_chromatic_number = min(best_chromatic_number, chromatic_number)

    return best_chromatic_number, basic_operations, configurations_tested


# NETWORKX RANDOM SEQUENTIAL with tracking of operations and configurations tested
def networkx_random_sequential(graph, trials):
    """
    Compute the chromatic number using NetworkX's random_sequential strategy.
    """
    best_chromatic_number = float('inf')

    for _ in range(trials):
        coloring = nx.coloring.greedy_color(graph, strategy='random_sequential')
        
        chromatic_number = max(coloring.values()) + 1
        best_chromatic_number = min(best_chromatic_number, chromatic_number)

    return best_chromatic_number




def main():
    trials = 1
    graph_folder = "graphs_web"  
    facebook_folder = "graphs_web/facebook"
    sw_folder = "graphs_web/sw"
    exhaustive_max_vertices = 11

    # Open the CSV files for saving the results
    with open('results_webgraphs/facebook/greedy_results.csv', mode='w', newline='') as facebook_greedy_file, \
         open('results_webgraphs/facebook/exhaustive_results.csv', mode='w', newline='') as facebook_exhaustive_file, \
         open('results_webgraphs/facebook/random_greedy_results.csv', mode='w', newline='') as facebook_random_greedy_file, \
         open('results_webgraphs/facebook/nx_random_sequential_results.csv', mode='w', newline='') as facebook_nx_random_sequential_file, \
         open('results_webgraphs/sw/greedy_results.csv', mode='w', newline='') as sw_greedy_file, \
         open('results_webgraphs/sw/exhaustive_results.csv', mode='w', newline='') as sw_exhaustive_file, \
         open('results_webgraphs/sw/random_greedy_results.csv', mode='w', newline='') as sw_random_greedy_file, \
         open('results_webgraphs/sw/nx_random_sequential_results.csv', mode='w', newline='') as sw_nx_random_sequential_file:
        
        # Create CSV writers for both folders
        facebook_writers = {
            "greedy": csv.writer(facebook_greedy_file),
            "exhaustive": csv.writer(facebook_exhaustive_file),
            "random_greedy": csv.writer(facebook_random_greedy_file),
            "nx_random_sequential": csv.writer(facebook_nx_random_sequential_file),
        }
        sw_writers = {
            "greedy": csv.writer(sw_greedy_file),
            "exhaustive": csv.writer(sw_exhaustive_file),
            "random_greedy": csv.writer(sw_random_greedy_file),
            "nx_random_sequential": csv.writer(sw_nx_random_sequential_file),
        }

        headers = ['Vertices', 'Edges', 'Chromatic Number', 'Exec Time', 
                   'Basic Operations', 'Configurations Tested', 'Precision']
        for writer in facebook_writers.values():
            writer.writerow(headers[:-1])
        for writer in sw_writers.values():
            writer.writerow(headers[:-1])

        def process_directory(folder, writers):
            graph_files = [f for f in os.listdir(folder) if f.endswith(".edges") or f.endswith(".txt")]
            sorted_graph_files = []

            for graph_filename in graph_files:
                G = load_webgraph(graph_folder, graph_filename)  
                if G is not None:
                    num_vertices = len(G.nodes())
                    sorted_graph_files.append((num_vertices, graph_filename))
                else:
                    print(f"Failed to load graph: {graph_filename}")

            sorted_graph_files.sort(key=lambda x: x[0])

            for num_vertices, graph_filename in sorted_graph_files:
                G = load_webgraph(graph_folder, graph_filename)

                if G is None:
                    print(f"Graph {graph_filename} not found!")
                    continue

                num_edges = G.number_of_edges()

                # Greedy Heuristic 
                greedy_times = []
                greedy_basic_ops = 0
                greedy_configs = 0
                chromatic_num_greedy = None

                for _ in range(trials):
                    start = time.time()
                    chromatic_num_greedy, basic_ops_greedy, configs_greedy = greedy_chromatic_number(G)
                    end = time.time()
                    greedy_times.append((end - start) * 10**3)
                    greedy_basic_ops += basic_ops_greedy
                    greedy_configs += configs_greedy

                avg_greedy_time = sum(greedy_times) / trials
                avg_greedy_ops = greedy_basic_ops // trials
                avg_greedy_configs = greedy_configs // trials

                # Random Greedy Heuristic 
                random_greedy_times = []
                random_greedy_basic_ops = 0
                random_greedy_configs = 0
                chromatic_num_random_greedy = None

                for _ in range(trials):
                    start = time.time()
                    chromatic_num_random_greedy, basic_ops_random_greedy, configs_random_greedy = random_greedy_chromatic_number(G, min(500, 6*num_vertices))
                    end = time.time()
                    random_greedy_times.append((end - start) * 10**3)
                    random_greedy_basic_ops += basic_ops_random_greedy
                    random_greedy_configs += configs_random_greedy

                avg_random_greedy_time = sum(random_greedy_times) / trials
                avg_random_greedy_ops = random_greedy_basic_ops // trials
                avg_random_greedy_configs = random_greedy_configs // trials

                # NetworkX Random Sequential 
                nx_random_sequential_times = []
                chromatic_num_nx_random_sequential = None

                for _ in range(trials):
                    start = time.time()
                    chromatic_num_nx_random_sequential = networkx_random_sequential(G, min(500, 6*num_vertices))
                    end = time.time()
                    nx_random_sequential_times.append((end - start) * 10**3)

                avg_nx_random_sequential_time = sum(nx_random_sequential_times) / trials


                # Exhaustive Search (only for smaller instances)
                if num_vertices <= exhaustive_max_vertices:
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
                    writers["exhaustive"].writerow([num_vertices, num_edges, chromatic_num_exhaustive, 
                                                    f"{avg_exhaustive_time:.4f}", avg_exhaustive_ops, avg_exhaustive_configs])

                    greedy_precision = abs(chromatic_num_exhaustive - chromatic_num_greedy)
                    random_greedy_precision = abs(chromatic_num_exhaustive - chromatic_num_random_greedy)
                else:
                    greedy_precision = None
                    random_greedy_precision = None

                writers["greedy"].writerow([num_vertices, num_edges, chromatic_num_greedy, f"{avg_greedy_time:.4f}", avg_greedy_ops, avg_greedy_configs])
                writers["random_greedy"].writerow([num_vertices, num_edges, chromatic_num_random_greedy, f"{avg_random_greedy_time:.4f}", avg_random_greedy_ops, avg_random_greedy_configs])
                writers["nx_random_sequential"].writerow([num_vertices, num_edges, chromatic_num_nx_random_sequential, f"{avg_nx_random_sequential_time:.4f}", "", ""])

        # Process Facebook graphs
        process_directory(facebook_folder, facebook_writers)

        # Process SW graphs
        process_directory(sw_folder, sw_writers)

if __name__ == "__main__":
    main()