from copy import copy

instruction_pointer = 0

def DEBUG(msg):
#    print(msg)
    pass

# original intcode
intcode = [ 3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 40, 71, 224, 1001, 224, -111, 224, 4, 224, 1002, 223, 8, 223, 101, 7, 224, 224, 1, 224, 223, 223, 1102, 66, 6, 225, 1102, 22, 54, 225, 1, 65, 35, 224, 1001, 224, -86, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 224, 223, 223, 1102, 20, 80, 225, 101, 92, 148, 224, 101, -162, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 5, 224, 224, 1, 224, 223, 223, 1102, 63, 60, 225, 1101, 32, 48, 225, 2, 173, 95, 224, 1001, 224, -448, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 4, 224, 1, 224, 223, 223, 1001, 91, 16, 224, 101, -79, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1101, 13, 29, 225, 1101, 71, 70, 225, 1002, 39, 56, 224, 1001, 224, -1232, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 14, 59, 225, 102, 38, 143, 224, 1001, 224, -494, 224, 4, 224, 102, 8, 223, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1102, 30, 28, 224, 1001, 224, -840, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 223, 224, 223, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 329, 1001, 223, 1, 223, 8, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 359, 101, 1, 223, 223, 1007, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 374, 1001, 223, 1, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 389, 101, 1, 223, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 404, 1001, 223, 1, 223, 108, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 419, 1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 434, 1001, 223, 1, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 449, 101, 1, 223, 223, 7, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 464, 1001, 223, 1, 223, 8, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 479, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 494, 101, 1, 223, 223, 1007, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 509, 1001, 223, 1, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 524, 1001, 223, 1, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 539, 101, 1, 223, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 554, 1001, 223, 1, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 569, 101, 1, 223, 223, 8, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 584, 1001, 223, 1, 223, 7, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 599, 101, 1, 223, 223, 1008, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 614, 101, 1, 223, 223, 1008, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 629, 1001, 223, 1, 223, 1108, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 644, 101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 659, 1001, 223, 1, 223, 1107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226 ]

# compare input to 8 (position mode)
# intcode = [ 3,9,8,9,10,9,4,9,99,-1,8 ]

# less than 8 (position mode)
#intcode = [3,9,7,9,10,9,4,9,99,-1,8]

# equal to 8 (immediate mode)
#intcode = [3,3,1108,-1,8,3,4,3,99]

# less than 8 (immediate mode)
#intcode = [ 3,3,1107,-1,8,3,4,3,99 ]

# jump test (position mode)
#intcode = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]

# jump test (immediate mode)
#intcode = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

#The following example program uses an input instruction to ask for a single number. The program will then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
#intcode = [3 ,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

# template
#intcode = []

def get_position_value(pos):
    DEBUG('getting value of position ' + str(pos))
    return intcode[pos]

def set_position_value(pos, value):
    DEBUG('setting value of position ' + str(pos) + ' to ' + str(value))
    intcode[pos] = value

def process_opcode_1(arg1,arg2,arg3):
    DEBUG("processing opcode 1...")
    set_position_value(arg3, arg1 + arg2)

def process_opcode_2(arg1,arg2,arg3):
    DEBUG("processing opcode 2...")
    set_position_value(arg3, arg1 * arg2)

def process_opcode_3(arg1):
    DEBUG("processing opcode 3...")
    val = int(input())
    set_position_value(arg1, val)

def process_opcode_4(arg1):
    DEBUG("processing opcode 4...")
    print(str(arg1))

def process_opcode_5(param1, param2):
    global instruction_pointer
    DEBUG("processing opcode 5..." + str(param1) + ' ' + str(param2))
    # is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    if param1 is not 0:
        instruction_pointer = param2
        return 0 # ignore jump ahead
    return 3 # proper jump ahead

def process_opcode_6(param1, param2):
    global instruction_pointer
    DEBUG("processing opcode 6..." + str(param1) + ' ' + str(param2))
    # is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    if param1 is 0:
        instruction_pointer = param2
        return 0 # ignore jump ahead
    return 3 # proper jump ahead

