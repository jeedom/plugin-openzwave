Description
===========

Este complemento permite el explotación de módulos Onda Z a través de
el biblioteca OpenZwave.

Introduction
============

Onda Z se comunica utilizando tecnología de radio de baja potencia
en el banda de frecuencia de 868.42 MHz. Está específicamente diseñado
para aplicaciones de domótica. El protocolo de radio Onda Z es
optimizado para intercambios de bajo ancho de banda (entre 9 y 40
kbit / / s) entre dispositivos alimentados por batería o por red.

Onda Z opera en el rango de frecuencia de sub gigahercios, dependiendo de
regiones (868 MHz en Europa, 908 MHz en los EE. UU. y otras frecuencias
según las bandas ISM de las regiones). El rango teórico es aproximadamente
30 metros en interiores y 100 metros en exteriores. El red Z-Wave
utiliza tecnología de malel para aumentar el alcance y
fiabilidad Onda Z está diseñado para integrarse fácilmente en
productos electrónicos de bajo consumo, incluidos
baterías como controles remotos, detectores de humo y
Seguridad.

El Onda Z +, trae ciertas mejoras que incluyen un mejor rango y
mejora el duración de el batería, entre otras cosas. El
Compatibilidad total con el Onda Z.

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
> quítelo de el caja usando un simple cable de extensión USB de 1M por
> Ejemplo.

El distancia entre otros transmisores inalámbricos como teléfonos
Las transmisiones de audio inalámbricas o de radio deben ser de al menos 3 metros. El
Se deben considerar las siguientes fuentes de radio :

-   Interferencia por interruptor de motores eléctricos.

-   Interferencia de dispositivos eléctricos defectuosos.

-   Interferencia de equipos de soldadura HF

-   dispositivos de tratamiento médico

Espesor de pared efectivo
---------------------------

Las ubicaciones de los módulos deben elegirse de tal manera que
el línea de conexión directa solo funciona en un tiempo muy corto
distancia a través del material (una pared), para evitar tanto como sea posible
mitigaciones.

![introduction01](../ /images/ /introduction01.png)

Las partes metálicas del edificio o los muebles pueden bloquear
ondas electromagneticas.

Malel y Enrutamiento
-------------------

Los nodos principales de Onda Z pueden transmitir y repetir mensajes
que no están dentro del alcance directo del controlador. Esto permite un más
Gran flexibilidad de comunicación, incluso Si no hay conexión.
inalámbrico directo o Si una conexión no está disponible temporalmente, para
debido a un cambio en el habitación o el edificio.

![introduction02](../ /images/ /introduction02.png)

El controlador **Id 1** puede comunicarse directamente con los nodos 2, 3
y 4. Nodo 6 está fuera de su alcance de radio, sin embargo, es
encontrado en el área de cobertura de radio del nodo 2. Por lo tanto, el
el controlador puede comunicarse con el nodo 6 a través del nodo 2. De esta
manera, el ruta desde el controlador a través del nodo 2 al nodo 6, se llama
camino En el caso donde el comunicación directa entre el nodo 1 y el
el nodo 2 está bloqueado, hay otra opción para comunicarse con
nodo 6, usando el nodo 3 como otro repetidor de señal.

Es obvio que cuantos más nodos de sector tenga, más
las opciones de enrutamiento aumentan y aumenta el estabilidad de el red.
El protocolo Onda Z es capaz de enrutar mensajes por
a través de un máximo de cuatro nodos repetidos. Es un
compensación entre tamaño de red, estabilidad y duración máxima
de un mensaje.

> **Tip**
>
> Se recomienda encarecidamente al inicio de el instalación tener una relación
> entre nodos sectoriales y nodo con 2/ /3 baterías, para tener una buena
> malel de red. Favorezca los micromódulos sobre los enchufes inteligentes. El
> los micro módulos estarán en una ubicación final y no serán
> desconectados, generalmente también tienen un mejor alcance. Una bueno
> el salida es el iluminación de las áreas comunes. Va a ayudar bien
> distribuya los módulos del sector en ubicaciones estratégicas en su
> casa. Luego puede agregar tantos módulos en el pila
> Si lo desea, Si sus rutas básicas son buenas.

> **Tip**
>
> El **Gráfico de red** así como el **Tabel de enrutamiento**
> le permite ver el calidad de su red.

> **Tip**
>
> Hay módulos repetidores para llenar áreas donde no hay módulo
> sector no tiene uso.

Propiedadesde de los dispositivos Z-Wave
-------------------------------

|  | Vecinos | Camino | Posibles funciones |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controlador | Conoce a todos los vecinos | Tiene acceso a el tabel de enrutamiento completa | Puede comunicarse con todos los dispositivos en el red, Si existe un canal |
| Esclavo | Conoce a todos los vecinos | No tiene información sobre el tabel de enrutamiento | No se puede responder al nodo que recibió el mensaje.. Por lo tanto, no se pueden enviar mensajes no solicitados. |
| Esclavos enrutamiento | Conoce a todos sus vecinos | Con conocimiento parcial de el tabel de enrutamiento. | Puede responder al nodo desde el que recibió el mensaje y puede enviar mensajes no solicitados a varios nodos |

En resumen:

-   Cada dispositivo Onda Z puede recibir y acusar recibo de
    messages

-   Los controladores pueden enviar mensajes a todos los nodos en el
    réseau, sollicités o non « El maître peut parler quand il veut y à
    a quien quiere »

-   Los esclavos no pueden enviar mensajes no solicitados,
    mais seulement une réponse aux demandesde «L'esclave ne parle que si
    le preguntamos »

-   Los esclavos enrutados pueden responder a las solicitudesde y son
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
Sin embargo, puedesde cambiar el configuración.

Dependencias
-----------

Esta parte le permite validar e instalar las dependencias requeridas
El correcto funcionamiento del complemento Zwave (tanto local como
deportado, aquí localmente) ![configuración02](../ /images/ /configuration02.png)

-   Una estatuto **OK** confirma que se cumplen las dependencias.

-   Si el estado es **NOK**, las dependencias deberán ser reinstaladas
    usando el botón ![configuración03](../ /images/ /configuration03.png)

> **Tip**
>
> El actualización de dependencias puede demorar más de 20 minutos dependiendo de
> tu material. El progreso se muestra en tiempo real y un registro
> **Openzwave\_update** es accesible.

> **Important**
>
> El actualización de dependencias normalmente solo se debe hacer
> Si el estatuto es **NOK**, pero es posible, sin embargo, ajustar
> ciertos problemas, para ser llamados a rehacer el instalación de
> Dependencias.

> **Tip**
>
> Si está en modo remoto, las dependencias del daemon local pueden
> ser NOK, es completamente normal.

Demonio
-----

Esta parte le permite validar el estado actual de los demonios y
configurar el gestión automática de estos.
![Configuración04](../ /images/ /configuration04.png) El démon local et
todos los demonios deportados se mostrarán con sus diferentes
informations

-   El **Statut** indica que el demonio se está ejecutando actualmente.

-   El **Configuration** indica Si el configuración del demonio
    es valido.

-   El botón **(Re)Iniciar** permite forzar el reinicio de la
    plugin, en modo normal o iniciarlo el primera vez.

