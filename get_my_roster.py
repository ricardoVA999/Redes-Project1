#Usando como referencia el codigo ejemplo de https://github.com/poezio/slixmpp/blob/master/examples/roster_browser.py
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.asyncio import asyncio


class GetRoster(slixmpp.ClientXMPP):

    """
    A basic script for dumping a client's roster to
    the command line.
    """

    def __init__(self, jid, password, u_search = None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.roster = {}
        self.u_search = u_search

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status", self.wait_for_presences)
        self.add_event_handler('disconnected', self.got_diss)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

        self.received = set()
        self.presences_received = asyncio.Event()

    def got_diss(self, event):
        print('Got disconnected')
        quit()
        

    async def start(self, event):
        """
        Process the session_start event.
        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.
        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
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

        if(not self.u_search):
            if len(self.roster) == 0:
                print("No hay usuario conectados")
            else:
                for key in self.roster.keys():
                    friend = self.roster[key]
                    print("- Jid: "+friend.jid+" Username:"+friend.username+" Show:"+friend.show+" Status:"+friend.status+" Subscription:"+friend.subscription)
        else:
            if self.u_search in self.roster.keys():
                user = self.roster[self.u_search]
                print("- Jid: "+user.jid+" Username:"+user.username+" Show:"+user.show+" Status:"+user.status+" Subscription:"+user.subscription)
            else:
                print("Usuario no encontrado")
        await asyncio.sleep(5)
        self.disconnect()

    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()


class User():
    def __init__(self, jid, show, status, subscription, username):
        self.jid = jid
        self.show = show
        self.status = status
        self.subscription = subscription
        self.username = username
