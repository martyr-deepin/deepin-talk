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
    
    def __init__(self, iconPath, parent=None):
        super(TrayIcon, self).__init__(QtGui.QIcon(iconPath), parent)
        self._hovered = False
        self.activated.connect(self.onTrayIconActivated)
        cSignal.blink_trayicon.connect(self.blinking_trayicon)
        cSignal.still_trayicon.connect(self.stilled_trayicon)
        keyBinder.backend.mouseMoved.connect(self.on_global_mouse_moved)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(200)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_timer_timeout)
        
        
    def onTrayIconActivated(self, reason):    
        print reason
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
        pass
    
    def stilled_trayicon(self, *args, **kwargs):
        pass
    
    def set_hovered(self, value):
        if self._hovered != value:
            self._hovered = value
            self._hoveredNty.emit()
            self.hoverStatusChanged.emit(value)
            
    def get_hovered(self):        
        return self._hovered
    
    def on_global_mouse_moved(self, x, y):
        rect = self.getNormalGeometry()
        width = rect.x() + rect.width()
        height = rect.y() + rect.height()
        if rect.x() <= x <= width and \
                rect.y() <= y <= height:
            self.timer.stop()            
            self.set_hovered(True)
        else:    
            self.timer.start()
            
    def on_timer_timeout(self):        
        self.set_hovered(False)
            
    hovered = QtCore.pyqtProperty(bool, get_hovered, set_hovered, notify=_hoveredNty)        
