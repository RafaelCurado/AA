### Manual chromatic (no trials)

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



def visualize_graph(G, coloring, filename):
    plt.figure(figsize=(8, 6))
    
    pos = nx.get_node_attributes(G, 'pos')

    colors = [
        'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 
        'gray', 'cyan', 'magenta', 'lime', 'olive', 'navy', 'maroon', 'teal',
        'gold', 'violet', 'turquoise', 'indigo', 'khaki', 'plum', 'salmon', 'tan'
    ]   


    node_colors = [colors[coloring[i]] for i in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=12, edge_color='gray')
    
    plt.savefig(filename)
    plt.show()


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
                return num_colors, coloring  
    return n, None  # Worst case -> chromatic number = N of vertices


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
    # edges = [12.5, 25, 50, 75]
    edges = [12.5]

    max_vertices = 10000    

    for num_vertices in range(4750, max_vertices+1):

        for possible_edges in edges:
            start = time.time()    
            G = generate_random_graph(num_vertices, possible_edges/100) # calculate points
            end = time.time()
            graph_generation_time = (end-start)*10**3


            start = time.time()    
            chromatic_num_greedy_top = greedy_chromatic_number_top(G)
            end = time.time()
            greedy_time_top = (end-start)*10**3


            print(f"\nVertices: "+str(num_vertices))
            print(f"Edges: "+str(possible_edges))
            print(f"Greedy Chromatic Number: "+str(chromatic_num_greedy_top))
            print(f"Greedy Execution Time: {greedy_time_top:.4f} ms")
            print(f"Graph Generation Time: {graph_generation_time:.4f} ms")

            # visualize_graph(G, coloring, f"graph_{num_vertices}_{possible_edges}.png")


if __name__ == "__main__":
    main()
