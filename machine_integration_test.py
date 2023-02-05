# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=no-self-use
# pylint: disable=line-too-long

"""Интеграционные тесты транслятора и машины
"""

import unittest

import machine
import translator


def start(source_code, output_file, input_file, data_sect):
    translator.main([source_code, output_file, data_sect])
    if input_file == "":
        return machine.main([output_file, data_sect])
    return machine.main([output_file, data_sect, input_file])


# class TestMachine(unittest.TestCase):
#
#     def test_prob5(self):
#         output = start("examples/prob5_code", "machine_code.out", "", "examples/data_section")
#         print(output)
#
#     def test_hello(self):
#         output = start("examples/hello_world_code", "data_sectionmachine_code.out", "", "examples/data_section")
#         assert output[0] == 'H' and output[1] == 'e' and output[2] == 'l' \
#                and output[3] == 'l' and output[4] == 'o' and output[5] == ' ' \
#                and output[6] == 'w' and output[7] == 'o' and output[8] == 'r' \
#                and output[9] == 'l' and output[10] == 'd' and output[11] == '!'
#
#     def test_cat(self):
#         output = start("examples/cat_code", "machine_code.out", "examples/input_hello", "examples/data_section")
#         assert output[0] == 'h' and output[1] == 'e' and output[2] == 'l' \
#                and output[3] == 'l' and output[4] == 'o'
#
#     def test_fib(self):
#         output = start("examples/fib_forth_code", "machine_code.out", "", "examples/data_section")
#         assert output[0] == '4613732'
#
#     def test_if(self):
#         output = start("examples/if_code", "machine_code.out", "", "examples/data_section")
#         assert output[0] == '-1'
#
#     def test_while(self):
#         output = start("examples/while_code", "machine_code.out", "", "examples/data_section")
#         assert output[0] == '-4' and output[1] == '-3' and output[2] == '-2'\
#                and output[3] == '-1'
