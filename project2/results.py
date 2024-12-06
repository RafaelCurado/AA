import pandas as pd
import matplotlib.pyplot as plt
import os

# Create a directory to save plots if not existing
if not os.path.exists('plots'):
    os.makedirs('plots')

# Load and process CSV data
def load_and_process_csv(file_path):
    df = pd.read_csv(file_path)
    df['Edge %'] = df['Edge %'].str.extract(r'(\d+\.\d+|\d+)\s?\%').astype(float)
    return df

# Load datasets
df_greedy_full = load_and_process_csv("results/greedy_results.csv")
df_random_greedy_full = load_and_process_csv("results/random_greedy_results.csv")
df_nx_random_sequential_full = load_and_process_csv("results/nx_random_sequential_results.csv")

# Extract unique edge densities and vertices for each dataset
edges = df_greedy_full["Edge %"].unique()
vertices_greedy = df_greedy_full["Vertices"]
vertices_random_greedy = df_random_greedy_full["Vertices"]
vertices_nx_random_sequential = df_nx_random_sequential_full["Vertices"]

# Find common vertices across all datasets
common_vertices = vertices_greedy[
    vertices_greedy.isin(vertices_random_greedy) & vertices_greedy.isin(vertices_nx_random_sequential)
].unique()

# Filter datasets to include only common vertices (full data for comparison)
df_greedy_full = df_greedy_full[df_greedy_full["Vertices"].isin(common_vertices)]
df_random_greedy_full = df_random_greedy_full[df_random_greedy_full["Vertices"].isin(common_vertices)]
df_nx_random_sequential_full = df_nx_random_sequential_full[df_nx_random_sequential_full["Vertices"].isin(common_vertices)]

