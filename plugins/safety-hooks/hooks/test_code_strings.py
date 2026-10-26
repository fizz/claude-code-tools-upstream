"""A shell's -c string and eval's arguments are commands."""
import pytest
from command_utils import extract_code_strings
from rm_block_hook import check_rm_command


def test_extracts_the_code_string():
    assert extract_code_strings("bash -c 'rm x'") == ["rm x"]
    assert extract_code_strings("bash -lc 'rm x'") == ["rm x"]
    assert extract_code_strings("sh -e -o pipefail -c 'rm x'") == ["rm x"]
    assert extract_code_strings("/bin/zsh -c -- 'rm x'") == ["rm x"]
    assert extract_code_strings("A=1 dash -c 'rm x'") == ["rm x"]
    assert extract_code_strings("eval rm x") == ["rm x"]
    assert extract_code_strings("eval 'rm x'") == ["rm x"]


def test_no_code_string():
    assert extract_code_strings("bash script.sh") == []
    assert extract_code_strings("bash --login") == []
    assert extract_code_strings("eval") == []
    assert extract_code_strings("echo -c 'rm x'") == []
    assert extract_code_strings("bash -c 'unbalanced") == []


@pytest.mark.parametrize("command", [
    'bash -c "rm x"',
    "sh -c 'rm -rf build'",
    "zsh -lc 'rm x'",
    'eval "rm x"',
    "eval rm x",
    "bash -c 'echo $(rm x)'",
    "ls && bash -c 'rm x'",
])
def test_blocks_rm_in_a_code_string(command):
    assert check_rm_command(command)[0]


@pytest.mark.parametrize("command", [
    "bash -c 'echo rm'",
    "bash rm.sh",
    "eval echo rm",
])
def test_allows_code_strings_without_rm(command):
    assert not check_rm_command(command)[0]
