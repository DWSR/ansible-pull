# -*- coding: utf-8 -*-
import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("ubuntu:debian")


@pytest.mark.parametrize("bin", ["git"])
def test_binaries_are_present(host, bin):
    cmd = host.run_expect([0], f"command -v {bin}")

    assert cmd.succeeded


@pytest.mark.parametrize(
    "package_name", ["python3-pip", "python3-venv", "python3-setuptools", "git"]
)
def test_packages_are_installed(host, package_name):
    pkg = host.package(package_name)

    assert pkg.is_installed


def test_pip_system_packages_installed(host):
    if (
        host.system_info.distribution == "centos"
        and float(host.system_info.release) < 8
    ):
        pip_path = "/usr/bin/pip"
        packages = ["virtualenv", "setuptools"]
    else:
        pip_path = "/usr/bin/pip3"
        packages = ["venv", "setuptools"]
    pip_pkgs = host.pip_package.get_packages(pip_path=pip_path)

    for pkg in packages:
        assert pkg in pip_pkgs
