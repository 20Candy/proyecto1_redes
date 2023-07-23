from asyncio import Future
from typing import Optional, Union
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET

import utils

class Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.name = jid.split('@')[0]
        self.add_event_handler('session_start', self.start)
        self.is_connected = False

    async def start(self, event):
        try:
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            print('Logged in')

            #SUBMENU CON OPCIONES DE CHAT ====================================================================================================================================
            while self.is_connected:

                utils.mostrar_submenu()
                opcion = input("\nIngresa tu opción: ")

                if opcion == "1":
                    print("Opción 1 seleccionada: Mostrar todos los datos y su estado")

                elif opcion == "2":
                    print("Opción 2 seleccionada: Agregar un usuario a los contactos")

                elif opcion == "3":
                    print("Opción 3 seleccionada: Mostrar detalles de contacto de un usuario")

                elif opcion == "4":
                    print("Opción 4 seleccionada: Comunicacion 1 a 1 con cualquier usuario/contacto")

                elif opcion == "5":
                    print("Opción 5 seleccionada: Participar en conversaciones grupales")

                elif opcion == "6":
                    print("Opción 6 seleccionada: Definiar mensaje de presencia")

                elif opcion == "7":
                    print("Opción 7 seleccionada: Enviar/recibir notificaciones")
                
                elif opcion == "8":
                    print("Opción 8 seleccionada: Enviar/recibir archivos")

                elif opcion == "9":
                    print("Opción 9 seleccionada: Cerrar sesion")
                    self.disconnect()
                    self.is_connected = False
                else:
                    utils.mostrar_error()
                

        # MANEJO DE ERRORES ===============================================================================================================================================
        except IqError as err:
            self.is_connected = False
            print(f"Error: {err.iq['error']['text']}")
            self.disconnect()
        except IqTimeout:
            self.is_connected = False
            print('Error: Server is taking too long to respond')
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

   

