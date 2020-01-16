# -*- coding: utf-8 -*-
import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "path", [("/opt/ansible/.ansible"), ("/opt/ansible/bin/.venv")],
)
def test_directory(host, path):
    f = host.file(path)

    assert f.exists
    assert f.is_directory
    assert f.user == "elbisna"
    assert f.group == "elbisna"


@pytest.mark.parametrize("package_name", [("ansible"), ("passlib"), ("proxmoxer")])
def test_venv_package(host, package_name):
    venv_path = "/opt/ansible/bin/.venv"
    if (
        host.system_info.distribution == "centos"
        and float(host.system_info.release) < 8
    ):
        pip_path = f"{venv_path}/bin/pip"
    else:
        pip_path = f"{venv_path}/bin/pip3"

    pip_pkgs = host.pip_package.get_packages(pip_path=pip_path)

    assert package_name in pip_pkgs


def test_running_ansible_pull(host):
    pull_script = "/opt/ansible/bin/do_ansible_pull"
    f = host.file(pull_script)

    assert f.exists
    assert f.user == "elbisna"
    assert f.group == "elbisna"
    assert f.mode == 0o700

    assert host.run_expect([0], pull_script)
