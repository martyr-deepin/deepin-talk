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

from sleekxmpp.jid import  _parse_jid, InvalidJID
from dtalk.controls.qobject import QPropertyObject, QInstanceModel, postGui
from dtalk.controls.models import FriendWrapper
from dtalk.controls import signals as cSignals
from dtalk.models import Friend
from dtalk.xmpp.base import xmppClient
from dtalk.xmpp import signals as xmppSignals
from dtalk.xmpp import utils as xmppUtils
from dtalk.utils.threads import threaded
from dtalk.utils.misc import Storage


class SearchGroupWrapper(QPropertyObject()):
    
    __qtprops__ = { "title" : "", "model" : QtCore.QVariant(), "type_" : "" }
    
    def __init__(self, title, model, type_, parent=None):
        super(SearchGroupWrapper, self).__init__(parent)
        self.title = title
        self.model = model
        self.type_ = type_

class SearchGroupModel(QInstanceModel):
    
    def __init__(self, parent=None):
        super(SearchGroupModel, self).__init__(parent)
        self.appendData("好友", LocalFriendModel(parent=self), "local")
        self.appendData("网络", RemoteFriendModel(parent=self), "remote")
        
    def appendData(self, title, model, type_):    
        self.append(SearchGroupWrapper(title, model, type_, parent=self))
        
    @QtCore.pyqtSlot(str)    
    def doSearch(self, text):
        for item in self._data:
            item.model.doSearch(text)
            
class LocalFriendModel(QInstanceModel):        
    
    def __init__(self, parent=None):
        super(LocalFriendModel, self).__init__(parent)
        
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
            
            
class RemoteFriendModel(QInstanceModel):            
    
    def __init__(self, parent=None):
        super(RemoteFriendModel, self).__init__(parent)
        xmppSignals.roster_got_vcard.connect(self._onRosterGotVcard)
        self._jid = None
        
    @postGui()    
    def _onRosterGotVcard(self, jid, vcard_temp, *args, **kwargs):    
        if self._jid != jid:
            return
        
        s = Storage()
        s['nickname'] = xmppUtils.get_vcard_nickname(vcard_temp)
        s['remark'] = ""
        s['jid'] = jid
        self.append(FriendWrapper(s, parent=self))
        
    def doSearch(self, text):    
                
        self.clear()        
        
        if text == "":
            self._jid = ""
            return 
        
        if "@" not in text:
            jid = "{0}@{1}".format(text, xmppClient.boundjid.domain)
        else:    
            jid = text
            
        try:    
            _parse_jid(jid)
        except InvalidJID:     
            return 
        
        self._jid = jid
        
        try:
            Friend.get(jid=self._jid)
        except Friend.DoesNotExist:    
            self.asyncRequestVCard(self._jid)
        
    @threaded 
    def asyncRequestVCard(self, *args, **kwargs):
        xmppClient.request_vcard(*args, **kwargs)
        
    @QtCore.pyqtSlot(int)        
    def doClicked(self, index):        
        pass
            
    @QtCore.pyqtSlot(int)        
    def doAddClicked(self, index):
        try:
            instance = self.get(index)
        except: pass    
        else:
            cSignals.open_add_friend_dialog.send(sender=self, friend=instance)