-   El botón **Detenido**, visible solo Si el gestión automática
    está desactivado, obliga al demonio a detenerse.

-   El **Gestión automática** permite que Jeedom se inicie automáticamente
    el demonio cuando se inicia Jeedom, así como reiniciarlo en caso de que
    de problema.

-   El **Última ejecución** es como su nombre indica el fecha de
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
> use este modo solo Si necesita diagnosticar un problema
> particular. No se recomienda dejar que el demonio corra mientras
> **Debug** permanentemente, Si usamos un **SD-Card**. Una vez que
> depurar, no te olvidesde de volver a un nivel inferior
> tan alto como el nivel **Error** que solo vuelve a lo posible
> errores.

Configuration
-------------

Esta parte le permite configurar los parámetros generales del complemento
![Configuración06](../ /images/ /configuration06.png)

-   **Principal** :

    -   **Eliminar automáticamente los dispositivos excluidos** :
        El opción Sí le permite eliminar los dispositivos excluidos del
        Red Onda Z. El opción No le permite conservar el equipo.
        en Jeedom incluso Si han sido excluidos de el red. El equipo
        tendrá que ser eliminado manualmente o reutilizado en él
        asignar una nueva Identificación de Onda Z Si está migrando el
        controlador principal.

    -   **Aplicar el conjunto de configuración recomendado para su inclusión.** :
        opción de aplicar el conjunto de
        configuración recomendada por el equipo de Jeedom (recomendado)

    -   **Desactivar el actualización en segundo plano de las unidades** :
        No solicite una actualización de las unidades
        en el fondo.

    -   **Ciclo (s)** : permite definir el frecuencia de los ascensores
        en Jeedom.

    -   **Puerto de llave Z-Wave** : el puerto USB en el que su interfaz
        Onda Z está conectado. Si usa el Razberry, tiene,
        dependiendo de su arquitectura (RPI o Jeedomboard) el 2
        posibilidadesde al final de el lista.

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
        > el configuración se acaba de aplicar, puede manualmente
        > comenzar a recuperar configuraciones de módulos.

Una vez recuperadas las configuraciones, tomará de acuerdo con los cambios
traído:

-   Para un nuevo módulo sin configuración o control : excluir y
    vuelva a incluir el módulo.

-   Para un módulo para el que solo se han actualizado los parámetros :
    iniciar el regeneración de el detección de nodos, a través de el pestaña Acciones
    del módulo (el complemento debe reiniciarse).

-   Pour un Modulo dont le « mapping » de encargos a été corrigé : la
    lupa en los controles, ver abajo.

    > **Tip**
    >
    > En caso de duda, se recomienda excluir y volver a incluir el módulo..

No te olvidesde de ![configuración08](../ /images/ /configuration08.png) si
haces un cambio.

> **Important**
>
> Si estás usando Ubuntu : Para que el demonio funcione, debes
> absolutamente tiene ubuntu 15.04 (las versiones inferiores tienen un error y
> el demonio no puede comenzar). Ten cuidado Si haces una apuesta
> actualizado desde 14.04 toma una vez en 15.04 relanzamiento
> instalación de dependencias.

> **Important**
>
> Selección del puerto clave Onda Z en modo de detección automática,
> **Auto**, solo funciona para dongles USB.

Panel móvil
-------------

![Configuración09](../ /images/ /configuration09.png)

Permite mostrar o no el panel móvil cuando usa
el aplicación en un teléfono.

Configuración del equipo
=============================

Se puede acceder a el configuración del equipo Onda Z desde el menú
Plugin :

![appliance01](../ /images/ /appliance01.png)

A continuación se muestra un ejemplo de una página de complemento de Onda Z (presentada con
algunos equipos) :

![appliance02](../ /images/ /appliance02.png)

> **Tip**
>
> Como en muchos lugares de Jeedom, coloca el mouse en el extremo izquierdo
> muestra un menú de acceso rápido (puede, en
> desde tu perfil, siempre déjalo visible).

> **Tip**
>
> Los botones en el linea superior **Synchroniser**,
> **Red Zwave** y **Santé**, son visibles solo Si estás en
> modo **Expert**. ![aparato03](../ /images/ /appliance03.png)

Principal
-------

Aquí encontrarás toda el configuración de tu equipo :

![appliance04](../ /images/ /appliance04.png)

-   **Nombre del equipo** : nombre de su módulo Onda Z.

-   **Objeto padre** : indica el objeto padre al que
    pertenece equipo.

-   **Categoría** : categorías de equipos (puede pertenecer a
    categorías múltiples).

-   **Activer** : activa su equipo.

-   **Visible** : lo hace visible en el tablero.

-   **Identificación de nodo** : Identificación del módulo en el red Onda Z. Esto puede ser
    útil si, por ejemplo, desea reemplazar un módulo defectuoso.
    Simplemente incluya el nuevo módulo, obtenga su Identificación y el
    poner en lugar de el Identificación del módulo anterior y finalmente eliminar
    el nuevo módulo.

-   **Module** : este campo solo aparece Si hay diferentes tipos de
    configuración para su módulo (caso para módulos que pueden hacer
    cables piloto por ejemplo). Te permite elegir el
    configuración para usarlo o modificarlo más tarde

-   **Marque** : fabricante de su módulo Onda Z.

-   **Configuration** : ventana para configurar los parámetros de la
    module

-   **Assistant** : solo disponible en ciertos módulos, usted
    ayuda a configurar el módulo (caso en el teclado zipato por ejemplo)

-   **Documentation** : Este botón le permite abrir directamente el
    Documentación de Jeedom sobre este módulo.

-   **Supprimer** : El permite eliminar un elemento del equipo y todos estos
    comandos adjuntos sin excluirlo de el red Onda Z.

> **Important**
>
> Eliminar un equipo no da como resultado el exclusión del módulo
> en el controlador. ![aparato11](../ /images/ /appliance11.png) Un
> el equipo eliminado que todavía está conectado a su controlador
> recreado automáticamente después de el sincronización.

Commandes
---------

A continuación encontrará el lista de pedidos. :

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
    esta configurado. Ejemplo para una lámpara, el intensidad está vinculada a su
    estado, esto permite que el widgy tenga el estado real de el lámpara.

-   tipo y subtipo.

-   el instancia de este comando Onda Z (reservado para expertos).

-   el clase del control Onda Z (reservado para expertos).

-   el índice de valor (reservado para expertos).

-   el pedido en sí (reservado para expertos).

-   "Valor de retroalimentación de estado "y" Duración antes de el retroalimentación de estado" : permet
    para indicarle a Jeedom que después de un cambio en el información
    el valor debe volver a Y, X min después del cambio. Ejemplo : dans
    el caso de un detector de presencia que emite solo durante un
    detección de presencia, es útEl esablecer por ejemplo 0
    valor y 4 en duración, de modo que 4 minutos después de una detección de
    movimiento (y Si no hubiera nuevos) Jeedom
    restablece el valor de el información a 0 (no se detecta más movimiento).

-   Guardar historial : permite historizar los datos.

-   Mostrar : permite mostrar los datos en el tablero.

-   Invertir : permite invertir el estado para tipos binarios.

-   Unidad : unidad de datos (puede estar vacía).

