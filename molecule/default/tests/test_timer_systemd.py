# -*- coding: utf-8 -*-
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_ansible_timer(host):
    svc = host.service("ansible-pull.timer")

    assert svc.is_enabled
    assert svc.is_running


def test_ansible_service(host):
    svc = host.service("ansible-pull.service")

    assert svc.is_enabled
