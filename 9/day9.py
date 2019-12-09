from copy import copy
from queue import Queue
import threading
import math

memory_length = int(math.pow(10, 7))
memory = [0] * memory_length

def DEBUG(msg):
    print(msg)
    pass


class IntcodeComputer(threading.Thread):
    def __init__(self, intcode, program_offset):
        threading.Thread.__init__(self)
        self._program_offset = program_offset
        self._relative_base = 0
        self._instruction_pointer = program_offset
        self._intcode = copy(intcode)
        self._intcode_backup = copy(intcode)
        self._input_queue = Queue()
        self._output_queue = Queue()

    def set_input_queue(self, in_queue):
        self._input_queue = in_queue

    def set_output_queue(self, out_queue):
        self._output_queue = out_queue

    def set_instruction_pointer(self, value):
        self._instruction_pointer = self._program_offset + int(value)

    def get_input(self):
        result = self._input_queue.get()
        DEBUG('Getting input: ' + str(result))
        return result

    def output_to_buffer(self, val):
        DEBUG('printing to output buffer: ' + str(val))
        self._output_queue.put(val)

    def get_position_value(self, pos):
        DEBUG('getting value of position ' + str(pos))
        return self._intcode[pos]

    def set_position_value(self, pos, value):
        DEBUG('setting value of position ' + str(pos) + ' to ' + str(value))
        self._intcode[pos] = value

    def process_opcode_1(self, arg1, arg2, arg3):
        DEBUG("processing opcode 1...")
        DEBUG('Adding ' + '(' + str(arg1) + ') + (' + str(arg2) + ') and saving in (' + str(arg3) + ')')
        self.set_position_value(arg3, int(arg1) + int(arg2))

    def process_opcode_2(self, arg1, arg2, arg3):
        DEBUG("processing opcode 2...")
        DEBUG('multiplying ' + '(' + str(arg1) + ') * (' + str(arg2) + ') and saving in (' + str(arg3) + ')')
        self.set_position_value(arg3, int(arg1) * int(arg2))

    def process_opcode_3(self, arg1):
        DEBUG("processing opcode 3...")
        DEBUG('asking for input to store in (' + str(arg1) + ')')
        val = int(self.get_input())
        self.set_position_value(arg1, val)

    def process_opcode_4(self, arg1):
        DEBUG("processing opcode 4...")
        DEBUG('outputting ' + str(arg1) + ')')
        self.output_to_buffer(arg1)

    def process_opcode_5(self, param1, param2):
        """
        is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value
        from the second parameter. Otherwise, it does nothing.
        """
        DEBUG("processing opcode 5 JNZ...")
        if param1 is not 0:
            DEBUG(str(param1) + ' is not zero, jumping to ' + str(param2))
            self.set_instruction_pointer(param2)
            return 0  # ignore jump ahead
        DEBUG(str(param1) + ' is zero, moving to next instruction')
        return 3  # proper jump ahead


    def process_opcode_6(self, param1, param2):
        """
        is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
        from the second parameter. Otherwise, it does nothing.
        """
        DEBUG("processing opcode 6 JEZ...")
        if param1 is 0:
            DEBUG(str(param1) + ' is zero, setting instruction pointer to ' + str(param2))
            self.set_instruction_pointer(param2)
            return 0  # ignore jump ahead
        DEBUG(str(param1) + ' is not zero, moving to next instruction')
        return 3  # proper jump ahead


    def process_opcode_7(self, param1, param2, param3):
        """
        is less than: if the first parameter is less than the second parameter, it stores 1 in the position given
        by the third parameter. Otherwise, it stores 0.
        """
        DEBUG("processing opcode 7...")
        if param1 < param2:
            DEBUG(str(param1) + ' is less than ' + str(param2) + ' -- setting ' + str(param3) + ' to 1')
            self.set_position_value(param3, 1)
        else:
            DEBUG(str(param1) + ' is not less than ' + str(param2) + ' -- setting ' + str(param3) + ' to 0')
            self.set_position_value(param3, 0)
        return 4  # proper jump ahead


    def process_opcode_8(self, param1, param2, param3):
        """
        # is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given
        by the third parameter. Otherwise, it stores 0.
        """
        DEBUG("processing opcode 8...")
        if param1 == param2:
            DEBUG(str(param1) + ' == ' + str(param2) + ' -- setting ' + str(param3) + ' to 1')
            self.set_position_value(param3, 1)
        else:
            DEBUG(str(param1) + ' != ' + str(param2) + ' -- setting ' + str(param3) + ' to 0')
            self.set_position_value(param3, 0)
        return 4  # proper jump ahead


    def process_opcode_9(self, param1):
        """
        # is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given
        by the third parameter. Otherwise, it stores 0.
        """
        DEBUG("processing opcode 9..." )
        DEBUG("increasing relative base of " + str(self._relative_base) + " by " + str(int(param1)))
        self._relative_base += int(param1)
        return 2  # proper jump ahead

    def get_param_modes(self, opcode):
        DEBUG('getting param modes')
        strcode = str(opcode)
        modes = strcode[:-2]
        mode_list = []
        while len(modes):
            mode_list.append(int(modes[-1]))
            modes = modes[:-1]
        DEBUG('param modes: ' + str(mode_list))
        while len(mode_list) < 3:
            mode_list.append(0)
        return mode_list


    def get_param_value_location(self, param, param_mode):
        if param_mode == 2:  # relative mode
            return self._relative_base + int(param)
        DEBUG("indirect param: " + str(param))
        return param  # indirect mode

    def get_param_value(self, param, param_mode):
        if param_mode == 1:  # immediate mode
            DEBUG("immediate param: " + str(param))
            return param
        if param_mode == 2:  # relative mode
            DEBUG("relative param, getting value...")
            DEBUG("param: " + str(param))
            DEBUG("relative base: " + str(self._relative_base))
            param_location = self._relative_base + int(param)
            DEBUG("param_location: " + str(param_location))
            param_value = self.get_position_value(param_location)
            DEBUG("param_value: " + str(param_value))
            return param_value
        DEBUG("indirect param: " + str(param))
        return self.get_position_value(param)  # indirect mode


    def process_next_instruction(self):
        DEBUG("=== EIP: " + str(self._instruction_pointer) + " ===")
        raw_opcode = self._intcode[self._instruction_pointer]
        strcode = str(raw_opcode)
        DEBUG('raw opcode:' + strcode)

        if len(strcode) > 2:
            param_modes = self.get_param_modes(raw_opcode)
            opcode = int(strcode[-2:])
        else:
            param_modes = [0, 0, 0]
            opcode = int(strcode)

        print(str(param_modes))
        # param modes default to 0
        param1_mode = param_modes[0]
        param2_mode = param_modes[1]
        param3_mode = param_modes[2]
        param1_addr = self._instruction_pointer + 1
        param2_addr = self._instruction_pointer + 2
        param3_addr = self._instruction_pointer + 3

        if opcode == 1:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self.get_param_value_location(self._intcode[param3_addr], param3_mode)
            print('opcode 1:' + str(param1) + ' ' + str(param2) + ' ' + str(param3))
            self.process_opcode_1(param1, param2, param3)
            jump_ahead = 4
        elif opcode == 2:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self.get_param_value_location(self._intcode[param3_addr], param3_mode)
            print('opcode 2:' + str(param1) + ' ' + str(param2) + ' ' + str(param3))
            self.process_opcode_2(param1, param2, param3)
            jump_ahead = 4
        elif opcode == 3:
            param1 = self.get_param_value_location(self._intcode[param1_addr], param1_mode)
            print('opcode 3:' + str(param1))
            self.process_opcode_3(param1)
            jump_ahead = 2
        elif opcode == 4:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            print('opcode 4:' + str(param1))
            self.process_opcode_4(param1)
            jump_ahead = 2
        elif opcode == 5:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            print('opcode 5:' + str(param1) + ' ' + str(param2))
            jump_ahead = self.process_opcode_5(param1, param2)
        elif opcode == 6:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            print('opcode 6:' + str(param1) + ' ' + str(param2))
            jump_ahead = self.process_opcode_6(param1, param2)
        elif opcode == 7:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self.get_param_value_location(self._intcode[param3_addr], param3_mode)
            print('opcode 7:' + str(param1) + ' ' + str(param2) + ' ' + str(param3))
            jump_ahead = self.process_opcode_7(param1, param2, param3)
        elif opcode == 8:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self.get_param_value_location(self._intcode[param3_addr], param3_mode)
            print('opcode 8:' + str(param1) + ' ' + str(param2) + ' ' + str(param3))
            jump_ahead = self.process_opcode_8(param1, param2, param3)
        elif opcode == 9:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            print('opcode 9:' + str(param1))
            jump_ahead = self.process_opcode_9(param1)
        elif opcode == 99:
            return -1
        else:
            DEBUG("Unrecognized opcode " + str(opcode))
            return -1
        return jump_ahead

    def run(self):
        jump_ahead = 0
        while jump_ahead > -1:
            jump_ahead = self.process_next_instruction()
            DEBUG('jumping ' + str(jump_ahead))
            self._instruction_pointer += jump_ahead

            if self._instruction_pointer < 0:
                print("NEGATIVE EIP")


