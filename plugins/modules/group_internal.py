#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2026 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: group_internal
author: "Paul Arthur (@flowerysong)"
short_description: Manage an OpenBao group
description:
  - Manage an OpenBao group
version_added: 0.5.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
options:
  name:
    description:
      - Name of the group to manage.
    type: str
    required: true
  state:
    description:
      - Desired state of the group.
    type: str
    choices:
      - present
      - absent
    default: present
  metadata:
    description:
      - A dictionary of arbitrary metadata that describes the group.
    type: dict
    default: {}
  policies:
    type: list
    elements: str
    description:
      - List of policies tied to the group.
    default: []
  member_group_ids:
    type: list
    elements: str
    description:
      - Group IDs of subgroups.
    default: []
  member_entity_ids:
    type: list
    elements: str
    description:
      - Entity IDs of members.
    default: []
"""

EXAMPLES = """
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    OpenBaoClient,
    openbao_argument_spec,
)

from ..module_utils.module import (
    OpenBaoModule,
    optspec_to_argspec,
)


class GroupModule(OpenBaoModule):
    def __init__(self, optspec, **kwargs):
        _argspec = openbao_argument_spec()
        _argspec.update(
            dict(
                name=dict(
                    required=True,
                ),
                state=dict(
                    choices=['present', 'absent'],
                    default='present',
                ),
            )
        )
        self.optspec = optspec
        _argspec.update(optspec_to_argspec(optspec))

        self.module = AnsibleModule(
            supports_check_mode=True,
            argument_spec=_argspec,
            **kwargs,
        )
        self.params = self.module.params
        self.params['mount_point'] = 'identity'
        self.client = OpenBaoClient(self.params, self.module)


def main():
    optspec = dict(
        metadata=dict(type='dict', default={}),
        policies=dict(type='list', elements='str', default=[]),
        member_group_ids=dict(type='list', elements='str', default=[]),
        member_entity_ids=dict(type='list', elements='str', default=[]),
    )

    module = GroupModule(
        optspec=optspec,
    )

    module.run(
        path_fmt='identity/group/name/{1}',
        config=dict(type='internal'),
        result_key='group',
        bad_keys=('id', 'creation_time', 'last_update_time', 'modify_index', 'namespace_id', 'name'),
    )


if __name__ == '__main__':
    main()
