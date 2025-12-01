import argparse
import re

def load_input(file_path:str) -> list[str]:
    read_file = open(file_path, "r") 
    data = read_file.read() 
    read_file.close() 
    return data

def mulsum(data:str) -> int:
    muls = re.findall(r"mul\((\d+)\,(\d+)\s*\)",data)
    mulssum = 0
    for mul in muls:
         mulssum += int(mul[0]) * int(mul[1])
    return mulssum

def enabledmulsum(data:str) -> int:
    commands = re.findall(r"mul\(\d+,\d+\s*\)|do\(\)|don't\(\)",data)
    mulssum = 0
    enabled = True
    for command in commands:
        if "mul" in command and enabled:
            mul = command.split("(")[1].split(")")[0].split(",")
            mulssum += int(mul[0]) * int(mul[1])
        elif command == "do()":
            enabled = True
        elif command == "don't()":
            enabled = False
    return mulssum

def main():
    parser = argparse.ArgumentParser(description="Calculate multiplication sums from commands.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file containing commands.')
    args = parser.parse_args()
    
    data = load_input(args.input)
    part1_result = mulsum(data)
    part2_result = enabledmulsum(data)
    
    print(f"Part 1 - Sum of multiplications: {part1_result}")
    print(f"Part 2 - Sum of enabled multiplications: {part2_result}")

if __name__ == "__main__":
    main()