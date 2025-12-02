import argparse

def load_input(file_path:str) -> list[str]:
    read_file = open(file_path, "r") 
    line = read_file.read().split(',')
    read_file.close() 
    data = []
    for x,y in (pair.split('-') for pair in line):
        data+=[str(i) for i in range(int(x),int(y)+1)]
    return data

def sum_invalid(data:list[list[int]]) -> int:
    invalid_sum = 0
    for i in data:
        if i[:int(len(i)/2)] == i[int(len(i)/2):]:
            invalid_sum += int(i)
    return invalid_sum

def strict_sum_invalid(data:list[list[int]]) -> int:
    invalid_sum = 0
    for i in data:
        for j in range(1,int(len(i)/2)+1):
            if len(i)%j == 0:
                ls = [i[k:k+j] for k in range(0, len(i), j)]
                if [ls[0]]*len(ls) == ls:
                    invalid_sum += int(i)
                    break
    return invalid_sum

def main():
    parser = argparse.ArgumentParser(description="Calculate valid entries from ranges.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file containing ranges.')
    args = parser.parse_args()
    
    data = load_input(args.input)
    part1_result = sum_invalid(data)
    part2_result = strict_sum_invalid(data)

    print(f"Part 1 - Sum of invalid entries: {part1_result}")
    print(f"Part 2 - Sum of strictly invalid entries: {part2_result}")

if __name__ == "__main__":
    main()