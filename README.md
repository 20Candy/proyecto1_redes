# Proyecto 1 - Redes - UVG
Implementación de un cliente de mensajería instantánea que soporte el protocolo
XMPP


## Instalacion 🔧

1. Clona este repositorio:  ```git remote add origin https://github.com/20Candy/proyecto1_redes ```
2. Accede al directorio del proyecto: ```cd nombre_del_directorio```
3. Instala las dependencias usando ```pip install -r requirements.txt```


## Correr el programa 🚀

```shell
  python main.py
```

## Construido con 🛠️
- Python

## Características 📋

Este cliente posee las siguientes implementaciones:

- [X] Registrarse con una cuenta nueva.
- [X]  Iniciar sesión con una cuenta existente.
- [X] Cerrar sesión de una cuenta existente.
- [x]  Eliminar una cuenta del servidor.
- [X]  Mostrar información y estado de los contactos.
- [X] Mostrar información de un contacto específico.
- [X] Agregar un nuevo contacto.
- [X] Mensajes de uno a uno.
- [X] Salas de chat.
  - [X] Ver salas de chat disponibles.
  - [X] Unirse a una sala de chat existente.
  - [X] Crear una nueva sala de chat.
- [X] Crear mensaje de presencia.
- [X] Enviar/Recibir notificaciones.
- [X] Enviar/Recibir archivos.


## Dificultades 📋

Considero que la parte más complicada de este proyecto fue el envío de archivos. El último método implementado fue utilizar Base64, el cual resultó menos difícil que otros métodos probados. Asimismo, la asincronicidad resultó un poco difícil al principio, pero luego de comprender su funcionamiento, fue más sencillo de implementar para el resto de las funcionalidades.


## Lecciones Aprendidas 📋

Dentro de las lecciones aprendidas en este proyecto se encuentran:
- El uso de un protocolo existente, como es XMPP.
- La comprensión y aplicación de la programación asincrónica, requerida para el funcionamiento del cliente.
- La importancia de leer la documentación previo a iniciar el desarrollo. 

## Video 🎥
https://youtu.be/NuZOVoRBlpQ

## Autores ✒️

* **Carol Arevalo** - *desarrollo* - [#20Candy](https://github.com/20Candy)


