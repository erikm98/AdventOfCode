import argparse
import numpy as np
import pulp as plp

def load_input(file_path: str) -> np.ndarray:
    with open(file_path, 'r') as f:
        data = f.readlines()
        lights = []
        all_switches = []
        joltages = []
        for line in data:
            circuit = line.strip().split(' ')
            light = []
            for i in circuit[0]:
                if i=='#':
                    light.append(True)
                elif i == '.':
                    light.append(False)
            lights.append(np.array(light, dtype=np.bool_))

            buttons = []
            for i in circuit[1:len(circuit)-1]:
                buttons.append([int(j) for j in i if j.isdigit()])
            switches = np.array([np.zeros(len(light), dtype=np.bool_)]*len(buttons))
            for i, button in enumerate(buttons):
                switches[i][button] = True
            all_switches.append(switches)
            
            jolts = circuit[-1].split(',')
            joltage = []
            for jolt in jolts:
                if '{' in jolt or '}' in jolt:
                    joltage.append(int(jolt.replace('{','').replace('}','')))
                else:
                    joltage.append(int(jolt))
            joltages.append(np.array(joltage, dtype=int))
    return lights, all_switches, joltages

def fewest_presses_lights(lights: list[np.ndarray], switches: list[np.ndarray]) -> int:
    presses = 0
    for i, light in enumerate(lights):    
        seen = [list(light.copy())]
        done = list(np.zeros(len(light), dtype=np.bool_))
        switch = switches[i]
        outcomes = np.logical_xor(light, switch)
        for outcome in outcomes:
            if list(outcome) not in seen:
                seen.append(list(outcome))
        n = 1
        while done not in seen:
            results = np.logical_xor(outcomes, switch[:,np.newaxis])
            shape = np.shape(results)
            results = results.reshape(shape[0]*shape[1], shape[2])
            outcomes = []
            for result in results:
                if list(result) not in seen:
                    seen.append(list(result))
                    outcomes.append(result)
            outcomes = np.array(outcomes)
            n += 1
        presses += n
    return presses

def fewest_presses_joltages(joltages: list[np.ndarray], switches: list[np.ndarray]) -> int:
    presses = 0
    solver = plp.PULP_CBC_CMD(msg=0)
    for i, joltage in enumerate(joltages):
        minpress = plp.LpProblem("Joltage_Adjustment", plp.LpMinimize)    
        switch = switches[i]
        switch_vars = plp.LpVariable.dicts(f'lswitch', range(len(switch)), cat='Integer', lowBound=0)
        minpress += plp.lpSum(switch_vars[i] for i in range(len(switch)))
        for idx, jolt in enumerate(joltage):
            minpress += (plp.lpSum(switch[j][idx] * switch_vars[j] for j in range(len(switch))) == jolt)
        minpress.solve(solver)
        presses += plp.value(minpress.objective)
    return int(presses)

def main():
    parser = argparse.ArgumentParser(description="Switch on the lights with fewest button presses.")
    parser.add_argument('-i', '--input_file', type=str, help='Path to the input file')
    args = parser.parse_args()

    lights, switches, joltages = load_input(args.input_file)
    result = fewest_presses_lights(lights, switches)
    print(f"Fewest total button presses: {result}")
    result = fewest_presses_joltages(joltages, switches)
    print(f"Fewest total button presses for joltages: {result}")

if __name__ == "__main__":
    main()