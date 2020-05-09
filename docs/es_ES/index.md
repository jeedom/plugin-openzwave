Description
===========

Este complemento permite la explotación de módulos Z-Wave a través de
la biblioteca OpenZwave.

Introduction
============

Z-Wave se comunica utilizando tecnología de radio de baja potencia en la banda de frecuencia de 868.42 MHz. Está específicamente diseñado para aplicaciones de domótica. El protocolo de radio Z-Wave está optimizado para intercambios de bajo ancho de banda (entre 9 y 40 kbit / s) entre dispositivos con batería o alimentados por la red eléctrica.

Z-Wave opera en el rango de frecuencia de sub gigahercios, dependiendo de
regiones (868 MHz en Europa, 908 MHz en los EE. UU. y otras frecuencias
según las bandas ISM de las regiones). El rango teórico es aproximadamente
30 metros en interiores y 100 metros en exteriores. La red Z-Wave
utiliza tecnología de malla para aumentar el alcance y
fiabilidad Z-Wave está diseñado para integrarse fácilmente en
productos electrónicos de bajo consumo, incluidos
baterías como controles remotos, detectores de humo y
Seguridad.

El Z-Wave +, trae ciertas mejoras que incluyen un mejor rango y
mejora la duración de la batería, entre otras cosas. El
Compatibilidad total con la Z-Wave.

Distancias a respetar con otras fuentes de señal inalámbrica
-----------------------------------------------------------------

Los receptores de radio deben colocarse a una distancia mínima de
50 cm de otras fuentes de radio.

Ejemplos de fuentes de radio.:

-   Ordinateurs

-   Aparatos de microondas

-   Transformadores electrónicos

-   equipo de audio y video

-   Dispositivos de preenganche para lámparas fluorescentes

> **Tip**
>
> Si tiene un controlador USB (Z-Stick), se recomienda
> quítelo de la caja usando un simple cable de extensión USB de 1M por
> Ejemplo.

La distancia entre otros transmisores inalámbricos como teléfonos
Las transmisiones de audio inalámbricas o de radio deben ser de al menos 3 metros. El
Se deben considerar las siguientes fuentes de radio :

-   Interferencia por interruptor de motores eléctricos.
-   Interferencia de dispositivos eléctricos defectuosos.
-   Interferencia de equipos de soldadura HF
-   dispositivos de tratamiento médico

Espesor de pared efectivo
---------------------------

Las ubicaciones de los módulos deben elegirse de tal manera que
la línea de conexión directa solo funciona en un tiempo muy corto
distancia a través del material (una pared), para evitar tanto como sea posible
mitigaciones.

![introduction01](../ /images/ /introduction01.png)

Las partes metálicas del edificio o los muebles pueden bloquear
ondas electromagneticas.

Malla y Enrutamiento
-------------------

Los nodos principales de Z-Wave pueden transmitir y repetir mensajes
que no están dentro del alcance directo del controlador. Esto permite un más
Gran flexibilidad de comunicación, incluso si no hay conexión.
inalámbrico directo o si una conexión no está disponible temporalmente, para
debido a un cambio en la habitación o el edificio.

![introduction02](../ /images/ /introduction02.png)

El controlador **Id 1** puede comunicarse directamente con los nodos 2, 3
y 4. Nodo 6 está fuera de su alcance de radio, sin embargo, es
encontrado en el área de cobertura de radio del nodo 2. Por lo tanto, el
el controlador puede comunicarse con el nodo 6 a través del nodo 2. De esta
manera, la ruta desde el controlador a través del nodo 2 al nodo 6, se llama
camino En el caso donde la comunicación directa entre el nodo 1 y el
el nodo 2 está bloqueado, hay otra opción para comunicarse con
nodo 6, usando el nodo 3 como otro repetidor de señal.

Es obvio que cuantos más nodos de sector tenga, más
las opciones de enrutamiento aumentan y aumenta la estabilidad de la red.
El protocolo Z-Wave es capaz de enrutar mensajes por
a través de un máximo de cuatro nodos repetidos. Es un
compensación entre tamaño de red, estabilidad y duración máxima
de un mensaje.

> **Tip**
>
> Se recomienda encarecidamente al inicio de la instalación tener una relación
> entre nodos sectoriales y nodo con 2/3 baterías, para tener una buena
> malla de red. Favorezca los micromódulos sobre los enchufes inteligentes. El
> los micro módulos estarán en una ubicación final y no serán
> desconectados, generalmente también tienen un mejor alcance. Un bueno
> la salida es la iluminación de las áreas comunes. Va a ayudar bien
> distribuya los módulos del sector en ubicaciones estratégicas en su
> casa. Luego puede agregar tantos módulos en la pila
> si lo desea, si sus rutas básicas son buenas.

> **Tip**
>
> El **Gráfico de red** así como el **Tabla de enrutamiento**
> le permite ver la calidad de su red.

> **Tip**
>
> Hay módulos repetidores para llenar áreas donde no hay módulo
> sector no tiene uso.

Propiedades de los dispositivos Z-Wave
-------------------------------

|  | Vecinos | Camino | Posibles funciones |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controlador | Conoce a todos los vecinos | Tiene acceso a la tabla de enrutamiento completa | Puede comunicarse con todos los dispositivos en la red, si existe un canal |
| Esclavo | Conoce a todos los vecinos | No tiene información sobre la tabla de enrutamiento | No se puede responder al nodo que recibió el mensaje.. Por lo tanto, no se pueden enviar mensajes no solicitados. |
| Esclavos enrutamiento | Conoce a todos sus vecinos | Con conocimiento parcial de la tabla de enrutamiento. | Puede responder al nodo desde el que recibió el mensaje y puede enviar mensajes no solicitados a varios nodos |

En resumen:

-   Cada dispositivo Z-Wave puede recibir y acusar recibo de
    messages

-   Los controladores pueden enviar mensajes a todos los nodos en el
    réseau, sollicités o non « El maître peut parler quand il veut y à
    a quien quiere »

-   Los esclavos no pueden enviar mensajes no solicitados,
    mais seulement une réponse aux demandesde «L'esclave ne parle que si
    le preguntamos »

-   Los esclavos enrutados pueden responder a las solicitudes y son
    permitido enviar mensajes no solicitados a ciertos nodos que
    le Controlador a prédéfini « L'esclave es toujours un esclave, mais
    con autorización, él puede hablar »

Configuración del plugin
=======================

Después de descargar el complemento, solo necesita activarlo y
configurer.

![Configuración01](../ /images/ /configuration01.png)

Una vez activado, el demonio debería lanzar. El complemento está preconfigurado
con valores predeterminados; normalmente no tienes nada más que hacer.
Sin embargo, puedes cambiar la configuración.

Dependencias
-----------

Esta parte le permite validar e instalar las dependencias requeridas
El correcto funcionamiento del complemento Zwave (tanto local como
deportado, aquí localmente) ![configuración02](../ /images/ /configuration02.png)

-   Un estatuto **OK** confirma que se cumplen las dependencias.

-   Si el estado es **NOK**, las dependencias deberán ser reinstaladas
    usando el botón ![configuración03](../ /images/ /configuration03.png)

> **Tip**
>
> La actualización de dependencias puede demorar más de 20 minutos dependiendo de
> tu material. El progreso se muestra en tiempo real y un registro
> **Openzwave\_update** es accesible.

> **Important**
>
> La actualización de dependencias normalmente solo se debe hacer
> Si el estado es **NOK**, pero es posible, sin embargo, ajustar
> ciertos problemas, para ser llamados a rehacer la instalación de
> Dependencias.

> **Tip**
>
> Si está en modo remoto, las dependencias del daemon local pueden
> ser NOK, es completamente normal.

Demonio
-----

Esta parte le permite validar el estado actual de los demonios y
configurar la gestión automática de estos.
![Configuración04](../ /images/ /configuration04.png) El démon local et
todos los demonios deportados se mostrarán con sus diferentes
informations

-   El **Statut** indica que el demonio se está ejecutando actualmente.

-   El **Configuration** indica si la configuración del demonio
    es valido.

-   El botón **(Re)Iniciar** permite forzar el reinicio de la
    plugin, en modo normal o iniciarlo la primera vez.

-   El botón **Detenido**, visible solo si la gestión automática
    está desactivado, obliga al demonio a detenerse.

-   El **Gestión automática** permite que Jeedom se inicie automáticamente
    el demonio cuando se inicia Jeedom, así como reiniciarlo en caso de que
    de problema.

