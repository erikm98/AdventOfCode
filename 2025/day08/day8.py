import argparse
import numpy as np

def load_input(file_path: str) -> np.ndarray:
    junctions = np.genfromtxt(file_path, dtype=np.int64, delimiter=',')
    return junctions

def make_pairs(junctions: np.ndarray) -> np.ndarray:
    sim_matrix = np.sqrt(np.square(junctions-junctions[:, np.newaxis,:]).sum(axis=2))
    np.fill_diagonal(sim_matrix, np.inf)
    pairs = []
    for i, row in enumerate(sim_matrix):
        for j, val in enumerate(row):
            if i == j:
                break
            else:
                pairs.append((i, j, float(val)))
    pairs.sort(key=lambda x: x[2])
    return pairs

def cluster_junctions(junctions: np.ndarray, stop: int) -> list[int]:
    pairs = make_pairs(junctions)
    n = len(junctions)
    root = list(range(n))
    for i, j, d in pairs[:stop]:
        if root[i] != root[j]:
            old_root = root[j]
            new_root = root[i]
            for k in range(n):
                if root[k] == old_root:
                    root[k] = new_root
    return root

def three_largest(clusters: list[list[int]]) -> int:
    cluster_sizes = [clusters.count(i) for i in set(clusters)]
    three_largest = sorted(cluster_sizes, reverse=True)[:3]
    return np.prod(three_largest)

def connect_all(junctions: np.ndarray) -> int:
    pairs = make_pairs(junctions)
    n = len(junctions)
    root = list(range(n))
    for i, j, d in pairs:
        if root[i] != root[j]:
            old_root = root[j]
            new_root = root[i]
            for k in range(n):
                if root[k] == old_root:
                    root[k] = new_root
        if len(set(root)) == 1:
            distance = junctions[i][0] * junctions[j][0]
            break
    return distance

def main():
    parser = argparse.ArgumentParser(description="Cluster junctions based on Euclidean distance.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file')
    parser.add_argument('-s','--stop', type=int, required=True, help='Number of connections to make')
    args = parser.parse_args()

    junctions = load_input(args.input)
    clusters = cluster_junctions(junctions, args.stop)
    product_largest = three_largest(clusters)
    print(f"Product of sizes of the three largest clusters: {product_largest}")
    distance_full = connect_all(junctions)
    print(f"X coordinates of two junction boxes that complete the network: {distance_full}")

if __name__ == "__main__":
    main()