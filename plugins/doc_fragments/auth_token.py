# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2022 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):
    DOCUMENTATION = """
options:
  token:
    description:
      - Authentication token to use.
      - If this is not set then the contents of C(~/.vault-token) will be checked.
    type: str
"""

    # Ansible doesn't currently support listing environment sources in modules,
    # so they need to be split out into a separate fragment. This also allows us
    # to add ini and vars as configuration sources.
    PLUGINS = """
options:
  token:
    env:
      - name: VAULT_TOKEN
    ini:
      - section: openbao
        key: token
    vars:
      - name: ansible_openbao_token
"""
