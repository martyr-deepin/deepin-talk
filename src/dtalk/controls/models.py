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

from dtalk.utils.six import string_types
from dtalk.models import signals as dbSignals
from dtalk.models import (Friend, Group, SendedMessage, ReceivedMessage,
                          common_db, UserHistory, check_common_db_inited, disable_auto_commit)

from dtalk.controls.base import AbstractWrapperModel, peeweeWrapper
from dtalk.controls.qobject import postGui, QPropertyObject, QInstanceModel
from dtalk.cache import avatarManager

import dtalk.cache.signals as cacheSignals
import dtalk.xmpp.signals as xmppSignals
import dtalk.controls.utils as controlUtils

def getJidInfo(jid):
    if not jid:
        return None
    
    if isinstance(jid, string_types):
        try:
            obj = Friend.get(jid=jid)
        except Friend.DoesNotExist:    
            return None
    else:    
        obj = jid
        
    return FriendWrapper(obj)    


class FriendWrapper(QPropertyObject()):
    
    __qtprops__ = {
        "jid" : "",
        "nickname" : "",
        "ramark" : "",
        "subscription" : "",
        "groupName" : "",
        "displayName" : "",
        "avatar" : "",
        "status" : "",
        "show" : "",
    }
    
    def __init__(self, instance, parent=None):
        super(FriendWrapper, self).__init__(parent)
        
        self.jid = instance.jid
        self.nickname = instance.nickname
        self.remark = instance.remark
        try:
            self.groupName = instance.group.name
        except:    
            self.groupName = ""
        
        self.avatar = avatarManager.get_avatar(self.jid)
        self.displayName = controlUtils.getDisplayName(instance)
        
        cacheSignals.avatar_saved.connect(self._onAvatarSaved)
        dbSignals.post_save.connect(self._onFriendPostSave, sender=Friend)
        xmppSignals.roster_changed_status.connect(self._onRosterChangedStatus)
        
    @postGui()            
    def _onAvatarSaved(self, jid, path, *args, **kwargs):    
        if jid == self.jid:
            self.avatar = path
            
    @postGui()        
    def _onFriendPostSave(self, instance, created, update_fields, *args, **kwargs):
        if not created and instance.jid == self.jid:
            for key in update_fields:
                setattr(self, key, getattr(instance, key, ""))
                
    @postGui()            
    def _onRosterChangedStatus(self, presence, *args, **kwargs):
        if self.jid == presence['from'].bare:
            self.status = presence['status']
            self.show = presence['show']

    def updateAvatar(self):    
        self.avatar = avatarManager.get_avatar(self.jid)
        
    def __eq__(self, other):    
        return self.jid == other.jid
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.jid)
    
class MessageWrapper(QPropertyObject()):    
        
    __qtprops__ = {
        "type_" : "",
        "successed" : True,
        "reaed" : False,
        "body" : "",
        "created" : ""
    }
    
    def __init__(self, instance, parent=None):
        super(MessageWrapper, self).__init__(parent)
        
        self._instance = instance
        self.type_ = instance.TYPE
        self.successed = getattr(instance, "successed", True)
        self.reaed = getattr(instance, "readed", False)
        self.body = instance.body
        self.created = instance.created.strftime("%H:%M:%S")
        
    def __eq__(self, other):    
        return self._instance.__class__ == other._instance.__class__ and self._instance.id == other._instance.id
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._instance.TYPE)

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
        
class FriendModel(QInstanceModel):
        
    def __init__(self, parent=None, groupId=None, initData=True):
        super(FriendModel, self).__init__(parent)
        self.groupId = groupId        
        
        self._initSignals()
        
        if initData:
            self._initData()
        
    def _initSignals(self):    
        dbSignals.post_save.connect(self.onFriendPostSave, sender=Friend)
        dbSignals.post_delete.connect(self.onFriendPostDelete, sender=Friend)
           
    def _initData(self):    
        kwargs = dict(subscription="both", isSelf=False)
        if self.groupId is not None:
            kwargs["group"] = self.groupId
        friends = list(map(lambda item: FriendWrapper(item), Friend.filter(**kwargs)))
        self.setAll(friends)
        
    @postGui()
    def onFriendPostSave(self, instance, created, update_fields, *args, **kwargs):    
        
        # verity instance
        if not self.verify(instance):        
            return 
        
        obj = FriendWrapper(instance)
        
        if created:
            self.append(obj)
            
    @postGui()        
    def onFriendPostDelete(self, instance, *args, **kwargs):
        obj = FriendWrapper(instance)
        try:
            self.remove(obj)
        except: pass    
    
    def getObjByJid(self, jid):    
        for index, obj in enumerate(self._data):
            if obj.jid == jid:
                return (obj, index)
        return None    
                
    def verify(self, instance):    
        return instance.subscription == "both" and instance.isSelf == False and self.groupId == instance.group.id

            
class MessageModel(QInstanceModel):
    _jidInfoSignal = QtCore.pyqtSignal()
    
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
        
    def loadUnreadedMessages(self):
        qs = ReceivedMessage.select().where(ReceivedMessage.readed==False,
                                            ReceivedMessage.friend==Friend.get(jid=self._toJid))
        objs = map(lambda item: MessageWrapper(item), qs)
        self.setAll(objs)
        with disable_auto_commit():
            for ins in qs:
                if ins.readed != True:
                    ins.readed = True
                    ins.save(update_fields=['readed'])
        
    @postGui()
    def onSendedMessage(self, sender, instance, created, update_fields, *args, **kwargs):    
        if created:
            self.appendMessage(instance)
    
    def appendMessage(self, instance, received=False):
        if not self.verify(instance):
            return
        
        self.append(MessageWrapper(instance))
        
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
            self._jidInfo = getJidInfo(self._toJid)
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

