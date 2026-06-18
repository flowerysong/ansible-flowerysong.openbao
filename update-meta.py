#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: © 2021 Paul Arthur
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import copy
import json
import os
import subprocess

import yaml


runtime = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'meta/runtime.yml')

with open(runtime, 'r') as f:
    old = yaml.safe_load(f)

res = subprocess.run(['ansible-doc', '-t', 'module', '-l', 'flowerysong.openbao', '-j'], capture_output=True, text=True)

modules = list(json.loads(res.stdout))

new = copy.deepcopy(old)

new['action_groups'] = {
    'openbao': modules,
}

print(yaml.dump(new, indent=2))

if old != new:
    with open(runtime, 'w') as f:
        f.write(yaml.dump(new, indent=2))
