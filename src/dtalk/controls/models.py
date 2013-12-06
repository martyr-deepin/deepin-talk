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
logger = logging.getLogger("controls.models")

from PyQt5 import QtCore

from dtalk.models.signals import post_save, post_delete
from dtalk.models import Resource, Friend
from dtalk.controls.base import AbstractWrapperModel        
from dtalk.controls.qobject import postGui
from dtalk.cache import avatarManager
import dtalk.cache.signals as cache_signals

class FriendModel(AbstractWrapperModel):        
    dbs = (Resource, Friend)
    unique_field = "id"
    other_fields = ("resource", "avatar")
    init_signals_on_db_finished = False
    ownerObj = None
        
    '''
    load(): select data from the database of interest
    init_signals: after the first call initData(), its initial
    '''
    
    def load(self):
        friends = Friend.filter(subscription="both", isSelf=False)
        if self.ownerObj is None:
            obj = Friend.get_self()
            if obj:
                self.ownerObj = self.wrapper_instance(obj)
        return friends
        
    def init_signals(self):    
        post_save.connect(self.on_post_save, sender=Resource)
        post_delete.connect(self.on_post_delete, sender=Resource)
        post_save.connect(self.on_post_save, sender=Friend)
        post_delete.connect(self.on_post_delete, sender=Friend)
        cache_signals.avatar_saved.connect(self.on_avatar_saved)
        
    def update_changed(self, instance, update_fields):    
        obj = self.get_obj_by_jid(instance.jid)
        if not obj:
            return
        if update_fields and isinstance(update_fields, list):
            for key in update_fields:            
                print "key"
                setattr(obj, key, getattr(instance, key, None))
                
    @postGui    
    def on_post_save(self, sender, instance, created, update_fields, *args, **kwargs):
        if sender == Friend:
            if not self.verify(instance):
                return 

            if created:
                obj = self.wrapper_instance(instance)                
                self.append(obj)
            else:    
                self.update_changed(instance, update_fields)
                
    @postGui            
    def on_post_delete(self, sender, instance, *args, **kwargs):
        pass
    
    def verify(self, instance):
        return instance.subscription == "both" or instance.isSelf == True
    
    def get_obj_by_jid(self, jid):
        ret = None
        for obj in self._data:
            if obj.jid == jid:
                ret = obj
                break
        if ret is None:    
            if self.ownerObj and self.ownerObj.jid == jid:
                return self.ownerObj
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
    
    @postGui
    def on_avatar_saved(self, sender, jid, path, *args, **kwargs):
        ret = self.get_obj_by_jid(jid)
        if ret:
            ret.avatar = path
            
    @QtCore.pyqtSlot(result="QVariant")
    def getSelf(self):        
        return self.ownerObj
    
