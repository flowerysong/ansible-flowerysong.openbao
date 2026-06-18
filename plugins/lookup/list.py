# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
name: list
author: Paul Arthur (@flowerysong)
short_description: Lookup for OpenBao
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
- name: List secrets
  debug:
    msg: The results are {{ lookup('flowerysong.openbao.list', 'secret/') }}
"""

RETURN = """
  _raw:
    description:
      - Secrets
    type: list
    elements: dict
"""

from urllib.error import URLError

from ansible.errors import AnsibleError
from ansible.utils.display import Display

from ..plugin_utils.lookup import OpenBaoLookupBase

display = Display()


class LookupModule(OpenBaoLookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.init_options(variables=variables, direct=kwargs)
        self.config_client()

        ret = []

        for term in terms:
            display.debug(f'flowerysong.openbao lookup term: {term}')

            try:
                secret = self.client.list(term)
            except URLError as e:
                raise AnsibleError('Unable to list endpoint') from e

            display.vvvv(f'flowerysong.openbao lookup found {secret}')

            if not secret:
                raise AnsibleError(f'No data from endpoint "{term}"')

            if self.get_option('raw'):
                ret.append(secret)
            else:
                ret.extend(secret['data']['keys'])

        return ret