-   El **Última ejecución** es como su nombre indica la fecha de
    último lanzamiento conocido del demonio.

Log
---

Esta parte le permite elegir el nivel de registro, así como consultarlo.
el contenido.

![Configuración05](../ /images/ /configuration05.png)

Seleccione el nivel y luego guarde, el demonio se reiniciará
con instrucciones y huellas seleccionadas.

El nivel **Debug** o **Info** puede ser útil para entender
por qué el demonio planta o no aumenta un valor.

> **Important**
>
> En modo **Debug** el demonio es muy detallado, se recomienda
> use este modo solo si necesita diagnosticar un problema
> particular. No se recomienda dejar que el demonio corra mientras
> **Debug** permanentemente, si usamos un **SD-Card**. Una vez que
> depurar, no te olvides de volver a un nivel inferior
> tan alto como el nivel **Error** que solo vuelve a lo posible
> errores.

Configuration
-------------

Esta parte le permite configurar los parámetros generales del complemento
![Configuración06](../ /images/ /configuration06.png)

-   **Principal** :

    -   **Eliminar automáticamente los dispositivos excluidos** :
        La opción Sí le permite eliminar los dispositivos excluidos del
        Red Z-Wave. La opción No le permite conservar el equipo.
        en Jeedom incluso si han sido excluidos de la red. El equipo
        tendrá que ser eliminado manualmente o reutilizado en él
        asignar una nueva ID de Z-Wave si está migrando el
        controlador principal.

    -   **Aplicar el conjunto de configuración recomendado para su inclusión.** :
        opción de aplicar el conjunto de
        configuración recomendada por el equipo de Jeedom (recomendado)

    -   **Desactivar la actualización en segundo plano de las unidades** :
        No solicite una actualización de las unidades
        en el fondo.

    -   **Ciclo (s)** : permite definir la frecuencia de los ascensores
        en Jeedom.

    -   **Puerto de llave Z-Wave** : el puerto USB en el que su interfaz
        Z-Wave está conectado. Si usa el Razberry, tiene,
        dependiendo de su arquitectura (RPI o Jeedomboard) el 2
        posibilidades al final de la lista.

    -   **Puerto del servidor** (modificación peligrosa, debe tener el mismo
        valor en todos los Jeedoms remotos Z-Wave) : permite
        modificar el puerto de comunicación interna del demonio.

    -   **Backups** : le permite administrar copias de seguridad del archivo
        topología de red (ver más abajo)

    -   **Módulos de configuración** : permite recuperar, manualmente,
        Archivos de configuración de OpenZWave con parámetros para
        módulos, así como definir comandos de módulo para
        sus usos.

        > **Tip**
        >
        > Se recuperan las configuraciones de los módulos.
        > automáticamente todas las noches.

        > **Tip**
        >
        > Reiniciar el demonio después de actualizar el
        > las configuraciones del módulo son innecesarias.

        > **Important**
        >
        > Si tiene un módulo no reconocido y una actualización de
        > la configuración se acaba de aplicar, puede manualmente
        > comenzar a recuperar configuraciones de módulos.

Una vez recuperadas las configuraciones, tomará de acuerdo con los cambios
traído:

-   Para un nuevo módulo sin configuración o control : excluir y
    vuelva a incluir el módulo.

-   Para un módulo para el que solo se han actualizado los parámetros :
    iniciar la regeneración de la detección de nodos, a través de la pestaña Acciones
    del módulo (el complemento debe reiniciarse).

-   Pour un Modulo dont le « mapping » de encargos a été corrigé : la
    lupa en los controles, ver abajo.

    > **Tip**
    >
    > En caso de duda, se recomienda excluir y volver a incluir el módulo..

No te olvides de ![configuración08](../ /images/ /configuration08.png) si
haces un cambio.

> **Important**
>
> Si estás usando Ubuntu : Para que el demonio funcione, debes
> absolutamente tiene ubuntu 15.04 (las versiones inferiores tienen un error y
> el demonio no puede comenzar). Ten cuidado si haces una apuesta
> actualizado desde 14.04 toma una vez en 15.04 relanzamiento
> instalación de dependencias.

> **Important**
>
> Selección del puerto clave Z-Wave en modo de detección automática,
> **Auto**, solo funciona para dongles USB.

Panel móvil
-------------

![Configuración09](../ /images/ /configuration09.png)

Permite mostrar o no el panel móvil cuando usa
la aplicación en un teléfono.

Configuración del equipo
=============================

Se puede acceder a la configuración del equipo Z-Wave desde el menú
Plugin :

![appliance01](../ /images/ /appliance01.png)

A continuación se muestra un ejemplo de una página de complemento de Z-Wave (presentada con
algunos equipos) :

![appliance02](../ /images/ /appliance02.png)

> **Tip**
>
> Como en muchos lugares de Jeedom, coloca el mouse en el extremo izquierdo
> muestra un menú de acceso rápido (puede, en
> desde tu perfil, siempre déjalo visible).

> **Tip**
>
> Los botones en la linea superior **Synchroniser**,
> **Red Zwave** y **Santé**, son visibles solo si estás en
> modo **Expert**. ![aparato03](../ /images/ /appliance03.png)

Principal
-------

Aquí encontrarás toda la configuración de tu equipo :

![appliance04](../ /images/ /appliance04.png)

-   **Nombre del equipo** : nombre de su módulo Z-Wave.

-   **Objeto padre** : indica el objeto padre al que
    pertenece equipo.

-   **Categoría** : categorías de equipos (puede pertenecer a
    categorías múltiples).

-   **Activer** : activa su equipo.

-   **Visible** : lo hace visible en el tablero.

-   **ID de nodo** : ID del módulo en la red Z-Wave. Esto puede ser
    útil si, por ejemplo, desea reemplazar un módulo defectuoso.
    Simplemente incluya el nuevo módulo, obtenga su ID y el
    poner en lugar de la ID del módulo anterior y finalmente eliminar
    el nuevo módulo.

-   **Module** : este campo solo aparece si hay diferentes tipos de
    configuración para su módulo (caso para módulos que pueden hacer
    cables piloto por ejemplo). Te permite elegir el
    configuración para usarlo o modificarlo más tarde

-   **Marque** : fabricante de su módulo Z-Wave.

-   **Configuration** : ventana para configurar los parámetros de la
    module

-   **Assistant** : solo disponible en ciertos módulos, usted
    ayuda a configurar el módulo (caso en el teclado zipato por ejemplo)

-   **Documentation** : Este botón le permite abrir directamente el
    Documentación de Jeedom sobre este módulo.

-   **Supprimer** : Le permite eliminar un elemento del equipo y todos estos
    comandos adjuntos sin excluirlo de la red Z-Wave.

> **Important**
>
> Eliminar un equipo no da como resultado la exclusión del módulo
> en el controlador. ![aparato11](../ /images/ /appliance11.png) Un
> el equipo eliminado que todavía está conectado a su controlador
> recreado automáticamente después de la sincronización.

Commandes
---------

A continuación encontrará la lista de pedidos. :

![appliance05](../ /images/ /appliance05.png)

> **Tip**
>
> Dependiendo de los tipos y subtipos, algunas opciones pueden ser
> ausente.

-   el nombre que se muestra en el tablero
-   Icono : en el caso de una acción le permite elegir un icono para
    mostrar en el tablero en lugar de texto
-   Valor del pedido : en el caso de un comando de tipo acción, su
    el valor se puede vincular a un comando de tipo de información, aquí es donde
    esta configurado. Ejemplo para una lámpara, la intensidad está vinculada a su
    estado, esto permite que el widget tenga el estado real de la lámpara.
-   tipo y subtipo.
-   la instancia de este comando Z-Wave (reservado para expertos).
-   la clase del control Z-Wave (reservado para expertos).
-   el índice de valor (reservado para expertos).
-   el pedido en sí (reservado para expertos).
-   "Valor de retroalimentación de estado "y" Duración antes de la retroalimentación de estado" : permet
    para indicarle a Jeedom que después de un cambio en la información
    el valor debe volver a Y, X min después del cambio. Ejemplo : dans
    el caso de un detector de presencia que emite solo durante un
    detección de presencia, es útil establecer por ejemplo 0
    valor y 4 en duración, de modo que 4 minutos después de una detección de
    movimiento (y si no hubiera nuevos) Jeedom
    restablece el valor de la información a 0 (no se detecta más movimiento).

