from disassembler import main, Disassembler
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
    monkeypatch.setattr("sys.argv", ["disassembler.py", inputFile, str(outputFile)])
    main(Disassembler)
    assert filecmp.cmp(sharedFile, outputFile, shallow=False)
    teardown()


def testCount(monkeypatch, setupTeardown, sharedFile):
    inputFile = "mx_files/count.mx"
    outputFile = "as_files/count.as"
    expectedOutput = """ldc R1 5
ldc R2 7
add R3 R1
prr R3
hlt
"""
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testAddBranch(monkeypatch, setupTeardown, sharedFile):
    inputFile = "mx_files/add_and_branch.mx"
    outputFile = "as_files/add_and_branch.as"
    expectedOutput = """ldc R1 5
L001:
ldr R1 R2
ldc R2 7
add R1 R2
beq R1 @L001
ldc R1 1
hlt
"""
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testBranchNotEqual(monkeypatch, setupTeardown, sharedFile):
    inputFile = "mx_files/branch_not_equal.mx"
    outputFile = "as_files/branch_not_equal.as"
    expectedOutput = """ldc R0 5
L001:
inc R0
dec R0
dec R0
bne R0 @L001
ldc R1 1
L002:
dec R1
beq R1 @L002
hlt
"""
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testCopyPrint(monkeypatch, setupTeardown, sharedFile):
    inputFile = "mx_files/copy_and_print.mx"
    outputFile = "as_files/copy_and_print.as"
    expectedOutput = """ldc R1 10
cpy R1 R2
prr R2
hlt
"""
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )


def testSwapSubtract(monkeypatch, setupTeardown, sharedFile):
    inputFile = "mx_files/swap_subtract_decrement.mx"
    outputFile = "as_files/swap_subtract_decrement.as"
    expectedOutput = """ldc R1 15
ldc R2 8
swp R1 R2
dec R1
dec R2
sub R1 R2
str R1 R2
prr R1
prm R2
hlt
"""
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )
