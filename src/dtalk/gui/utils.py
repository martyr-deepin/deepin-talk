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

import sys
import traceback
from PyQt5 import QtCore, QtWidgets, QtGui
from dtalk.utils.xdg import get_qss
from dtalk.utils.six import text_type
from contextlib import contextmanager 


def setObjectTransparent(obj):
    obj.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
    
def loadStyleSheet():
    f = get_qss("dtalk.css")
    styleSheet = None
    with open(f) as fp:
        content = fp.read()
        styleSheet = text_type(content, encoding='utf8')
    if styleSheet is not None:    
        QtWidgets.QApplication.instance().setStyleSheet(styleSheet)

        
@contextmanager
def disableAntialias(painter):
    renderHints = painter.renderHints()
    painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
    try:  
        yield  
    except Exception, e:  
        print('function cairo_disable_antialias got error: %s' % e)
        traceback.print_exc(file=sys.stdout)
    else:  
        # Restore antialias.
        painter.setRenderHints(renderHints)
        
def getObjectWidget(name, widget=QtWidgets.QPushButton):        
    button = widget()
    button.setObjectName(name)
    return button

def createProxyWidget(widget, minimum=None, preferred=None, maximum=None):
    w = QtWidgets.QGraphicsProxyWidget()
    w.setWidget(widget)
    if minimum is not None:
        w.setMinimumSize(minimum)
    if preferred is not None:    
        w.setPreferredSize(preferred)
    if maximum is not None:    
        w.setMaximumSize(maximum)
    return w    


def qimageToBase64(image, imageType):
    imageAsByteArray = QtCore.QByteArray()
    imageBuffer = QtCore.QBuffer(imageAsByteArray)
    imageBuffer.open(QtCore.QIODevice.WriteOnly)
    image.save(imageBuffer, imageType)
    return str(imageAsByteArray.toBase64())

        
        