-   Guardar historial : permite historizar los datos.
-   Mostrar : permite mostrar los datos en el tablero.
-   Invertir : permite invertir el estado para tipos binarios.
-   Unidad : unidad de datos (puede estar vacía).
-   Min / max : límites de datos (pueden estar vacíos).
-   Configuración avanzada (ruedas con muescas pequeñas) : muestra la configuración avanzada del comando (método de registro, widget, etc.).

-   Probar : Se usa para probar el comando.
-   Eliminar (firmar -) : permite eliminar el comando.

> **Important**
>
> El botón **Tester** en el caso de un comando de tipo Información, no
> no consultar el módulo directamente sino el valor disponible en el
> jeedom cache. La prueba devolverá el valor correcto solo si el
> El módulo en cuestión ha transmitido un nuevo valor correspondiente al
> definición del comando. Entonces es completamente normal no
> obtener resultados después de la creación de un nuevo comando de información,
> especialmente en un módulo de batería que rara vez notifica a Jeedom.

El **loupe**, disponible en la pestaña general, le permite recrear
todos los comandos para el módulo actual.
![appliance13](../ /images/ /appliance13.png) Si aucune Comando n'est
presente o si los comandos son incorrectos, la lupa debe remediar
la situación.

> **Important**
>
> El **loupe** borrará los pedidos existentes. Si las órdenes
> fueron utilizados en escenarios, deberá corregir su
> escenarios en otros lugares donde se operaban los controles.

Juegos de comando
-----------------

Algunos módulos tienen varios conjuntos de comandos preconfigurados

![appliance06](../ /images/ /appliance06.png)

Puede seleccionarlos a través de las posibles opciones, si el módulo
permet.

> **Important**
>
> Debe llevar la lupa para aplicar los nuevos conjuntos de
> Comandos.

Documentación y Asistente
--------------------------

Para un cierto número de módulos, ayuda específica para configurar
lugar, así como recomendaciones de parámetros están disponibles.

![appliance07](../ /images/ /appliance07.png)

El botón **Documentation** proporciona acceso a la documentación
módulo específico para Jeedom.

Los módulos especiales también tienen un asistente específico para
para facilitar la aplicación de ciertos parámetros u operaciones.

El botón **Assistant** permite el acceso a la pantalla de asistente específica
del módulo.

Configuración recomendada
-------------------------

![appliance08](../ /images/ /appliance08.png)

Le permite aplicar un conjunto de configuración recomendado por el equipo
Jeedom.

> **Tip**
>
> Cuando se incluyen, los módulos tienen la configuración predeterminada de
> fabricante y algunas funciones no están activadas por defecto.

Lo siguiente, según corresponda, se aplicará para simplificar
usando el módulo.

-   **Configuraciones** permitiendo una rápida puesta en marcha de la asamblea
    funcionalidad del módulo.

-   **Grupos de asociaciones** requerido para una operación adecuada.

-   **Intervalo de despertador**, para módulos con batería.

-   Activación de **actualización manual** para módulos hacer
    no volviendo por sí mismos sus cambios de estado.

Para aplicar el conjunto de configuración recomendado, haga clic en el botón
: **Configuración recomendada**, luego confirme la aplicación de
configuraciones recomendadas.

![appliance09](../ /images/ /appliance09.png)

El asistente activa los diversos elementos de configuración..

Se mostrará una confirmación del buen progreso en forma de banner.

![appliance10](../ /images/ /appliance10.png)

> **Important**
>
> Los módulos de batería se deben activar para aplicar el conjunto de
> Configuración.

La página del equipo le informa si los artículos aún no han sido
sido activado en el módulo. Consulte la documentación de la
módulo para activarlo manualmente o esperar el próximo ciclo de
despertar.

![aparato11](../ /images/ /appliance11.png)

> **Tip**
>
> Es posible activar automáticamente la aplicación del juego.
> configuración recomendada cuando se incluye un nuevo módulo, ver
> la sección de configuración del complemento para más detalles.

Configuracion de modulos
=========================

Aquí es donde encontrará toda la información sobre su módulo.

![node01](../ /images/ /node01.png)

La ventana tiene varias pestañas. :

Resumen
------

Proporciona un resumen completo de su nodo con información variada
en este caso, por ejemplo, el estado de las solicitudes que permite conocer
si el nodo está esperando información o la lista de nodos vecinos.

> **Tip**
>
> En esta pestaña es posible tener alertas en caso de detección
> posible por un problema de configuración, Jeedom indicará la marcha
> seguir para corregir. No confunda una alerta con un
> error, la alerta es en la mayoría de los casos un simple
> recomendación.

Valeurs
-------

![node02](../ /images/ /node02.png)

Aquí encontrará todos los comandos y estados posibles en su
módulo Se ordenan por instancia y clase de comando y luego indexan.
El « mapping » desde Comandos es entièrement basé sur ces Información.

> **Tip**
>
> Forzar actualización de un valor. Los módulos de batería
> actualizar un valor solo en el siguiente ciclo de activación. El es
> sin embargo, es posible reactivar manualmente un módulo, consulte el
> Documentación del módulo.

> **Tip**
>
> Es posible tener más pedidos aquí que en Jeedom, es
> completamente normal. En Jeedom las órdenes han sido preseleccionadas
> para usted.

> **Important**
>
> Algunos módulos no envían automáticamente sus estados, es necesario
> en este caso active la actualización manual a los 5 minutos en el
> valores deseados. Se recomienda dejar automáticamente el
> Refrescante. El abuso del refresco manual puede afectar
> fuertemente el rendimiento de la red Z-Wave, use solo para
> los valores recomendados en la documentación específica de Jeedom.
> ![nodo16](../ /images/ /node16.png) El conjunto de valores (índice) de
> la instancia de un comando de clase se volverá a montar, activando el
> actualización manual en el índice más pequeño de la instancia de la
> comando de clase. Repita para cada instancia si es necesario.

Configuraciones
----------

![node03](../ /images/ /node03.png)

Aquí encontrará todas las posibilidades de configuración para
parámetros de su módulo, así como la capacidad de copiar el
configuración de otro nodo ya en su lugar.

Cuando se modifica un parámetro, la línea correspondiente se vuelve amarilla,
![node04](../ /images/ /node04.png) le paramètre es en attente d'être
appliqué.

Si el módulo acepta el parámetro, la línea vuelve a ser transparente.

Sin embargo, si el módulo rechaza el valor, la línea se volverá roja
con el valor aplicado devuelto por el módulo.
![node05](../ /images/ /node05.png)

En la inclusión, se detecta un nuevo módulo con los parámetros por
defecto del fabricante. En algunos módulos, la funcionalidad no
no estará activo sin modificar uno o más parámetros.
Consulte la documentación del fabricante y nuestras recomendaciones.
para configurar correctamente sus nuevos módulos.

> **Tip**
>
> Los módulos en la pila aplicarán los cambios de parámetros.
> solo en el próximo ciclo de despertador. Sin embargo, es posible
> activar manualmente un módulo, ver documentación del módulo.

> **Tip**
>
> El orden **Reanudar desde ...** le permite reanudar la configuración
> desde otro módulo idéntico, en el módulo actual.

![node06](../ /images/ /node06.png)

> **Tip**
>
> El orden **Aplicar en ...** le permite aplicar el
> configuración actual del módulo en uno o más módulos
> idéntico.

![node18](../ /images/ /node18.png)

> **Tip**
>
> El orden **Actualizar configuraciones** obligar al módulo a actualizar
> los parámetros guardados en el módulo.

Si no se define un archivo de configuración para el módulo, un
el asistente manual le permite aplicar parámetros al módulo.
![node17](../ /images/ /node17.png) Veillez vous référer à el documentation
del fabricante para conocer la definición del índice, valor y tamaño.

Associations
------------

Aquí es donde encuentra la gestión de los grupos de asociación de su
module.

![node07](../ /images/ /node07.png)

Los módulos Z-Wave pueden controlar otros módulos Z-Wave, sin
no pasar por el controlador Jeedom. La relación entre un módulo de
control y otro módulo se llama asociación.

Para controlar otro módulo, el módulo de control necesita
mantener una lista de dispositivos que recibirán el control de
ordenes. Estas listas se denominan grupos de asociación y son
siempre vinculado a ciertos eventos (por ejemplo, el botón presionado, el
activadores del sensor, etc.).

