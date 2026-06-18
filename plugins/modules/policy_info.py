#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: policy_info
author: "Paul Arthur (@flowerysong)"
short_description: List ACLs within OpenBao
description:
  - List ACLs within OpenBao.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
"""

EXAMPLES = """
- flowerysong.openbao.policy_info:
  register: result
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

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = OpenBaoClient(module.params, module)
    result = client.list('sys/policies/acl')
    module.exit_json(changed=False, policies=result['data']['keys'])


if __name__ == '__main__':
    main()
