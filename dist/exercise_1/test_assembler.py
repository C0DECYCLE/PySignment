import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../vm/")

from assembler import main, Assembler
import filecmp
import pytest


@pytest.fixture
def setupTeardown(sharedFile):
    def setup(content):
        with open(sharedFile, "w") as file:
            file.write(content)

    def teardown():
        with open(sharedFile, "w"):
            pass

    return setup, teardown


@pytest.fixture
def sharedFile(tmp_path):
    file_path = tmp_path / "expected.mx"
    return str(file_path)


def fileTesting(
    monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
):
    setup, teardown = setupTeardown
    setup(expectedOutput)
    monkeypatch.setattr("sys.argv", ["assembler.py", inputFile, str(outputFile)])
    main(Assembler)
    assert filecmp.cmp(sharedFile, outputFile, shallow=False)
    teardown()


def testCount(monkeypatch, setupTeardown, sharedFile):
    inputFile = "as_files/count.as"
    outputFile = "mx_files/count.mx"
    expectedOutput = "050102\n070202\n010306\n00030a\n000001\n"
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testAddBranch(monkeypatch, setupTeardown, sharedFile):
    inputFile = "as_files/add_and_branch.as"
    outputFile = "mx_files/add_and_branch.mx"
    expectedOutput = "050102\n020103\n070202\n020106\n010108\n010102\n000001\n"
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testBranchNotEqual(monkeypatch, setupTeardown, sharedFile):
    inputFile = "as_files/branch_not_equal.as"
    outputFile = "mx_files/branch_not_equal.mx"
    expectedOutput = """050002
00000c
00000d
00000d
010009
010102
00010d
060108
000001
"""
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testCopyPrint(monkeypatch, setupTeardown, sharedFile):
    inputFile = "as_files/copy_and_print.as"
    outputFile = "mx_files/copy_and_print.mx"
    expectedOutput = "0a0102\n020104\n00020a\n000001\n"
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testSwapSubtract(monkeypatch, setupTeardown, sharedFile):
    inputFile = "as_files/swap_subtract_decrement.as"
    outputFile = "mx_files/swap_subtract_decrement.mx"
    expectedOutput = "0f0102\n080202\n02010e\n00010d\n00020d\n020107\n020105\n00010a\n00020b\n000001\n"
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )
