import argparse

def load_input(file_path: str) -> dict:
    server = {}
    with open(file_path, 'r') as file:
        data = file.readlines()
        for line in data:
            connection = line.strip().split(': ')
            server[connection[0]] = connection[1].split(' ')
    return server

class YouToOut:
    def __init__(self, server: dict):
        self.server = server
        self.memo = {}

    def count_paths(self, current: str) -> int:
        if current == 'out':
            return 1
        if current in self.memo:
            return self.memo[current]
        total = 0
        for neighbor in self.server[current]:
            total += self.count_paths(neighbor)
        self.memo[current] = total
        return total

    def walk(self):
        total = 0
        for start in self.server['you']:
            total += self.count_paths(start)
        return total

class SvrToOut:
    def __init__(self, server: dict):
        self.server = server
        self.memo = {}

    def count_paths(self, current: str, dac: bool, fft: bool) -> int:
        state = (current, dac, fft)
        if state in self.memo:
            return self.memo[state]
        total = 0
        for neighbor in self.server[current]:
            new_dac = dac or (neighbor == 'dac')
            new_fft = fft or (neighbor == 'fft')
            if neighbor == 'out':
                if new_dac and new_fft:
                    total += 1
            else:
                total += self.count_paths(neighbor, new_dac, new_fft)
        self.memo[state] = total
        return total

    def walk(self):
        total = 0
        for start in self.server['svr']:
            total += self.count_paths(start, False, False)
        return total

def main():
    parser = argparse.ArgumentParser(description="Count paths through a server network.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file')
    args = parser.parse_args()

    server = load_input(args.input)
    youtoout = YouToOut(server)
    npaths = youtoout.walk()
    print(f"Number of distinct paths from 'you' to 'out': {npaths}")

    svrtoout = SvrToOut(server)
    npaths_dac_fft = svrtoout.walk()
    print(f"Number of distinct paths from 'svr' to 'out' passing through 'dac' and 'fft': {npaths_dac_fft}")

if __name__ == "__main__":
    main()