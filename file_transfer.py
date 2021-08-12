import slixmpp
from slixmpp.exceptions import IqTimeout


class File_Upload(slixmpp.ClientXMPP):

    """
    A basic client asking an entity if they confirm the access to an HTTP URL.
    """

    def __init__(self, jid, password, recipient, filename, domain=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.filename = filename
        self.domain = domain

        self.add_event_handler("session_start", self.start)
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0071')
        self.register_plugin('xep_0128')
        self.register_plugin('xep_0363')

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        print('Subiendo el archivo...')
        try:
            url = await self['xep_0363'].upload_file(
                self.filename, domain=self.domain, timeout=10
            )
        except IqTimeout:
            raise TimeoutError('Could not send message in time')
        print('Upload success!')

        print('Mandando el archivo a' + self.recipient)
        html = (
            f'<body xmlns="http://www.w3.org/1999/xhtml">'
            f'<a href="{url}">{url}</a></body>'
        )
        message = self.make_message(mto=self.recipient, mbody=url, mhtml=html)
        message['oob']['url'] = url
        message.send()
        print("Se mando el archivo correctamente")
        self.disconnect()
        quit()