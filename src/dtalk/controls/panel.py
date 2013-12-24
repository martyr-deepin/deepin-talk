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


# DON'T DELETE BELOW CODE!
# Calls XInitThreads() as part of the QApplication construction in order to make Xlib calls thread-safe. 
# This attribute must be set before QApplication is constructed.
# Otherwise, you will got error:
#     "python: ../../src/xcb_conn.c:180: write_vec: Assertion `!c->out.queue_len' failed."
# 
# Qt5 application hitting the race condition when resize and move controlling for a frameless window.
# Race condition happened while Qt was using xcb to read event and request window position movements from two threads. 
# Same time rendering thread was drawing scene with opengl. 
# Opengl driver (mesa) is using Xlib for buffer management. Result is assert failure in libxcb in different threads. 
# 
import os
from PyQt5 import QtCore
if os.name == 'posix':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True) 

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt5 import QtWidgets
from dtalk.utils.xdg import get_qml
from dtalk.controls.managers import modelManager, serverManager, controlManager
from dtalk.views.base import BaseView
from dtalk.controls.trayicon import TrayIcon
from dtalk.keybinder import keyBinder
# from dtalk.views.chatWindow import ChatWindow


class Panel(BaseView):
    
    hideOtherWindow = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Panel, self).__init__()
        self.setMinimumSize(QtCore.QSize(336, 780))        
        QtWidgets.qApp.focusWindowChanged.connect(self.onFocusWindowChanged)
        
        self.initTray()        
        self.setContextProperty("modelManager", modelManager)
        self.setContextProperty("controlManager", controlManager)
        self.setContextProperty("serverManager", serverManager)
        self.setContextProperty("trayIcon", self.trayIcon)
        self.setSource(QtCore.QUrl.fromLocalFile(get_qml('Main.qml')))
        # self.chat = ChatWindow(None, None)
        # self.chat.show()

        self.initKeybinder()
        
    def onFocusWindowChanged(self, focusWindow):    
        if focusWindow.__class__.__name__ != "QQuickWindow":
            self.hideOtherWindow.emit()
            
    def initTray(self):        
        self.trayIcon = TrayIcon(self)
        self.trayIcon.show()

    def initKeybinder(self):    
        keyBinder.start()
        
    @QtCore.pyqtSlot()    
    def closeWindow(self):
        pass
    
        
