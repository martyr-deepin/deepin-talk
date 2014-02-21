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



from Xlib import display
from Xlib.ext import record
from Xlib import X, XK
from Xlib.protocol import rq

from dtalk.keybinder.base import BaseBackend
        
local_dpy = display.Display()
record_dpy = display.Display()

known_modifiers_mask = 0
x_modifiers = (X.ControlMask, X.ShiftMask, X.Mod1Mask, 
               X.Mod2Mask, X.Mod3Mask, X.Mod4Mask, X.Mod5Mask)
 
for mod in x_modifiers:
    known_modifiers_mask |= mod
    
ctx = None
def record_event(record_callback):
    global ctx
    ctx = record_dpy.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.MotionNotify),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
                }])
         
    record_dpy.record_enable_context(ctx, record_callback)
    record_dpy.record_free_context(ctx)
    
def stop_record():    
    record_dpy.record_disable_context(ctx)
    record_dpy.close()
    local_dpy.close()
        
def get_event_data(data):
    return rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
    
def get_keyname(event):
    keysym = local_dpy.keycode_to_keysym(event.detail, 0)
    for name in dir(XK):
        if name[:3] == "XK_" and getattr(XK, name) == keysym:
            return name[3:]
    return "[%d]" % keysym
     
def check_valid_event(reply):
    if reply.category != record.FromServer:
        return 
    if reply.client_swapped:
        return
    if not len(reply.data) or ord(reply.data[0]) < 2:
        return
    
def parse_keystring(keystring):
    keys = keystring.split("+")
    modifier_mask = 0
    
    if len(keys) == 1:
        keyval = XK.string_to_keysym(keys[0].upper())
    else:    
        keyval = XK.string_to_keysym(keys[-1].lower())
                
        if "Ctrl" in keys[0:-1]:
            modifier_mask |= X.ControlMask
        if "Alt"  in keys[0:-1]:
            modifier_mask |= X.Mod1Mask
        if "Shift" in keys[0:-1]:
            modifier_mask |= X.ShiftMask        
            
    keycode = local_dpy.keysym_to_keycode(keyval)
    return (keycode, modifier_mask)
    
class XlibBackend(BaseBackend):    
    
    def initial(self):
        self.wait_for_release = False
        self._identifier = None
        self._stop_flag = False
        
    def response(self):    
        record_event(self.record_callback)
        
    def parse_key(self, keys):    
        return parse_keystring(keys)
        
    def record_callback(self, reply):    
        check_valid_event(reply)
        data = reply.data
        
        while len(data):
            if self._stop_flag:
                break
            event, data = get_event_data(data)
            if event.type == X.KeyPress and not self.wait_for_release:
                keycode = event.detail
                modifiers = event.state & known_modifiers_mask
                identifier = (keycode, modifiers)
                if self.check_key_event(identifier):
                    self.wait_for_release = True
                    self._identifier = identifier
            elif event.type == X.KeyRelease and self.wait_for_release:    
                self.wait_for_release = False
                if self._identifier:
                    self.emitKeyRelease(self._identifier)
                    
            elif event.type == X.MotionNotify:     
                self.emitMouseMoved(int(event.root_x), int(event.root_y))
                
    def stop(self):            
        self._stop_flag = True        
        stop_record()        


