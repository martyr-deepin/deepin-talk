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

from dtalk.models.signals import post_save, post_delete, db_init_finished
from dtalk.models import Resource, Friend, Group, SendedMessage, common_db, UserHistory, check_common_db_inited
from dtalk.controls.base import AbstractWrapperModel, peeweeWrapper
from dtalk.controls.qobject import postGui
from dtalk.cache import avatarManager
import dtalk.cache.signals as cache_signals
import dtalk.xmpp.signals as xmpp_signals
import dtalk.controls.utils as controlUtils


class GroupModel(AbstractWrapperModel):    
    other_fields = ("friendModel",)
    
    def initial(self, *args, **kwargs):
        xmpp_signals.user_roster_received.connect(self._on_roster_received)
        
    @postGui()    
    def _on_roster_received(self, *args, **kwargs):    
        if self.db_is_created:
            self.initData()    
    
    def load(self):
        return Group.select()
    
    @classmethod
    def attach_attrs(cls, instance):
        friend_model = FriendModel(group_id=instance.id)
        setattr(instance, "friendModel", friend_model)
        

class FriendModel(AbstractWrapperModel):        
    other_fields = ("resource", "avatar")
    ownerObj = None
        
    '''
    load(): select data from the database of interest
    init_signals: after the first call initData(), its initial
    '''
    
    def initial(self, group_id=None, *args, **kwargs):
        self.group_id = group_id
        self.initData()    
        self.init_signals()
    
    def load(self):
        kwargs = dict(subscription="both", isSelf=False)
        if self.group_id is not None:
            kwargs["group"] = self.group_id
        friends = Friend.filter(**kwargs)
        return friends
        
    def init_signals(self):    
        post_save.connect(self.on_post_save, sender=Resource, dispatch_uid=str(id(self)))
        post_delete.connect(self.on_post_delete, sender=Resource, dispatch_uid=str(id(self)))
        post_save.connect(self.on_post_save, sender=Friend, dispatch_uid=str(id(self)))
        post_delete.connect(self.on_post_delete, sender=Friend, dispatch_uid=str(id(self)))
        cache_signals.avatar_saved.connect(self.on_avatar_saved, dispatch_uid=str(id(self)))
        
    def update_changed(self, instance, update_fields):    
        obj = self.get_obj_by_jid(instance.jid)
        if not obj:
            return
        if update_fields and isinstance(update_fields, list):
            for key in update_fields:            
                setattr(obj, key, getattr(instance, key, None))
                
    @postGui()    
    def on_post_save(self, sender, instance, created, update_fields, *args, **kwargs):
        if sender == Friend:
            if not self.verify(instance):
                return 
            if created:
                obj = self.wrapper_instance(instance)                
                self.append(obj)
            else:    
                self.update_changed(instance, update_fields)
                
    @postGui()            
    def on_post_delete(self, sender, instance, *args, **kwargs):
        pass
    
    def verify(self, instance):
        return instance.subscription == "both" and instance.isSelf == False and self.group_id == instance.group.id
    
    def get_obj_by_jid(self, jid):
        ret = None
        for obj in self._data:
            if obj.jid == jid:
                ret = obj
                break
        return ret
    
    @classmethod
    def attach_attrs(cls, instance):
        resources = sorted(instance.resources, key=lambda item: item.priority, reverse=True)
        if len(resources) >= 1:
            resource = resources[0]
        else:    
            resource = Resource.get_dummy_data()
        avatar = avatarManager.get_avatar(instance.jid)    
        setattr(instance, "avatar", avatar)
        setattr(instance, "resource", resource)                    
    
    @postGui()
    def on_avatar_saved(self, sender, jid, path, *args, **kwargs):
        ret = self.get_obj_by_jid(jid)
        if ret:
            ret.avatar = path

            
class MessageModel(AbstractWrapperModel):
    other_fields = ("type", "successed", "readed")
    _jidInfoSignal = QtCore.pyqtSignal()
    
    def initial(self, to_jid):
        self.to_jid = to_jid
        self._jidInfo = None
        self.init_signals()
        
    def init_signals(self):    
        post_save.connect(self.on_sended_message, sender=SendedMessage)
        post_save.connect(self.on_userinfo_changed, sender=Friend)
    
    @postGui()
    def on_sended_message(self, sender, instance, created, update_fields, *args, **kwargs):    
        if created:
            self.appendMessage(instance)
    
    def appendMessage(self, instance, received=False):
        if not self.verify(instance):
            return
        obj = self.wrapper_instance(instance)
        self.append(obj)
        
        if received:
            if hasattr(instance, "readed"):
                if instance.readed != True:
                    instance.readed = True
                    instance.save(update_fields=["readed"])
        
    def verify(self, instance):    
        return instance.friend.jid == self.to_jid
    
    @classmethod
    def attach_attrs(cls, instance):
        if isinstance(instance, SendedMessage):
            setattr(instance, "readed", True)
        else:    
            setattr(instance, "successed", True)
        setattr(instance, "type", instance.TYPE)    
        strCreated = instance.created.strftime("%H:%M:%S")
        instance.created = strCreated

        
    @QtCore.pyqtSlot(str)
    def postMessage(self, body):
        SendedMessage.send_message(self.to_jid, body)        
            
    @QtCore.pyqtProperty("QVariant", notify=_jidInfoSignal)
    def jidInfo(self):
        if self._jidInfo is None:
            self._jidInfo = controlUtils.getJidInfo(self.to_jid)
        return self._jidInfo    
    
    @jidInfo.setter
    def jidInfo(self, obj):
        self._jidInfo = obj
        self._jidInfoSignal.emit()
    
    @postGui()    
    def on_userinfo_changed(self, instance, *args, **kwargs):
        if instance.jid == self.to_jid:
            self.jidInfo = controlUtils.getJidInfo(instance)
            
            
class UserHistoryModel(AbstractWrapperModel):            
    _db = None
    
    def initial(self):
        if check_common_db_inited():
            self.initData()
        else:    
            db_init_finished.connect(self._on_common_db_inited, sender=common_db)
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

