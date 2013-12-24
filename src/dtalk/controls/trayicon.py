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
from dtalk.keybinder  import keyBinder

class TrayIcon(QtWidgets.QSystemTrayIcon):
    
    _hoveredNty = QtCore.pyqtSignal()
    hoverStatusChanged = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent=None):
        self.defaultIcon = QtGui.QIcon(":/images/common/logo.png")        
        super(TrayIcon, self).__init__(self.defaultIcon, parent)
        self.transparentIcon = QtGui.QIcon(":/images/common/transparent.png")
        self.blinkIcon = None
        self.currentIcon = self.defaultIcon
        self._hovered = False
        self.activated.connect(self.onTrayIconActivated)
        
        cSignal.blink_trayicon.connect(self.blinking_trayicon)
        cSignal.still_trayicon.connect(self.stilled_trayicon)
        keyBinder.mouseMoved.connect(self.on_global_mouse_moved)
        
        self.hoverTimer = QtCore.QTimer()
        self.hoverTimer.setInterval(200)
        self.hoverTimer.setSingleShot(True)
        self.hoverTimer.timeout.connect(self.on_timer_timeout)
        self.blinkTimer = QtCore.QTimer()
        self.blinkTimer.setInterval(400)
        self.blinkTimer.setSingleShot(False)
        self.blinkTimer.timeout.connect(self.on_blink_timer_timeout)
        
    def onTrayIconActivated(self, reason):    
        if reason in (QtWidgets.QSystemTrayIcon.Context, QtWidgets.QSystemTrayIcon.Trigger):
            pass
        
    @QtCore.pyqtSlot(result="QVariant")        
    def getPos(self):        
        geometry = self.geometry()
        mouseX = int(geometry.x() / 2 + geometry.width() / 2)
        mouseY = int(geometry.y() / 2)
        return QtCore.QPoint(mouseX, mouseY)
    
    def getNormalGeometry(self):
        geometry = self.geometry()
        return QtCore.QRect(geometry.x() / 2, geometry.y() / 2, geometry.width(), geometry.height())
    
    def mouseMoveEvent(self, event):
        print event

    def blinking_trayicon(self, sender, icon, *args, **kwargs):
        self.blinkIcon = QtGui.QIcon(icon)
        self.blinkTimer.start(400)
        self.currentIcon = self.blinkIcon
    
    def stilled_trayicon(self, *args, **kwargs):
        self.blinkTimer.stop()
        self.currentIcon = self.defaultIcon
        self.setIcon(self.defaultIcon)
    
    def on_blink_timer_timeout(self):
        if self.currentIcon != self.transparentIcon:
            self.currentIcon = self.transparentIcon
            self.setIcon(self.transparentIcon)
        else:    
            if self.blinkIcon is not None:
                self.currentIcon = self.blinkIcon
                self.setIcon(self.blinkIcon)
    
    def set_hovered(self, value):
        if self._hovered != value:
            self._hovered = value
            self._hoveredNty.emit()
            self.hoverStatusChanged.emit(value)
            
    def get_hovered(self):        
        return self._hovered
    
    def on_global_mouse_moved(self, x, y):
        rect = self.getNormalGeometry()
        if rect.contains(x, y):
            self.hoverTimer.stop()            
            self.set_hovered(True)
        else:    
            self.hoverTimer.start()
            
    def on_timer_timeout(self):        
        self.set_hovered(False)
            
    hovered = QtCore.pyqtProperty(bool, get_hovered, set_hovered, notify=_hoveredNty)        
