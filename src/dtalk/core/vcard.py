from pyxmpp2.etree import ElementTree
from pyxmpp2.interfaces import StanzaPayload, payload_element_name


'''
    
    def get_vcard(self, jid, callback=None):
        if not callback:
            callback = self.vcard_callback
        q = Iq(
            to_jid = jid.bare(),
            stanza_type = 'get'
            )
        # vc = ET.Element("{vcard-temp}vCard")
        q.add_payload(VCardPayload())
        self.stanza_processor.set_response_handlers(q, callback, callback)
        self.send(q)        
        
    def vcard_callback(self, stanza):    
        vcard =  stanza.get_payload(VCardPayload)
        if vcard:
            print vcard.get("name")
    
'''

VCARD_TAG = u'{vcard-temp}vCard'

@payload_element_name(VCARD_TAG)
class VCardPayload(StanzaPayload):
    
    def __init__(self, attrs=None):
        if attrs is not None:
            self._dict = dict(attrs)
        else:    
            self._dict = dict()
            
    @classmethod
    def from_xml(cls, element):
        attrs = dict()
        if element.tag !=VCARD_TAG:
            raise ValueError("{0!r} is not a vcard item".format(element))
        try:
            photo = element.find(".//{vcard-temp}BINVAL").text
        except:    
            photo = ""
            
        try:
            name = element.find(".//{vcard-temp}FN").text
        except: name = ""    
        attrs["photo"] = photo
        attrs["name"] = name
        return cls(attrs)

    
    def as_xml(self):
        element = ElementTree.Element(VCARD_TAG)
        return element
    
    def get(self, key, default=""):
        return self._dict.get(key, default)
    
