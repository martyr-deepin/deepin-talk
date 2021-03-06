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

'''
select id, user_id, resource, show, status, max(priority) as priority from dtalk_resource where show is null or show != 'offline' group by user_id;

Resource.select(Resource, pw.fn.Max(Resource.priority).alias('priority')).group_by(Resource.friend)
'''

import os
import sys
import datetime
import logging
import peewee as pw
import traceback

from dtalk.utils.contextdecorator import contextmanager
from dtalk.utils.xdg import get_jid_db, get_config_path
from dtalk.utils.threads import threaded
from dtalk.utils import six
from dtalk.models import signals
from dtalk.models.db import Model
from sleekxmpp.jid import JID
from dtalk.dispatch import receiver
import  dtalk.xmpp.signals as xmpp_signals

USER_DB_VERSION = "0.1"
COMMON_DB_VERSION = "0.1"

logger = logging.getLogger('models.Model')

DEFAULT_GROUP = '我的好友'

user_db = pw.SqliteDatabase(None, check_same_thread=False, threadlocals=True)
common_db = pw.SqliteDatabase(None, check_same_thread=False, threadlocals=True)

user_db_init_finished = False
common_db_init_finished = False

def check_user_db_inited():
    return user_db_init_finished

def check_common_db_inited():
    return common_db_init_finished

@contextmanager
def disable_auto_commit(database=user_db):
    database.set_autocommit(False)
    try:
        yield
    except:
        traceback.print_exc(file=sys.stdout)
    else:
        database.commit()
    finally:
        database.set_autocommit(True)

@threaded        
def init_user_db(jid):        
    global user_db_init_finished
    f = get_jid_db(jid, name="data_{0}.db".format(USER_DB_VERSION))
    user_db.init(f)
    created = False
    if not os.path.exists(f):
        logger.info("-- initial {0!r} database".format(jid))
        user_db.connect()
        create_user_tables()
        Friend.create_self(jid)
        created = True
        
    user_db_init_finished = True    
    signals.db_init_finished.send(sender=user_db, created=created)    
    
@threaded    
def init_common_db():
    global common_db_init_finished
    f = get_config_path("common_{0}.db".format(COMMON_DB_VERSION))    
    common_db.init(f)
    created = False
    if not os.path.exists(f):
        created = True
        common_db.connect()
        create_common_tables()
        
    common_db_init_finished = True    
    signals.db_init_finished.send(sender=common_db, created=created)    
        
def check_update_data(obj, data):
    change = False
    change_fields = []
    for (key, new_value,) in six.iteritems(data):
        old_val = getattr(obj, key, None)
        if old_val != new_value:
            change = True
            change_fields.append(key)
            setattr(obj, key, new_value)

    if change:
        obj.save(update_fields=change_fields)
        
class BaseCommonModel(Model):        
    
    class Meta:
        database = common_db
        
class UserHistory(BaseCommonModel):        
    jid = pw.CharField(unique=True, index=True)
    password = pw.CharField()
    nickname = pw.CharField(null=True)
    status = pw.CharField(null=True)
    remember = pw.BooleanField(default=True)
    auto_login = pw.BooleanField(default=True)
    last_logined = pw.DateTimeField(default=datetime.datetime.now)

class BaseUserModel(Model):

    class Meta:
        database = user_db

class Group(BaseUserModel):
    name = pw.CharField()

    class Meta:
        db_table = 'dtalk_group'


