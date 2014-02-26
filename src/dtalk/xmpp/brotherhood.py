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

class Brotherhood(BasePlugin):
    name = "brotherhood"
    description = "xmpp extension:brotherhood"
    dependencies = set()
    default_config = {}

    def plugin_init(self):
        self.xmpp.register_handler(
                Callback("Disco Users",
                         StanzaPath("iq/disco_brother"),
                         self.handle_disco_users))

        register_stanza_plugin(Iq, DiscoUsers)
        
    def plugin_end(self):
        self.xmpp.remove_handler("Disco Users")

    def post_init(self):
        BasePlugin.post_init(self)
        self.xmpp['xep_0030'].add_feature("deepin:iq:brotherhood")

    def handle_disco_users(self, iq):
        if iq["type"] == "get":
            print "handle disco users get"
        elif iq["type"] == "result":
            print "handle disco users result"

    def hello(self):
        print "Hello, World!"

    def get_all_users(self, **kwargs):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_all_users"
        return iq.send()

    def get_vhost_users(self, host, **kwargs):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_vhost_users"
        query["host"] = host
        return iq.send()

    def get_all_online_users(self):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_all_online_users"
        return iq.send()

    def get_vhost_online_users(self, host):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_vhost_online_users"
        query["host"] = host
        return iq.send()

class DiscoUsers(ElementBase):
    name = "query"
    namespace = "deepin:iq:brotherhood"
    plugin_attrib = "disco_brother"
    interfaces = set(("method", "host", "server", "users"))

    _users = set()

    def setup(self, xml = None):
        ElementBase.setup(self, xml)
        self._users = set([user[0:2] for user in self["users"]])

    def add_user(self, jid, server = None, nickname = None):
        if (jid, server) not in self._users:
            self._users.add((jid, server))
            user = DiscoUser(parent = self)
            user["jid"] = jid
            user["server"] = server
            user["nickname"] = nickname
            self.iterables.append(user)
            return True
        return False

    def del_user(self, jid, server = None):
        if (jid, server) in self._users:
            for user_xml in self.findall('{%s}user' % self.namespace):
                user = (user_xml.attrib["jid"],
                        user_xml.attrib.get("server", None)) 
                if user == (jid, server):
                    self.xml.remove(user_xml)
                    return True
        return False

    def get_users(self):
        users = set()
        for user in self["substanzas"]:
            if isinstance(user, DiscoUser):
                users.add(user["jid"], user["server"], user["nickname"])
        return users

    def set_users(self, users):
        self.del_users()
        for user in users:
            jid, server, nickname = user
            self.add_user(jid, server, nickname)

    def del_users(self):
        self._users = set()
        users = [i for i in self.iterables if isinstance(i, DiscoUser)]
        for user in users:
            self.xml.remove(user.xml)
            self.iterables.remove(user)

class DiscoUser(ElementBase):
    name = "user"
    namespace = "deepin:iq:brotherhood"
    plugin_attrib = name
    interfaces = set(("jid", "server", "nickname"))

    def get_server(self):
        return self._get_attr("server", None)

    def get_nickname(self):
        return self.__get_attr("nickname", None)

register_stanza_plugin(DiscoUsers, DiscoUser, iterable = True)
