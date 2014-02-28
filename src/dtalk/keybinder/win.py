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

import pyHook


from dtalk.keybinder.base import BaseBackend
from dtalk.utils import six

ID2KEY = {
    8: 'Back',
    9: 'Tab',
    13: 'Return',
    20: 'Capital',
    27: 'Escape',
    32: 'Space',
    33: 'Prior',
    34: 'Next',
    35: 'End',
    36: 'Home',
    37: 'Left',
    38: 'Up',
    39: 'Right',
    40: 'Down',
    44: 'Snapshot',
    46: 'Delete',
    48: '0',
    49: '1',
    50: '2',
    51: '3',
    52: '4',
    53: '5',
    54: '6',
    55: '7',
    56: '8',
    57: '9',
    65: 'A',
    66: 'B',
    67: 'C',
    68: 'D',
    69: 'E',
    70: 'F',
    71: 'G',
    72: 'H',
    73: 'I',
    74: 'J',
    75: 'K',
    76: 'L',
    77: 'M',
    78: 'N',
    79: 'O',
    80: 'P',
    81: 'Q',
    82: 'R',
    83: 'S',
    84: 'T',
    85: 'U',
    86: 'V',
    87: 'W',
    88: 'X',
    89: 'Y',
    90: 'Z',
    91: 'Lwin',
    96: 'Numpad0',
    97: 'Numpad1',
    98: 'Numpad2',
    99: 'Numpad3',
    100: 'Numpad4',
    101: 'Numpad5',
    102: 'Numpad6',
    103: 'Numpad7',
    104: 'Numpad8',
    105: 'Numpad9',
    106: 'Multiply',
    107: 'Add',
    109: 'Subtract',
    110: 'Decimal',
    111: 'Divide',
    112: 'F1',
    113: 'F2',
    114: 'F3',
    115: 'F4',
    116: 'F5',
    117: 'F6',
    118: 'F7',
    119: 'F8',
    120: 'F9',
    121: 'F10',
    122: 'F11',
    123: 'F12',
    144: 'Numlock',
    160: 'Lshift',
    161: 'Rshift',
    162: 'Lcontrol',
    163: 'Rcontrol',
    164: 'Lmenu',
    165: 'Rmenu',
    186: 'Oem_1',
    187: 'Oem_Plus',
    188: 'Oem_Comma',
    189: 'Oem_Minus',
    190: 'Oem_Period',
    191: 'Oem_2',
    192: 'Oem_3',
    219: 'Oem_4',
    220: 'Oem_5',
    221: 'Oem_6',
    222: 'Oem_7',
    1001: 'mouse left', #mouse hotkeys
    1002: 'mouse right',
    1003: 'mouse middle',
    1000: 'mouse move', #single event hotkeys
    1004: 'mouse wheel up',
    1005: 'mouse wheel down',
    1010: 'Ctrl', #merged hotkeys
    1011: 'Alt',
    1012: 'Shift'
}

KEY2ID = dict((v, k) for k,v in six.iteritems(ID2KEY))

"""
Merge two keys into one

KeyID   MEID    MergeHumanHotkey
162     1010     Ctrl  (Lcontrol)
163     1010     Ctrl  (Rcontrol
164     1011     Alt   (Lmenu)
165     1011     Alt   (Rmenu)
160     1012     Shift (Lshift)
161     1012     Shift (Rshift)
"""

MEID2KEYIDS = {
    1010 : (162, 163),
    1011 : (164, 165),
    1012 : (160, 161)
}

class Win32Backend(BaseBackend):
    
    def initial(self):
        
        hm = pyHook.HookManager()
        hm.KeyUp = self._on_key_up
        hm.KeyDown = self._on_key_down
        hm.MouseMove = self._on_mouse_move
        
        self._keymap = {}
        self._key_downs = []
        self._key_ups = []
        self._identifier = None
        
        # set the hook
        hm.HookKeyboard()
        hm.HookMouse()
    
    def _on_key_down(self, event):
        if event.KeyID not in self._key_downs:
            self._key_downs.append(event.KeyID)        
            
        self._check_hotkey()    
        
        return True
            
    def _on_key_up(self, event):    
        
        if self._identifier is not None:
            self.emitKeyRelease(self._identifier)
            self._identifier = None
            
        try:
            self._key_downs.remove(event.KeyID)
        except: pass    
        
        return True
        
    def _on_mouse_move(self, event):
        p = event.Position
        if len(p) >= 2:
            self.emitMouseMoved(int(p[0]), int(p[1]))
            
        return True    
    
    def _check_hotkey(self):
        removed_keys = []
        for k, v in six.iteritems(self._keymap):
            if len(v) != len(self._key_downs):
                continue
            
            if self._check_key_downs(v):
                if self.check_key_event(k):
                    self._identifier = k
                else: 
                    removed_keys.append(k)
                    
        for key in removed_keys:            
            del self._keymap[key]
                    
    def _check_key_downs(self, hotkeys):
        for each_key in hotkeys:
            if isinstance(each_key, (tuple, list)):
                flag = bool(set(each_key) & set(self._key_downs))
                if not flag:
                    return False
            else:        
                if each_key not in self._key_downs:
                    return False
        return True        
                    
    def response(self):
        # pythoncom.PumpMessages()
        pass
    
    def parse_key(self, key):
        keys = key.split("+")
        
        # parse human keys to ids
        key_ids = filter(bool, [ KEY2ID.get(k, None) for k in keys ])
        
        # parse human keys from ids
        if len(keys) != len(key_ids):
            return None
        
        for index, k in enumerate(key_ids):
            if k in MEID2KEYIDS:
                key_ids[index] = MEID2KEYIDS[k]
                
        self._keymap[key] = key_ids
        return key
    
    def stop(self):
        # ctypes.windll.user32.PostQuitMessage(0)
        pass
