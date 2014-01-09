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


import os
from PyQt5 import QtQuick, QtQml, QtGui
from dtalk.utils.xdg import program_dir

EXPRESSION_DIR = os.path.join(program_dir, "dtalk", 'views', "expression")


class DefaultProvider(QtQuick.QQuickImageProvider):
    
    NAME = "qq"
    DIRPATH = os.path.join(EXPRESSION_DIR, "QQexpression")
    
    def __init__(self):
        super(DefaultProvider, self).__init__(QtQml.QQmlImageProviderBase.ImageType)
        
    def requestImage(self, imageId, size, requestSize):    
        return QtGui.QImage(self.getExpression(imageId))
    
    @classmethod
    def getAllUrls(cls):
        pass
    
    @classmethod    
    def getExpression(cls, imageId):
        return os.path.join(cls.DIRPATH, imageId)
        
        
