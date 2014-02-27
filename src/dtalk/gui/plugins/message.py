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


from __future__ import unicode_literals, print_function

from PIL import Image
from PyQt5 import QtCore, QtQuick, QtGui, QtWidgets
from dtalk.utils.xdg import get_uuid_screentshot_path

class DMessage(QtQuick.QQuickItem):
    _maxWidthNfy = QtCore.pyqtSignal()
    _documentNfy = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(DMessage, self).__init__(parent)
        self.systemClipboard = None
        self._textDocument = None
        # self._textEdit = QtWidgets.QTextEdit()

        self._maxWidth = 150
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton|QtCore.Qt.RightButton)
        self.setAcceptHoverEvents(True)
        
    def getDocument(self):
        return self._textDocument
    
    def setDocument(self, quickTextDocument):
        textDocument = quickTextDocument.textDocument()
        if self._textDocument is None:
            self._textDocument = textDocument
            self._textCursor = QtGui.QTextCursor(self._textDocument)
            # self._textEdit.setDocument(self._textDocument)
        self._documentNfy.emit()    
        
    document = QtCore.pyqtProperty(QtQuick.QQuickTextDocument, getDocument, setDocument, notify=_documentNfy)
    
    def getMaxWidth(self):
        return self._maxWidth
    
    def setMaxWidth(self, width):
        self._maxWidth = width
        self._maxWidthNfy.emit()
        
    maxWidth = QtCore.pyqtProperty(int, getMaxWidth, setMaxWidth, notify=_maxWidthNfy)
        
    @QtCore.pyqtSlot()        
    def insertFromClipboard(self):
        self.initialClipboard()        
        mimeData = self.systemClipboard.mimeData()
        self.insertFromMimedata(mimeData)
            
    def insertFromMimedata(self, mimeData):    
        if mimeData.hasImage():
            url = get_uuid_screentshot_path()
            img = mimeData.imageData()
            img.save(url, "png")
            self.insertImage(url)
        elif mimeData.hasText():    
            self.insertText(mimeData.text())
        
    def initialClipboard(self):
        if self.systemClipboard is None:
            self.systemClipboard = QtWidgets.QApplication.clipboard()        
            
    def dropImage(self, url, image):        
        self.insertImage(url.toString())
        
    @QtCore.pyqtSlot() 
    def selectWord(self):    
        self.insertFromClipboard()
        
    @QtCore.pyqtSlot(str)    
    def insertImage(self, image):
        url = QtCore.QUrl(image)
        image =  url.toLocalFile()
        imageSize = self.getImageSize(image)
        width = imageSize.width()
        height = imageSize.height()
        if width > self.maxWidth:
            height = height * (self.maxWidth / float(width))            
            width = self.maxWidth
            
        # imageFormat = QtGui.QTextImageFormat()    
        # imageFormat.setName(image)
        # imageFormat.setWidth(width)
        # imageFormat.setHeight(height)
        # self._textCursor.insertImage(imageFormat)
        self._textCursor.insertHtml('<img src="{0}" width="{1}" height="{2}" />'.format(image, width, height))
        
    def getImageSize(self, url):    
        im = Image.open(url)
        size_ = QtCore.QSize(*im.size)
        del im
        return size_
        
    @QtCore.pyqtSlot(str)    
    def insertText(self, text):
        self._textCursor.insertText(text)
        
    @QtCore.pyqtSlot(str)
    def insertHtml(self, html):
        self._textCursor.insertHtml(html)
        
    def cursorForPosition(self, point):    
        cursorPos = self._textDocument.documentLayout().hitTest(point, QtCore.Qt.FuzzyHit)
        if cursorPos == -1:
            cursorPos = 0
        c = QtGui.QTextCursor(self._textDocument)
        c.setPosition(cursorPos)
        return c
    

    @QtCore.pyqtSlot(int, int)
    def testCursor(self, width, height):
        point = QtCore.QPoint(width, height)
        textCursor = self.cursorForPosition(point)
        fmt = textCursor.charFormat()
        if fmt.isImageFormat():
            ifmt = fmt.toImageFormat()
            print(ifmt.name())
            
    def mousePressEvent(self, event):        
        self.testCursor(event.x(), event.y())
        event.setAccepted(False)
        
    # def mouseMoveEvent(self, event):
    #     print "moveEvent"
    #     self.testCursor(event.x(), event.y())
    #     event.setAccepted(False)
        
    # def hoverMoveEvent(self, event):    
    #     print "hoverMoveEvent"
    #     event.setAccepted(False)
