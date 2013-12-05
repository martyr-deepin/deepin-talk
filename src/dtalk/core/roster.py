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
from pyxmpp2.interfaces import presence_stanza_handler, event_handler
from pyxmpp2.roster import RosterReceivedEvent, RosterUpdatedEvent
from pyxmpp2.presence import Presence, ACCEPT_RESPONSES, DENY_RESPONSES
from pyxmpp2.jid import JID
from dtalk.models import Friend, Resource, FriendNotice
from dtalk.conf import settings
from dtalk.core import signals

logger = logging.getLogger("dtalk.core.RosterMixin")

class RosterMixin(object):
            
    def __init__(self):
        self._presences = []
        self.update_presence_flag = True
    
    @event_handler(RosterReceivedEvent)
    def handle_roster_received(self, event):
        rosters = self.client.roster.values()
        Friend.create_or_update_roster(rosters)
        signals.user_roster_received.send(sender=self)
        if self.update_presence_flag:
            self.client.main_loop.delayed_call(2, self.delayed_update_presence)        
        return True    
    
    @event_handler(RosterUpdatedEvent)
    def handle_roster_updated(self, event):
        item = event.item
        Friend.create_or_update_roster([ item ])
        return True
    
    @presence_stanza_handler()
    def handle_presence_available(self, stanza):
        if stanza.stanza_type not in ("available", None):
            return False
        if self.update_presence_flag:
            self._presences.append(stanza)        
        else:    
            Resource.update_status(stanza)
        return True    
        
    @presence_stanza_handler("unavailable")    
    def handle_presence_unavailable(self, stanza):
        Resource.offline(stanza)
        return True
        
    def delayed_update_presence(self):    
        Resource.update_presences(self._presences)
        del self._presences[:]
        self.update_presence_flag = False
        signals.user_roster_status_received.send(sender=self)
        return True
    
    @presence_stanza_handler("subscribe")
    def handle_presence_subscribe(self, stanza):
        logger.info("-- {0!r} requested presence subscription".format(stanza.from_jid))
        if settings.Roster.auto_accept:
            presence = self.request_add_friend(stanza.from_jid, send=False)
            return [stanza.make_accept_response(), presence]
        else:
            FriendNotice.record_from_stanza(stanza)
        return True    
            
    def request_add_friend(self, jid, send=True):        
        presence = self.generate_presence(jid, stanza_type="subscribe")
        if send:
            return self.send(presence)
        return presence
    
    def remove_friend(self, jid, send=True):
        presence = self.generate_presence(jid, stanza_type="unsubscribe")
        if send:
            return self.send(presence)
        return presence
        
    def generate_presence(self, jid, stanza_type):    
        if not isinstance(jid, JID):
            jid = JID(jid)
        return Presence(to_jid=jid.bare(), stanza_type=stanza_type)        
    
    def accept_friend_request(self, jid):
        if not isinstance(jid, JID):
            jid = JID(jid)
        stanza = Presence(stanza_type=ACCEPT_RESPONSES["subscribe"], to_jid=jid.bare())
        self.send(stanza)
        self.request_add_friend(jid)
        
    def deny_friend_request(self, jid):
        if not isinstance(jid, JID):
            jid = JID(jid)
        stanza = Presence(stanza_type=DENY_RESPONSES["subscribe"], to_jid=jid.bare())
        self.send(stanza)
    
    @presence_stanza_handler("unsubscribe")
    def handle_presence_unsubscribe(self, stanza):
        logging.info("{0} canceled presence subscription".format(stanza.from_jid))
        presence = self.remove_friend(stanza.from_jid, send=False)
        return [stanza.make_accept_response(), presence]
    
    @presence_stanza_handler("subscribed")
    def handle_presence_subscribed(self, stanza):
        logging.info("{0!r} accepted our subscription request".format(stanza.from_jid))
        FriendNotice.record_from_stanza(stanza)
        return True
    
    @presence_stanza_handler("unsubscribed")
    def handle_presence_unsubscribed(self, stanza):
        logging.info("{0!r} acknowledged our subscrption cancelation".format(stanza.from_jid))
        FriendNotice.record_from_stanza(stanza)
        return True