En caso de que ocurra un evento, todos los dispositivos
registrado en el grupo de asociación correspondiente recibirá un pedido
Basic.

> **Tip**
>
> Consulte la documentación del módulo para comprender las diferentes
> posibles grupos de asociación y su comportamiento.

> **Tip**
>
> La mayoría de los módulos tienen un grupo de asociación reservado
> para el controlador principal, se utiliza para volver a montar el
> información al controlador. Generalmente se llama : **Report** ou
> **LifeLine**.

> **Tip**
>
> Su módulo puede no tener ningún grupo.

> **Tip**
>
> La modificación de los grupos de asociación de un módulo en la pila será
> aplicado al siguiente ciclo de despertador. Sin embargo, es posible
> activar manualmente un módulo, ver documentación del módulo.

Para saber con qué otros módulos está asociado el módulo actual,
solo haz clic en el menú **Asociado con qué módulos**

![node08](../ /images/ /node08.png)

Todos los módulos que utilizan el módulo actual, así como los nombres de los
se mostrarán grupos de asociación.

**Asociaciones de instancias múltiples**

algunos módulos admiten un comando de clase de asociaciones de varias instancias.
Cuando un módulo admite este CC, es posible especificar con
en qué cuerpo queremos crear la asociación

![node09](../ /images/ /node09.png)

> **Important**
>
> Ciertos módulos deben estar asociados con la instancia 0 del controlador
> principal para funcionar bien. Por esta razón, el controlador
> está presente con y sin instancia 0.

Sistemas
--------

Pestaña que agrupa los parámetros del sistema del módulo.

![node10](../ /images/ /node10.png)

> **Tip**
>
> Los módulos de batería se activan a ciclos regulares, llamados
> Intervalo de activación. El intervalo de activación es un
> compensación entre la duración máxima de la batería y las respuestas
> deseado desde el dispositivo. Para maximizar la vida de tu
> módulos, adapte el valor del intervalo de activación, por ejemplo, a 14400
> segundos (4h), ver aún más alto dependiendo de los módulos y su uso.
> ![nodo11](../ /images/ /node11.png)

> **Tip**
>
> Los módulos **Interrupteur** y **Variateur** puede implementar un
> Clase de orden especial llamada **SwitchAll** 0x27. Usted puede
> cambiar el comportamiento aquí. Dependiendo del módulo, hay varias opciones
> disponible. El orden **Encender / apagar todo** se puede iniciar a través de
> su módulo controlador principal.

Actions
-------

Le permite realizar ciertas acciones en el módulo.

![node12](../ /images/ /node12.png)

Ciertas acciones estarán activas dependiendo del tipo de módulo y su
posibilidades o de acuerdo con el estado actual del módulo, como por ejemplo
si se supone muerto por el controlador.

> **Important**
>
> No use acciones en un módulo si no sabe qué
> que hacemos. Algunas acciones son irreversibles.. Las acciones
> puede ayudar a resolver problemas con uno o más módulos
> Onda Z.

> **Tip**
>
> El **Regeneración de detección de nodos** puede detectar el
> módulo para recuperar el último conjunto de parámetros. Esta acción
> se requiere cuando se le informa que una actualización de parámetros y
> o se requiere un comportamiento del módulo para una operación adecuada. El
> La regeneración de la detección de nodos implica un reinicio de la
> red, el asistente lo realiza automáticamente.

> **Tip**
>
> Si tiene varios módulos idénticos de los cuales es necesario
> para ejecutar el **Regeneración de detección de nodos**, El es
> posible lanzarlo una vez para todos los módulos idénticos.

![node13](../ /images/ /node13.png)

> **Tip**
>
> Si ya no se puede acceder a un módulo de batería y desea
> excluirlo, que la exclusión no tiene lugar, puede iniciar
> **Eliminar nodo fantasma** Un asistente realizará diferentes
> acciones para eliminar el llamado módulo fantasma. Esta acción implica
> reinicie la red y puede demorar varios minutos
> completado.

![node14](../ /images/ /node14.png)

Una vez iniciado, se recomienda cerrar la pantalla de configuración del
módulo y supervisar la eliminación del módulo a través de la pantalla de estado
Z-Wave.

> **Important**
>
> Solo los módulos con batería se pueden eliminar a través de este asistente.

Statistiques
------------

Esta pestaña proporciona algunas estadísticas de comunicación con el nodo.

![node15](../ /images/ /node15.png)

Puede ser de interés en el caso de módulos que se presumen muertos por el
controlador "muerto".

inclusión / exclusión
=====================

Cuando sale de fábrica, un módulo no pertenece a ninguna red Z-Wave.

Modo de inclusión
--------------

El módulo debe unirse a una red Z-Wave existente para comunicarse
con los otros módulos de esta red. Este proceso se llama
**Inclusion**. Los dispositivos también pueden salir de una red.
Este proceso se llama **Exclusion**. Ambos procesos se inician
por el controlador principal de la red Z-Wave.

![addremove01](../ /images/ /addremove01.png)

Este botón le permite cambiar al modo de inclusión para agregar un módulo
a su red Z-Wave.

Puede elegir el modo de inclusión después de hacer clic en el botón
**Inclusion**.

![addremove02](../ /images/ /addremove02.png)

Desde la aparición del Z-Wave +, es posible asegurar el
intercambios entre el controlador y los nodos. Por lo tanto, se recomienda
hacer inclusiones en modo **Seguro**.

Sin embargo, si no se puede incluir un módulo en modo seguro, por favor
incluirlo en modo **No es seguro**.

Una vez en modo de inclusión : Jeedom te dice.

\ [CONSEJO \] Un módulo 'no seguro' puede ordenar módulos 'no
seguro '. Un módulo 'no seguro' no puede ordenar un módulo
'seguro '. Un módulo 'seguro' puede ordenar módulos 'no
seguro 'siempre que el transmisor lo soporte.

![addremove03](../ /images/ /addremove03.png)

Una vez que se inicia el asistente, debe hacer lo mismo en su módulo
(consulte su documentación para cambiarlo al modo
inclusion).

> **Tip**
>
> Hasta que tenga la diadema, no está en modo
> inclusión.

Si vuelve a hacer clic en el botón, sale del modo de inclusión.

> **Tip**
>
> Se recomienda, antes de la inclusión de un nuevo módulo que sería
> "nuevo "en el mercado, para lanzar el pedido **Módulos de configuración** via
> pantalla de configuración del complemento. Esta acción se recuperará
> todas las últimas versiones de los archivos de configuración
> Openzwave y el mapeo del comando Jeedom.

> **Important**
>
> Durante una inclusión, se aconseja que el módulo esté cerca
> desde el controlador principal, a menos de un metro de tu libertad.

> **Tip**
>
> Algunos módulos requieren una inclusión en modo
> **Seguro**, por ejemplo para cerraduras.

> **Tip**
>
> Tenga en cuenta que la interfaz móvil también le da acceso a la inclusión,
> el panel móvil debe haber sido activado.

> **Tip**
>
> Si el módulo ya pertenece a una red, siga el proceso
> exclusión antes de incluirlo en su red. De lo contrario, la inclusión de
> este módulo fallará. También se recomienda realizar un
> exclusión antes de la inclusión, incluso si el producto es nuevo, fuera de
> carton.

> **Tip**
>
> Una vez que el módulo esté en su ubicación final, debe iniciar
> la acción se encarga de la red, para poder consultar todos los módulos de
> refrescar a todos los vecinos.

Modo de exclusión
--------------

![addremove04](../ /images/ /addremove04.png)

Este botón le permite ingresar al modo de exclusión, esto para eliminar un
módulo de su red Z-Wave, debe hacer lo mismo con su
módulo (consulte su documentación para cambiarlo al modo
exclusion).

![addremove05](../ /images/ /addremove05.png)

> **Tip**
>
> Hasta que tenga la diadema, no está en modo
> Exclusión.

Si vuelve a hacer clic en el botón, saldrá del modo de exclusión.

> **Tip**
>
> Tenga en cuenta que la interfaz móvil también le da acceso a la exclusión.

> **Tip**
>
> Un módulo no necesita ser excluido por el mismo controlador en
> que fue incluido previamente. De ahí el hecho de que recomendamos
> ejecutar una exclusión antes de cada inclusión.

Synchroniser
------------

![addremove06](../ /images/ /addremove06.png)