-   Min / / max : límites de datos (pueden estar vacíos).

-   Configuración avanzada (ruedas con muescas pequeñas) : Muestra
    El configuración avanzada del comando (método
    historia, widgy ...).

-   Probar : Se usa para probar el comando.

-   Eliminar (firmar -) : permite eliminar el comando.

> **Important**
>
> El botón **Tester** en el caso de un comando de tipo Información, no
> no consultar el módulo directamente sino el valor disponible en el
> jeedom Cubierta. El prueba devolverá el valor correcto solo Si el
> El módulo en cuestión ha transmitido un nuevo valor correspondiente al
> definición del comando. Entonces es completamente normal no
> obtener resultados después de el creación de un nuevo comando de información,
> especialmente en un módulo de batería que rara vez notifica a Jeedom.

El **loupe**, disponible en el pestaña general, le permite recrear
todos los comandos para el módulo actual.
![appliance13](../ /images/ /appliance13.png) Si aucune Comando n'est
presente o Si los comandos son incorrectos, el lupa debe remediar
el situación.

> **Important**
>
> El **loupe** borrará los pedidos existentes. Si las órdenes
> fueron utilizados en escenarios, deberá corregir su
> escenarios en otros lugares donde se operaban los controles.

Juegos de comando
-----------------

Algunos módulos tienen varios conjuntos de comandos preconfigurados

![appliance06](../ /images/ /appliance06.png)

Puede seleccionarlos a través de las posibles opciones, Si el módulo
permet.

> **Important**
>
> Debe llevar el lupa para aplicar los nuevos conjuntos de
> Comandos.

Documentación y Asistente
--------------------------

Para un cierto número de módulos, ayuda específica para configurar
lugar, así como recomendaciones de parámetros están disponibles.

![appliance07](../ /images/ /appliance07.png)

El botón **Documentation** proporciona acceso a el documentación
módulo específico para Jeedom.

Los módulos especiales también tienen un asistente específico para
para facilitar el aplicación de ciertos parámetros u operaciones.

El botón **Assistant** permite el acceso a el pantalel de asistente específica
del módulo.

Configuración recomendada
-------------------------

![appliance08](../ /images/ /appliance08.png)

El permite aplicar un conjunto de configuración recomendado por el equipo
Jeedom.

> **Tip**
>
> Cuando se incluyen, los módulos tienen el configuración predeterminada de
> fabricante y algunas funciones no están activadas por defecto.

Lo siguiente, según corresponda, se aplicará para simplificar
usando el módulo.

-   **Configuraciones** permitiendo una rápida puesta en marcha de el asamblea
    funcionalidad del módulo.

-   **Grupos de asociaciones** requerido para una operación adecuada.

-   **Intervalo de despertador**, para módulos con batería.

-   Activación de **actualización manual** para módulos hacer
    no volviendo por sí mismos sus cambios de estado.

Para aplicar el conjunto de configuración recomendado, haga clic en el botón
: **Configuración recomendada**, luego confirme el aplicación de
configuraciones recomendadas.

![appliance09](../ /images/ /appliance09.png)

El asistente activa los diversos elementos de configuración..

Se mostrará una confirmación del buen progreso en forma de banner.

![appliance10](../ /images/ /appliance10.png)

> **Important**
>
> Los módulos de batería se deben activar para aplicar el conjunto de
> Configuración.

El página del equipo le informa Si los artículos aún no han sido
sido activado en el módulo. Consulte el documentación de la
módulo para activarlo manualmente o esperar el próximo ciclo de
despertar.

![aparato11](../ /images/ /appliance11.png)

> **Tip**
>
> Es posible activar automáticamente el aplicación del juego.
> configuración recomendada cuando se incluye un nuevo módulo, ver
> el sección de configuración del complemento para más detalles.

Configuracion de modulos
=========================

Aquí es donde encontrará toda el información sobre su módulo.

![node01](../ /images/ /node01.png)

El ventana tiene varias pestañas. :

Resumen
------

Proporciona un resumen completo de su nodo con información variada
en este caso, por ejemplo, el estado de las solicitudesde que permite conocer
Si el nodo está esperando información o el lista de nodos vecinos.

> **Tip**
>
> En esta pestaña es posible tener alertas en caso de detección
> posible por un problema de configuración, Jeedom indicará el marcha
> seguir para corregir. No confunda una alerta con un
> error, el alerta es en el mayoría de los casos un simple
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
> en este caso active el actualización manual a los 5 minutos en el
> valores deseados. Se recomienda dejar automáticamente el
> Refrescante. El abuso del refresco manual puede afectar
> fuertemente el rendimiento de el red Z-Wave, use solo para
> los valores recomendados en el documentación específica de Jeedom.
> ![nodo16](../ /images/ /node16.png) El conjunto de valores (índice) de
> el instancia de un comando de clase se volverá a montar, activando el
> actualización manual en el índice más pequeño de el instancia de la
> comando de clase. Repita para cada instancia Si es necesario.

Configuraciones
----------

![node03](../ /images/ /node03.png)

Aquí encontrará todas las posibilidadesde de configuración para
parámetros de su módulo, así como el capacidad de copiar el
configuración de otro nodo ya en su lugar.

Cuando se modifica un parámetro, el línea correspondiente se vuelve amarilla,
![node04](../ /images/ /node04.png) le paramètre es en attente d'être
appliqué.

Si el módulo acepta el parámetro, el línea vuelve a ser transparente.

Sin embargo, Si el módulo rechaza el valor, el línea se volverá roja
con el valor aplicado devuelto por el módulo.
![node05](../ /images/ /node05.png)

En el inclusión, se detecta un nuevo módulo con los parámetros por
defecto del fabricante. En algunos módulos, el funcionalidad no
no estará activo sin modificar uno o más parámetros.
Consulte el documentación del fabricante y nuestras recomendaciones.
para configurar correctamente sus nuevos módulos.

> **Tip**
>
> Los módulos en el piel aplicarán los cambios de parámetros.
> solo en el próximo ciclo de despertador. Sin embargo, es posible
> activar manualmente un módulo, ver documentación del módulo.

> **Tip**
>
> El orden **Reanudar desde ...** le permite reanudar el configuración
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
del fabricante para conocer el definición del índice, valor y tamaño.

Associations
------------

Aquí es donde encuentra el gestión de los grupos de asociación de su
module.

![node07](../ /images/ /node07.png)

Los módulos Onda Z pueden controlar otros módulos Z-Wave, sin
no pasar por el controlador Jeedom. El relación entre un módulo de
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
> Consulte el documentación del módulo para comprender las diferentes
> posibles grupos de asociación y su comportamiento.

> **Tip**
>
> El mayoría de los módulos tienen un grupo de asociación reservado
> para el controlador principal, se utiliza para volver a montar el
> información al controlador. Generalmente se llama : **Report** ou
> **LifeLine**.

> **Tip**
>
> Su módulo puede no tener ningún grupo.

> **Tip**
>
> El modificación de los grupos de asociación de un módulo en el piel será
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
en qué cuerpo queremos crear el asociación

![node09](../ /images/ /node09.png)

