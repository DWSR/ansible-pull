# ansible_pull

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

**For CentOS 7 users:** This role will install pip via a `curl2bash` command if
it is not detected in the system path. To sanely install `pip` on remote nodes,
check out [Geerlingguy's Pip role](https://galaxy.ansible.com/geerlingguy/pip)

## Role Variables

| Variable                            |   Type  |              Default Value            | Description |
|-------------------------------------|:-------:|:-------------------------------------:|-------------|
| ansible_pull_create_ssh_key         | Boolean |                 `true`                | Whether or not to create an SSH key if not also creating a user. Ignored if `ansible_pull_create_user` is `true`. |
| ansible_pull_create_user            | Boolean |                 `true`                | Whether or not to create a system user for Ansible to run under. |
| ansible_pull_crontab_schedule       | Dict    |            Every 15 minutes           | The crontab schedule to use if `ansible_pull_timer_method` is set to `cron`. Uses the same argument names as the [cron module](https://docs.ansible.com/ansible/latest/modules/cron_module.html) |
| ansible_pull_existing_ssh_privkey   | String  | `.ssh/id_ed25519` | The path to an existing SSH private key to use. This path is relative to the home directory of the account used to connect to the remote node. |
| ansible_pull_existing_ssh_pubkey    | String  | `.ssh/id_ed25519.pub` | The path to an existing SSH public key to use. This is only used when adding a deploy key to a GitHub repository. |
| ansible_pull_extra_packages         | Dict    | `{}` | Extra PyPI packages to install when `ansible_pull_install_method` is set to `venv`. The key is the package name and the value is the version |
| ansible_pull_github                 | Dict    | `{}` | Used for automatically adding a deploy key to a GitHub repository. See [Adding a Deploy Key to a GitHub repo](#adding-a-deploy-key-to-a-github-repo)|
| ansible_pull_install_dir            | String  | `/opt/ansible` | The directory to install Ansible into. If `ansible_pull_create_user` is `true`, this will be used as the home directory for the created user. |
| ansible_pull_install_method         | String  | `venv` | How to install Ansible. Currently only `venv` is supported. |
| ansible_pull_install_pip            | Boolean | `true` | Whether or not to install Pip via `curl2bash` under CentOS 7. If set to `false`, `pip` must be present in the system path otherwise this role will fail. |
| ansible_pull_install_system_prereqs | Boolean | `true` | Whether or not to install system packages to satisfy prerequisites of this module. See `vars/main.yml` for a list of packages that will be installed. |
| ansible_pull_inventory              | String  | `""` | The inventory file to pass to `ansible-pull`. Path is relative to the repository root. |
| ansible_pull_logs_path              | String  | `logs/ansible-pull/ansible-pull.log`  | The path to the log file that will be generated when `ansible_pull_timer_method` is set to a value other than `systemd`. Interpreted as relative to `ansible_pull_install_dir` |
| ansible_pull_logs_rotate            | Boolean | `true` | Whether or not to place a `logrotate` config file into `/etc/logrotate.d`. Ignored if `ansible_pull_timer_method` is set to `systemd`. Requires `become`. |
| ansible_pull_playbook               | String  | `""` | The playbook file to pass to `ansible-pull`. Path is relative to the repository root. |
| ansible_pull_repo_branch            | String  | `""` | The repository branch to use for `ansible-pull`. Can be any valid Git ref. |
| ansible_pull_repo_url               | String  | `""` | The URL to the repository to pass to `ansible-pull`. When using an SSH URL, authentication will use the role-created private key or the path in `ansible_pull_existing_ssh_privkey`.
| ansible_pull_systemd_period         | String  | `15min` | When `ansible_pull_timer_method` is set to `systemd`, this is used as the period between runs. Takes any value systemd considers valid for `OnUnitActiveSec`. |
| ansible_pull_timer_method           | String  | `systemd` | The timer method to use. Currently supports either `systemd` or `cron`. |
| ansible_pull_username               | String  | `ansible` | The username of the user that `ansible-pull` will be run as. Will be created or updated if `ansible_pull_create_user` is set to `true`. |
| ansible_pull_vaults                 | Dict    | `{}` | The Ansible Vault identities and passphrases to save to the node. The key is the identity name and the value is the passphrase, which will be saved to a file. These Vault identities will be passed to `ansible-pull` via `--vault-id`. |

## Dependencies

None

## Adding a Deploy Key to a GitHub Repo

This role supports automatically adding a
[Deploy Key](https://github.blog/2015-06-16-read-only-deploy-keys/) to a GitHub
repository if **all of** the following keys are added to the
`ansible_pull_github` dict:

* `auth_token`: A [Personal Access Token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
  that will be used to authenticate to the GitHub API. As with any API key, this
  value should be encrypted (e.g. using Ansible Vault).
* `repo_name`: The name of the repository.
* `repo_owner`: The owner of the repository. This is either a GitHub username or
  GitHub organization.

The added Deploy Key will have a comment of `<user>@<ansible_host>`

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

MPL-2.0

## Author Information

This role was created in 2020 by [Brandon McNama](https://github.com/dwsr).
