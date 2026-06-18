#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2026 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: namespace
author: "Paul Arthur (@flowerysong)"
short_description: Manage an OpenBao namespace
description:
  - Manage an OpenBao namespace
version_added: 0.5.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
options:
  state:
    description:
      - Desired namespace state.
    type: str
    choices:
      - absent
      - present
    default: present
  path:
    description:
      - Namespace path
    type: str
    required: true
  custom_metadata:
    description:
      - A dictionary of arbitrary metadata that describes the namespace.
    type: dict
    default: {}
"""

EXAMPLES = """
- name: Create a namespace for the Necrobinder
  flowerysong.openbao.namespace:
    path: phylactery
    custom_medatata:
      business_owner: neow
"""

RETURN = """
"""

from urllib.error import URLError

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    OpenBaoClient,
    openbao_argument_spec,
    openbao_compare,
)


def main():
    argspec = openbao_argument_spec()
    local_argspec = dict(
        path=dict(type='str', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        custom_metadata=dict(type='dict', default={}),
    )
    argspec.update(local_argspec)

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = OpenBaoClient(module.params, module)

    path = f'sys/namespaces/{module.params["path"]}'

    try:
        result = client.get(path, fatal=False)['data']
    except URLError:
        result = {}

    changed = False

    if module.params['state'] == 'absent':
        if result:
            changed = True
            if not module.check_mode:
                client.delete(path)
        module.exit_json(changed=changed)

    config = {
        'custom_metadata': module.params['custom_metadata'],
    }

    diff = openbao_compare(config, result, ignore_keys=['id', 'locked', 'path', 'tainted', 'uuid'])
    if diff or not result:
        changed = True
        if not module.check_mode:
            client.post(path, config)

    if module.check_mode:
        result = config
    else:
        result = client.get(path)['data']

    module.exit_json(changed=changed, diff=diff, namespace=result)


if __name__ == '__main__':
    main()
