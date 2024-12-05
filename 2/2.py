from pathlib import Path

import numpy as np

def get_data():
    lines = Path('input').read_text().strip().splitlines()
    lines = [
        np.array([int(n) for n in l.split()])
        for l in lines
    ]
    return lines


def is_safe(report: list[int]):
    diff = [r - l for l, r in zip(report, report[1:])]
    monotonic = all(d >= 0 for d in diff) or all(d <= 0 for d in diff)
    min_diff = abs(min(diff))
    max_diff = abs(max(diff))
    min_diff, max_diff = min(min_diff, max_diff), max(min_diff, max_diff)
    return monotonic and min_diff >= 1 and max_diff <= 3

def part_1():
    data = get_data()
    num_safe = 0
    for report in data:
        if is_safe(report):
            num_safe += 1
    print(num_safe)


def is_safe_dampened(report: np.ndarray) -> bool:
    diff = np.diff(report)
    # flip the sign so we only have to deal with positive numbers
    if np.sign(diff).mean() < 0:
        report *= -1
        diff = np.diff(report)

    num_increasing = np.sum(diff > 0)
    num_decreasing = np.sum(diff < 0)
    if num_increasing > 1 and num_decreasing > 1:
        return False
    
    idxs = np.where(diff > 3)[0]
    if len(idxs) > 1:
        return False
    if len(idxs) == 1:
        idx = idxs[0]
        if is_safe([*report[:idx], *report[idx + 1:]]):
            return True
        if is_safe([*report[:idx+1], *report[idx+2:]]):
            return True
    
    idxs = np.where(diff < 1)[0]
    if len(idxs) > 1:
        return False
    if len(idxs) == 1:
        idx = idxs[0]
        if is_safe([*report[:idx], *report[idx + 1:]]):
            return True
        if is_safe([*report[:idx+1], *report[idx+2:]]):
            return True
    
    return False



def part_2():
    data = get_data()
    num_safe = 0
    for report in data:
        if is_safe(report) or is_safe_dampened(report):
            num_safe += 1
        # else:
        #     unsafe_idx = which_unsafe(report)
        #     if is_safe([*report[:unsafe_idx], *report[unsafe_idx + 1:]]):
        #         print(report, unsafe_idx)
        #         num_safe += 1
            # if is_safe([*report[:unsafe_idx-1], *report[unsafe_idx:]]):
            #     num_safe += 1
    print(num_safe)

if __name__ == '__main__':
    part_1()
    part_2()