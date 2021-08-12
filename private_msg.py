import slixmpp

# Ricardo Antonio Valenzuela Avila 18762
# Redes
# Clase para el manejo de envio de mensajes hacia un usuario en especifico
# Toma como parametro el Jid de la fuente, su contrsania, el Jid del destino y el mensaje a ser inviado
# Tomando como referencia un ejemplo extraido de https://github.com/poezio/slixmpp/blob/master/examples/send_client.py

#Definicion de la clase
class PrivMsg(slixmpp.ClientXMPP):
    def __init__(self, jid, password, uname, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.uname = uname
        self.msg = msg

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('presence_subscribed', self.new_subscribed)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        #Mandar mensaje
        self.send_message(mto=self.uname,
                          mbody=self.msg,
                          mtype='chat')
        
        print('Mensaje mandado correctamente')

        #En caso de mandar mas mensajes o no
        keep = True
        while keep:
            cont = input('Desea mandar otro mensaje (y,n):')
            if cont == 'y':
                otro_msg = input('Nuevo mensaje: ')
                self.send_presence()
                await self.get_roster()
                self.send_message(mto=self.uname,
                          mbody=otro_msg,
                          mtype='chat')
                print('Mensaje mandado correctamente')
            elif cont == 'n':
                #Por cuestiones de funcionamiento se debe desconectar y salir del programa :c
                self.disconnect()
                quit()
            else:
                print('Opcion no valida')
    
    #Menejo de nuevas subscripciones
    def new_subscribed(self, presence):
        print(presence.get_from()+' se suscribio a ti!')
