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

import copy
from PyQt5 import QtCore
from dtalk.utils import six
from dtalk.controls.qobject import QObjectListModel, QPropertyMeta
from dtalk.models import BaseModel
from dtalk.models import signals


def string_title(name):
    names = name.split("_")
    lasts = "".join(map(lambda name: name.title(), names[1:]))
    return "%s%s" % (names[0], lasts)


class WrapperModelMeta(QtCore.pyqtWrapperType):
    
    def __new__(cls, cls_name, bases, cls_dict):
        super_new = super(WrapperModelMeta, cls).__new__
        _db =  cls_dict.get("db", None)
        if _db is not None:
            fields = _db._meta.fields
            roles = dict()
            for idx, key in enumerate(fields.keys()):
                val = QtCore.Qt.UserRole + (idx+1)
                name_title = string_title(key)
                cls_dict[name_title+"Role"] = val
                roles[val] = key
            cls_dict["_roles"] = roles                
                
        return super_new(cls, cls_name, bases, cls_dict)    
    
    
def get_instance_dict(instance, result=None, key_profix="", other_fields=None, level=1):    
    if result is None:
        result = dict()
        
    keys = copy.deepcopy(instance._meta.fields.keys())
    
    if other_fields is not None:
        keys.extend(list(other_fields))
        keys = set(keys)
    for key in keys:
        value = getattr(instance, key, None)
        if value is None:
            value = ""
        if key_profix != "":
            key = key.title()
        if isinstance(value, BaseModel) and level != 0:
            get_instance_dict(value, result, key_profix="%s%s" % (key_profix, key), other_fields=None, level=level-1)
        elif isinstance(value, dict):
            for k, v in six.iteritems(value):
                result["%s%s%s" % (key_profix, key, k.title())] = v
        else:
            result["%s%s" % (key_profix, key)] = value
    return result        

        
def get_qobject_wrapper(instance, unique_obj, other_fields=None):    
    result = get_instance_dict(instance, other_fields=other_fields)
    class WrapperQuery(six.with_metaclass(QPropertyMeta, QtCore.QObject)):
        __qtprops__ = result
        
        def __eq__(self, other):
            has = hasattr(self, unique_obj) and hasattr(other, unique_obj)
            if not has:
                return False
            return getattr(self, unique_obj) == getattr(other, unique_obj)
        
        def __ne__(self, other):
            return not self == other
    return WrapperQuery()    

class AbstractWrapperModel(QObjectListModel):
    
    dbs = None                  # ('db',)
    unique_obj = ""
    other_fields = None         # ('key',)
    init_signals_on_db_finished = True
    instanceRole = QtCore.Qt.UserRole + 1
    _roles = { instanceRole : "instance" }
        
    def __init__(self, parent=None):
        super(AbstractWrapperModel, self).__init__(parent)
        self._data = []
        signals.db_init_finished.connect(self.on_db_init_finished)
        
    def load(self):    
        pass
    
    def on_db_init_finished(self, *args, **kwargs):
        self.initData(self.init_signals_on_db_finished)
    
    def initData(self, init_signals=True):
        if init_signals:
            self.init_signals()
        data = self.load()
        if data:
            instances = list(map(self.wrapper_instance, data))
            self.setAll(instances)
    
    def verify(self, obj):
        return True
    
    def wrapper_instance(self, instance):
        return get_qobject_wrapper(instance, self.unique_obj, self.other_fields)
    
    def init_signals(self):
        pass
    
    def init_wrappers(self):
        if self._data:
            self._data = list(map(self.wrapper_instance, self._data))
        
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size:
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        if role == self.instanceRole:
            return item
        return QtCore.QVariant()        
