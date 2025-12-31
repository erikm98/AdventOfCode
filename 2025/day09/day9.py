import argparse
import numpy as np

def load_input(file_path: str) -> list[list[int]]:
    with open(file_path, 'r') as file:
        data = file.readlines()
        theater = []
        for line in data:
            theater.append([int(i) for i in line.strip().split(',')])
    return np.array(theater, dtype=np.int64)

def rectangle_sizes(theater: np.ndarray) -> int:
    return np.product(np.abs(theater - theater[:,np.newaxis,:])+1,axis=2)

def draw_border(theater: np.ndarray) -> np.ndarray:
    border = []
    for i, row in enumerate(theater):
        if (row == theater[-1]).all():
            nxrow = theater[0]
        else:
            nxrow = theater[i+1]
        if row[0] == nxrow[0]:
            border+=[[row[0], j] for j in range(min(row[1], nxrow[1]), max(row[1], nxrow[1])+1)]
        else:
            border+=[[i, row[1]] for i in range(min(row[0], nxrow[0]), max(row[0], nxrow[0])+1)]
    return np.array(border)

def tiled_only(theater: np.ndarray, sizes: np.ndarray) -> np.ndarray:
    border = draw_border(theater)
    max_tiled_size = 0
    tis = theater[:,0]
    tjs = theater[:,1]
    while max_tiled_size == 0:
        max_size = np.unravel_index(sizes.argmax(), sizes.shape)
        i1, j1 = theater[max_size[0]]
        i2, j2 = theater[max_size[1]]
        j_min, j_max = min(j1, j2), max(j1, j2)
        i_min, i_max = min(i1, i2), max(i1, i2)
        if len(tis[(tis > i_min) & (tis < i_max) & (tjs > j_min) & (tjs < j_max)]) > 0:
            sizes[max_size, max_size[::-1]] = 0
            continue
        else:
            top = np.array_equal(np.unique([j for i, j in border if i <= i_min and j_min <= j <= j_max]), np.arange(j_min, j_max+1))
            bottom = np.array_equal(np.unique([j for i, j in border if i >= i_max and j_min <= j <= j_max]), np.arange(j_min, j_max+1))
            left = np.array_equal(np.unique([i for i, j in border if j <= j_min and i_min <= i <= i_max]), np.arange(i_min, i_max+1))
            right = np.array_equal(np.unique([i for i, j in border if j >= j_max and i_min <= i <= i_max]), np.arange(i_min, i_max+1))
            if top and bottom and left and right:
                max_tiled_size = sizes[max_size]
            else:
                sizes[max_size, max_size[::-1]] = 0
                continue
    return max_tiled_size

def main():
    parser = argparse.ArgumentParser(description="Find the largest rectangle in a theater seating arrangement.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file')
    args = parser.parse_args()

    theater = load_input(args.input)
    area_sizes = rectangle_sizes(theater)
    print(f"Largest rectangle area: {np.max(area_sizes)}")
    max_area_tiled = tiled_only(theater, area_sizes)
    print(f"Largest rectangle area (tiled only): {max_area_tiled}")

if __name__ == "__main__":
    main()