# Create sampled data for plotting
def reduce_samples_in_order(df, num_samples=50):
    return df.groupby("Edge %").apply(lambda x: x.iloc[::max(1, len(x) // num_samples)])

df_greedy_sampled = reduce_samples_in_order(df_greedy_full)
df_random_greedy_sampled = reduce_samples_in_order(df_random_greedy_full)
df_nx_random_sequential_sampled = reduce_samples_in_order(df_nx_random_sequential_full)

# --- Calculate Differences using Full Data ---
df_random_greedy_full["Difference"] = df_random_greedy_full["Chromatic Number"].values - df_greedy_full["Chromatic Number"].values
df_nx_random_sequential_full["Difference"] = df_nx_random_sequential_full["Chromatic Number"].values - df_greedy_full["Chromatic Number"].values
df_random_greedy_full["Random_vs_NX"] = df_random_greedy_full["Chromatic Number"].values - df_nx_random_sequential_full["Chromatic Number"].values

# --- Print Summary Statistics ---
def print_summary_statistics(algorithm_name, differences):
    print(f"\n--- {algorithm_name} vs Greedy ---")
    print(f"Overall Difference (Mean): {differences.mean():.2f}")
    print(f"{algorithm_name} Won (Lower Chromatic Number): {(differences < 0).sum()}")
    print(f"Tied (Equal Chromatic Number): {(differences == 0).sum()}")
    print(f"{algorithm_name} Lost (Higher Chromatic Number): {(differences > 0).sum()}")

def print_summary_statistics_comparison(algorithm_1_name, algorithm_2_name, differences):
    print(f"\n--- {algorithm_1_name} vs {algorithm_2_name} ---")
    print(f"Overall Difference (Mean): {differences.mean():.2f}")
    print(f"{algorithm_1_name} Won (Lower Chromatic Number): {(differences < 0).sum()}")
    print(f"Tied (Equal Chromatic Number): {(differences == 0).sum()}")
    print(f"{algorithm_1_name} Lost (Higher Chromatic Number): {(differences > 0).sum()}")

# Print statistics
print_summary_statistics("Random Greedy", df_random_greedy_full["Difference"])
print_summary_statistics("NX Random Sequential", df_nx_random_sequential_full["Difference"])
print_summary_statistics_comparison("Random Greedy", "NX Random Sequential", df_random_greedy_full["Random_vs_NX"])

# --- Plotting Chromatic Numbers ---
def plot_chromatic_numbers(edge_density):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Filter sampled data for the specific edge density
    greedy_subset = df_greedy_sampled[df_greedy_sampled["Edge %"] == edge_density]
    random_greedy_subset = df_random_greedy_sampled[df_random_greedy_sampled["Edge %"] == edge_density]
    nx_random_sequential_subset = df_nx_random_sequential_sampled[df_nx_random_sequential_sampled["Edge %"] == edge_density]

    # Plot Chromatic Numbers
    ax.plot(
        greedy_subset["Vertices"], greedy_subset["Chromatic Number"],
        label="Greedy", marker="o", linestyle="-"
    )
    ax.plot(
        random_greedy_subset["Vertices"], random_greedy_subset["Chromatic Number"],
        label="Random Greedy", marker="x", linestyle="--"
    )
    ax.plot(
        nx_random_sequential_subset["Vertices"], nx_random_sequential_subset["Chromatic Number"],
        label="NX Random Sequential", marker="x", linestyle=":"
    )

    # Customize the plot
    ax.set_title(f"Chromatic Numbers (Edge Density = {edge_density}%)")
    ax.set_xlabel("Number of Vertices")
    ax.set_ylabel("Chromatic Number")
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend()

    # Save and show the figure
    plt.tight_layout()
    plt.savefig(f"plots/chromatic_numbers_edge_{edge_density}.png")
    plt.show()

# --- Plotting Execution Times ---
def plot_execution_times(edge_density):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Filter sampled data for the specific edge density
    greedy_subset = df_greedy_sampled[df_greedy_sampled["Edge %"] == edge_density]
    random_greedy_subset = df_random_greedy_sampled[df_random_greedy_sampled["Edge %"] == edge_density]
    nx_random_sequential_subset = df_nx_random_sequential_sampled[df_nx_random_sequential_sampled["Edge %"] == edge_density]

    # Plot Execution Times
    ax.plot(
        greedy_subset["Vertices"], greedy_subset["Exec Time"],
        label="Greedy", marker="o", linestyle="-", color="red"
    )
    ax.plot(
        random_greedy_subset["Vertices"], random_greedy_subset["Exec Time"],
        label="Random Greedy", marker="x", linestyle="--", color="green"
    )
    ax.plot(
        nx_random_sequential_subset["Vertices"], nx_random_sequential_subset["Exec Time"],
        label="NX Random Sequential", marker="x", linestyle=":", color="blue"
    )

    # Customize the plot
    ax.set_title(f"Execution Times (Edge Density = {edge_density}%)")
    ax.set_xlabel("Number of Vertices")
    ax.set_ylabel("Execution Time (ms)")
    ax.grid(True, linestyle="--", alpha=0.7)
    plt.yscale("log")
    ax.legend()

    # Save and show the figure
    plt.tight_layout()
    plt.savefig(f"plots/execution_times_edge_{edge_density}.png")
    plt.show()

# --- Plotting Execution Times (Aggregated) ---
def plot_aggregated_execution_times():
    fig, ax = plt.subplots(figsize=(8, 6))

    # Combine the execution time data across all edge densities
    greedy_combined = df_greedy_sampled[['Vertices', 'Exec Time']]
    random_greedy_combined = df_random_greedy_sampled[['Vertices', 'Exec Time']]
    nx_random_sequential_combined = df_nx_random_sequential_sampled[['Vertices', 'Exec Time']]

    # Plot Execution Times (all edge densities combined)
    ax.plot(
        greedy_combined["Vertices"], greedy_combined["Exec Time"],
        label="Greedy", marker="o", linestyle="", color="red"
    )
    ax.plot(
        random_greedy_combined["Vertices"], random_greedy_combined["Exec Time"],
        label="Random Greedy", marker="x", linestyle="", color="green"
    )
    ax.plot(
        nx_random_sequential_combined["Vertices"], nx_random_sequential_combined["Exec Time"],
        label="NX Random Sequential", marker="x", linestyle="", color="blue"
    )

    # Customize the plot
    ax.set_title("Execution Times")
    ax.set_xlabel("Number of Vertices")
    ax.set_ylabel("Execution Time (ms)")
    ax.grid(True, linestyle="--", alpha=0.7)
    # plt.yscale("log")  # Log scale for better visualization
    ax.legend()

    # Save and show the figure
    plt.tight_layout()
    plt.savefig("plots/aggregated_execution_times.png")
    plt.show()

# Generate the aggregated execution time plot
plot_aggregated_execution_times()


# Generate the separate plots for each edge density
edge_densities = [12.5, 25, 50, 75]

# for edge in edge_densities:
#     plot_chromatic_numbers(edge)
#     plot_execution_times(edge)
