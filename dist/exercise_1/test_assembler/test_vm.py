from vm import main, VirtualMachine
import filecmp
import pytest


@pytest.fixture
def setupTeardown(sharedFile):
    def setup(content):
        pass

    def teardown():
        pass
    return setup, teardown


@pytest.fixture
def sharedFile(tmp_path):
    file_path = tmp_path / "expected.mx"
    return str(file_path)


def testCountVM(monkeypatch, setupTeardown, sharedFile, capsys):
    setup, teardown = setupTeardown
    inputFile = "mx_files/count.mx"
    expectedOutput = """>> 5
R000000 = 000000
R000001 = 000005
R000002 = 000007
R000003 = 000005
000000:   050102  070202  010306  00030a
000004:   000001  000000  000000  000000
"""

    setup(expectedOutput)
    monkeypatch.setattr("sys.argv", ["vm.py", inputFile, "-"])

    main(VirtualMachine)
    acutalOutput = capsys.readouterr().out

    assert acutalOutput == expectedOutput
    teardown()

def testAddBranchVM(monkeypatch, setupTeardown, sharedFile, capsys):
    setup, teardown = setupTeardown
    inputFile = "mx_files/add_and_branch.mx"
    expectedOutput = """R000000 = 000000
R000001 = 000001
R000002 = 000007
R000003 = 000000
000000:   050102  020103  070202  020106
000004:   010108  010102  000001  000000
"""

    setup(expectedOutput)
    monkeypatch.setattr("sys.argv", ["vm.py", inputFile, "-"])

    main(VirtualMachine)
    acutalOutput = capsys.readouterr().out

    assert acutalOutput == expectedOutput
    teardown()


def testCopyPrintVM(monkeypatch, setupTeardown, sharedFile, capsys):
    setup, teardown = setupTeardown
    inputFile = "mx_files/copy_and_print.mx"
    expectedOutput = """>> 0
R000000 = 000000
R000001 = 000000
R000002 = 000000
R000003 = 000000
000000:   0a0102  020104  00020a  000001
"""

    setup(expectedOutput)
    monkeypatch.setattr("sys.argv", ["vm.py", inputFile, "-"])

    main(VirtualMachine)
    acutalOutput = capsys.readouterr().out

    assert acutalOutput == expectedOutput
    teardown()

def testSwapSubtractVM(monkeypatch, setupTeardown, sharedFile, capsys):
    setup, teardown = setupTeardown
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

    setup(expectedOutput)
    monkeypatch.setattr("sys.argv", ["vm.py", inputFile, "-"])

    main(VirtualMachine)
    acutalOutput = capsys.readouterr().out

    assert acutalOutput == expectedOutput
    teardown()

