from pathlib import Path

import pdb

def get_data() -> str:
    return Path("input").read_text()


def part_1():
    data = get_data()
    total = 0
    while (data := discard_up_to("mul", data)) is not None:
        try:
            _, data = eat_substring("mul", data)
            _, data = eat_substring("(", data)
            left, data = eat_int(data)
            _, data = eat_substring(",", data)
            right, data = eat_int(data)
            _, data = eat_substring(")", data)
            total += left * right
        except:
            continue

    print(total)

def discard_up_to(sub: str, data: str) -> str|None:
    try:
        return data[data.index(sub):]
    except ValueError:
        return None

def eat_substring(sub: str, data: str) -> tuple[str, str]|None:
    """find the location of the next"""
    l = len(sub)
    if data.startswith(sub):
        return data[:l], data[l:]
    return None
            
def eat_int(data: str) -> tuple[int, str]|None:
    i = 0
    while data[i].isdigit():
        i += 1
    if i == 0:
        return None
    
    return int(data[:i]), data[i:]

def part_2():
    data = get_data()
    total = 0
    do_next = True
    while (task := next_thing(data)) is not None:
        if task == "mul":
            try:
                data = discard_up_to("mul", data)
                _, data = eat_substring("mul", data)
                _, data = eat_substring("(", data)
                left, data = eat_int(data)
                _, data = eat_substring(",", data)
                right, data = eat_int(data)
                _, data = eat_substring(")", data)
                if do_next:
                    total += left * right
            except:
                continue
        elif task == "do":
            data = discard_up_to("do()", data)
            _, data = eat_substring("do()", data)
            do_next = True
        elif task == "dont":
            data = discard_up_to("don't()", data)
            _, data = eat_substring("don't()", data)
            do_next = False
        else:
            raise ValueError("Unknown task")
    print(total)

def next_thing(data: str) -> str|None:
    next_mul = idx_of_substring("mul", data)
    next_do = idx_of_substring("do()", data)
    next_dont = idx_of_substring("don't()", data)
    idxs = [
        ('mul', next_mul), 
        ('do', next_do), 
        ('dont', next_dont)
    ]
    idxs = [i for i in idxs if i[1] is not None]
    if not idxs:
        return None
    idxs.sort(key=lambda x: x[1])
    return idxs[0][0]
    

    

def idx_of_substring(sub: str, data: str, fail=None) -> int:
    try:
        return data.index(sub)
    except:
        return fail



if __name__ == "__main__":
    part_1()
    part_2()