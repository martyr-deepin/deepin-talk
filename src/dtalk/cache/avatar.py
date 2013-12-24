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
import base64
import logging

import dtalk.conf
from dtalk.utils.xdg import get_avatar_dir, get_qml
from dtalk.utils import crypto
from dtalk.cache.signals import avatar_saved

logger = logging.getLogger("dtalk.cache.avatar")

class AvatarManager(object):
    
    def __init__(self):
        self.default_avatar = "qrc:/images/common/face.jpg"
    
    @classmethod
    def base64encode(cls, path):
        with open(path, 'rb') as fp:
            data = fp.read()
            return base64.b64encode(data).decode("ascii")
        
    @classmethod
    def base64decode(cls, data):
        return base64.decodestring(data)
    
    def has_avatar(self, jid):
        return self.get_avatar(jid) != self.default_avatar
    
    def get_avatars(self, jid):
        jid_md5 = crypto.get_md5(jid)
        avatar_files = filter(lambda p: p.startswith(jid_md5), os.listdir(self.avatar_dir))
        full_path_files = [ os.path.join(self.avatar_dir, f) for f in avatar_files ]
        return sorted(full_path_files, key=lambda item: os.path.getmtime(item), reverse=True)
    
    def get_avatar(self, jid, sha1hash=None):

        if sha1hash:
            jid_md5 = crypto.get_md5(jid)
            path = os.path.join(self.avatar_dir, "%s_%s" % (jid_md5, sha1hash))            
            if os.path.exists(path):
                return path
            return self.default_avatar
        else:    
            avatars = self.get_avatars(jid)
            if len(avatars) == 0:
                return self.default_avatar
            else:
                return avatars[0]
            
    def avatar_filepath(self, jid, sha1hash, need_hash=False):
        return os.path.join(self.avatar_dir, self.format_filename(jid, sha1hash, need_hash=need_hash))
                        
    def format_filename(self, jid, sha1hash, need_hash=False):        
        if need_hash:
            sha1hash = crypto.sha1hash(sha1hash)
        return "%s_%s" % (crypto.get_md5(jid), sha1hash)
            
    @property       
    def avatar_dir(self):    
        owner_jid = dtalk.conf.OWNER_JID
        if owner_jid is None:
            logger.warning("AvatarManager must be run after logged in")
            raise RuntimeError("AvatarManager must be run after logged in")
        return get_avatar_dir(owner_jid)

    def save_avatar(self, jid, base64data):
        before_avatar = self.get_avatar(jid)
        if before_avatar != self.default_avatar:
            os.remove(before_avatar)
            
        image_data = self.base64decode(base64data)
        path = self.avatar_filepath(jid, image_data, need_hash=True)
        if os.path.exists(path):
            return 
        with open(path, 'wb') as fp:
            fp.write(image_data)
        logger.debug("{0} avatar have saved".format(jid))    
        avatar_saved.send(sender=self, jid=jid, path=path)    
        
    def check_avatar(self, jid, sha1hash, need_hash=False):    
        path = self.avatar_filepath(jid, sha1hash, need_hash=need_hash)
        if os.path.exists(path):
            return True
        return False
            
avatarManager = AvatarManager()
