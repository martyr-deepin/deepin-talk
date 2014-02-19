#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2014 Deepin, Inc.
#               2011 ~ 2014 lovesnow
# 
# Author:     lovesnow <houshao55@gmail.com>
# Maintainer: lovesnow <houshao55@gmail.com>
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
from dtalk.controls.qobject import QObjectListModel, postGui

from dtalk.models import signals as dbSignals
from dtalk.models import Friend, Group
from dtalk.controls.utils import getDisplayName
from dtalk.cache.avatar import avatarManager
from dtalk.cache import signals as cacheSignals
from dtalk.xmpp import signals as xmppSignals

class GroupModel(QObjectListModel):
    
    nameRole = QtCore.Qt.UserRole + 1
    friendModelRole = QtCore.Qt.UserRole + 3
    
    _roles = {
        nameRole : "name",
        friendModelRole : "friendModel",
    }
    
    def __init__(self, parent=None):
        super(GroupModel, self).__init__(parent)
        self._initSignals()
        
    def _initSignals(self):    
        xmppSignals.user_roster_received.connect(self._onRosterReceived)
        
    def _initData(self):    
        groups = list(Group.select())
        for g in groups:
            setattr(g, "friendModel", FriendModel(parent=self, groupId=g.id))
        self.setAll(groups)    
                
    @postGui()    
    def _onRosterReceived(self, *args, **kwargs):    
        self._initData()

    def data(self, index, role):    
        if not index.isValid() or index.row() > self.size():
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:    
            return QtCore.QVariant()
        
        roleName = self._roles[role]

        if roleName == "name":
            return item.name
        elif roleName == "friendModel":
            return item.friendModel
        return QtCore.QVariant()
        

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
            return getDisplayName(item)
        return QtCore.QVariant()
    
    
        
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
    
