import sys

from architecture import OPS, VMState
from vm_extend import VirtualMachineExtend


class VirtualMachineBreak(VirtualMachineExtend):
    # [init]
    def __init__(self):
        super().__init__()
        self.breaks = {}
        self.watch = {}
        self.handlers |= {
            "break": self._do_add_breakpoint,
            "clear": self._do_clear_breakpoint,
            "watch": self._do_add_watchpoint,
            "end": self._do_end_watchpoint,
        }

    # [/init]

    # [show]
    def show(self, args):
        super().show(args)
        if self.breaks:
            self.write("-" * 6)
            self.write("Breakpoints:")
            for key, instruction in self.breaks.items():
                self.write(f"{key:06x}: {self.disassemble(key, instruction)}")
        if self.watch:
            self.write("-" * 6)
            self.write("Watchpoints:")
            for key, memory in self.watch.items():
                self.write(f"{key:06x}: {memory:06x}")

    # [/show]

    # [run]
    def run(self):
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:
            instruction = self.ram[self.ip]
            op, arg0, arg1 = self.decode(instruction)

            if op == OPS["brk"]["code"]:
                original = self.breaks[self.ip]
                op, arg0, arg1 = self.decode(original)
                self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)

            elif op == OPS["wap"]["code"]:
                original = self.watch[self.ip]
                op, arg0, arg1 = self.decode(original)
                self.ip += 1
                self.execute(op, arg0, arg1)

            elif op == OPS["str"]["code"]:
                self.assert_is_register(arg0)
                self.assert_is_register(arg1)
                self.assert_is_address(self.reg[arg1])
                if self.ram[self.reg[arg1]] == OPS["wap"]["code"]:
                    self.state = VMState.STEPPING
                    old = self.watch[self.reg[arg1]]
                    new = self.reg[arg0]
                    self.write(
                        f"Memory Adress: {self.reg[arg1]:06x} | old Value: {old} | new Value: {new}"
                    )
                    self.watch[self.reg[arg1]] = new
                    self.interact(self.ip)
                    self.ip += 1
                    self.execute(op, arg0, arg1)
                else:
                    if self.state == VMState.STEPPING:
                        self.interact(self.ip)
                    self.ip += 1
                    self.execute(op, arg0, arg1)

            else:
                if self.state == VMState.STEPPING:
                    self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)

    # [/run]

    # [add]
    def _do_add_breakpoint(self, addr, args):
        if not self.ensure_length_interact(args, 1):
            return
        addr = addr if not args else int(args[0])
        if self.ram[addr] == OPS["brk"]["code"]:
            return
        self.breaks[addr] = self.ram[addr]
        self.ram[addr] = OPS["brk"]["code"]
        return True

    # [/add]

    # [clear]
    def _do_clear_breakpoint(self, addr, args):
        if not self.ensure_length_interact(args, 1):
            return
        addr = addr if not args else int(args[0])
        if self.ram[addr] != OPS["brk"]["code"]:
            return
        self.ram[addr] = self.breaks[addr]
        del self.breaks[addr]
        return True

    # [/clear]

    def _do_add_watchpoint(self, addr, args):
        if not self.ensure_length_interact(args, 1):
            return
        addr = addr if not args else int(args[0])
        if self.ram[addr] == OPS["wap"]["code"]:
            return
        self.watch[addr] = self.ram[addr]
        self.ram[addr] = OPS["wap"]["code"]
        return True

    def _do_end_watchpoint(self, addr, args):
        if not self.ensure_length_interact(args, 1):
            return
        addr = addr if not args else int(args[0])
        if self.ram[addr] != OPS["wap"]["code"]:
            return
        self.ram[addr] = self.watch[addr]
        del self.watch[addr]

    def ensure_length_interact(self, args, length):
        if not args:
            return True
        if type(length) == tuple:
            if len(args) not in length:
                self.write(f"Arguments cannot exceed length {max(length)}")
                self.interact(self.ip)
                return False
        elif len(args) != length:
            self.write(f"Arguments cannot exceed length {length}")
            self.interact(self.ip)
            return False
        return True


if __name__ == "__main__":
    VirtualMachineBreak.main()
