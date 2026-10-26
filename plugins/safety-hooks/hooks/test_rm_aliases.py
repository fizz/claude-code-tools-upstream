"""unlink, srm and shred -u delete files as rm does."""
import pytest
from rm_block_hook import check_rm_command


@pytest.mark.parametrize("command", [
    "unlink foo",
    "/bin/unlink foo",
    "srm foo",
    "shred -u foo",
    "shred -zu -n 3 foo",
    "shred --remove foo",
    "shred --remove=wipesync foo",
    "ls && unlink foo",
])
def test_blocks_commands_that_delete(command):
    assert check_rm_command(command)[0]


@pytest.mark.parametrize("command", [
    "shred foo",
    "shred -z -n 3 foo",
    "echo unlink",
    "rmdir empty",
])
def test_allows_commands_that_keep_the_file(command):
    assert not check_rm_command(command)[0]
