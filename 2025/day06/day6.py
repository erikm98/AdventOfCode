import argparse
import numpy as np

def load_input(file_path: str) -> np.ndarray:
    data = np.genfromtxt(file_path, dtype=str)
    operations = data[-1]
    problems = data[:-1].astype(np.int64)
    return operations, np.transpose(problems)

def cephalopod_load_input(file_path: str) -> np.ndarray:
    with open(file_path, 'r') as file:
        data = file.readlines()
        operations = np.array(data[-1].strip().split(' '))
        operations = operations[np.where(operations != '')]
        problems = []
        for line in data[:-1]:
            problems.append([i for i in line if i != "\n"])
        problems = np.rot90(np.array(problems))
        problems = np.array([''.join(row) for row in problems])
        c_problem = []
        c_problems = []
        for problem in problems:
            if problem == '    ':
                c_problems.append(np.array(c_problem, dtype=np.int64))
                c_problem = []
            else:
                c_problem.append(problem)
        c_problems.append(np.array(c_problem, dtype=np.int64))
    return np.flip(operations), c_problems

def calculate_problems(operations: np.ndarray, problems: np.ndarray) -> int:
    total = 0
    for i, problem in enumerate(problems):
        if operations[i] == '+':
            total += np.sum(problem)
        else:
            total += np.prod(problem)
    return total

def main():
    parser = argparse.ArgumentParser(description="Calculate problems based on operations.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file')
    args = parser.parse_args()

    operations, problems = load_input(args.input)
    total = calculate_problems(operations, problems)
    operations, problems = cephalopod_load_input(args.input)
    total_cephalopod = calculate_problems(operations, problems)

    print(f"Total calculated value: {total}")
    print(f"Total calculated value using cephalopod math: {total_cephalopod}")

if __name__ == "__main__":
    main()