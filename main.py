from file_transfer import File_Upload
from client import register_to_server, my_client
from get_my_roster import GetRoster
from private_msg import PrivMsg
from muc import *
from getpass import getpass
import time

# Ricardo Antonio Valenzuela Avila 18762
# Redes
# Main para el manejo de un cliente utilizando el protocolo xmpp


show_options = ['chat', 'away', 'xa', 'dnd']
still_running = True

# Definicion de menus
def logginMenu():
    print('''--------Menu de Inicio--------
    1. Iniciar Sesion
    2. Registrar nueva cuenta
    3. Salir''')

def groupMenu():
    print('''--------Menu de Grupos--------
    1. Crear Grupo
    2. Unirse a grupo
    3. Mandar mensaje a grupo
    4. Salir del grupo
    5. Cancelar''')

def mainMenu():
    print('''
    1. Ver mi roster
    2. Agregar usuario a contactos
    3. Mostrar detalles de un contacto
    4. Mandar mensaje privado
    5. Madar mensaje general
    6. Definir mensaje de presencia
    7. Enviar archivos
    8. Cerrar Sesion
    9. Eliminiar cuenta
    ''')

# Funcion que controla todas funcionalidades del programa
def my_session(event):
    is_in_session = True
    my_client_session.start()
    print('Bienvenido:', my_client_session.boundjid.bare)
    while is_in_session:
        mainMenu()
        option = input('Ingrese su accion:')

        #Obtencion de Roster
        if option == '1':
            print('----------------------------------')
            get_my_roster = GetRoster(my_client_session.jid, my_client_session.password)
            get_my_roster.connect()
            get_my_roster.process(forever=False)
            print('----------------------------------')

        #Agregar nuevo contacto
        elif option == '2':
            print('--------Registremos un nuevo contacto a tu lista--------')
            contact_jid = input('Ingrese el JID del usuario que desea agregar:')
            if '@' in contact_jid:
                my_client_session.add_friend(contact_jid)
                print('Amigo añadido correctamente!')
            else:
                print('El dato ingresado no es compatible')
            print('----------------------------------')
        
        #Obtener informacion de usuario en especifico
        elif option == '3':
            uname = input('Ingrese el nombre de usuario que desea buscar:')
            if '@' in uname:
                get_my_roster = GetRoster(my_client_session.jid, my_client_session.password,uname)
                get_my_roster.connect()
                get_my_roster.process(forever=False)
            else:
                print('El dato ingresado no es compatible')

        #Envio de mensaje 1 a 1
        elif option == '4':
            print('--------Enviando mensaje--------')
            uname = input('Ingrese el JID del usuario a mandar mensaje:')
            if '@' in uname:
                to_send = input('Mensaje a enviar:')
                if to_send:
                    my_priv = PrivMsg(my_client_session.jid, my_client_session.password, uname, to_send)
                    my_priv.connect()
                    my_priv.process(forever=False)
                else:
                    print('No se encontro mensaje a mandar')
            else:
                print('El dato ingresado no es compatible')
            print('----------------------------------')


        #Manejo de rooms
        elif option == '5':
            groupMenu()
            groupOpt = input('Ingrese su opcion: ')

            #Crear nuevo Room
            if groupOpt == '1':
                print('--------Creando nuevo grupo--------')
                name = input('Group URL: ')
                nick = input('Nickname: ')
                if nick and name and '@conference.' in name:
                    group_create = create_group(my_client_session.jid, my_client_session.password, name, nick)
                    group_create.connect()
                    group_create.process(forever=False)
                else:
                    ('Ingrese valores correctos')
                    continue
            
            #Unirse a Room
            elif groupOpt == '2':
                print('--------Unirse a grupo--------')
                name = input('Room URL: ')
                nick = input('Nick: ')
                if nick and name and '@conference.' in name:
                    group_join = join_group(my_client_session.jid, my_client_session.password, name, nick)
                    group_join.connect()
                    group_join.process(forever=False)
                else:
                    print('Datos ingresados incorrectamente')
                    continue
            
            #Mandar mensaje a Room
            elif groupOpt == '3':
                print('--------Mandar mensaje a grupo--------')
                name = input('Room URL: ')
                msg = input('Mensaje: ')
                if msg and name and '@conference.' in name:
                    group_send = sendmsg_group(my_client_session.jid, my_client_session.password, name, msg)
                    group_send.connect()
                    group_send.process(forever=False)
                else:
                    print('Datos ingresados incorrectamente')
                    continue
            
            #Salir de Room
            elif groupOpt == '4':
                print('--------Salir del grupo--------')
                name = input('Room URL: ')
                nick = input('Nick: ')
                if nick and name and '@conference.' in name:
                    group_exit = leave_group(my_client_session.jid, my_client_session.password, name, nick)
                    group_exit.connect()
                    group_exit.process(forever=False)
                else:
                    print('Datos ingresados incorrectamente')
                    continue
            elif groupOpt == '5':
                print('Regresando a menu principal...')
            else:
                print('Opcion no valida')
        
        #Nuevo mensaje de presencia
        elif option == '6':
            print('--------Settemos un nuevo mensaje de presencia--------')
            print('Elija una de las siguientes:')
            i = 1
            for opt in show_options:
                print(str(i)+'. '+opt)
                i += 1
            show_input = input('Option para show: ')
            status = input('Su nuevo status: ')
            try:
                show = show_options[int(show_input)-1]
            except:
                print('Opcion ingresada invalida setteando defoult -available-')
                show = 'available'
            my_client_session.set_presence(show, status)
            print('Seteado correctamente')
        
        #Envio de files
        elif option == '7':
            print('--------Mandar o recivir un file--------')
            uname = input('Ingrese a quien va dirigido el file: ')
            file = input('Ingrese el file name que desea mandar: ')
            if file and uname and '@' in uname:
                send_file = File_Upload(my_client_session.jid, my_client_session.password, uname, file, my_client_session.boundjid.domain)
                send_file.connect()
                send_file.process(forever=False)
            
        #Salir de sesion
        elif option == '8':
            print('Cerrando Sesion...')
            my_client_session.disconnect()
            is_in_session = False
        
        #Eliminar cuenta del server
        elif option == '9':
            print('Eliminando cuenta...')
            my_client_session.delete()
            time.sleep(3)
            my_client_session.disconnect()
            is_in_session = False
        else:
            print('Esa opcion no esta disponible.')


#-------------------- Main -----------------------

while(still_running):
    logginMenu()
    choice = input('Ingrese su accion: ')
    #Inicio de sesion
    if choice == '1':
        print('\n--------Iniciemos Sesion--------')
        uname = input('Nombre  de usuario: ')
        upass = getpass('Contrasenia: ')
        my_client_session = my_client(jid= uname, password = upass)

        my_client_session.add_event_handler('session_start', my_session)

        my_client_session.connect()
        my_client_session.process(forever=False)
        
    #Registro de nueva cuenta
    elif choice == '2':
        print('\n--------Registremos un nuevo usuario--------')
        uname = input('Nombre  de usuario: ')
        upass = getpass('Contrasenia: ')

        xmpp = register_to_server(jid=uname, password=upass)

        xmpp.connect()
        xmpp.process(forever=False)
    
    #Salir
    elif choice == '3':
        still_running = False
        quit()
    else:
        print('Opcion no valida')