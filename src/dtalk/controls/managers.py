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
from PyQt5 import QtCore, QtWidgets

import dtalk.core.signals as serverSignals
import dtalk.models.signals as dbSignals
from dtalk.models import ReceivedMessage, Friend
import dtalk.utils.xdg as dtalkXdg
import dtalk.controls.utils as controlUtils

from dtalk.controls.qobject import QPropertyObject
from dtalk.controls.models import GroupModel, MessageModel
from dtalk.views.chat import ChatWindow
from dtalk.core.server import XMPPServer
from dtalk.controls.qobject import postGui
from dtalk.controls.notify import NotifyModel


logger = logging.getLogger("dtalk.controls.managers")


class CommonManager(QPropertyObject()):
    
    _ownerInfoSignal = QtCore.pyqtSignal()
    dbInitFinished = QtCore.pyqtSignal()
    
    def __init__(self):
        super(CommonManager, self).__init__()
        self.groupModel = GroupModel()
        self._ownerInfo = None
        dbSignals.db_init_finished.connect(self.on_db_init_finished)
        dbSignals.post_save.connect(self.on_post_save, sender=Friend)
    
    @QtCore.pyqtSlot(str, result="QVariant")
    def getModel(self, modelType):
        return self.groupModel
    
    @QtCore.pyqtSlot(str, result="QVariant")
    def getJidInfo(self, jid):
        return controlUtils.getJidInfo(jid)
        
    @QtCore.pyqtProperty("QVariant", notify=_ownerInfoSignal)
    def ownerInfo(self):
        if self._ownerInfo is None:
            self._ownerInfo = controlUtils.getJidInfo(dtalkXdg.OWNER_JID)
        return self._ownerInfo
    
    @ownerInfo.setter
    def ownerInfo(self, obj):
        self._ownerInfo = obj
        self._ownerInfoSignal.emit()
        
    @postGui()    
    def on_post_save(self, instance,  *args, **kwargs):    
        if instance.isSelf:
            self.ownerInfo = controlUtils.getJidInfo(instance)
            
    def on_db_init_finished(self, *args, **kwargs):        
        self.dbInitFinished.emit()
    
class ServerManager(QPropertyObject()):
    __qtprops__ = { "loginFailedReason" : "" }
    
    userLoginSuccessed = QtCore.pyqtSignal()
    userLoginFailed = QtCore.pyqtSignal(str)
    userRosterReceived = QtCore.pyqtSignal()
    userRosterStatusReceived = QtCore.pyqtSignal()
    
    def __init__(self):
        super(ServerManager, self).__init__()
        self._server = XMPPServer()
        serverSignals.user_login_successed.connect(self.on_user_login_successed)
        serverSignals.user_roster_received.connect(self.on_user_roster_received)
        serverSignals.user_roster_status_received.connect(self.on_user_friends_status_received)
        serverSignals.user_login_failed.connect(self.on_user_login_failed)
        
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
        
    def on_user_login_failed(self, reason, *args, **kwargs):    
        self.loginFailedReason = reason
        self.userLoginFailed.emit(reason)
        
class ControlManager(QPropertyObject()):        
    
    def __init__(self):
        super(ControlManager, self).__init__()
        self.chatWindowManager = dict()
        self.notifyModel = NotifyModel(self)
        dbSignals.post_save.connect(self.on_received_message, sender=ReceivedMessage)        
    
    @QtCore.pyqtSlot(str)
    def openChat(self, jid):
        if jid not in self.chatWindowManager:
            w = ChatWindow(model=self.createModel(jid), jid=jid)
            w.requestClose.connect(self.onChatWindowClose)
            w.setContextProperty("commonManager", commonManager)
            self.chatWindowManager[jid] = w
            w.show()
        else:    
            self.chatWindowManager[jid].raise_()
            
    def createModel(self, jid):        
        return MessageModel(to_jid=jid)
    
    @postGui()
    def on_received_message(self, sender, instance, created, update_fields, *args, **kwargs):
        if created:
            jid = instance.friend.jid
            if jid in self.chatWindowManager:
                w = self.chatWindowManager[jid]
                w.model.appendMessage(instance, received=True)
            else:    
                self.notifyModel.appendMessage(instance)
                
    @QtCore.pyqtSlot(result="QVariant")            
    def getNotifyModel(self):
        return self.notifyModel
    
    def onChatWindowClose(self):
        w = self.sender()
        jid = w.jid
        self.chatWindowManager.pop(jid)        
        w.requestClose.disconnect(self.onChatWindowClose)
        w.hide()
        w.close()
        w.deleteLater()        

        
serverManager = ServerManager()    
commonManager = CommonManager()
controlManager = ControlManager()
