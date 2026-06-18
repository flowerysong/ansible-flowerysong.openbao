# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
name: read
author: Paul Arthur (@flowerysong)
short_description: Simple lookup for OpenBao
description:
  - A simple lookup for OpenBao.
options:
  _terms:
    description: Paths to look up.
    required: True
  raw:
    description: Controls whether the entire API response is returned, or just the data.
    type: bool
    default: false
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.base.PLUGINS
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.auth_token.PLUGINS
"""

EXAMPLES = """
- name: Look up a standard secret
  debug:
    msg: The result is {{ lookup('flowerysong.openbao.read', 'secret/ping') }}

- name: Look up multiple secrets
  debug:
    msg: The results are {{ query('flowerysong.openbao.read', 'secret/ping', 'secret/penguin') }}

- name: Look up a K/V v2 secret's data
  debug:
    msg: The result is {{ lookup('flowerysong.openbao.read', 'secret/data/ping').data }}

- name: Get the entire raw response
  debug:
    msg: The result is {{ lookup('flowerysong.openbao.read', 'secret/config', raw=true) }}

- name: Use a variable to configure the lookup
  debug:
    msg: The result is {{ lookup('flowerysong.openbao.read', 'secret/ping', **hashi_conf) }}
  vars:
    hashi_conf:
      token: s.b5lmbxyphjvhcfesmdffqhun
      raw: true
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

        return super().run(terms)
