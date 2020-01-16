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


@pytest.mark.parametrize("path", ["/opt/ansible/.ansible/.vault/test"])
def test_vault(host, path):
    f = host.file(path)

    assert f.exists
    assert f.is_file
    assert f.user == "elbisna"
    assert f.group == "elbisna"
    assert f.mode == 0o600
    assert f.content_string == "ansiblepull"
