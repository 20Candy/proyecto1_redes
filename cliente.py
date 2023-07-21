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

def delete_account(client, password):
    jid = xmpp.JID(client)
    account = xmpp.Client(jid.getDomain(), debug=[])
    account.connect()

    try:
        account.auth(jid.getNode(), password)
        account.del_account()
        account.disconnect()
        return True
    except xmpp.protocol.NoStream:
        account.disconnect()
        return False
    
async def delete_account(jid, password):

    client = slixmpp.ClientXMPP(jid, password)

    try:
        await client.connect()
        await client.process(forever=False)

        # Request the account removal
        response = await client.Iq()
        response['type'] = 'set'
        fragment = """
            <query xmlns='jabber:iq:register'>
                <remove/>
            </query>
        """
        response.appendxml(fragment)

        try:
            # send the request to the server
            await response.send()
            print(f"Account deleted successfully: {client.boundjid.jid}!")
            return True
        except IqError as e:
            print(f"Error on deleting account: {e.iq['error']['text']}")
            return False
        except IqTimeout:
            print("No response from the server.")
            return False
        finally:
            # Disconnect the client after the account deletion attempt
            await client.disconnect()

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

