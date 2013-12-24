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
from dtalk.gui.window import DWindow

class DGraphicsWindow(DWindow):
    
    def __init__(self, parent=None):
        super(DGraphicsWindow, self).__init__(parent)
        
        self.view = QtWidgets.QGraphicsView(self)
        self.view.setViewportMargins(0, 0, 0, 0)        
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scene = QtWidgets.QGraphicsScene(self.view)
        self.view.setScene(self.scene)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setBackgroundPixmap(":/images/common/bg.png")

        
    def resizeEvent(self, event):
        super(DGraphicsWindow, self).resizeEvent(event)
        
    addItem = property(lambda self: self.scene.addItem)
    addWidget = property(lambda self: self.scene.addWidget)
    
    def setMinimumSize(self, size):
        super(DGraphicsWindow, self).setMinimumSize(size)
        rect =  self.contentsRect()
        self.scene.setSceneRect(QtCore.QRectF(rect))
