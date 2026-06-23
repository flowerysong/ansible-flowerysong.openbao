#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2026 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: aws_auth_config_client
author: "Paul Arthur (@flowerysong)"
short_description: Manage AWS authentication in OpenBao
description:
  - Manage AWS authentication in OpenBao.
version_added: 0.5.0
extends_documentation_fragment:
  - flowerysong.openbao.base
  - flowerysong.openbao.auth_token
options:
  mount_point:
    type: str
    default: aws
    description:
      - Path under auth/ where the AWS backend is mounted.
  access_key:
    type: str
    description:
      - Access key for AWS.
  secret_key:
    type: str
    description:
      - Secret key for AWS.
  endpoint:
    type: str
    description:
      - URL to override the default generated endpoint for making AWS EC2 API calls.
  iam_endpoint:
    type: str
    description:
      - URL to override the default generated endpoint for making AWS IAM API calls.
  sts_endpoint:
    type: str
    description:
      - URL to override the default generated endpoint for making AWS STS API calls.
  sts_region:
    type: str
    description:
      - Region for STS API calls.
  use_sts_region_from_client:
    type: bool
    default: true
    description:
      - Use the region from client requests to determine the STS endpoint, instead of a static value.
  iam_server_id_header_value:
    type: str
    description:
      - Value to require in the C(X-Vault-AWS-IAM-Server-ID) request header.
  allowed_sts_header_values:
    type: list
    elements: str
    description:
      - Additional headers that are allowed to be in AWS STS request headers.
  max_retries:
    type: int
    default: -1
    description:
      - Maximum number of retries for recoverable exceptions of AWS APIs.
      - V(-1) uses the AWS SDK's default.
"""

EXAMPLES = """
"""

RETURN = """
"""

from urllib.error import URLError

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    OpenBaoClient,
    openbao_argument_spec,
    openbao_compare,
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
                default='aws',
            ),
        )
    )

    optspec = dict(
        access_key=dict(no_log=True),
        secret_key=dict(no_log=True),
        endpoint=dict(),
        iam_endpoint=dict(),
        sts_endpoint=dict(),
        sts_region=dict(),
        use_sts_region_from_client=dict(type='bool', default=True),
        iam_server_id_header_value=dict(),
        allowed_sts_header_values=dict(type='list', elements='str'),
        max_retries=dict(type='int', default=-1),
    )
    argspec.update(optspec_to_argspec(optspec))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    path = f'auth/{module.params["mount_point"]}/config/client'
    client = OpenBaoClient(module.params, module)

    try:
        config = client.get(path, fatal=False)['data']
    except URLError:
        config = {}

    new_config = optspec_to_config(optspec, module.params)

    changed = False
    diff = openbao_compare(config, new_config, ignore_keys=['secret_key'])
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