> **Important**
>
> Ciertos módulos deben estar asociados con el instancia 0 del controlador
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
> compensación entre el duración máxima de el batería y las respuestas
> deseado desde el dispositivo. Para maximizar el vida de tu
> módulos, adapte el valor del intervalo de activación, por ejemplo, a 14400
> segundos (4h), ver aún más alto dependiendo de los módulos y su uso.
> ![nodo11](../ /images/ /node11.png)

> **Tip**
>
> Los módulos **Interrupteur** y **Variateur** puede implementar un
> Clase de orden especial llamada **SwitchAll** 0x27. Usted puede
> cambiar el comportamiento aquí. Dependiendo del módulo, hay varias opciones
> disponible. El orden **Encender / / apagar todo** se puede iniciar a través de
> su módulo controlador principal.

Actions
-------

El permite realizar ciertas acciones en el módulo.

![node12](../ /images/ /node12.png)

Ciertas acciones estarán activas dependiendo del tipo de módulo y su
posibilidadesde o de acuerdo con el estado actual del módulo, como por ejemplo
Si se supone muerto por el controlador.

> **Important**
>
> No use acciones en un módulo Si no sabe qué
> que hacemos. Algunas acciones son irreversibles.. Las acciones
> puede ayudar a resolver problemas con uno o más módulos
> Onda Z.

> **Tip**
>
> El **Regeneración de detección de nodos** puede detectar el
> módulo para recuperar el último conjunto de parámetros. Esta acción
> se requiere cuando se le informa que una actualización de parámetros y
> o se requiere un comportamiento del módulo para una operación adecuada. El
> El regeneración de el detección de nodos implica un reinicio de la
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
> excluirlo, que el exclusión no tiene lugar, puede iniciar
> **Eliminar nodo fantasma** Una asistente realizará diferentes
> acciones para eliminar el llamado módulo fantasma. Esta acción implica
> reinicie el red y puede demorar varios minutos
> completado.

![node14](../ /images/ /node14.png)

Una vez iniciado, se recomienda cerrar el pantalel de configuración del
módulo y supervisar el eliminación del módulo a través de el pantalel de estado
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

inclusión / / exclusión
=====================

Cuando sale de fábrica, un módulo no pertenece a ninguna red Onda Z.

Modo de inclusión
--------------

El módulo debe unirse a una red Onda Z existente para comunicarse
con los otros módulos de esta red. Este proceso se llama
**Inclusion**. Los dispositivos también pueden salir de una red.
Este proceso se llama **Exclusion**. Ambos procesos se inician
por el controlador principal de el red Onda Z.

![addremove01](../ /images/ /addremove01.png)

Este botón le permite cambiar al modo de inclusión para agregar un módulo
a su red Onda Z.

Puede elegir el modo de inclusión después de hacer clic en el botón
**Inclusion**.

![addremove02](../ /images/ /addremove02.png)

Desde el aparición del Onda Z +, es posible asegurar el
intercambios entre el controlador y los nodos. Por lo tanto, se recomienda
hacer inclusiones en modo **Seguro**.

Sin embargo, Si no se puede incluir un módulo en modo seguro, por favor
incluirlo en modo **No es seguro**.

Una vez en modo de inclusión : Jeedom te dice.

\ [CONSEJO \] Una módulo 'no seguro' puede ordenar módulos 'no
seguro '. Una módulo 'no seguro' no puede ordenar un módulo
'seguro '. Una módulo 'seguro' puede ordenar módulos 'no
seguro 'siempre que el transmisor lo soporte.

![addremove03](../ /images/ /addremove03.png)

Una vez que se inicia el asistente, debe hacer lo mismo en su módulo
(consulte su documentación para cambiarlo al modo
inclusion).

> **Tip**
>
> Hasta que tenga el diadema, no está en modo
> inclusión.

Si vuelve a hacer clic en el botón, sale del modo de inclusión.

> **Tip**
>
> Se recomienda, antes de el inclusión de un nuevo módulo que sería
> "nuevo "en el mercado, para lanzar el pedido **Módulos de configuración** via
> pantalel de configuración del complemento. Esta acción se recuperará
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
> Tenga en cuenta que el interfaz móvil también le da acceso a el inclusión,
> el panel móvil debe haber sido activado.

> **Tip**
>
> Si el módulo ya pertenece a una red, siga el proceso
> exclusión antes de incluirlo en su red. De lo contrario, el inclusión de
> este módulo fallará. También se recomienda realizar un
> exclusión antes de el inclusión, incluso Si el producto es nuevo, fuera de
> carton.

> **Tip**
>
> Una vez que el módulo esté en su ubicación final, debe iniciar
> el acción se encarga de el red, para poder consultar todos los módulos de
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
> Hasta que tenga el diadema, no está en modo
> Exclusión.

Si vuelve a hacer clic en el botón, saldrá del modo de exclusión.

> **Tip**
>
> Tenga en cuenta que el interfaz móvil también le da acceso a el exclusión.

> **Tip**
>
> Una módulo no necesita ser excluido por el mismo controlador en
> que fue incluido previamente. De ahí el hecho de que recomendamos
> ejecutar una exclusión antes de cada inclusión.

Synchroniser
------------

![addremove06](../ /images/ /addremove06.png)

Botón para sincronizar los módulos de el red Onda Z con el
Equipo de Jeedom. Los módulos están asociados con el controlador principal.,
el equipo en Jeedom se crea automáticamente cuando es
inclusión. También se eliminan automáticamente cuando se excluyen.,
Si el opción **Eliminar automáticamente los dispositivos excluidos** est
activado.

Si ha incluido módulos sin Jeedom (requiere un dongle con
batería como el Aeon-labs Z-Stick GEN5), el sincronización será
necesario después de enchufar el llave, una vez que el demonio ha comenzado y
fonctionnel.

> **Tip**
>
> Si no tiene el imagen o Jeedom no ha reconocido su módulo,
> este botón se puede usar para corregir (siempre que el entrevista con el
> módulo está completo).

> **Tip**
>
> Si en su tabel de enrutamiento y / / o en el pantalel de estado de Z-Wave, usted
> tener uno o más módulos nombrados con sus **nombre genérico**, la
> el sincronización remediará esta situación.

El botón Sincronizar solo es visible en modo experto :
![addremove07](../ /images/ /addremove07.png)

Redesde Z-Wave
==============

![network01](../ /images/ /network01.png)

Aquí encontrará información general sobre su red Onda Z.

![network02](../ /images/ /network02.png)

Resumen
------

El primera pestaña le brinda el resumen básico de su red Z-Wave,
En particular, encontrará el estado de el red Onda Z y el número
artículos en el cola.

**Informations**

-   Proporciona información general sobre el red, el fecha de
    inicio, el tiempo requerido para obtener el red en un estado
    dice funcional.

-   El número total de nodos en el red, así como el número que duerme
    en el momento.

-   El intervalo de solicitud está asociado con el actualización manual. Él
    está preestablecido en el motor Onda Z a los 5 minutos.

-   Los vecinos del controlador..

**Etat**

![network03](../ /images/ /network03.png)

Una conjunto de información sobre el estado actual de el red, a saber :

-   Estado actual, tal vez **Conductor inicializado**, **Topología cargada**
    o **Ready**.

-   Coel saliente, indica el número de mensajes en coel en el
    controlador esperando ser enviado. Este valor es generalmente
    alto durante el inicio de el red cuando el estado todavía está en
    **Conductor inicializado**.

