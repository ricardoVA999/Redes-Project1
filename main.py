from logging import log
from os import close
from re import U, X
from ssl import OP_NO_RENEGOTIATION
from slixmpp import roster
from slixmpp.xmlstream.asyncio import asyncio

from client import register_to_server, my_client
from getpass import getpass


still_running = True

def logginMenu():
    print('''--------Menu de Inicio--------
    1. Iniciar Sesion
    2. Registrar nueva cuenta
    3. Salir''')

def groupMenu():
    print('''--------Menu de Grupos--------
    1. Crear Grupo
    2. Unirse a Grupo
    3. Mandar mensaje a grupo
    4. Salir de grupo
    5. Cancelar''')

def mainMenu():
    print('''
    1. Ver mi roster
    2. Agregar usuario a contactos
    3. Mostrar detalles de un contacto
    4. Mandar mensaje privado
    5. Madar mensaje general
    6. Definir mensaje de presencia
    7. Enviar/recibir archivos
    8. Cerrar Sesion
    9. Eliminiar cuenta
    ''')

def my_session(event):
    is_in_session = True
    xmpp.start()
    print("Bienvenido:", xmpp.boundjid.bare)
    while is_in_session:
        mainMenu()
        option = input("Ingrese su accion:")
        if option == "1":
            print('----------------------------------')
            xmpp.get_my_roster()
            print('----------------------------------')

        elif option == '2':
            print('--------Registremos un nuevo contacto a tu lista--------')
            contact_jid = input('Ingrese el JID del usuario que desea agregar:')
            if '@' in contact_jid:
                xmpp.add_friend(contact_jid)
                print("Amigo añadido correctamente!")
            else:
                print('El dato ingresado no es compatible')
            print('----------------------------------')
        
        elif option == '3':
            uname = input('Ingrese el nombre de usuario que desea buscar:')
            if '@' in uname:
                data = xmpp.get_user_info(uname)
                print(data)
            else:
                print('El dato ingresado no es compatible')

        elif option == '4':
            print('--------Enviando mensaje--------')
            roster = xmpp.friends
            users = list(roster.keys())
            print('Usuarios a mandar mensaje:')
            for user in users:
                print(user)
            uname = input('Ingrese el JID del usuario a mandar mensaje:')
            if '@' in uname:
                received_messages = roster[uname].messages
                if received_messages:
                    print('Los mensajes con: '+uname+' son: ')
                    for msg in received_messages:
                        print("-"+msg)
                
                to_send = input("Mensaje a enviar:")
                xmpp.send_private_message(uname, to_send)
            else:
                print('El dato ingresado no es compatible')
            print('----------------------------------')
        elif option == '5':
            groupMenu()
            groupOpt = input("Ingrese su opcion: ")
            if groupOpt == '1':
                print('--------Creando nuevo grupo--------')
                name = input('Group URL: ')
                nick = input('Nickname: ')
                if nick and name:
                    xmpp.create_room(name, nick)
                    print("Grupo Creado!")
                else:
                    ("Ingrese valores correctos")
                    continue
            elif groupOpt == '2':
                print('--------Unirse a grupo--------')
                name = input('Room URL: ')
                nick = input('Nick: ')
                if nick and name:
                    xmpp.join_room(name, nick)
                    print("Unido correctamente")
                else:
                    print("Datos ingresados incorrectamente")
                    continue
            else:
                print('Opcion no valida')
        elif option == '8':
            print("Cerrando Sesion...")
            xmpp.disconnect()
            is_in_session = False
        elif option == '9':
            print('Eliminando cuenta...')
            xmpp.delete()
            xmpp.disconnect()
            is_in_session = False
        else:
            print("Esa opcion no esta disponible.")






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
        xmpp.process()
        
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