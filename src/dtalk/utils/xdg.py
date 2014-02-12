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


import os
import time

from dtalk.utils.constant import PROGRAM_NAME
from dtalk.utils.crypto import get_md5

OWNER_JID = None

def get_parent_dir(filepath, level=1):
    parent_dir = os.path.realpath(filepath)
    
    while(level > 0):
        parent_dir = os.path.dirname(parent_dir)
        level -= 1
    
    return parent_dir


_home = os.path.expanduser("~")
lastdir = _home

data_home = os.environ.get('XDG_DATA_HOME') or os.path.join(_home, '.local', 'share')
data_home = os.path.join(data_home, PROGRAM_NAME)

config_home = os.environ.get('XDG_CONFIG_HOME') or os.path.join(_home, '.config')
config_home = os.path.join(config_home, PROGRAM_NAME)

cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')
cache_home = os.path.join(cache_home, PROGRAM_NAME)

config_dirs = []
data_dirs = []

program_dir = get_parent_dir(__file__, 3)

data_dirs.insert(0, data_home)
config_dirs.insert(0, config_home)

local_hack = False

# Detect if Program is not installed.
if os.path.exists(os.path.join(program_dir, 'setup.py')):
    local_hack = True
    
    # Insert the "data" directory to data_dirs.
    # data_dir = os.path.join(program_dir, 'data')
    # data_dirs.insert(0, data_dir)
    
    # insert the config dir
    # config_dir = os.path.join(program_dir, 'data', 'config')
    # config_dirs.insert(0, config_dir)


def get_config_dir():
    return config_home

def get_config_dirs():
    return config_dirs[:]

def get_data_dir():
    return data_home

def get_data_dirs():
    return data_dirs[:]

def _get_path(basedirs, *subpath_elements, **kwargs):
    check_exists = kwargs.get("check_exists", False)
    subpath = os.path.join(*subpath_elements)
    for d in basedirs:
        path = os.path.join(d, subpath)
        if not check_exists or os.path.exists(path):
            return path
    return None

def get_data_path(*subpath_elements, **kwargs):
    return _get_path(data_dirs, *subpath_elements, **kwargs)

def get_config_path(*subpath_elements, **kwargs):
    return _get_path(config_dirs, *subpath_elements, **kwargs)

def get_cache_path(*subpath_elements, **kwargs):
    return _get_path((cache_home,), *subpath_elements, **kwargs)

def get_last_dir():
    return lastdir

def get_qml(*subpath_elements):
    return os.path.join(program_dir, "dtalk", "views", "qml", *subpath_elements)

def get_qss(*subpath_elements):
    return os.path.join(program_dir, "dtalk", "views", "qss", *subpath_elements)


def get_jid_dir(jid=None):
    if jid is None:
        jid  = OWNER_JID
        
    if jid is None:
        raise RuntimeError("must be run after logged in")
    
    d =  get_config_path(get_md5(jid))
    return makedirs(d)

def makedirs(d):
    if not os.path.exists(d):
        os.makedirs(d)
    return d    

def get_jid_db(jid=None, name="data.db"):
    return os.path.join(get_jid_dir(jid), name)

def get_avatar_dir(jid=None):
    d = os.path.join(get_jid_dir(jid), 'avatar')
    return makedirs(d)

def get_screenshot_dir(jid=None):
    d = os.path.join(get_jid_dir(jid), "screenshots")
    return makedirs(d)

def generate_time_md5():
    t = str(time.time())
    return get_md5(t)

def get_uuid_screentshot_path():
    path = os.path.join(get_screenshot_dir(), generate_time_md5())
    while os.path.exists(path):
        path = os.path.join(get_screenshot_dir(), generate_time_md5())
    return path    
    
def _make_missing_dirs():
    """
        Make any missing base XDG directories

        called by the main Exaile object, should not be used elsewhere.
    """
    if not os.path.exists(data_home):
        os.makedirs(data_home)
    if not os.path.exists(config_home):
        os.makedirs(config_home)
    if not os.path.exists(cache_home):
        os.makedirs(cache_home)
