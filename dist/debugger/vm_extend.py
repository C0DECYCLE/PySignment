import sys

from architecture import VMState
from vm_step import VirtualMachineStep


class VirtualMachineExtend(VirtualMachineStep):
    # [init]
    def __init__(self, reader=input, writer=sys.stdout):
        super().__init__(reader, writer)
        self.handlers = {
            "d": self._do_disassemble,
            "dis": self._do_disassemble,
            "i": self._do_ip,
            "ip": self._do_ip,
            "m": self._do_memory,
            "memory": self._do_memory,
            "q": self._do_quit,
            "quit": self._do_quit,
            "r": self._do_run,
            "run": self._do_run,
            "s": self._do_step,
            "step": self._do_step,
        }
        self.multiHandlers = ["m", "memory"]

    # [/init]

    # [interact]
    def interact(self, addr):
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        interacting = True
        while interacting:
            try:
                command = self.read(f"{addr:06x} [{prompt}]> ")
                command = command.split()
                if not command[0]:
                    continue
                elif command[0] not in self.handlers:
                    self.write(f"Unknown command {command}")
                elif command[0] in self.multiHandlers:
                    args = None if len(command) == 1 else command[1:]
                    interacting = self.handlers[command[0]](self.ip, args)
                elif len(command) > 1:
                    self.write(f"Command takes no arguments")
                else:
                    interacting = self.handlers[command[0]](self.ip)
            except EOFError:
                self.state = VMState.FINISHED
                interacting = False

    # [/interact]

    def _do_disassemble(self, addr):
        self.write(self.disassemble(addr, self.ram[addr]))
        return True

    def _do_ip(self, addr):
        self.write(f"{self.ip:06x}")
        return True

    # [memory]
    def _do_memory(self, addr, args=None):
        self.show(args)
        return True

    # [/memory]

    def _do_quit(self, addr):
        self.state = VMState.FINISHED
        return False

    def _do_run(self, addr):
        self.state = VMState.RUNNING
        return False

    # [step]
    def _do_step(self, addr):
        self.state = VMState.STEPPING
        return False

    # [/step]


if __name__ == "__main__":
    VirtualMachineExtend.main()
