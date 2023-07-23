import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET

class Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.name = jid.split('@')[0]
        self.add_event_handler('session_start', self.start)

    async def start(self, event):
        try:
            self.send_presence()
            await self.get_roster()
            print('Welcome to the chat')
        except IqError as e:
            print('Not abble to log in')
            self.disconnect()
        except IqTimeout:
            print('Not abble to connect')
            self.disconnect()   
        

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

   

