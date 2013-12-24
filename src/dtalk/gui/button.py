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

from dtalk.utils import six
from PyQt5 import QtGui, QtWidgets, QtCore

class ImageButton(QtWidgets.QGraphicsObject):
    
    def __init__(self, images, parent=None):
        super(ImageButton, self).__init__(parent)
        
        # accept hover events.
        self.setAcceptHoverEvents(True)
        
        # flags
        self._pressFlag = False
        
        # images 
        self.normalImage = self.hoverImage = self.pressImage = QtGui.QPixmap()
        
        if isinstance(images, six.string_types):
            self.normalImage = QtGui.QPixmap(images)
        elif isinstance(images, tuple):    
            if len(images) == 3:
                self.normalImage, self.hoverImage, self.pressImage = list(map(QtGui.QPixmap, images))
            elif len(images) == 2:
                self.normalImage, self.hoverImage = list(map(QtGui.QPixmap, images))
                
        self.currentPixmap = self.normalImage        
                
        
    def hoverEnterEvent(self, event):
        if not self.hoverImage.isNull() and self.currentPixmap != self.hoverImage:
            self.currentPixmap = self.hoverImage            
            self.update()
        
    def hoverLeaveEvent(self, event):    
        if not self.normalImage.isNull() and self.currentPixmap != self.normalImage:
            self.currentPixmap = self.normalImage
            self.update()
            
    def mousePressEvent(self, event):            
        if not self.pressImage.isNull() and self.currentPixmap != self.pressImage:
            self.currentPixmap = self.pressImage
            self.update()
            
    def mouseReleaseEvent(self, event):        
        if not self.normalImage.isNull() and self.currentPixmap != self.normalImage:
            self.currentPixmap = self.normalImage
            self.update()
        
    def boundingRect(self):    
        return QtCore.QRectF(self.currentPixmap.rect())
    
    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self.currentPixmap)
