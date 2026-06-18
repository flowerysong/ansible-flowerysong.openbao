#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: read
author: "Paul Arthur (@flowerysong)"
short_description: Read something from OpenBao
description:
  - Read data from OpenBao. This can be used to read secrets, get
    configuration details, etc.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
options:
  path:
    description:
      - Path to retrieve from the OpenBao server.
    type: str
    required: true
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


def main():
    argspec = openbao_argument_spec()
    argspec.update(
        dict(
            path=dict(
                required=True,
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = OpenBaoClient(module.params, module)

    result = client.get(module.params['path'])

    module.exit_json(changed=False, result=result)


if __name__ == '__main__':
    main()
