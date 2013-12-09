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

from dtalk.models.signals import post_save, post_delete
from dtalk.models import Resource, Friend, Group
from dtalk.controls.base import AbstractWrapperModel        
from dtalk.controls.qobject import postGui
from dtalk.cache import avatarManager
import dtalk.cache.signals as cache_signals
import dtalk.core.signals as server_signals


class GroupModel(AbstractWrapperModel):    
    other_fields = ("friendModel",)
    
    def initial(self, *args, **kwargs):
        server_signals.user_roster_status_received.connect(self._on_roster_received)
        
    @postGui(inclass=True)    
    def _on_roster_received(self, *args, **kwargs):    
        if self.db_is_created:
            self.initData()    
    
    def load(self):
        return Group.select()
    
    def attach_attrs(self, instance):
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
        print id(self), "#####"
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
                
    @postGui(inclass=True)    
    def on_post_save(self, sender, instance, created, update_fields, *args, **kwargs):
        if sender == Friend:
            print self.group_id, instance.group.id
            if not self.verify(instance):
                return 
            if created:
                obj = self.wrapper_instance(instance)                
                self.append(obj)
            else:    
                self.update_changed(instance, update_fields)
                
    @postGui(inclass=True)            
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
    
    def attach_attrs(self, instance):
        resources = sorted(instance.resources, key=lambda item: item.priority, reverse=True)
        if len(resources) >= 1:
            resource = resources[0]
        else:    
            resource = Resource.get_dummy_data()
        avatar = avatarManager.get_avatar(instance.jid)    
        setattr(instance, "avatar", avatar)
        setattr(instance, "resource", resource)                    
    
    @postGui(inclass=True)
    def on_avatar_saved(self, sender, jid, path, *args, **kwargs):
        ret = self.get_obj_by_jid(jid)
        if ret:
            ret.avatar = path
    
