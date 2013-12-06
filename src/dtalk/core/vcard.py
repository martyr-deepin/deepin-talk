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


VCARD_NS = "{vcard-temp}"
VCARD_TAG = VCARD_NS + "vCard"

from pyxmpp2.etree import ElementTree as ET
from pyxmpp2.interfaces import StanzaPayload, payload_element_name
from pyxmpp2.xmppserializer import serialize

def get_element_tag(element):
    return element.tag.strip().strip(VCARD_NS)

class TagNotMatch(Exception):
    pass

VCARD_FIELDS = {}

class VcardType(type):
    def __new__(cls, cls_name, bases, attrs):
        new_cls = super(VcardType, cls).__new__(cls, cls_name, bases, attrs)
        tag = attrs.get("TAG", None)
        if tag and tag not in VCARD_FIELDS:
            VCARD_FIELDS[tag] = new_cls
        return new_cls        
                

class BaseString(object):    
    TAG = ""
    __metaclass__ = VcardType
    
    def __init__(self, value=None):
        self.value = value
        
    @classmethod
    def from_xml(cls, element):
        tag = get_element_tag(element)
        if tag != cls.TAG:
            raise TagNotMatch
        return cls(value=element.text)
    
    def as_xml(self, parent=None):
        if parent is not None:
            element = ET.SubElement(parent, VCARD_NS+self.TAG)
        else:    
            element = ET.Element(VCARD_NS+self.TAG)
        element.text = self.value 
        return element
    
    
class BaseField(object):    
    TAG = ""
    CHILD_TAGS = ()
    __metaclass__ = VcardType
        
    def __init__(self, **kwargs):
        for k in self.CHILD_TAGS:
            setattr(self, k.lower(), None)
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    @classmethod    
    def from_xml(cls, element):
        result = dict()
        for child in element:        
            tag = get_element_tag(child)
            value = child.text
            if tag in cls.CHILD_TAGS:
                result[tag.lower()] = value
        return cls(**result)        
    
    def as_xml(self, parent=None):
        if parent is not None:
            element = ET.SubElement(parent, VCARD_NS+self.TAG)
        else:    
            element = ET.Element(parent, VCARD_NS+self.TAG)
        for tag in self.CHILD_TAGS:    
            child = ET.SubElement(element, VCARD_NS+tag)
            child.text = getattr(self, tag.lower())
        return element    
    
    
class FN(BaseString):    
    TAG = "FN"
    
class Name(BaseField):    
    TAG = "N"    
    CHILD_TAGS = ("FAMILY", "GIVEN", "MIDDLE", "PREFIX", "SUFFIX")
    
class Nickname(BaseString):
    TAG = "NICKNAME"
    
class Photo(BaseField):    
    TAG = "PHOTO"
    CHILD_TAGS = ("TYPE", "BINVAL", "EXTVAL")
    
class Bday(BaseString):
    TAG = "BDAY"
    
 
@payload_element_name(VCARD_TAG)
class VCardPayload(StanzaPayload):
    
    def __init__(self, **kwargs):
        for key in VCARD_FIELDS:
            setattr(self, key.lower(), None)
        for k, v in kwargs.items():
            if k.upper() in VCARD_FIELDS: 
                setattr(self, k, v)
            
    @classmethod
    def from_xml(cls, element):
        result = {}
        if element.tag != VCARD_TAG:
            raise ValueError("{0!r} is not a vcard item".format(element))
        for child in element:        
            tag = get_element_tag(child)
            if tag in VCARD_FIELDS:
                result[tag.lower()] = VCARD_FIELDS[tag].from_xml(child)
        return cls(**result)        
    
    def as_xml(self):
        element = ET.Element(VCARD_TAG)
        for key in VCARD_FIELDS:
            child = getattr(self, key.lower(), None)
            if child:
                child.as_xml(element)
        return element
    
    def serialize(self):
        return serialize(self.as_xml())
    
    def get_nickname(self):
        if self.nickname is not None:
            nickname = self.nickname.value
            if nickname: 
                return nickname
        if self.fn is not None:    
            return self.fn.value
        return None    
    
    def get_avatar(self):
        if self.photo is not None:
            return self.photo.binval
        return None
        
        
