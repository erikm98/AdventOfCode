import argparse
import re
import numpy as np

def load_input(file_path:str) -> np.ndarray:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            r = line.strip()
            data.append([i for i in r])
    return np.array(data, dtype=str)

def count_xmas(line:str) -> int:            
    return len(re.findall(r'XMAS', line))+len(re.findall(r'SAMX', line))

def xmas_search(data:np.ndarray) -> int:
    count = 0
    for row in range(np.shape(data)[0]):
        count += count_xmas(''.join(list(data[row,:])))
        count += count_xmas(''.join(list(np.diagonal(data, offset=row))))
        count += count_xmas(''.join(list(np.diagonal(np.rot90(data), offset=-row))))
    for col in range(np.shape(data)[1]):
        count += count_xmas(''.join(list(data[:,col])))
        if col !=0:
            count += count_xmas(''.join(list(np.diagonal(data, offset=-col))))
            count += count_xmas(''.join(list(np.diagonal(np.rot90(data), offset=col))))
    return count

def masx_search(data:np.ndarray) -> int:
    count = 0
    centres = list(zip(*np.where(data=='A')))
    rows = data.shape[0]
    cols = data.shape[1]
    for centre in centres:
        i, j = centre
        if i !=0 and i != rows-1 and j !=0 and j != cols-1:
            ul=data[i-1][j-1]
            ur=data[i-1][j+1]
            dl=data[i+1][j-1]
            dr=data[i+1][j+1]
            if ((ul=='M' and dr=='S') or (ul=='S' and dr=='M')) and ((ur=='M' and dl=='S') or (ur=='S' and dl=='M')):
                count += 1
    return count

def main():
    parser = argparse.ArgumentParser(description="Count XMAS and MASX patterns in a grid.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file containing the grid.')
    args = parser.parse_args()
    
    data = load_input(args.input)
    part1_result = xmas_search(data)
    part2_result = masx_search(data)

    print(f"Part 1 - Number of XMAS patterns: {part1_result}")
    print(f"Part 2 - Number of MASX patterns: {part2_result}")

if __name__ == "__main__":
    main()