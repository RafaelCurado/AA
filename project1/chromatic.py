import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import csv
from itertools import combinations, product

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



# EXAUSTIVE SEARCH

def is_valid_coloring(graph, coloring):
    for u, v in graph.edges():
        if coloring[u] == coloring[v]:
            return False
    return True 

def exhaustive_chromatic_number(graph):
    n = len(graph.nodes())

    for num_colors in range(1, n + 1):
        for coloring in product(range(num_colors), repeat=n):
            if is_valid_coloring(graph, coloring):
                return num_colors  
    return n  # Worst case -> chromatic number = N of vertices


# GREEDY HEURISTIC (TOP)

def greedy_chromatic_number_top(graph):
    n = len(graph.nodes())
    coloring = {}
    
    # Sort vertices by descending degree = n of edges
    vertices = sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)
    
    for vertex in vertices:
        neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}
        
        # Find the smallest available color that isn't used by neighbors
        color = 0
        while color in neighbor_colors:
            color += 1
        
        coloring[vertex] = color  # Assign the found color
    
    # Max color used + 1
    chromatic_number = max(coloring.values()) + 1
    return chromatic_number


# GREEDY HEURISTIC (BOTTOM)

def greedy_chromatic_number_bottom(graph):
    n = len(graph.nodes())
    coloring = {}
    
    # Sort vertices by ascending degree = n of edges
    vertices = sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=False)
    
    for vertex in vertices:
        neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(vertex) if neighbor in coloring}  
        
        # Find the smallest available color that isn't used by neighbors
        color = 0
        while color in neighbor_colors:
            color += 1
        
        coloring[vertex] = color  # Assign the found color
    
    # Max color used + 1
    chromatic_number = max(coloring.values()) + 1
    return chromatic_number




def main():
    edges = [12.5, 25, 50, 75]
    trials = 3
    maxVertices = 500

    with open('exec_times/greedy_top_times.csv', mode='w', newline='') as greedy_top_file, \
         open('exec_times/greedy_bottom_times.csv', mode='w', newline='') as greedy_bottom_file, \
         open('exec_times/exhaustive_times.csv', mode='w', newline='') as exhaustive_file:

        greedy_top_writer = csv.writer(greedy_top_file)
        greedy_bottom_writer = csv.writer(greedy_bottom_file)
        exhaustive_writer = csv.writer(exhaustive_file)

        headers = ['Vertices / Edge %'] + [f'{edge}%' for edge in edges]
        greedy_top_writer.writerow(headers)
        greedy_bottom_writer.writerow(headers)
        exhaustive_writer.writerow(headers)

        for num_vertices in range(4, maxVertices + 1):  # Adjusted range to include maxVertices

            greedy_top_row = [num_vertices]
            greedy_bottom_row = [num_vertices]
            exhaustive_row = [num_vertices]

            for possible_edges in edges:

                greedy_top_times = []
                greedy_bottom_times = []
                exhaustive_times = []

                G = generate_random_graph(num_vertices, possible_edges / 100)  # Generate the graph

                for trial in range(trials):
                    # Greedy Top
                    start = time.time()
                    chromatic_num_greedy_top = greedy_chromatic_number_top(G)
                    end = time.time()
                    greedy_top_times.append((end - start) * 10**3)

                    # Greedy Bottom
                    start = time.time()
                    chromatic_num_greedy_bottom = greedy_chromatic_number_bottom(G)
                    end = time.time()
                    greedy_bottom_times.append((end - start) * 10**3)

                    # Exhaustive Search (max 11 vertices)
                    if num_vertices <= 11:
                        start = time.time()
                        chromatic_num_exhaustive = None
                        chromatic_num_exhaustive = exhaustive_chromatic_number(G)
                        end = time.time()
                        exhaustive_times.append((end - start) * 10**3)


                avg_greedy_top_time = sum(greedy_top_times) / trials
                avg_greedy_bottom_time = sum(greedy_bottom_times) / trials
                
                greedy_top_row.append(avg_greedy_top_time)
                greedy_bottom_row.append(avg_greedy_bottom_time)

                if num_vertices <= 11:
                    avg_exhaustive_time = sum(exhaustive_times) / trials
                    exhaustive_row.append(avg_exhaustive_time)



                print(f"\n\n\n({num_vertices} vertices, {possible_edges}% edges)")

                print(f"\nGreedy Chromatic Number (Top): "+str(chromatic_num_greedy_top))
                print(f"Greedy (Top) Execution Time: {avg_greedy_top_time:.4f} ms")

                print(f"\nGreedy Chromatic Number (Bottom): "+str(chromatic_num_greedy_bottom))
                print(f"Greedy (Bottom) Execution Time: {avg_greedy_bottom_time:.4f} ms")

                print(f"\nExaustive Chromatic Number: "+str(chromatic_num_exhaustive))
                print(f"Exhaustive Execution Time: {avg_exhaustive_time:.4f} ms")

                
            # Write rows to CSV files
            greedy_top_writer.writerow(greedy_top_row)
            greedy_bottom_writer.writerow(greedy_bottom_row)
            if num_vertices <= 11:
                exhaustive_writer.writerow(exhaustive_row)


if __name__ == "__main__":
    main()
