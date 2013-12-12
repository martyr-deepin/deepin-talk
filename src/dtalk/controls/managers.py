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

import logging
from PyQt5 import QtCore
from dtalk.controls.qobject import QPropertyObject
from dtalk.controls.models import GroupModel, MessageModel
from dtalk.views.chat import ChatWindow
from dtalk.core.server import XMPPServer
import dtalk.core.signals as serverSignals
import dtalk.models.signals as dbSignals
from dtalk.models import ReceivedMessage
from dtalk.controls.qobject import postGui
from dtalk.controls.notify import NotifyModel

logger = logging.getLogger("dtalk.controls.managers")

class ModelManager(QPropertyObject()):
    
    dbInitFinished = QtCore.pyqtSignal()
    
    def __init__(self):
        super(ModelManager, self).__init__()
        dbSignals.db_init_finished.connect(self.on_db_init_finished)
        self.groupModel = GroupModel()
    
    @QtCore.pyqtSlot(str, result="QVariant")
    def getModel(self, modelType):
        return self.groupModel
        
    def on_db_init_finished(self, *args, **kwargs):    
        self.dbInitFinished.emit()
    
    
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
        logger.info("-- [{0}] user login successed".format(jid))
        self.userLoginSuccessed.emit()
        
    def on_user_roster_received(self, *args, **kwargs):    
        self.userRosterReceived.emit()
        
    def on_user_friends_status_received(self, *args, **kwargs):    
        self.userRosterStatusReceived.emit()
        
class ControlManager(QPropertyObject()):        
    
    def __init__(self):
        super(ControlManager, self).__init__()
        self.chatWindowManager = dict()
        self.notifyModel = NotifyModel()
        dbSignals.post_save.connect(self.on_received_message, sender=ReceivedMessage)        
        
    
    @QtCore.pyqtSlot(str)
    def openChat(self, jid):
        if jid not in self.chatWindowManager:
            self.chatWindowManager[jid] = ChatWindow(model=self.createModel(jid))
            self.chatWindowManager[jid].show()
        else:    
            self.chatWindowManager[jid].raise_()
            
    def createModel(self, jid):        
        return MessageModel(to_jid=jid)
    
    @postGui()
    def on_received_message(self, sender, instance, created, update_fields, *args, **kwargs):
        if created:
            jid = instance.friend.jid
            if jid in self.chatWindowManager:
                self.chatWindowManager[jid].model.appendMessage(instance, received=True)
            else:    
                self.notifyModel.appendMessage(instance)
                
    @QtCore.pyqtSlot(result="QVariant")            
    def getNotifyModel(self):
        return self.notifyModel
    

serverManager = ServerManager()    
modelManager = ModelManager()
controlManager = ControlManager()
