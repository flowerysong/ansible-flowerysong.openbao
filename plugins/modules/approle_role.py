#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: approle_role
author: "Paul Arthur (@flowerysong)"
short_description: Manage AppRole roles in OpenBao
description:
  - Manage AppRole roles in OpenBao.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.role
  - flowerysong.openbao.token
options:
  mount_point:
    default: approle
  bind_secret_id:
    type: bool
    default: true
    description:
      - Whether a SecretID is required to authenticate.
  secret_id_bound_cidrs:
    type: list
    elements: str
    default: []
    description:
      - CIDR blocks that are allowed to authenticate.
  secret_id_num_uses:
    type: int
    default: 0
    description:
      - Number of times any particular SecretID can be used to authenticate.
      - C(0) is unlimited.
  secret_id_ttl:
    type: int
    default: 0
    description:
      - Duration in seconds after which a SecretID expires.
"""

EXAMPLES = """
"""

RETURN = """
"""

from ..module_utils.base import openbao_token_argument_spec
from ..module_utils.module import OpenBaoModule


class AppRoleModule(OpenBaoModule):
    def mangle_result(self, result):
        if not self.module.check_mode:
            result.update(self.client.get(self._path + '/role-id')['data'])
        return result


def main():
    argspec = dict(
        mount_point=dict(
            default='approle',
        ),
    )

    optspec = openbao_token_argument_spec()

    optspec.update(
        dict(
            bind_secret_id=dict(
                type='bool',
                default=True,
            ),
            secret_id_bound_cidrs=dict(
                type='list',
                elements='str',
                default=[],
                no_log=False,
            ),
            secret_id_num_uses=dict(
                type='int',
                default=0,
                no_log=False,
            ),
            secret_id_ttl=dict(
                type='int',
                default=0,
                no_log=False,
            ),
        )
    )

    module = AppRoleModule(
        argspec=argspec,
        optspec=optspec,
    )

    module.run(
        path_fmt='auth/{0}/role/{1}',
        config=dict(),
        bad_keys=['local_secret_ids'],
    )


if __name__ == '__main__':
    main()
