from pathlib import Path
import numpy as np

from matplotlib import pyplot as plt
import pdb

def get_input():
    text = Path('input').read_text().strip().splitlines()
    data = np.array([[c for c in line] for line in text])
    return data


def part_1():
    data = get_input()
    data, regions = pad_and_flood_fill(data)
    cost = 0
    for i in range(1, regions.max() + 1):
        region = (regions == i)
        area = region.sum()
        pts = np.argwhere(region)
        neighbors = np.concatenate([
            pts + [dy, dx]
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        ])

        # # remove out of bounds. Not necessary since we padded the data
        # neighbors = neighbors[
        #     (neighbors[:, 0] >= 0) & (neighbors[:, 0] < data.shape[0]) &
        #     (neighbors[:, 1] >= 0) & (neighbors[:, 1] < data.shape[1])
        # ]

        # count up the number of neighbors that are not part of the region
        perimeter = (regions[*neighbors.T] != i).sum()
        cost += area * perimeter
    
    print(cost)


def pad_and_flood_fill(data: np.ndarray) -> np.ndarray:
    # pad the data so it's easy to count border on the outside
    data = np.pad(data, 1, constant_values='.')

    # flood fill algorithm
    fill = np.zeros_like(data, dtype=int)
    i = 1
    while (fill == 0).any():
        y0, x0 = np.argwhere(fill == 0)[0]
        letter = data[y0, x0]
        stack = [(y0, x0)]
        while len(stack) > 0:
            y, x = stack.pop()
            fill[y, x] = i
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                y1, x1 = y + dy, x + dx
                if 0 <= y1 < data.shape[0] and 0 <= x1 < data.shape[1]:
                    if data[y1, x1] == letter:
                        # sanity check
                        assert fill[y1, x1] in (0, i), f'{fill[y1, x1]} not in (0, {i}). i.e. failed to completely fill a region...'
                        if fill[y1, x1] == 0:
                            stack.append((y1, x1))
        i += 1

    # subtract 1 to make the background region be 0 so it can be ignored
    fill -= 1

    return data, fill 


def part_2():
    data = get_input()
    data, regions = pad_and_flood_fill(data)
    cost = 0
    for i in range(1, regions.max() + 1):
        total_walls = 0
        region = (regions == i)
        area = region.sum().item()

        pts = np.argwhere(region)

        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbors = pts + [dy, dx]
            is_filled_neighbor = region[*neighbors.T]
            empty_neighbor_pts = neighbors[~is_filled_neighbor]

            # convert horizontal walls to vertical walls for easier processing
            if dx == 0:
                empty_neighbor_pts = empty_neighbor_pts[:, ::-1]

            # make 2D array of walls (1 for wall 0 for none), and then per each column find transitions from 0 to 1
            walls = np.zeros_like(data, dtype=int)
            walls[*empty_neighbor_pts.T] = 1
            new_walls = ((walls[1:] - walls[:-1]) == 1).sum().item()
            total_walls += new_walls
          
        cost += total_walls * area
    
    print(cost)



if __name__ == '__main__':
    part_1()
    part_2()
