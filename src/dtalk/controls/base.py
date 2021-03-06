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

from PyQt5 import QtCore
from dtalk.utils import six
from dtalk.controls.qobject import QObjectListModel, QPropertyMeta, postGui, ObjectWrapper
from dtalk.models.db import Model
from dtalk.models import signals, user_db

def string_title(name):
    names = name.split("_")
    lasts = "".join(map(lambda name: name.title(), names[1:]))
    return "%s%s" % (names[0], lasts)

def peeweeWrapper(instance, others=None):
    params = instance.__dict__['_data']
    ret = {}
    for k, v in six.iteritems(params):
        ret[string_title(k)] = v
    ret.update(others)    
    return ObjectWrapper(ret)


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
        
    keys = list(instance.__dict__['_data'].keys())
    
    if other_fields is not None:
        keys.extend(list(other_fields))
        keys = set(keys)
    for key in keys:
        value = getattr(instance, key, None)
        if value is None:
            value = ""
        key = string_title(key)
        if key_profix != "":
            key = key.title()
        if isinstance(value, Model) and level != 0:
            get_instance_dict(value, result, key_profix="%s%s" % (key_profix, key), other_fields=None, level=level-1)
        elif isinstance(value, dict):
            for k, v in six.iteritems(value):
                result["%s%s%s" % (key_profix, key, k.title())] = v
        else:
            result["%s%s" % (key_profix, key)] = value
    return result        

        
def get_qobject_wrapper(instance, unique_field, other_fields=None):    
    result = get_instance_dict(instance, other_fields=other_fields)
    class WrapperQuery(six.with_metaclass(QPropertyMeta, QtCore.QObject)):
        __qtprops__ = result
        
        def __eq__(self, other):
            has = hasattr(self, unique_field) and hasattr(other, unique_field)
            if not has:
                return False
            return getattr(self, unique_field) == getattr(other, unique_field)
        
        def __ne__(self, other):
            return not self == other
    return WrapperQuery()    

class AbstractWrapperModel(QObjectListModel):
    _db = user_db
    unique_field = "id"
    other_fields = None         # ('key',)
    instanceRole = QtCore.Qt.UserRole + 1
    _roles = { instanceRole : "instance" }
        
    def __init__(self, parent=None, *args, **kwargs):
        super(AbstractWrapperModel, self).__init__(parent)
        self.db_is_created = False        
        self._data = []
        if self._db is not None:
            signals.db_init_finished.connect(self.on_db_init_finished, sender=self._db)        
        self.initial(*args, **kwargs)

    def load(self):    
        pass
    
    def initial(self):
        pass

    @postGui()
    def on_db_init_finished(self, created, *args, **kwargs):
        self.db_is_created = created        
        if not created:
            self.initData()
            self.init_signals()

    def initData(self, init_signals=True):
        data = self.load()
        if data:
            instances = list(map(self.wrapper_instance, data))
            self.setAll(instances)
    
    @classmethod        
    def wrapper_instance(cls, instance):
        cls.attach_attrs(instance)
        return get_qobject_wrapper(instance, cls.unique_field, cls.other_fields)
    
    def init_wrappers(self):
        if self._data:
            self._data = list(map(self.wrapper_instance, self._data))
        
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size():
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        if role == self.instanceRole:
            return item
        return QtCore.QVariant()        
    
    @classmethod
    def attach_attrs(cls, instance):
        pass
    
    def init_signals(self):
        pass
    
