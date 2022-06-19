# Tarea 3: DCCalamar :school_satchel:


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Networking: 23 pts (18%)
##### ✅ Protocolo: Toda la comunicación TCP/IP en este programa está basada en "comandos" entre el servidor y el cliente. Estos comandos van separados de \n ya que es un caracter que en ninguna parte envío.
##### ✅ Correcto uso de sockets: Los sockets son abiertos y cerrados cuando es necesario
##### ✅ Conexión: La coneción se mantiene abierta mientras se está usando.
##### ✅Manejo de clientes: Todos los clientes dentro del servidor estan almacenados en objetos tipo Client() en donde almacenan todos los datos del cliente (Socket y otros)
#### Arquitectura Cliente - Servidor: 31 pts (24%)
##### ✅Roles: Todo lo que tiene que ser validado, es enviado al servidor, el cual entrega una respuesta acorde a lo requerido. También todo que el servidor procesa (cantidad de canicas y otros) es replicado a ambos clientes dentro de la partida. Toda la información importante para el juego es almacenada por el servidor
##### ✅Consistencia: Todo mantiene una separación funcional, y es posible acceder a todas las interfaces de manera consistente
##### ✅ Logs: Todos los logs pedidos (y extras) están implementados
#### Manejo de Bytes: 20 pts (15%)
##### ✅Codificación: La codificación es realizada en utils/comms.py para el cliente y el servidor en sus respectivas carpetas
##### ✅ Decodificación: La decodificación es realizada en utils/comms.py para el cliente y el servidor en sus respectivas carpetas
##### ✅Encriptación:  La Encriptación es realizada en utils/comms.py para el cliente y el servidor en sus respectivas carpetas
##### ✅Integración: La codificación, decodificación y la encriptación, son manejadas en utils/comms.py para poder integrarlas en un solo lugar.
#### Interfaz gráfica: 31 pts (24%)
##### ✅ Modelación: El modelo está basado en las imagenes mostradas en el pdf del proyecto, pero no tienen un theme o stylesheeet
##### ✅ Ventana inicio: Tiene QLineEdits para el nombre de usuario y la fecha de nacimiento aparte de un QPushButton para entrar a la sala principal
##### ✅ Sala Principal: Se muestran los jugadores conectados junto a sus respectivos botones para retarlos a una partida (Solo si no ha sido ya invitado sin responder)
##### ✅ Ventana de Invitación: Se muestran los botones para aceptar o rechazar la partida
##### ✅Sala de juego: Se muestran todos los elementos pedidos
##### ✅Ventana final: Se muestra al ganador y al perdedor de la partida junto a un boton para volver al inicio y poder jugar de nuevo
#### Reglas de DCCalamar: 21 pts (16%)
##### ✅ Inicio del juego: Se inicia el juego y se inician todos los valores (Canicas, etc)
##### ✅Ronda: Se juega por turnos y al finalizar la ronda, se muestra al perdedor si hay uno, o un texto de empate. Y se actualizan las canicas para cada jugador
##### ✅ Termino del juego: Se muestra el ganador de la partida y se les permite a los jugadores volver al menu por si quieren volver a jugar
#### General: 4 pts (3%)
##### ✅ Parámetros (JSON): De los parametros, se leen 'host' y 'port' y si estos no son validos, o no existen, se usan ip y puerto por defecto
#### Bonus: 5 décimas máximo
##### ✅ Cheatcode: Ambos cheatcodes funcionan. El F-A necesita que el jugador sea el 2, ya que por los turnos, es el unico que puede saber lo que hace el jugador 1. Para ambos, es necesario no tener seleccionado el SpinBox, (Mas info en los supuestos 7, 8 y 9)
##### ✅ Turnos con tiempo: Dentro del ```parametros.json``` del servidor, está la configuración ```TIEMPO_TURNO``` el cual es el tiempo maximo por turno, si se pone en 0, se desactiva el limite de tiempo y las barras dentro del GUI de los jugadores se usa para indicar el turno
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. para el cliente y servidor en sus respectivas carpetas
1. ```parametros.json``` debe estár en ```cliente\```
2. ```parametros.json``` debe estár en ```servidor\```
2. Todos los archivos .ui deben estar en  ```cliente\*\``` (Al menos a una carpeta de distancia a cliente para que los paths definidos en los .ui no creen problemas) y esa carpeta debe estar especificada en parametros.json
2. Todos los sprites en sus respectivas carpetas dentro de ```cliente\Sprites\```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```pyqt5```
2. ```socket```
3. ```time```: ```sleep()```
4. ```threading```: ```Thread()```, ```Event()```
5. ```sys```: ```__excepthook__```, ```argv```
5. ```json```: ```load()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```cliente/utils/comms.py```: Contiene ```ClientServerConnection``` el cual se encarga de guardar el socket y de la comunicación cliente-servidor.
2. ```servidor/utils/comms.py```: Contiene ```ClientConnection``` el cual se encarga de almacenar la data de la coneción por cada cliente
3. ```servidor/utils/client.py```: Contiene ```Client``` el cual es una instancia que se encarga de almacenar todo lo que tiene que ver con el cliente, desde la partida a la que está conectado, hasta la connection ````ClientConnection```
3. ````servidor/utils/checks.py````: Contiene los checkeos que se hacen al username y a la fecha de nacimiento
3. ````servidor/utils/game.py````: Contiene a la clase ````Game```` que guarda la información de la partida de 2 jugadores y se encarga de hacer parse a los comandos enviados que tengan relación al juego en progreso
3. ```server/utils/server.py``` Contiene ````Server```` el cual se encarga de recibir los mensajes de los jugadores en un thread separado al principal que se encarga de aceptar nuevas conexiones.
3. ````server/utils/server_utils.py```` Tiene a la clase ```Timer``` la cual se usa para los juegos con tiempo limite. Permite ejecutar una función después de una cantidad de tiempo definida.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Cuando en el pdf dice ```los usuarios participarán por turnos hasta que sólo quede un único jugador``` Me imagino que esto se refiere a que un usuario juega y recién ahí el oponente puede elegir su movida

2. Para las apuestas, la cantidad que se gana/pierde es la cantidad de apostó el jugador perdedor (Nunca he apostado y tampoco aparece en el pdf, por lo que fue lo unico que se me ocurrió), de todas formas, el programa es suficientemente modular como para necesitar solo cambiar un par de lineas en server.py para cambiar este comportamiento.

3. Si el archivo parametros.json no existe o no es valido, el programa imprime en la consola y termina, ya que no se especifica qué hacer en ese caso.

4. Si el archivo parametros.json no tiene las variables 'host' o 'port' el programa imprime en la consola y usa ```socket.gethostname()```:```9000``` por defecto, ya que no se especifica qué hacer en este caso

5. Parto de la suposición de que ```except socket.error as e``` no es "ambiguo" y solo cuando se usa dentro del programa, en la mayoria de los usos, se separa el error ```e.errno``` para separar el tipo de error y se hace ```raise e``` si no está considerado. En algunos lugares, se manejan todos los errores tipo ```socket.error``` pero solo si el programa puede continuar funcionando sin anomalías luego del bloque ```try```.

6. Aunque se verifica que estén definidos los paths en ```parametros.json``` y se usa un camino por defecto si no se encuentran, el programa **no** verifica si existen los paths hasta ser necesitados ya que aunque la librería os está permitida, no sé si se pueda decir lo mismo para la función ```os.path.isfile()``` u ```os.path.exists()```. Tampoco se verifica que los caminos a las imagenes dentro de los archivos .ui sigan apuntandó al mismo camino (es relativo)

7. Para el bonus de cheatcodes, no se puede hacer la combinación de cheatcodes mientras se tenga el textbox seleccionado. Esto se podría tratar de arreglar, pero tiene el positivo de que no puedes ejecutarlo mientras tratas de escribir

8. Para el bonus de cheatcodes el orden que se presionan las teclas **si** importa, ya que esto es tipico para las combinaciones de letras (Ej. Ctrl + c)

9. El cheatcode F+A solo puede ser utilizado por el jugador n2 ya que después de que este juega, empieza la siguiente ronda y por tanto el jugador n1 no ha hecho una apuesta

10. Como la mayoría de los directorios que no quiero subir a github, están en el .gitignore en el root del repositorio, y ```venv/``` tiene su propio .gitignore por defecto, solo puse algunos archivos que no quería subir, ya que en la entrega anterior me bajaron nota por no subir un gitignore en la tarea (Aunque en ese momento no había subido el gitignore al repo)

11. Para el bonus de tiempo, el parametro ```TIEMPO_TURNO``` está en segundos ya que no se especificó y si fuese milisegundos, por problemas de ping, el cliente no va a tener tanta presición y si fuese minutos, el administrador del servidor, no tendría muchas opciónes de configuración

12. Para el bonus de tiempo, me imagino que no es necesario que esté perfectamente syncronizado el cliente con el servidor, ya que los delays generados por la conexión, generan que tengan un desface (No es muy notorio a menos que el ```TIEMPO_TURNO``` sea pequeño o que el ping entre el servidor y el cliente sea muy alto)

    


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:





## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
