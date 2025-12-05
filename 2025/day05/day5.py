import argparse
import numpy as np

def load_input(file_path: str) -> np.ndarray:
    with open(file_path, 'r') as file:
        data = file.readlines()
        fresh = []
        food = []
        read_fresh = True
        for line in data:
            line.strip()
            if line.strip() == '':
                read_fresh = False
                continue
            if read_fresh:
                fresh.append(line.strip().split('-'))
            else:
                food.append(line.strip())
    return np.sort(np.array(fresh, dtype=np.int64), axis=0), np.array(food, dtype=np.int64)

def compact_fresh(fresh: np.ndarray) -> np.ndarray:
    to_delete = []
    for i in range(len(fresh)-1):
        if fresh[i][1]+1 >= fresh[i+1][0]:
            fresh[i+1][0] = fresh[i][0]
            to_delete.append(i)
    fresh = np.delete(fresh, to_delete, 0)
    return fresh

def check_freshness(fresh: np.ndarray, food: np.ndarray) -> int:
    fresh_count = 0
    for item in food:
        f = np.argwhere((fresh[:,0] <= item) & (fresh[:,1] >= item))
        if len(fresh[f]) > 0:
            fresh_count += 1
    return fresh_count

def count_all_fresh(fresh:np.ndarray) -> int:
    total_fresh = np.sum(fresh[:,1]-fresh[:,0]+1)
    return total_fresh

def main():
    parser = argparse.ArgumentParser(description="Check food freshness against fresh date ranges.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file')
    args = parser.parse_args()

    fresh, food = load_input(args.input)
    compacted_fresh = compact_fresh(fresh)
    fresh_count = check_freshness(compacted_fresh, food)
    total_fresh = count_all_fresh(compacted_fresh)

    print(f"Number of fresh food items: {fresh_count}")
    print(f"Total number of fresh days covered: {total_fresh}")

if __name__ == "__main__":
    main()