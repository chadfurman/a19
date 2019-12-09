from copy import copy
from queue import Queue
import threading
import itertools


def DEBUG(msg):
    print(msg)
    pass


class IntcodeComputer(threading.Thread):
    def __init__(self, intcode, name):
        threading.Thread.__init__(self)
        self._name = name
        self._instruction_pointer = 0
        self._intcode = copy(intcode)
        self._intcode_backup = copy(intcode)
        self._input_queue = Queue()
        self._output_queue = Queue()

    def set_input_queue(self, in_queue):
        self._input_queue = in_queue

    def set_output_queue(self, out_queue):
        self._output_queue = out_queue

    def set_instruction_pointer(self, value):
        self._instruction_pointer = int(value)

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
        DEBUG("processing opcode 1..." + '(' + str(arg1) + ')' + '(' + str(arg2) + ')' + '(' + str(arg3) + ')')
        self.set_position_value(arg3, int(arg1) + int(arg2))

    def process_opcode_2(self, arg1, arg2, arg3):
        DEBUG("processing opcode 2..." + '(' + str(arg1) + ')' + '(' + str(arg2) + ')' + '(' + str(arg3) + ')')
        self.set_position_value(arg3, int(arg1) * int(arg2))

    def process_opcode_3(self, arg1):
        DEBUG("processing opcode 3..." + '(' + str(arg1) + ')')
        val = int(self.get_input())
        self.set_position_value(arg1, val)

    def process_opcode_4(self, arg1):
        DEBUG("processing opcode 4..." + '(' + str(arg1) + ')')
        self.output_to_buffer(arg1)

    def process_opcode_5(self, param1, param2):
        """
        is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value
        from the second parameter. Otherwise, it does nothing.
        """
        DEBUG("processing opcode 5..." + str(param1) + ' ' + str(param2))

        if param1 is not 0:
            self._instruction_pointer = param2
            return 0  # ignore jump ahead
        return 3  # proper jump ahead


    def process_opcode_6(self, param1, param2):
        """
        is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
        from the second parameter. Otherwise, it does nothing.
        """
        DEBUG("processing opcode 6..." + str(param1) + ' ' + str(param2))
        if param1 is 0:
            self._instruction_pointer = param2
            return 0  # ignore jump ahead
        return 3  # proper jump ahead


    def process_opcode_7(self, param1, param2, param3):
        """
        is less than: if the first parameter is less than the second parameter, it stores 1 in the position given
        by the third parameter. Otherwise, it stores 0.
        """
        DEBUG("processing opcode 7..." + str(param1) + ' ' + str(param2))
        if param1 < param2:
            self.set_position_value(param3, 1)
        else:
            self.set_position_value(param3, 0)
        return 4  # proper jump ahead


    def process_opcode_8(self, param1, param2, param3):
        """
        # is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given
        by the third parameter. Otherwise, it stores 0.
        """
        DEBUG("processing opcode 8..." + str(param1) + ' ' + str(param2) + ' ' + str(param3))
        if param1 == param2:
            self.set_position_value(param3, 1)
        else:
            self.set_position_value(param3, 0)
        return 4  # proper jump ahead


    def get_param_modes(self, opcode):
        DEBUG('getting param modes')
        strcode = str(opcode)
        modes = strcode[:-2]
        mode_list = []
        while len(modes):
            mode_list.append(int(modes[-1]))
            modes = modes[:-1]
        DEBUG('param modes: ' + str(mode_list))
        return mode_list


    def get_param_value(self, param, param_mode):
        if param_mode == 1:  # immediate mode
            return param
        return self.get_position_value(param)  # indirect mode


    def process_next_instruction(self):
        DEBUG("=== EIP: " + str(self._instruction_pointer) + " ===")
        raw_opcode = self._intcode[self._instruction_pointer]
        strcode = str(raw_opcode)

        if len(strcode) > 2:
            param_modes = self.get_param_modes(raw_opcode)
            opcode = int(strcode[-2:])
        else:
            param_modes = [0, 0, 0]
            opcode = int(strcode)

        # param modes default to 0
        param1_mode = param_modes[0] if (len(param_modes) > 0) else 0
        param2_mode = param_modes[1] if (len(param_modes) > 1) else 0
        param3_mode = param_modes[2] if (len(param_modes) > 2) else 0
        param1_addr = self._instruction_pointer + 1
        param2_addr = self._instruction_pointer + 2
        param3_addr = self._instruction_pointer + 3

        if opcode == 1:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self._intcode[param3_addr]
            self.process_opcode_1(param1, param2, param3)
            jump_ahead = 4
        elif opcode == 2:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self._intcode[param3_addr]
            self.process_opcode_2(param1, param2, param3)
            jump_ahead = 4
        elif opcode == 3:
            param1 = self._intcode[param1_addr]
            self.process_opcode_3(param1)
            jump_ahead = 2
        elif opcode == 4:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            self.process_opcode_4(param1)
            jump_ahead = 2
        elif opcode == 5:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            jump_ahead = self.process_opcode_5(param1, param2)
        elif opcode == 6:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            jump_ahead = self.process_opcode_6(param1, param2)
        elif opcode == 7:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self._intcode[param3_addr]
            jump_ahead = self.process_opcode_7(param1, param2, param3)
        elif opcode == 8:
            param1 = self.get_param_value(self._intcode[param1_addr], param1_mode)
            param2 = self.get_param_value(self._intcode[param2_addr], param2_mode)
            param3 = self._intcode[param3_addr]
            jump_ahead = self.process_opcode_8(param1, param2, param3)
        elif opcode == 99:
            return -1
        else:
            DEBUG("Unrecognized opcode " + str(opcode))
            return -1
        return jump_ahead

    def run(self):
        jump_ahead = 0
        DEBUG('Running ' + self._name)
        while jump_ahead > -1:
            jump_ahead = self.process_next_instruction()
            DEBUG('jumping ' + str(jump_ahead))
            self._instruction_pointer += jump_ahead

