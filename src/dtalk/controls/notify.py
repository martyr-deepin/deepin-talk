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
from dtalk.controls.qobject import QPropertyObject, QObjectListModel, postGui
from dtalk.controls.utils import getDisplayName, getFriend
from dtalk.controls import signals as cSignals
from dtalk.cache import avatarManager
from dtalk.models import signals as dbSignals, FriendNotice


NOTIFY_JID = "roster@im.linuxdeepin.com"
NOTIFY_TYPE_MESSAGE = 1
NOTIFY_TYPE_ROSTER = 2

class BaseNotifyObject(QPropertyObject()):
    __qtprops__ = { "title" : "", "total": 0, "image" : "", "type_" : NOTIFY_TYPE_MESSAGE, "jid" : "" }
    
    def __eq__(self, other):
        return self.type_ == other.type_ and self.jid == other.jid
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def onClicked(self):
        raise NotImplementedError
    
    def addInstance(self, instance):
        self.total += 1
            
class MessageNotifyObject(BaseNotifyObject):    
    
    def __init__(self, instance):
        super(MessageNotifyObject, self).__init__()
        friend = getFriend(instance)        
        self._instance = instance
        self.title = getDisplayName(instance)
        self.image = avatarManager.get_avatar(friend.jid)    
        self.total = 1
        self.type_ = NOTIFY_TYPE_MESSAGE
        self.jid = friend.jid
        
    def onClicked(self):    
        cSignals.show_message.send(sender=self, jid=self.jid)    
        return True
        
class RosterNotifyObject(BaseNotifyObject):    
    
    def __init__(self, presence):
        super(RosterNotifyObject, self).__init__()
        self._instance = presence
        self.type_ = NOTIFY_TYPE_ROSTER
        self.title = "验证消息"        
        self.jid = NOTIFY_JID
        self.image = "qrc:/images/common/logo.png"
        self.total = 1
        self._instances = [ presence ]
        
    def onClicked(self):    
        presence = self._instances.pop()
        cSignals.roster_request_add.send(sender=self, instance=presence)
        self.total -= 1
        if self.total <= 0:
            return True
        return False
    
    def addInstance(self, instance):
        self._instances.append(instance._instance)
        self.total += 1
        
class NotifyModel(QObjectListModel):        
    
    instanceRole = QtCore.Qt.UserRole + 1
    _roles = { instanceRole : "instance" }
    
    def __init__(self, parent=None):
        super(NotifyModel, self).__init__(parent)
        dbSignals.post_save.connect(self.onFriendNoticePostSave, sender=FriendNotice)
        
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size():
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        if role == self.instanceRole:
            return item
        return QtCore.QVariant()        
    
    def getObjByInstance(self, instance):
        if instance in self._data:
            return self._data[self._data.index(instance)]
        return None
    
    @QtCore.pyqtSlot(int)
    def onClicked(self, index):
        try:
            obj = self.get(index)        
        except:
            pass
        else:
            if self.size() > 0:
                newObj = self.get(0)
                cSignals.blink_trayicon.send(sender=self, icon=newObj.image)
            else:    
                cSignals.still_trayicon.send(sender=self)
                
            removed = obj.onClicked()    
            if removed:
                self.removeAt(index)
                
    def appendObject(self, newObj):        
        obj = self.getObjByInstance(newObj)
        if obj is not None:
            obj.addInstance(newObj)
        else:    
            self.append(newObj)
            cSignals.blink_trayicon.send(sender=self, icon=newObj.image)
                
    def appendMessage(self, instance):
        obj = MessageNotifyObject(instance)        
        self.appendObject(obj)
            
    def appendNotice(self, presence):        
        notifyObj = RosterNotifyObject(presence)
        self.appendObject(notifyObj)

    @postGui()    
    def onFriendNoticePostSave(self, instance, *args, **kwargs):
        self.appendNotice(instance)
        
        
