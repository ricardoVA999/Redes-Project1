import slixmpp
class join_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)


        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.alias = alias

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        
        self.plugin['xep_0045'].join_muc(self.room, self.alias)
    
    def muc_message(self, msg):
        pass
    
    def muc_online(self, presence):
        pass
