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
    for i in range(1, regions.max() + 1):
        region = (regions == i)
        area = region.sum()

        pts = np.argwhere(region)

        # collect all points with at least one empty neighbor
        neighbors = np.concatenate([
            pts + [dy, dx]
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        ])
        idxs = np.concatenate([np.arange(len(pts)) for _ in range(4)]).T

        is_filled_neighbor = region[*neighbors.T]
        idxs = idxs[~is_filled_neighbor]
        idxs = np.unique(idxs)

        candidate_start_points = pts[idxs]
        traced_regions = np.zeros_like(region, dtype=bool)

        # find all regions: 1 outside, and 0 or more inside the current region
        # take a candidate start point that is touching a region not yet traced
        # trace around keeping the right hand on the wall until you return to the start
        # while tracing, count the number of times the direction changes. This is the number of edges
        
        pdb.set_trace()

    pdb.set_trace()



if __name__ == '__main__':
    part_1()
    part_2()
