import numpy as np
import torch
from pathlib import Path
from enum import Enum, auto
from tqdm import tqdm

import pdb

def get_input() -> np.ndarray:
    lines = Path('input').read_text().strip().splitlines()
    data = np.array([list(line) for line in lines])
    return data

def print_data(data):
    for row in data:
        print(''.join(row))
    print()

def advance(data: np.ndarray) -> bool:
    # find the current position:
    dirs = {
        '^': (-1, 0),
        '>': (0, +1),
        'v': (+1, 0),
        '<': (0, -1),
    }
    for dir_i, dir in enumerate(dirs):
        loc = np.array(np.where(data == dir))
        if loc.shape == (2, 0):
            continue
        assert loc.shape == (2, 1), f'Unexpected shape for loc: {loc.shape}'
        y, x = loc.T[0]
        break
    else:
        raise ValueError('No current position found')

    # find the next position:
    dy, dx = dirs[dir]
    if y + dy < 0 or y + dy >= data.shape[0] or x + dx < 0 or x + dx >= data.shape[1]:
        data[y, x] = 'X'
        return False

    # if the next position is a wall, turn right
    while data[y + dy, x + dx] == '#':
        dir = [*dirs.keys()][(dir_i + 1) % len(dirs)]
        dy, dx = dirs[dir]

    assert (at_next:=data[y + dy, x + dx]) in ('.', 'X'), f'Unexpected character at next position: {at_next}'
    data[y, x] = 'X'
    data[y+dy, x+dx] = dir

    return True



def part_1():
    data = get_input()
    while advance(data): ...
        # print_data(data)
    # print_data(data)
    # count the number of 'X's in the data
    print(np.sum(data == 'X'))


class State(int, Enum):
    running = auto()
    exited = auto()
    looping = auto()

