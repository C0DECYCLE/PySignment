import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../vm/")

from vm import main as vmMain, VirtualMachine
from assembler import main as asMain
from arrays import DataAllocator


def testOutOfMemoryError(monkeypatch):
    inputFile = "as_files/out_of_memory.as"
    expectedError = "Allocation 'array' requires too much memory"
    monkeypatch.setattr("sys.argv", ["arrays.py", inputFile, "-"])
    try:
        asMain(DataAllocator)
    except AssertionError as e:
        assert str(e) == expectedError


def testUnknownError(monkeypatch):
    inputFile = "mx_files/unknown.mx"
    expectedError = "Unknown op 00000f"
    monkeypatch.setattr("sys.argv", ["vm.py", inputFile, "-"])
    try:
        vmMain(VirtualMachine)
    except AssertionError as e:
        assert str(e) == expectedError
