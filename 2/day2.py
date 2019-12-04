from copy import copy
intcode = [
        1,12,2,3,
        1,1,2,3,
        1,3,4,3,
        1,5,0,3,
        2,9,1,19,
        1,19,5,23,
        1,9,23,27,
        2,27,6,31,
        1,5,31,35,
        2,9,35,39,
        2,6,39,43,
        2,43,13,47,
        2,13,47,51,
        1,10,51,55,
        1,9,55,59,
        1,6,59,63,
        2,63,9,67,
        1,67,6,71,
        1,71,13,75,
        1,6,75,79,
        1,9,79,83,
        2,9,83,87,
        1,87,6,91,
        1,91,13,95,
        2,6,95,99,
        1,10,99,103,
        2,103,9,107,
        1,6,107,111,
        1,10,111,115,
        2,6,115,119,
        1,5,119,123,
        1,123,13,127,
        1,127,5,131,
        1,6,131,135,
        2,135,13,139,
        1,139,2,143,
        1,143,10,0,
        99,2,0,14,
        0]

def get_position_value(pos):
    return intcode[pos]

def set_position_value(pos, value):
    intcode[pos] = value

def process_opcode_1(arg1,arg2,arg3):
    print("processing opcode 1...")
    operand1 = get_position_value(arg1)
    operand2 = get_position_value(arg2)
    set_position_value(arg3, operand1 + operand2)

def process_opcode_2(arg1,arg2,arg3):
    print("processing opcode 2...")
    operand1 = get_position_value(arg1)
    operand2 = get_position_value(arg2)
    set_position_value(arg3, operand1 * operand2)

def process_opcode(opcode, arg1, arg2, arg3):
    if opcode == 1: process_opcode_1(arg1, arg2, arg3)
    if opcode == 2: process_opcode_2(arg1, arg2, arg3)
    if opcode == 99: return get_position_value(0)
    else:
        print("Unrecognized opcode " + str(opcode))
    return -1

if __name__ == "__main__":
    backup_intcode = copy(intcode)
    output = 0
    target_output = 19690720
    
    for noun in range(0,100):
        for verb in range(0,100):
            intcode = copy(backup_intcode)
            intcode[1] = noun
            intcode[2] = verb
            for i in range(0,len(intcode),4):
                opcode = intcode[i]
                arg1 = intcode[i + 1]
                arg2 = intcode[i + 2]
                arg3 = intcode[i + 3]
                result = process_opcode(opcode, arg1, arg2, arg3)
                if result > -1:
                    output = result
                    break
            if output == target_output:
                print(str(100 * noun + verb))
                exit()
