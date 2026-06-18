# OpenBao Ansible Plugins

[![ansible-test](https://github.com/flowerysong/ansible-flowerysong.openbao/actions/workflows/ansible-test.yml/badge.svg)](https://github.com/flowerysong/ansible-flowerysong.openbao/actions/workflows/ansible-test.yml)

This [Ansible](https://www.ansible.com/) collection
implements a number of plugins for interacting with
[OpenBao](https://openbao.org/). A complete set of low-level
operations (read, write, list, and delete) are available, so
functionality which does not yet have a higher-level interface should
still be possible to use. The implementation of high-level interfaces
prioritizes the subset of OpenBao functionality that I use.

## Dependencies

These plugins use standard Ansible features and require no extra
dependencies on the control node or target.

## Supported Ansible Versions

This collection is tested against the stable-2.18, stable-2.19,
stable-2.20, stable-2.21, and devel branches of ansible-core. Other
versions may or may not work.

## Supported OpenBao Versions

This collection is tested against OpenBao 2.5.x. Other versions may or
may not work.

Some plugin interfaces include features that were originally specific
to Vault Enterprise and are not yet covered by tests.

## Where's the Documentation?

Documentation is not available online. If you have the collection
installed you can access each plugin's documentation via the
ansible-doc command, e.g. `ansible-doc flowerysong.openbao.engine` or
`ansible-doc -t lookup flowerysong.openbao.read`
