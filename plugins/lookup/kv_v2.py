# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
name: kv_v2
author: Paul Arthur (@flowerysong)
short_description: Lookup for OpenBao KV version 2
description:
  - Ansible lookup for OpenBao.
options:
  _terms:
    description:
      - Secrets to look up.
    required: True
  mount_point:
    description:
      - Path where the KV secrets engine is mounted
    default: secret
  version:
    description:
      - Requested version of the secret.
      - If not specified the latest version will be returned.
    type: int
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.base.PLUGINS
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.auth_token.PLUGINS
"""

EXAMPLES = """
- name: Look up a secret
  debug:
    msg: The result is {{ lookup('flowerysong.openbao.kv_v2', 'ping') }}

- name: Look up a specific version of a secret
  debug:
    msg: The result is {{ lookup('flowerysong.openbao.kv_v2', 'ping', version=2) }}
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
        version = self.get_option('version')
        version = f'?version={version}' if version else ''
        terms = [f'{mount}/data/{x}{version}' for x in terms]

        result = super().run(terms)
        return [x['data'] for x in result]
