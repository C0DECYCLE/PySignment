import sys

from architecture import VMState
from vm_step import VirtualMachineStep


class VirtualMachineExtend(VirtualMachineStep):
    # [init]
    def __init__(self, reader=input, writer=sys.stdout):
        super().__init__(reader, writer)
        self.handlers = {
            "dis": self._do_disassemble,
            "ip": self._do_ip,
            "memory": self._do_memory,
            "quit": self._do_quit,
            "run": self._do_run,
            "step": self._do_step,
        }
        self.multiHandlers = ["memory", "break", "clear", "watch", "end"]

    # [/init]

    def commandFinder(self, command):
        if not command:
            return "empty"
        realCommand = None
        for chars in self.handlers.keys():
            if chars.startswith(command):
                realCommand = chars
        return realCommand

    # [interact]
    def interact(self, addr):
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        interacting = True
        while interacting:
            try:
                cliargs = self.read(f"{addr:06x} [{prompt}]> ")
                command = cliargs.split()
                if not command:
                    continue
                args = None if len(command) == 1 else command[1:]
                handler = self.commandFinder(command[0])
                if not handler:
                    self.write(f"Unknown command {handler}")
                elif handler in self.multiHandlers:
                    interacting = self.handlers[handler](self.ip, args)
                elif args:
                    self.write(f"Command takes no arguments")
                else:
                    interacting = self.handlers[handler](self.ip)
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
