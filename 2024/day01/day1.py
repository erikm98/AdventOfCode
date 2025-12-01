import numpy as np
import argparse

def load_input(file_path:str) -> tuple[np.ndarray, np.ndarray]:
    data = np.genfromtxt(file_path, dtype=int)
    return data[:,0], data[:,1]

def calc_distance(list1: np.ndarray, list2: np.ndarray) -> int:
    sorted_1 = np.sort(list1)
    sorted_2 = np.sort(list2)
    return np.sum(np.abs(sorted_1 - sorted_2))

def sim_score(list1: np.ndarray, list2: np.ndarray) -> int:
    unique, counts = np.unique(list2, return_counts=True)
    count_dict = dict(zip(unique, counts))
    sim_score=0
    for i in list1:
        if i in count_dict.keys():
            count = count_dict[i]
            sim_score+= count*i
        else:
            sim_score+= 0
    return sim_score

def main():
    parser = argparse.ArgumentParser(description="Calculate distance and similarity of two lists of integers.")
    parser.add_argument('-i', '--input_file', required=True, type=str, help='Path to the input file')
    args = parser.parse_args()

    list1, list2 = load_input(args.input_file)
    distance = calc_distance(list1, list2)
    print(f"The distance between the lists is: {distance}")
    score = sim_score(list1, list2)
    print(f"The similarity score between the lists is: {score}")

if __name__ == "__main__":
    main()