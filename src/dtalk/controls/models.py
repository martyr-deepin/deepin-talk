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
logger = logging.getLogger("dtalk.controls.models")

import peewee as pw

from PyQt5 import QtCore

from dtalk.models import signals as dbSignals
from dtalk.models import (Friend, Group, SendedMessage, ReceivedMessage,
                          common_db, UserHistory, check_common_db_inited, disable_auto_commit)

from dtalk.controls.base import AbstractWrapperModel, peeweeWrapper
from dtalk.controls.qobject import postGui, QObjectListModel
from dtalk.cache import avatarManager
from dtalk.utils.threads import threaded

import dtalk.cache.signals as cacheSignals
import dtalk.xmpp.signals as xmppSignals
import dtalk.controls.utils as controlUtils


class GroupModel(AbstractWrapperModel):    
    other_fields = ("friendModel",)
    
    def initial(self, *args, **kwargs):
        xmppSignals.user_roster_received.connect(self._on_roster_received)
        
    @postGui()    
    def _on_roster_received(self, *args, **kwargs):    
        if self.db_is_created:
            self.initData()    
    
    def load(self):
        return Group.select()
    
    @classmethod
    def attach_attrs(cls, instance):
        friend_model = FriendModel(groupId=instance.id)
        setattr(instance, "friendModel", friend_model)
        
class FriendModel(QObjectListModel):
    jidRole = QtCore.Qt.UserRole + 1
    nicknameRole = QtCore.Qt.UserRole + 2
    remarkRole  = QtCore.Qt.UserRole + 3
    subscriptionRole  = QtCore.Qt.UserRole + 4
    groupRole = QtCore.Qt.UserRole + 5
    isSelfRole = QtCore.Qt.UserRole + 6
    displayNameRole = QtCore.Qt.UserRole + 7
    
    # extends
    avatarRole = QtCore.Qt.UserRole + 8
        
    _roles = {
        jidRole : "jid",
        nicknameRole : "nickname",
        remarkRole : "remark",
        subscriptionRole : "subscription",
        groupRole : "groupName",
        isSelfRole : "isSelf",
        avatarRole : "avatar",
        displayNameRole: "displayName",
    }
        
        
    def __init__(self, parent=None, groupId=None):
        super(FriendModel, self).__init__(parent)
        self.groupId = groupId        
        
        self._initSignals()
        self._initData()
        
    def _initSignals(self):    
        dbSignals.post_save.connect(self.onFriendPostSave, sender=Friend)
        dbSignals.post_delete.connect(self.onFriendPostDelete, sender=Friend)
        cacheSignals.avatar_saved.connect(self.onAvatarSaved, sender=Friend)
        
    def _initData(self):    
        kwargs = dict(subscription="both", isSelf=False)
        if self.groupId is not None:
            kwargs["group"] = self.groupId
        friends = list(Friend.filter(**kwargs))
        self.setAll(friends)
        
    @postGui()
    def onFriendPostSave(self, instance, created, update_fields, *args, **kwargs):    
        
        # verity instance
        if not self.verify(instance):        
            return 
        
        if created:
            self.append(instance)
        else:    
            self.replace(instance)
            
    @postGui()        
    def onFriendPostDelete(self, instance, *args, **kwargs):
        try:
            self.remove(instance)
        except: pass    
    
    @postGui()
    def onAvatarSaved(self, jid, path):
        ret = self.getObjByJid(jid)
        if ret:
            _, index = ret
            self.itemChange(index)
        
    def getObjByJid(self, jid):    
        for index, obj in enumerate(self._data):
            if obj.jid == jid:
                return (obj, index)
        return None    
                
    def verify(self, instance):    
        return instance.subscription == "both" and instance.isSelf == False and self.groupId == instance.group.id
        
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size():
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:    
            return QtCore.QVariant()
        
        roleName = self._roles[role]
        if hasattr(item, roleName):
            return getattr(item, roleName)
        elif roleName == "groupName":
            return item.group.name
        elif roleName == "avatar":
            return avatarManager.get_avatar(item.jid)
        elif roleName == "displayName":
            return controlUtils.getDisplayName(item)
        return QtCore.QVariant()

            
