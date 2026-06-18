# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
name: kv
author: Paul Arthur (@flowerysong)
short_description: Lookup for OpenBao KV version 1 secrets
description:
  - Ansible lookup for OpenBao.
options:
  _terms:
    description:
      - Secrets to look up.
    required: True
  mount_point:
    description:
      - Path where the KV backend is mounted.
    default: secret
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.base.PLUGINS
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.auth_token.PLUGINS
"""

EXAMPLES = """
- name: Look up a secret
  debug:
    msg: The result is {{ lookup('flowerysong.openbao.kv', 'ping') }}
"""

RETURN = """
  _raw:
    description:
      - Secrets
    type: list
    elements: dict
"""

from ..plugin_utils.lookup import OpenBaoLookupBase


class LookupModule(OpenBaoLookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.init_options(variables=variables, direct=kwargs)
        self.config_client()

        mount = self.get_option('mount_point')
        terms = ['/'.join((mount, x)) for x in terms]

        return super().run(terms)
