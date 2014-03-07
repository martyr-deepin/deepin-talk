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


from __future__ import unicode_literals

from PyQt5 import QtCore, QtGui
from dtalk.views.base import BaseView
from dtalk.utils.xdg import get_qml
from dtalk.cache.avatar import avatarManager

class BaseDialog(BaseView):
    
        
    @QtCore.pyqtSlot()    
    def closeWindow(self):
        self.engine().trimComponentCache()        
        self.engine().clearComponentCache()
        self.hide()
        # self.close()
        # self.deleteLater()

class AddFriendDialog(BaseDialog):        
    
    def __init__(self, parent=None):
        super(AddFriendDialog, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(360, 170))        
        self.setSource(QtCore.QUrl.fromLocalFile(get_qml("Dialog", "AddFriendDialog.qml")))

    def setFriendInstance(self, friend):    
        self.setContextProperty("friend", friend)
        
        