def process_opcode_7(param1, param2, param3):
    DEBUG("processing opcode 7..." + str(param1) + ' ' + str(param2))
    # is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    if param1 < param2:
        set_position_value(param3,1)
    else:
        set_position_value(param3,0)
    return 4 # proper jump ahead

def process_opcode_8(param1, param2, param3):
    DEBUG("processing opcode 8..." + str(param1) + ' ' + str(param2) + ' ' + str(param3))
    # is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    if param1 == param2:
        set_position_value(param3,1)
    else:
        set_position_value(param3,0)
    return 4 # proper jump ahead

def get_param_modes(opcode):
    DEBUG('getting param modes')
    strcode = str(opcode)
    modes = strcode[:-2]
    mode_list = []
    while len(modes):
        mode_list.append(int(modes[-1]))
        modes = modes[:-1]
    DEBUG('param modes: ' + str(mode_list))
    return mode_list

def get_param_value(param, param_mode):
    if param_mode == 1: # immediate mode
        return param
    return get_position_value(param) # indirect mode

def process_next_instruction():
    DEBUG("=== EIP: " + str(instruction_pointer) + " ===")
    raw_opcode = intcode[instruction_pointer]
    strcode = str(raw_opcode)
    
    if len(strcode) > 2:
        param_modes = get_param_modes(raw_opcode)
        opcode = int(strcode[-2:])
    else:
        param_modes = [0,0,0]
        opcode = int(strcode)

    # param modes default to 0
    param1_mode =  param_modes[0] if (len(param_modes) > 0) else 0
    param2_mode =  param_modes[1] if (len(param_modes) > 1) else 0
    param3_mode =  param_modes[2] if (len(param_modes) > 2) else 0
    param1_addr = instruction_pointer + 1
    param2_addr = instruction_pointer + 2
    param3_addr = instruction_pointer + 3


    if opcode == 1: 
        param1 = get_param_value(intcode[param1_addr], param1_mode)
        param2 = get_param_value(intcode[param2_addr], param2_mode)
        param3 = intcode[param3_addr]
        process_opcode_1(param1, param2, param3)
        jump_ahead = 4
    elif opcode == 2:
        param1 = get_param_value(intcode[param1_addr], param1_mode)
        param2 = get_param_value(intcode[param2_addr], param2_mode)
        param3 = intcode[param3_addr]
        process_opcode_2(param1, param2, param3)
        jump_ahead = 4
    elif opcode == 3: 
        param1 = intcode[param1_addr]
        process_opcode_3(param1)
        jump_ahead = 2
    elif opcode == 4: 
        param1 = get_param_value(intcode[param1_addr], param1_mode)
        process_opcode_4(param1)
        jump_ahead = 2
    elif opcode == 5: 
        param1 = get_param_value(intcode[param1_addr], param1_mode)
        param2 = get_param_value(intcode[param2_addr], param2_mode)
        jump_ahead = process_opcode_5(param1,param2)
    elif opcode == 6: 
        param1 = get_param_value(intcode[param1_addr], param1_mode)
        param2 = get_param_value(intcode[param2_addr], param2_mode)
        jump_ahead = process_opcode_6(param1,param2)
    elif opcode == 7: 
        param1 = get_param_value(intcode[param1_addr], param1_mode)
        param2 = get_param_value(intcode[param2_addr], param2_mode)
        param3 = intcode[param3_addr]
        jump_ahead = process_opcode_7(param1,param2,param3)
    elif opcode == 8: 
        param1 = get_param_value(intcode[param1_addr], param1_mode)
        param2 = get_param_value(intcode[param2_addr], param2_mode)
        param3 = intcode[param3_addr]
        jump_ahead = process_opcode_8(param1,param2,param3)
    elif opcode == 99: return -1
    else:
        DEBUG("Unrecognized opcode " + str(opcode))
        return -1
    return jump_ahead

if __name__ == "__main__":
    jump_ahead = 0
    while jump_ahead > -1:
        jump_ahead = process_next_instruction()
        DEBUG('jumping ' + str(jump_ahead))
        instruction_pointer += jump_ahead

