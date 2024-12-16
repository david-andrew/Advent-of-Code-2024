from pathlib import Path
import pdb

def get_data():
    data = Path('input').read_text().strip()
    # data = '233313312141413140235277364' #test input
    return data

def part_1():
    data = get_data()
    id_num = 0
    i = 0
    chunks = []
    while i < len(data):
        chunks.append(chr(id_num + ord('0')) * int(data[i]))
        if i+1 < len(data):
            chunks.append(int(data[i+1]) * '.')
        i += 2
        id_num += 1
    disk = ''.join(chunks)
    disk = list(disk)


    l, r = 0, len(disk) - 1
    while True:
        while l < len(disk) and disk[l] != '.':
            l += 1
        while r >= 0 and disk[r] == '.':
            r -= 1
        if l < r:
            disk[l], disk[r] = disk[r], disk[l]
        else:
            break

    result = 0
    for i, n in enumerate(disk):
        if n == '.':
            continue
        result += (ord(n) - ord('0')) * i

    print(result)


def part_2():
    data = get_data()
    # print(data)

if __name__ == '__main__':
    part_1()
    part_2()
