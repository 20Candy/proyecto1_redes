# Proyecto de Redes - UVG - 2023
# Autore: Caro Arevalo
# Version 1.0
# Fecha: 09/05/2021
# Descripcion: Este archivo contiene todas las funciones necesarias para el funcionamiento del programa utilizando princiapalmente la linbreia slixmpp.
# ======================================================================================================================================================

#Importar librerias externas
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET
from aioconsole import ainput
from aioconsole.stream import aprint
import asyncio
import tkinter as tk
from tkinter import messagebox
import base64

#Importar librerias propias
import utils

#   CLASE CLIENTE ======================================================================================================================================================
class Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        # Variables de clase
        self.name = jid.split('@')[0]
        self.is_connected = False
        self.actual_chat = ''
        self.room = ''
        self.nick = ''

        #generado con chatgpt 
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0066') # Out of Band Data
        self.register_plugin('xep_0363') # HTTP File Upload

        #Handlers de eventos
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.chat_received)
        self.add_event_handler('disco_items', self.print_rooms)
        self.add_event_handler('groupchat_message', self.chatroom_message)
        self.add_event_handler('presence', self.presence_handler)

    #Fucniones handler de eventos =========================================================================================================================================

    # Funcion para recibir mensajes ---------------------------------------------------------------------------------------------------------------------------------------
    async def chat_received(self, message):

        # si el mensaje es de tipo chat (1 a 1)
        if message['type'] == 'chat':
            # obtener solo el nombre del usuaroi sin el dominio
            user = str(message['from']).split('@')[0]

            # aparartado de recepcion de archivos
            if message['body'].startswith("file://"):  
                file_info = message['body'][7:].split("://") # se obtiene la informacion del archivo
                extension = file_info[0] # se obtiene la extension del archivo
                encoded_data = file_info[1] # se obtiene el contenido del archivo en base64
                
                try:
                    decoded_data = base64.b64decode(encoded_data) # se decodifica el contenido del archivo
                    with open("recibido." + extension, "wb") as file:
                        file.write(decoded_data)
                        self.show_popup_notification(f"Archivo recibido y guardado como recibido.{extension} por parte de {user}")

                except Exception as e:
                    print("\nError decoding and saving the received file:", e)

            # apartado de recepcion de mensajes
            else:
                # si el usuario que envia el mensaje es el mismo que el usuario con el que se esta chateando
                if user == self.actual_chat.split('@')[0]:
                    print(f'{user}: {message["body"]}')

                # en caso contrraio se muestra una notificacion
                else:
                    self.show_popup_notification(f"Tienes un nuevo mensaje de {user}")

    # Funcion para recibir mensajes de salas de chat --------------------------------------------------------------------------------------------------------------------------------
    async def chatroom_message(self, message=''):

        user = message['mucnick'] # se obtiene el nombre del usuario que envia el mensaje
        is_actual_room = self.room in str(message['from'])
        display_message = f'{user}: {message["body"]}'

        if user != self.boundjid.user:
            if is_actual_room:
                print(display_message)
            else:
                self.show_popup_notification(f"Tienes un nuevo mensaje de {user} en la sala de chat {self.room.split('@')[0]}")


    # Funcion para mostrar salas de chat disponibles ----------------------------------------------------------------------------------------------------------------------
    async def print_rooms(self, iq):

        if iq['type'] == 'result':
            print('\nSalas de chat disponibles:')
            for salita in iq["disco_items"]:
                print(f'Nomrbre:{salita["name"]}')
                print(f'JID: {salita["jid"]}')
                print("")

    # Funcion para manejar presencia ---------------------------------------------------------------------------------------------------------------------------------------
    async def presence_handler(self, presence):

        # Si se obtiene una solicitud de suscripcion, se acepta automaticamente --------------------------------------------------------------------------------------------
        if presence['type'] == 'subscribe':
            try:
                self.send_presence_subscription(pto=presence['from'], ptype='subscribed')
                await self.get_roster()
                self.show_popup_notification("Solicitud de suscripción aceptada de " + str(presence['from']).split('@')[0]) # se muestra una notificacion
            except IqError as e:
                print(f"Error accepting subscription request: {e.iq['error']['text']}")
            except IqTimeout:
                print("No response from server.")

        # Si se obtiene una presencia ---------------------------------------------------------------------------------------------------------------------------------------
        else:
            
            # mostrar notificacion solo si se esta conectado ----------------------------------------------------------------------------------------------------------------
            if self.is_connected:

                if presence['type'] == 'available':
                    self.show_presence_notification(presence, True) 

                elif presence['type'] == 'unavailable':
                    self.show_presence_notification(presence, False)
                
                else:
                    self.show_presence_notification(presence, None)

    # Funcion para mostrar notificacion de nuevo mensaje ==================================================================================================================
    def show_popup_notification(self, mensaje):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Nuevo Mensaje", mensaje)
        root.destroy()

    # Funcion para mostrar notificacion de presencia =====================================================================================================================
    def show_presence_notification(self, presence, is_available):

        # si el usuario que envia la presencia es diferente al usuario actual y no es una sala de chat, se muestra la notificacion -------------------------------------------
        if str(presence['from']).split("/")[0] != self.boundjid.bare and "conference" not in str(presence['from']):

            # obtener el estado del usuario
            if is_available:
                show = 'available'
            elif is_available == False:
                show = 'offline'
            else:
                show = presence['show']

            # obtener el mensaje de estado del usuario
            user = (str(presence['from']).split('/')[0])
            #obtener presencia de cada contacto
            status = presence['status']

            if status != '':
                notification_message = f'{user} is {show} - {status}'
            else:
                notification_message = f'{user} is {show}'

            self.show_popup_notification(notification_message) # se muestra la notificacion


    # Funciones asincronas ================================================================================================================================================

    # Funcion para definir mensaje de presencia ===========================================================================================================================
    async def change_presece(self):
        status, status_message = utils.get_status() # se llama a la funcion get_status de utils.py
        self.status = status
        self.status_message = status_message
        self.send_presence(pshow=self.status, pstatus=self.status_message) 
        await self.get_roster() 

    # Funcion para agregar un contacto ====================================================================================================================================
    async def add_contact(self):
        jid_to_add = input("Ingresa el JID del usuario que deseas agregar: ")
        try:
            # Enviar solicitud de suscripcion
            self.send_presence_subscription(pto = jid_to_add)
            print(f"Solicitud de suscripción enviada a {jid_to_add}")
            await self.get_roster()
        except IqError as e:
            print(f"Error sending subscription request: {e.iq['error']['text']}")
        except IqTimeout:
            print("No response from server.")

    # Funcion para mostrar todos los contactos y su estado ===============================================================================================================
    async def show_contacts_status(self):
        # obtener lista de contactos
        roster = self.client_roster
        contacts = roster.keys()
        contact_list = []

        # si no hay contactos, se muestra un mensaje de que no hay contactos
        if not contacts:
            print("No contacts found.")
            return

        # obtener informacion de cada contacto
        for jid in contacts:
            user = jid

            #obtener presencia de cada contacto
            connection = roster.presence(jid)
            show = 'available'
            status = ''

            # obtener estado y mensaje de estado de cada contacto
            for answer, presence in connection.items():
                if presence['show']:
                    show = presence['show']
                if presence['status']:
                    status = presence['status']

            contact_list.append((user, show, status))

        print("\nLista de contactos:")
        for c in contact_list:

            # si el contacto es el usuario actual, se muestra un mensaje de que es el usuario actual
            if c[0] == self.boundjid.bare:
                print("\nUsuario actual:")

            print(f"Contacto: {c[0]}")
            print(f"Estado: {c[1]}")
            print(f"Mensaje de estado: {c[2]}")
            print("")
        print("")

    # Funcion para mostrar detalles de contacto de un usuario ============================================================================================================
    async def show_contact_details(self):
        jid_to_find = input("Ingresa el JID del usuario/contacto que deseas buscar: ") # se obtiene el JID del usuario a buscar
        roster = self.client_roster
        contacts = roster._jids.keys()

        # si el usuario no se encuentra en la lista de contactos, se muestra un mensaje de que no se encuentra en la lista de contactos ---------------------------------------
        if jid_to_find not in contacts:
            print("El usuario/contacto no se encuentra en la lista de contactos.")
            return

        # Obtener presencia del contacto
        connection = roster.presence(jid_to_find)
        show = 'available'
        status = ''

        # obtener estado y mensaje de estado del contacto
        for answer, presence in connection.items():
            if presence['show']:
                show = presence['show']
            if presence['status']:
                status = presence['status']


        print("\nDetalles del contacto:")
        print(f"Usuario: {jid_to_find}")
        print(f"Mensaje de estado: {status}")
        print("")

    # Funcion para enviar mensaje a un contacto ==========================================================================================================================
    async def send_message_to_contact(self):

        jid = await ainput('Ingrasa el JID del usuario\n')  # se obtiene el JID del usuario a buscar
        self.actual_chat = jid

        await aprint(f'\n===================== Espacio de chat" {jid.split("@")[0]} =====================')
        await aprint('*Para salir, por favor presiona x')
        chatting = True

        # mientras se este chateando
        while chatting:
            message = await ainput('')
            if message == 'x':
                chatting = False
                self.actual_chat = ''
            else:
                self.send_message(mto=jid, mbody=message, mtype='chat')

    # Funcion para mostrar todas las salas de chat existentes ============================================================================================================
    async def show_all_rooms(self):
        try:
            # obtener lista de salas de chat
            await self['xep_0030'].get_items(jid = "conference.alumchat.xyz")
        except (IqError, IqTimeout):
            print("There was an error, please try again later")

    # Funcion para crear una sala de chat =================================================================================================================================
    async def create_chat_room(self,room_name):
        try:
            # crear sala de chat
            self.plugin['xep_0045'].join_muc(room_name, self.boundjid.user)

            await asyncio.sleep(2) # esperar 2 segundos

            # configurar sala de chat
            form = self.plugin['xep_0004'].make_form(ftype='submit', title='Configuracion de sala de chat')
            form['muc#roomconfig_roomname'] = room_name
            form['muc#roomconfig_persistentroom'] = '1'
            form['muc#roomconfig_publicroom'] = '1'
            form['muc#roomconfig_membersonly'] = '0'
            form['muc#roomconfig_allowinvites'] = '0'
            form['muc#roomconfig_enablelogging'] = '1'
            form['muc#roomconfig_changesubject'] = '1'
            form['muc#roomconfig_maxusers'] = '100'
            form['muc#roomconfig_whois'] = 'anyone'
            form['muc#roomconfig_roomdesc'] = 'Chat de prueba'
            form['muc#roomconfig_roomowners'] = [self.boundjid.user]

            await self.plugin['xep_0045'].set_room_config(room_name, config=form)

            # enviar mensaje de confirmacion
            self.send_message(mto=room_name, mbody="Sala de chat creada", mtype='groupchat')

            print(f"Sala de chat '{room_name}' creada correctamente.")
        except IqError as e:
            print(f"Error al crear la sala de chat: {e}")
        except IqTimeout:
            print("Tiempo de espera agotado al crear la sala de chat.")
                
    # Funcion para unirse a una sala de chat existente ==================================================================================================================
    async def join_chat_room(self, roomName):
        self.room = roomName # se guarda el nombre de la sala de chat
        self.nick = self.boundjid.user # se guarda el nombre de usuario

        # obtener ultimos mensajes de la sala de chat
        print(f"\nUtlimos mensajes de  {roomName}...")

        try:
            # unirse a la sala de chat
            await self.plugin['xep_0045'].join_muc(roomName, self.nick)
        except IqError as e:
            print(f"Error creating chat room: {e.iq['error']['text']}")
        except IqTimeout:
            print("No response from server.")
            return

        # sala de chat
        await aprint(f'\n===================== Espacio de chat {self.room.split("@")[0]} =====================')
        await aprint('*Para salir, por favor presiona x')
        chatting = True

        # mientras se este chateando
        while chatting:
            message = await ainput('')
            if message == 'x':
                chatting = False
                self.actual_chat = ''
                self.exit_room()
            else:
                self.send_message(self.room, message, mtype='groupchat')

    # Funcion para salir de una sala de chat =============================================================================================================================
    def exit_room(self):
        self['xep_0045'].leave_muc(self.room, self.nick)
        self.room = None
        self.nick = None

    # Funcion para enviar archivos ========================================================================================================================================
    async def send_file(self, recipient_jid, file_path):
        extension = file_path.split(".")[-1] # se obtiene la extension del archivo

        with open(file_path, "rb") as file: # se abre el archivo
            file_data = file.read()

        # se codifica el archivo en base64
        encoded_data = base64.b64encode(file_data).decode()
        message =  message = f"file://{extension}://{encoded_data}" # se crea el mensaje con la informacion del archivo en base64

        self.send_message(mto=recipient_jid, mbody=message, mtype='chat')


    # Funcion principal =================================================================================================================================================
    
    async def start(self, event):
        try:
            # Iniciar sesion
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            print('Logged in')

            # inicio de menu
            asyncio.create_task(self.run_main_event_loop())

            
        # MANEJO DE ERRORES ===============================================================================================================================================
        except IqError as err:
            self.is_connected = False
            print(f"Error: {err.iq['error']['text']}")
            self.disconnect()
        except IqTimeout:
            self.is_connected = False
            print('Error: Server is taking too long to respond')
            self.disconnect()

    # Funcion para correr el loop de eventos =============================================================================================================================
    async def run_main_event_loop(self):
        
        #SUBMENU CON OPCIONES DE CHAT ====================================================================================================================================
        while self.is_connected:

            utils.mostrar_submenu()
            opcion = await ainput("\nIngresa tu opción: ")

            #Funcion para mostrar todos los contactos y su estado =======================================================================================================
            if opcion == "1":
                print("Opción 1 seleccionada: Mostrar todos los contactos y su estado")
                await self.show_contacts_status()

            #Funcion para agregar un usuario a los contactos ==============================================================================================================
            elif opcion == "2":
                print("Opción 2 seleccionada: Agregar un usuario a los contactos")
                await self.add_contact()

            #Funcion para mostrar detalles de contacto de un usuario =======================================================================================================
            elif opcion == "3":
                print("Opción 3 seleccionada: Mostrar detalles de contacto de un usuario")
                await self.show_contact_details()

            #Funcion para comunicacion 1 a 1 con cualquier usuario/contacto =================================================================================================
            elif opcion == "4":
                print("Opción 4 seleccionada: Comunicacion 1 a 1 con cualquier usuario/contacto")
                await self.send_message_to_contact()
                
            elif opcion == "5":
                print("Opción 5 seleccionada: Participar en conversaciones grupales")
                
                # SUBMENU CON OPCIONES DE GRUPOS ============================================================================================================================
                utils.mostrar_menu_grupos()
                opcion = await ainput("\nIngresa tu opción: ")

                # Funcion para crear una sala de chat ========================================================================================================================
                if opcion == "1":
                    print("Opción 1 seleccionada: Crear una sala de chat")

                    room = input("Ingresa el nombre de la sala de chat: ")
                    roomName = f"{room}@conference.alumchat.xyz"
                    await self.create_chat_room(roomName)

                # Funcion para unirse a una sala de chat existente ==========================================================================================================
                elif opcion == "2":
                    print("Opción 2 seleccionada: Unirse a una sala de chat existente")
                    room = input("Ingresa el nombre de la sala de chat: ")
                    await self.join_chat_room(room)
                    
                # Funcion para mostrar todas las salas de chat existentes ==================================================================================================
                elif opcion == "3":
                    print("Opción 3 seleccionada: Mostrar todas las salas de chat existentes")
                    await self.show_all_rooms()
                    
                # Funcion para regresar ====================================================================================================================================
                elif opcion == "4":
                    print("Opción 4 seleccionada: Regresar")
                    pass

            # Funcion para definir mensaje de presencia ====================================================================================================================
            elif opcion == "6":
                print("Opción 6 seleccionada: Definir mensaje de presencia")
                await self.change_presece()

            # Funcion para enviar archivos ====================================================================================================================================
            elif opcion == "7":
                print("Opción 7 seleccionada: Enviar archivos")
                user = input("Ingresa el JID del usuario al que deseas enviar el archivo: ")
                path = input("Ingresa la ruta del archivo que deseas enviar: ")
                await self.send_file(user, path)
        
            # Funcion para cerrar sesion ====================================================================================================================================
            elif opcion == "8":
                print("Opción 8 seleccionada: Cerrar sesion")
                self.disconnect()
                self.is_connected = False
            else:
                utils.mostrar_error()

            await asyncio.sleep(0.1)  # se espera 0.1 segundos

# ======================================================================================================================================================================

#  CLASE DELETE_CLIENTE =================================================================================================================================================

class Delete_Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.add_event_handler("session_start", self.start)
        
    # Funcion para eliminar cuenta ========================================================================================================================================
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.unregister()
        self.disconnect()
        
    # Funcion para desregistrar cuenta ====================================================================================================================================
    async def unregister(self):
        response = self.Iq()
        response['type'] = 'set'
        response['from'] = self.boundjid.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>") # creado con chatgpt
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
# Funcion para registrar cuenta ========================================================================================================================================
def register(client, password):

	jid = xmpp.JID(client)
	account = xmpp.Client(jid.getDomain(), debug=[])
	account.connect()
	return bool(
	    xmpp.features.register(account, jid.getDomain(), {
	        'username': jid.getNode(),
	        'password': password
	    }))
