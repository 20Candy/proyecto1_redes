from asyncio import Future
from typing import Optional, Union
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET
from aioconsole import ainput
from aioconsole.stream import aprint
import asyncio

import utils

class Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.name = jid.split('@')[0]
        self.is_connected = False

        
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('subscription_request', self.accept_subscription)
        self.add_event_handler('message', self.chat_recived)


    async def accept_subscription(self, presence):
        if presence['type'] == 'subscribe':
            # Automatically accept the subscription request
            try:
                self.send_presence_subscription(pto=presence['from'], ptype='subscribed')
                await self.get_roster()
                print(f"Accepted subscription request from {presence['from']}")
            except IqError as e:
                print(f"Error accepting subscription request: {e.iq['error']['text']}")
            except IqTimeout:
                print("No response from server.")

    async def chat_recived(self, message):
        if message['type'] == 'chat':
            user = str(message['from']).split('@')[0]
            if user == self.actual_chat.split('@')[0]:
                print(f'{user}: {message["body"]}')
            else:
                print(f'You have a new message from {user}')

    def send_message_p_g(self, to, message = '', typeM = "chat"):

        self.send_message(
            mto=to,
            mbody=message,
            mtype=typeM
		)

    async def change_presece(self):
        status, status_message = utils.get_status()
        self.status = status
        self.status_message = status_message
        self.send_presence(pshow=self.status, pstatus=self.status_message) 
        await self.get_roster() 
    
    async def add_contact(self):
        jid_to_add = input("Ingresa el JID del usuario que deseas agregar (Ejemplo: usuario@servidor.com): ")
        try:
            self.send_presence_subscription(pto = jid_to_add)
            print(f"Solicitud de suscripción enviada a {jid_to_add}")
            await self.get_roster()
        except IqError as e:
            print(f"Error sending subscription request: {e.iq['error']['text']}")
        except IqTimeout:
            print("No response from server.")


    async def show_contacts_status(self):
        # Extract roster items and their presence status
        roster = self.client_roster
        contacts = roster.keys()
        contact_list = []

        if not contacts:
            print("No contacts found.")
            return

        for jid in contacts:
            user = jid

            #obtener presencia de cada contacto
            connection = roster.presence(jid)
            show = 'available'
            status = ''

            for answer, presence in connection.items():
                if presence['show']:
                    show = presence['show']
                if presence['status']:
                    status = presence['status']

            contact_list.append((user, show, status))

        print("\nLista de contactos:")
        for c in contact_list:
            print(f"Contacto: {c[0]}")
            print(f"Estado: {c[1]}")
            print(f"Mensaje de estado: {c[2]}")
            print("")
        print("")

    async def show_contact_details(self):
        jid_to_find = input("Ingresa el JID del usuario/contacto que deseas buscar: ")
        roster = self.client_roster
        contacts = roster._jids.keys()

        if jid_to_find not in contacts:
            print("El usuario/contacto no se encuentra en la lista de contactos.")
            return

        # Obtener presencia del contacto
        connection = roster.presence(jid_to_find)
        show = 'available'
        status = ''

        for answer, presence in connection.items():
            if presence['show']:
                show = presence['show']
            if presence['status']:
                status = presence['status']


        print("\nDetalles del contacto:")
        print(f"Usuario: {jid_to_find}")
        print(f"Mensaje de estado: {status}")
        print("")

            
    async def send_message_to_contact(self):
        jid_to_send = input("Ingresa el JID del usuario/contacto al que deseas enviar un mensaje: ")
        message = input("Ingresa tu mensaje: ")

        try:
            self.send_message(mto=jid_to_send, mbody=message, mtype='chat')
            print(f"Mensaje enviado a {jid_to_send}: {message}")
            await self.get_roster()
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
                    await self.show_contact_details()

                elif opcion == "4":
                    print("Opción 4 seleccionada: Comunicacion 1 a 1 con cualquier usuario/contacto")
                    

                    jid = await ainput('Enter the JID of the user:\n>')
                    self.actual_chat = jid
                    await aprint(f'===================== Welcom to the chat with {jid.split("@")[0]} =====================')
                    await aprint('To exit the chat, type "exit" and then press enter')
                    chatting = True
                    while chatting:
                        message = await ainput('')
                        if message == 'exit':
                            chatting = False
                            self.actual_chat = ''
                        else:
                            self.send_message_p_g(jid, message)
                            await asyncio.sleep(0.5) # wait 0.5 seconds to make sure the message was sent

                elif opcion == "5":
                    print("Opción 5 seleccionada: Participar en conversaciones grupales")
                    print("PENDIENTE")

                elif opcion == "6":
                    print("Opción 6 seleccionada: Definir mensaje de presencia")
                    await self.change_presece()

                elif opcion == "7":
                    print("Opción 7 seleccionada: Enviar/recibir notificaciones")
                    print("PENDIENTE")
                
                elif opcion == "8":
                    print("Opción 8 seleccionada: Enviar/recibir archivos")
                    print("PENDIENTE")

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

   

