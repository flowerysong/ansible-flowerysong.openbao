#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2026 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: jwt_role_oidc
author: "Paul Arthur (@flowerysong)"
short_description: Manage OIDC authentication roles in OpenBao
description:
  - Manage OIDC authentication roles in OpenBao.
version_added: 0.5.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.role
  - flowerysong.openbao.token
options:
  mount_point:
    default: oidc
  bound_audiences:
    type: list
    elements: str
    description:
      - List of C(aud) claims to match against.
  user_claim:
    type: str
    description:
      - The claim to use to uniquely identify the user; this will be used as the name for the Identity entity alias created after successful login.
      - Required if O(state=present).
  user_claim_json_pointer:
    type: bool
    description:
      - Enable JSON Pointer syntax for O(user_claim).
    default: false
  bound_subject:
    type: str
    description:
      - Required value for the C(sub) claim.
  bound_claims:
    type: dict
    description:
      - Claims to match against specified values.
      - Keys support JSON pointer syntax for referencing claims.
      - The expected value can be a single string or a list of strings.
      - The interpretation of the values is configured with O(bound_claims_type).
  bound_claims_type:
    type: str
    description:
      - Matching mode used for O(bound_claims) values.
    choices:
      string: Exact match.
      glob: Wildcard matching with C(*) matching any number of characters.
    default: string
  groups_claim:
    type: str
    description:
      - The claim that identifies the set of groups to which the user belongs;
        this will be used as the names for the Identity group aliases created
        due to a successful login. The claim value must be a list of strings.
      - Supports JSON pointer syntax for referencing claims.
  claim_mappings:
    type: dict
    description:
      - Map claims to specified metadata fields.
      - Supports JSON pointer syntax for referencing claims.
  oauth2_metadata:
    type: list
    elements: str
    description:
      - Which tokens from the OIDC provider to return in metadata.
      - These tokens can potentially include sensitive security information.
    choices:
      - access_token
      - id_token
      - refresh_token
  oidc_scopes:
    type: list
    elements: str
    description:
      - OIDC scopes to request. C(openid) is always requested and does not need to be included here.
  allowed_redirect_uris:
    type: list
    elements: str
    description:
      - Allowed values for C(redirect_uri) during OIDC logins.
      - Required if O(state=present).
  callback_mode:
    type: str
    description:
      - Callback mode for the OIDC provider.
    choices:
      client: callback through the client
      direct: callback to the OpenBao server
      device: no callback
    default: client
  poll_interval:
    type: int
    description:
      - Poll interval in seconds for device and direct callback modes.
  oidc_disable_confirmation:
    type: bool
    description:
      - Disable the interactive confirmation page displayed in direct callback mode.
    default: false
  verbose_oidc_logging:
    type: bool
    description:
      - Enable logging of received OIDC tokens and claims when debug-level
        logging is active. This can expose sensitive information in the logs.
    default: false
  max_age:
    type: int
    description:
      - The allowable elapsed time in seconds since the last time the user was
        actively authenticated with the OIDC provider.
  token_policies_template_claims:
    type: bool
    description:
      - Enable Go templating for entries in O(token_policies). Templates which
        evaluate to the empty string are removed and all referenced claims must
        exist on the authenticating token.
    default: false
"""

EXAMPLES = """
"""

RETURN = """
"""

from ..module_utils.base import openbao_token_argument_spec
from ..module_utils.module import OpenBaoModule


def main():
    argspec = dict(
        mount_point=dict(
            default='oidc',
        ),
    )

    optspec = openbao_token_argument_spec()

    optspec.update(
        dict(
            bound_audiences=dict(
                type='list',
                elements='str',
            ),
            user_claim=dict(),
            user_claim_json_pointer=dict(type='bool', default=False),
            bound_subject=dict(),
            bound_claims=dict(type='dict'),
            bound_claims_type=dict(choices=('string', 'glob'), default='string'),
            groups_claim=dict(),
            claim_mappings=dict(type='dict'),
            oauth2_metadata=dict(type='list', elements='str', choices=['access_token', 'id_token', 'refresh_token']),
            oidc_scopes=dict(type='list', elements='str'),
            allowed_redirect_uris=dict(type='list', elements='str'),
            callback_mode=dict(choices=('client', 'direct', 'device'), default='client'),
            poll_interval=dict(type='int'),
            oidc_disable_confirmation=dict(type='bool', default=False),
            verbose_oidc_logging=dict(type='bool', default=False),
            max_age=dict(type='int'),
            token_policies_template_claims=dict(type='bool', default=False),
        )
    )

    module = OpenBaoModule(
        argspec=argspec,
        optspec=optspec,
        required_if=[
            ['state', 'present', ['allowed_redirect_uris', 'user_claim']],
        ],
    )

    module.run(
        path_fmt='auth/{0}/role/{1}',
        config=dict(role_type='oidc'),
    )


if __name__ == '__main__':
    main()
