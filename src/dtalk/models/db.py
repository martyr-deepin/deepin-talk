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

from peewee import Model as _Model
from dtalk.models import signals 

class Model(_Model):
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        signals.pre_init.send(sender=self.__class__, instance=self)

    def prepared(self):
        super(Model, self).prepared()
        signals.post_init.send(sender=self.__class__, instance=self)

    def save(self, *args, **kwargs):
        created = not bool(self.get_id())
        signals.pre_save.send(sender=self.__class__, instance=self, created=created)
        super(Model, self).save(*args, **kwargs)
        signals.post_save.send(sender=self.__class__, instance=self, created=created)
        
    def delete_instance(self, *args, **kwargs):
        signals.pre_delete.send(sender=self.__class__, instance=self)
        super(Model, self).delete_instance(*args, **kwargs)
        signals.post_delete.send(sender=self.__class__, instance=self)

