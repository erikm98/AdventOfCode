import argparse
import numpy as np

def read_file(file_path:str):
    turns = []
    with open(file_path, 'r') as file:
        data = file.readlines()
        for line in data:
            r = line.strip()
            if 'L' in r:
                turns.append(-int(r[1:]))
            elif 'R' in r:
                turns.append(int(r[1:]))
    return turns

def crack_password_part1(turns:list, start:int=50):
    idx = start
    password = 0
    for turn in turns:
        idx += turn%100
        if idx > 99:
            idx = idx - 100
        elif idx < 0:
            idx = 100 + idx
        if idx == 0:
            password += 1
    return password

def crack_password_part2(turns:list, start:int=50):
    idx = start
    password = 0
    for turn in turns:
        if idx == 0:
            update = False
        else:
            update = True
        rotations = abs(turn)//100
        if turn%100 == 0 and idx == 0:
            rotations -= 1
        password += rotations
        idx += np.sign(turn) * (abs(turn)%100)
        if idx > 100:
            idx = idx - 100
            if update:
                password += 1
        elif idx < 0:
            idx = 100 + idx
            if update:
                password += 1
        elif idx == 0 or idx == 100:
            idx = 0
            password += 1
    return password

def main():
    parser = argparse.ArgumentParser(description="Crack the password.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file containing turns.')
    parser.add_argument('-s','--start', type=int, default=50, help='Starting position for cracking the password.')
    parser.add_argument('-p','--part', type=int, choices=[1, 2], default=1, help='Part of the challenge to solve (1 or 2).')
    args = parser.parse_args()

    turns = read_file(args.input)
    if args.part == 1:
        password = crack_password_part1(start=args.start, turns=turns)
    else:
        password = crack_password_part2(start=args.start, turns=turns)
    print(f"The cracked password is: {password}")

if __name__ == "__main__":
    main()