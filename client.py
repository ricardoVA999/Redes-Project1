import asyncio
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
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
        self.jid = jid
        self.password = password


        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)
        self.add_event_handler('presence_subscribed', self.new_subscribed)
        self.add_event_handler('message', self.message)

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
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')

        self['xep_0077'].force_registration = True

    def message(self, msg):
        sender = str(msg['from'])
        jid = sender.split('/')[0]
        username = jid.split('@')[0]
        if msg['type'] in ('chat', 'normal'):
            print('Nuevo mensaje de: '+username+' dice: '+msg['body'])
        elif msg['type'] in ('groupchat', 'normal'):
            nick  = sender.split('/')[1]
            if jid != self.jid:
                print('Nuevo mensaje del grupo: '+nick+' de: '+jid+' dice: '+msg['body'])

    def handle_error(self, event):
        print("ERROR")
        self.disconnect()

    def failed(self, event):
        print("Fallo al comprobar sus credenciales...")

    def start(self):
        self.send_presence()
        self.get_roster()

    def got_diss(self, event):
        print('Got disconnected...')

    def new_subscribed(self, presence):
        print(presence.get_from()+' se suscribio a ti!')

    def set_presence(self, show, status):
        self.send_presence(pshow=show, pstatus=status)
    
    def delete(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full
        resp['register']['remove'] = True

        try:
            print("Cuenta "+self.boundjid.bare+" eliminada con exito...")
            resp.send()
        except IqError as err:
            print("No se pudo eliminar la cuenta", self.boundjid)
            self.disconnect()
        except IqTimeout:
            print("No se recibio respuesta del servidor")
            self.disconnect()
    
    """def create_room(self, room, nick):
        status = 'NEW'

        self.plugin['xep_0045'].joinMUC(room,nick,pstatus=status,pfrom=self.boundjid.full)

        self.plugin['xep_0045'].setAffiliation(room, self.boundjid.full, affiliation='owner')
        self.plugin['xep_0045'].configureRoom(room, ifrom=self.boundjid.full)

        self.rooms[room] = group(room, nick, status)"""
    
    def add_friend(self, JID):
        self.send_presence_subscription(pto=JID, ptype='subscribe', pfrom = self.boundjid.bare)
        self.get_roster()
        time.sleep(3)