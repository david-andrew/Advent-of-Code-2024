from pathlib import Path
from dataclasses import dataclass
import pdb
from bdb import set_trace

def get_data():
    data = Path('input').read_text().strip()
    # data = '233313312141413140235277364' #test input
    # data = '2333133121414131402' #test input
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



@dataclass
class File:
    id: int
    size: int

@dataclass
class Free:
    size: int

def disk_str(disk: list[File|Free]):
    chunks = []
    for chunk in disk:
        if isinstance(chunk, File):
            chunks.append(chr(chunk.id + ord('0')) * chunk.size)
        else:
            chunks.append('.' * chunk.size)
    return ''.join(chunks)

def part_2():
    data = get_data()
    id_num = 0
    i = 0
    chunks: list[File|Free] = []
    while i < len(data):
        chunks.append(File(id_num, int(data[i])))
        # chunks.append(chr(id_num + ord('0')) * int(data[i]))
        if i+1 < len(data):
            chunks.append(Free(int(data[i+1])))
        i += 2
        id_num += 1


    i = len(chunks) - 1
    while i >= 0:
        # print(disk_str(chunks))
        block = chunks[i]
        if not isinstance(block, File):
            i -= 1
            continue
        for j, free in enumerate(chunks):
            if not isinstance(free, Free):
                continue
            if free.size >= block.size and j < i:
                free.size -= block.size
                block = chunks.pop(i)
                new_free = Free(block.size)
                chunks.insert(j, block)
                chunks.insert(i, new_free)
                break
        i -= 1

    disk = disk_str(chunks)
    # print(disk)
    result = 0
    for i, n in enumerate(disk):
        if n == '.':
            continue
        result += (ord(n) - ord('0')) * i

    print(result)






if __name__ == '__main__':
    part_1()
    part_2()
