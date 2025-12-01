import argparse

def load_input(file_path:str) -> list[list[int]]:
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            r = line.strip()
            data.append([int(x) for x in r.split()])
    return data

    diff_ls = []
    for i, value in enumerate(report):
        diff = report[i+1]-value
        diff_ls.append(diff)
    if sum([i < 0 for i in diff_ls]) > sum([i > 0 for i in diff_ls]):
        return False
    else:
        return True

def is_valid(report:list[int]) -> bool:
    if report[0] < report[-1]:
        order = 'asc'
    elif report[0] > report[-1]:
        order = 'desc'
    else:
        return False
    for i, value in enumerate(report[:-1]):
        diff = report[i+1]-value
        if order == 'asc' and 1 <= diff <= 3:
            continue
        elif order == 'desc' and -3 <= diff <= -1:
            continue
        else:
            return False
    return True

def safe_count(reports:list[list[int]]) -> int:
    safe = 0
    for report in reports:
        if is_valid(report):
            safe += 1
    return safe

def asc_or_desc(report:list[int]) -> str:
    diff_ls = []
    for i, value in enumerate(report[:-1]):
        diff = report[i+1]-value
        diff_ls.append(diff)
    if sum([i < 0 for i in diff_ls]) > sum([i > 0 for i in diff_ls]):
        return 'desc'
    else:
        return 'asc'

def tolerant_is_valid(report:list[int]) -> bool:
    order = asc_or_desc(report)
    for i, value in enumerate(report[:-1]):
        diff = report[i+1]-value
        if order == 'asc' and 1 <= diff <= 3:
            continue
        elif order == 'desc' and -3 <= diff <= -1:
            continue
        elif i == len(report)-2:
            return True
        elif order=='asc':
            if 1 <= report[i+2]-value <= 3:
                return is_valid(report[:i+1] + report[i+2:])
            else:
                return is_valid(report[:i] + report[i+1:])
        elif order=='desc':
            if -3 <= report[i+2]-value <= -1:
                return is_valid(report[:i+1] + report[i+2:])
            else:
                return is_valid(report[:i] + report[i+1:])
    return True

def tolerant_safe_count(reports:list[list[int]]) -> int:
    safe = 0
    for report in reports:
        if tolerant_is_valid(report):
            safe += 1
    return safe

def main():
    parser = argparse.ArgumentParser(description="Count valid reports based on given criteria.")
    parser.add_argument('-i', '--input_file', required=True, type=str, help='Path to the input file')
    args = parser.parse_args()

    reports = load_input(args.input_file)
    safe_reports = safe_count(reports)
    print(f"The number of valid reports is: {safe_reports}")
    tolerant_safe_reports = tolerant_safe_count(reports)
    print(f"The number of valid reports with tolerance is: {tolerant_safe_reports}")

if __name__ == "__main__":
    main()