Botón para sincronizar los módulos de la red Z-Wave con el
Equipo de Jeedom. Los módulos están asociados con el controlador principal.,
el equipo en Jeedom se crea automáticamente cuando es
inclusión. También se eliminan automáticamente cuando se excluyen.,
si la opción **Eliminar automáticamente los dispositivos excluidos** est
activado.

Si ha incluido módulos sin Jeedom (requiere un dongle con
batería como el Aeon-labs Z-Stick GEN5), la sincronización será
necesario después de enchufar la llave, una vez que el demonio ha comenzado y
fonctionnel.

> **Tip**
>
> Si no tiene la imagen o Jeedom no ha reconocido su módulo,
> este botón se puede usar para corregir (siempre que la entrevista con el
> módulo está completo).

> **Tip**
>
> Si en su tabla de enrutamiento y / o en la pantalla de estado de Z-Wave, usted
> tener uno o más módulos nombrados con sus **nombre genérico**, la
> la sincronización remediará esta situación.

El botón Sincronizar solo es visible en modo experto :
![addremove07](../ /images/ /addremove07.png)

Redes Z-Wave
==============

![network01](../ /images/ /network01.png)

Aquí encontrará información general sobre su red Z-Wave.

![network02](../ /images/ /network02.png)

Resumen
------

La primera pestaña le brinda el resumen básico de su red Z-Wave,
En particular, encontrará el estado de la red Z-Wave y el número
artículos en la cola.

**Informations**

-   Proporciona información general sobre la red, la fecha de
    inicio, el tiempo requerido para obtener la red en un estado
    dice funcional.

-   El número total de nodos en la red, así como el número que duerme
    en el momento.

-   El intervalo de solicitud está asociado con la actualización manual. Él
    está preestablecido en el motor Z-Wave a los 5 minutos.

-   Los vecinos del controlador..

**Etat**

![network03](../ /images/ /network03.png)

Un conjunto de información sobre el estado actual de la red, a saber :

-   Estado actual, tal vez **Conductor inicializado**, **Topología cargada**
    o **Ready**.

-   Cola saliente, indica el número de mensajes en cola en el
    controlador esperando ser enviado. Este valor es generalmente
    alto durante el inicio de la red cuando el estado todavía está en
    **Conductor inicializado**.

Una vez que la red ha alcanzado al menos **Topología cargada**, des
los mecanismos internos del servidor Z-Wave forzarán actualizaciones a
valores, entonces es completamente normal ver el número de
mensajes Esto volverá rápidamente a 0.

> **Tip**
>
> Se dice que la red es funcional cuando alcanza el estado
> **Topología cargada**, es decir que el conjunto de nodos sectoriales
> han completado sus entrevistas. Dependiendo del número de módulos, el
> distribución de batería / sector, la elección del dongle USB y la PC en la que
> activa el complemento Z-Wave, la red alcanzará este estado entre un
> y cinco minutos.

Una red **Ready**, significa que todos los nodos de sector y pila tienen
completaron su entrevista.

> **Tip**
>
> Dependiendo de los módulos que tenga, es posible que la red
> nunca alcanza el estado por sí mismo **Ready**. Los controles remotos,
> por ejemplo, no se despierte solo y no complementará
> nunca su entrevista. En este tipo de casos, la red está completamente
> operacional e incluso si los controles remotos no han completado su
> entrevista, aseguran su funcionalidad dentro de la red.

**Capacidades**

Se utiliza para averiguar si el controlador es un controlador principal o
secondaire.

**Sistema**

Muestra diversa información del sistema.

-   Información sobre el puerto USB utilizado.

-   Versión de la biblioteca OpenZwave

-   Versión de la biblioteca Python-OpenZwave

Actions
-------

![network05](../ /images/ /network05.png)

Aquí encontrará todas las acciones posibles para todos sus
Red Z-Wave. Cada acción va acompañada de una breve descripción..

> **Important**
>
> Algunas acciones son realmente arriesgadas o incluso irreversibles, el equipo
> Jeedom no se hace responsable en caso de mal
> manipulación.

> **Important**
>
> Algunos módulos requieren inclusión en modo seguro, por
> ejemplo para cerraduras de puertas. La inclusión segura debe ser
> lanzado a través de la acción de esta pantalla.

> **Tip**
>
> Si no se puede iniciar una acción, se desactivará hasta
> cuando se puede ejecutar de nuevo.

Statistiques
------------

![network06](../ /images/ /network06.png)

Aquí encontrará estadísticas generales para todos sus
Red Z-Wave.

Gráfico de red
-------------------

![network07](../ /images/ /network07.png)

Esta pestaña le dará una representación gráfica de los diferentes
enlaces entre nodos.

Explicación de la leyenda del color. :

-   **Noir** : El controlador principal, generalmente representado
    como Jeedom.

-   **Vert** : Comunicación directa con el controlador, ideal.

-   **Blue** : Para los controladores, como los controles remotos, son
    asociado con el controlador primario, pero no tiene vecino.

-   **Jaune** : Todos los caminos tienen más de un salto antes de llegar.
    al controlador.

-   **Gris** : La entrevista aún no se ha completado, los enlaces serán
    realmente conocido una vez que se completa la entrevista.

-   **Rouge** : presuntamente muerto, o sin vecino, no participa / ya no participa en
    malla de red.

> **Tip**
>
> Solo el equipo activo se mostrará en el gráfico de red.

La red Z-Wave consta de tres tipos diferentes de nodos con
tres funciones principales.

La principal diferencia entre los tres tipos de nodos es su
conocimiento de la tabla de enrutamiento de la red y de allí en adelante
capacidad de enviar mensajes a la red:

Tabla de enrutamiento
----------------

Cada nodo puede determinar qué otros nodos están en
Comunicación directa. Estos nodos se llaman vecinos. A lo largo de
inclusión y / o posterior solicitud, el nodo puede
informar al controlador de la lista de vecinos. Gracias a estos
información, el controlador puede construir una tabla que tiene
toda la información sobre posibles vías de comunicación en
Una red.

![network08](../ /images/ /network08.png)

Las filas de la tabla contienen los nodos de origen y las columnas.
contener nodos de destino. Consulte la leyenda para
entender los colores de las celdas que indican los enlaces entre dos
nudos.

Explicación de la leyenda del color. :

-   **Vert** : Comunicación directa con el controlador, ideal.

-   **Blue** : Al menos 2 rutas con un salto.

-   **Jaune** : Menos de 2 rutas con un salto.

-   **Gris** : La entrevista aún no se ha completado, en realidad será
    actualizado después de completar la entrevista.

-   **Orange** : Todos los caminos tienen más de un salto.. Puede causar
    latencias.

> **Tip**
>
> Solo el equipo activo se mostrará en el gráfico de red.

> **Important**
>
> Un módulo presunto muerto, no participa / ya no participa en la red de la red.
> Se marcará aquí con un signo de exclamación rojo en un triángulo..

> **Tip**
>
> Puede iniciar manualmente la actualización de vecinos, por módulo
> o para toda la red utilizando los botones disponibles en el
> Tabla de enrutamiento.

Santé
=====

![health01](../ /images/ /health01.png)

Esta ventana resume el estado de su red Z-Wave :

![health02](../ /images/ /health02.png)

Tienes aqui :

-   **Module** : el nombre de su módulo, un clic en él le permite
    acceder directamente.

-   **ID** : ID de su módulo en la red Z-Wave.

-   **Notification** : último tipo de intercambio entre el módulo y el
    Controlador

-   **Groupe** : indica si la configuración del grupo está bien
    (controlador al menos en un grupo). Si no tienes nada es porque
    el módulo no admite la noción de grupo, esto es normal

-   **Constructeur** : indica si se está recuperando información
    la identificación del módulo está bien

-   **Voisin** : indica si se ha recuperado la lista de vecinos

-   **Statut** : Indica el estado de la entrevista (etapa de consulta) del
    module

-   **Batterie** : nivel de batería del módulo (un enchufe de red
    indica que el módulo se alimenta de la red eléctrica).

-   **Hora de despertarse** : para módulos de batería, da la
    frecuencia en segundos de los instantes cuando el módulo
    despertarse automáticamente.

-   **Paquete total** : muestra el número total de paquetes recibidos o
    enviado con éxito al módulo.

-   **%OK** : muestra el porcentaje de paquetes enviados / recibidos
    con éxito.

-   **Temporisation** : muestra el retraso promedio de envío de paquetes en ms.

