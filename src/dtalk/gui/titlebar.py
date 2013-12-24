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

from PyQt5 import QtWidgets, QtCore
from dtalk.gui.utils import getObjectWidget, setObjectTransparent

class Titlebar(QtWidgets.QWidget):
    
    def __init__(self,  topWin, parent=None):
        super(Titlebar, self).__init__(parent)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        
        self.topWin = topWin
        self._oldPos = None
        self._pressFlag = False
        self.setContentsMargins(0, 0, 0, 0)
        setObjectTransparent(self)        
        
        # init buttons.
        themeButton = getObjectWidget("themeButton")
        menuButton = getObjectWidget("menuButton")
        minButton = getObjectWidget("minButton")
        closeButton = getObjectWidget("closeButton")
        closeButton.clicked.connect(self.onCloseButtonClicked)
        
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 5, 0)
        layout.setSpacing(0)
        layout.addStretch()
        layout.addWidget(themeButton)
        layout.addWidget(menuButton)
        layout.addWidget(minButton)
        layout.addWidget(closeButton)
        
        self.setLayout(layout)
                
    def mousePressEvent(self, event):    
        self._oldPos = self.topWin.mapToGlobal(event.globalPos())
        self._pressFlag = True
        
    def mouseReleaseEvent(self, event):    
        self._pressFlag = False
    
    def mouseMoveEvent(self, event):
        if self._pressFlag:
            newPos = self.topWin.mapToGlobal(event.globalPos())
            delta = newPos - self._oldPos
            self.topWin.move(self.topWin.x()+delta.x(), self.topWin.y()+delta.y())
            self._oldPos = newPos
            
    def onCloseButtonClicked(self):        
        self.topWin.closeWindow()
