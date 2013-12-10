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
from dtalk.views.base import BaseView
from dtalk.utils.xdg import get_qml


class ChatWindow(BaseView):
    
    def __init__(self, model, parent=None):
        super(ChatWindow, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(600, 620))        
        self.model = model
        self.setSource(QtCore.QUrl.fromLocalFile(get_qml('ChatFrame','ChatWindow.qml')))
        
    @QtCore.pyqtSlot(result=str)    
    def getJid(self):
        return self.jid
    
    @QtCore.pyqtSlot(result="QVariant")
    def getModel(self):
        return self.model
