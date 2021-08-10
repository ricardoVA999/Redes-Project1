import asyncio
from logging import error, fatal
from re import X, search
import re
import threading
from xml.etree.ElementTree import fromstring
import slixmpp
from slixmpp import jid
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.plugins.xep_0004.stanza import field
from slixmpp.plugins.xep_0004.stanza.form import Form
from xml.etree import cElementTree as ET
import time


#Usando ejemplo de xmpp obtenido de https://docplayer.net/60687805-Slixmpp-documentation.html

class register_to_server(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('register', self.register)
        self.add_event_handler('disconnected', self.got_diss)
    
    def got_diss(self, event):
        print('Got disconnected')
    def register(self, event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
    
        try:
            resp.send()
            print('\nCuenta creada con exito')
        except IqError:
            print('\nNo se pudo crear la cuenta')
        except IqTimeout:
            print('\nSin respuesta del server')

        self.disconnect()

class my_client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.users = {}
        self.friends = {}

        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)
        self.add_event_handler('presence_subscribed', self.new_subscribed)
        self.add_event_handler('changed_status', self.wait_presences)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0085')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0050')
        self.register_plugin('xep_0047')
        self.register_plugin('xep_0231')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0092')
        self.register_plugin('xep_0095')
        self.register_plugin('xep_0096')
        self.register_plugin('xep_0047')

        self['xep_0077'].force_registration = True

        self.received = set()
        self.presences_received = threading.Event()

    def handle_error(self):
        print("ERROR")
        self.disconnect()

    def failed(self):
        print("Fallo al comprobar sus credenciales...")
        self.disconnect()

    def start(self):
        self.send_presence()
        self.get_roster()

    def got_diss(self, event):
        print('Got disconnected...')

    def wait_presences(self, presence):
        self.received.add(presence['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
            self.presences_received.clear()

        self.create_friends_dict()

    def new_subscribed(self, presence):
        print(presence.get_from()+' se suscribio a ti!')
    
    def delete(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full
        resp['register']['remove'] = True

        try:
            resp.send()
            print("Cuenta "+self.boundjid+" eliminada con exito...")
        except IqError as err:
            print("No se pudo eliminar la cuenta", self.boundjid)
            self.disconnect()
        except IqTimeout:
            print("No se recibio respuesta del servidor")
            self.disconnect()
    
    def get_all_users(self):

        iq = self.Iq()
        iq.set_from(self.boundjid.full)
        iq.set_to('search.'+self.boundjid.domain)
        iq.set_type('get')
        iq.set_query('jabber:iq:search')

        iq.send()

        form = Form()
        form.set_type('sumbit')

        form.add_field(var='FORM_TYPE', ftype='hidden', type='hidden', value='jabber:iq:search')
        form.add_field(var='search', ftype='text-single', type='text-single', label='Search', required=True, value='*')
        form.add_field(var='Username', ftype='boolean', type='boolean', label='Username', value=1)
        form.add_field(var='Name', ftype='boolean', type='boolean', label='Name', value=1)
        form.add_field(var='Email', ftype='boolean', type='boolean', label='Email', value=1)

        search = self.Iq()
        search.set_type('set')
        search.set_to('search.'+self.boundjid.domain)
        search.set_from(self.boundjid.full)

        my_query = ET.Element('{jabber:iq:search}query')
        my_query.append(form.xml)

        search.append(my_query)
        
        resp = yield from search.send()

        print(resp)

        tree = ET.fromstring(str(resp))

        data = []

        for i in tree:
            for j in i:
                for k in j:
                    data.append[k]


        for item in data:
            children = item.getchildren()

            if len(children) > 0:
                for i in children:
                    try:
                        child = i.getchildren()[0]
                    except:
                        continue

                    if i.attribp['var'] == 'Email':
                        email = child.text
                    elif i.attribp['var'] == 'jid':
                        jid = child.text
                    elif i.attribp['var'] == 'Name':
                        name = child.text
                    elif i.attribp['var'] == 'Username':
                        user_na = child.text
                if jid:
                    self.users[jid] = [user_na, name, email]

        return self.users
    
    def add_friend(self, JID):
        self.send_presence_subscription(pto=JID, ptype='subscribe', pfrom = self.boundjid.bare)
        if not JID in self.friends:
            self.friends[JID] = user(JID,'','','','to',JID.split('@')[0])
        self.get_roster()
        time.sleep(1)
        self.create_friends_dict()

    def get_friends(self):
        if not self.friends():
            self.create_friends_dict()
        return self.friends()

    def create_friends_dict(self):
        self.get_roster()
        groups = self.client_roster.groups()
        if groups:
            for jid in groups['']:
                if jid == self.boundjid.bare or 'conference' in jid:
                    continue

                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                uname = str(jid.split('@')[0])
                connections = self.client_roster.presence(jid)

                if connections.items():
                    for res, pres in connections.items():
                        show = 'available'
                        status = ''
                        if pres['show']:
                            show = pres['show']
                        if pres['status']:
                            status = pres['status']

                        if not jid in self.friends:
                            self.friends[jid] = user(jid, name, show, status, sub, uname,res)
                        else:
                            self.friends[jid].update_data(status, show, res, sub)
                else:
                    self.friends[jid] = user(jid, name, 'unavailable', '', sub, uname, '')
    
class user():
    def __init__(self, jid, name, show, status, subscription, username, resource=None):
        self.jid = jid
        self.name = name
        self.show = show
        self.status = status
        self.subscription = subscription
        self.username = username
        self.resource = resource
        self.messages = []

    def update_data(self, status, show, resource=None, subscription=None):
        self.status = status
        self.show = show
        self.resource = resource
        if subscription:
            self.subscription = subscription
