#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2026 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: jwt_config
author: "Paul Arthur (@flowerysong)"
short_description: Manage JWT/OIDC authentication in OpenBao
description:
  - Manage JWT/OIDC authentication in OpenBao.
version_added: 0.5.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
  - flowerysong.openbao.token
options:
  mount_point:
    type: str
    default: jwt
    description:
      - Path under auth/ where the JWT backend is mounted.
  oidc_discovery_url:
    type: str
    description:
      - Base URL for OIDC discovery (without C(.well-known/openid-configuration))
      - Cannot be used with O(jwks_url) or O(jwt_validation_pubkeys).
  oidc_discovery_ca_pem:
    type: str
    description:
      - CA certificate or chain of certificates, in PEM format, to use to validate connections to the OIDC Discovery URL.
      - If not set, system certificates are used.
  oidc_client_id:
    type: str
    description: OAuth client ID.
  oidc_client_secret:
    type: str
    description: OAuth client secret.
  oidc_response_mode:
    type: str
    description:
      - Authentication method to use for the token endpoint.
    choices:
      - query
      - form_post
    default: query
  oidc_response_types:
    type: list
    description:
      - Response types to request.
    elements: str
    choices:
      - code
      - id_token
    default:
      - code
  jwks_url:
    type: str
    description:
      - JWKS URL to use to authenticate signatures.
      - Cannot be used with O(oidc_discovery_url) or O(jwt_validation_pubkeys).
  jwks_ca_pem:
    type: str
    description:
      - CA certificate or chain of certificates, in PEM format, to use to validate connections to the JWKS URL.
      - If not set, system certificates are used.
  jwt_validation_pubkeys:
    type: list
    description:
      - PEM-encoded public keys to use to authenticate signatures locally.
      - Cannot be used with O(oidc_discovery_url) or O(jwks_url).
    elements: str
  bound_issuer:
    type: str
    description:
      - Required value for the C(iss) field in the JWT.
  jwt_supported_algs:
    type: list
    elements: str
    description:
      - Supported signing algorithms.
      - When not set the default behaviour depends on whether the plugin is configured for OIDC or JWT authentication.
  default_role:
    type: str
    description:
      - Role to use if none is provided during login.
  provider_config:
    type: dict
    description:
      - Configuration options for provider-specific handling.
  override_allowed_server_names:
    type: list
    description:
      - Hostnames to accept when performing TLS validation. By default the TLS subject to match the hostname specified in the connection URL.
    elements: str
  namespace_in_state:
    type: bool
    description:
      - Pass the namespace in the OIDC state parameter instead of as a separate query parameter.
    default: true
  skip_jwks_validation:
    type: bool
    description:
      - Update the config even if the specified O(oidc_discovery_url) or O(jwks_url) cannot currently be validated.
    default: false
"""

EXAMPLES = """
- name: Configure OpenIDC authentication
  flowerysong.openbao.jwt_config:
    path: oidc
    oidc_discovery_url: https://auth.example.com/
    oidc_client_id: 0oDEAD60FF
    oidc_client_secret: FF06DAEDDEAD60FF

"""

RETURN = """
"""

from urllib.error import URLError

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    OpenBaoClient,
    openbao_argument_spec,
    openbao_compare,
    openbao_token_argument_spec,
)
from ..module_utils.module import (
    optspec_to_argspec,
    optspec_to_config,
)


def main():
    argspec = openbao_argument_spec()
    argspec.update(
        dict(
            mount_point=dict(
                default='jwt',
            ),
        )
    )

    optspec = openbao_token_argument_spec()
    optspec.update(
        dict(
            oidc_discovery_url=dict(),
            oidc_discovery_ca_pem=dict(),
            oidc_client_id=dict(),
            oidc_client_secret=dict(no_log=True),
            oidc_response_mode=dict(choices=['query', 'form_post'], default='query'),
            oidc_response_types=dict(type='list', elements='str', choices=['code', 'id_token'], default=['code']),
            jwks_url=dict(),
            jwks_ca_pem=dict(),
            jwt_validation_pubkeys=dict(type='list', elements='str'),
            bound_issuer=dict(),
            jwt_supported_algs=dict(type='list', elements='str'),
            default_role=dict(),
            provider_config=dict(type='dict'),
            override_allowed_server_names=dict(type='list', elements='str'),
            namespace_in_state=dict(type='bool', default=True),
            skip_jwks_validation=dict(type='bool', default=False),
        )
    )
    argspec.update(optspec_to_argspec(optspec))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        mutually_exclusive=[
            ('oidc_discovery_url', 'jwks_url', 'jwt_validation_pubkeys'),
        ],
        required_one_of=[
            ('oidc_discovery_url', 'jwks_url', 'jwt_validation_pubkeys'),
        ],
        required_by={
            'oidc_discovery_url': ('oidc_client_id', 'oidc_client_secret'),
        },
    )

    path = f'auth/{module.params["mount_point"]}/config'
    client = OpenBaoClient(module.params, module)

    try:
        config = client.get(path, fatal=False)['data']
    except URLError:
        config = {}

    new_config = optspec_to_config(optspec, module.params)

    changed = False
    # FIXME: how do we handle updating the client secret?
    diff = openbao_compare(config, new_config, ignore_keys=['skip_jwks_validation', 'status', 'oidc_client_secret', 'token_type'])
    if diff:
        changed = True
        if module.check_mode:
            config = new_config
        else:
            client.post(path, new_config)
            config = client.get(path)['data']

    module.exit_json(changed=changed, config=config, diff=diff)


if __name__ == '__main__':
    main()
