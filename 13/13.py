from pathlib import Path
from dataclasses import dataclass
import numpy as np

import pdb

@dataclass
class Game:
    A: tuple[int, int]
    B: tuple[int, int]
    prize: tuple[int, int]

def parse_line(line: str) -> tuple[int, int]:
    return tuple(int(i.strip(',XY+=')) for i in line.split(' ')[-2:])

def get_input():
    game_chunks = Path('input').read_text().strip().split('\n\n')
    games = [
        Game(*map(parse_line, chunk.splitlines())) for chunk in game_chunks
    ]
    return games

def part_1():
    games = get_input()
    cost = np.array([3, 1]) # 3 tokens for A, 1 token for B
    total_cost = 0
    for game in games:
        # Linear equation to compute the moves needed to win the game
        A = np.array([game.A, game.B]).T
        inv = np.linalg.inv(A)
        Y = np.array(game.prize)
        X = inv @ Y
        
        # check if the game is winnable (i.e. solution was integer)
        Xi = np.round(X, 0).astype(int)
        if (A @ Xi != Y).any():
            # print(f'unwinnable game: {game}. {X=}')
            continue

        total_cost += (cost * Xi).sum().item()
    print(total_cost)

def part_2():
    games = get_input()
    cost = np.array([3, 1]) # 3 tokens for A, 1 token for B
    total_cost = 0
    for game in games:
        # Linear equation to compute the moves needed to win the game
        A = np.array([game.A, game.B]).T
        inv = np.linalg.inv(A)
        Y = np.array(game.prize) + 10000000000000 #part 2 says prize is shifted by 1e10 in x and y
        X = inv @ Y
        
        # check if the game is winnable (i.e. solution was integer)
        Xi = np.round(X, 0).astype(int)
        if (A @ Xi != Y).any():
            # print(f'unwinnable game: {game}. {X=}')
            continue

        total_cost += (cost * Xi).sum().item()
    print(total_cost)



if __name__ == '__main__':
    part_1()
    part_2()
