from logging import log
from os import close

from slixmpp import jid
from client import register_to_server, my_client
from getpass import getpass

still_running = True

def logginMenu():
    print('''--------Menu de Inicio--------
    1. Iniciar Sesion
    2. Registrar nueva cuenta
    3. Salir''')

def mainMenu():
    print('''
    1. Ver conectados
    2. Mandar mensaje privado
    3. Madar mensaje general
    ''')

def my_session(event):
    is_in_session = True
    xmpp.start()
    print("Bienvenido:", xmpp.boundjid.bare)
    while is_in_session:
        mainMenu()
        option = input("Ingrese su accion:")
        if option == "1":
            pass
        else:
            is_in_session = False






while(still_running):
    logginMenu()
    choice = input('Ingrese su accion: ')
    if choice == '1':
        print('\n--------Iniciemos Sesion--------')
        uname = input('Nombre  de usuario: ')
        upass = getpass('Contrasenia: ')
        xmpp = my_client(jid= uname, password = upass)

        xmpp.add_event_handler('session_start', my_session)

        xmpp.connect()
        xmpp.process(forever=False)
        
    elif choice == '2':
        print('\n--------Registremos un nuevo usuario--------')
        uname = input('Nombre  de usuario: ')
        upass = getpass('Contrasenia: ')

        xmpp = register_to_server(jid=uname, password=upass)
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0004')  # Data forms
        xmpp.register_plugin('xep_0066')  # Out-of-band Data
        xmpp.register_plugin('xep_0077')  # In-band Registration
        xmpp.register_plugin('xep_0045')  # Groupchat
        xmpp.register_plugin('xep_0199')  # XMPP Ping
        xmpp['xep_0077'].force_registration = True

        xmpp.connect()
        xmpp.process(forever=False)
    elif choice == '3':
        still_running = False
        quit()
    else:
        print('Opcion no valida')