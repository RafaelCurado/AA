import random
import networkx as nx
import numpy as np
import os
import pickle
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


def save_graph(graph, folder, filename):
    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(graph, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_graph(folder, filename):
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return None
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        print(f"Error: Corrupted file {filepath}.")
        return None