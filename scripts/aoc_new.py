import os
import sys
from pathlib import Path
import requests

__here__ = Path(__file__).parent.resolve()

def main():
    try:
        day = sys.argv[1]
        day = int(day)
    except:
        print("Please provide a day number. Usage: python aoc_new.py <day>")
        sys.exit(1)

    AOC_2024_SESSION_COOKIE = os.environ.get('AOC_2024_SESSION_COOKIE')
    if not AOC_2024_SESSION_COOKIE:
        print("Please set the AOC_2024_SESSION_COOKIE environment variable")
        sys.exit(1)
    
    # create a new folder for the day
    new_day = __here__.parent / f"{day}"
    new_day.mkdir(exist_ok=False) # fail if the folder already exists

    # download the input file
    print(f"Downloading day {day} input")
    url = f"https://adventofcode.com/2024/day/{day}/input"
    r = requests.get(url, cookies={'session': AOC_2024_SESSION_COOKIE})
    r.raise_for_status()
    input_file = new_day / 'input'
    input_file.write_text(r.text)


    # create the solution file
    print("Creating solution file stub")
    solution = new_day / f'{day}.py'
    solution.write_text("""\
from pathlib import Path

import pdb

def get_input():
    text = Path('input').read_text().strip()#.splitlines()
    pdb.set_trace()
    # TODO: any input parsing here


def part_1():
    data = get_input()
    pdb.set_trace()


def part_2():
    data = get_input()
    pdb.set_trace()



if __name__ == '__main__':
    part_1()
    part_2()
""")

    print('Done!')



if __name__ == '__main__':
    main()
