import slixmpp

class create_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.alias = alias

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        
        status = 'open'
        self.plugin['xep_0045'].join_muc(
            self.room,
            self.alias,
            pstatus=status,
            pfrom=self.boundjid.full)

        await self.plugin['xep_0045'].set_affiliation(self.room, jid = self.boundjid.full,
            affiliation = 'owner')

        print("Grupo Creado con exito")
        self.disconnect()
        quit()


class join_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.alias = alias

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        
        status = 'open'
        self.plugin['xep_0045'].join_muc(
            self.room,
            self.alias,
            pstatus=status,
            pfrom=self.boundjid.full)

        self.disconnect()
        quit()

class leave_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.alias = alias

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        print("AQUI")
        await self.plugin['xep_0045'].leave_muc(self.room, self.alias)
        print("AQUI")
        self.disconnect()
        quit()

class sendmsg_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.msg = msg

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        self.send_message(
            mto=self.room,
            mbody=self.msg,
            mtype='groupchat',
            mfrom=self.boundjid.full
        )
        print("Mensaje mandado correctamente")
        keep = True
        while keep:
            cont = input("Desea mandar otro mensaje (y,n):")
            if cont == 'y':
                otro_msg = input("Nuevo mensaje: ")
                self.send_presence()
                await self.get_roster()
                self.send_message(mto=self.room,
                          mbody=otro_msg,
                          mtype='groupchat',
                          mfrom=self.boundjid.full)
                print("Mensaje mandado correctamente")
            elif cont == 'n':
                self.disconnect()
                quit()
            else:
                print("Opcion no valida")

