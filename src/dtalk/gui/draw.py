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

from PyQt5 import QtCore, QtGui

def drawRectWidthCorner(painter, rect,
                        position=QtCore.Qt.LeftEdge, 
                        shadowHeight=0, 
                        marginWidth=30,
                        cornerHeight=10,
                        cornerWidth=12,
                        cornerOffset=0.5,
                        isHalf=False,
                        radius=5,
                        ):
    r = 2 * radius
    x = rect.x() + marginWidth
    y = rect.y() + marginWidth
    w = rect.width() - marginWidth * 2 - shadowHeight
    h = rect.height() - marginWidth * 2 - shadowHeight

    path = QtGui.QPainterPath()
    
    if position == QtCore.Qt.LeftEdge:
        x += cornerHeight
        w -= cornerHeight
        path.moveTo(x+w, y+r)
        path.arcTo(x+w-r, y, r, r, 0.0, 90.0)
        path.lineTo(x+r, y)
        path.arcTo(x, y, r, r, 90.0, 90.0)
        
        centerOffsetY = y + h * cornerOffset
        if isHalf:
            bottomStartY = centerOffsetY - cornerWidth / 2
        else:    
            bottomStartY = centerOffsetY
        path.lineTo(x, centerOffsetY-cornerWidth/2)            
        path.lineTo(x-cornerHeight, bottomStartY)
        path.lineTo(x, centerOffsetY+cornerWidth/2)
        path.lineTo(x, y+h-r)
        
        path.arcTo(x, y+h-r, r, r, 180.0, 90.0)
        path.lineTo(x+w-r, y+h);
        path.arcTo(x+w-r, y+h-r, r, r, 270.0, 90.0);
        path.lineTo(x+w, y+r) # or path.closeSubpath()
        
    elif position == QtCore.Qt.RightEdge:    
        w -= cornerHeight
        path.moveTo(x+w, y+r)
        path.arcTo(x+w-r, y, r, r, 0.0, 90.0)
        path.lineTo(x+r, y)
        
        path.arcTo(x, y, r, r, 90.0, 90.0)
        path.lineTo(x, y+h-r)
        
        path.arcTo(x, y+h-r, r, r, 180.0, 90.0)
        path.lineTo(x+w-r, y+h)
        path.arcTo(x+w-r, y+h-r, r, r, 270.0, 90.0)
        
        centerOffsetY = y + h * cornerOffset
        if isHalf:
            bottomStartY = centerOffsetY - cornerWidth / 2
        else:    
            bottomStartY = centerOffsetY

        path.lineTo(x+w, centerOffsetY+cornerWidth/2 )                            
        path.lineTo(x+w+cornerHeight, bottomStartY)
        path.lineTo(x+w, centerOffsetY-cornerWidth/2)        
        path.lineTo(x+w, y+r)
        
    elif position == QtCore.Qt.TopEdge:    
        y += cornerHeight
        h -= cornerHeight
        path.moveTo(x+w, y+r)
        path.arcTo(x+w-r, y, r, r, 0.0, 90.0)
        
        centerOffsetX = x + w * cornerOffset
        if isHalf:
            rightStartX = centerOffsetX - cornerWidth / 2
        else:    
            rightStartX = centerOffsetX

        path.lineTo(centerOffsetX+cornerWidth/2, y)                    
        path.lineTo(rightStartX, y-cornerHeight)
        path.lineTo(centerOffsetX-cornerWidth/2, y)                
        path.lineTo(x+r, y)
        
        path.arcTo(x, y, r, r, 90.0, 90.0)
        path.lineTo(x, y+h-r)
        
        path.arcTo(x, y+h-r, r, r, 180.0, 90.0);
        path.lineTo(x+w-r, y+h);
        path.arcTo(x+w-r, y+h-r, r, r, 270.0, 90.0);
        path.lineTo(x+w, y+r)
        
    elif position == QtCore.Qt.BottomEdge:    
        h -= cornerHeight
        path.moveTo(x+w, y+r)
        path.arcTo(x+w-r, y, r, r, 0.0, 90.0)
        path.lineTo(x+r, y)
        
        path.arcTo(x, y, r, r, 90.0, 90.0)
        path.lineTo(x, y+h-r)
        
        path.arcTo(x, y+h-r, r, r, 180.0, 90.0);
        
        centerOffsetX = x + w * cornerOffset
        if isHalf:
            rightStartX = centerOffsetX - cornerWidth / 2
        else:    
            rightStartX = centerOffsetX
        path.lineTo(centerOffsetX-cornerWidth/2, y+h)                            
        path.lineTo(rightStartX, y+h+cornerHeight)
        path.lineTo(centerOffsetX+cornerWidth/2, y+h)        
        path.lineTo(x+w-r, y+h)
        path.arcTo(x+w-r, y+h-r, r, r, 270.0, 90.0);
        path.lineTo(x+w, y+r)
        
    return path, QtCore.QRect(x, y, w, h)    

def drawCornerImage(painter, image, rect):
    image = image.strip("qrc")    
    
    painter.save()
    path = QtGui.QPainterPath()
    path.addRoundedRect(QtCore.QRectF(rect), rect.width()/2.0, rect.height()/2.0)
    painter.setClipPath(path)
    painter.drawPixmap(rect, QtGui.QPixmap(image))
    painter.restore()
    
    
    
    
