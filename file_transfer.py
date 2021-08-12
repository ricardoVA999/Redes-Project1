import slixmpp
from slixmpp.exceptions import IqTimeout

# Ricardo Antonio Valenzuela Avila 18762
# Redes
# Clase para el manejo de envio de archivos hacia un usuario en especifico
# Toma como parametro el Jid de la fuente, su contrsania, el Jid del destino y el archivo a ser enviado
# Tomando como referencia un ejemplo extraido de https://github.com/poezio/slixmpp/blob/master/examples/http_upload.py

#Definicion de la clase
class File_Upload(slixmpp.ClientXMPP):

    #Parametros de entrada e inicializacion de la clase
    def __init__(self, jid, password, recipient, filename, domain=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.filename = filename
        self.domain = domain

        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0071')
        self.register_plugin('xep_0128')
        self.register_plugin('xep_0363')

    #Subida de archivo y mandarselo al destinatario
    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        print('Subiendo el archivo...')
        try:
            url = await self['xep_0363'].upload_file(
                self.filename, domain=self.domain, timeout=10
            )
        except IqTimeout:
            print('Error no se pudo acceder al servidor')

        print('El archivo se subio exitosamente')

        print('Mandando el archivo a' + self.recipient)
        html = (
            f'<body xmlns="http://www.w3.org/1999/xhtml">'
            f'<a href="{url}">{url}</a></body>'
        )
        message = self.make_message(mto=self.recipient, mbody=url, mhtml=html)
        message['oob']['url'] = url
        message.send()
        print('Se mando el archivo correctamente')

        #Por cuestiones de funcionamiento se debe desconectar y salir del programa :c
        self.disconnect()
        quit()