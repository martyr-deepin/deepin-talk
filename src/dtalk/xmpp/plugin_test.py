#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import sleekxmpp
import brotherhood

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

class EchoBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("get_hosts", self.get_hosts)
        self.add_event_handler("get_all_users", self.get_all_users)
        self.add_event_handler("get_all_online_users", self.get_all_online_users)
        self.add_event_handler("get_vhost_users", self.get_vhost_users)
        self.add_event_handler("get_vhost_online_users", self.get_vhost_online_users)

    def get_hosts(self, hosts):
        print "result of get hosts"
        print hosts

    def get_all_users(self, users):
        print "result of get all users"
        print users

    def get_all_online_users(self, users):
        print "result of get all online users"
        print users

    def get_vhost_users(self, users):
        print "result of vhost users"
        print users

    def get_vhost_online_users(self, users):
        print "result of vhost online users"
        print users

    def start(self, event):
        #self.send_presence()
        #self.get_roster()
        #self.plugin["Brotherhood"].hello()
        #self.plugin["Brotherhood"].get_hosts()
        #self.plugin["Brotherhood"].get_all_users()
        #self.plugin["Brotherhood"].get_all_online_users()
        #self.plugin["Brotherhood"].get_vhost_users("talk.linuxdeepin.com")
        self.plugin["Brotherhood"].get_vhost_online_users("talk.linuxdeepin.com")

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()


if __name__ == '__main__':
    xmpp = EchoBot("test@im.linuxdeepin.com", "sinfei")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin("Brotherhood", module = "brotherhood")

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
