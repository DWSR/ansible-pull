# ansible-pull

An Ansible role to install and configure ansible-pull

## Requirements

### Control Node

None

### Remote Node

None, though it is advisable to have the ability to install a Python virtualenv
already on the remote node. This role will attempt to install system packages
in an effort to ensure that it functions as expected, but more advanced users
will want to disable this functionality by setting
`ansible_pull_install_system_prereqs` and `ansible_pull_install_pip` to `false`.

To sanely install `pip` on remote nodes, check out
[Geerlingguy's Pip role](https://galaxy.ansible.com/geerlingguy/pip)

## Role Variables

A description of the settable variables for this role should go here, including
any variables that are in defaults/main.yml, vars/main.yml, and any variables
that can/should be set via parameters to the role. Any variables that are read
from other roles and/or the global scope (ie. hostvars, group vars, etc.) should
be mentioned here as well.

## Dependencies

None

## Example Playbook

This example is the minimum amount of information that must be passed to this
role in order for it to function.

Supplying only this information will cause this role to:

* Create a new user called `ansible` that will be used to run `ansible-pull`
* Install `ansible-pull` in a Virtualenv
* Run `ansible-pull` periodically via a `systemd` timer

```yaml
- hosts: pihole
  roles:
      - role: ansible-pull
        vars:
          ansible_pull_playbook: playbooks/pihole.yml
          ansible_pull_inventory: inventory.yml
          ansible_pull_repo_url: git@github.com:contoso/ansible.git
```

## License

BSD

## Author Information

This role was created in 2020 by [Brandon McNama](https://github.com/dwsr).
