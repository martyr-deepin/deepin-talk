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
import sleekxmpp    
import logging
import threading


from sleekxmpp.exceptions import IqError, IqTimeout
from dtalk.models import signals as db_signals
from dtalk.models import SendedMessage, ReceivedMessage, Friend
from dtalk.xmpp import signals as xmpp_signals

from dtalk.models import init_db
import dtalk.utils.xdg
from dtalk.utils.threads import threaded

logger = logging.getLogger("dtalk.xmpp")
    
class BaseMessage(object):    
    
    def __init__(self):
        
        db_signals.post_save.connect(self.on_message_sended_from_db, sender=SendedMessage)
        self.add_event_handler("message", self.on_message_received)        
        
    def on_message_sended_from_db(self, sender, instance, created, *args, **kwargs):
        self.send_message(mto=instance.friend.jid,
                          mbody=instance.body,
                          mtype='chat')
    
    def on_message_received(self, msg):
        if msg['type'] == "chat":
            ReceivedMessage.received_message_from_sleek(msg)
            
class BaseRoster(object):            
    
    # @threaded
    def request_roster(self):
        self.get_roster()
        self.send_presence()
    
    def process_all_roster(self):
        Friend.create_or_update_roster_sleek(self.client_roster)
            
class BaseVCard(object):            
    
    def __init__(self):
        self.add_event_handler("vcard_avatar_update", self._on_vcard_avatar)        
        
    def _on_vcard_avatar(self, pres):    
        logger.info("Received vCard avatar update from {0}. Asking for vcard".format(pres['from'].bare))
        self.plugin['xep_0054'].get_vcard(pres['from'], block=False, callable=self._on_vcard_get)
        
    def _on_vcard_get(self, stanza):    
        vcard_temp = stanza.get("vcard_temp")
        jid = stanza.get_from().bare
        logger.info("Received vCard from {0}".format(jid))
        
        photo = vcard_temp['PHOTO']
        if not photo:
            return
        photo_bin = photo.get("BINVAL")
        if not photo_bin:
            return
        
        # photo_hash = hashlib.sha1()
        # photo_hash.update(photo_bin)
        # photo_hash = photo_hash.hexdigest()
        
class BaseClient(sleekxmpp.ClientXMPP, BaseMessage, BaseRoster, BaseVCard):    
    
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        
        self.process(block=False)
        
        self.register_plugin("xep_0004") # Data Forms
        self.register_plugin("xep_0030") # Service Discovery
        # self.register_plugin("xep_0054") # vcard-temp
        # self.register_plugin("xep_0153")
        self.register_plugin("xep_0060") # pubsub
        
        BaseMessage.__init__(self)
        BaseRoster.__init__(self)
        BaseVCard.__init__(self)
        
        # event handlers.
        self.add_event_handler("session_start", self._on_session_start)
        self.add_event_handler("disconnected", self._on_disconnected)
        self.add_event_handler("failed_auth", self._on_failed_auth)
        self.add_event_handler("auth_success", self._on_auth_success)
        self.use_ipv6 = False
        
    def _handle_roster(self, iq):        
        sleekxmpp.ClientXMPP._handle_roster(self, iq)
        self.process_all_roster()                
        
    def _on_session_start(self, event):   
        self.request_roster()
        
    def _on_disconnected(self, event):    
        xmpp_signals.session_disconnected.send(sender=self)
        
    def _on_failed_auth(self, direct):    
        xmpp_signals.auth_failed.send(sender=self)
        
    def _on_auth_success(self, direct=False):    
        
        # init db.
        self.initial_db()
        
        # send auth successed signal.
        xmpp_signals.auth_successed.send(sender=self, jid=self.boundjid.bare)
        
    def initial_db(self):    
        jid = self.boundjid.bare
        dtalk.conf.xdg.OWNER_JID = jid
        init_db(jid)
    
    def run_service(self):    
        self.connect()
            
    def action_logout(self):        
        self.disconnect(wait=True)
