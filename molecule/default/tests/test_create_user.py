# -*- coding: utf-8 -*-
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_account(host):
    u = host.user("elbisna")
    assert u.uid <= 1000
    assert "elbisna" in u.groups
    assert "elbisna" in u.group
    assert u.shell == "/bin/bash"

    ssh_key = host.file(f"{u.home}/.ssh/id_ed25519")

    assert ssh_key.mode == 0o600
    assert ssh_key.user == "elbisna"
    assert ssh_key.group == "elbisna"
    assert ssh_key.contains("-----BEGIN OPENSSH PRIVATE KEY-----")
    assert ssh_key.contains("-----END OPENSSH PRIVATE KEY-----")

    ssh_pub_key = host.file(f"{u.home}/.ssh/id_ed25519.pub")

    assert ssh_pub_key.mode == 0o644
    assert ssh_pub_key.user == "elbisna"
    assert ssh_pub_key.group == "elbisna"
    assert ssh_pub_key.contains("ssh-ed25519")
    assert ssh_pub_key.contains("ansible-generated")


def test_pwless_sudo(host):
    with host.sudo("elbisna"):
        with host.sudo():
            host.run_expect([0], "echo 'Hello, world!'")
