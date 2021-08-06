from re import X
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

import logging
from getpass import getpass
from argparse import ArgumentParser


#Usando ejemplo de xmpp obtenido de https://docplayer.net/60687805-Slixmpp-documentation.html

def logginMenu():
    print("""
    1. Iniciar Sesion
    2. Registrar nueva cuenta
    3. Salir
    """)

def mainMenu():
    print("""
    1. Ver conectados
    2. Mandar mensaje privado
    3. Madar mensaje general
    """)

import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp

class register_to_server(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("register", self.register)

    def register(self, event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
    
        try:
            resp.send()
            print("Cuenta creada con exito")
        except IqError:
            print("No se pudo crear la cuenta")
        except IqTimeout:
            print("Sin respuesta del server")

        self.disconnect()

class Client(slixmpp.ClientXMPP):

    """
    A simple Slixmpp bot that will echo messages it
    receives, along with a short thank you message.
    """
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

        self.add_event_handler("disconnected", self._handle_disconnected)
        self.add_event_handler('failed_auth', self.failed_auth)

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
        self.send_presence()
        await self.get_roster()

    def _handle_disconnected(self, event):
        print("You got disconnected")
        return super()._handle_disconnected(event)
    
    def failed_auth(self, event):
        print("Incorrect Credentials")
        self.disconnect()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=Client.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")
    
    xmpp = register_to_server(jid=args.jid, password=args.password)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0004')  # Data forms
    xmpp.register_plugin('xep_0066')  # Out-of-band Data
    xmpp.register_plugin('xep_0077')  # In-band Registration
    xmpp.register_plugin('xep_0045')  # Groupchat
    xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp['xep_0077'].force_registration = True

    xmpp.connect()
    xmpp.process(forever=False)

