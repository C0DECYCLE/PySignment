import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../vm/")

from vm import main, VirtualMachine


def fileTesting(monkeypatch, capsys, inputFile, expectedOutput):
    monkeypatch.setattr("sys.argv", ["vm.py", inputFile, "-"])
    main(VirtualMachine)
    actualOutput = capsys.readouterr().out
    assert actualOutput == expectedOutput


def testCountVM(monkeypatch, capsys):
    inputFile = "mx_files/count.mx"
    expectedOutput = """>> 5
R000000 = 000000
R000001 = 000005
R000002 = 000007
R000003 = 000005
000000:   050102  070202  010306  00030a
000004:   000001  000000  000000  000000
"""
    fileTesting(monkeypatch, capsys, inputFile, expectedOutput)


def testAddBranchVM(monkeypatch, capsys):
    inputFile = "mx_files/add_and_branch.mx"
    expectedOutput = """R000000 = 000000
R000001 = 000001
R000002 = 000007
R000003 = 000000
000000:   050102  020103  070202  020106
000004:   010108  010102  000001  000000
"""
    fileTesting(monkeypatch, capsys, inputFile, expectedOutput)


def testBranchNotEqualVM(monkeypatch, capsys):
    inputFile = "mx_files/branch_not_equal.mx"
    expectedOutput = """R000000 = 000000
R000001 = -00001
R000002 = 000000
R000003 = 000000
000000:   050002  00000c  00000d  00000d
000004:   010009  010102  00010d  060108
000008:   000001  000000  000000  000000
"""
    fileTesting(monkeypatch, capsys, inputFile, expectedOutput)


def testCopyPrintVM(monkeypatch, capsys):
    inputFile = "mx_files/copy_and_print.mx"
    expectedOutput = """>> 0
R000000 = 000000
R000001 = 000000
R000002 = 000000
R000003 = 000000
000000:   0a0102  020104  00020a  000001
"""
    fileTesting(monkeypatch, capsys, inputFile, expectedOutput)


def testSwapSubtractVM(monkeypatch, capsys):
    inputFile = "mx_files/swap_subtract_decrement.mx"
    expectedOutput = """>> -7
>> -7
R000000 = 000000
R000001 = -00007
R000002 = 00000e
R000003 = 000000
000000:   0f0102  080202  02010e  00010d
000004:   00020d  020107  020105  00010a
000008:   00020b  000001  000000  000000
00000c:   000000  000000  -00007  000000
"""
    fileTesting(monkeypatch, capsys, inputFile, expectedOutput)
