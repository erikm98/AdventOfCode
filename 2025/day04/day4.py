import argparse
import numpy as np

def load_input(file_path: str) -> np.ndarray:
    with open(file_path, 'r') as file:
        rolls = []
        for line in file.readlines():
            rolls.append([i for i in line.strip()])
    return np.array(rolls, dtype=str)

def count_accessible(rolls: np.ndarray) -> int:
    nrows = rolls.shape[0]
    ncols = rolls.shape[1]
    total_accessible = 0
    for roll in np.argwhere(rolls=='@'):
        i = roll[0]
        j = roll[1]
        roll_count = np.sum(rolls[max(0,i-1):min(i+2,nrows), max(0,j-1):min(j+2,ncols)]=='@')-1
        if roll_count < 4:
            total_accessible += 1
    return total_accessible

def count_accessible_time(rolls: np.ndarray) -> int:
    nrows = rolls.shape[0]
    ncols = rolls.shape[1]
    total_accessible = 0
    start = -1
    while start!=total_accessible:
        start = total_accessible
        for roll in np.argwhere(rolls=='@'):
            i = roll[0]
            j = roll[1]
            roll_count = np.sum(rolls[max(0,i-1):min(i+2,nrows), max(0,j-1):min(j+2,ncols)]=='@')-1
            if roll_count < 4:
                rolls[i][j] = '.'
                total_accessible += 1
    return total_accessible

def main():
    parser = argparse.ArgumentParser(description="Calculate accessible rolls from rolls data.")
    parser.add_argument('-i', '--input_file', type=str, help='Path to the input file containing rolls data.')
    args = parser.parse_args()

    rolls = load_input(args.input_file)
    result = count_accessible(rolls)
    result_time = count_accessible_time(rolls)
    print(f"Total accessible rolls: {result}")
    print(f"Total accessible rolls over time: {result_time}")

if __name__ == "__main__":
    main()