#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Deepin, Inc.
#               2014 Long Wei
# 
# Author:     Long Wei <yilang2007lw@gmail.com>
# Maintainer: Long Wei <yilang2007lw@gmail.com>

from sleekxmpp import Iq
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin
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
                Callback("Deepin Qun",
                         StanzaPath("iq/qun_query"),
                         self.handle_qun))
        register_stanza_plugin(Iq, QueryElement)
        
    def plugin_end(self):
        self.xmpp.remove_handler("Deepin Qun")

    def handle_qun(self, iq):
        print "handle qun"
        if iq["type"] == "result":
            method = iq["qun_query"]["method"]
            if method == "get_qun_list":
                quns = iq["qun_query"]["quns"]
                self.xmpp.event("get_qun_list",quns)
            elif method == "get_qun_users":
                users = iq["qun_query"]["qun_qun"]["users"]
                self.xmpp.event("get_qun_users", users)
            elif method == "join_qun":
                print iq["qun_query"]["qun_qun"]
                self.xmpp.event("join_qun", true)
            elif method == "levae_qun":
                print iq["qun_query"]["qun_qun"]
                self.xmpp.event("leave_qun", true)
        else:
            pass

    def get_qun_list(self, block=False, timeout=None, callback=None, **kwargs):
        iq =  self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["qun_query"]
        query["method"] = "get_qun_list"
        return iq.send(block=block, timeout=timeout, callback=callback)

    def search_qun(self, key):
        pass

    def get_qun_info(self, qid):
        pass

    def get_qun_users(self, qid, block=False, timeout=None, callback=None, **kwargs):
        iq =  self.xmpp.Iq()
        iq["type"] = "get"
        query = iq["qun_query"]
        query["method"] = "get_qun_users"
        query["qun_qun"]["qid"] = str(qid)
        return iq.send(block=block, timeout=timeout, callback=callback)

    def join_qun(self, qid, block=False, timeout=None, callback=None, **kwargs):
        iq =  self.xmpp.Iq()
        iq["type"] = "set"
        query = iq["qun_query"]
        query["method"] = "join_qun"
        query["qun_qun"]["qid"] = str(qid)
        return iq.send(block=block, timeout=timeout, callback=callback)

    def leave_qun(self, qid, block=False, timeout=None, callback=None, **kwargs):
        iq =  self.xmpp.Iq()
        iq["type"] = "set"
        query = iq["qun_query"]
        query["method"] = "leave_qun"
        query["qun_qun"]["qid"] = str(qid)
        return iq.send(block=block, timeout=timeout, callback=callback)

    def delete_qun_user(self, qid, user, block=False, timeout=None, callback=None, **kwargs):
        iq =  self.xmpp.Iq()
        iq["type"] = "set"
        query = iq["qun_query"]
        query["method"] = "delete_qun_user"
        query["qun_qun"]["qid"] = str(qid)
        query["qun_qun"]["qun_user"] = str(user)
        return iq.send(block=block, timeout=timeout, callback=callback)

    def update_qun_info(self, qid, info):
        pass

    def create_qun(self, qname):
        pass

    def destroy_qun(self, qid):
        pass

    def transfer_qun(self, qid, jid):
        pass

    def set_qun_admin(self, qid, jid):
        pass

    def unset_qun_admin(self, qid, jid):
        pass

class QueryElement(ElementBase):
    name = "query"
    namespace = "deepin:iq:qun"
    plugin_attrib = "qun_query"
    interfaces = set(("method", "quns"))
    sub_interfaces = set(("qun",))

    def setup(self, xml = None):
        ElementBase.setup(self, xml)

    def get_quns(self):
        quns = set()
        for item in self["substanzas"]:
            if isinstance(item, QunElement):
                quns.add(item.xml.attrib["qid"])
        return quns

class QunElement(ElementBase):
    name = "qun"
    namespace = "deepin:iq:qun"
    plugin_attrib = "qun_qun"
    interfaces = set(("users", "qid"))
    sub_interfaces = set(("user",))
    
    def get_users(self):
        users = set()
        for item in self["substanzas"]:
            if isinstance(item, UserElement):
                role = item.xml.attrib["role"]
                jid = item.xml.text
                users.add((jid, role))
        return users

class SuccessElement(ElementBase):
    name = "succeed"
    namespace = "deepin:iq:qun"
    plugin_attrib = "qun_succeed"
    interfaces = set()
    sub_interfaces = set(("detail",))

class FailureElement(ElementBase):
    name = "failed"
    namespace = "deepin:iq:qun"
    plugin_attrib = "qun_failed"
    interfaces = set()
    sub_interfaces = set(("detail",))

class DetailElement(Element):
    name = "failed"
    namespace = "deepin:iq:qun"
    plugin_attrib = "qun_detail"
    interfaces = set()
    sub_interfaces = set()

class UserElement(ElementBase):
    name = "user"
    namespace = "deepin:iq:qun"
    plugin_attrib = "qun_user"
    interfaces = set(("role",))

register_stanza_plugin(QueryElement, QunElement, iterable = True)
register_stanza_plugin(QunElement, UserElement, iterable = True)
