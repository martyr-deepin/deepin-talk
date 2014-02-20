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
import dtalk.models.signals as dbSignals
from dtalk.models import ReceivedMessage, Friend

import dtalk.utils.xdg as dtalkXdg
import dtalk.controls.utils as controlUtils

from dtalk.controls.qobject import QPropertyObject
from dtalk.controls.models import GroupModel, MessageModel, UserHistoryModel, getJidInfo
from dtalk.views.chat import ChatWindow

from dtalk.controls.qobject import postGui
from dtalk.controls.notify import NotifyModel

from dtalk.xmpp.base import AsyncClient
from dtalk.xmpp import signals as xmppSignals


logger = logging.getLogger("dtalk.controls.managers")


class CommonManager(QPropertyObject()):
    
    _ownerInfoSignal = QtCore.pyqtSignal()
    dbInitFinished = QtCore.pyqtSignal()
    
    def __init__(self):
        super(CommonManager, self).__init__()
        self.groupModel = GroupModel()
        self._userHistoryModel = UserHistoryModel(self)
        self._ownerInfo = None
        dbSignals.db_init_finished.connect(self.on_db_init_finished)
        dbSignals.post_save.connect(self.on_post_save, sender=Friend)
    
    @QtCore.pyqtSlot(str, result="QVariant")
    def getModel(self, modelType):
        if modelType == "group":
            return self.groupModel
        elif modelType == "userHistory":
            return self._userHistoryModel
        return self.groupModel
    
    @QtCore.pyqtSlot(str, result="QVariant")
    def getJidInfo(self, jid):
        return getJidInfo(jid)
        
    @QtCore.pyqtProperty("QVariant", notify=_ownerInfoSignal)
    def ownerInfo(self):
        if self._ownerInfo is None:
            self._ownerInfo = getJidInfo(dtalkXdg.OWNER_JID)
        return self._ownerInfo
    
    @ownerInfo.setter
    def ownerInfo(self, obj):
        self._ownerInfo = obj
        self._ownerInfoSignal.emit()
        
    @postGui()    
    def on_post_save(self, instance,  *args, **kwargs):    
        if instance.isSelf:
            self.ownerInfo = getJidInfo(instance)
            
    def on_db_init_finished(self, *args, **kwargs):        
        self.dbInitFinished.emit()
    
class SessionManager(QPropertyObject()):
    __qtprops__ = { "loginFailedReason" : "" }
    
    userLoginSuccessed = QtCore.pyqtSignal()
    userLoginFailed = QtCore.pyqtSignal(str)
    userRosterReceived = QtCore.pyqtSignal()
    userRosterStatusReceived = QtCore.pyqtSignal()
    
    def __init__(self):
        super(SessionManager, self).__init__()
        
        xmppSignals.auth_successed.connect(self.on_user_login_successed)
        xmppSignals.auth_failed.connect(self.on_user_login_failed)        
        xmppSignals.user_roster_received.connect(self.on_user_roster_received)
        xmppSignals.user_roster_status_received.connect(self.on_user_friends_status_received)

        # self.client = None
        self.client = AsyncClient()
        
        
    @QtCore.pyqtSlot(str, str, bool, bool, str)
    def login(self, jid, password, remember, autoLogin, status):
        # self.client = BaseClient(jid, password)
        # self.client.run_service()
        self.client.action_login(jid, password, remember, autoLogin, status)
        self.client.start()
        
    def on_user_login_failed(self, *args, **kwargs):    
        self.userLoginFailed.emit("linux")
        
    def on_user_login_successed(self, *args, **kwargs):    
        self.userLoginSuccessed.emit()
        
    def on_user_roster_received(self, *args, **kwargs):    
        self.userRosterReceived.emit()
       
    def on_user_friends_status_received(self, *args, **kwargs):    
        self.userRosterStatusReceived.emit()
        
    def disconnect(self):    
        try:
            self.client.action_logout()
        except:    
            pass
        
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
        return MessageModel(toJid=jid)
    
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

        
# serverManager = ServerManager()    
sessionManager = SessionManager()
commonManager = CommonManager()
controlManager = ControlManager()
