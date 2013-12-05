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

from dtalk.dispatch import Signal

user_login_successed = Signal(providing_args=['jid'])
user_login_failed = Signal(providing_args=['jid'])
user_logged_out = Signal(providing_args=['jid'])
user_roster_init_completed = Signal(providing_args=[])
user_roster_received = Signal(providing_args=[])
user_roster_status_received = Signal(providing_args=[])
server_disconnected = Signal(providing_args=[])

