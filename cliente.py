import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET

class Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        self.name = jid.split('@')[0]

        ## plugins
        self.register_plugin('xep_0030') # Service Discovery    
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub

		# events
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.chat_recived)
        self.add_event_handler('groupchat_message', self.chatroom_message)
        self.add_event_handler('disco_items', self.print_rooms)


# ======================================================================================================================================================================
class Delete_Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.add_event_handler("session_start", self.start)
        
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.unregister()
        self.disconnect()
        
    async def unregister(self):
        response = self.Iq()
        response['type'] = 'set'
        response['from'] = self.boundjid.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        response.append(fragment)
        
        try:
            await response.send()
            print(f"Account deleted successfully: {self.boundjid.jid}!")
        except IqError as e:
            print(f"Error on deleted account: {e.iq['error']['text']}")
            self.disconnect()
        except IqTimeout:
            print("No response from server.")
            self.disconnect()

#======================================================================================================================================================================
def register(client, password):

	jid = xmpp.JID(client)
	account = xmpp.Client(jid.getDomain(), debug=[])
	account.connect()
	return bool(
	    xmpp.features.register(account, jid.getDomain(), {
	        'username': jid.getNode(),
	        'password': password
	    }))

   

