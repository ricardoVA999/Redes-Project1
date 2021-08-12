# Ricardo Antonio Valenzuela Avila 18762
# Redes
# Clase para la obtencion del roster del usuario conectado, tambien sirve para obtener la informacion de un amigo en especifico.
# Toma como parametro el Jid de la fuente, su contrsania y en caso de ser usado el Jid del amigo a consultar
# Tomando como referencia un ejemplo extraido de https://github.com/poezio/slixmpp/blob/master/examples/roster_browser.py

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.asyncio import asyncio

#Definicion de la clase
class GetRoster(slixmpp.ClientXMPP):

    #Parametros de entrada e inicializacion de la clase
    def __init__(self, jid, password, u_search = None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.roster = {}
        self.u_search = u_search

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('changed_status', self.wait_for_presences)
        self.add_event_handler('disconnected', self.got_diss)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

        self.received = set()
        self.presences_received = asyncio.Event()

    #Control en caso de desconectarse
    def got_diss(self, event):
        print('Got disconnected')
        quit()
        
    #Manejo de roster y busqueda individual
    async def start(self, event):
        try:
            await self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        self.send_presence()

        print('Waiting for presence updates...')
        await asyncio.sleep(5)

        print('El roster de %s es:' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                status = ''
                show = ''
                sub = ''
                name = ''
                sub = self.client_roster[jid]['subscription']
                conexion = self.client_roster.presence(jid)
                name = self.client_roster[jid]['name']
                for answer, pres in conexion.items():
                    if pres['show']:
                        show = pres['show']
                    if pres['status']:
                        status = pres['status']
                self.roster[jid] = User(jid, show, status, sub, name)
        
        #Caso de busqueda general
        if(not self.u_search):
            if len(self.roster) == 0:
                print('No hay usuario conectados')
            else:
                for key in self.roster.keys():
                    friend = self.roster[key]
                    print('- Jid: '+friend.jid+' Username:'+friend.username+' Show:'+friend.show+' Status:'+friend.status+' Subscription:'+friend.subscription)
        #Caso de busqueda especifica
        else:
            if self.u_search in self.roster.keys():
                user = self.roster[self.u_search]
                print('- Jid: '+user.jid+' Username:'+user.username+' Show:'+user.show+' Status:'+user.status+' Subscription:'+user.subscription)
            else:
                print('Usuario no encontrado')
        
        #Por cuestiones de funcionamiento se debe desconectar y salir del programa :c
        await asyncio.sleep(5)
        self.disconnect()

    # Se lleva control de aquellos quienes han recivido mis actualizaciones de presencia
    def wait_for_presences(self, pres):
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

# Clase para facilitar el control de usuarios del roster
class User():
    def __init__(self, jid, show, status, subscription, username):
        self.jid = jid
        self.show = show
        self.status = status
        self.subscription = subscription
        self.username = username
