#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Deepin, Inc.
#               2014 Long Wei
# 
# Author:     Long Wei <yilang2007lw@gmail.com>
# Maintainer: Long Wei <yilang2007lw@gmail.com>

from sleekxmpp import Iq
from sleekxmpp.xmlstream import ElementBase, ET, register_stanza_plugin
from sleekxmpp.plugins import BasePlugin
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher import StanzaPath

class QunPlugin(BasePlugin):
    name = "qun"
    description = "xmpp extension:qun"
    dependencies = set()
    default_config = {}

    def plugin_init(self):
        self.xmpp.register_handler(
                Callback("Qun",
                         StanzaPath("iq/qun"),
                         self.handle_qun))
        register_stanza_plugin(Iq, DiscoBrother)
        
    def plugin_end(self):
        self.xmpp.remove_handler("Disco Brother")

    def handle_qun(self, iq):
        print "handle qun"

    def get_qun_list(self):
        pass

    def search_qun(self, key):
        pass

    def get_qun_info(self, qid):
        pass

    def get_qun_users(self, qid):
        pass

    def get_qun_user_info(self, qid, jid):
        pass

    def join_qun(self, qid):
        pass

    def leave_qun(self, qid):
        pass

    def delete_qun_user(self, qid, user):
        pass

    def update_qun_info(self, qid, info):
        pass

    def create_qun(self, qname):
        pass

    def destroy_qun(self, qid):
        pass

    def transfer_qun(self, qid, jid):
        pass

    def update_user_rold(self, qid, jid):
        pass
