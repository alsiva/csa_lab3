# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=invalid-name
# pylint: disable=line-too-long

import sys

from isa import Opcode, write_code, Term


s2o = {
    "OVER": Opcode.OVER.value,
    "POW": Opcode.POW.value,
    "/": Opcode.DIV.value,
    ".": Opcode.PRINT.value,
    "DUP": Opcode.DUP.value,
    "<": Opcode.LT.value,
    "MOD": Opcode.MOD.value,
    "NEGATE": Opcode.NEG.value,
    "INVERT": Opcode.INV.value,
    "+": Opcode.PLUS.value,
    "*": Opcode.MULT.value,
    "DROP": Opcode.DROP.value,
    "PUSH": Opcode.PUSH.value,
    "WR": Opcode.WR_DIR.value,
    "WR#": Opcode.WR_NDR.value,
    "ROT": Opcode.ROT.value,
    "SWAP": Opcode.SWAP.value,
    "READ": Opcode.READ_DIR.value,
    "READ#": Opcode.READ_NDR.value,
    "NOP": Opcode.NOP.value,
}

commands = {
    "NOP",
    "ROT",
    "PUSH",
    ".",
    "OVER",
    "BEGIN",
    "DUP",
    "<",
    "WHILE",
    "WR",
    "WR#",
    "MOD",
    "NEGATE",
    "INVERT",
    "IF",
    "+",
    "*",
    "/",
    'POW',
    "ELSE",
    "ENDIF",
    "REPEAT",
    "DROP",
    "SWAP",
    "READ",
    "READ#"
}

def is_number(_str):
    try:
        float(_str)
        return True
    except ValueError:
        return False


def check_brackets(terms):
    deep_if = 0
    deep_else = 0
    for term in terms:
        if term.com == "IF":
            deep_if += 1
        if term.com == "ELSE":
            deep_if -= 1
            deep_else += 1
        if term.com == "ENDIF":
            assert deep_if + 1 == deep_else, "Unbalanced brackets!"
            deep_else -= 1
        assert deep_if >= 0 and deep_else >= 0, "Unbalanced brackets!"
    assert deep_if == 0 and deep_else == 0, "Unbalanced brackets!"

    loop_stack = []
    for term in terms:
        if term.com == "BEGIN":
            loop_stack.append("BEGIN")
        if term.com == "WHILE":
            assert loop_stack.pop() != "WHILE", "More than one while in one cycle!"
            loop_stack.append("WHILE")
        if term.com == "REPEAT":
            assert loop_stack.pop() == "WHILE", 'Infinite loop'

    assert len(loop_stack) == 0, 'Unbalanced brackets'


def translate(file):
    terms = []
    words_dict = {}
    vars_dict = {
        "#IN": 0,
        "#OUT": 1
    }
    strings_map = [ord('0'), ord('0')]

    lines = file.readlines()
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        com = line.split(" ", 1)
        if com[0] == "":
            continue

        com[0] = com[0].strip()

        if com[0][-1] == ':' and com[0][-2] == ')' and com[0][0] == '(':
            words_dict[com[0][1:-2]] = len(strings_map)
            for ch in com[1]:
                strings_map.append(ord(ch))
            strings_map.append(ord('\0'))
            continue

        if com[0][-1] == ':':
            if is_number(com[1].upper()):
                vars_dict[com[0].upper()[:-1]] = com[1].upper()
            else:
                vars_dict[com[0].upper()[:-1]] = words_dict[com[1][1:]]
            continue

        if com[0][0] == '\\':
            com[0] = chr(int(com[0][2:]))

        if com[0][-1] == '\n':
            com = com[0][0:-1]

        if com[0].upper() in commands:
            terms.append(Term(line_num, com[0].upper(), None))
        else:
            if com[0].upper() in vars_dict:
                terms.append(Term(line_num, "PUSH", vars_dict[com[0].upper()]))
            else:
                terms.append(Term(line_num, "PUSH", com[0]))

    check_brackets(terms)

    code = []
    jmp_stack = []

    for i, term in enumerate(terms):

        if term.com == "IF":
            code.append(None)
            jmp_stack.append(i)

        elif term.com.upper() == "ELSE":
            code.append(None)
            jmp_stack.append(i)

        elif term.com.upper() == "ENDIF":
            else_i = jmp_stack.pop()
            if_i = jmp_stack.pop()

            jmp_skipping_then = {"opcode": Opcode.JNT.value, "arg": else_i + 1, "term": terms[if_i]}

            jmp_skipping_else = {"opcode": Opcode.JMP.value, "arg": i + 1, "term": terms[else_i]}
            code[if_i] = jmp_skipping_then
            code[else_i] = jmp_skipping_else
            code.append({"opcode": Opcode.NOP.value, "term": term})

        elif term.com.upper() == "BEGIN":
            code.append(None)
            jmp_stack.append(i)

        elif term.com.upper() == "WHILE":
            code.append(None)
            jmp_stack.append(i)

        elif term.com.upper() == "REPEAT":
            i_while = jmp_stack.pop()
            i_begin = jmp_stack.pop()

            jmp_to_begin = {"opcode": Opcode.JMP.value, "arg": i_begin + 1, "term": term}
            jmp_skipping_while = {"opcode": Opcode.JNT.value, "arg": i + 1, "term": terms[i_while]}

            code[i_begin] = {"opcode": Opcode.BEGIN.value, "term": terms[i_begin]}
            code[i_while] = jmp_skipping_while
            code.append(jmp_to_begin)

        else:
            if term.arg is None:
                code.append({"opcode": s2o[term.com.upper()], "term": term})
            else:
                code.append({"opcode": s2o[term.com.upper()], "arg": term.arg, "term": term})

    code.append({"opcode": Opcode.HALT.value, "term": Term(len(code) + 1, "HALT", None)})
    return strings_map, code, len(lines)


def main(args):
    assert len(args) == 3, "Wrong arguments: translator.py <input_file> <target_file> <data_section_file>"
    source, target, data_section = args

    with open(source, "rt", encoding="utf-8") as f:
        strings, code, loc = translate(f)

    print("source LoC:", loc, "code instr:", len(code))
    write_code(target, code, strings, data_section)


if __name__ == "__main__":
    main(sys.argv[1:])
