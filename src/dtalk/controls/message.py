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
logger = logging.getLogger("dtalk.controls.message")

from PyQt5 import QtCore
from dtalk.models.signals import post_save
from dtalk.models import ReceivedMessage, SendedMessage
from dtalk.controls.base import AbstractWrapperModel        
from dtalk.controls.qobject import postGui


class MessageModel(AbstractWrapperModel):
    other_fields = ("type", "successed", "readed")
    
    def initial(self, to_jid):
        self.to_jid = to_jid
        self.init_signals()
        
    def init_signals(self):    
        post_save.connect(self.on_received_message, sender=ReceivedMessage)        
        post_save.connect(self.on_sended_message, sender=SendedMessage)
        
    @postGui    
    def on_received_message(self, sender, instance, created, update_fields, *args, **kwargs):    
        self.appendMessage(instance)
    
    @postGui
    def on_sended_message(self, sender, instance, created, update_fields, *args, **kwargs):    
        self.appendMessage(instance)
    
    
    def appendMessage(self, instance):
        if not self.verify(instance):
            return
        obj = self.wrapper_instance(instance)
        self.append(obj)
        
    def verify(self, instance):    
        return instance.friend.jid == self.to_jid
    
    def attach_attrs(self, instance):
        if isinstance(instance, SendedMessage):
            setattr(instance, "readed", True)
        else:    
            setattr(instance, "successed", True)
        setattr(instance, "type", instance.TYPE)    
        
    @QtCore.pyqtSlot(str)
    def sendMessage(self, body):
        SendedMessage.send_message(self.to_jid, body)
        
        
    