Una vez que el red ha alcanzado al menos **Topología cargada**, des
los mecanismos internos del servidor Onda Z forzarán actualizaciones a
valores, entonces es completamente normal ver el número de
mensajes Esto volverá rápidamente a 0.

> **Tip**
>
> Se dice que el red es funcional cuando alcanza el estado
> **Topología cargada**, es decir que el conjunto de nodos sectoriales
> han completado sus entrevistas. Dependiendo del número de módulos, el
> distribución de batería / / sector, el elección del dongle USB y el PC en el que
> activa el complemento Z-Wave, el red alcanzará este estado entre un
> y cinco minutos.

Una red **Ready**, significa que todos los nodos de sector y piel tienen
completaron su entrevista.

> **Tip**
>
> Dependiendo de los módulos que tenga, es posible que el red
> nunca alcanza el estado por sí mismo **Ready**. Los controles remotos,
> por ejemplo, no se despierte solo y no complementará
> nunca su entrevista. En este tipo de casos, el red está completamente
> operacional e incluso Si los controles remotos no han completado su
> entrevista, aseguran su funcionalidad dentro de el red.

**Capacidades**

Se utiliza para averiguar Si el controlador es un controlador principal o
secondaire.

**Sistema**

Muestra diversa información del sistema.

-   Información sobre el puerto USB utilizado.

-   Versión de el biblioteca OpenZwave

-   Versión de el biblioteca Python-OpenZwave

Actions
-------

![network05](../ /images/ /network05.png)

Aquí encontrará todas las acciones posibles para todos sus
Red Onda Z. Cada acción va acompañada de una breve descripción..

> **Important**
>
> Algunas acciones son realmente arriesgadas o incluso irreversibles, el equipo
> Jeedom no se hace responsable en caso de mal
> manipulación.

> **Important**
>
> Algunos módulos requieren inclusión en modo seguro, por
> ejemplo para cerraduras de puertas. El inclusión segura debe ser
> lanzado a través de el acción de esta pantalla.

> **Tip**
>
> Si no se puede iniciar una acción, se desactivará hasta
> cuando se puede ejecutar de nuevo.

Statistiques
------------

![network06](../ /images/ /network06.png)

Aquí encontrará estadísticas generales para todos sus
Red Onda Z.

Gráfico de red
-------------------

![network07](../ /images/ /network07.png)

Esta pestaña le dará una representación gráfica de los diferentes
enlaces entre nodos.

Explicación de el leyenda del color. :

-   **Noir** : El controlador principal, generalmente representado
    como Jeedom.

-   **Vert** : Comunicación directa con el controlador, ideal.

-   **Blue** : Para los controladores, como los controles remotos, son
    asociado con el controlador primario, pero no tiene vecino.

-   **Jaune** : Todos los caminos tienen más de un salto antes de llegar.
    al controlador.

-   **Gris** : El entrevista aún no se ha completado, los enlaces serán
    realmente conocido una vez que se completa el entrevista.

-   **Rouge** : presuntamente muerto, o sin vecino, no participa / / ya no participa en
    malel de red.

> **Tip**
>
> Solo el equipo activo se mostrará en el gráfico de red.

El red Onda Z consta de tres tipos diferentes de nodos con
tres funciones principales.

El principal diferencia entre los tres tipos de nodos es su
conocimiento de el tabel de enrutamiento de el red y de allí en adelante
capacidad de enviar mensajes a el red:

Tabel de enrutamiento
----------------

Cada nodo puede determinar qué otros nodos están en
Comunicación directa. Estos nodos se llaman vecinos. A lo largo de
inclusión y / / o posterior solicitud, el nodo puede
informar al controlador de el lista de vecinos. Gracias a estos
información, el controlador puede construir una tabel que tiene
toda el información sobre posibles vías de comunicación en
una red.

![network08](../ /images/ /network08.png)

Las filas de el tabel contienen los nodos de origen y las columnas.
contener nodos de destino. Consulte el leyenda para
entender los colores de las celdas que indican los enlaces entre dos
nudos.

Explicación de el leyenda del color. :

-   **Vert** : Comunicación directa con el controlador, ideal.

-   **Blue** : Al menos 2 rutas con un salto.

-   **Jaune** : Menos de 2 rutas con un salto.

-   **Gris** : El entrevista aún no se ha completado, en realidad será
    actualizado después de completar el entrevista.

-   **Orange** : Todos los caminos tienen más de un salto.. Puede causar
    latencias.

> **Tip**
>
> Solo el equipo activo se mostrará en el gráfico de red.

> **Important**
>
> Una módulo presunto muerto, no participa / / ya no participa en el red de el red.
> Se marcará aquí con un signo de exclamación rojo en un triángulo..

> **Tip**
>
> Puede iniciar manualmente el actualización de vecinos, por módulo
> o para toda el red utilizando los botones disponibles en el
> Tabel de enrutamiento.

Santé
=====

![health01](../ /images/ /health01.png)

Esta ventana resume el estado de su red Onda Z :

![health02](../ /images/ /health02.png)

Tienes aquien :

-   **Module** : el nombre de su módulo, un clic en él le permite
    acceder directamente.

-   **ID** : Identificación de su módulo en el red Onda Z.

-   **Notification** : último tipo de intercambio entre el módulo y el
    Controlador

-   **Groupe** : indica Si el configuración del grupo está bien
    (controlador al menos en un grupo). Si no tienes nada es porque
    el módulo no admite el noción de grupo, esto es normal

-   **Constructeur** : indica Si se está recuperando información
    el identificación del módulo está bien

-   **Voisin** : indica Si se ha recuperado el lista de vecinos

-   **Statut** : Indica el estado de el entrevista (etapa de consulta) del
    module

-   **Batterie** : nivel de batería del módulo (un enchufe de red
    indica que el módulo se alimenta de el red eléctrica).

-   **Hora de despertarse** : para módulos de batería, da la
    frecuencia en segundos de los instantes cuando el módulo
    despertarse automáticamente.

-   **Paquete total** : muestra el número total de paquetes recibidos o
    enviado con éxito al módulo.

-   **%OK** : muestra el porcentaje de paquetes enviados / / recibidos
    con éxito.

-   **Temporisation** : muestra el retraso promedio de envío de paquetes en ms.

-   **Última notificación** : Fecha de el última notificación recibida de
    módulo y el próxima hora de activación programada para módulos
    quien duerme.

    -   También permite informar Si el nodo aún no está
        desperté una vez desde el lanzamiento del demonio.

    -   E indica Si un nodo no se ha despertado como se esperaba.

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
> El comando De ping se puede usar Si se presume que el módulo está muerto
> "MUERTE "para confirmar Si este es realmente el caso.

> **Tip**
>
> Los módulos dormidos solo responderán a De ping cuando
> siguiente despertar.

> **Tip**
>
> El notificación de tiempo de espera no necesariamente significa un problema
> con el módulo. De ping y en el mayoría de los casos el módulo
> responderá con una notificación **NoOperation** que confirma un regreso
> De ping fructífero.

