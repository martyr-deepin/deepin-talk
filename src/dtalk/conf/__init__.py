#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2014 Deepin, Inc.
#               2011 ~ 2014 Hou ShaoHui
# 
# Author:     Hou ShaoHui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from functools import partial
from dtalk.utils import xdg
# from dtalk.utils import pyini
from dtalk.conf.ini import NotifyIni

user_settings_file = xdg.get_config_path("settings.ini", check_exists=True)
settings = NotifyIni(os.path.join(xdg.get_parent_dir(__file__), "default_settings.ini"))
if user_settings_file:
    settings.read(filename=user_settings_file)
settings.write = partial(settings.save, filename=user_settings_file)

DEBUG = True