-   **Última notificación** : Fecha de la última notificación recibida de
    módulo y la próxima hora de activación programada para módulos
    quien duerme.

    -   También permite informar si el nodo aún no está
        desperté una vez desde el lanzamiento del demonio.

    -   E indica si un nodo no se ha despertado como se esperaba.

-   **Ping** : Enviar una serie de mensajes al módulo a
    probar su correcto funcionamiento.

> **Important**
>
> Se mostrará el equipo deshabilitado pero no habrá información de
> el diagnóstico solo estará presente.

El nombre del módulo puede ir seguido de una o dos imágenes.:

![health04](../ /images/ /health04.png) Modules supportant la
MANDO\_CLASE\_ZWAVE\_PLUS\_INFO

![health05](../ /images/ /health05.png) Modules supportant la
MANDO\_CLASE\_SEGURIDAD y seguridad.

![health06](../ /images/ /health06.png) Modules supportant la
MANDO\_CLASE\_SEGURIDAD y no seguro.

![health07](../ /images/ /health07.png) Modulo FLiRS, routeurs esclaves
(módulos de batería) con escucha frecuente.

> **Tip**
>
> El comando Ping se puede usar si se presume que el módulo está muerto
> "MUERTE "para confirmar si este es realmente el caso.

> **Tip**
>
> Los módulos dormidos solo responderán a Ping cuando
> siguiente despertar.

> **Tip**
>
> La notificación de tiempo de espera no necesariamente significa un problema
> con el módulo. Ping y en la mayoría de los casos el módulo
> responderá con una notificación **NoOperation** que confirma un regreso
> Ping fructífero.

> **Tip**
>
> Tiempo de espera y% OK en los nodos con baterías antes de la finalización
> de su entrevista no es significativa. De hecho, el nudo no se va
> responder las preguntas del controlador sobre el hecho de que está dormido
> profundo.

> **Tip**
>
> El servidor Z-Wave se encarga automáticamente de iniciar pruebas en el
> Módulos de tiempo de espera después de 15 minutos

> **Tip**
>
> El servidor Z-Wave intenta automáticamente remontar módulos
> presunto muerto.

> **Tip**
>
> Se enviará una alerta a Jeedom si se presume que el módulo está muerto. Vosotras
> puede activar una notificación para estar más informado
> posible rápidamente. Vea la configuración de Mensajes en la pantalla
> Configuración de Jeedom.

![health03](../ /images/ /health03.png)

> **Tip**
>
> Si en su tabla de enrutamiento y / o en la pantalla de estado de Z-Wave usted
> tener uno o más módulos nombrados con sus **nombre genérico**, la
> la sincronización remediará esta situación.

> **Tip**
>
> Si en su tabla de enrutamiento y / o en la pantalla de estado de Z-Wave usted
> tener uno o más módulos llamados **Unknown**, eso significa que
> la entrevista del módulo no se completó con éxito. Teneis
> probablemente un **NOK** en la columna del constructor. Abre el detalle
> del módulo (s), para probar las soluciones sugeridas.
> (Consulte la sección Solución de problemas y diagnóstico, a continuación)

Estado de la entrevista
---------------------

Paso de entrevistar un módulo después de iniciar el demonio.

-   **None** Inicialización del proceso de búsqueda de nodos..

-   **ProtocolInfo** Recupere la información del protocolo, si esto
    nodo está escuchando (oyente), su velocidad máxima y sus clases
    de periféricos.

-   **Probe** Haga ping al módulo para ver si está despierto.

-   **WakeUp** Inicie el proceso de activación, si es un
    nudo durmiente.

-   **ManufacturerSpecific1** Recupere el nombre del fabricante y
    productos ids si ProtocolInfo lo permite.

-   **NodeInfo** Recuperar información sobre la gestión de clases.
    comandos soportados.

-   **NodePlusInfo** Recupere información de ZWave + sobre soporte
    clases de comando compatibles.

-   **SecurityReport** Recupere la lista de clases de orden que
    requieren seguridad.

-   **ManufacturerSpecific2** Recupere el nombre del fabricante y el
    identificadores de producto.

-   **Versions** Recuperar información de la versión.

-   **Instances** Recuperar información de clase de varias instancias
    de encargo.

-   **Static** Recuperar información estática (no cambia).

-   **CacheLoad** Haga ping al módulo durante el reinicio con la caché de configuración
    del dispositivo.

-   **Associations** Recuperar información sobre asociaciones.

-   **Neighbors** Recuperar la lista de nodos vecinos..

-   **Session** Recuperar información de la sesión (rara vez cambia).

-   **Dynamic** Recuperar información dinámica
    (cambia con frecuencia).

-   **Configuration** Recuperar información de parámetros de
    configuraciones (solo bajo pedido).

-   **Complete** El proceso de entrevista ha finalizado para este nodo..

Notification
------------

Detalles de notificaciones enviadas por módulos

-   **Completed** Acción completada con éxito.

-   **Timeout** Informe de retraso informado al enviar un mensaje.

-   **NoOperation** Informe sobre una prueba de nodo (Ping), que el mensaje
    ha sido enviado con éxito.

-   **Awake** Informar cuando un nodo acaba de despertarse

-   **Sleep** Informar cuando un nodo se ha quedado dormido.

-   **Dead** Informe cuando un nodo se presume muerto.

-   **Alive** Informar cuando se relanza un nodo.

Backups
=======

La parte de respaldo le permitirá administrar los respaldos de la topología.
de tu red. Este es su archivo zwcfgxxx.xml, es el
último estado conocido de su red, es una forma de caché de su
red Desde esta pantalla puedes :

-   Inicie una copia de seguridad (se realiza una copia de seguridad en cada parada reiniciando el
    red y durante operaciones críticas). Las últimas 12 copias de seguridad
    se mantienen

-   Restaurar una copia de seguridad (seleccionándola de la lista
    justo arriba)

-   Eliminar una copia de seguridad

![backup01](../ /images/ /backup01.png)

Actualizar OpenZWave
=======================

Después de una actualización del complemento Z-Wave, es posible que Jeedom
Solicite actualizar las dependencias de Z-Wave. Un NOK a nivel de
se mostrarán las dependencias:

![update01](../ /images/ /update01.png)

> **Tip**
>
> No se debe hacer una actualización de las dependencias con cada actualización
> plugin.

Jeedom debería lanzar la actualización de dependencia por sí solo si el
el complemento considera que son **NOK**. Esta validación se lleva a cabo en
después de 5 minutos.

La duración de esta operación puede variar según su sistema
(hasta más de 1 hora con frambuesa pi)

Una vez que se complete la actualización de dependencias, el demonio se reiniciará
automáticamente tras la validación de Jeedom. Esta validación es
hecho después de 5 minutos.

> **Tip**
>
> En el caso de que no ocurra la actualización de dependencias
> no completo, por favor consulte el registro **Openzwave\_update** qui
> debería informarle sobre el problema.

Lista de módulos compatibles.
============================

