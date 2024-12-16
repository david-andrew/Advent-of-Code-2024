from pathlib import Path
from itertools import product
from typing import Callable
from tqdm import tqdm

import pdb

def get_data() -> tuple[list[int], list[list[int]]]:
    lines = Path('input').read_text().strip().splitlines()
    targets, operandss = zip(*map(lambda line: line.split(':'), lines))
    targets = list(map(int, targets))
    operandss = list(map(lambda line: list(map(int, line.strip().split(' '))), operandss))
    return targets, operandss


def interleave(lst1, lst2):
    return [val for pair in zip(lst1, lst2) for val in pair]

def part_1():
    funcs = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y
    }
    solution(funcs)

def solution(funcs: dict[str, Callable[[int, int], int]]):
    targets, operandss = get_data()

    total = 0
    for target, operands in tqdm(zip(targets, operandss), total=len(targets), desc='Counting'):
        num_ops = len(operands) - 1
        ops_candidates = product(funcs.keys(), repeat=num_ops)
        for ops in ops_candidates:
            queue = operands.copy()
            acc = queue.pop(0)
            for op, val in zip(ops, queue):
                acc = funcs[op](acc, val)
            if acc == target:
                total += target
                # print(f'{target}: {interleave(operands, ops)} = {acc}')
                break

    print(total)

def part_2():
    funcs = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y,
        '||': lambda x, y: int(str(x) + str(y))
    }
    solution(funcs)


if __name__ == '__main__':
    part_1()
    part_2()
