from pathlib import Path
import numpy as np
from collections import defaultdict

import pdb

def get_input():
    lines = Path('input').read_text().strip().splitlines()
    data = np.array([[int(x) if x.isdigit() else -1 for x in line] for line in lines])
    return data


def part_1():
    data = get_input()
    zeros = np.array(np.where(data == 0)).T
    score = 0
    for zero in zeros:
        summits: set[tuple[int, int]] = set()
        stack = [zero]
        while len(stack) > 0:
            y, x = stack.pop()
            n = data[y, x]

            if n == 9:
                summits.add((y, x))
                continue

            # check if any neighbors are are n+1
            neighbors = [
                (y-1, x),
                (y+1, x),
                (y, x-1),
                (y, x+1),
            ]
            for ny, nx in neighbors:
                if ny < 0 or ny >= data.shape[0] or nx < 0 or nx >= data.shape[1]:
                    continue
                if data[ny, nx] == n+1:
                    stack.append((ny, nx))
        score += len(summits)
    print(score)

def part_2():
    data = get_input()
    zeros = np.array(np.where(data == 0)).T
    accum = np.zeros_like(data, dtype=int)
    summits: dict[tuple[int,int], int] = defaultdict(int) # {(y,x): subscore}
    score = 0

    for (zy, zx) in zeros:
        stack = [(zy, zx)]
        accum[zy, zx] = 1

        while len(stack) > 0:
            y, x = stack.pop()
            n = data[y, x]
            count = accum[y, x]

            if n == 9:
                if summits[(y, x)] < count:
                    summits[(y, x)] = count                    
                continue

            # check if any neighbors are are n+1
            neighbors = [
                (y-1, x),
                (y+1, x),
                (y, x-1),
                (y, x+1),
            ]
            for ny, nx in neighbors:
                if ny < 0 or ny >= data.shape[0] or nx < 0 or nx >= data.shape[1]:
                    continue

                if data[ny, nx] == n+1:
                    stack.append((ny, nx))
                    accum[ny, nx] += count
            
            accum[y, x] = 0

    # add up the number of trails accumulated at each summit
    score = sum(summits.values())
    print(score)



if __name__ == '__main__':
    part_1()
    part_2()