Encontrará la lista de módulos compatibles.
[aquí](https:/ // /doc.jeedom.com/es_ES/zwave/ /equipement.compatible)

Solución de problemas y diagnóstico
=======================

Mi módulo no se detecta o no proporciona sus identificadores de producto y tipo
-------------------------------------------------------------------------------

![troubleshooting01](../ /images/ /troubleshooting01.png)

Inicie la regeneración de la detección de nodos desde la pestaña Acciones
del módulo.

Si tiene varios módulos en este escenario, inicie **Actualizar
detección de nodos desconocidos** desde la pantalla **Red Zwave** onglet
**Actions**.

Mi módulo se presume muerto por el controlador Dead
--------------------------------------------------

![troubleshooting02](../ /images/ /troubleshooting02.png)

Si el módulo todavía está enchufado y accesible, siga las soluciones
propuesto en la pantalla del módulo.

Si el módulo ha sido cancelado o está realmente defectuoso, usted
puede excluirlo de la red usando **eliminar el nodo por error**
a través de la pestaña **Actions**.

Si el módulo ha sido reparado y un nuevo módulo
se ha entregado el reemplazo que puede lanzar **Reemplazar nodo fallido**
a través de la pestaña **Actions**, el controlador activa la inclusión, entonces usted
debe proceder con la inclusión en el módulo. La identificación del antiguo módulo será
cumplió tan bien como sus órdenes.

Cómo usar el comando SwitchAll
--------------------------------------

![troubleshooting03](../ /images/ /troubleshooting03.png)

Está disponible a través de su nodo controlador. Su controlador debe
tener los comandos de Encender todo y Apagar todo.

Si su controlador no aparece en su lista de módulos, inicie el
synchronisation.

![troubleshooting04](../ /images/ /troubleshooting04.png)

El comando Switch All Class generalmente se admite en
interruptores y atenuadores. Su comportamiento es configurable en
cada módulo que lo soporta.

Entonces podemos:

-   Desactivar el comando Cambiar todas las clases.

-   Activar para encendido y apagado.

-   Activar solo en.

-   Activar solo apagado.

La elección de las opciones depende del fabricante..

Por lo tanto, debe tomarse el tiempo para revisar todos sus
interruptores / atenuadores antes de configurar un escenario si no
no solo luces piloto.

Mi módulo no tiene un comando de escena o botón
----------------------------------------------

![troubleshooting05](../ /images/ /troubleshooting05.png)

Puede agregar el comando en la pantalla de asignación de comandos.

Esta es una orden **Info** en CC **0x2b** Instancia **0** commande
**datos \ [0 \]. val**

El modo de escena debe activarse en la configuración del módulo. Ver la
documentación de su módulo para más detalles.

Forzar valores de actualización
-------------------------------------

Es posible forzar a petición la actualización de los valores
una instancia para un comando de clase específico.

Es posible hacerlo a través de una solicitud http o crear un pedido
en la pantalla de mapeo de equipos.

![troubleshooting06](../ /images/ /troubleshooting06.png)

Esta es una orden **Action** elige el **CC** deseado para un
**Instance** dado con el comando **datos \ [0 \]. ForceRefresh ()**

Se colocarán todos los índices de instancia para este comando de clase
al día. Los nudos en las baterías esperarán su próximo despertar antes de
actualizar su valor.

También puede usar por script emitiendo una solicitud http para
Servidor REST Z-Wave.

Reemplace ip\_jeedom, node\_id, instancia\_id, cc\_id e index

http:/ // /token:\#APIKEY\#@ip\_jeedom:8083/ /ZWaveAPI/ /Run/ /devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

El acceso a la API REST ha cambiado, ver detalles
[aquí](./ /restapi.asciidoc).

Transfiera los módulos a un nuevo controlador
------------------------------------------------

Por diferentes razones, puede que tenga que transferir
todos sus módulos en un nuevo controlador principal.

Decides irte de **raZberry** un **Z-Stick Gen5** o porque
eso, tienes que realizar un **Reset** completo del controlador principal.

Aquí hay diferentes pasos para llegar sin perder sus escenarios.,
widgets de valor e historia:

-   1 \) Hacer una copia de seguridad de Jeedom.

-   2 \) Recuerde anotar (captura de pantalla) los valores de sus parámetros para cada
    módulo, se perderán debido a la exclusión.

-   3 \) En la configuración de Z-Wave, desmarque "Eliminar
    excluye automáticamente los dispositivos "y realiza una copia de seguridad.
    reinicios de red.

-   4a) En el caso de un **Reset**, Restablecer el controlador
    principal y reinicie el complemento.

-   4b) Para un nuevo controlador, detenga Jeedom, desconecte el viejo
    controlador y enchufe el nuevo. Inicie Jeedom.

-   5 \) Para cada dispositivo Z-Wave, cambie la ID de ZWave a **0**.

-   6 \) Abra 2 páginas del complemento Z-Wave en diferentes pestañas.

-   7 \) (a través de la primera pestaña) Vaya a la página de configuración de un
    módulo que desea incluir en el nuevo controlador.

-   8 \) (a través de la segunda pestaña) Excluir e incluir
    del módulo. Se crearán nuevos equipos..

-   9 \) Copie la ID de Z-Wave del nuevo equipo, luego elimine
    este equipo.

-   10 \) Regrese a la pestaña del módulo anterior (primera pestaña) y luego pegue
    la nueva identificación en lugar de la identificación anterior.

-   11 \) Los parámetros ZWave se perdieron durante la exclusión / inclusión,
    recuerde restablecer su configuración específica si no está utilizando el
    valores por defecto.

-   11 \) Repita los pasos 7 a 11 para cada módulo a transferir.

-   12 \) Al final, ya no debería tener equipo en ID 0.

-   13 \) Verifique que todos los módulos estén correctamente nombrados en la pantalla de
    salud Z-Wave. Inicie la sincronización si este no es el caso.

Reemplace un módulo defectuoso
------------------------------

Cómo rehacer la inclusión de un módulo defectuoso sin perder su
escenarios de valor, widgets e historia

Si se supone que el módulo está "Muerto" :

-   Tenga en cuenta (captura de pantalla) los valores de sus parámetros, se perderán
    siguiente inclusión.

-   Vaya a la pestaña de acciones del módulo y ejecute el comando
    "Reemplazar nodo fallido".

-   El controlador está en modo de inclusión, proceda con la inclusión de acuerdo con
    Documentación del módulo.

-   Restablece tus parámetros específicos.

Si no se presume que el módulo está "Muerto" pero aún está accesible:

-   En la configuración de ZWave, desmarque "Eliminar
    dispositivos excluidos automáticamente".

-   Tenga en cuenta (captura de pantalla) los valores de sus parámetros, se perderán
    siguiente inclusión.

-   Excluir el módulo defectuoso..

-   Vaya a la página de configuración del módulo defectuoso..

-   Abra la página del complemento ZWave en una pestaña nueva.

-   Incluir el módulo.

-   Copie la ID del nuevo módulo, luego elimine este equipo.

-   Regrese a la pestaña del módulo anterior y luego pegue la nueva ID en
    el lugar de la identificación anterior.

-   Restablece tus parámetros específicos.

Eliminación del nodo fantasma
----------------------------

Si ha perdido toda comunicación con un módulo alimentado por batería y
desea excluirlo de la red, es posible que la exclusión
no tiene éxito o el nodo permanece presente en su red.

El asistente automático de nodo fantasma está disponible.

-   Vaya a la pestaña de acciones del módulo para eliminar.

-   Probablemente tendrá un estado **CacheLoad**.

-   Comando de inicio **Eliminar nodo fantasma**.

-   La red Z-Wave se detiene. El asistente automático modifica el
    Expediente **zwcfg** para eliminar el CC WakeUp del módulo. El
    reinicios de red.

-   Cerrar la pantalla del módulo.

-   Abra la pantalla Z-Wave Health.

-   Espere a que se complete el ciclo de inicio (topología cargada).

-   El módulo normalmente se marcará como presunto muerto.

-   Al minuto siguiente, verá que el nodo desaparece de la pantalla.
    de salud.

-   Si en la configuración de Z-Wave, ha desmarcado la opción
    "Eliminar automáticamente los dispositivos excluidos ", deberá
    eliminar manualmente el equipo correspondiente.

Este asistente solo está disponible para módulos de batería.

Acciones posteriores a la inclusión
----------------------

Se recomienda realizar la inclusión al menos a 1M del controlador
principal, pero no será la posición final de su nuevo módulo.
Aquí hay algunas buenas prácticas a seguir luego de la inclusión de un nuevo
módulo en su red.

Una vez que se completa la inclusión, una serie de
parámetros de nuestro nuevo módulo para aprovecharlo al máximo. Recordatorio,
Los módulos, después de la inclusión, tienen la configuración predeterminada de
constructor Disfruta estar al lado del controlador y la interfaz
Jeedom para configurar correctamente su nuevo módulo. También será más
simple para activar el módulo para ver el efecto inmediato del cambio.
Algunos módulos tienen documentación específica de Jeedom para usted
ayuda con diferentes parámetros y valores recomendados.

Pruebe su módulo, valide los comentarios de información, los comentarios de estado
y posibles acciones en el caso de un actuador.

Durante la entrevista, su nuevo módulo buscó a sus vecinos..
Sin embargo, los módulos en su red aún no conocen su
nuevo módulo.

Mueva su módulo a su ubicación final. Comience la actualización
de sus vecinos y despertarlo nuevamente.

![troubleshooting07](../ /images/ /troubleshooting07.png)

Vemos que ve un cierto número de vecinos pero que el
los vecinos no lo ven.

Para remediar esta situación, se deben tomar medidas para tratar el
red, para pedir a todos los módulos que encuentren a sus vecinos.

Esta acción puede tomar 24 horas antes de terminar, sus módulos
con batería realizará la acción solo la próxima vez que se despierten.

![troubleshooting08](../ /images/ /troubleshooting08.png)

