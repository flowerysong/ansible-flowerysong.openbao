#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: auth_method
author: "Paul Arthur (@flowerysong)"
short_description: Manage mounted authentication methods within OpenBao
description:
  - Manage mounted authentication methods within OpenBao.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.mount
options:
  token_type:
    description:
      - Type of token that should be returned.
      - C(default-service) and C(default-batch) set a default that can be
        overridden by the auth method, while C(service) and C(batch) take
        precedence over the auth method's preference.
    type: str
    choices:
        - default-service
        - default-batch
        - service
        - batch
    default: default-service
"""

EXAMPLES = """
"""

RETURN = """
"""

from ..module_utils.mount import OpenBaoMountModule


def main():
    module = OpenBaoMountModule(
        'sys/auth',
        extra_config=dict(
            token_type=dict(
                choices=[
                    'default-service',
                    'default-batch',
                    'service',
                    'batch',
                ],
                default='default-service',
            ),
        ),
    )

    module.run()


if __name__ == '__main__':
    main()
