# -*- coding: utf-8 -*-
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_known_hosts_does_not_exist(host):
    u = host.user("elbisna")
    ssh_known_hosts = host.file(f"{u.home}/.ssh/known_hosts")

    assert not ssh_known_hosts.exists
