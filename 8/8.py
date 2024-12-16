from pathlib import Path
import numpy as np
from itertools import combinations

import pdb

def get_data():
    lines = Path('input').read_text().strip().splitlines()
    data = np.array([[c for c in line] for line in lines])
    return data



def part_1():
    data = get_data()
    freqs = np.unique(data)
    freqs = freqs[freqs != '.'] # remove empty cells
    output = np.zeros_like(data, dtype=bool)
    for freq in freqs:
        locs = np.array(np.where(data == freq)).T
        # loop over every pair of locs
        for loc0, loc1 in combinations(locs, 2):
            delta = loc1 - loc0
            node0 = loc0 - delta
            node1 = loc1 + delta
            # if either node is in bounds, mark it on the output
            # note the shorter inbounds check here only works because the input is square
            if np.all(node0 >= 0) and np.all(node0 < data.shape[0]):
                output[*node0] = True
            if np.all(node1 >= 0) and np.all(node1 < data.shape[0]):
                output[*node1] = True

    print(np.sum(output))


# def loc_inbounds(loc:np.ndarray, size: int):
#     return np.all(loc >= 0) and np.all(loc < size)

def part_2():
    data = get_data()
    freqs = np.unique(data)
    freqs = freqs[freqs != '.'] # remove empty cells
    output = np.zeros_like(data, dtype=bool)
    for freq in freqs:
        locs = np.array(np.where(data == freq)).T
        # loop over every pair of locs
        for loc0, loc1 in combinations(locs, 2):
            delta = loc1 - loc0
            node = loc0.copy()
            while True:
                if not (np.all(node >= 0) and np.all(node < data.shape[0])):
                    break
                output[*node] = True
                node -= delta
            node = loc1.copy()
            while True:
                if not (np.all(node >= 0) and np.all(node < data.shape[0])):
                    break
                output[*node] = True
                node += delta

    # for row in data:
    #     print(''.join(row))
    # print()
    # for row in output:
    #     print(''.join(['#' if x else '.' for x in row]))
    # print()

    print(np.sum(output))



if __name__ == '__main__':
    part_1()
    part_2()
