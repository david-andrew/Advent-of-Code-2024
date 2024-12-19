from pathlib import Path
from dataclasses import dataclass
from itertools import count
import numpy as np
from matplotlib import pyplot as plt
import cv2

import pdb

@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

def make_robot(line:str) -> Robot:
    p, v = line.split(' ')
    x, y = map(int, p.strip('p=-').split(','))
    dx, dy = map(int, v.strip('v=>').split(','))
    return Robot(x, y, dx, dy)

def get_input():
    lines = Path('input').read_text().strip().splitlines()
    robots = [
        make_robot(line) for line in lines
    ]
    return robots


def part_1():
    width = 101
    height = 103
    robots = get_input()
    for _ in range(100):
        for robot in robots:
            robot.x = (robot.x + robot.dx) % width
            robot.y = (robot.y + robot.dy) % height
    
    width_midline = width // 2
    height_midline = height // 2
    upper_lefts = [robot for robot in robots if robot.y < height_midline and robot.x < width_midline]
    lower_lefts = [robot for robot in robots if robot.y > height_midline and robot.x < width_midline]
    upper_rights = [robot for robot in robots if robot.y < height_midline and robot.x > width_midline]
    lower_rights = [robot for robot in robots if robot.y > height_midline and robot.x > width_midline]
    print(len(upper_lefts) * len(lower_lefts) * len(upper_rights) * len(lower_rights))
    


def hough_score(space: np.ndarray) -> float:
    """come up with a score for how non-random the points are"""
    lines = cv2.HoughLines(space, 1, np.pi/180, 20)
    if lines is None:
        return 0
    return len(lines)

def part_2():
    width = 101
    height = 103
    Path('output').mkdir(exist_ok=True)
    robots = get_input()
    X = np.array([[robot.x, robot.y] for robot in robots])
    V = np.array([[robot.dx, robot.dy] for robot in robots])
    for i in count(1): # i is how many seconds have elapsed
        X += V
        X[:, 0] %= width
        X[:, 1] %= height
        space = np.zeros((height, width), dtype=np.uint8)
        space[X[:, 1], X[:, 0]] = 255
        score = hough_score(space)
        if score > 3:
            print(f'{score=}')
            # save to a file
            plt.imsave(f'output/{i}.png', space, cmap='gray')




if __name__ == '__main__':
    part_1()
    part_2()
