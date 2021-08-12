import slixmpp

# Ricardo Antonio Valenzuela Avila 18762
# Redes
# Clases para el manejo de todo lo relacionado con rooms, creacion, unirse, mandar mensaje, y salir.
# Tomando como referencia un ejemplo extraido de https://github.com/poezio/slixmpp/blob/master/examples/muc.py

#Creacion de grupo, recibe el jid del usuario, su contrasenia, el jid de la Room a crear, y el alias que se usara.
class create_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler('session_start', self.start)

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

        print('Grupo Creado con exito')

        #Por cuestiones de funcionamiento se debe desconectar y salir del programa :c
        self.disconnect()
        quit()

#Unirse a grupo existente, recibe el jid del usuario, su contrasenia, el jid de la Room, y el alias que se usara.
class join_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler('session_start', self.start)

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

        #Por cuestiones de funcionamiento se debe desconectar y salir del programa :c
        self.disconnect()
        quit()

#Salirse de grupo existente, recibe el jid del usuario, su contrasenia, el jid de la Room, y el alias que se usara.
class leave_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler('session_start', self.start)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.alias = alias

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        print('AQUI')
        await self.plugin['xep_0045'].leave_muc(self.room, self.alias)
        print('AQUI')

        #Por cuestiones de funcionamiento se debe desconectar y salir del programa :c
        self.disconnect()
        quit()

#Mandar mensaje a grupo, recibe el jid del usuario, su contrasenia, el jid de la Room y el mensaje
class sendmsg_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler('session_start', self.start)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.msg = msg

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        
        #Envio de mensaje
        self.send_message(
            mto=self.room,
            mbody=self.msg,
            mtype='groupchat',
            mfrom=self.boundjid.full
        )
        print('Mensaje mandado correctamente')
        #En caso de seguir mandando mensajes o salir
        keep = True
        while keep:
            cont = input('Desea mandar otro mensaje (y,n):')
            if cont == 'y':
                otro_msg = input('Nuevo mensaje: ')
                self.send_presence()
                await self.get_roster()
                self.send_message(mto=self.room,
                          mbody=otro_msg,
                          mtype='groupchat',
                          mfrom=self.boundjid.full)
                print('Mensaje mandado correctamente')
            elif cont == 'n':
                #Por cuestiones de funcionamiento se debe desconectar y salir del programa :c
                self.disconnect()
                quit()
            else:
                print('Opcion no valida')

