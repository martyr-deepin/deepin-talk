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

import threading
import weakref

from PyQt5 import QtCore
from dtalk.dispatch import saferef
from dtalk.keybinder.xutils import XlibBackend

WEAKREF_TYPES = (weakref.ReferenceType, saferef.BoundMethodWeakref)


class KeyBinder(threading.Thread, QtCore.QObject):
    
    keyRelease = QtCore.pyqtSignal(object)    
    mouseMoved = QtCore.pyqtSignal(int, int)
    
    def __init__(self):
        threading.Thread.__init__(self)
        QtCore.QObject.__init__(self)
        self.lock = threading.Lock()
        self.setDaemon(True)
        self.backend = XlibBackend(self)
        self.keyRelease.connect(self.on_key_release_event)
        self.receivers = {}
        
    def bind(self, key, receiver, weak=True):    
        key = self.backend.parse_key(key)
        if weak:
            receiver = saferef.safeRef(receiver, onDelete=self._remove_receiver)
        with self.lock:    
            self.receivers[key] = receiver
            
    def check_key_event(self, identifier):        
        with self.lock:
            if identifier in self.receivers:
                return True
            return False
    
    def unbind(self, key):
        key = self.backend.parse_key(key)
        with self.lock:
            if key in self.receivers:
                del self.receivers[key]
            
    def _remove_receiver(self, receiver):
        with self.lock:
            remove_key = None
            for key, connected_receiver in self.receivers.items():
                if connected_receiver == receiver:
                    remove_key = key
                    break
            if remove_key:    
                del self.receivers[remove_key]
                
    def run(self):            
        self.backend.response()
        
    def on_key_release_event(self, identifier):    
        if not self.receivers:
            return
        receiver = None
        with self.lock:
            if identifier in self.receivers:
                receiver = self.receivers[identifier]
                if isinstance(receiver, WEAKREF_TYPES):
                    receiver = receiver()
                        
        if receiver is not None and callable(receiver):            
            receiver()
            
keyBinder = KeyBinder()
