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

import logging
import socket
from collections import defaultdict

from pyxmpp2.jid import JID

from pyxmpp2.settings import XMPPSettings
from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.interfaces import XMPPFeatureHandler
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent
from pyxmpp2 import exceptions

# from dtalk.models import Friend
from dtalk.core.roster import RosterMixin
from dtalk.models import init_db
from dtalk.core import signals
from dtalk.models import signals as db_signals
from dtalk.core.mainloop import QThreadPool
from dtalk.core.client import QClient
import dtalk.utils.xdg

logger = logging.getLogger(__name__)
# logging.basicConfig(level = logging.DEBUG) # change to 'DEBUG' to see more
logging.basicConfig(level = logging.INFO) # change to 'DEBUG' to see more
# logging.basicConfig(filename="/home/evilbeast/myap.log", level = logging.DEBUG) # change to 'DEBUG' to see more

class XMPPServer(RosterMixin, EventHandler, XMPPFeatureHandler):
    
    def __init__(self):
        RosterMixin.__init__(self)
        self.presence = defaultdict(dict)        
        signals.raise_excepted.connect(self.on_received_raise_exception)
        db_signals.db_init_finished.connect(self.on_db_init_finished)
        
        self.settings = XMPPSettings({
                "tls_verify_peer": False,
                "starttls": True,
                "poll_interval": 10,
        })
        self.main_loop = QThreadPool(self.settings)
        self.client = QClient(None, [self,], self.settings, main_loop=self.main_loop)
        self.is_authored = False        
        
    def try_connect(self, jid, password):    
        self.my_jid = JID(jid)
        self.settings["password"] = password
        self.client.jid = self.my_jid
        self.client.connect()
        self.run_main_loop()
        
    def run_main_loop(self):    
        self.main_loop.run_loop()
        
    def login(self, jid, password):    
        self.plain_jid = jid        

        dtalk.conf.xdg.OWNER_JID = jid
        
        # init db
        self.try_connect(jid, password)
        
    def logout(self):    
        signals.user_logged_out.send(sender=self, jid=self.plain_jid)        
        
    def disconnect(self):    
        self.client.disconnect()        
        self.main_loop.stop(join=True)
        
    def initial_db(self):    
        init_db(self.plain_jid)
        
    send = property(lambda self: self.client.stream.send)
    owner_jid = property(lambda self: self.client.jid)
    
    @event_handler(AuthorizedEvent)
    def handle_authorized(self, event):
        
        # init db.
        self.initial_db()
        
        signals.user_login_successed.send(sender=self, jid=self.plain_jid)
        self.is_authored = True
        
    def on_db_init_finished(self, *args, **kwargs):    
        self.client.roster_client.delay_request_roster()
        
    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        signals.server_disconnected.send(sender=self)
        self.is_authored = False
        return QUIT
    
    @event_handler()
    def hanlde_all(self, event):
        logging.info(u"-- {0}".format(event))
        
    def on_received_raise_exception(self, exc_info, *args, **kwargs):    
        exc_type =  exc_info[0]
        if exc_type == exceptions.SASLAuthenticationFailed:
            signals.user_login_failed.send(sender=self, jid=self.plain_jid, reason="输入密码不对，请核对后再输")
        if exc_type == socket.error and not self.is_authored:
            signals.user_login_failed.send(sender=self, jid=self.plain_jid, reason="该帐号不存在")
        print exc_info    
