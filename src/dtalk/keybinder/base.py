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

from PyQt5 import QtCore

class BaseBackend(QtCore.QObject):
    
    keyRelease = QtCore.pyqtSignal(object)    
    mouseMoved = QtCore.pyqtSignal(int, int)
    
    def __init__(self, check_key_event, *args, **kwargs):
        super(BaseBackend, self).__init__()
        self.check_key_event = check_key_event
        self.initial(*args, **kwargs)
        
    def initial(self, *args, **kwargs):    
        pass
    
    def parse_key(self, keys):
        raise NotImplementedError
    
    def response(self):
        raise NotImplementedError
    
    def emitKeyRelease(self, identifier):
        self.keyRelease.emit(identifier)
        
    def emitMouseMoved(self, x, y):    
        self.mouseMoved.emit(x, y)
