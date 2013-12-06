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


from pyxmpp2.etree import ElementTree as ET
from pyxmpp2.interfaces import StanzaPayload, payload_element_name
from pyxmpp2.xmppserializer import serialize as xmlserialize

VCARD_UPDATE_NS = "{vcard-temp:x:update}"
VCARD_UPDATE_TAG = VCARD_UPDATE_NS + "x"
VCARD_UPDATE_PHOTO_TAG = VCARD_UPDATE_NS + "photo"


@payload_element_name(VCARD_UPDATE_TAG)
class VCardUpdatePayload(StanzaPayload):
    
    def __init__(self, photo):
        self.photo = photo
        
    @classmethod    
    def from_xml(cls, element):
        child = element.find(VCARD_UPDATE_PHOTO_TAG)            
        if child is not None:
            photo = child.text
        else:    
            photo = None
        return cls(photo=photo)    
    
    def as_xml(self, parent=None):
        if parent is None:
            element = ET.Element(VCARD_UPDATE_TAG)
        else:    
            element = ET.SubElement(parent, VCARD_UPDATE_TAG)
        child = ET.SubElement(element, VCARD_UPDATE_PHOTO_TAG)    
        child.text = self.photo
        return element
    
    def serialize(self):
        return xmlserialize(self.as_xml())