> **Tip**
>
> Tiempo de espera y% Bueno en los nodos con baterías antes de el finalización
> de su entrevista no es significativa. De hecho, el nudo no se va
> responder las preguntas del controlador sobre el hecho de que está dormido
> profundo.

> **Tip**
>
> El servidor Onda Z se encarga automáticamente de iniciar pruebas en el
> Módulos de tiempo de espera después de 15 minutos

> **Tip**
>
> El servidor Onda Z intenta automáticamente remontar módulos
> presunto muerto.

> **Tip**
>
> Se enviará una alerta a Jeedom Si se presume que el módulo está muerto. Vosotras
> puede activar una notificación para estar más informado
> posible rápidamente. Vea el configuración de Mensajes en el pantalla
> Configuración de Jeedom.

![health03](../ /images/ /health03.png)

> **Tip**
>
> Si en su tabel de enrutamiento y / / o en el pantalel de estado de Onda Z usted
> tener uno o más módulos nombrados con sus **nombre genérico**, la
> el sincronización remediará esta situación.

> **Tip**
>
> Si en su tabel de enrutamiento y / / o en el pantalel de estado de Onda Z usted
> tener uno o más módulos llamados **Unknown**, eso significa que
> el entrevista del módulo no se completó con éxito. Teneis
> probablemente un **NOK** en el columna del constructor. Abre el detalle
> del módulo (s), para probar las soluciones sugeridas.
> (Consulte el sección Solución de problemas y diagnóstico, a continuación)

Estado de el entrevista
---------------------

Paso de entrevistar un módulo después de iniciar el demonio.

-   **None** Inicialización del proceso de búsqueda de nodos..

-   **ProtocolInfo** Recupere el información del protocolo, Si esto
    nodo está escuchando (oyente), su velocidad máxima y sus clases
    de periféricos.

-   **Probe** Haga ping al módulo para ver Si está despierto.

-   **WakeUp** Inicie el proceso de activación, Si es un
    nudo durmiente.

-   **ManufacturerSpecific1** Recupere el nombre del fabricante y
    productos ids Si ProtocolInformación lo permite.

-   **NodeInfo** Recuperar información sobre el gestión de clases.
    comandos soportados.

-   **NodePlusInfo** Recupere información de ZWave + sobre soporte
    clases de comando compatibles.

-   **SecurityReport** Recupere el lista de clases de orden que
    requieren seguridad.

-   **ManufacturerSpecific2** Recupere el nombre del fabricante y el
    identificadores de producto.

-   **Versions** Recuperar información de el versión.

-   **Instances** Recuperar información de clase de varias instancias
    de encargo.

-   **Static** Recuperar información estática (no cambia).

-   **CacheLoad** Haga ping al módulo durante el reinicio con el caché de configuración
    del dispositivo.

-   **Associations** Recuperar información sobre asociaciones.

-   **Neighbors** Recuperar el lista de nodos vecinos..

-   **Session** Recuperar información de el sesión (rara vez cambia).

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

El parte de respaldo le permitirá administrar los respaldos de el topología.
de tu red. Este es su archivo zwcfgxxx.xml, es el
último estado conocido de su red, es una forma de caché de su
red Desde esta pantalel puedesde :

-   Inicie una copia de seguridad (se realiza una copia de seguridad en cada parada reiniciando el
    red y durante operaciones críticas). Las últimas 12 copias de seguridad
    se mantienen

-   Restaurar una copia de seguridad (seleccionándoel de el lista
    justo arriba)

-   Eliminar una copia de seguridad

![backup01](../ /images/ /backup01.png)

Actualizar OpenZWave
=======================

Después de una actualización del complemento Z-Wave, es posible que Jeedom
Solicite actualizar las dependencias de Onda Z. Una NBueno a nivel de
se mostrarán las dependencias:

![update01](../ /images/ /update01.png)

> **Tip**
>
> No se debe hacer una actualización de las dependencias con cada actualización
> Plugin.

Jeedom debería lanzar el actualización de dependencia por sí solo Si el
el complemento considera que son **NOK**. Esta validación se lleva a cabo en
después de 5 minutos.

El duración de esta operación puede variar según su sistema
(hasta más de 1 hora con frambuesa pi)

Una vez que se complete el actualización de dependencias, el demonio se reiniciará
automáticamente tras el validación de Jeedom. Esta validación es
hecho después de 5 minutos.

> **Tip**
>
> En el caso de que no ocurra el actualización de dependencias
> no completo, por favor consulte el registro **Openzwave\_update** qui
> debería informarle sobre el problema.

Lista de módulos compatibles.
============================

Encontrará el lista de módulos compatibles.
[aquí](https:/ // /jeedom.fr/ /doc/ /documentation/ /zwave-modules/ /fr_FR/ /doc-zwave-modules-equipement.compatible.html)

Solución de problemas y diagnóstico
=======================

Mi módulo no se detecta o no proporciona sus identificadores de producto y tipo
-------------------------------------------------------------------------------

![troubleshooting01](../ /images/ /troubleshooting01.png)

Inicie el regeneración de el detección de nodos desde el pestaña Acciones
del módulo.

Si tiene varios módulos en este escenario, inicie **Actualizar
detección de nodos desconocidos** desde el pantalel **Red Zwave** onglet
**Actions**.

Mi módulo se presume muerto por el controlador Dead
--------------------------------------------------

![troubleshooting02](../ /images/ /troubleshooting02.png)

Si el módulo todavía está enchufado y accesible, siga las soluciones
propuesto en el pantalel del módulo.

Si el módulo ha sido cancelado o está realmente defectuoso, usted
puede excluirlo de el red usando **eliminar el nodo por error**
a través de el pestaña **Actions**.

Si el módulo ha sido reparado y un nuevo módulo
se ha entregado el reemplazo que puede lanzar **Reemplazar nodo fallido**
a través de el pestaña **Actions**, el controlador activa el inclusión, entonces usted
debe proceder con el inclusión en el módulo. El identificación del antiguo módulo será
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

El elección de las opciones depende del fabricante..

Por lo tanto, debe tomarse el tiempo para revisar todos sus
interruptores / / atenuadores antes de configurar un escenario Si no
no solo luces piloto.

Mi módulo no tiene un comando de escena o botón
----------------------------------------------

![troubleshooting05](../ /images/ /troubleshooting05.png)

Puede agregar el comando en el pantalel de asignación de comandos.

Esta es una orden **Info** en CC **0x2b** Instancia **0** commande
**datos \ [0 \]. val**

El modo de escena debe activarse en el configuración del módulo. Ver la
documentación de su módulo para más detalles.

Forzar valores de actualización
-------------------------------------

Es posible forzar a petición el actualización de los valores
una instancia para un comando de clase específico.

Es posible hacerlo a través de una solicitud http o crear un pedido
en el pantalel de mapeo de equipos.

![troubleshooting06](../ /images/ /troubleshooting06.png)

Esta es una orden **Action** elige el **CC** deseado para un
**Instance** dado con el comando **datos \ [0 \]. ForceRefresh ()**

Se colocarán todos los índices de instancia para este comando de clase
al día. Los nudos en las baterías esperarán su próximo despertar antes de
actualizar su valor.

También puede usar por script emitiendo una solicitud http para
Servidor REST Onda Z.

Reemplace ip\_jeedom, node\_id, instancia\_id, cc\_id e index

http:/ // /token:\#APIKEY\#@ip\_jeedom:8083/ /ZWaveAPI/ /Run/ /devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

El acceso a el API REST ha cambiado, ver detalles
[aquí](./ /restapi.asciidoc).

Transfiera los módulos a un nuevo controlador
------------------------------------------------

Por diferentes razones, puede que tenga que transferir
todos sus módulos en un nuevo controlador principal.

Decidesde irte de **raZberry** un **Z-Stick Gen5** o porque
eso, tienes que realizar un **Reset** completo del controlador principal.

Aquí hay diferentes pasos para llegar sin perder sus escenarios.,
widgets de valor e historia:

-   1 \) Hacer una copia de seguridad de Jeedom.

