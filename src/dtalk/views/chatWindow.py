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

from PyQt5 import QtCore, QtWidgets
from dtalk.gui.graphics import DGraphicsWindow
from dtalk.gui.utils import getObjectWidget, createProxyWidget
from dtalk.gui.titlebar import Titlebar
from dtalk.views.widgets.chatview import ChatView

class ChatWindow(DGraphicsWindow):
    requestClose = QtCore.pyqtSignal()
    
    def __init__(self, model, jid, parent=None):
        super(ChatWindow, self).__init__(parent)
        
        # set size
        self.setMinimumSize(QtCore.QSize(580, 600))
        self.anchorLayout = QtWidgets.QGraphicsAnchorLayout()
        self.anchorLayout.setSpacing(0)
        self.anchorLayout.setMinimumSize(QtCore.QSizeF(self.contentsRect().width(), self.contentsRect().height()))
        
        titlebar = createProxyWidget(Titlebar(self), QtCore.QSizeF(self.rect().width(), -1))
        mask = createProxyWidget(getObjectWidget("mask", QtWidgets.QLabel), 
                                 minimum=QtCore.QSizeF(self.rect().width(), 136),
                                 maximum=QtCore.QSizeF(self.rect().width(), 136))
        self.chatview = ChatView(model)
        _chatview = createProxyWidget(self.chatview, QtCore.QSizeF(self.rect().width(), -1))
        self.anchorLayout.addAnchor(mask, QtCore.Qt.AnchorTop, self.anchorLayout, QtCore.Qt.AnchorTop)                
        self.anchorLayout.addAnchor(titlebar, QtCore.Qt.AnchorTop, self.anchorLayout, QtCore.Qt.AnchorTop)        
        self.anchorLayout.addAnchor(_chatview, QtCore.Qt.AnchorTop, mask, QtCore.Qt.AnchorBottom)
        self.anchorLayout.addAnchor(_chatview, QtCore.Qt.AnchorBottom, self.anchorLayout, QtCore.Qt.AnchorBottom)
        
        mainWidget = QtWidgets.QGraphicsWidget()
        mainWidget.setLayout(self.anchorLayout)
        # mainWidget.setPos(-5, -5)        
        mainWidget.setPos(0, -5)        
        
        self.addItem(mainWidget)
        
        self.model = model
        self.jid = jid
        
    @QtCore.pyqtSlot()    
    def closeWindow(self):
        self.requestClose.emit()
        
        

