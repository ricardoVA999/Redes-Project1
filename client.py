from re import X
import threading
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout


#Usando ejemplo de xmpp obtenido de https://docplayer.net/60687805-Slixmpp-documentation.html

import slixmpp

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
        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0050')
        self.register_plugin('xep_0047')
        self.register_plugin('xep_0231')
        self.register_plugin('xep_0045')
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
        try:
            self.get_roster(block=True)
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        
        self.send_presence()
        print("Si se conecto")

    def got_diss(self, event):
        print('Got disconnected...')