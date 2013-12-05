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

import logging
from collections import defaultdict

from pyxmpp2.jid import JID
from pyxmpp2.iq import Iq
from pyxmpp2.message import Message
from pyxmpp2.client import Client
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.interfaces import XMPPFeatureHandler
from pyxmpp2.interfaces import message_stanza_handler, presence_stanza_handler
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent
from pyxmpp2.roster import RosterReceivedEvent, RosterUpdatedEvent
from pyxmpp2.mainloop.threads import ThreadPool        

logging.basicConfig(level = logging.INFO) # change to 'DEBUG' to see more
logger = logging.getLogger(__name__)

from pyxmpp2.interfaces import StanzaPayload, payload_element_name

from vcard import VCardPayload

class Poster(EventHandler, XMPPFeatureHandler):
    
    def __init__(self, my_jid, password):
        self.my_jid = JID(my_jid)
        settings = XMPPSettings({
                "tls_verify_peer": False,
                "starttls": True,
                "poll_interval": 10,
                "password" : password,
        })

        self.main_loop = ThreadPool(settings)
        self.client = Client(self.my_jid, [self,], settings, main_loop=self.main_loop)
        self.presence = defaultdict(dict)
        self.is_authored = False
        
    def run(self):    
        self.client.connect()
        self.client.run()
        self.main_loop.start(True)
        print "runing"
        
    def disconnect(self):    
        self.client.disconnect()
        self.client.run(timeout=2)
        
    def send_message(self, target_jid, message, message_type="chat", thread=None):    
        message = Message(to_jid=JID(target_jid), body=message, stanza_type=message_type,
                          thread=thread)
        self.client.stream.send(message)
        
    @message_stanza_handler()
    def handle_message(self, stanza):
        """Echo every non-error ``<message/>`` stanza.
        
        Add "Re: " to subject, if any.
        """
        if stanza.subject:
            subject = u"Re: " + stanza.subject
        else:
            subject = None
        msg = Message(stanza_type = stanza.stanza_type,
                        from_jid = stanza.to_jid, to_jid = stanza.from_jid,
                        subject = subject, body = stanza.body,
                        thread = stanza.thread)
        return msg
        print stanza.body
        # self.send_message(stanza.from_jid, stanza.body)
        
    @event_handler(AuthorizedEvent)
    def handle_authorized(self, event):
        self.is_authored = True
        
    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        self.is_authored = False
        return QUIT
    
    @event_handler(RosterReceivedEvent)
    def handle_roster_received(self, event):
        self.print_roster()
        
    @presence_stanza_handler()
    def handle_presence_available(self, stanza):
        if stanza.stanza_type not in ("available", None):
            return
        print "##################"
        print "available"
        
        
    def print_roster(self):
        roster = self.client.roster  # event.roster would also do
        print "Roster received:"
        if roster.version is None:
            print u"  (not versioned)"
        else:
            print u"  Version: '{0}'".format(roster.version)
        if len(roster):
            print u"  Items:"
            for item in roster.values():
                self.print_item(item)
        
    def print_item(self, item):
        print "#############################################"
        print u"    JID: {0}".format(item.jid)
        print " resource: ", item.jid.resource
        # print self.get_vcard(item.jid)
        print u"    Name: {0}".format(item.name)
        print u"    Subscription: {0}".format(item.subscription)
        print u"    Pending {0}".format(item.ask)
        print u"    Approved"
        if item.groups:
            groups = u",".join(
                            [u"'{0}'".format(g) for g in item.groups])
            print u"    Groups: {0}".format(groups)
        presences = self.presence.get(item.jid)
        if not presences:
            print u"    OFFLINE"
        else:
            print u"    ONLINE:"
            for jid, presence in presences.items():
                if presence.show:
                    show = u": [{0}]".format(presence.show)
                elif not presence.status:
                    show = u""
                else:
                    show = u":"
                if presence.status:
                    status = u" '{0}'".format(presence.status)
                else:
                    status = u""
                print u"      /{0}{1}{2}".format(jid.resource, show, status)
    
    
    
    @event_handler()
    def hanlde_all(self, event):
        logging.info(u"-- {0}".format(event))
        
    def get_vcard(self, jid, callback=None):
        if not callback:
            callback = self.vcard_callback
        q = Iq(
            to_jid = jid.bare(),
            stanza_type = 'get'
            )
        # vc = ET.Element("{vcard-temp}vCard")
        q.add_payload(VCardPayload())
        self.stanza_processor.set_response_handlers(q, callback, callback)
        self.send(q)        
        
    def vcard_callback(self, arg):    
        # print arg.serialize()
        t =  arg.get_payload(VCardPayload)
        if t:
            print t.get("name")
        
        
    def send(self, stanza):
        self.client.stream.send(stanza)        
        
