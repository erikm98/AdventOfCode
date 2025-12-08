import argparse
import numpy as np

def load_input(file_path: str) -> np.ndarray:
    with open(file_path, 'r') as file:
        data = file.readlines()
        manifold = []
        for line in data:
            manifold.append([i for i in line.strip()])
    return np.array(manifold, dtype=str)

def count_splits(manifold: np.ndarray) -> int:
    nsplits = 0
    for i in range(0,len(manifold), 2):
        if i == 0:
            manifold[i+1,np.argwhere(manifold=='S')[0][1]] = '|'
        else:
            splits = np.argwhere((manifold[i]=='^') & (manifold[i-1]=='|'))
            manifold[i:i+2,[[splits-1],[splits+1]]] = '|'
            straight = np.argwhere((manifold[i]!='^') & (manifold[i-1]=='|'))
            manifold[i:i+2,straight] = '|'
            nsplits += len(splits)
    return manifold, nsplits

def count_timelines(manifold_in: np.ndarray) -> int:
    manifold = np.zeros(manifold_in.shape, dtype=np.int64)
    manifold[manifold_in=='S']= 1
    manifold[manifold_in=='^']= -1
    for i in range(0,len(manifold), 2):
        if i == 0:
            manifold[i+1,np.argwhere(manifold==1)[0][1]] = 1
        else:
            straight = np.argwhere((manifold[i]!=-1) & (manifold[i-1]!=0))
            manifold[i:i+2,straight] = manifold[i-1,straight]
            splits = np.argwhere((manifold[i]==-1) & (manifold[i-1]!=0))
            for split in splits:
                for j in [-1,1]:
                    if manifold[i,split+j] != 0:
                        manifold[i:i+2,split+j] += manifold[i-1,split]
                    else:
                        manifold[i:i+2,split+j] = manifold[i-1,split]
    timelines = manifold[-1,:].sum()
    return manifold, timelines

def main():
    parser = argparse.ArgumentParser(description="Count tachyon splits in a manifold.")
    parser.add_argument('-i','--input', type=str, required=True, help='Path to the input file')
    args = parser.parse_args()

    manifold = load_input(args.input)
    manifold, nsplits = count_splits(manifold)
    time_manifold, timelines = count_timelines(manifold)
    print(f"Number of splits in the manifold: {nsplits}")
    print(f"Number of timelines in the manifold: {timelines}")
    print("Final manifold state:")
    for row in manifold:
        print("".join(row))

if __name__ == "__main__":
    main()