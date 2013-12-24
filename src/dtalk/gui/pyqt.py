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

from __future__ import print_function

import gc
from PyQt5.QtCore import QObject, QTimer

class GarbageCollector(QObject):
    
    INTERVAL = 500

    def __init__(self, parent=None, debug=False):
        super(GarbageCollector, self).__init__(parent)
        self.debug = debug
        self.timer = QTimer()
        self.timer.timeout.connect(self.check)
        self.threshold = gc.get_threshold()
        # gc.set_debug(gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_OBJECTS)
        gc.disable()
        self.timer.start(self.INTERVAL)

    def check(self):
        (l0, l1, l2,) = gc.get_count()
        if self.debug:
            print(u'gc_check called:', l0, l1, l2)
        if l0 > self.threshold[0]:
            num = gc.collect(0)
            if self.debug:
                print(u'collecting gen 0, found:', num, u'unreachable')
            if l1 > self.threshold[1]:
                num = gc.collect(1)
                if self.debug:
                    print(u'collecting gen 1, found:', num, u'unreachable')
                if l2 > self.threshold[2]:
                    num = gc.collect(2)
                    if self.debug:
                        print(u'collecting gen 2, found:', num, u'unreachable')

    def debug_cycles(self):
        gc.collect()
        for obj in gc.garbage:
            print(obj, repr(obj), type(obj))
