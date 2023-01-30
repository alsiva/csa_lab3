# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

import json
from collections import namedtuple
from enum import Enum


class Opcode(str, Enum):
    WR_DIR = 'WRITE_DIR'
    WR_NDR = 'WRITE_NDR'
    READ_DIR = 'READ_DIR'
    READ_NDR = 'READ_NDR'

    PRINT = 'PRINT'

    BEGIN = 'BEGIN'
    NOP = 'NOP'

    MOD = 'MOD'
    PLUS = 'PLUS'
    LT = 'LT'
    NEG = 'NEG'
    INV = 'INVERT'

    DUP = 'DUP'
    OVER = 'OVER'
    ROT = 'ROT'
    SWAP = 'SWAP'

    PUSH = 'PUSH'
    DROP = 'DROP'

    JMP = 'JMP'
    JNT = 'JNT'

    HALT = 'HALT'


class Term(namedtuple('Term', 'line_num com arg')):
    """Описание выражения из исходного текста программы."""


def write_code(filename, code, strings, data_section_file):
    """Записать машинный код в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(code, indent=4))

    with open(data_section_file, "w", encoding="utf-8") as file:
        file.write(json.dumps(strings, indent=4))


def read_code(filename, data_section):
    """Прочесть машинный код из файла."""
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())

    for instr in code:
        # Конвертация строки в Opcode
        instr['opcode'] = Opcode(instr['opcode'])
        # Конвертация списка из term в класс Term
        if 'term' in instr:
            instr['term'] = Term(
                instr['term'][0], instr['term'][1], instr['term'][2])

    with open(data_section, encoding="utf-8") as file2:
        if data_section == "":
            data_section = []
        else:
            data_section = json.loads(file2.read())
    return code, data_section
