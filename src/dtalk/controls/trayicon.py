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

from PyQt5 import QtWidgets, QtGui, QtCore
from dtalk.controls import signals as cSignal 
from dtalk.controls.qobject import postGui
from dtalk.keybinder  import keyBinder

class TrayIcon(QtWidgets.QSystemTrayIcon):
    
    _hoveredNty = QtCore.pyqtSignal()
    hoverStatusChanged = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent=None):
        self.defaultIcon = QtGui.QIcon(":/images/common/logo.png")        
        super(TrayIcon, self).__init__(self.defaultIcon, parent)
        self.currentIcon = self.defaultIcon
        self._hovered = False
        self.activated.connect(self.onTrayIconActivated)
        
        cSignal.blink_trayicon.connect(self.blinkingTrayicon)
        cSignal.still_trayicon.connect(self.stilledTrayicon)
        keyBinder.mouseMoved.connect(self.onGlobalMouseMoved)
        
        self.hoverTimer = QtCore.QTimer()
        self.hoverTimer.setInterval(200)
        self.hoverTimer.setSingleShot(True)
        self.hoverTimer.timeout.connect(self.onHoverTimerTimeout)
        self.flashTimer = QtCore.QTimer()
        self.flashTimer.setInterval(400)
        self.flashTimer.setSingleShot(False)
        self.flashTimer.timeout.connect(self.flash)
        self._flashFlag = True
        
    def onTrayIconActivated(self, reason):    
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            cSignal.raise_window.send(sender=self)
        
    @QtCore.pyqtSlot(int, int, result="QVariant")        
    def getPos(self, width, height):        
        offset = 12
        screenSize = QtWidgets.QApplication.desktop().geometry().size()
        geometry = self.geometry()
        mouseX = int(geometry.x() + geometry.width() / 2)
        mouseY = int(geometry.y())
        x = mouseX - int(width / 2)
        if mouseY > int(screenSize.height() / 2):
            y = mouseY - height 
        else:    
            y = mouseY + offset
        
        return QtCore.QPoint(x, y)
    
    def getNormalGeometry(self):
        geometry = self.geometry()
        return QtCore.QRect(geometry.x(), geometry.y(), geometry.width(), geometry.height())
        
    def flash(self):    
        if self._flashFlag:
            self.setIcon(QtGui.QIcon())
        else:    
            self.setIcon(self.currentIcon)
        self._flashFlag = not self._flashFlag    

    @postGui()    
    def blinkingTrayicon(self, sender, icon, *args, **kwargs):
        try:
            if icon.startswith("qrc:/"):
                icon = icon.lstrip("qrc")
        except: pass
        
        blinkingIcon = QtGui.QIcon(icon)
        if blinkingIcon.isNull():
            self.currentIcon = self.defaultIcon
        else:    
            self.currentIcon = blinkingIcon
            
        self.flashTimer.start(400)
    
    @postGui()    
    def stilledTrayicon(self, *args, **kwargs):
        self.flashTimer.stop()
        self.currentIcon = self.defaultIcon
        self.setIcon(self.defaultIcon)
        
    def setHovered(self, value):
        if self._hovered != value:
            self._hovered = value
            self._hoveredNty.emit()
            self.hoverStatusChanged.emit(value)
            
    def getHovered(self):        
        return self._hovered
    
    def onGlobalMouseMoved(self, x, y):
        rect = self.getNormalGeometry()
        if rect.contains(x, y):
            self.hoverTimer.stop()            
            self.setHovered(True)
        else:    
            self.hoverTimer.start()
            
    def onHoverTimerTimeout(self):        
        self.setHovered(False)
            
    hovered = QtCore.pyqtProperty(bool, getHovered, setHovered, notify=_hoveredNty)        
