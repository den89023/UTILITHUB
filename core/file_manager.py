# UtilHub - Central Utility Dashboard
# Copyright (C) 2026 den89023
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

import os

def get_scripts_list():
    scripts_dir = "scripts"
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
        return []
    return [f for f in os.listdir(scripts_dir) if f.endswith(".py")]
