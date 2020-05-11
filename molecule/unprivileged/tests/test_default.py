# -*- coding: utf-8 -*-
import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "path", ["/home/elbisna/bin/.venv", "/home/elbisna/logs", "/home/elbisna/.ansible"]
)
def test_paths(host, path):
    f = host.file(path)

    assert f.exists
    assert f.is_directory
    assert f.user == "elbisna"
    assert f.group == "elbisna"


def test_wrapper(host):
    wrapper_script = "/home/elbisna/bin/do_ansible_pull"
    f = host.file(wrapper_script)

    assert f.exists
    assert f.is_file
    assert f.user == "elbisna"
    assert f.group == "elbisna"

    host.run_expect([0], f"sudo -Hu elbisna {wrapper_script}")

    log = host.file("/home/elbisna/logs/ansible-pull/ansible-pull.log")

    assert log.exists
    assert log.is_file
    assert log.user == "elbisna"
    assert log.group == "elbisna"
    assert log.size > 0


def test_crontab(host):
    if host.system_info.distribution == "centos":
        f = host.file("/var/spool/cron/elbisna")
        group = "elbisna"
    else:
        f = host.file("/var/spool/cron/crontabs/elbisna")
        group = "crontab"

    entry = "*/15 * * * * /home/elbisna/bin/do_ansible_pull > /dev/null 2>&1"

    assert f.exists
    assert f.is_file
    assert f.user == "elbisna"
    assert f.group == group
    assert entry in f.content_string
