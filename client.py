import asyncio
from asyncio.events import get_event_loop
from asyncio.tasks import wait

from xml.etree.ElementTree import fromstring
import slixmpp

from slixmpp.exceptions import IqError, IqTimeout

from slixmpp.plugins.xep_0004.stanza.form import Form
from xml.etree import cElementTree as ET
import time
from get_my_roster import GetRoster


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
        self.jid = jid
        self.password = password

        self.users = {}
        self.friends = {}
        self.rooms = {}

        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)
        self.add_event_handler('presence_subscribed', self.new_subscribed)
        self.add_event_handler('changed_status', self.wait_presences)
        self.add_event_handler('message', self.received_message)

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
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')

        self['xep_0077'].force_registration = True

        self.received = set()
        self.presences_received = asyncio.Event()

    def received_message(self, msg):
        sender = str(msg['from'])
        jid = sender.split('/')[0]
        username = jid.split('@')[0]
        if msg['type'] in ('chat', 'normal'):
            print('Nuevo mensaje de:', jid)
            
            if not jid in self.friends:
                self.friends[jid] = user(
                    jid, '', '', '', '', username)

            self.friends[jid].messages.append(msg['body'])


    def handle_error(self, event):
        print("ERROR")
        self.disconnect()

    def failed(self, event):
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
    
    def create_room(self, room, nick):
        status = 'NEW'

        self.plugin['xep_0045'].joinMUC(room,nick,pstatus=status,pfrom=self.boundjid.full)

        self.plugin['xep_0045'].setAffiliation(room, self.boundjid.full, affiliation='owner')
        self.plugin['xep_0045'].configureRoom(room, ifrom=self.boundjid.full)

        self.rooms[room] = group(room, nick, status)

    def join_room(self, room, nick):
        status = 'available'
        self.plugin['xep_0045'].joinMUC(room,nick,pstatus=status,pfrom=self.boundjid.full)
        if not room in self.room_dict:
            self.rooms[room] = group(room, nick, status)
    
    def get_my_roster(self):
        xmpp2 = GetRoster(self.jid, self.password)
        xmpp2.register_plugin('xep_0030')  # Service Discovery
        xmpp2.register_plugin('xep_0004')  # Data forms
        xmpp2.register_plugin('xep_0066')  # Out-of-band Data
        xmpp2.register_plugin('xep_0077')  # In-band Registration
        xmpp2.register_plugin('xep_0045')  # Groupchat
        xmpp2.register_plugin('xep_0199')  # XMPP Ping
        xmpp2['xep_0077'].force_registration = True
        xmpp2.connect()
        xmpp2.process(forever=False)

    def send_private_message(self, to, msg):
        jid = self.boundjid.bare
        self.send_message(mto=to, mbody=msg, mtype='chat',mfrom=self.boundjid.bare)
        if to in self.friends and msg:
            self.friends[to].messages.append(msg)
        if msg:
            print("Se mando el mensaje")
    
    def add_friend(self, JID):
        self.send_presence_subscription(pto=JID, ptype='subscribe', pfrom = self.boundjid.bare)
        if not JID in self.friends:
            self.friends[JID] = user(JID,'','','','to',JID.split('@')[0])
        self.get_roster()
        time.sleep(1)
        self.create_friends_dict()

    def get_user_info(self, jid):
        if jid in self.friends.keys():
            return "JID: " + self.friends[jid].jid + ' Subscription: ' + self.friends[jid].subscription + ' Username: ' + self.friends[jid].username
        else:
            return "Usuario no encontrado dentro de sus amigos"

    def create_friends_dict(self):
        self.get_roster()
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
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

class group():
    def __init__(self, room, nick, status=None):
        self.room = room
        self.nick = nick
        self.status = status
        self.messages = []