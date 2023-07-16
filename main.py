from registro import registro
from inicioSesion import inicioSesion

def mostrar_menu_principal():
    print("\nBienvenido al chat")
    print("1) Registrar una nueva cuenta en el servidor")
    print("2) Iniciar sesión con una cuenta")
    print("3) Salir")

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

def menu_principal():
    mostrar_menu_principal()
    opcion = input("\nIngresa tu opción: ")

    while opcion != "3":

        #REGISTRO -------------------------------------------------------------------------------------------------------------------
        if opcion == "1":
            print("Opción 1 seleccionada: Registrar una nueva cuenta en el servidor")
            name = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")

            if registro(name, password):
                print("Registro exitoso")
            else:
                print("Registro fallido")

        #INICO SESION-----------------------------------------------------------------------------------------------------------------
        elif opcion == "2":
            print("Opción 2 seleccionada: Iniciar sesión con una cuenta")
            name = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")

            sesionIniciada = False
            
            if inicioSesion(name, password):
                sesionIniciada = True
                print("Inicio de sesión exitoso")
            else:
                print("Inicio de sesión fallido")


            #SUBMENU-----------------------------------------------------------------------------------------------------------------
            if sesionIniciada:

                mostrar_submenu()
                opcion_submenu = input("Ingresa tu opción: ")
                while opcion_submenu != "11":
                    if opcion_submenu == "1":
                        print("Opción 1 seleccionada: Cerrar sesión con una cuenta")
                        # Agrega aquí la lógica para cerrar sesión
                        break
                    elif opcion_submenu == "2":
                        print("Opción 2 seleccionada: Eliminar la cuenta del servidor")
                        # Agrega aquí la lógica para eliminar la cuenta
                        break
                    elif opcion_submenu == "3":
                        print("Opción 3 seleccionada: Mostrar todos los contactos y su estado")
                        # Agrega aquí la lógica para mostrar los contactos
                        break
                    elif opcion_submenu == "4":
                        print("Opción 4 seleccionada: Agregar un usuario a los contactos")
                        # Agrega aquí la lógica para agregar un usuario a los contactos
                        break
                    elif opcion_submenu == "5":
                        print("Opción 5 seleccionada: Mostrar detalles de contacto de un usuario")
                        # Agrega aquí la lógica para mostrar detalles de un contacto
                        break
                    elif opcion_submenu == "6":
                        print("Opción 6 seleccionada: Comunicación 1 a 1 con cualquier usuario/contacto")
                        # Agrega aquí la lógica para la comunicación 1 a 1
                        break
                    elif opcion_submenu == "7":
                        print("Opción 7 seleccionada: Participar en conversaciones grupales")
                        # Agrega aquí la lógica para participar en conversaciones grupales
                        break
                    elif opcion_submenu == "8":
                        print("Opción 8 seleccionada: Definir mensaje de presencia")
                        # Agrega aquí la lógica para definir el mensaje de presencia
                        break
                    elif opcion_submenu == "9":
                        print("Opción 9 seleccionada: Enviar/recibir notificaciones")
                        # Agrega aquí la lógica para enviar/recibir notificaciones
                        break
                    elif opcion_submenu == "10":
                        print("Opción 10 seleccionada: Enviar/recibir archivos")
                        # Agrega aquí la lógica para enviar/recibir archivos
                        break
                    else:
                        mostrar_error()
                    opcion_submenu = input("Ingresa tu opción: ")
        else:
            mostrar_error()

        mostrar_menu_principal()
        opcion = input("Ingresa tu opción: ")

menu_principal()
