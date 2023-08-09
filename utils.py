# Proyecto de Redes - UVG - 2023
# Autore: Caro Arevalo
# Version 1.0
# Fecha: 09/05/2021
# Descripcion: Este archivo contiene funciones auxiliares para el programa.
# ======================================================================================================================================================

# Funcion para obtener el JID y la contraseña
def get_jid_and_password():
	jid = input('JID: ')
	password = input('Password: ')
	return jid, password

# Funcion para mostrar el menu principal
def mostrar_menu_principal():
    print("\nBienvenido al chat. A continuacion de muestran las opciones sin iniciar sesion")
    print("1) Registrar una nueva cuenta en el servidor")
    print("2) Iniciar sesión con una cuenta")
    print("3) Eliminar una cuenta")
    print("4) Salir")

# Funcion para mostrar el menu de opciones
def mostrar_submenu():
    print("\nBienvenido al tu sesion de chat")
    print("1) Mostrar todos los contactos y su estado")
    print("2) Agregar un usuario a los contactos")
    print("3) Mostrar detalles de contacto de un usuario")
    print("4) Comunicacion 1 a 1 con cualquier usuario/contacto")
    print("5) Participar en conversaciones grupales")
    print("6) Definiar mensaje de presencia")
    print("7) Enviar archivos")
    print("8) Cerrar sesion")

# Funcion para mostrar el menu de opciones de grupos
def mostrar_menu_grupos():

    print("\nSelecciona el estado que deseas mostrar:")
    print("1) Crear una sala de chat")
    print("2) Unirse a una sala de chat existente")
    print("3) Mostrar todas las salas de chat existentes")
    print("4) Regresar")

# Funcion para mostrar el menu de opciones de estado
def mostrar_status_menu():
    print("\nSelecciona la opcion que desees realizar:")
    print("1) Disponible")
    print("2) Ausente")
    print("3) Ocupado")
    print("4) No molestar")

# Funcion para mostrar el menu de opciones de estado
def mostrar_error():
    print("Opción inválida. Por favor, intenta de nuevo.")


# Funcion para obtener el estado
def get_status():

    status_incorrecto = True

    # Mientras el estado sea incorrecto, se ejecuta el menu de estado
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
        
    print('Escribe tu mensaje de estado: ')
    status_message = input('')
    return status, status_message 
