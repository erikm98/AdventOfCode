import argparse

def load_input(rules_path: str, orders_path: str) -> list[str]:
    with open(rules_path, 'r') as file:
        data = file.readlines()
        rules_dict = {}
        for rule in data:
            a,b = rule.split('|')
            if int(b) in rules_dict.keys():
                rules_dict[int(b)].append(int(a))
            else:
                rules_dict[int(b)]=[int(a)]
    with open(orders_path, 'r') as file:
        data = file.readlines()
        orders = []
        for order in data:
            order_ls=[int(i) for i in order.split(',')]
            orders.append(order_ls)
    return rules_dict, orders

def check_rulebreaks(rules: list[list[int]], orders: list[int]) -> int:
    correct_order=0
    broken_orders=[]
    for order in orders:
        broken = False
        for i, n in enumerate(order):
            rules_for_n = rules.get(n, [])
            if len(set(rules_for_n) & set(order[i+1:])) != 0:
                broken_orders.append(order)
                broken = True
                break
        if not broken:
            correct_order+=order[int(len(order)/2)]
    return correct_order, broken_orders

def fix_orders(broken_orders: list[list[int]], rules: list[list[int]]) -> int:
    fixed_order = 0
    for order in broken_orders:
        temp_order = order.copy()
        rule_break = True
        while rule_break:
            rule_break = False
            for i, n in enumerate(temp_order[:int(len(order)/2+1)]):
                rules_for_n = rules.get(n, [])
                if len(set(rules_for_n) & set(temp_order[i+1:])) != 0:
                    temp_order = temp_order[:i] + temp_order[i+1:] + [n]
                    rule_break = True
                    break
        fixed_order += temp_order[int(len(temp_order)/2)]
    return fixed_order

def main():
    parser = argparse.ArgumentParser(description="Check for rule breaks in orders.")
    parser.add_argument('-r','--rules', type=str, required=True, help='Path to the rules input file')
    parser.add_argument('-o','--orders', type=str, required=True, help='Path to the orders input file')
    args = parser.parse_args()

    rules, orders = load_input(args.rules, args.orders)
    correct_order, broken_orders = check_rulebreaks(rules, orders)
    fixed_order = fix_orders(broken_orders, rules)
    print(f"Sum of correct order middle values: {correct_order}")
    print(f"Sum with fixed broken orders: {fixed_order}")

if __name__ == "__main__":
    main()