# takes no input and produces a copy of itself as output.
#outside_intcode = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

# # should output a 16-digit number.
#outside_intcode = [1102,34915192,34915192,7,4,7,99,0]
#
# # should output the large number in the middle.
#outside_intcode = [104,1125899906842624,99]

#outside_intcode = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,38,1003,1102,24,1,1008,1102,1,29,1009,1102,873,1,1026,1102,1,32,1015,1102,1,1,1021,1101,0,852,1023,1102,1,21,1006,1101,35,0,1018,1102,1,22,1019,1102,839,1,1028,1102,1,834,1029,1101,0,36,1012,1101,0,31,1011,1102,23,1,1000,1101,405,0,1024,1101,33,0,1013,1101,870,0,1027,1101,0,26,1005,1101,30,0,1004,1102,1,39,1007,1101,0,28,1017,1101,34,0,1001,1102,37,1,1014,1101,20,0,1002,1102,1,0,1020,1101,0,859,1022,1102,1,27,1016,1101,400,0,1025,1102,1,25,1010,109,-6,1207,10,29,63,1005,63,201,1001,64,1,64,1105,1,203,4,187,1002,64,2,64,109,3,2107,25,8,63,1005,63,221,4,209,1106,0,225,1001,64,1,64,1002,64,2,64,109,-4,2101,0,9,63,1008,63,18,63,1005,63,245,1106,0,251,4,231,1001,64,1,64,1002,64,2,64,109,3,2108,38,7,63,1005,63,273,4,257,1001,64,1,64,1106,0,273,1002,64,2,64,109,22,21102,40,1,0,1008,1018,40,63,1005,63,299,4,279,1001,64,1,64,1106,0,299,1002,64,2,64,109,-16,21108,41,41,10,1005,1012,321,4,305,1001,64,1,64,1105,1,321,1002,64,2,64,109,6,2102,1,-2,63,1008,63,22,63,1005,63,341,1105,1,347,4,327,1001,64,1,64,1002,64,2,64,109,21,1206,-8,359,1106,0,365,4,353,1001,64,1,64,1002,64,2,64,109,-7,21101,42,0,-6,1008,1016,44,63,1005,63,389,1001,64,1,64,1105,1,391,4,371,1002,64,2,64,109,2,2105,1,0,4,397,1106,0,409,1001,64,1,64,1002,64,2,64,109,-3,1205,0,427,4,415,1001,64,1,64,1105,1,427,1002,64,2,64,109,-13,2102,1,-1,63,1008,63,39,63,1005,63,449,4,433,1106,0,453,1001,64,1,64,1002,64,2,64,109,-10,1202,4,1,63,1008,63,20,63,1005,63,479,4,459,1001,64,1,64,1106,0,479,1002,64,2,64,109,7,2108,37,-2,63,1005,63,495,1105,1,501,4,485,1001,64,1,64,1002,64,2,64,109,4,21101,43,0,1,1008,1010,43,63,1005,63,523,4,507,1106,0,527,1001,64,1,64,1002,64,2,64,109,-4,1208,-5,23,63,1005,63,549,4,533,1001,64,1,64,1106,0,549,1002,64,2,64,109,-4,1208,7,27,63,1005,63,565,1106,0,571,4,555,1001,64,1,64,1002,64,2,64,109,15,1205,4,587,1001,64,1,64,1106,0,589,4,577,1002,64,2,64,109,-7,1202,-7,1,63,1008,63,18,63,1005,63,613,1001,64,1,64,1106,0,615,4,595,1002,64,2,64,109,5,21107,44,43,1,1005,1015,635,1001,64,1,64,1105,1,637,4,621,1002,64,2,64,109,-2,21102,45,1,6,1008,1018,44,63,1005,63,661,1001,64,1,64,1105,1,663,4,643,1002,64,2,64,109,-18,1207,6,24,63,1005,63,685,4,669,1001,64,1,64,1105,1,685,1002,64,2,64,109,4,2101,0,8,63,1008,63,21,63,1005,63,707,4,691,1105,1,711,1001,64,1,64,1002,64,2,64,109,17,1206,5,725,4,717,1105,1,729,1001,64,1,64,1002,64,2,64,109,9,21107,46,47,-9,1005,1015,751,4,735,1001,64,1,64,1106,0,751,1002,64,2,64,109,-9,1201,-6,0,63,1008,63,26,63,1005,63,775,1001,64,1,64,1106,0,777,4,757,1002,64,2,64,109,-15,1201,0,0,63,1008,63,23,63,1005,63,803,4,783,1001,64,1,64,1105,1,803,1002,64,2,64,109,-1,2107,30,10,63,1005,63,819,1106,0,825,4,809,1001,64,1,64,1002,64,2,64,109,24,2106,0,5,4,831,1105,1,843,1001,64,1,64,1002,64,2,64,109,-5,2105,1,5,1001,64,1,64,1105,1,861,4,849,1002,64,2,64,109,14,2106,0,-5,1105,1,879,4,867,1001,64,1,64,1002,64,2,64,109,-17,21108,47,44,4,1005,1019,899,1001,64,1,64,1105,1,901,4,885,4,64,99,21101,0,27,1,21102,915,1,0,1106,0,922,21201,1,58969,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1105,1,922,22102,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1106,0,968,21201,-2,0,-2,109,-3,2105,1,0]
outside_intcode = [1102, 34463338, 34463338, 63, 1007, 63, 34463338, 63, 1005, 63, 53, 1102, 3, 1, 1000, 109, 988, 209, 12, 9, 1000, 209, 6, 209, 3, 203, 0, 1008, 1000, 1, 63, 1005, 63, 65, 1008, 1000, 2, 63, 1005, 63, 904, 1008, 1000, 0, 63, 1005, 63, 58, 4, 25, 104, 0, 99, 4, 0, 104, 0, 99, 4, 17, 104, 0, 99, 0, 0, 1102, 1, 38, 1003, 1102, 24, 1, 1008, 1102, 1, 29, 1009, 1102, 873, 1, 1026, 1102, 1, 32, 1015, 1102, 1, 1, 1021, 1101, 0, 852, 1023, 1102, 1, 21, 1006, 1101, 35, 0, 1018, 1102, 1, 22, 1019, 1102, 839, 1, 1028, 1102, 1, 834, 1029, 1101, 0, 36, 1012, 1101, 0, 31, 1011, 1102, 23, 1, 1000, 1101, 405, 0, 1024, 1101, 33, 0, 1013, 1101, 870, 0, 1027, 1101, 0, 26, 1005, 1101, 30, 0, 1004, 1102, 1, 39, 1007, 1101, 0, 28, 1017, 1101, 34, 0, 1001, 1102, 37, 1, 1014, 1101, 20, 0, 1002, 1102, 1, 0, 1020, 1101, 0, 859, 1022, 1102, 1, 27, 1016, 1101, 400, 0, 1025, 1102, 1, 25, 1010, 109, -6, 1207, 10, 29, 63, 1005, 63, 201, 1001, 64, 1, 64, 1105, 1, 203, 4, 187, 1002, 64, 2, 64, 109, 3, 2107, 25, 8, 63, 1005, 63, 221, 4, 209, 1106, 0, 225, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -4, 2101, 0, 9, 63, 1008, 63, 18, 63, 1005, 63, 245, 1106, 0, 251, 4, 231, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 3, 2108, 38, 7, 63, 1005, 63, 273, 4, 257, 1001, 64, 1, 64, 1106, 0, 273, 1002, 64, 2, 64, 109,22,21102,40,1,0,1008,1018,40,63,1005,63,299,4,279,1001,64,1,64,1106,0,299,1002,64,2,64,109,-16,21108,41,41,10,1005,1012,321,4,305,1001,64,1,64,1105,1,321,1002,64,2,64,109,6,2102,1,-2,63,1008,63,22,63,1005,63,341,1105,1,347,4,327,1001,64,1,64,1002,64,2,64,109,21,1206,-8,359,1106,0,365,4,353,1001,64,1,64,1002,64,2,64,109,-7,21101,42,0,-6,1008,1016,44,63,1005,63,389,1001,64,1,64,1105,1,391,4,371,1002,64,2,64,109,2,2105,1,0,4,397,1106,0,409,1001,64,1,64,1002,64,2,64,109,-3,1205,0,427,4,415,1001,64,1,64,1105,1,427,1002,64,2,64,109,-13,2102,1,-1,63,1008,63,39,63,1005,63,449,4,433,1106,0,453,1001,64,1,64,1002,64,2,64,109,-10,1202,4,1,63,1008,63,20,63,1005,63,479,4,459,1001,64,1,64,1106,0,479,1002,64,2,64,109,7,2108,37,-2,63,1005,63,495,1105,1,501,4,485,1001,64,1,64,1002,64,2,64,109,4,21101,43,0,1,1008,1010,43,63,1005,63,523,4,507,1106,0,527,1001,64,1,64,1002,64,2,64,109,-4,1208,-5,23,63,1005,63,549,4,533,1001,64,1,64,1106,0,549,1002,64,2,64,109,-4,1208,7,27,63,1005,63,565,1106,0,571,4,555,1001,64,1,64,1002,64,2,64,109,15,1205,4,587,1001,64,1,64,1106,0,589,4,577,1002,64,2,64,109,-7,1202,-7,1,63,1008,63,18,63,1005,63,613,1001,64,1,64,1106,0,615,4,595,1002,64,2,64,109,5,21107,44,43,1,1005,1015,635,1001,64,1,64,1105,1,637,4,621,1002,64,2,64,109,-2,21102,45,1,6,1008,1018,44,63,1005,63,661,1001,64,1,64,1105,1,663,4,643,1002,64,2,64,109,-18,1207,6,24,63,1005,63,685,4,669,1001,64,1,64,1105,1,685,1002,64,2,64,109,4,2101,0,8,63,1008,63,21,63,1005,63,707,4,691,1105,1,711,1001,64,1,64,1002,64,2,64,109,17,1206,5,725,4,717,1105,1,729,1001,64,1,64,1002,64,2,64,109,9,21107,46,47,-9,1005,1015,751,4,735,1001,64,1,64,1106,0,751,1002,64,2,64,109,-9,1201,-6,0,63,1008,63,26,63,1005,63,775,1001,64,1,64,1106,0,777,4,757,1002,64,2,64,109,-15,1201,0,0,63,1008,63,23,63,1005,63,803,4,783,1001,64,1,64,1105,1,803,1002,64,2,64,109,-1,2107,30,10,63,1005,63,819,1106,0,825,4,809,1001,64,1,64,1002,64,2,64,109,24,2106,0,5,4,831,1105,1,843,1001,64,1,64,1002,64,2,64,109,-5,2105,1,5,1001,64,1,64,1105,1,861,4,849,1002,64,2,64,109,14,2106,0,-5,1105,1,879,4,867,1001,64,1,64,1002,64,2,64,109,-17,21108,47,44,4,1005,1019,899,1001,64,1,64,1105,1,901,4,885,4,64,99,21101,0,27,1,21102,915,1,0,1106,0,922,21201,1,58969,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1105,1,922,22102,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1106,0,968,21201,-2,0,-2,109,-3,2105,1,0]

if __name__ == "__main__":
    DEBUG('running')
    input_queue  = Queue()
    output_queue = Queue()
    program_start = 0

    DEBUG('loading code into memory')
    for code_index in range(len(outside_intcode)):
        memory_location = int(code_index + program_start)
        code = outside_intcode[code_index]
        memory[memory_location] = code

    DEBUG('initializing program')
    computer = IntcodeComputer(memory, program_start)

    # init input queue
    input_queue.put(2)

    # attach queues
    computer.set_input_queue(input_queue)
    computer.set_output_queue(output_queue)

    DEBUG('starting program')
    computer.start()
    computer.join()

    DEBUG('printing output')
    while output_queue.empty() is False:
        output = output_queue.get()
        print(str(output))
