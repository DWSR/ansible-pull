# -*- coding: utf-8 -*-
import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("path", ["/opt/anzibal/.ansible", "/opt/anzibal/bin/.venv"])
def test_paths(host, path):
    f = host.file(path)

    assert f.exists
    assert f.is_directory
    assert f.user == "anzibal"
    assert f.group == "anzibal"


@pytest.mark.parametrize(
    "path",
    ["/opt/anzibal/bin/do_ansible_pull", "/opt/anzibal/bin/.venv/bin/ansible-pull"],
)
def test_bins(host, path):
    f = host.file(path)
    assert f.exists
    assert f.is_file
    assert f.user == "anzibal"
    assert f.group == "anzibal"


def test_account(host):
    u = host.user("anzibal")
    assert u.uid <= 1000
    assert "anzibal" in u.groups
    assert "anzibal" in u.group
    assert u.shell == "/bin/bash"

    ssh_key = host.file(f"{u.home}/.ssh/ansible_deploy_key")

    assert ssh_key.user == "anzibal"
    assert ssh_key.group == "anzibal"
    assert ssh_key.contains("-----BEGIN OPENSSH PRIVATE KEY-----")
    assert ssh_key.contains("-----END OPENSSH PRIVATE KEY-----")

    ssh_pub_key = host.file(f"{u.home}/.ssh/ansible_deploy_key.pub")

    assert ssh_pub_key.user == "anzibal"
    assert ssh_pub_key.group == "anzibal"
    assert ssh_pub_key.contains("ssh-ed25519")
    assert ssh_pub_key.contains("ansible-generated")


def test_ansible_timer(host):
    svc = host.service("ansible-pull.timer")

    assert svc.is_enabled
    assert svc.is_running


def test_ansible_service(host):
    svc = host.service("ansible-pull.service")

    assert svc.is_enabled


def test_running_ansible_pull(host):
    pull_script = "/opt/anzibal/bin/do_ansible_pull"

    assert host.run_expect([0], pull_script)
