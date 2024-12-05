from pathlib import Path
from collections import defaultdict


def get_data():
    data = Path('input').read_text().strip().splitlines()
    data = list(zip(*(l.split() for l in data)))
    left, right = data
    left = [int(x) for x in left]
    right = [int(x) for x in right]

    return left, right


def part_1():
    left, right = get_data()
    left = sorted(left)
    right = sorted(right)
    diffs = [abs(a - b) for a, b in zip(left, right)]
    print(sum(diffs))


def part_2():
    left_counts = defaultdict(int)
    right_counts = defaultdict(int)
    left, right = get_data()
    for l in left:
        left_counts[l] += 1
    for r in right:
        right_counts[r] += 1

    sum = 0
    for k, v in left_counts.items():
        sum += k * right_counts[k] * v

    print(sum)


if __name__ == '__main__':
    part_1()
    part_2()