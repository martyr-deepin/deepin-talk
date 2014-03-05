#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Deepin, Inc.
#               2014 Long Wei
# 
# Author:     Long Wei <yilang2007lw@gmail.com>
# Maintainer: Long Wei <yilang2007lw@gmail.com>

import sys
import logging
import sleekxmpp
import qun

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

        self.add_event_handler("get_qun_list", self.handle_get_qun_list)
        self.add_event_handler("get_qun_users", self.handle_get_qun_users)
        self.add_event_handler("join_qun", self.handle_join_qun)
        self.add_event_handler("leave_qun", self.handle_leave_qun)


    def start(self, event):
        #self.plugin["QunPlugin"].get_qun_list()
        #self.plugin["QunPlugin"].get_qun_users(2)
        #self.plugin["QunPlugin"].join_qun(4)
        self.plugin["QunPlugin"].leave_qun(4)

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

    def handle_get_qun_list(self, quns):
        print "result of get qun list"
        print quns

    def handle_get_qun_users(self, users):
        print "result of get qun users"
        print users

    def handle_join_qun(self, result):
        print "result of join qun"
        print result

    def handle_leave_qun(self, result):
        print "result of leave qun"
        print result

if __name__ == '__main__':
    xmpp = EchoBot("yks@talk.linuxdeepin.com", "yks")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin("QunPlugin", module = "qun")

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
