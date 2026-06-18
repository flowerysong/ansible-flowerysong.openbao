#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: init
author: "Paul Arthur (@flowerysong)"
short_description: Initialize a OpenBao cluster
description:
  - Initialize a OpenBao cluster.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
options:
  secret_shares:
    description:
      - The number of shares to split the primary unseal key into.
    type: int
    default: 1
  secret_threshold:
    description:
      - The number of shares required to reconstruct the key.
    type: int
    default: 1
  pgp_keys:
    description:
      - A list of PGP public keys to use for encrypting the key shares.
    type: list
    elements: str
  root_token_pgp_key:
    description:
      - A PGP public key to use for encrypting the root token.
    type: str
  stored_shares:
    description:
      - Number of shares to store in the HSM for auto-unsealing.
      - B(UNTESTED)
    type: int
  recovery_shares:
    description:
      - Number of shares to split the recovery key into.
      - B(UNTESTED)
    type: int
  recovery_threshold:
    description:
      - Number of shares required to reconstruct the key.
      - B(UNTESTED)
    type: int
  recovery_pgp_keys:
    description:
      - A list of PGP public keys to use for encrypting the key shares.
      - B(UNTESTED)
    type: list
    elements: str
"""

EXAMPLES = """
- name: Initialize OpenBao
  flowerysong.openbao.init:
    secret_shares: 3
    secret_threshold: 2
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    OpenBaoClient,
    openbao_argument_spec,
)


def main():
    argspec = openbao_argument_spec()
    local_argspec = dict(
        secret_shares=dict(type='int', default=1, no_log=False),
        secret_threshold=dict(type='int', default=1, no_log=False),
        pgp_keys=dict(type='list', elements='str', no_log=False),
        root_token_pgp_key=dict(type='str', no_log=False),
        stored_shares=dict(type='int'),
        recovery_shares=dict(type='int'),
        recovery_threshold=dict(type='int'),
        recovery_pgp_keys=dict(type='list', elements='str', no_log=False),
    )
    argspec.update(local_argspec)

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = OpenBaoClient(module.params, module)

    if module.params['secret_threshold'] > module.params['secret_shares']:
        module.fail_json(msg='secret_threshold cannot be larger than secret_shares')

    if module.params['secret_shares'] > 1 and module.params['secret_threshold'] < 2:
        module.fail_json(msg='secret_threshold must be at least 2 when splitting a key, otherwise each share is equivalent to the full key')

    result = client.get('sys/init')

    if result['initialized']:
        module.exit_json(changed=False, **result)

    if module.check_mode:
        module.exit_json(changed=True)

    params = {}
    for p in local_argspec:
        if module.params[p] is not None:
            params[p] = module.params[p]

    result = client.put('sys/init', params)
    result.update(client.get('sys/init'))

    module.exit_json(changed=True, **result)


if __name__ == '__main__':
    main()
