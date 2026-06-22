#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2026 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: group_alias
author: "Paul Arthur (@flowerysong)"
short_description: Manage group aliases in OpenBao
description:
  - Manage group aliases in OpenBao.
version_added: 0.5.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
options:
  state:
    type: str
    choices:
      - present
      - absent
    default: present
    description:
      - Desired state of the alias.
  name:
    type: str
    required: true
    description:
     - Name of the alias.
  mount_accessor:
    type: str
    required: true
    description:
      - Mount that this alias belongs to.
  group_name:
    type: str
    required: true
    description:
      - Group that this is an alias to.
"""

EXAMPLES = """
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
    argspec.update(
        dict(
            state=dict(
                choices=['present', 'absent'],
                default='present',
            ),
            name=dict(required=True),
            group_name=dict(required=True),
            mount_accessor=dict(required=True),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = OpenBaoClient(module.params, module)

    try:
        group = client.get(f'identity/group/name/{module.params["group_name"]}', fatal=False)['data']
    except URLError:
        if module.params['state'] == 'absent':
            module.exit_json(changed=False)
        module.fail_json(f'Unable to find a group named "{module.params["group_name"]}"')

    changed = False

    if module.params['state'] == 'absent':
        if group.get('alias'):
            changed = True
            client.delete(f'identity/group-alias/id/{group["alias"]["id"]}')
        module.exit_json(changed=changed)

    result = group['alias']

    alias_config = {
        'name': module.params['name'],
        'mount_accessor': module.params['mount_accessor'],
        'canonical_id': group['id'],
    }

    diff = openbao_compare(
        alias_config,
        result,
        ignore_keys=('creation_time', 'id', 'last_update_time', 'merged_from_canonical_ids', 'metadata', 'mount_path', 'mount_type'),
    )

    if diff:
        changed = True
        if module.check_mode:
            result = alias_config
        else:
            result = client.post('identity/group-alias', alias_config)['data']
            result = client.get(f'identity/group-alias/id/{result["id"]}')['data']

    module.exit_json(changed=changed, diff=diff, group_alias=result)


if __name__ == '__main__':
    main()
