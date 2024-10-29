import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists('plots'):
    os.makedirs('plots')

# Read csvs
greedy_data = pd.read_csv('greedy_results.csv')
exhaustive_data = pd.read_csv('exhaustive_results.csv')

# Strip the '%' 
edges = greedy_data.columns[1:].str.rstrip('%').astype(float)  
vertices = greedy_data['Vertices / Edge %']  


greedy_execution_times = greedy_data.iloc[:, 1:].values  
exhaustive_execution_times = exhaustive_data.iloc[:, 1:].values

# --- Line Plot for Greedy Algorithm ---
plt.figure(figsize=(10, 6))

for i, edge_percentage in enumerate(edges):
    plt.plot(vertices, greedy_execution_times[:, i], label=f'{edge_percentage}% Edges (Greedy)')


plt.title('Greedy Algorithm Execution Times vs Number of Vertices')
plt.xlabel('Number of Vertices')
plt.ylabel('Execution Time (ms)')
plt.legend(title='Edge Percentage')
plt.grid(True)
plt.savefig('plots/greedy_algorithm_plot.png')  # Save the plot
plt.show()

# --- Line Plot for Exhaustive Algorithm ---
plt.figure(figsize=(10, 6))

for i, edge_percentage in enumerate(edges):
    plt.plot(vertices, exhaustive_execution_times[:, i], label=f'{edge_percentage}% Edges (Exhaustive)')

plt.ylim(0, 46)  # Adjust the Y 

plt.title('Exhaustive Algorithm Execution Times vs Number of Vertices')
plt.xlabel('Number of Vertices')
plt.ylabel('Execution Time (ms)')
plt.legend(title='Edge Percentage')
plt.grid(True)
plt.savefig('plots/exhaustive_algorithm_plot.png')  # Save the plot
plt.show()




# --- Plot comparison of greedy and exhaustive for a specific edge percentage ---
def plot_comparison_for_edge_percentage(edge_percentage):
    edge_index = edges.tolist().index(edge_percentage)
    
    # Create a figure
    plt.figure(figsize=(10, 6))
    
    # Plot both Greedy and Exhaustive times
    plt.plot(vertices, greedy_execution_times[:, edge_index], label=f'{edge_percentage}% Edges (Greedy)', marker='o', linestyle='-')
    plt.plot(vertices, exhaustive_execution_times[:, edge_index], label=f'{edge_percentage}% Edges (Exhaustive)', marker='o', linestyle='--')
    
    plt.title(f'Greedy vs Exhaustive Algorithm Execution Times ({edge_percentage}% Edges)')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Execution Time (ms)')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f'plots/greedy_vs_exhaustive_{edge_percentage}_percent_edges.png')
    plt.show()


for edge_percentage in [12.5, 25, 50, 75]:
    plot_comparison_for_edge_percentage(edge_percentage)
