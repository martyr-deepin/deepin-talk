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
from dtalk.controls.qobject import QPropertyObject, QInstanceModel
from dtalk.controls.models import FriendWrapper
from dtalk.controls import signals as cSignals
from dtalk.models import Friend

class SearchGroupWrapper(QPropertyObject()):
    
    __qtprops__ = { "title" : "", "model" : QtCore.QVariant() }
    
    def __init__(self, title, model, parent=None):
        super(SearchGroupWrapper, self).__init__(parent)
        self.title = title
        self.model = model

class SearchGroupModel(QInstanceModel):
    
    def __init__(self, parent=None):
        super(SearchGroupModel, self).__init__(parent)
        self.appendData("好友", SearchFriendModel(parent=self))
        
    def appendData(self, title, model):    
        self.append(SearchGroupWrapper(title, model, parent=self))
        
        
    @QtCore.pyqtSlot(str)    
    def doSearch(self, text):
        for item in self._data:
            item.model.doSearch(text)
            
class SearchFriendModel(QInstanceModel):        
    
    def __init__(self, parent=None):
        super(SearchFriendModel, self).__init__(parent)
        
    def doSearch(self, text):    
        
        self.clear()        
        
        if text == "":
            return 
        
        qs = Friend.select().where(Friend.jid ** "%{0}%".format(text), Friend.isSelf == False)
        friends = [ FriendWrapper(item, parent=self) for item in qs ]
        self.setAll(friends)
            
    @QtCore.pyqtSlot(int)        
    def doClicked(self, index):        
        try:
            instance = self.get(index)
        except: pass    
        else:
            cSignals.show_message.send(sender=self, jid=instance.jid, loaded=False)