-   2 \) Recuerde anotar (captura de pantalla) los valores de sus parámetros para cada
    módulo, se perderán debido a el exclusión.

-   3 \) En el configuración de Z-Wave, desmarque "Eliminar
    excluye automáticamente los dispositivos "y realiza una copia de seguridad.
    reinicios de red.

-   4a) En el caso de un **Reset**, Restablecer el controlador
    principal y reinicie el complemento.

-   4b) Para un nuevo controlador, detenga Jeedom, desconecte el viejo
    controlador y enchufe el nuevo. Inicie Jeedom.

-   5 \) Para cada dispositivo Z-Wave, cambie el Identificación de ZWave a **0**.

-   6 \) Abra 2 páginas del complemento Onda Z en diferentes pestañas.

-   7 \) (a través de el primera pestaña) Vaya a el página de configuración de un
    módulo que desea incluir en el nuevo controlador.

-   8 \) (a través de el segunda pestaña) Excluir e incluir
    del módulo. Se crearán nuevos equipos..

-   9 \) Copie el Identificación de Onda Z del nuevo equipo, luego elimine
    este equipo.

-   10 \) Regrese a el pestaña del módulo anterior (primera pestaña) y luego pegue
    el nueva identificación en lugar de el identificación anterior.

-   11 \) Los parámetros ZWave se perdieron durante el exclusión / / inclusión,
    recuerde restablecer su configuración específica Si no está utilizando el
    valores por defecto.

-   11 \) Repita los pasos 7 a 11 para cada módulo a transferir.

-   12 \) Al final, ya no debería tener equipo en Identificación 0.

-   13 \) Verifique que todos los módulos estén correctamente nombrados en el pantalel de
    salud Onda Z. Inicie el sincronización Si este no es el caso.

Reemplace un módulo defectuoso
------------------------------

Cómo rehacer el inclusión de un módulo defectuoso sin perder su
escenarios de valor, widgets e historia

Si se supone que el módulo está "Muerto" :

-   Tenga en cuenta (captura de pantalla) los valores de sus parámetros, se perderán
    siguiente inclusión.

-   Vaya a el pestaña de acciones del módulo y ejecute el comando
    "Reemplazar nodo fallido".

-   El controlador está en modo de inclusión, proceda con el inclusión de acuerdo con
    Documentación del módulo.

-   Restablece tus parámetros específicos.

Si no se presume que el módulo está "Muerto" pero aún está accesible:

-   En el configuración de ZWave, desmarque "Eliminar
    dispositivos excluidos automáticamente".

-   Tenga en cuenta (captura de pantalla) los valores de sus parámetros, se perderán
    siguiente inclusión.

-   Excluir el módulo defectuoso..

-   Vaya a el página de configuración del módulo defectuoso..

-   Abra el página del complemento ZWave en una pestaña nueva.

-   Incluir el módulo.

-   Copie el Identificación del nuevo módulo, luego elimine este equipo.

-   Regrese a el pestaña del módulo anterior y luego pegue el nueva Identificación en
    el lugar de el identificación anterior.

-   Restablece tus parámetros específicos.

Eliminación del nodo fantasma
----------------------------

Si ha perdido toda comunicación con un módulo alimentado por batería y
desea excluirlo de el red, es posible que el exclusión
no tiene éxito o el nodo permanece presente en su red.

El asistente automático de nodo fantasma está disponible.

-   Vaya a el pestaña de acciones del módulo para eliminar.

-   Probablemente tendrá un estado **CacheLoad**.

-   Comando de inicio **Eliminar nodo fantasma**.

-   El red Onda Z se detiene. El asistente automático modifica el
    Expediente **zwcfg** para eliminar el CC Despertador del módulo. El
    reinicios de red.

-   Cerrar el pantalel del módulo.

-   Abra el pantalel Onda Z Health.

-   Espere a que se complete el ciclo de inicio (topología cargada).

-   El módulo normalmente se marcará como presunto muerto.

-   Al minuto siguiente, verá que el nodo desaparece de el pantalla.
    de salud.

-   Si en el configuración de Z-Wave, ha desmarcado el opción
    "Eliminar automáticamente los dispositivos excluidos ", deberá
    eliminar manualmente el equipo correspondiente.

Este asistente solo está disponible para módulos de batería.

Acciones posteriores a el inclusión
----------------------

Se recomienda realizar el inclusión al menos a 1M del controlador
principal, pero no será el posición final de su nuevo módulo.
Aquí hay algunas buenas prácticas a seguir luego de el inclusión de un nuevo
módulo en su red.

Una vez que se completa el inclusión, una serie de
parámetros de nuestro nuevo módulo para aprovecharlo al máximo. Recordatorio,
Los módulos, después de el inclusión, tienen el configuración predeterminada de
constructor Disfruta estar al lado del controlador y el interfaz
Jeedom para configurar correctamente su nuevo módulo. También será más
simple para activar el módulo para ver el efecto inmediato del cambio.
Algunos módulos tienen documentación específica de Jeedom para usted
ayuda con diferentes parámetros y valores recomendados.

Pruebe su módulo, valide los comentarios de información, los comentarios de estado
y posibles acciones en el caso de un actuador.

Durante el entrevista, su nuevo módulo buscó a sus vecinos..
Sin embargo, los módulos en su red aún no conocen su
nuevo módulo.

Mueva su módulo a su ubicación final. Comience el actualización
de sus vecinos y despertarlo nuevamente.

![troubleshooting07](../ /images/ /troubleshooting07.png)

Vemos que ve un cierto número de vecinos pero que el
los vecinos no lo ven.

Para remediar esta situación, se deben tomar medidas para tratar el
red, para pedir a todos los módulos que encuentren a sus vecinos.

Esta acción puede tomar 24 horas antes de terminar, sus módulos
con batería realizará el acción solo el próxima vez que se despierten.

![troubleshooting08](../ /images/ /troubleshooting08.png)

El opción de tratar el red dos veces por semana le permite hacer esto
proceso sin acción de su parte, es útil al configurar
coloca nuevos módulos y / / o cuando se mueven.

No hay comentarios de el condición de el batería
-------------------------------

Los módulos Onda Z rara vez envían el estado de su batería al
controlador Algunos lo harán en el inclusión solo cuando
esto alcanza el 20% u otro valor umbral crítico.

Para ayudarlo a controlar mejor el estado de sus baterías, el pantalel Baterías
en el menú Análisis le da una visión general del estado de su
baterías Una mecanismo de notificación de batería baja también es
disponible.