La opción de tratar la red dos veces por semana le permite hacer esto
proceso sin acción de su parte, es útil al configurar
coloca nuevos módulos y / o cuando se mueven.

No hay comentarios de la condición de la batería
-------------------------------

Los módulos Z-Wave rara vez envían el estado de su batería al
controlador Algunos lo harán en la inclusión solo cuando
esto alcanza el 20% u otro valor umbral crítico.

Para ayudarlo a controlar mejor el estado de sus baterías, la pantalla Baterías
en el menú Análisis le da una visión general del estado de su
baterías Un mecanismo de notificación de batería baja también es
disponible.

El valor devuelto desde la pantalla Baterías es el último conocido en el
cache.

Todas las noches, el complemento Z-Wave le pide a cada módulo que se actualice
Valor de la batería. La próxima vez que se despierte, el módulo envía el valor a
Jeedom para ser agregado al caché. Por lo general, tienes que esperar hasta
al menos 24 horas antes de obtener un valor en la pantalla Baterías.

> **Tip**
>
> Por supuesto, es posible actualizar manualmente el valor
> Batería a través de la pestaña Valores del módulo y luego espere el siguiente
> alarma o despertar manualmente el módulo para obtener un
> recuperación inmediata. El intervalo de activación del módulo
> se define en la pestaña Sistema del módulo. Para optimizar la vida de
> sus baterías, se recomienda espaciar este retraso tanto como sea posible. Por 4h,
> aplicar 14400, 12h 43200. Algunos módulos deben
> escuche regularmente mensajes del controlador como
> Termostatos. En este caso, es necesario pensar en 15 min o 900. Cada
> el módulo es diferente, por lo que no existe una regla exacta, este es el caso
> por caso y por experiencia.

> **Tip**
>
> La descarga de una batería no es lineal, algunos módulos lo harán
> mostrar un gran porcentaje de pérdida en los primeros días de apuesta
> en servicio, luego no se mueva durante semanas para vaciar
> rápidamente una vez pasado el 20%.

El controlador se está inicializando
----------------------------------------

Cuando inicias el demonio Z-Wave, si intentas iniciar
inmediatamente una inclusión / exclusión, corre el riesgo de obtener esto
message: \* "El controlador se está inicializando, por favor
intente nuevamente en unos minutos"

> **Tip**
>
> Después de que se inicia el demonio, el controlador cambia a todos los
> módulos para repetir su entrevista. Este comportamiento es
> completamente normal en OpenZWave.

Sin embargo, si después de varios minutos (más de 10 minutos), tiene
Todavía este mensaje, ya no es normal.

Tienes que probar los diferentes pasos:

-   Asegúrese de que las luces de la pantalla de salud Jeedom sean verdes.

-   Asegúrese de que la configuración del complemento esté en orden.

-   Asegúrese de haber seleccionado el puerto correcto para
    Tecla ZWave.

-   Asegúrese de que la configuración de su red Jeedom sea correcta.
    (Atención si ha realizado una restauración desde una instalación de bricolaje a
    imagen oficial, el sufijo / libertad no debe incluirse)

-   Mire el registro del complemento para ver si hay un error
    no arriba.

-   Mira el **Console** Complemento ZWave, para ver si hay un error
    no subió.

-   Lanzar el demonio por **Debug** mira de nuevo a la **Console** et
    registros de complementos.

-   Reiniciar completamente Jeedom.

-   Asegúrese de tener un controlador Z-Wave, el
    Razberry a menudo se confunde con EnOcean (error durante
    la orden).

Ahora debemos comenzar las pruebas de hardware:

-   El Razberry está bien conectado al puerto GPIO.

-   La alimentación USB es suficiente.

Si el problema persiste, reinicie el controlador:

-   Detenga completamente su Jeedom a través del menú de detención en el
    perfil de usuario.

-   Desconecta el poder.

-   Retire el dongle USB o Razberry según corresponda, aproximadamente
    5 minutos.

-   Vuelva a conectar todo e intente nuevamente.

El controlador ya no responde.
----------------------------

No se transmiten más pedidos a los módulos, pero regresa
de estados subieron hacia Jeedom.

La cola de mensajes del controlador puede estar llena.
Vea la pantalla de la red Z-Wave si el número de mensajes pendientes no
qu'augmenter.

En este caso, debe reiniciar el Demon Z-Wave.

Si el problema persiste, debe reiniciar el controlador:

-   Detenga completamente su Jeedom a través del menú de detención en el
    perfil de usuario.

-   Desconecta el poder.

-   Retire el dongle USB o Razberry según corresponda, aproximadamente
    5 minutos.

-   Vuelva a conectar todo e intente nuevamente.

Error durante dependencias
---------------------------

Pueden ocurrir varios errores al actualizar
dependencias Debe consultar el registro de actualización de dependencias.
para determinar cuál es exactamente el error. De manera general,
el error está al final del registro en las últimas líneas.

Aquí están los posibles problemas y sus posibles soluciones.:

-   no se pudo instalar mercurial - abortar

El paquete mercurial no desea instalar, para corregir el inicio en
ssh:

````
    sudo rm / /var/ /lib/ /dpkg/ /info/ /$mercurial* -f
    sudo apt-gy install mercurial
````

-   Las adicciones parecen bloqueadas en un 75%

Con un 75%, este es el comienzo de la compilación de la biblioteca openzwave también
envoltura de pitón openzwave. Este paso es muy largo, podemos
sin embargo, consulte el progreso a través de la vista de registro de actualización. Él
así que sé paciente.

-   Error al compilar la biblioteca openzwave

````
        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed source if appropriate.
        See <file:/ // // /usr/ /share/ /doc/ /gcc-4.9/ /README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targy 'build' failed
        make: *** [build] Error 1
````

Este error puede ocurrir debido a la falta de memoria RAM durante el
compilation.

Desde la interfaz de usuario de Jeedom, inicie la compilación de dependencias.

Una vez lanzado, en ssh, detenga estos procesos (los consumidores en
memoria) :

````
    sudo systemctl stop cron
    sudo systemctl stop apache2
    sudo systemctl stop mysql.
````

Para seguir el progreso de la compilación, adaptamos el
archivo de registro de openzwave\_update.

````
    tail -f / /var/ /www/ /html/ /log/ /openzwave_update
````

Cuando la compilación esté completa y sin error, reinicie el
servicios que detuvo

sudo systemctl start cron sudo systemctl start apache2 sudo systemctl
iniciar mysql

Usando la tarjeta Razberry en una Raspberry Pi 3
------------------------------------------------------

Para usar un controlador Razberry en una Raspberry Pi 3, el
El controlador Bluetooth interno de Raspberry debe estar deshabilitado.

Agrega esta línea:

````
    dtoverlay=pi3-miniuart-bt
````

Al final del archivo:

````
    / /boot/ /config.txt
````

Luego reinicie su Frambuesa.

API HTTP
========

El complemento Z-Wave proporciona desarrolladores y usuarios
Una API completa para operar la red Z-Wave mediante solicitud
HTTP.

Puede utilizar todos los métodos expuestos por el
Servidor REST del demonio Z-Wave.

La sintaxis para llamar a las rutas es de esta forma:

URL =
[http:/ // /token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/ \#ROUTE\#](http:/ // /token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/ /#ROUTE#)

-   \#API\_KEY\# corresponde a su clave API, específica de
    su instalación. Para encontrarlo, ve al menú «
    Principal », puis « Administration » y « Configuración », en activant
    Modo experto, verá una línea de clave API.

-   \#IP\_JEEDOM\# corresponde a su URL de acceso de Jeedom.

-   \#PORTDEMON\# corresponde al número de puerto especificado en la página de
    configuración del complemento Z-Wave, por defecto: 8083.

-   \#ROUTE\# corresponde a la ruta en el servidor REST para ejecutar.

Para conocer todas las rutas, consulte
[Github](https:/ // /github.com/ /jeedom/ /plugin-openzwave) del complemento Z-Wave.

Example: Para hacer ping al id del nodo 2

URL =
http:/ // /token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ /ZWaveAPI/ /Run/ /devices\[2\].TestNode()

# FAQ

> **Me sale el error "No hay suficiente espacio en el búfer de flujo"**
>
> Desafortunadamente, este error es hardware, no hay nada que podamos hacer y estamos buscando por el momento cómo forzar un reinicio del demonio en el caso de este error (pero a menudo también es necesario desconectar la clave durante 5 minutos para que vuelva a comenzar)
