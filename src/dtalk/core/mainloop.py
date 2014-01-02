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

import Queue
import logging
import threading
from pyxmpp2.mainloop.threads import ThreadPool
from dtalk.core.signals import raise_excepted

logger = logging.getLogger("dtalk.mainloop.QThreadPool")

class QThreadPool(ThreadPool):
    
    def __init__(self, *args, **kwargs):
        super(QThreadPool, self).__init__(*args, **kwargs)
        self.loop_thread = None
    
    def loop_iteration(self, timeout = 0.1):
        """Wait up to `timeout` seconds, raise any exception from the
        threads.
        """
        try:
            exc_info = self.exc_queue.get(True, timeout)[1]
        except Queue.Empty:
            return
        # exc_type, exc_value, ext_stack = exc_info
        raise_excepted.send(sender=self, exc_info=exc_info)
    
    def run_loop(self, timeout=None):
        self.start(daemon=True)
        
        if self.loop_thread is not None and self.loop_thread.is_alive():
            logger.warning("loop_thread don't quit!!!!!!!!!!!!!!")
        self.loop_thread = threading.Thread(target=self.loop, args=(timeout,))
        self.loop_thread.daemon = True
        self.loop_thread.start()

