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
    print("1) Cerrar sesión con una cuenta")
    print("2) Eliminar la cuenta del servidor")
    print("3) Mostrar todos los contactos y su estado")
    print("4) Agregar un usuario a los contactos")
    print("5) Mostrar detalles de contacto de un usuario")
    print("6) Comunicación 1 a 1 con cualquier usuario/contacto")
    print("7) Participar en conversaciones grupales")
    print("8) Definir mensaje de presencia")
    print("9) Enviar/recibir notificaciones")
    print("10) Enviar/recibir archivos")
    print("11) Salir")

def mostrar_error():
    print("Opción inválida. Por favor, intenta de nuevo.")