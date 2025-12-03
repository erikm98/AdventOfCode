import argparse
import numpy as np

def load_input(file_path: str) -> np.ndarray:
    with open(file_path, 'r') as file:
        banks = []
        for line in file.readlines():
            banks.append([int(i) for i in line.strip()])
    return np.array(banks, dtype=np.int64)

def large_jolts(banks: np.ndarray, nturns: int) -> int:
    total_jolts = 0
    bank_size = len(banks[0])
    for bank in banks:
        n=nturns-1
        max_place=-1
        while n >= 0:
            window = bank[max_place+1:bank_size-n]
            max_jolt = max(window)
            max_place += np.argwhere(window == max_jolt)[0][0]+1
            total_jolts += max_jolt * (10 ** (n))
            n -= 1
    return total_jolts

def main():
    parser = argparse.ArgumentParser(description="Calculate maximum jolts from banks data.")
    parser.add_argument('-i', '--input_file', type=str, help='Path to the input file containing banks data.')
    args = parser.parse_args()

    banks = load_input(args.input_file)
    result2 = large_jolts(banks,nturns=2)
    result12 = large_jolts(banks,nturns=12)
    print(f"Total maximum jolts with 2 batteries: {result2}")
    print(f"Total maximum jolts with 12 batteries: {result12}")

if __name__ == "__main__":
    main()