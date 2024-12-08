from pathlib import Path

import numpy as np


def get_data():
    s = Path("input").read_text()
    lines = s.strip().splitlines()
    arr = [[c for c in line] for line in lines]
    return arr

def part_1():
    data = get_data()
    target = 'XMAS'
    total = 0
    for i, row in enumerate(data):
        for j, _ in enumerate(row):
            total += count_at_pos(data, i, j, target)
    print(total)


def count_at_pos(data: list[list[str]], i: int, j: int, target: str) -> int:
    dydx = [
        (0, 1), # right
        (1, 1), # down right
        (1, 0), # down
        (1, -1), # down left
        (0, -1), # left
        (-1, -1), # up left
        (-1, 0), # up
        (-1, 1), # up right
    ]
    count = 0
    for dy, dx in dydx:
        y, x = i, j
        for target_c in target:
            if x < 0 or x >= len(data[0]) or y < 0 or y >= len(data):
                break
            if data[x][y] != target_c:
                break
            x += dx
            y += dy
        else:
            # print(f"Found {target} at ({i},{j}) for ({dx}, {dy})")
            count += 1
    return count


# found: set[str] = set()
def part_2():
    data = get_data()
    data = np.array(data)
    data = np.pad(data, 1, constant_values='.')
    count = 0
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c != 'A':
                continue
            d1 = {data[i-1, j-1], data[i+1, j+1]}
            d2 = {data[i-1, j+1], data[i+1, j-1]}
            if d1 == d2 and d1 == {'M', 'S'}:
                count += 1
            # if xmas_at_pos(data, i, j):
                # count += 1
    print(count)

# def xmas_at_pos(data: list[list[str]], i: int, j: int) -> bool:
#     try:
#         if not data[i][j] == 'A':
#             return False
#         if not {data[i-1][j-1], data[i+1][j+1]} == {'M', 'S'}:
#             return False
#         if not {data[i-1][j+1], data[i+1][j-1]} == {'M', 'S'}:
#             return False
#         # debug print the 3x3 square
#         # print(f'{data[i-1][j-1]}.{data[i-1][j+1]}')
#         # print(f'.{data[i][j]}.')
#         # print(f'{data[i+1][j-1]}.{data[i+1][j+1]}')
#         # print()
#         # s = f'{data[i-1][j-1]}.{data[i-1][j+1]}\n.{data[i][j]}.\n{data[i+1][j-1]}.{data[i+1][j+1]}'
#         # print(s)
#         # found.add(s)
#         return True
#     except:
#         return False

if __name__ == '__main__':
    part_1()
    part_2()