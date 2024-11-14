import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists('plots'):
    os.makedirs('plots')

# Read the CSVs for Greedy Top and Greedy Bottom heuristics
greedy_top_data = pd.read_csv('exec_times/greedy_top_times.csv')
greedy_bottom_data = pd.read_csv('exec_times/greedy_bottom_times.csv')
exhaustive_data = pd.read_csv('exec_times/exhaustive_times.csv')

# Strip the '%' symbol for easier handling of edge percentage values
edges = greedy_top_data.columns[1:].str.rstrip('%').astype(float)

# Extract vertices from each dataset
greedy_vertices = greedy_top_data['Vertices / Edge %']
exhaustive_vertices = exhaustive_data['Vertices / Edge %']

# Find common vertices across datasets for accurate plotting
common_vertices = greedy_vertices[greedy_vertices.isin(exhaustive_vertices)].values

# Filter the datasets to include only the common vertices
greedy_top_execution_times = greedy_top_data[greedy_top_data['Vertices / Edge %'].isin(greedy_vertices)].iloc[:, 1:].values
greedy_bottom_execution_times = greedy_bottom_data[greedy_bottom_data['Vertices / Edge %'].isin(greedy_vertices)].iloc[:, 1:].values
exhaustive_execution_times = exhaustive_data[exhaustive_data['Vertices / Edge %'].isin(common_vertices)].iloc[:, 1:].values

# --- Plot for Greedy Top Heuristic ---
plt.figure(figsize=(10, 6))
for i, edge_percentage in enumerate(edges):
    plt.plot(greedy_vertices, greedy_top_execution_times[:, i], label=f'{edge_percentage}% Edges (Greedy Top)')
plt.title('Greedy Algorithm Execution Times (Top Heuristic)')
plt.xlabel('Number of Vertices')
plt.ylabel('Execution Time (ms)')
plt.legend(title='Edge Percentage')
plt.grid(True, which="both", ls="--")
# plt.yscale('log')
plt.savefig('plots/greedy_top_plot.png')
plt.show()

# --- Plot for Greedy Bottom Heuristic ---
plt.figure(figsize=(10, 6))
for i, edge_percentage in enumerate(edges):
    plt.plot(greedy_vertices, greedy_bottom_execution_times[:, i], label=f'{edge_percentage}% Edges (Greedy Bottom)')
plt.title('Greedy Algorithm Execution Times (Bottom Heuristic)')
plt.xlabel('Number of Vertices')
plt.ylabel('Execution Time (ms)')
plt.legend(title='Edge Percentage')
plt.grid(True, which="both", ls="--")
plt.yscale('log')
plt.savefig('plots/greedy_bottom_plot.png')
plt.show()

# --- Plot for Exhaustive Algorithm ---
plt.figure(figsize=(10, 6))
for i, edge_percentage in enumerate(edges):
    plt.plot(common_vertices, exhaustive_execution_times[:, i], label=f'{edge_percentage}% Edges (Exhaustive)')
plt.title('Exhaustive Algorithm Execution Times vs Number of Vertices')
plt.xlabel('Number of Vertices')
plt.ylabel('Execution Time (ms)')
plt.legend(title='Edge Percentage')
plt.grid(True)
# plt.yscale('log')
plt.savefig('plots/exhaustive_algorithm_plot.png')
plt.show()


greedy_top_execution_times = greedy_top_data[greedy_top_data['Vertices / Edge %'].isin(common_vertices)].iloc[:, 1:].values
greedy_bottom_execution_times = greedy_bottom_data[greedy_bottom_data['Vertices / Edge %'].isin(common_vertices)].iloc[:, 1:].values


# --- Plot comparison of greedy and exhaustive for a specific edge percentage ---
def plot_comparison_for_edge_percentage(edge_percentage):
    edge_index = edges.tolist().index(edge_percentage)
    
    plt.figure(figsize=(10, 6))
    plt.plot(common_vertices, greedy_top_execution_times[:, edge_index], label=f'{edge_percentage}% Edges (Greedy (Top))', marker='o', linestyle='-')
    plt.plot(common_vertices, exhaustive_execution_times[:, edge_index], label=f'{edge_percentage}% Edges (Exhaustive)', marker='o', linestyle='--')
    
    plt.title(f'Greedy (Top) vs Exhaustive Algorithm Execution Times ({edge_percentage}% Edges)')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Execution Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')

    
    plt.savefig(f'plots/greedy_vs_exhaustive_{edge_percentage}_percent_edges.png')
    plt.show()

for edge_percentage in [12.5, 25, 50, 75]:
    plot_comparison_for_edge_percentage(edge_percentage)
