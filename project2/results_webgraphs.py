import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure 'plots' directory exists
if not os.path.exists('plots'):
    os.makedirs('plots')

# Load CSV files
def load_and_process_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Plot Chromatic Numbers
def plot_chromatic_numbers(df_greedy, df_random_greedy, df_nx_random, repo):
    plt.figure(figsize=(10, 6))

    # Plot Greedy Algorithm's Chromatic Numbers
    plt.plot(df_greedy["Vertices"], df_greedy["Chromatic Number"], label="Greedy", marker="o", color="blue", linestyle=" ", markersize=12)

    # Plot Random Greedy Algorithm's Chromatic Numbers
    plt.plot(df_random_greedy["Vertices"], df_random_greedy["Chromatic Number"], label="Random Greedy", marker="X", color="red", linestyle=" ", markersize=12)

    # Plot NetworkX Random Sequential's Chromatic Numbers
    plt.plot(df_nx_random["Vertices"], df_nx_random["Chromatic Number"], label="NetworkX Random Sequential", marker="*", color="green", linestyle=" ", markersize=12)

    # Labels and title
    plt.title(f"Chromatic Number Comparison between Greedy, Random Greedy, and NetworkX ({repo})")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Chromatic Number")
    plt.legend()

    # Save plot to file
    plot_path = f"plots/chromatic_numbers_{repo}.png"
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

# Plot Execution Times
def plot_execution_times(df_greedy, df_random_greedy, df_nx_random, repo):
    plt.figure(figsize=(10, 6))

    # Plot Greedy Algorithm's Execution Times
    plt.plot(df_greedy["Vertices"], df_greedy["Exec Time"], label="Execution Time (Greedy)", marker="o", color="blue", linestyle="-", markersize=6)

    # Plot Random Greedy Algorithm's Execution Times
    plt.plot(df_random_greedy["Vertices"], df_random_greedy["Exec Time"], label="Execution Time (Random Greedy)", marker="x", color="red", linestyle="--", markersize=6)

    # Plot NetworkX Random Sequential's Execution Times
    plt.plot(df_nx_random["Vertices"], df_nx_random["Exec Time"], label="Execution Time (NetworkX Random Sequential)", marker="*", color="green", linestyle="-.", markersize=6)

    # Labels and title
    plt.title(f"Execution Time Comparison among Greedy, Random Greedy, and NetworkX ({repo})")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (ms)")
    plt.yscale("log")
    plt.legend()

    # Save plot to file
    plot_path = f"plots/execution_times_{repo}.png"
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

# Compute differences and count wins
def compare_algorithms(df_greedy, df_random_greedy, df_nx_random):
    merged = pd.merge(
        pd.merge(
            df_greedy, df_random_greedy,
            on=["Vertices", "Edges"],
            suffixes=("_greedy", "_random_greedy")
        ),
        df_nx_random,
        on=["Vertices", "Edges"]
    )
    merged.rename(columns={"Chromatic Number": "Chromatic Number_nx_random"}, inplace=True)

    results = {
        "Greedy Wins": (
            (merged["Chromatic Number_greedy"] < merged["Chromatic Number_random_greedy"]) &
            (merged["Chromatic Number_greedy"] < merged["Chromatic Number_nx_random"])
        ).sum(),
        "Random Greedy Wins": (
            (merged["Chromatic Number_random_greedy"] < merged["Chromatic Number_greedy"]) &
            (merged["Chromatic Number_random_greedy"] < merged["Chromatic Number_nx_random"])
        ).sum(),
        "NetworkX Wins": (
            (merged["Chromatic Number_nx_random"] < merged["Chromatic Number_greedy"]) &
            (merged["Chromatic Number_nx_random"] < merged["Chromatic Number_random_greedy"])
        ).sum(),
        "Ties": (
            (merged["Chromatic Number_greedy"] == merged["Chromatic Number_random_greedy"]) &
            (merged["Chromatic Number_greedy"] == merged["Chromatic Number_nx_random"])
        ).sum(),
    }
    
    return results

# Main function
if __name__ == "__main__":
    repos = ["facebook", "sw"]

    for repo in repos:
        # Replace with paths to your CSVs
        greedy_csv = f"results_webgraphs/{repo}/greedy_results.csv"
        random_greedy_csv = f"results_webgraphs/{repo}/random_greedy_results.csv"
        nx_random_csv = f"results_webgraphs/{repo}/nx_random_sequential_results.csv"

        df_greedy = load_and_process_csv(greedy_csv)
        df_random_greedy = load_and_process_csv(random_greedy_csv)
        df_nx_random = load_and_process_csv(nx_random_csv)

        # Compare the algorithms
        results = compare_algorithms(df_greedy, df_random_greedy, df_nx_random)
        
        # Print the results
        print(f"Comparison Results ({repo}):")
        print(f"Greedy Wins: {results['Greedy Wins']}")
        print(f"Random Greedy Wins: {results['Random Greedy Wins']}")
        print(f"NetworkX Wins: {results['NetworkX Wins']}")
        print(f"Ties: {results['Ties']}\n")

        # Plot Chromatic Numbers
        plot_chromatic_numbers(df_greedy, df_random_greedy, df_nx_random, repo)
        
        # Plot Execution Times
        plot_execution_times(df_greedy, df_random_greedy, df_nx_random, repo)
