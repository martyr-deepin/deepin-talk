#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou ShaoHui
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

import sys
if sys.version_info < (3, 0):
    from dtalk.utils.misc import setdefaultencoding
    setdefaultencoding('utf8')

from PyQt5 import QtWidgets
import dtalk.views.resources_rc
import dtalk.gui.plugins
from dtalk.controls.panel import Panel

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.DEBUG) # change to 'DEBUG' to see more
# logging.basicConfig(level=logging.INFO) # change to 'DEBUG' to see more

if __name__ == "__main__":        
    from dtalk.gui.utils import loadStyleSheet
    app = QtWidgets.QApplication(sys.argv)
    loadStyleSheet()
    win = Panel()
    win.show()
    sys.exit(app.exec_())
