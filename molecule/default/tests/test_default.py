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


def test_file_content(host):
    """Verify that the file contains the expected content."""
    ff = host.file("/etc/ssh/sshd_config.d/99-allow-rsakeys.conf")

    if host.system_info.distribution in ["amzn"]:
        # OpenSSH pre-8.5
        assert ff.contains("^PubkeyAcceptedKeyTypes")
    elif host.system_info.distribution in ["debian"]:
        if host.system_info.codename in ["stretch", "buster", "bullseye"]:
            # OpenSSH pre-8.5
            assert ff.contains("^PubkeyAcceptedKeyTypes")
        elif host.system_info.codename in ["bookworm"]:
            # OpenSSH 8.5+
            assert ff.contains("^PubkeyAcceptedAlgorithms")
        else:
            assert False, f"Unknown Debian codename {host.system_info.codename}"
    elif host.system_info.distribution in ["ubuntu"]:
        if host.system_info.codename in ["bionic", "focal"]:
            # OpenSSH pre-8.5
            assert ff.contains("^PubkeyAcceptedKeyTypes")
        else:
            assert False, f"Unknown Ubuntu codename {host.system_info.codename}"
    elif host.system_info.distribution in ["fedora", "kali"]:
        # OpenSSH 8.5+
        assert ff.contains("^PubkeyAcceptedAlgorithms")
    else:
        assert False, f"Unknown distribution {host.system_info.distribution}"
