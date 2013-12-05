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

from dtalk.models.signals import post_save, post_delete
from dtalk.models import Resource, Friend
from dtalk.controls.base import AbstractWrapperModel        
from dtalk.controls.qobject import postGui

class FriendModel(AbstractWrapperModel):        
    dbs = (Resource, Friend)
    unique_obj = "id"
    other_fields = ("resource",)
    
    def load(self):
        friends = Friend.filter(subscription="both")
        
        for f in friends:
            resources = sorted(f.resources, key=lambda item: item.priority, reverse=True)
            if len(resources) >= 1:
                resource = resources[0]
            else:    
                resource = Resource.get_dummy_data()
            setattr(f, "resource", resource)                    
        return friends
        
    def init_signals(self):    
        post_save.connect(self.on_post_save, sender=Resource)
        post_delete.connect(self.on_post_delete, sender=Resource)
        post_save.connect(self.on_post_save, sender=Friend)
        post_delete.connect(self.on_post_delete, sender=Friend)
        
    @postGui    
    def on_post_save(self, sender, instance, created, *args, **kwargs):
        if sender == Friend:
            obj = self.wrapper_instance(instance)
            if created:
                self.append(obj)
            else:    
                self.replace(obj)
                
    @postGui            
    def on_post_delete(self, sender, instance, *args, **kwargs):
        pass
    
