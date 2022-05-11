"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("f", ["/etc/ssh/sshd_config.d/99-allow-rsakeys.conf"])
def test_files(host, f):
    """Verify that all expected files indeed exist."""
    ff = host.file(f)
    assert ff.exists
    assert ff.is_file
    assert ff.user == "root"
    assert ff.group == "root"
    assert ff.mode == 0o644
