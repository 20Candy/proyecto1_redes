def get_jid_and_password():
	"""
	Get the jid (email) and password of the user
	"""
	jid = input('JID: ')
	password = input('Password: ')
	return jid, password

def mostrar_menu_principal():
    print("\nBienvenido al chat. A continuacion de muestran las opciones sin iniciar sesion")
    print("1) Registrar una nueva cuenta en el servidor")
    print("2) Iniciar sesión con una cuenta")
    print("3) Eliminar una cuenta")
    print("4) Salir")

def mostrar_submenu():
    print("\nBienvenido al tu sesion de chat")
    print("1) Mostrar todos los contactos y su estado")
    print("2) Agregar un usuario a los contactos")
    print("3) Mostrar detalles de contacto de un usuario")
    print("4) Comunicacion 1 a 1 con cualquier usuario/contacto")
    print("5) Participar en conversaciones grupales")
    print("6) Definiar mensaje de presencia")
    print("7) Enviar/recibir notificaciones")
    print("8) Enviar/recibir archivos")
    print("9) Cerrar sesion")

def mostrar_status_menu():
    print("\nSelecciona el estado que deseas mostrar:")
    print("1) Disponible")
    print("2) Ausente")
    print("3) Ocupado")
    print("4) No molestar")

def mostrar_error():
    print("Opción inválida. Por favor, intenta de nuevo.")

def get_status():

    status_incorrecto = True

    while status_incorrecto:
        mostrar_status_menu()
        status = input('')

        if status == '1':
            status_incorrecto = False
            status = 'chat'
        elif status == '2':
            status_incorrecto = False
            status = 'away'
        elif status == '3':
            status_incorrecto = False
            status = 'xa'
        elif status == '4':
            status_incorrecto = False
            status = 'dnd'
        else:
            mostrar_error()
        
    print('Write down your status message: ')
    status_message = input('')
    return status, status_message
