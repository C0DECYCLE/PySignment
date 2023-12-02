import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../vm/")

from assembler import main
from arrays import DataAllocator
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
    monkeypatch.setattr("sys.argv", ["arrays.py", inputFile, str(outputFile)])
    main(DataAllocator)
    assert filecmp.cmp(sharedFile, outputFile, shallow=False)
    teardown()


def testArray(monkeypatch, setupTeardown, sharedFile):
    inputFile = "as_files/array.as"
    outputFile = "mx_files/array.mx"
    expectedOutput = """270002
060102
000105
000304
040202
00030c
030205
060202
00030c
030205
070202
00030c
030205
020202
00030c
030205
010202
00030c
030205
080202
00030c
030205
000203
000206
00000c
000103
020303
020105
000305
00000c
00020d
020104
000304
030107
00010c
260108
00010d
190109
000001
"""
    fileTesting(
        monkeypatch, setupTeardown, sharedFile, inputFile, outputFile, expectedOutput
    )