# original intcode
outside_intcode = [ 3,8,1001,8,10,8,105,1,0,0,21,38,59,84,93,110,191,272,353,434,99999,3,9,101,5,9,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,4,9,9,1002,9,4,9,4,9,99,3,9,102,5,9,9,1001,9,4,9,1002,9,2,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,1002,9,2,9,4,9,99,3,9,1002,9,5,9,101,4,9,9,102,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99 ]
#phase_settings_list = itertools.permutations([0,1,2,3,4], 5)
phase_settings_list = itertools.permutations([5, 6, 7, 8, 9], 5)

# Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):
#outside_intcode = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#phase_settings_list = itertools.permutations([0,1,2,3,4], 5)

# Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):
#outside_intcode = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]
#phase_settings_list = itertools.permutations([0,1,2,3,4], 5)

# Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):
#outside_intcode = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
#phase_settings_list = itertools.permutations([0,1,2,3,4], 5)


# Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
#outside_intcode = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#phase_settings_list = itertools.permutations([5, 6, 7, 8, 9], 5)

# Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
#outside_intcode = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
#phase_settings_list = itertools.permutations([5, 6, 7, 8, 9], 5)

# compare input to 8 (position mode)
#outside_intcode = [ 3,9,8,9,10,9,4,9,99,-1,8 ]

# less than 8 (position mode)
#outside_intcode = [3,9,7,9,10,9,4,9,99,-1,8]

# equal to 8 (immediate mode)
#outside_intcode = [3,3,1108,-1,8,3,4,3,99]

# less than 8 (immediate mode)
#outside_intcode = [ 3,3,1107,-1,8,3,4,3,99 ]

# jump test (position mode)
#outside_intcode = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]

# jump test (immediate mode)
#outside_intcode = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

#The following example program uses an input instruction to ask for a single number. The program will then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
#outside_intcode = [3 ,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

# template
#outside_intcode = []


if __name__ == "__main__":
    thruster_inputs = []
    for phase_settings in phase_settings_list:
        DEBUG("phase settings " + str(phase_settings))
        amplifier_output = 0
        amplifiers = []
        amplifier_queues = []

        # create amplifiers and amplifier queues
        for amplifier_number in range(0,5):
            amplifier_queue = Queue()
            # init amplifier
            amplifier = IntcodeComputer(outside_intcode, 'Amplifier #'+str(amplifier_number))
            amplifiers.append(amplifier)
            amplifier_queues.append(amplifier_queue)

        for amplifier_index in range(len(amplifiers)):
            # input queue is the output queue of the previous amplifier
            # if on the first amplifier, then the input queue is the output queue of the last amplifier
            input_queue = amplifier_queues[amplifier_index - 1]

            # init input queue with phase setting for the amplifier
            input_queue.put(phase_settings[amplifier_index])

            # if we're on the first amplifier, initial input is 0
            if amplifier_index == 0:
                input_queue.put(0)

            # get the output queue for the current amplifier
            output_queue = amplifier_queues[amplifier_index]

            # get the current amplifier
            amplifier = amplifiers[amplifier_index]

            # attach queues to amplifier
            amplifier.set_input_queue(input_queue)
            amplifier.set_output_queue(output_queue)

        # start each amplifier once they're all initialized
        for amplifier in amplifiers:
            amplifier.start()

        # wait for all amplifiers to finish
        for amplifier in amplifiers:
            amplifier.join()

        for output_queue_index in range(len(amplifier_queues)):
            output_queue = amplifier_queues[output_queue_index]
            print('Output Queue #' + str(output_queue_index))
            while output_queue.empty() is False:
                amplifier_output = output_queue.get()
                print(str(amplifier_output))
                thruster_inputs.append((amplifier_output, phase_settings))

    max_thruster_input = 0
    max_phase_setting = []
    print(str(thruster_inputs))
    for thruster_input in thruster_inputs:
        if thruster_input[0] > max_thruster_input:
            max_thruster_input = thruster_input[0]
            max_phase_setting = thruster_input[1]
    print('max input: ' + str(max_thruster_input))
    print('max setting: ' + str(max_phase_setting))
