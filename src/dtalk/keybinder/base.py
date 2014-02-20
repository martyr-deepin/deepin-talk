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

class BaseBackend(object):
    
    def __init__(self, keybinder, *args, **kwargs):
        self.keybinder = keybinder
        self.initial(*args, **kwargs)
        
    check_key_event = property(lambda self: self.keybinder.check_key_event)    
        
    def initial(self, *args, **kwargs):    
        pass
    
    def parse_key(self, keys):
        raise NotImplementedError
    
    def response(self):
        raise NotImplementedError
    
    def emitKeyRelease(self, identifier):
        self.keybinder.keyRelease.emit(identifier)
        
    def emitMouseMoved(self, x, y):    
        self.keybinder.mouseMoved.emit(x, y)
        
    def stop(self):    
        raise NotImplementedError

