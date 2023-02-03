# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=no-self-use

"""Интеграционные тесты транслятора и машины
"""

import unittest

import isa
import translator


def start(input_file, output_file, correct_file, data_section_file):
    translator.main([input_file, output_file, data_section_file])
    result = isa.read_code(output_file, data_section_file)
    print(result)
    #correct_code = isa.read_code(correct_file, data_section_file)
    #assert result == correct_code


class TestTranslator(unittest.TestCase):

    def test_fib(self):
        start("examples/fib_forth_code", "machine_code.out",
              "examples/correct_fib_forth_code", "examples/data_section")

    def test_cat(self):
        start("examples/cat_code", "machine_code.out",
              "examples/correct_cat_code", "examples/data_section")
