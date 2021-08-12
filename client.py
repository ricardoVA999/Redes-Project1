import asyncio
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import time

# Ricardo Antonio Valenzuela Avila 18762
# Redes
# Clases para manejo de configuraciones generalels del usuario
# Solamente toma como parametro el jid y el password
# Usando ejemplo de xmpp obtenido de https://docplayer.net/60687805-Slixmpp-documentation.html

# Definicion de la clase para el bot de registro
class register_to_server(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('register', self.register)
        self.add_event_handler('disconnected', self.got_diss)
        self.register_plugin('xep_0030')  #Service Discovery
        self.register_plugin('xep_0004')  #Data forms
        self.register_plugin('xep_0066')  #Out-of-band Data
        self.register_plugin('xep_0077')  #In-band Registration
        self.register_plugin('xep_0045')  #Multi user chat
        self.register_plugin('xep_0199')  #XMPP Ping
        self['xep_0077'].force_registration = True
    
    def got_diss(self, event):
        print('Got disconnected')
    
    # Registro de nuevo usuario
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

#Clase principal del cliente
class my_client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.password = password

        #Manejo de eventos importantes
        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)
        self.add_event_handler('presence_subscribed', self.new_subscribed)
        self.add_event_handler('message', self.message)
        self.add_event_handler('got_offline', self.handle_offline)
        self.add_event_handler('got_online', self.handle_online)

        self.register_plugin('xep_0004') #Data Forms
        self.register_plugin('xep_0030') #Service Discovery
        self.register_plugin('xep_0045') #Multi user chat
        self.register_plugin('xep_0047') #In-band Bytestreams
        self.register_plugin('xep_0050') #Ad-Hoc Commands
        self.register_plugin('xep_0066') #Out of Band Data
        self.register_plugin('xep_0077') #In-band Registration
        self.register_plugin('xep_0085') #Chat State Notifications
        self.register_plugin('xep_0092') #Software version
        self.register_plugin('xep_0199') #Xmpp ping
        self.register_plugin('xep_0231') #Bits of Binary

        self['xep_0077'].force_registration = True

    #En caso de recibir un mensaje individual o grupal
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

    #En caso de recibir un evento de tipo error
    def handle_error(self, event):
        print('ERROR')
        self.disconnect()

    #Al detectar que un usuario se desconecto
    def handle_offline(self, presence):
        print(str(presence['from']).split('/')[0] + ' se desconecto.')

    #Al detectar que un usuario se conecto
    def handle_online(self, presence):
        print(str(presence['from']).split('/')[0] + ' se conecto.')

    #En caso de tener un error al iniciar sesion
    def failed(self, event):
        print('Fallo al comprobar sus credenciales...')
    
    #Mandar presencia y recivir roster
    def start(self):
        self.send_presence()
        self.get_roster()
    
    #En caso de desconectarse del servidor
    def got_diss(self, event):
        print('Got disconnected...')

    #En caso de recibir una nueva subscripcion
    def new_subscribed(self, presence):
        print(presence.get_from()+' se suscribio a ti!')

    #Mandar y settear un nuevo mensaje de presencia
    def set_presence(self, show, status):
        self.send_presence(show, status)
        self.get_roster()
        time.sleep(3)
    
    #Eliminar la cuenta del server
    def delete(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full
        resp['register']['remove'] = True

        try:
            print('Cuenta '+self.boundjid.bare+' eliminada con exito...')
            resp.send()
        except IqError as err:
            print('No se pudo eliminar la cuenta', self.boundjid)
            self.disconnect()
        except IqTimeout:
            print('No se recibio respuesta del servidor')
            self.disconnect()
    
    #Aniadir nuevo amigo al roster
    def add_friend(self, JID):
        self.send_presence_subscription(pto=JID, ptype='subscribe', pfrom = self.boundjid.bare)
        self.get_roster()
        time.sleep(3)