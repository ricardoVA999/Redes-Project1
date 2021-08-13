# Redes-Project1
## Ricado Antonio Valenzuela Avila 18762
### Cliente XMPP con las siguientes funcionalidades
#### Manejo de cuenta
- Creacion de cuenta
- Inicio de sesion
- Salir de sesion
- Eliminar cuenta
#### Manejo de mensajes y actividades dentro del server
- Ver lista de contactos
- Agregar usuario a contactos
- Ver informacion de un contacto en especifico
- Mandar mensaje 1 a 1
- Mandar mensaje grupal
- Definir mensajes de presencia
- Envio de archivos
El cliente tambien esa capaz de recibir mensajes de presencia y desplegar mensajes recibidos individuales y grupales.

### -----------------------------------------------------------------------------------------------------------------------
Uso de las diferentes funcionalidades:
#### Creacion de cuenta: crea nueva cuenta en el server determinado
- Usuario: usuario de la forma 'nombre@example.com' en donde 'example.com' es el dominio del servidor xmpp a utilizar.
- Contraseña: contraseña a utilizar en su cuenta, No la olvide!
#### Inicio de sesion: hace el inicio de sesion en el server determinado
- Usuario: usuario de la forma 'nombre@example.com' en donde 'example.com' es el dominio del servidor xmpp a utilizar.
- Contraseña: contraseña a utilizar en su cuenta, No la olvide!
#### Salir de session: sale de la sesion del server determinado.
#### Eliminar cuenta: elimina y sale de la sesion del server determinado.
#### Ver lista de contactos: obtiene la lista de todos los contactos que se han suscrito a ti.
#### Agregar usuario a contactos: agrega el usuario especificado a tu lista de contactos
- Usuario a agregar: usuario de la forma 'nombre@example.com' en donde 'example.com' es el dominio del servidor xmpp a utilizar.
#### Ver info de contacto: devuelve la info del usuario especificado
- Usuario a agregar: usuario de la forma 'nombre@example.com' en donde 'example.com' es el dominio del servidor xmpp a utilizar.
#### Mensaje 1 a 1: opcion para mandar mensajes 1 a 1 con el usuario especficicado.
- Usuario a agregar: usuario de la forma 'nombre@example.com' en donde 'example.com' es el dominio del servidor xmpp a utilizar.
- Mensaje a mandar: mensaje a mandar a la persona.
#### Mensaje grupal: creacion de grupo, unirse a grupo, mandar mensaje, salir de grupo.
- Grupo a utilizar: nombre del grupo de la forma 'nombre@conference.example.com' en donde 'example.com' es el dominio del servidor xmpp a utilizar.
- Mensaje a mandar: mensaje a enviar al grupo.
- Alias: alias que se tendra dentro del grupo.
#### Definir mensaje de presencia: cambia el mensaje de presencia del usuario
- Show: forma del mensaje de presencia
- Mensaje: nuevo mensaje de presencia
#### Envio de files (Not quite done)
- Path del file: path del file a mandar
- Usuario: usuario de la forma 'nombre@example.com' en donde 'example.com' es el dominio del servidor xmpp a utilizar, aquien va dirigido el file.
