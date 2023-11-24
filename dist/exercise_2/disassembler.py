import sys
from dist.vm.architecture import OP_MASK, OP_SHIFT, OPS


class Disassembler:
    def disassemble(self, lines):
        lines = self._get_lines(lines)
        instructions = [int(ln, 16) for ln in lines]
        codeOPS = self._reverse_OPS()
        labels = []
        decompiled = [self._decompile(instr, codeOPS, labels) for instr in instructions]
        program = self._insert_labels(decompiled, labels)
        return program

    def _get_lines(self, lines):
        lines = [ln.strip() for ln in lines]
        lines = [ln for ln in lines if len(ln) > 0]
        return lines

    def _reverse_OPS(self):
        revCode = {}
        for key in OPS:
            code = OPS[key]["code"]
            revCode[code] = key
        return revCode

    def _decompile(self, instruction, codeOPS, labels):
        code, arg0, arg1 = self._uncombine(instruction)
        op = codeOPS[code]
        fmt = OPS[op]["fmt"]
        half = f"{op} {self._format(arg0, fmt[0])}"
        if self._is_label(op):
            i = self._store_label(labels, arg1)
            return f"{half} @{self._format_label(i)}"
        return f"{half} {self._format(arg1, fmt[1])}"

    def _uncombine(self, instruction):
        op = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return [op, arg0, arg1]

    def _format(self, arg, fmt):
        if fmt == "-":
            return ""
        elif fmt == "r":
            return f"R{arg}"
        elif fmt == "v":
            return f"{arg}"
        assert False, f"Unknown fmt {fmt}"

    def _is_label(self, op):
        return op == "beq" or op == "bne"

    def _store_label(self, labels, arg):
        i = len(labels) + 1
        labels.append((i, arg))
        return i

    def _format_label(self, i):
        return f"L{i:03x}"

    def _insert_labels(self, program, labels):
        labels.sort(key=lambda x: x[1], reverse=True)
        for label in labels:
            program.insert(label[1], f"{self._format_label(label[0])}:")
        return program


def main(disassembler_cls):
    assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
    reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
    writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout
    lines = reader.readlines()
    disassembler = disassembler_cls()
    program = disassembler.disassemble(lines)
    for instruction in program:
        print(instruction, file=writer)


if __name__ == "__main__":
    main(Disassembler)
