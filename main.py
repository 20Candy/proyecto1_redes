# Proyecto de Redes - UVG - 2023
# Autore: Caro Arevalo
# Version 1.0
# Fecha: 09/05/2021
# Descripcion: Este archivo contiene el menu principal del programa, el cual permite al usuario registrarse, iniciar sesion y eliminar su cuenta.
# =================================================================================================================================================

#Importar librerias
import cliente
from cliente import Cliente, Delete_Cliente
import utils
import asyncio

# Menu principal
def menu_principal():

    # Para evitar el error de que el evento no se puede ejecutar en Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # opcion 
    opcion = ""

    # Mientras la opcion sea diferente de 4, se ejecuta el menu principal
    while opcion != "4":

        # Se vuelve a mostrar el menu principal
        utils. mostrar_menu_principal()
        opcion = input("Ingresa tu opción: ")


        #REGISTRO -------------------------------------------------------------------------------------------------------------------
        if opcion == "1":
            print("Opción 1 seleccionada: Registrar una nueva cuenta en el servidor")
            jid, password = utils.get_jid_and_password() # Se llama a la funcion get_jid_and_password de utils.py

            # Se llama a la funcion register de cliente.py
            if cliente.register(jid, password):
                print("Registro exitoso")
            else:
                print("Registro fallido")

        #INICO SESION-----------------------------------------------------------------------------------------------------------------
        elif opcion == "2":
            print("Opción 2 seleccionada: Iniciar sesión con una cuenta")
            jid, password = utils.get_jid_and_password() # Se llama a la funcion get_jid_and_password de utils.py

            # Se llama a la funcion connect de cliente.py, por problemas de certificado del servidor fue necesario poner use_ssl=False
            client = Cliente(jid, password)
            client.connect(disable_starttls=True, use_ssl=False)
            client.process(forever=False)
            
        #ELIMINAR CUENTA-----------------------------------------------------------------------------------------------------------------
        elif opcion == "3":
            print("Opción 3 seleccionada: Eliminar una cuenta")
            jid, password = utils.get_jid_and_password() # Se llama a la funcion get_jid_and_password de utils.py

            # Se llama a la funcion Delete_Cliente de cliente.py, por problemas de certificado del servidor fue necesario poner use_ssl=False
            client = Delete_Cliente(jid, password)
            client.connect(disable_starttls=True, use_ssl=False)
            client.process(forever=False)

        else:
            utils.mostrar_error()

# Se llama a la funcion menu_principal
menu_principal()