def advance_campaigns(campaigns: torch.Tensor, histories: torch.Tensor) -> tuple[dict[State, int], torch.Tensor, torch.Tensor]:
    ptrs = torch.tensor(list(map(ord, [ '^',  '>',  'v',  '<'])), dtype=torch.uint8, device='cuda')
    deltas = torch.tensor([(-1, 0), (0, +1), (+1, 0), (0, -1)], dtype=torch.int8, device='cuda')

    state_counts = {state: 0 for state in State}

    def get_pos(campaigns: torch.Tensor, ptrs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # find the current position and deltas
        _, ys, xs, dir_idxs = torch.where(campaigns[..., None] == ptrs[None, None, None])
        return ys, xs, dir_idxs

    def get_dirs(dir_idxs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        dys, dxs = deltas[dir_idxs].T
        return dys, dxs

    def filter_campaigns(campaigns: torch.Tensor, histories: torch.Tensor, dir_idxs: torch.Tensor, mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        campaigns = campaigns[~mask]
        histories = histories[:, ~mask]
        dir_idxs = dir_idxs[~mask]
        return campaigns, histories, dir_idxs

    # find the current position and deltas
    ys, xs, dir_idxs = get_pos(campaigns, ptrs)
    dys, dxs = get_dirs(dir_idxs)

    # figure out which campaigns exited and filter them out
    exited_mask = (ys + dys < 0) | (ys + dys >= campaigns.shape[1]) | (xs + dxs < 0) | (xs + dxs >= campaigns.shape[2])
    state_counts[State.exited] += torch.sum(exited_mask).item()
    campaigns, histories, dir_idxs = filter_campaigns(campaigns, histories, dir_idxs, exited_mask)
    ys, xs, _ = get_pos(campaigns, ptrs)
    dys, dxs = get_dirs(dir_idxs)

    # figure out which campaigns are at walls and make them turn right
    while True:
        at_wall_mask = campaigns[torch.arange(len(campaigns)), ys + dys, xs + dxs] == ord('#')
        if not at_wall_mask.any():
            break
        dir_idxs[at_wall_mask] = (dir_idxs[at_wall_mask] + 1) % len(ptrs)
        dys, dxs = get_dirs(dir_idxs)

    # DEBUG
    # print(f'{dir_idxs=}')

    # # check if any have exited again, now that some are facing a different direction
    # exited_mask = (ys + dys < 0) | (ys + dys >= campaigns.shape[1]) | (xs + dxs < 0) | (xs + dxs >= campaigns.shape[2])
    # state_counts[State.exited] += np.sum(exited_mask)
    # campaigns, histories, dir_idxs = filter_campaigns(campaigns, histories, dir_idxs, exited_mask)
    # ys, xs, _ = get_pos(campaigns, ptrs)
    # dys, dxs = get_dirs(dir_idxs)

    # filter out any campaigns that are looping
    looping_mask = histories[dir_idxs, torch.arange(len(campaigns)), ys, xs] == ord('X')
    state_counts[State.looping] += torch.sum(looping_mask).item()
    campaigns, histories, dir_idxs = filter_campaigns(campaigns, histories, dir_idxs, looping_mask)
    ys, xs, _ = get_pos(campaigns, ptrs)
    dys, dxs = get_dirs(dir_idxs)

    # mark the current position as visited in the histories
    histories[dir_idxs, torch.arange(len(campaigns)), ys, xs] = ord('X')

    # clear the current position in the campaigns
    campaigns[torch.arange(len(campaigns)), ys, xs] = ord('.')

    # move the campaigns forward
    campaigns[torch.arange(len(campaigns)), ys + dys, xs + dxs] = ptrs[dir_idxs]

    # count how many campaigns are still running
    state_counts[State.running] += len(campaigns)

    return state_counts, campaigns, histories

# This looked like it was going to take ~10-20 hours to run with numpy so I switched to pytorch which took 3 minutes
def part_2_brute():
    data = get_input()

    # run the original simulation to see where the guard goes
    res = data.copy()
    while advance(res): ...

    #mask out the starting point
    y0, x0 = np.array(np.where(data == '^')).T[0]
    res[y0, x0] = '.'

    # collect the list of points the guard went to
    pts = torch.tensor(np.array(np.where(res == 'X')).T, device='cuda')

    # move data to the GPU
    data = torch.tensor(np.vectorize(ord)(data), device='cuda', dtype=torch.uint8)

    # 1 campaign for each possible obstacle location
    campaigns = torch.stack([data] * len(pts), dim=0)
    campaigns[torch.arange(len(pts), device='cuda'), pts[:, 0], pts[:, 1]] = ord('#')

    # make 4 extra copies of each campaign to track if the guard walked on a square in that direction
    histories = torch.stack([campaigns] * 4, dim=0)
    histories[:, y0, x0] = ord('.')

    num_looping = 0
    progress_bar = tqdm(total=len(campaigns), desc='Finding Loops')
    while len(campaigns) > 0:
        # advance all campaigns by 1 steps
        state_counts, campaigns, histories = advance_campaigns(campaigns, histories)

        # increment the count for how many looped
        num_looping += state_counts[State.looping]

        # update the progress bar
        progress_bar.update(state_counts[State.looping] + state_counts[State.exited])
    progress_bar.close()

    print(num_looping)


# def get_out_of_bounds_mask(data: np.ndarray, pts: np.ndarray) -> np.ndarray:
#     return (pts[:, 0] < 0) | (pts[:, 0] >= data.shape[0]) | (pts[:, 1] < 0) | (pts[:, 1] >= data.shape[1])

# def get_obstacles_mask(data: np.ndarray, pts: np.ndarray) -> np.ndarray:
#     return data[pts[:, 0], pts[:, 1]] == '#'

# def part_2():
#     data = get_input()
#     dirs = {
#         '^': (-1, 0),
#         '>': (0, +1),
#         'v': (+1, 0),
#         '<': (0, -1),
#     }
#     y0, x0 = np.array(np.where(data == '^')).T[0]
#     paths = np.stack([data] * 4, axis=0)
#     paths[:, y0, x0] = '.'
#     pts = np.array(np.where(data == '#')).T
#     for i, (dir, (dy, dx)) in enumerate(dirs.items()):
#         cur = pts.copy()
#         prev_dy, prev_dx = dirs[[*dirs.keys()][(i - 1) % len(dirs)]]
#         cur[:, 0] -= prev_dy
#         cur[:, 1] -= prev_dx
#         if i == 0: #include the starting point
#             cur = np.concatenate([cur, [[y0, x0]]], axis=0)
#         oob_mask = get_out_of_bounds_mask(data, cur)
#         cur = cur[~oob_mask]
#         obstacle_mask = get_obstacles_mask(data, cur)
#         cur = cur[~obstacle_mask]
#         paths[i, cur[:, 0], cur[:, 1]] = 'X' # entry points onto the path

#         while True:
#             cur[:, 0] += dy
#             cur[:, 1] += dx
#             oob_mask = get_out_of_bounds_mask(data, cur)
#             cur = cur[~oob_mask]
#             obstacle_mask = get_obstacles_mask(data, cur)
#             prev_cur = cur[obstacle_mask]
#             prev_cur[:, 0] -= dy
#             prev_cur[:, 1] -= dx
#             paths[i, prev_cur[:, 0], prev_cur[:, 1]] = 'O'
#             cur = cur[~obstacle_mask]
#             if len(cur) == 0:
#                 break
#             paths[i, cur[:, 0], cur[:, 1]] = 'X'

#     for path in paths:
#         print_data(path)
#         print()
#     pdb.set_trace()
#     ...



if __name__ == '__main__':
    # part_1()
    # part_2()
    part_2_brute()
