import argparse
import numpy as np

def load_input(file_path: str) -> list[np.ndarray] | np.ndarray:
    with open(file_path, 'r') as file:
        presents = []
        trees = []
        present = []
        required = []
        for line in file.readlines():
            line = line.strip()
            if line == '':
                if present:
                    presents.append(np.array(present, dtype=np.bool_))
                    present = []
            elif ':' in line and 'x' not in line:
                if present:
                    presents.append(np.array(present, dtype=np.bool_))
                present = []
            elif line and line[0].isdigit():
                tree = line.split(': ')
                size = [int(i) for i in tree[0].split('x')]
                req = [int(j) for j in tree[1].split(' ')]
                trees.append(size)
                required.append(req)
            elif '#' in line:
                presentpart = []
                for char in line:
                    if char == '#':
                        presentpart.append(True)
                    elif char == '.':
                        presentpart.append(False)
                present.append(presentpart)
        if present:
            presents.append(np.array(present, dtype=np.bool_))
    return presents, np.array(trees), np.array(required)

def main():
    parser = argparse.ArgumentParser(description="Fit presents under the trees.")
    parser.add_argument('-i', '--input_file', type=str, help='Path to the input file containing presents and trees data.')
    args = parser.parse_args()

    presents, trees, required = load_input(args.input_file)
    present_sizes = np.array([present.sum() for present in presents])
    min_required_size = present_sizes * required
    max_required_size = 9 * required
    print(f"Number of required presents that definitely do not fit under the trees: {np.sum(np.sum(min_required_size, axis=1) > np.prod(trees, axis=1))}")
    print(f"Number of required presents that definitely fit under the trees: {np.sum(np.sum(max_required_size, axis=1) <= np.prod(trees, axis=1))}")

if __name__ == "__main__":
    main()