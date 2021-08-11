import slixmpp

class PrivMsg(slixmpp.ClientXMPP):
    def __init__(self, jid, password, uname, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.uname = uname
        self.msg = msg

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler('presence_subscribed', self.new_subscribed)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        #Send message of type chat
        self.send_message(mto=self.uname,
                          mbody=self.msg,
                          mtype='chat')
        
        print("Mensaje mandado correctamente")

        keep = True
        while keep:
            cont = input("Desea mandar otro mensaje (y,n):")
            if cont == 'y':
                otro_msg = input("Nuevo mensaje: ")
                self.send_presence()
                await self.get_roster()
                self.send_message(mto=self.uname,
                          mbody=otro_msg,
                          mtype='chat')
                print("Mensaje mandado correctamente")
            elif cont == 'n':
                self.disconnect()
                quit()
            else:
                print("Opcion no valida")


    def new_subscribed(self, presence):
        print(presence.get_from()+' se suscribio a ti!')
