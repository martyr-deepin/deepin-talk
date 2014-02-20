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

from dtalk.models import Friend
from dtalk.controls.base import get_qobject_wrapper
from dtalk.cache import avatarManager
from dtalk.utils.six import string_types

def getFriend(obj):
    if hasattr(obj, "friend"):
        return obj.friend
    return obj

def getDisplayName(obj):
    instance = getFriend(obj)
    if instance.remark:
        return instance.remark
    if instance.nickname:
        return instance.nickname
    return instance.jid
    
