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
from collections import defaultdict

from pyxmpp2.jid import JID
from pyxmpp2.message import Message
from pyxmpp2.client import Client
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.interfaces import XMPPFeatureHandler
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent
from pyxmpp2 import exceptions
from pyxmpp2.mainloop.threads import ThreadPool        

from dtalk.core.roster import RosterMixin
from dtalk.models import init_db
from dtalk.core import signals
import dtalk.conf

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.DEBUG) # change to 'DEBUG' to see more
# logging.basicConfig(level = logging.INFO) # change to 'DEBUG' to see more
# logging.basicConfig(filename="/home/evilbeast/myap.log", level = logging.DEBUG) # change to 'DEBUG' to see more

class XMPPServer(RosterMixin, EventHandler, XMPPFeatureHandler):
    
    def __init__(self):
        RosterMixin.__init__(self)
        self.presence = defaultdict(dict)        
        
    def run(self):    
        self.client.connect()
        self.client.run()
        self.main_loop.start(True)
        
    def init_server(self, jid, password):    
        self.my_jid = JID(jid)
        self.settings = XMPPSettings({
                "tls_verify_peer": False,
                "starttls": True,
                "poll_interval": 10,
                "password" : password,
        })

        self.main_loop = ThreadPool(self.settings)
        self.client = Client(self.my_jid, [self,], self.settings, main_loop=self.main_loop)
        self.is_authored = False
        
        
    def login(self, jid, password):    
        self.plain_jid = jid        
        dtalk.conf.OWNER_JID = jid
        init_db(self.plain_jid)        
        self.init_server(jid, password)

        try:
            self.run()
        except:    
            self.disconnect()
            signals.user_login_failed.send(sender=self, jid=self.plain_jid)
        
    def logout(self):    
        signals.user_logged_out.send(sender=self, jid=self.plain_jid)        
        
    def disconnect(self):    
        self.client.disconnect()        
        self.client.run(timeout=2)        
        self.main_loop.stop(join=True)
        
    def send_message(self, target_jid, message, message_type="chat", thread=None):    
        message = Message(to_jid=JID(target_jid), body=message, stanza_type=message_type,
                          thread=thread)
        self.client.stream.send(message)
        
    send = property(lambda self: self.client.stream.send)
    owner_jid = property(lambda self: self.client.jid)
    
    @event_handler(AuthorizedEvent)
    def handle_authorized(self, event):
        signals.user_login_successed.send(sender=self, jid=self.plain_jid)
        self.is_authored = True
        
    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        signals.server_disconnected.send(sender=self)
        self.is_authored = False
        return QUIT
    
    @event_handler()
    def hanlde_all(self, event):
        logging.info(u"-- {0}".format(event))
