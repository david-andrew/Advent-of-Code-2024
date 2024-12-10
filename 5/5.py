from pathlib import Path
from collections import defaultdict, deque

import pdb

Rule = tuple[int, int]
Update = list[int]
RuleDict = dict[int, set[int]]


#If bug, check if any rules are duplicated. might affect the topological sort

def get_data() -> tuple[list[Rule], list[Update]]:
    text = Path('input').read_text()
    rules, updates = text.split('\n\n')
    rules = [[int(i)for i in line.split('|')] for line in rules.strip().split('\n')]
    updates = [[int(i) for i in line.split(',')] for line in updates.strip().split('\n')]
    return rules, updates


def part_1():
    rules, updates = get_data()
    followers_map: RuleDict = defaultdict(set)
    preceders_map: RuleDict = defaultdict(set)
    for rule in rules:
        followers_map[rule[0]].add(rule[1])
        preceders_map[rule[1]].add(rule[0])
    
    total = 0
    for update in updates:
        if update_is_valid(update, followers_map, preceders_map):
            total += update[len(update) // 2] # they want the sum of the middle elements of the valid updates

    print(total)



def update_is_valid(update: Update, followers_map: RuleDict, preceders_map: RuleDict) -> bool:
    for i, num in enumerate(update):
        befores = update[:i]
        afters = update[i+1:]
        allowed_befores = preceders_map[num]
        allowed_afters = followers_map[num]
        if len(allowed_afters.intersection(befores)) != 0 or len(allowed_befores.intersection(afters)) != 0:
            return False
        
    return True


def part_2():
    rules, updates = get_data()
    followers_map: RuleDict = defaultdict(set)
    preceders_map: RuleDict = defaultdict(set)
    for rule in rules:
        followers_map[rule[0]].add(rule[1])
        preceders_map[rule[1]].add(rule[0])

    
    total = 0
    for update in updates:
        if not update_is_valid(update, followers_map, preceders_map):
            update = fix_update(update, rules)
            total += update[len(update) // 2] # they want the sum of the middle elements of the valid updates

    print(total)    


def topological_sort(edges: list[Rule]) -> list[int]:    
    # compute the in-degree of each node
    parents, children = zip(*edges)
    nodes = set(parents + children)
    in_degree: dict[str, int] = defaultdict(int)
    for _, target in edges:
        in_degree[target] += 1

    # Create a queue and enqueue all nodes with in-degree 0
    queue = deque([node for node in nodes if in_degree[node] == 0])

    result: list[int] = []
    seen = set() # keep track of nodes that have been visited

    # Perform topological sort
    while queue:
        current = queue.popleft()
        assert current not in seen, "Graph is not a DAG"
        seen.add(current)
        result.append(current)

        for src, tgt in edges:
            if src == current:
                in_degree[tgt] -= 1
                if in_degree[tgt] == 0:
                    queue.append(tgt)

    return result
 


def fix_update(update: Update, rules: list[Rule]) -> Update:
    # filter rules for only those relevant to the update
    rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
    canonical_order = topological_sort(rules)
    if len(canonical_order) == len(update):
        return canonical_order

    # otherwise sort the update based on the canonical order
    pdb.set_trace()
    update_set = set(update)
    fixed_update = [i for i in canonical_order if i in update_set]
    return fixed_update



if __name__ == '__main__':
    part_1()
    part_2()