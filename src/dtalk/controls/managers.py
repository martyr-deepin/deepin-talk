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

# from dtalk.controls.models import 

from PyQt5 import QtCore
from dtalk.controls.qobject import QPropertyObject
from dtalk.controls.models import FriendModel
from dtalk.core.server import XMPPServer
import dtalk.core.signals as serverSignals

class ModelManager(QPropertyObject()):
    
    def __init__(self):
        super(ModelManager, self).__init__()
        
        self.friendModel = FriendModel()
    
    @QtCore.pyqtSlot(str, result="QVariant")
    def getModel(self, modelType):
        return self.friendModel
    
    
class ServerManager(QPropertyObject()):
    
    userLoginSuccessed = QtCore.pyqtSignal()
    userRosterReceived = QtCore.pyqtSignal()
    userRosterStatusReceived = QtCore.pyqtSignal()
    
    def __init__(self):
        super(ServerManager, self).__init__()
        self._server = XMPPServer()
        serverSignals.user_login_successed.connect(self.on_user_login_successed)
        serverSignals.user_roster_received.connect(self.on_user_roster_received)
        serverSignals.user_roster_status_received.connect(self.on_user_friends_status_received)
        
    @QtCore.pyqtSlot(str, str)    
    def login(self, jid, password):
        self._server.login(jid, password)
        
    def on_user_login_successed(self, sender, jid, *args, **kwargs):    
        self.userLoginSuccessed.emit()
        
    def on_user_roster_received(self, *args, **kwargs):    
        self.userRosterReceived.emit()
        
    def on_user_friends_status_received(self, *args, **kwargs):    
        self.userRosterStatusReceived.emit()