El valor devuelto desde el pantalel Baterías es el último conocido en el
cache.

Todas las noches, el complemento Onda Z le pide a cada módulo que se actualice
Valor de el batería. El próxima vez que se despierte, el módulo envía el valor a
Jeedom para ser agregado al caché. Por lo general, tienes que esperar hasta
al menos 24 horas antes de obtener un valor en el pantalel Baterías.

> **Tip**
>
> Por supuesto, es posible actualizar manualmente el valor
> Batería a través de el pestaña Valores del módulo y luego espere el siguiente
> alarma o despertar manualmente el módulo para obtener un
> recuperación inmediata. El intervalo de activación del módulo
> se define en el pestaña Sistema del módulo. Para optimizar el vida de
> sus baterías, se recomienda espaciar este retraso tanto como sea posible. Por 4h,
> aplicar 14400, 12h 43200. Algunos módulos deben
> escuche regularmente mensajes del controlador como
> Termostatos. En este caso, es necesario pensar en 15 min o 900. Cada
> el módulo es diferente, por lo que no existe una regel exacta, este es el caso
> por caso y por experiencia.

> **Tip**
>
> El descarga de una batería no es lineal, algunos módulos lo harán
> mostrar un gran porcentaje de pérdida en los primeros días de apuesta
> en servicio, luego no se mueva durante semanas para vaciar
> rápidamente una vez pasado el 20%.

El controlador se está inicializando
----------------------------------------

Cuando inicias el demonio Z-Wave, Si intentas iniciar
inmediatamente una inclusión / / exclusión, corre el riesgo de obtener esto
message: \* "El controlador se está inicializando, por favor
intente nuevamente en unos minutos"

> **Tip**
>
> Después de que se inicia el demonio, el controlador cambia a todos los
> módulos para repetir su entrevista. Este comportamiento es
> completamente normal en OpenZWave.

Sin embargo, Si después de varios minutos (más de 10 minutos), tiene
Todavía este mensaje, ya no es normal.

Tienes que probar los diferentes pasos:

-   Asegúrese de que las luces de el pantalel de salud Jeedom sean verdes.

-   Asegúrese de que el configuración del complemento esté en orden.

-   Asegúrese de haber seleccionado el puerto correcto para
    Tecel ZWave.

-   Asegúrese de que el configuración de su red Jeedom sea correcta.
    (Atención Si ha realizado una restauración desde una instalación de bricolaje a
    imagen oficial, el sufijo / / libertad no debe incluirse)

-   Mire el registro del complemento para ver Si hay un error
    no arriba.

-   Mira el **Console** Complemento ZWave, para ver Si hay un error
    no subió.

-   Lanzar el demonio por **Debug** mira de nuevo a el **Console** et
    registros de complementos.

-   Reiniciar completamente Jeedom.

-   Asegúrese de tener un controlador Z-Wave, el
    Razberry a menudo se confunde con EnOcean (error durante
    el orden).

Ahora debemos comenzar las pruebas de hardware:

-   El Razberry está bien conectado al puerto GPIO.

-   El alimentación USB es suficiente.

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

El coel de mensajes del controlador puede estar llena.
Vea el pantalel de el red Onda Z Si el número de mensajes pendientes no
qu'augmenter.

En este caso, debe reiniciar el Demon Onda Z.

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

    sudo rm / / var / / lib / / dpkg / / info / / $ mercurial * -f
    sudo apt-gy install mercurial

-   Las adicciones parecen bloqueadas en un 75%

Con un 75%, este es el comienzo de el compilación de el biblioteca openzwave también
envoltura de pitón openzwave. Este paso es muy largo, podemos
sin embargo, consulte el progreso a través de el vista de registro de actualización. Él
así que sé paciente.

-   Error al compilar el biblioteca openzwave

        arm-linux-gnueabihf-gcc: error interno del compilador: Asesinado (programa cc1plus)
        Por favor envíe un informe de error completo,
        con fuente preprocesada Si corresponde.
        Ver <file:/ // // /usr/ /share/ /doc/ /gcc-4.9/ /README.Errores> para instrucciones.
        error: el comando 'arm-linux-gnueabihf-gcc' falló con el estado de salida 4
        Makefile:266: el receta para el 'compilación' objetivo falló
        make: *** [build] Error 1

Este error puede ocurrir debido a el falta de memoria RAM durante el
compilation.

Desde el interfaz de usuario de Jeedom, inicie el compilación de dependencias.

Una vez lanzado, en ssh, detenga estos procesos (los consumidores en
memoria) :

    sudo systemctl Detener cron
    sudo systemctl Detener apache2
    sudo systemctl Detener mysql

Para seguir el progreso de el compilación, adaptamos el
archivo de registro de openzwave\_update.

    tail -f / / var / / www / / html / / log / / openzwave_update

Cuando el compilación esté completa y sin error, reinicie el
servicios que detuvo

sudo systemctl comienzo cron sudo systemctl comienzo apache2 sudo systemctl
iniciar mysql

> **Tip**
>
> Si todavía está en nginx, deberá reemplazar **apache2** par
> **nginx** en pedidos **stop** / / **start**. El archivo de registro
> openzwave\_update estará en el carpeta:
> / / usr / / share / / Nginx / / www / / jeedom / / log .

Usando el tarjeta Razberry en una Raspberry Pi 3
------------------------------------------------------

Para usar un controlador Razberry en una Raspberry Pi 3, el
El controlador Bluetooth interno de Raspberry debe estar deshabilitado.

Agrega esta línea:

    dtoverlay = pi3-miniuart-bt

Al final del archivo:

    / /boot/ /config.txt

Luego reinicie su Frambuesa.

API HTTP
========

El complemento Onda Z proporciona desarrolladores y usuarios
Una API completa para operar el red Onda Z mediante solicitud
HTTP.

Puede utilizar todos los métodos expuestos por el
Servidor REST del demonio Onda Z.

El sintaxis para llamar a las rutas es de esta forma:

URL =
[http:/ // /token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/ /\#ROUTE\#](http:/ // /token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/ /#ROUTE#)

-   \#API\_KEY \# corresponde a su clave API, específica de
    su instalación. Para encontrarlo, ve al menú «
    Principal », puis « Administration » y « Configuración », en activant
    Modo experto, verá una línea de clave API.

-   \#IP\_JEEDOM \# corresponde a su URL de acceso de Jeedom.

-   \#PORTDEMON \# corresponde al número de puerto especificado en el página
    configuración del complemento Z-Wave, por defecto: 8083.

-   \#ROUTE \# corresponde a el ruta en el servidor REST que se ejecutará.

Para conocer todas las rutas, consulte
[Github](https:/ // /github.com/ /jeedom/ /plugin-openzwave) del complemento Onda Z.

Example: Para hacer ping al id del nodo 2

URL =
http:/ // /token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ /ZWaveAPI/ /Run/ /devices\[2\].TestNode()

# FAQ

> **Me sale el error "No hay suficiente espacio en el búfer de flujo"**
>
> Desafortunadamente, este error es hardware, no hay nada que podamos hacer y estamos buscando por el momento cómo forzar un reinicio del demonio en el caso de este error (pero a menudo también es necesario desconectar el clave durante 5 minutos para que vuelva a comenzar)
