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
                Callback("Disco Brother",
                         StanzaPath("iq/disco_brother"),
                         self.handle_disco_brother))
        register_stanza_plugin(Iq, DiscoBrother)
        
    def plugin_end(self):
        self.xmpp.remove_handler("Disco Brother")

    #def post_init(self):
    #    BasePlugin.post_init(self)
    #    self.xmpp['xep_0030'].add_feature("deepin:iq:brotherhood")

    def handle_disco_brother(self, iq):
        if iq["type"] == "get":
            print "handle disco brother get"

        elif iq["type"] == "result":
            method = iq["disco_brother"]["method"]
            if method == "get_all_users":
                users = iq["disco_brother"]["users"]
                self.xmpp.event("get_all_users", users)
            elif method == "get_all_online_users":
                users = iq["disco_brother"]["users"]
                self.xmpp.event("get_all_online_users", users)
            elif method == "get_vhost_users":
                users = iq["disco_brother"]["users"]
                self.xmpp.event("get_vhost_users", users)
            elif method == "get_vhost_online_users":
                users = iq["disco_brother"]["users"]
                self.xmpp.event("get_vhost_online_users", users)
            elif method == "get_hosts":
                hosts = iq["disco_brother"]["hosts"]
                self.xmpp.event("get_hosts", hosts)
            else:
                print "unknown method %s" % method
        else:
            print "invalid iq type:%s" % iq

    def hello(self):
        print "Hello, World!"

    def get_hosts(self, block=False, timeout=None, callback=None, **kwargs):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_hosts"
        return iq.send(block=block, timeout=timeout, callback=callback)

    def get_all_users(self, block=False, timeout=None, callback=None, **kwargs):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_all_users"
        return iq.send(block=block, timeout=timeout, callback=callback)

    def get_vhost_users(self, host, block=False, timeout=None, callback=None, **kwargs):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_vhost_users"
        query["host"] = host
        return iq.send(block=block, timeout=timeout, callback=callback)

    def get_all_online_users(self, block=False, timeout=None, callback=None, **kwargs):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_all_online_users"
        return iq.send(block=block, timeout=timeout, callback=callback)

    def get_vhost_online_users(self, host, block=False, timeout=None, callback=None, **kwargs):
        iq = self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["disco_brother"]
        query["method"] = "get_vhost_online_users"
        query["host"] = host
        return iq.send(block=block, timeout=timeout, callback=callback)

class DiscoBrother(ElementBase):
    name = "query"
    namespace = "deepin:iq:brotherhood"
    plugin_attrib = "disco_brother"
    interfaces = set(("method", "hosts", "users"))
    sub_interfaces = set(("host", "user"))

    def setup(self, xml = None):
        ElementBase.setup(self, xml)

    def get_users(self):
        users = set()
        for item in self["substanzas"]:
            if isinstance(item, DiscoUser):
                users.add(item.xml.attrib["jid"])
        return users

    def get_hosts(self):
        hosts = set()
        for item in self["substanzas"]:
            if isinstance(item, DiscoHost):
                hosts.add(item.xml.attrib["server"])
        return hosts

class DiscoHost(ElementBase):
    name = "host"
    namespace = "deepin:iq:brotherhood"
    plugin_attrib = "disco_host"
    interfaces = set("server")

class DiscoUser(ElementBase):
    name = "user"
    namespace = "deepin:iq:brotherhood"
    plugin_attrib = "disco_user"
    interfaces = set("jid")

register_stanza_plugin(DiscoBrother, DiscoHost, iterable = True)
register_stanza_plugin(DiscoBrother, DiscoUser, iterable = True)