class MessageModel(QObjectListModel):
    _jidInfoSignal = QtCore.pyqtSignal()
    
    typeRole = QtCore.Qt.UserRole + 1
    successedRole = QtCore.Qt.UserRole + 2
    readedRole = QtCore.Qt.UserRole + 3
    bodyRole  = QtCore.Qt.UserRole + 4
    createdRole = QtCore.Qt.UserRole + 5
    
    _roles = {
        typeRole : "type",
        successedRole : "successed",
        readedRole : "readed",
        bodyRole : "body",
        createdRole : "published"
    }
    
    def __init__(self, toJid, loadMessages=False, parent=None):
        super(MessageModel, self).__init__(parent)
        self._toJid = toJid
        self._jidInfo = None
        self._initSignals()
        if loadMessages:
            self.loadUnreadedMessages()
        
    def _initSignals(self):    
        dbSignals.post_save.connect(self.onSendedMessage, sender=SendedMessage)
        dbSignals.post_save.connect(self.onUserinfoChanged, sender=Friend)
        
    def data(self, index, role):    
        if not index.isValid() or index.row() > self.size():
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:    
            return QtCore.QVariant()
        
        roleName = self._roles[role]
        if hasattr(item, roleName):
            return getattr(item, roleName)
        elif roleName == "published":
            return item.created.strftime("%H:%M:%S")
        return QtCore.QVariant()
        
    def loadUnreadedMessages(self):
        qs = ReceivedMessage.select().where(ReceivedMessage.readed==False,
                                            ReceivedMessage.friend==Friend.get(jid=self._toJid))
        objs = list(qs)
        self.setAll(objs)
        with disable_auto_commit():
            for obj in objs:
                if obj.readed != True:
                    obj.readed = True
                    obj.save(update_fields=['readed'])
        
    @postGui()
    def onSendedMessage(self, sender, instance, created, update_fields, *args, **kwargs):    
        if created:
            self.appendMessage(instance)
    
    def appendMessage(self, instance, received=False):
        if not self.verify(instance):
            return
        
        self.append(instance)
        
        if received:
            if hasattr(instance, "readed"):
                if instance.readed != True:
                    instance.readed = True
                    instance.save(update_fields=["readed"])
        
    def verify(self, instance):    
        return instance.friend.jid == self._toJid
        
    @QtCore.pyqtSlot(str)
    def postMessage(self, body):
        SendedMessage.send_message(self._toJid, body)        
            
    @QtCore.pyqtProperty("QVariant", notify=_jidInfoSignal)
    def jidInfo(self):
        if self._jidInfo is None:
            self._jidInfo = controlUtils.getJidInfo(self._toJid)
        return self._jidInfo    
    
    @jidInfo.setter
    def jidInfo(self, obj):
        self._jidInfo = obj
        self._jidInfoSignal.emit()
    
    @postGui()    
    def onUserinfoChanged(self, instance, *args, **kwargs):
        if instance.jid == self._toJid:
            self.jidInfo = controlUtils.getJidInfo(instance)
            
            
class UserHistoryModel(AbstractWrapperModel):            
    _db = None
    
    def initial(self):
        if check_common_db_inited():
            self.initData()
        else:    
            dbSignals.db_init_finished.connect(self._on_common_db_inited, sender=common_db)
        self._obj = None    
            
    @postGui()        
    def _on_common_db_inited(self, *args, **kwargs):        
        self.initData()
            
    def load(self):        
        return UserHistory.select()
    
    @QtCore.pyqtSlot(int)
    def removeByIndex(self, index):
        obj = self.get(index)
        dq = UserHistory.delete().where(UserHistory.id==obj.id)
        dq.execute()
        self.removeAt(index)
        
    @QtCore.pyqtSlot(str, result="QVariant")    
    def queryJid(self, jid):
        jid = jid.lower()
        jids = UserHistory.select().where(
            (pw.fn.Lower(pw.fn.Substr(UserHistory.jid, 1, len(jid))) == jid)
        )
        jids = list(jids)
        if len(jids) > 0:
            instance = jids[0]
            others = dict(selStart=len(jid), selEnd=len(instance.jid))
            self._obj = peeweeWrapper(jids[0], others)
            return self._obj
        return QtCore.QVariant()

