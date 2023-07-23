import cliente
import logging
from cliente import Cliente, Delete_Cliente
import utils
import asyncio
from optparse import OptionParser


def menu_principal():
    optp = OptionParser()
    optp.add_option('-d', '--debug', help='set loggin to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-q', '--quiet', help='set loggin to ERROR', action='store_const', dest='loglevel', const=logging.ERROR, default=logging.INFO)
    opts, args = optp.parse_args()

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    utils.mostrar_menu_principal()
    opcion = input("\nIngresa tu opción: ")

    while opcion != "4":

        #REGISTRO -------------------------------------------------------------------------------------------------------------------
        if opcion == "1":
            print("Opción 1 seleccionada: Registrar una nueva cuenta en el servidor")
            jid, password = utils.get_jid_and_password()

            if cliente.register(jid, password):
                print("Registro exitoso")
            else:
                print("Registro fallido")

                

        #INICO SESION-----------------------------------------------------------------------------------------------------------------
        elif opcion == "2":
            print("Opción 2 seleccionada: Iniciar sesión con una cuenta")
            jid, password = utils.get_jid_and_password()

            client = Cliente(jid, password)
            client.connect(disable_starttls=True)
            client.process(forever=False)
            

        elif opcion == "3":
            print("Opción 3 seleccionada: Eliminar una cuenta")
            jid, password = utils.get_jid_and_password()
            client = Delete_Cliente(jid, password)
            client.connect(disable_starttls=True)
            client.process(forever=False)


        else:
            utils.mostrar_error()

        utils. mostrar_menu_principal()
        opcion = input("Ingresa tu opción: ")

menu_principal()
