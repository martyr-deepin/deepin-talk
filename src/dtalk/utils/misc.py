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

import sys

def setdefaultencoding(encoding):
    """
    Set the current default string encoding used by the Unicode implementation.

    Actually calls sys.setdefaultencoding under the hood - see the docs for that
    for more details.  This method exists only as a way to call find/call it
    even after it has been 'deleted' when the site module is executed.

    :param string encoding: An encoding name, compatible with sys.setdefaultencoding
    """
    func = getattr(sys, 'setdefaultencoding', None)
    if func is None:
        import gc
        import types
        for obj in gc.get_objects():
            if (isinstance(obj, types.BuiltinFunctionType)
                    and obj.__name__ == 'setdefaultencoding'):
                func = obj
                break
        if func is None:
            raise RuntimeError("Could not find setdefaultencoding")
        sys.setdefaultencoding = func
    return func(encoding
)


class Storage(dict):
    def __getattr__(self, key): 
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __setattr__(self, key, value): 
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __repr__(self):     
        return '<Storage ' + dict.__repr__(self) + '>'

