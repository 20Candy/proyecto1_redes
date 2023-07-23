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

    async def add_contact(self):
        jid_to_add = input("Ingresa el JID del usuario que deseas agregar (Ejemplo: usuario@servidor.com): ")
        try:
            self.send_presence_subscription(pto=jid_to_add, pfrom=self.boundjid.full, ptype='subscribe')
            print(f"Solicitud de suscripción enviada a {jid_to_add}")
        except IqError as e:
            print(f"Error sending subscription request: {e.iq['error']['text']}")
        except IqTimeout:
            print("No response from server.")

    async def show_contacts_status(self):
        # Extract roster items and their presence status
        roster = self.client_roster
        contacts = roster.keys()
        my_contacts = []

        if not contacts:
            print("No contacts found.")
            return

        for jid in contacts:
            sub = roster[jid]['subscription']
            name = roster[jid]['name']
            connections = roster.presence(jid)
            status = 'Offline'

            if connections:
                status = connections[0]['show'] or 'Online'
            my_contacts.append((name, jid, status, sub))

        print("\nContact List:")
        print("JID\t\t\t\tName\t\t\t\tStatus\t\t\t\tSubscription")
        print("--------------------------------------------------------------------------")
        for i in my_contacts:
            print(f"{i[1]}\t\t\t\t{i[0]}\t\t\t\t{i[2]}\t\t\t\t{i[3]}")


    async def set_presence_message(self):
        show_options = ['away', 'chat', 'dnd', 'xa', None]
        show = None
        status = input("Ingresa tu mensaje de estado: ")
        print("Opciones de disponibilidad:")
        print("1. away")
        print("2. chat")
        print("3. dnd")
        print("4. xa")
        print("5. clear (no custom presence message)")
        option = input("Ingresa el número de la opción que deseas: ")

        if option.isdigit():
            option = int(option)
            if option >= 1 and option <= 4:
                show = show_options[option - 1]

        self.send_presence(pshow=show, pstatus=status)
        print("Mensaje de presencia actualizado")

    async def send_message_to_contact(self):
        jid_to_send = input("Ingresa el JID del usuario/contacto al que deseas enviar un mensaje: ")
        message = input("Ingresa tu mensaje: ")

        try:
            self.send_message(mto=jid_to_send, mbody=message, mtype='chat')
            print(f"Mensaje enviado a {jid_to_send}: {message}")
        except IqError as e:
            print(f"Error sending the message: {e.iq['error']['text']}")
        except IqTimeout:
            print("No response from server.")
            

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
                    print("Opción 1 seleccionada: Mostrar todos los contactos y su estado")
                    await self.show_contacts_status()

                elif opcion == "2":
                    print("Opción 2 seleccionada: Agregar un usuario a los contactos")
                    await self.add_contact()

                elif opcion == "3":
                    print("Opción 3 seleccionada: Mostrar detalles de contacto de un usuario")

                elif opcion == "4":
                    print("Opción 4 seleccionada: Comunicacion 1 a 1 con cualquier usuario/contacto")
                    await self.send_message_to_contact()


                elif opcion == "5":
                    print("Opción 5 seleccionada: Participar en conversaciones grupales")

                elif opcion == "6":
                    print("Opción 6 seleccionada: Definir mensaje de presencia")
                    await self.set_presence_message()

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

   

