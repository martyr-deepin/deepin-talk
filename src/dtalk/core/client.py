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

from pyxmpp2.client import Client, _move_session_handler
from pyxmpp2.stanzaprocessor import StanzaProcessor
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.roster import RosterClient
from pyxmpp2.streamevents import AuthorizedEvent
from pyxmpp2.interfaces import event_handler


class QClient(Client):
    
    def __init__(self, jid, handlers, settings=None, main_loop=None):
        
        self._ml_handlers = []
        self._base_handlers = []
        self.jid = jid
        self.handlers = handlers
        self.settings = settings if settings else XMPPSettings()
        
        StanzaProcessor.__init__(self, self.settings[u"default_stanza_timeout"])
        self.roster_client = self.roster_client_factory()                
        self.main_loop = main_loop
        self.stream = None

    def setup_handlers(self, handlers=None):    

        self._base_handlers = self.base_handlers_factory()
        self._base_handlers += [self.roster_client]
        
        self._ml_handlers += list(self.handlers) + self._base_handlers + [self]
        
        _move_session_handler(self._ml_handlers)
        
        for handler in self._ml_handlers:
            self.main_loop.add_handler(handler)
            
    def connect(self):        
        self.clear_handlers()
        self.setup_handlers()
        super(QClient, self).connect()
        
    def clear_handlers(self):    
        for handler in self._ml_handlers:
            self.main_loop.remove_handler(handler)
        del self._ml_handlers[:]    
        del self._base_handlers[:]
        
    def roster_client_factory(self):
        return QRosterClient(self.settings)
        
class QRosterClient(RosterClient):        
    
    @event_handler(AuthorizedEvent)
    def handle_authorized_event(self, event):
        self.server = event.authorized_jid.bare()
        if "versioning" in self.server_features:
            if self.roster is not None and self.roster.version is not None:
                version = self.roster.version
            else:
                version = u""
        else:
            version = None
        self.version = version    
        
    def delay_request_roster(self):    
        version = getattr(self, 'version', None)
        self.request_roster(version)
