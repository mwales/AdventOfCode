#!/usr/bin/env python3

import sys


def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")

def doMath(values, operation):
    ret_val = values[0]
    for i in range(1, len(values)):
        if operation == "+":
            ret_val += values[i]
        else:
            operation *= values[i]
    return ret_val

def replace_char(orig_str, pos, new_char):
    debug(f"replace_char({orig_str},{pos},{new_char}")
    ret_str = orig_str[:pos] + new_char + orig_str[pos+1:]
    return ret_str

def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    seperator_cols = []
    x = 0
    y = 0
    while( x < len(data[0])):
        while(True):
            if data[y][x] != ' ':
                y = 0
                x += 1
                break
            
            y += 1
            if y == len(data):
                seperator_cols.append(x)
                x += 1
                y = 0
                break

    debug(f"cols = {seperator_cols}")

    oper_str = ""
    for c in range(len(data[-1])):
        if c in seperator_cols:
            oper_str += ","
        else:
            oper_str += data[-1][c]


    debug(f"oper str = {oper_str}")
    operations = [ x.strip() for x in oper_str.split(",") ]

    debug(f"Operations: {operations}")

    solution = 0
    operation_index = 0
    cur_val = None
    for x in range(len(data[0])):
        if x in seperator_cols:
            solution += cur_val
            debug(f"Finished operation, solution = {solution}\n")
            operation_index += 1
            cur_val = None
        else:
            cur_num_str = ""
            for y in range(len(data)-1):
                cur_num_str += data[y][x]

            cur_num = int(cur_num_str)
            debug(f"Number for col {x} is {cur_num}")

            if cur_val == None:
                # First column is the start val
                cur_val = cur_num
                debug(f"Setting cur_val to {cur_val}")
            else:
                if operations[operation_index] == "+":
                    cur_val += cur_num
                    debug(f"After adding, cur_val = {cur_val}")
                else:
                    cur_val *= cur_num
                    debug(f"After multiplying, cur_val = {cur_val}")

    # Dont forget final one
    solution += cur_val

    print(f"Solution: {solution}")



if __name__ == "__main__":
    main(sys.argv)
