from pathlib import Path
from functools import cache

import pdb

def get_input():
    text = Path('input').read_text().strip()
    nums = list(map(int, text.split(' ')))
    return nums


def part_1():
    nums = get_input()
    for _ in range(25):
        next_gen = []
        for num in nums:
            if num == 0:
                next_gen.append(1)
            elif len(num_str:=str(num)) % 2 == 0:
                left = int(num_str[:len(num_str)//2])
                right = int(num_str[len(num_str)//2:])
                next_gen.append(left)
                next_gen.append(right)
            else:
                next_gen.append(num * 2024)
        nums = next_gen
    print(len(nums))


@cache
def next_number(num: int) -> int | tuple[int, int]:
    if num == 0:
        return 1
    elif len(num_str:=str(num)) % 2 == 0:
        left = int(num_str[:len(num_str)//2])
        right = int(num_str[len(num_str)//2:])
        return left, right
    else:
        return num * 2024

@cache
def count_children(num: int, generations: int) -> int:
    if generations == 0:
        return 1
    next_num = next_number(num)
    if isinstance(next_num, int):
        return count_children(next_num, generations - 1)
    left, right = next_num
    return count_children(left, generations - 1) + count_children(right, generations - 1)


def part_2():
    nums = get_input()
    total = sum(count_children(num, 75) for num in nums)
    print(total)



if __name__ == '__main__':
    part_1()
    part_2()
