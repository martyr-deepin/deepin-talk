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

from PyQt5 import QtCore
from dtalk.controls.qobject import QPropertyObject, QObjectListModel
from dtalk.controls.utils import get_display_name, get_friend
from dtalk.controls import signals as cSignals
from dtalk.cache import avatarManager


class BaseNotifyObject(QPropertyObject()):
    __qtprops__ = { "title" : "", "total": 0, "image" : ""}
    
    def __eq__(self, other):
        return self.instance.friend.jid == other.friend.jid
    
    def __ne__(self, other):
        return not self == other
            
class MessageNotifyObject(BaseNotifyObject):    
    
    def __init__(self, instance):
        super(MessageNotifyObject, self).__init__()
        self.instance = instance
        self.title = get_display_name(instance)
        friend = get_friend(instance)
        self.image = avatarManager.get_avatar(friend.jid)    
        self.total = 1
        
        
class NotifyModel(QObjectListModel):        
    
    instanceRole = QtCore.Qt.UserRole + 1
    _roles = { instanceRole : "instance" }
    
    def __init__(self, parent=None):
        super(NotifyModel, self).__init__(parent)
        
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size:
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        if role == self.instanceRole:
            return item
        return QtCore.QVariant()        
    
    def get_obj_by_instance(self, instance):
        ret = None
        for obj in self._data:
            if obj.instance.friend.jid == instance.friend.jid:
                ret = obj
                break
        return ret    
                
    
    def appendMessage(self, instance):
        obj = self.get_obj_by_instance(instance)
        if obj is not None:
            obj.total += 1
        else:    
            notifyObj = MessageNotifyObject(instance)
            self.append(notifyObj)
            cSignals.blink_trayicon.send(sender=self, icon=notifyObj.image)
