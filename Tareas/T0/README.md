# Tarea 0: DCCommerce :school_satchel:


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

La tarea hace todo lo pedido.

No se encarga de crear los archivos comentarios.csv, publicaciones.csv, usuarios.csv

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Requisitos: Hecha completa
* Iniciar sesión: Hecha completa
* Ingresar como usuario anónimo: Hecha completa
* Registrar usuario: Hecha completa
* Salir: Hecha completa
* Menú principal: Hecha completa
* Menú publicaciones: Hecha completa
* Menú publicaciones realizadas: Hecha completa
* Usuarios: Hecha completa
* Publicaciones: Hecha completa
* Comentarios: Hecha completa
* Manejo de archivos: Hecha completa
* General: Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
- No se debe crear ningun archivo fuera de lo que se descarga en el repositorio (comentarios.csv, parámetros.csv, publicaciones.csv)

## Librerías :books:

### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```datetime```: ```datetime.now()```

### Librerías propias

Ninguna

## Supuestos y consideraciones adicionales :thinking:

Los supuestos que realicé durante la tarea son los siguientes:

1. No es necesario ordenar las publicaciones y comentarios al leerlas del archivo, ya que al añadirse al csv, quedan ordenadas

2. No es necesario revisar que los archivos existas y estén con un formato correcto, ya que por algo nos los dan listos en el repo

3. No es necesario hacer login al usuario al registrarse ya que, en un caso real, el usuario tendria que completar los pasos de verificación primero (Solo sería necesario agregar:

   ```
   cache.user = username
   cache.curMenu = MenuMainMenu()
   ```

   En la linea 85-main.py)


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

Ninguna



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).