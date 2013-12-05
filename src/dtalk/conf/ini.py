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


from dtalk.utils import pyini
from dtalk.conf.signals import value_changed

class NotifyIni(pyini.Ini):
    
    def set_var(self, key, value):
        keys = key.split("/", 1)
        if len(keys) != 2:
            raise KeyError("ini key error")
        super(NotifyIni, self).set_var(key, value)
        section, config = keys
        value_changed.send(sender=self, section=section, config=config, value=value)
        return True
