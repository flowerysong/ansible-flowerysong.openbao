#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: engine
author: "Paul Arthur (@flowerysong)"
short_description: Manage secrets engines within OpenBao
description:
  - Manage mounted secrets engines within OpenBao.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.mount
"""

EXAMPLES = """
"""

RETURN = """
"""

from ..module_utils.mount import OpenBaoMountModule


def main():
    module = OpenBaoMountModule(
        'sys/mounts',
    )

    module.run()


if __name__ == '__main__':
    main()
