#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2026 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: namespace_info
author: "Paul Arthur (@flowerysong)"
short_description: List namespaces within OpenBao
description:
  - List namespaces within OpenBao.
version_added: 0.5.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
"""

EXAMPLES = """
- flowerysong.openbao.namespace_info:
  register: result
"""

RETURN = """
"""

from urllib.error import URLError

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

    ns = {}
    try:
        result = client.list('sys/namespaces', fatal=False)
    except URLError as e:
        if getattr(e, 'code', 0) != 404:
            raise
    else:
        ns = result['data']['key_info']

    module.exit_json(changed=False, namespaces=ns)


if __name__ == '__main__':
    main()
