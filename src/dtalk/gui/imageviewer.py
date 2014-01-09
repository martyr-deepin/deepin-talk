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


from PyQt5 import QtCore, QtGui, QtWidgets


class ImageViewer(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargin(0, 0, 0, 0)
        layout.addWidget(self.scrollArea)
        
        self.scaleFactor = 1.0        
        
    def open(self):    
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", QtWidgets.QDir.currentPath())
        if filename:
            image = QtGui.QImage(filename)
            if image.isNull():
                QtWidgets.QMessageBox.information(self, "Image Viewer", "Can't load %s." % filename)
                return
            
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            
    def scaleImage(self, factor):    
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
        
    def adjustScrollBar(self, scrollBar, factor):    
        scrollBar.setValue(int(factor * scrollBar.value()) + ((factor - 1) * scrollBar.pageStep()/2))
        
    def zoomIn(self):    
        self.scaleImage(1.25)
        
    def zoomOut(self):    
        self.scaleImage(0.8)