class Friend(BaseUserModel):
    jid = pw.CharField(unique=True, index=True)
    nickname = pw.CharField(null=True)
    remark = pw.CharField(null=True)
    subscription = pw.CharField(null=True)
    group = pw.ForeignKeyField(Group, related_name='friends', null=True)
    approved = pw.BooleanField(default=False)
    isSelf = pw.BooleanField(default=False)

    class Meta:
        db_table = 'dtalk_friend'

        
    @classmethod     
    def create_self(cls, jid):
        try:
            cls.get(jid=jid, isSelf=True)
        except cls.DoesNotExist:    
            cls.create(jid=jid, isSelf=True)

    @classmethod    
    def get_self(cls):
        try:        
            obj = cls.get(isSelf=True)
        except cls.DoesNotExist:    
            obj = None
        return obj    
    
    @classmethod                
    def create_or_update_roster_sleek(cls, client_roster):
        with disable_auto_commit():
            for jid in client_roster.keys():
                item = client_roster[jid]
                data = dict()
                data['jid'] = item.jid
                data['remark'] = item['name']
                data['subscription'] = item['subscription']
                groups = item['groups']
                if len(groups) >= 1:
                    group_name = groups[0]
                else:   
                    group_name = DEFAULT_GROUP
                    
                data['group'] = Group.get_or_create(name=group_name)
                try:
                    obj = cls.get(jid=data['jid'])
                except cls.DoesNotExist:   
                    cls.create(**data)
                else:    
                    check_update_data(obj, data)
                    
    @classmethod                
    def update_nickname(cls, jid, nickname):
        try:
            obj = cls.get(jid=jid)
        except cls.DoesNotExist:    
            pass
        else:
            if obj.nickname != nickname:
                obj.nickname = nickname
                obj.save(update_fields=["nickname"])

class ReceivedMessage(BaseUserModel):        
    TYPE = "received"
    friend = pw.ForeignKeyField(Friend, related_name="sends")
    body = pw.TextField()
    readed = pw.BooleanField(default=False)
    created = pw.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        db_table = "dtalk_received_message"
        
            
    @classmethod        
    def received_message_from_sleek(cls, msg):
        jid = JID(msg['from']).bare

        try:
            obj = Friend.get(jid=jid)
        except Friend.DoesNotExist:    
            logger.warning("-- have a message received but [{0}] not in your roster".format(jid))
        else:    
            cls.create(friend=obj, body=msg['body'])
    
class SendedMessage(BaseUserModel):
    TYPE = "sended"
    friend = pw.ForeignKeyField(Friend, related_name="receives")
    body = pw.TextField()
    successed = pw.BooleanField(default=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        db_table = "dtalk_sended_message"
    
    @classmethod    
    def send_message(cls, jid, body):    
        if not isinstance(body, six.text_type):
            body = body.decode("utf-8")
        try:
            obj = Friend.get(jid=jid)
        except Friend.DoesNotExist:    
            logger.warning("-- {0} not in SendedMessage table".format(jid))
            raise cls.DoesNotExist
        else:    
            return cls.create(friend=obj, body=body)

class FriendNotice(BaseUserModel):
    TYPE_REQUEST = 1
    TYPE_ACCEPT = 2
    TYPE_DENY = 3
    TYPE_UNKNOW = 4
    CHOICES = (
        (TYPE_REQUEST, '好友请求'), 
        (TYPE_ACCEPT, '请求被接受'), 
        (TYPE_DENY, '请求被拒绝')
        )
    ACTION_CHOICES = (
        (TYPE_ACCEPT, '接受好友请求'), 
        (TYPE_DENY, '拒绝好友请求'),
        (TYPE_UNKNOW, '未处理'),
    )
    
    type_ = pw.IntegerField(choices=CHOICES, default=TYPE_REQUEST)
    jid = pw.CharField()
    content = pw.TextField(null=True)
    readed = pw.BooleanField(default=False)
    action = pw.IntegerField(choices=ACTION_CHOICES, default=TYPE_UNKNOW)
    action_content = pw.TextField(null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'dtalk_friend_notice'
    
def create_user_tables():
    Group.create_table()
    Friend.create_table()
    ReceivedMessage.create_table()
    SendedMessage.create_table()
    FriendNotice.create_table()
    
def create_common_tables():    
    UserHistory.create_table()
    
@receiver(xmpp_signals.auth_successed)
def _add_to_user_history(sender, jid, password, remember, auto_login, status, *args, **kwargs):
    data = dict(jid=jid, password=password, remember=remember, auto_login=auto_login, status=status)
    try:
        obj = UserHistory.get(jid=jid)
    except UserHistory.DoesNotExist:    
        UserHistory.create(**data)
    else:    
        data['last_logined'] = datetime.datetime.now()
        check_update_data(obj, data)

        
@receiver(xmpp_signals.roster_subscription_request)        
def _add_to_roster_notice(presence, *args, **kwargs):
    params = dict(
        type_ = FriendNotice.TYPE_REQUEST,
        jid = presence['from'].bare,
        content = presence['status']
    )
    FriendNotice.create(**params)
    
