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

from __future__ import print_function

from PyQt5 import QtCore, QtWidgets, QtGui
from dtalk.gui.utils import setObjectTransparent
from dtalk.gui.draw import drawRectWidthCorner, drawCornerImage
from dtalk.cache.avatar import avatarManager

class ChatView(QtWidgets.QListView):
    
    def __init__(self, model, parent=None):
        super(ChatView, self).__init__(parent)
        setObjectTransparent(self)
        self.setStyleSheet("background: transparent; border: none;")
        self.viewport().setAutoFillBackground(False)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        itemDelegate = MessageDelegate()
        self.setItemDelegate(itemDelegate)
        self.setModel(model)
        
        
class MessageDelegate(QtWidgets.QStyledItemDelegate):        
    
    def __init__(self, parent=None):    
        super(MessageDelegate, self).__init__(parent)
        
        self.textDocument = QtGui.QTextDocument(self)
        self.textDocument.cursorPositionChanged.connect(self.onCursorChanged)
        
        
    def onCursorChanged(self, cursor):    
        print(cursor)
        
    def paint(self, painter, option, index):
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform 
                            | QtGui.QPainter.TextAntialiasing)
        
        model = index.model()
        instance = index.data(model.instanceRole)
        
        
        imageWidth = 80
        imageRect = QtCore.QRect(option.rect.x(), option.rect.y() + (option.rect.height() - imageWidth) / 2, imageWidth, imageWidth)
        image = avatarManager.get_avatar(instance.friendJid)
        drawCornerImage(painter, image, imageRect)
        dummyRect = option.rect.adjusted(imageWidth, 0, -imageWidth, 0)
        
        
        path, rect = drawRectWidthCorner(painter, dummyRect, marginWidth=5)
        painter.fillPath(path, QtGui.QColor(82, 60, 145))
        
        # draw body
        doc = self.textDocument
        doc.setHtml(instance.body)
        doc.setTextWidth(rect.width())
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        painter.save()
        painter.translate(rect.topLeft());
        painter.setClipRect(option.rect.translated(-rect.topLeft()))
        dl = doc.documentLayout()
        dl.draw(painter, ctx)
        painter.restore()        
        

    def sizeHint(self, option, index):
        size = super(MessageDelegate, self).sizeHint(option, index)
        size.setHeight(size.height() * 5)
        return size
        
    
