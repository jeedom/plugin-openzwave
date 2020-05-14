# Complemento OpenZWave

Este complemento permite la explotación de módulos Z-Wave a través de la biblioteca OpenZwave.

# Introduction

Z-Wave se comunica utilizando tecnología de radio de baja potencia en la banda de frecuencia de 868.42 MHz. Está específicamente diseñado para aplicaciones de domótica. El protocolo de radio Z-Wave está optimizado para intercambios de bajo ancho de banda (entre 9 y 40 kbit / s) entre dispositivos con batería o alimentados por la red eléctrica.

Z-Wave opera en el rango de frecuencia de sub gigahercios, según las regiones (868 MHz en Europa, 908 MHz en los EE. UU., Y otras frecuencias según las bandas ISM de las regiones). El alcance teórico es de unos 30 metros en interiores y 100 metros en exteriores. La red Z-Wave utiliza tecnología de malla para aumentar el alcance y la confiabilidad. Z-Wave está diseñado para integrarse fácilmente en productos electrónicos de baja potencia, incluidos dispositivos que funcionan con baterías, como controles remotos, detectores de humo y sensores de seguridad.

El Z-Wave +, trae ciertas mejoras que incluyen un mejor alcance y mejora la vida útil de las baterías, entre otros. Compatibilidad con versiones anteriores de Z-Wave.

## Distancias a respetar con otras fuentes de señal inalámbrica

Los receptores de radio deben colocarse a una distancia mínima de 50 cm de otras fuentes de radio.

Ejemplos de fuentes de radio:

-   Ordinateurs
-   Aparatos de microondas
-   Transformadores electrónicos
-   equipo de audio y video
-   Dispositivos de preenganche para lámparas fluorescentes

> **Punta**
>
> Si tiene un controlador USB (Z-Stick), se recomienda alejarlo de la caja usando un simple cable de extensión USB de 1M, por ejemplo.

La distancia entre otros transmisores inalámbricos, como teléfonos inalámbricos o transmisiones de audio por radio, debe ser de al menos 3 metros. Se deben considerar las siguientes fuentes de radio :

-   Interferencia por interruptor de motores eléctricos
-   Interferencia de dispositivos eléctricos defectuosos
-   Interferencia de equipos de soldadura HF
-   dispositivos de tratamiento médico

## Espesor de pared efectivo

Las ubicaciones de los módulos deben elegirse de tal manera que la línea de conexión directa funcione solo por una distancia muy corta a través del material (una pared), para evitar la atenuación tanto como sea posible.

![introduction01](../images/introduction01.png)

Las partes metálicas del edificio o los muebles pueden bloquear las ondas electromagnéticas.

## Malla y Enrutamiento

Los nodos principales de Z-Wave pueden transmitir y repetir mensajes que no están dentro del alcance directo del controlador. Esto permite una mayor flexibilidad de comunicación, incluso si no hay una conexión inalámbrica directa o si una conexión no está disponible temporalmente, debido a un cambio en la habitación o el edificio.

![introduction02](../images/introduction02.png)

El controlador **Id 1** puede comunicarse directamente con los nodos 2, 3 y 4. El nodo 6 está fuera de su alcance de radio, sin embargo, está en el área de cobertura de radio del nodo 2. Por lo tanto, el controlador puede comunicarse con el nodo 6 a través del nodo 2. De esta manera, la ruta del controlador a través del nodo 2 al nodo 6 se denomina ruta. En caso de que la comunicación directa entre el nodo 1 y el nodo 2 esté bloqueada, existe otra opción para comunicarse con el nodo 6, utilizando el nodo 3 como otro repetidor de señal.

Es obvio que cuantos más nodos de sector tenga, más aumentan las opciones de enrutamiento y más aumenta la estabilidad de la red. El protocolo Z-Wave es capaz de enrutar mensajes a través de hasta cuatro nodos repetidos. Es un compromiso entre el tamaño de la red, la estabilidad y la duración máxima de un mensaje.

> **Punta**
>
> Se recomienda encarecidamente al comienzo de la instalación tener una relación entre los nodos del sector y el nodo en baterías de 2/3, para tener una buena red de malla. Favorece los micromódulos sobre los enchufes inteligentes. Los micro módulos estarán en una ubicación final y no se desconectarán, generalmente también tienen un mejor rango. Un buen comienzo es la iluminación de las áreas comunes. Le permitirá distribuir adecuadamente los módulos del sector en ubicaciones estratégicas de su hogar. Luego puede agregar tantos módulos en la pila como desee, si sus rutas básicas son buenas.

> **Punta**
>
> El **Gráfico de red** así como el **Tabla de enrutamiento** le permite ver la calidad de su red.

> **Punta**
>
> Hay módulos repetidores para llenar áreas donde ningún módulo sectorial es útil.

## Propiedades de los dispositivos Z-Wave

|  | Vecinos | Camino | Posibles funciones |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controlador | Conoce a todos los vecinos | Tiene acceso a la tabla de enrutamiento completa | Puede comunicarse con todos los dispositivos en la red, si existe un canal |
| Esclavo | Conoce a todos los vecinos | No tiene información sobre la tabla de enrutamiento | No se puede responder al nodo que recibió el mensaje. Por lo tanto, no se pueden enviar mensajes no solicitados |
| Esclavos enrutamiento | Conoce a todos sus vecinos | Con conocimiento parcial de la tabla de enrutamiento | Puede responder al nodo desde el que recibió el mensaje y puede enviar mensajes no solicitados a varios nodos |

En resumen:

-   Cada dispositivo Z-Wave puede recibir y confirmar mensajes
-   Les contrôleurs peuvent envoyer des messages à tous les nœuds du réseau, sollicités o non « El maître peut parler quand il veut y à qui il veut »
-   Les esclaves ne peuvent pas envoyer des messages non sollicités, mais seulement une réponse aux demandes «L'esclave ne parle que si on le lui demande »
-   Les esclaves de routage peuvent répondre à des demandes y ils sont autorisés à envoyer des messages non sollicités à certains nœuds que le contrôleur a prédéfini « L'esclave est toujours un esclave, mais sur autorisation, il peut parler »

# Configuración del plugin

Después de descargar el complemento, solo necesita activarlo y configurarlo.

![configuration01](../images/configuration01.png)

Una vez activado, el demonio debería lanzar. El complemento está preconfigurado con valores predeterminados; normalmente no tienes nada más que hacer. Sin embargo, puedes cambiar la configuración.

## Dependencias

Esta parte le permite validar e instalar las dependencias necesarias para el correcto funcionamiento del complemento Zwave (tanto local como remotamente, aquí localmente) ![configuración02](../images/configuration02.png)

-   Un estatuto **Bueno** confirma que se cumplen las dependencias.
-   Si el estado es **NOK**, las dependencias deberán reinstalarse con el botón ![configuración03](../images/configuration03.png)

> **Punta**
>
> La actualización de dependencias puede demorar más de 20 minutos dependiendo de su hardware. El progreso se muestra en tiempo real y un registro **Openzwave\_update** es accesible.

> **Importante**
>
> La actualización de dependencias normalmente se realizará solo si el estado es **NOK**, pero es posible, sin embargo, resolver ciertos problemas, ser llamado para rehacer la instalación de dependencias.

> **Punta**
>
> Si está en modo remoto, las dependencias del demonio local pueden ser NOK, esto es completamente normal.

## Demonio

Esta parte le permite validar el estado actual de los demonios y configurar la gestión automática de estos. ![configuración04](../images/configuration04.png) El demonio local y todos los demonios deportados se mostrarán con su información diferente

-   El **Estado** indica que el demonio se está ejecutando actualmente.
-   El **Configuración** indica si la configuración del daemon es válida.
-   El botón **(Re)Iniciar** permite forzar el reinicio del complemento, en modo normal o iniciarlo por primera vez.
-   El botón **Detenido**, visible solo si la gestión automática está desactivada, obliga al demonio a detenerse.
-   El **Gestión automática** permite a Jeedom iniciar automáticamente el demonio cuando se inicia Jeedom, así como reiniciarlo en caso de un problema.
-   El **Última ejecución** es como su nombre indica la fecha del último lanzamiento conocido del demonio.

## Log

Esta parte le permite elegir el nivel de registro y consultar su contenido.

![configuration05](../images/configuration05.png)

Seleccione el nivel y luego guarde, el demonio se reiniciará con las instrucciones y los rastros seleccionados.

El nivel **Depurar** o **Información** puede ser útil para entender por qué el demonio planta o no sube un valor.

> **Importante**
>
> En modo **Depurar** el demonio es muy detallado, se recomienda usar este modo solo si tiene que diagnosticar un problema en particular. No se recomienda dejar que el demonio corra mientras **Depurar** permanentemente, si usamos un **Tarjeta SD**. Una vez finalizada la depuración, no olvide volver a un nivel inferior como el nivel **Error** que solo vuelve a posibles errores.

## Configuration

Esta parte le permite configurar los parámetros generales del complemento ![configuración06](../images/configuration06.png)

-   **Principal** :
    -   **Borrar automatiquement les périphériques exclus** :La opción Sí le permite eliminar dispositivos excluidos de la red Z-Wave. La opción No le permite mantener el equipo en Jeedom incluso si ha sido excluido de la red. El equipo
        luego tendrá que eliminarse manualmente o reutilizarse asignándole una nueva ID de Z-Wave si está migrando desde el controlador principal.
    -   **Aplicar el conjunto de configuración recomendado para su inclusión** : opción de aplicar directamente el conjunto de configuración recomendado por el equipo de Jeedom para su inclusión (recomendado)
    -   **Desactivar la actualización en segundo plano de las unidades** : No solicite la actualización de unidades en segundo plano.
    -   **Ciclo (s)** : permite definir la frecuencia de los ascensores a la libertad.
    -   **Puerto de llave Z-Wave** : el puerto USB en el que está conectada su interfaz Z-Wave. Si usa Razberry, tiene, dependiendo de su arquitectura (RPI o Jeedomboard), las 2 posibilidades al final de la lista.
    -   **Puerto del servidor** (modificación peligrosa, debe tener el mismo valor en todos los Jeedoms remotos Z-Wave) : permite modificar el puerto de comunicación interna del demonio.
    -   **Copias de seguridad** : le permite administrar copias de seguridad del archivo de topología de red (ver más abajo)
    -   **Módulos de configuración** : permite recuperar, manualmente, los archivos de configuración de OpenZWave con los parámetros de los módulos, así como la definición de los comandos de los módulos para sus usos.

        > **Punta**
        >
        > Las configuraciones de los módulos se recuperan automáticamente todas las noches.

        > **Punta**
        >
        > Reiniciar el demonio después de actualizar las configuraciones del módulo es inútil.

        > **Importante**
        >
        > Si tiene un módulo no reconocido y se acaba de aplicar una actualización de configuración, puede iniciar manualmente la recuperación de las configuraciones del módulo.

Una vez que se han recuperado las configuraciones, dependiendo de los cambios realizados:

-   Para un nuevo módulo sin configuración o control : excluir y volver a incluir el módulo.
-   Para un módulo para el que solo se han actualizado los parámetros : iniciar la regeneración de la detección de nodos, a través de la pestaña Acciones del módulo (el complemento debe reiniciarse).
-   Pour un module dont le « mapping » de commandes a été corrigé : la lupa en los controles, ver abajo.

    > **Punta**
    >
    > En caso de duda, se recomienda excluir y volver a incluir el módulo.

No te olvides de ![configuración08](../images/configuration08.png) si haces un cambio.

> **Importante**
>
> Si estás usando Ubuntu : Para que el demonio funcione, debes tener ubuntu 15.04 (las versiones inferiores tienen un error y el demonio no puede iniciarse). Tenga cuidado si actualiza desde 14.04 toma una vez en 15.04 reiniciar la instalación de dependencias.

> **Importante**
>
> Selección del puerto clave Z-Wave en modo de detección automática, **Auto**, solo funciona para dongles USB.

## Panel móvil

![configuration09](../images/configuration09.png)

Le permite mostrar o no el panel móvil cuando usa la aplicación en un teléfono.

# Configuración del equipo

Se puede acceder a la configuración del equipo Z-Wave desde el menú de complementos :

![appliance01](../images/appliance01.png)

Debajo de un ejemplo de una página de plugin Z-Wave (presentada con algunos equipos) :

![appliance02](../images/appliance02.png)

> **Punta**
>
> Como en muchos lugares de Jeedom, colocar el mouse en el extremo izquierdo permite que aparezca un menú de acceso rápido (puede, desde su perfil, dejarlo siempre visible).

> **Punta**
>
> Los botones en la linea superior **Sincronizar**, **Red Zwave** y **Salud**, solo son visibles si está en modo **Experto**. ![aparato03](../images/appliance03.png)

## Principal

Aquí encontrarás toda la configuración de tu equipo :

![appliance04](../images/appliance04.png)

-   **Nombre del equipo** : nombre de su módulo Z-Wave.
-   **Objeto padre** : indica el objeto padre al que pertenece el equipo.
-   **Categoría** : categorías de equipos (puede pertenecer a varias categorías).
-   **Activar** : activa su equipo.
-   **Visible** : lo hace visible en el tablero.
-   **ID de nodo** : ID del módulo en la red Z-Wave. Esto puede ser útil si, por ejemplo, desea reemplazar un módulo defectuoso. Simplemente incluya el nuevo módulo, recupere su ID y colóquelo en lugar del ID del módulo anterior y finalmente elimine el nuevo módulo.
-   **Modulo** : este campo solo aparece si hay diferentes tipos de configuración para su módulo (caso de módulos que pueden hacer cables piloto, por ejemplo). Le permite elegir la configuración para usar o modificarla más tarde

-   **Hacer** : fabricante de su módulo Z-Wave.
-   **Configuración** : ventana de configuración de ajustes del módulo
-   **Asistente** : solo disponible en ciertos módulos, le ayuda a configurar el módulo (caso en el teclado zipato por ejemplo)
-   **Documentación** : Este botón le permite abrir directamente la documentación de Jeedom relacionada con este módulo.
-   **Borrar** : Le permite eliminar un elemento del equipo y todos estos comandos adjuntos sin excluirlo de la red Z-Wave.

> **Importante**
>
> Eliminar el equipo no conduce a la exclusión del módulo del controlador. ![aparato11](../images/appliance11.png) El equipo eliminado que todavía está conectado a su controlador se recreará automáticamente después de la sincronización.

## Commandes

A continuación encontrará la lista de pedidos :

![appliance05](../images/appliance05.png)

> **Punta**
>
> Dependiendo de los tipos y subtipos, pueden faltar algunas opciones.

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
-   "Valor de retroalimentación de estado "y" Duración antes de la retroalimentación de estado" : permite indicar a Jeedom que después de un cambio en la información, su valor debe volver a Y, X min después del cambio. Ejemplo : en el caso de un detector de presencia que emite solo durante una detección de presencia, es útil establecer, por ejemplo, 0 en valor y 4 en duración, de modo que 4 minutos después de una detección de movimiento (y si entonces , no hubo nuevos) Jeedom restablece el valor de la información a 0 (se detecta más movimiento).
-   Guardar historial : permite historizar los datos.
-   Mostrar : permite mostrar los datos en el tablero.
-   Invertir : permite invertir el estado para tipos binarios.
-   Unidad : unidad de datos (puede estar vacía).
-   Min / max : límites de datos (pueden estar vacíos).
-   Configuración avanzada (ruedas con muescas pequeñas) : muestra la configuración avanzada del comando (método de registro, widget, etc.).

-   Probar : Se usa para probar el comando.
-   Eliminar (firmar -) : permite eliminar el comando.

> **Importante**
>
> El botón **Probar** en el caso de un comando de tipo Información, no consultará el módulo directamente sino el valor disponible en el caché Jeedom. La prueba devolverá el valor correcto solo si el módulo en cuestión ha transmitido un nuevo valor correspondiente a la definición del comando. Por lo tanto, es completamente normal no obtener un resultado después de la creación de un nuevo comando Info, especialmente en un módulo alimentado por batería que rara vez notifica a Jeedom.

El **lupa**, disponible en la pestaña general, le permite recrear todos los comandos para el módulo actual. ![aparato13](../images/appliance13.png) Si no hay un comando presente o si los comandos son incorrectos, la lupa debe remediar la situación.

> **Importante**
>
> El **lupa** borrará los pedidos existentes. Si los comandos se usaron en escenarios, entonces tendrá que corregir sus escenarios en los otros lugares donde se usaron los comandos.

## Juegos de comando

Algunos módulos tienen varios conjuntos de comandos preconfigurados

![appliance06](../images/appliance06.png)

Puede seleccionarlos a través de las posibles opciones, si el módulo lo permite.

> **Importante**
>
> Debe ampliar para aplicar los nuevos conjuntos de comandos.

## Documentación y Asistente

Para un cierto número de módulos, hay disponible ayuda específica para la instalación, así como recomendaciones de parámetros.

![appliance07](../images/appliance07.png)

El botón **Documentación** proporciona acceso a la documentación del módulo específico para Jeedom.

Los módulos particulares también tienen un asistente específico para facilitar la aplicación de ciertos parámetros u operaciones.

El botón **Asistente** da acceso a la pantalla auxiliar específica del módulo.

## Configuración recomendada

![appliance08](../images/appliance08.png)

Aplicar un conjunto de configuración recomendado por el equipo de Jeedom.

> **Punta**
>
> Cuando se incluyen, los módulos tienen los parámetros predeterminados del fabricante y ciertas funciones no se activan de manera predeterminada.

Los siguientes elementos, según corresponda, se aplicarán para simplificar el uso del módulo.

-   **Configuraciones** permitiendo una rápida puesta en marcha de todas las funcionalidades del módulo.
-   **Grupos d'association** requerido para una operación adecuada.
-   **Intervalo de despertador**, para módulos con batería.
-   Activación de **actualización manual** para módulos que no suben solos, su estado cambia.

Para aplicar el conjunto de configuración recomendado, haga clic en el botón : **Configuración recommandée**, luego confirme la aplicación de las configuraciones recomendadas.

![appliance09](../images/appliance09.png)

El asistente activa los diversos elementos de configuración.

Se mostrará una confirmación del buen progreso en forma de banner

![appliance10](../images/appliance10.png)

> **Importante**
>
> Se deben activar los módulos de batería para aplicar el conjunto de configuración.

La página del equipo le informa si los elementos aún no se han activado en el módulo. Consulte la documentación del módulo para activarlo manualmente o espere el próximo ciclo de activación.

![aparato11](../images/appliance11.png)

> **Punta**
>
> Es posible activar automáticamente la aplicación del conjunto de configuración recomendado cuando se incluye un nuevo módulo; consulte la sección Configuración del complemento para obtener más detalles.

# Configuracion de modulos

Aquí es donde encontrará toda la información sobre su módulo

![node01](../images/node01.png)

La ventana tiene varias pestañas :

## Resumen

Proporciona un resumen completo de su nodo con información variada sobre él, como el estado de las solicitudes que le permite saber si el nodo está esperando información o la lista de nodos vecinos.

> **Punta**
>
> En esta pestaña es posible recibir alertas en caso de posible detección de un problema de configuración, Jeedom le indicará el procedimiento a seguir para corregir. No confunda una alerta con un error, la alerta es en la mayoría de los casos una recomendación simple.

## Valeurs

![node02](../images/node02.png)

Encontrará aquí todos los comandos y estados posibles en su módulo. Se ordenan por instancia y clase de comando y luego indexan. El « mapping » des commandes est entièrement basé sur ces informations.

> **Punta**
>
> Forzar actualización de un valor. Los módulos en la batería actualizarán un valor solo en el próximo ciclo de activación. Sin embargo, es posible activar manualmente un módulo, consulte la documentación del módulo.

> **Punta**
>
> Es posible tener más pedidos aquí que en Jeedom, esto es completamente normal. En Jeedom los pedidos han sido preseleccionados para ti.

> **Importante**
>
> Algunos módulos no envían automáticamente sus estados, en este caso es necesario activar la actualización manual a los 5 minutos en los valores deseados. Se recomienda dejar automáticamente la actualización. El abuso de la actualización manual puede tener un fuerte impacto en el rendimiento de la red Z-Wave, use solo los valores recomendados en la documentación específica de Jeedom. ![nodo16](../images/node16.png) El conjunto de valores (índice) de la instancia de un comando de clase se volverá a montar, activando la actualización manual en el índice más pequeño de la instancia del comando de clase. Repita para cada instancia si es necesario.

## Configuraciones

![node03](../images/node03.png)

Aquí encontrará todas las posibilidades para configurar los parámetros de su módulo, así como la posibilidad de copiar la configuración desde otro nodo ya en su lugar.

Cuando se modifica un parámetro, la línea correspondiente se vuelve amarilla, ![nodo04](../images/node04.png) la configuración está esperando ser aplicada.

Si el módulo acepta el parámetro, la línea vuelve a ser transparente.

Sin embargo, si el módulo rechaza el valor, la línea se volverá roja con el valor aplicado devuelto por el módulo. ![nodo05](../images/node05.png)

Al incluirlo, se detecta un nuevo módulo con la configuración predeterminada del fabricante. En algunos módulos, las funcionalidades no estarán activas sin modificar uno o más parámetros. Consulte la documentación del fabricante y nuestras recomendaciones para configurar correctamente sus nuevos módulos.

> **Punta**
>
> Los módulos de batería aplicarán cambios de parámetros solo al siguiente ciclo de activación. Sin embargo, es posible activar manualmente un módulo, consulte la documentación del módulo.

> **Punta**
>
> El orden **Reanudar desde** le permite reanudar la configuración de otro módulo idéntico, en el módulo actual.

![node06](../images/node06.png)

> **Punta**
>
> El orden **Aplicar en** le permite aplicar la configuración actual del módulo a uno o más módulos idénticos.

![node18](../images/node18.png)

> **Punta**
>
> El orden **Actualizar configuraciones** fuerza al módulo a actualizar los parámetros guardados en el módulo.

Si no se define un archivo de configuración para el módulo, un asistente manual le permite aplicar parámetros al módulo. ![nodo17](../images/node17.png) Consulte la documentación del fabricante para la definición del índice, el valor y el tamaño.

##Associations

Aquí es donde se encuentra la administración de los grupos de asociación de su módulo.

![node07](../images/node07.png)

Los módulos Z-Wave pueden controlar otros módulos Z-Wave, sin pasar por el controlador o Jeedom. La relación entre un módulo de control y otro módulo se llama asociación.

Para controlar otro módulo, el módulo de comando necesita mantener una lista de dispositivos que recibirán control de comando. Estas listas se denominan grupos de asociación y siempre están vinculadas a ciertos eventos (por ejemplo, el botón presionado, los activadores del sensor, etc.).

En el caso de que ocurra un evento, todos los dispositivos registrados en el grupo de asociación en cuestión recibirán un comando básico.

> **Punta**
>
> Consulte la documentación del módulo para comprender los diferentes grupos de posibles asociaciones y su comportamiento.

> **Punta**
>
> La mayoría de los módulos tienen un grupo de asociación que está reservado para el controlador principal, se utiliza para enviar información al controlador. Generalmente se llama : **Informe** o **Línea de vida**.

> **Punta**
>
> Su módulo puede no tener ningún grupo.

> **Punta**
>
> La modificación de los grupos de asociación de un módulo de batería se aplicará al próximo ciclo de activación. Sin embargo, es posible activar manualmente un módulo, consulte la documentación del módulo.

Para saber con qué otros módulos está asociado el módulo actual, simplemente haga clic en el menú **Asociado con qué módulos**

![node08](../images/node08.png)

Se mostrarán todos los módulos que utilizan el módulo actual, así como el nombre de los grupos de asociación.

**Asociaciones multi-instances**

Algunos módulos admiten un comando de clase de asociaciones de varias instancias. Cuando un módulo admite este CC, es posible especificar con qué instancia se desea crear la asociación

![node09](../images/node09.png)

> **Importante**
>
> Algunos módulos deben estar asociados con la instancia 0 del controlador principal para funcionar correctamente. Por esta razón, el controlador está presente con y sin la instancia 0.

## Sistemas

Pestaña que agrupa los parámetros del sistema del módulo.

![node10](../images/node10.png)

> **Punta**
>
> Los módulos de batería se activan a ciclos regulares, llamado intervalo de activación. El intervalo de activación es un compromiso entre la duración máxima de la batería y las respuestas deseadas del dispositivo. Para maximizar la vida útil de sus módulos, adapte el valor del intervalo de activación, por ejemplo, a 14,400 segundos (4h), vea incluso más alto dependiendo de los módulos y su uso. ![nodo11](../images/node11.png)

> **Punta**
>
> Los módulos **Interruptor** y **Dimmer** puede implementar una clase de comando especial llamada **SwitchAll** 0x27. Puedes cambiar el comportamiento aquí. Dependiendo del módulo, hay varias opciones disponibles. El orden **SwitchAll On/OFF** se puede iniciar a través de su módulo controlador principal.

## Actions

Le permite realizar ciertas acciones en el módulo.

![node12](../images/node12.png)

Ciertas acciones estarán activas de acuerdo con el tipo de módulo y sus posibilidades o de acuerdo con el estado actual del módulo, como si el controlador lo considera muerto.

> **Importante**
>
> No use acciones en un módulo si no sabe lo que está haciendo. Algunas acciones son irreversibles. Las acciones pueden ayudar a resolver problemas con uno o más módulos Z-Wave.

> **Punta**
>
> El **Regeneración de detección de nodos** permite detectar el módulo para aceptar los últimos conjuntos de parámetros. Esta acción es necesaria cuando se le informa que se requiere una actualización de los parámetros y / o el comportamiento del módulo para su correcto funcionamiento. La regeneración de la detección del nodo implica un reinicio de la red, el asistente lo realiza automáticamente.

> **Punta**
>
> Si tiene varios módulos idénticos necesarios para ejecutar el **Regeneración de detección de nodos**, es posible iniciarlo una vez para todos los módulos idénticos.

![node13](../images/node13.png)

> **Punta**
>
> Si ya no se puede acceder a un módulo en una pila y desea excluirlo, y la exclusión no tiene lugar, puede iniciar **Borrar le noeud fantôme** Un asistente realizará varias acciones para eliminar el llamado módulo fantasma. Esta acción implica reiniciar la red y puede tardar varios minutos en completarse.

![node14](../images/node14.png)

Una vez iniciado, se recomienda cerrar la pantalla de configuración del módulo y monitorear la eliminación del módulo a través de la pantalla de estado de Z-Wave.

> **Importante**
>
> Solo los módulos con batería se pueden eliminar a través de este asistente.

## Statistiques

Esta pestaña proporciona algunas estadísticas de comunicación con el nodo.

![node15](../images/node15.png)

Puede ser interesante en el caso de módulos que el controlador presume muertos".

# Inclusión / exclusión

Cuando sale de fábrica, un módulo no pertenece a ninguna red Z-Wave.

## Modo de inclusión

El módulo debe unirse a una red Z-Wave existente para comunicarse con los otros módulos de esta red. Este proceso se llama **Inclusión**. Los dispositivos también pueden salir de una red. Este proceso se llama **Exclusión**. Ambos procesos son iniciados por el controlador principal de la red Z-Wave.

![addremove01](../images/addremove01.png)

Este botón le permite cambiar al modo de inclusión para agregar un módulo a su red Z-Wave.

Puede elegir el modo de inclusión después de hacer clic en el botón
**Inclusión**.

![addremove02](../images/addremove02.png)

Desde la aparición del Z-Wave +, es posible asegurar intercambios entre el controlador y los nodos. Por lo tanto, se recomienda hacer las inclusiones en modo **Seguro**.

Sin embargo, si un módulo no se puede incluir en modo seguro, inclúyalo en modo seguro **No es seguro**.

Una vez en modo de inclusión : Jeedom te dice.

>**Punta**
>
>Un módulo 'no seguro' puede pedir módulos 'inseguros''. Un módulo 'no seguro' no puede pedir un módulo 'seguro''. Un módulo 'seguro' puede pedir módulos 'no seguros' siempre que el transmisor lo admita.

![addremove03](../images/addremove03.png)

Una vez que se inicia el asistente, debe hacer lo mismo en su módulo (consulte su documentación para cambiarlo al modo de inclusión).

> **Punta**
>
> Mientras no tenga el banner, no estará en modo de inclusión.

Si vuelve a hacer clic en el botón, sale del modo de inclusión.

> **Punta**
>
> Se recomienda, antes de la inclusión de un nuevo módulo que sería "nuevo" en el mercado, lanzar el pedido **Módulos de configuración** a través de la pantalla de configuración del complemento. Esta acción recuperará todas las últimas versiones de los archivos de configuración de Openzwave, así como la asignación de comandos de Jeedom.

> **Importante**
>
> Durante una inclusión, se recomienda que el módulo se encuentre cerca del controlador principal, o a menos de un metro de su libertad.

> **Punta**
>
> Algunos módulos requieren una inclusión en modo **Seguro**, por ejemplo para cerraduras.

> **Punta**
>
> Tenga en cuenta que la interfaz móvil también le da acceso a la inclusión, el panel móvil debe haber sido activado.

> **Punta**
>
> Si el módulo ya pertenece a una red, siga el proceso de exclusión antes de incluirlo en su red. De lo contrario, la inclusión de este módulo fallará. También se recomienda ejecutar una exclusión antes de la inclusión, incluso si el producto es nuevo, listo para usar.

> **Punta**
>
> Una vez que el módulo está en su ubicación final, es necesario iniciar la acción para cuidar la red, a fin de solicitar a todos los módulos que actualicen a todos los vecinos.

## Modo de exclusión

![addremove04](../images/addremove04.png)

Este botón le permite cambiar al modo de exclusión, para eliminar un módulo de su red Z-Wave, debe hacer lo mismo con su módulo (consulte su documentación para cambiarlo al modo de exclusión).

![addremove05](../images/addremove05.png)

> **Punta**
>
> Mientras no tenga el banner, no estará en modo de exclusión.

Si vuelve a hacer clic en el botón, saldrá del modo de exclusión.

> **Punta**
>
> Tenga en cuenta que la interfaz móvil también le da acceso a la exclusión.

> **Punta**
>
> Un módulo no necesita ser excluido por el mismo controlador en el que se incluyó anteriormente. De ahí el hecho de que se recomienda ejecutar una exclusión antes de cada inclusión.

## Synchroniser

![addremove06](../images/addremove06.png)

Botón que permite la sincronización de los módulos de red Z-Wave con el equipo Jeedom. Los módulos están asociados con el controlador principal, los dispositivos en Jeedom se crean automáticamente cuando se incluyen. También se eliminan automáticamente cuando se excluyen, si la opción **Borrar automatiquement les périphériques exclus** está activado.

Si ha incluido módulos sin Jeedom (requiere un dongle de batería como el Aeon-labs Z-Stick GEN5), la sincronización será necesaria después de conectar la llave, una vez que el demonio haya comenzado y esté operativo.

> **Punta**
>
> Si no tiene la imagen o Jeedom no ha reconocido su módulo, este botón se puede usar para corregir (siempre que la entrevista del módulo esté completa).

> **Punta**
>
> Si en su tabla de enrutamiento y / o en la pantalla de estado de Z-Wave, tiene uno o más módulos nombrados con su **nombre genérico**, la sincronización remediará esta situación.

El botón Sincronizar solo es visible en modo experto :
![addremove07](../images/addremove07.png)

# Redes Z-Wave

![network01](../images/network01.png)

Aquí encontrará información general sobre su red Z-Wave.

![network02](../images/network02.png)

## Resumen

La primera pestaña le brinda el resumen básico de su red Z-Wave, en particular encontrará el estado de la red Z-Wave, así como el número de elementos en la cola.

**Información**

-   Proporciona información general sobre la red, la fecha de inicio, el tiempo requerido para obtener la red en un estado funcional denominado.
-   El número total de nodos en la red, así como el número que están durmiendo en el momento.
-   El intervalo de solicitud está asociado con la actualización manual. Está preestablecido en el motor Z-Wave a los 5 minutos.
-   Los vecinos del controlador.

**Estado**

![network03](../images/network03.png)

Un conjunto de información sobre el estado actual de la red, a saber :

-   Estado actual, tal vez **Conductor inicializado**, **Topología cargada** o **Listo**.
-   Cola saliente, indica la cantidad de mensajes en cola en el controlador que esperan ser enviados. Este valor generalmente es alto durante el inicio de la red cuando el estado aún está en **Conductor inicializado**.

Una vez que la red ha alcanzado al menos **Topología cargada**, Los mecanismos internos del servidor Z-Wave forzarán actualizaciones de valores, por lo tanto, es completamente normal ver que aumenta el número de mensajes. Esto volverá rápidamente a 0.

> **Punta**
>
> Se dice que la red es funcional cuando alcanza el estado **Topología cargada**, es decir que todos los nodos del sector han completado sus entrevistas. Dependiendo de la cantidad de módulos, la distribución de la batería / sector, la elección del dongle USB y la PC en la que se ejecuta el complemento Z-Wave, la red alcanzará este estado entre uno y cinco minutos.

Una red **Listo**, significa que todos los nodos del sector y de la batería han completado su entrevista.

> **Punta**
>
> Dependiendo de los módulos que tenga, es posible que la red nunca alcance el estado por sí misma **Listo**. Los controles remotos, por ejemplo, no se despiertan solos y nunca completarán su entrevista. En este tipo de casos, la red está completamente operativa e incluso si los controles remotos no han completado su entrevista, aseguran su funcionalidad dentro de la red.

**Capacidades**

Se usa para averiguar si el controlador es un controlador primario o secundario.

**Sistema**

Muestra diversa información del sistema.

-   Información sobre el puerto USB utilizado.
-   Versión de la biblioteca OpenZwave
-   Versión de la biblioteca Python-OpenZwave

## Actions

![network05](../images/network05.png)

Aquí encontrará todas las acciones posibles para toda su red Z-Wave. Cada acción va acompañada de una breve descripción.

> **Importante**
>
> Ciertas acciones son realmente arriesgadas o incluso irreversibles, el equipo de Jeedom no se hace responsable en caso de manejo incorrecto.

> **Importante**
>
> Algunos módulos requieren inclusión en modo seguro, por ejemplo para cerraduras de puertas. La inclusión segura debe iniciarse mediante la acción en esta pantalla.

> **Punta**
>
> Si no se puede iniciar una acción, se desactivará hasta que se pueda volver a ejecutar.

## Statistiques

![network06](../images/network06.png)

Aquí encontrará estadísticas generales para toda su red Z-Wave.

## Gráfico de red

![network07](../images/network07.png)

Esta pestaña le dará una representación gráfica de los diferentes enlaces entre los nodos.

Explicación de la leyenda del color :

-   **Negro** : El controlador principal, generalmente representado como Jeedom.
-   **Verde** : Comunicación directa con el controlador, ideal.
-   **Azul** : Para los controladores, como los controles remotos, están asociados con el controlador primario, pero no tienen ningún vecino.
-   **Amarillo** : Todos los caminos tienen más de un salto antes de llegar al controlador.
-   **Gris** : La entrevista aún no se ha completado, los enlaces se conocerán realmente una vez que se complete la entrevista.
-   **Rojo** : presuntamente muerto, o sin un vecino, no participa / ya no participa en la red de la red.

> **Punta**
>
> Solo el equipo activo se mostrará en el gráfico de red.

La red Z-Wave consta de tres tipos diferentes de nodos con tres funciones principales.

La principal diferencia entre los tres tipos de nodos es su conocimiento de la tabla de enrutamiento de la red y, posteriormente, su capacidad para enviar mensajes a la red.

## Tabla de enrutamiento

Cada nodo puede determinar qué otros nodos están en comunicación directa. Estos nodos se llaman vecinos. Durante la inclusión y / o posterior solicitud, el nodo puede informar al controlador de la lista de vecinos. Gracias a esta información, el controlador puede construir una tabla que tiene toda la información sobre las posibles rutas de comunicación en una red.

![network08](../images/network08.png)

Las filas de la tabla contienen los nodos de origen y las columnas contienen los nodos de destino. Consulte la leyenda para comprender los colores de las celdas que indican los enlaces entre dos nodos.

Explicación de la leyenda del color :

-   **Verde** : Comunicación directa con el controlador, ideal.
-   **Azul** : Al menos 2 rutas con un salto.
-   **Amarillo** : Menos de 2 rutas con un salto.
-   **Gris** : La entrevista aún no se ha completado, en realidad se actualizará una vez que se complete la entrevista.
-   **Naranja** : Todos los caminos tienen más de un salto. Puede causar latencias.

> **Punta**
>
> Solo el equipo activo se mostrará en el gráfico de red.

> **Importante**
>
> Un módulo presunto muerto, no participa / ya no participa en la red de la red. Se marcará aquí con un signo de exclamación rojo en un triángulo.

> **Punta**
>
> Puede iniciar manualmente la actualización de vecino, por módulo o para toda la red utilizando los botones disponibles en la tabla de enrutamiento.

# Santé

![health01](../images/health01.png)

Esta ventana resume el estado de su red Z-Wave :

![health02](../images/health02.png)

Tienes aqui :

-   **Modulo** : el nombre de su módulo, haga clic en él para acceder directamente.
-   **Identificación** : ID de su módulo en la red Z-Wave.
-   **Notificación** : último tipo de intercambio entre el módulo y el controlador
-   **Grupo** : indica si la configuración del grupo está bien (controlador al menos en un grupo). Si no tiene nada es que el módulo no admite la noción de grupo, es normal
-   **Fabricante** : indica si la recuperación de la información de identificación del módulo está bien
-   **Vecino** : indica si se ha recuperado la lista de vecinos
-   **Estado** : Indica el estado de la entrevista del módulo (etapa de consulta)
-   **Batería** : nivel de batería del módulo (un enchufe de red indica que el módulo recibe alimentación de la red).
-   **Hora de despertarse** : para módulos con batería, proporciona la frecuencia en segundos de los instantes cuando el módulo se activa automáticamente.
-   **Paquete total** : muestra el número total de paquetes recibidos o enviados con éxito al módulo.
-   **% Ok** : muestra el porcentaje de paquetes enviados / recibidos con éxito.
-   **Retraso de tiempo** : muestra el retraso promedio de envío de paquetes en ms.
-   **Última notificación** : Fecha de la última notificación recibida del módulo y la hora del próximo despertador programado, para los módulos que duermen.
    -   También permite informar si el nodo no se ha despertado una vez desde el lanzamiento del demonio.
    -   E indica si un nodo no se ha despertado como se esperaba.
-   **De ping** : Le permite enviar una serie de mensajes al módulo para probar su correcto funcionamiento.

> **Importante**
>
> Se mostrará el equipo deshabilitado pero no habrá información de diagnóstico.

El nombre del módulo puede ir seguido de una o dos imágenes:

![health04](../images/health04.png) Modules supportant la COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../images/health05.png) Modules supportant la COMMAND\_CLASS\_SECURITY y securisé.

![health06](../images/health06.png) Modules supportant la COMMAND\_CLASS\_SECURITY y non Seguro.

![health07](../images/health07.png) Modulo FLiRS, routeurs esclaves (modules à piles) à écoute fréquente.

> **Punta**
>
> El comando Ping se puede usar si se presume que el módulo está muerto "MUERTE" para confirmar si este es realmente el caso.

> **Punta**
>
> Los módulos dormidos solo responderán a Ping la próxima vez que se despierten.

> **Punta**
>
> La notificación de tiempo de espera no significa necesariamente un problema con el módulo. Inicie un Ping y, en la mayoría de los casos, el módulo responderá con una Notificación **No Operación** que confirma un retorno fructífero de ping.

> **Punta**
>
> El retraso y el% OK en los nodos con baterías antes de completar su entrevista no es significativo. De hecho, el nodo no responderá a los interrogatorios del controlador sobre el hecho de que está en sueño profundo.

> **Punta**
>
> El servidor Z-Wave se encarga automáticamente de iniciar las pruebas en los módulos en Tiempo de espera después de 15 minutos

> **Punta**
>
> El servidor Z-Wave intenta automáticamente reensamblar los módulos que se presumen muertos.

> **Punta**
>
> Se enviará una alerta a Jeedom si se presume que el módulo está muerto. Puede activar una notificación para ser informado lo antes posible. Vea la configuración del mensaje en la pantalla de configuración de Jeedom.

![health03](../images/health03.png)

> **Punta**
>
> Si en su tabla de enrutamiento y / o en la pantalla de estado de Z-Wave tiene uno o más módulos nombrados con su **nombre genérico**, la sincronización remediará esta situación.

> **Punta**
>
> Si en su tabla de enrutamiento y / o en la pantalla de estado de Z-Wave tiene uno o más módulos llamados **Desconocido**, Esto significa que la entrevista del módulo no se ha completado con éxito. Probablemente tengas un **NOK** en la columna del constructor. Abra los detalles de los módulos para probar las soluciones sugeridas (consulte la sección Solución de problemas y diagnósticos, a continuación).

## Estado de la entrevista

Paso de entrevistar un módulo después de iniciar el demonio.

-   **Ninguno** Inicialización del proceso de búsqueda de nodos.
-   **ProtocolInfo** Recupere la información del protocolo, si este nodo está escuchando (oyente), su velocidad máxima y sus clases de dispositivo.
-   **Sonda** Haga ping al módulo para ver si está despierto.
-   **Despertador** Inicie el proceso de activación, si es un nodo inactivo.
-   **Fabricante Específico1** Recupere el nombre del fabricante y los identificadores del producto si ProtocolInfo lo permite.
-   **NodeInfo** Recuperar información sobre el soporte de clases de comando compatibles.
-   **NodePlusInfo** Recupere información de ZWave + sobre el soporte para clases de comando compatibles.
-   **Informe de seguridad** Recupere la lista de clases de orden que requieren seguridad.
-   **Fabricante Específico2** Recupere el nombre del fabricante y los identificadores del producto.
-   **Versiones** Recuperar información de la versión.
-   **Instancias** Recuperar información de clase de comando de varias instancias.
-   **Estática** Recuperar información estática (no cambia).
-   **CacheLoad** Haga ping al módulo durante el reinicio con la caché de configuración del dispositivo.
-   **Asociaciones** Recuperar información sobre asociaciones.
-   **Vecinos** Recuperar la lista de nodos vecinos.
-   **Sesión** Recuperar información de la sesión (rara vez cambia).
-   **Dinámico** Recuperar información dinámica (cambios frecuentes).
-   **Configuración** Recuperar información de parámetros de configuración (solo se realiza bajo pedido).
-   **Completa** El proceso de entrevista ha finalizado para este nodo.

## Notification

Detalles de notificaciones enviadas por módulos

-   **Completado** Acción completada con éxito.
-   **Tiempo de espera** Informe de retraso informado al enviar un mensaje.
-   **No Operación** Informe sobre una prueba del nodo (Ping), que el mensaje se envió correctamente.
-   **Despierto** Informar cuando un nodo acaba de despertarse
-   **Dormir** Informar cuando un nodo se ha quedado dormido.
-   **Muerto** Informe cuando un nodo se presume muerto.
-   **Vivo** Informar cuando se relanza un nodo.

# Backups

La parte de respaldo le permitirá administrar los respaldos de su topología de red. Este es su archivo zwcfgxxx.xml, constituye el último estado conocido de su red, es una forma de caché de su red. Desde esta pantalla puedes :

-   Iniciar una copia de seguridad (se realiza una copia de seguridad en cada reinicio de la red y durante las operaciones críticas). Las últimas 12 copias de seguridad se mantienen
-   Restaurar una copia de seguridad (seleccionándola de la lista justo arriba)
-   Eliminar una copia de seguridad

![backup01](../images/backup01.png)

# Actualizar OpenZWave

Después de una actualización del complemento Z-Wave, es posible que Jeedom le pida que actualice las dependencias de Z-Wave. Se mostrará un NOK de dependencia:

![update01](../images/update01.png)

> **Punta**
>
> No se debe hacer una actualización de las dependencias con cada actualización del complemento.

Jeedom debería lanzar la actualización de dependencia por sí mismo si el complemento considera que son **NOK**. Esta validación se lleva a cabo después de 5 minutos.

La duración de esta operación puede variar según su sistema (hasta más de 1 hora con raspberry pi)

Una vez que se completa la actualización de las dependencias, el demonio se reiniciará automáticamente al validar Jeedom. Esta validación se lleva a cabo después de 5 minutos.

> **Punta**
>
> En caso de que no se complete la actualización de las dependencias, consulte el registro **Openzwave\_update** quien debe informarle sobre el problema.

# Lista de módulos compatibles

Encontrará la lista de módulos compatibles
[aquí](https://doc.jeedom.com/es_ES/zwave/equipement.compatible)

# Solución de problemas y diagnóstico

## Mi módulo no se detecta o no proporciona sus identificadores de producto y tipo

![troubleshooting01](../images/troubleshooting01.png)

Inicie la regeneración de la detección de nodos desde la pestaña Acciones del módulo.

Si tiene varios módulos en este escenario, inicie **Regenera la detección de nodos desconocidos** desde la pantalla **Red Zwave** pestaña **Acciones**.

## Mi módulo se presume muerto por el controlador Dead

![troubleshooting02](../images/troubleshooting02.png)

Si el módulo aún está conectado y accesible, siga las soluciones propuestas en la pantalla del módulo.

Si el módulo se ha cancelado o está realmente defectuoso, puede excluirlo de la red utilizando **eliminar el nodo por error** a través de la pestaña **Acciones**.

Si el módulo ha sido reparado y se ha entregado un nuevo módulo de reemplazo, puede iniciar **Reemplazar nodo fallido** a través de la pestaña **Acciones**, el controlador activa la inclusión, entonces debe proceder con la inclusión en el módulo. Se conservará la identificación del antiguo módulo, así como sus comandos.

## Cómo usar el comando SwitchAll

![troubleshooting03](../images/troubleshooting03.png)

Está disponible a través de su nodo controlador. Su controlador debe tener los comandos Encender todo y Apagar todo.

Si su controlador no aparece en su lista de módulos, inicie la sincronización.

![troubleshooting04](../images/troubleshooting04.png)

Class Switch All Command generalmente se admite en conmutadores y unidades. Su comportamiento es configurable en cada módulo que lo soporta.

Entonces podemos:

-   Desactivar el comando Cambiar todas las clases.
-   Activar para encendido y apagado.
-   Activar solo en.
-   Activar solo apagado.

La elección de las opciones depende del fabricante.

Por lo tanto, debe tomarse el tiempo de revisar todos sus interruptores / atenuadores antes de configurar un escenario si no controla solo las luces.

## Mi módulo no tiene un comando de escena o botón

![troubleshooting05](../images/troubleshooting05.png)

Puede agregar el comando en la pantalla de asignación de comandos.

Esta es una orden **Información** en CC **0x2b** Instancia **0** commande
**datos \ [0 \]. val**

El modo de escena debe activarse en la configuración del módulo. Consulte la documentación de su módulo para obtener más detalles.

## Forzar valores de actualización

Es posible forzar la solicitud para actualizar los valores de una instancia para un comando de clase específico.

Es posible hacerlo a través de una solicitud http o crear un pedido en la pantalla de mapeo de equipos.

![troubleshooting06](../images/troubleshooting06.png)

Esta es una orden **Acción** elige el **CC** deseado para un **Instancia** dado con el comando **datos \ [0 \]. ForceRefresh ()**

Todos los índices de instancia para este comando de Clase se actualizarán. Los nodos de las baterías esperarán su próximo despertar antes de llevar a cabo la actualización de su valor.

También puede usar por script enviando una solicitud http al servidor REST de Z-Wave.
Reemplace ip\_jeedom, node\_id, instancia\_id, cc\_id e index

``http://token:\#APIKEY\#@ip\_jeedom:8083/ZWaveAPI/Run/devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()``

## Transfiera los módulos a un nuevo controlador

Por diferentes razones, es posible que deba transferir todos sus módulos a un nuevo controlador principal.

Decides irte de **raZberry** un **Z-Stick Gen5** o porque, tienes que realizar un **Restablecer** completo del controlador principal.

Aquí hay diferentes pasos para llegar allí sin perder sus valiosos escenarios, widgets e historial:

-   1 \) Hacer una copia de seguridad de Jeedom.
-   2 \) Recuerde anotar (captura de pantalla) los valores de sus parámetros para cada módulo, se perderán después de la exclusión.
-   3 \) En la configuración de Z-Wave, desmarque la opción "Eliminar automáticamente los dispositivos excluidos" y guarde. Reinicios de red.
-   4a) En el caso de un **Restablecer**, Restablezca el controlador principal y reinicie el complemento.
-   4b) Para un nuevo controlador, detenga Jeedom, desconecte el controlador anterior y conecte el nuevo. Inicie Jeedom.
-   5 \) Para cada dispositivo Z-Wave, cambie la ID de ZWave a **0**.
-   6 \) Abra 2 páginas del complemento Z-Wave en diferentes pestañas.
-   7 \) (a través de la primera pestaña) Vaya a la página de configuración de un módulo que desea incluir en el nuevo controlador.
-   8 \) (a través de la segunda pestaña) Excluir y luego incluir el módulo. Se crearán nuevos equipos.
-   9 \) Copie la ID de Z-Wave del nuevo dispositivo, luego elimine este dispositivo.
-   10 \) Regrese a la pestaña del módulo anterior (primera pestaña) y luego pegue la nueva ID en lugar de la ID anterior.
-   11 \) Los parámetros de ZWave se perdieron durante la exclusión / inclusión, recuerde restablecer sus parámetros específicos si no utiliza los valores predeterminados.
-   11 \) Repita los pasos 7 a 11 para cada módulo a transferir.
-   12 \) Al final, ya no debería tener equipo en ID 0.
-   13 \) Verifique que todos los módulos estén correctamente nombrados en la pantalla de estado de Z-Wave. Inicie la sincronización si este no es el caso.

## Reemplace un módulo defectuoso

Cómo rehacer la inclusión de un módulo que falla sin perder sus escenarios de valor, widgets e historiales

Si se supone que el módulo está "Muerto" :

-   Tenga en cuenta (captura de pantalla) los valores de sus parámetros, se perderán después de la inclusión.
-   Vaya a la pestaña de acciones del módulo y ejecute el comando "Reemplazar nodo fallido".
-   El controlador está en modo de inclusión, proceda a la inclusión de acuerdo con la documentación del módulo.
-   Restablece tus parámetros específicos.

Si no se presume que el módulo está "Muerto" pero aún está accesible:

-   En la configuración de ZWave, desmarque "Eliminar automáticamente los dispositivos excluidos".
-   Tenga en cuenta (captura de pantalla) los valores de sus parámetros, se perderán después de la inclusión.
-   Excluir el módulo defectuoso.
-   Vaya a la página de configuración del módulo defectuoso.
-   Abra la página del complemento ZWave en una pestaña nueva.
-   Incluir el módulo.
-   Copie la ID del nuevo módulo, luego elimine este equipo.
-   Regrese a la pestaña del módulo anterior y luego pegue la nueva ID en lugar de la ID anterior.
-   Restablece tus parámetros específicos.

## Eliminación del nodo fantasma

Si ha perdido toda la comunicación con un módulo de batería y desea excluirlo de la red, es posible que la exclusión no tenga éxito o que el nodo permanezca presente en su red.

El asistente automático de nodo fantasma está disponible.

-   Vaya a la pestaña de acciones del módulo para eliminar.
-   Probablemente tendrá un estado **CacheLoad**.
-   Comando de inicio **Borrar nœud fantôme**.
-   La red Z-Wave se detiene. El asistente automático modifica el archivo **zwcfg** eliminar CC WakeUp del módulo. Reinicios de red.
-   Cerrar la pantalla del módulo.
-   Abra la pantalla Z-Wave Health.
-   Espere a que se complete el ciclo de inicio (topología cargada).
-   El módulo normalmente se marcará como presunto muerto.
-   Al minuto siguiente, debería ver que el nodo desaparece de la pantalla de estado.
-   Si en la configuración de Z-Wave, ha desmarcado la opción "Eliminar automáticamente los dispositivos excluidos", deberá eliminar manualmente el equipo correspondiente.

Este asistente solo está disponible para módulos de batería.

## Acciones posteriores a la inclusión

Se recomienda realizar la inclusión al menos a 1M del controlador principal, o esta no será la posición final de su nuevo módulo. Estas son algunas buenas prácticas a seguir luego de la inclusión de un nuevo módulo en su red.

Una vez que se completa la inclusión, debemos aplicar una cierta cantidad de parámetros a nuestro nuevo módulo para aprovecharlo al máximo. Recordatorio, los módulos, después de la inclusión, tienen la configuración predeterminada del fabricante. Aproveche la posibilidad de estar junto al controlador y la interfaz Jeedom para configurar correctamente su nuevo módulo. También será más fácil activar el módulo para ver el efecto inmediato del cambio. Algunos módulos tienen documentación específica de Jeedom para ayudarlo con los diferentes parámetros, así como con los valores recomendados.

Pruebe su módulo, confirme la retroalimentación, retroalimentación de estado y posibles acciones en el caso de un actuador.

Durante la entrevista, su nuevo módulo buscó a sus vecinos. Sin embargo, los módulos en su red aún no conocen su nuevo módulo.

Mueva su módulo a su ubicación final. Inicie la actualización de sus vecinos y vuelva a activarla.

![troubleshooting07](../images/troubleshooting07.png)

Vemos que él ve un cierto número de vecinos pero que los vecinos no lo ven.

Para remediar esta situación, es necesario iniciar la acción para cuidar la red, a fin de pedir a todos los módulos que encuentren a sus vecinos.

Esta acción puede tardar 24 horas antes de completarse, los módulos de batería realizarán la acción solo la próxima vez que se activen.

![troubleshooting08](../images/troubleshooting08.png)

La opción de cuidar la red dos veces por semana le permite realizar este proceso sin ninguna acción de su parte, es útil durante la instalación de nuevos módulos o al moverlos.

## No hay comentarios de la condición de la batería

Los módulos Z-Wave rara vez envían el estado de su batería al controlador. Algunos lo harán en el momento de la inclusión, solo cuando alcance el 20% u otro valor umbral crítico.

Para ayudarlo a controlar mejor el estado de sus baterías, la pantalla Baterías en el menú Análisis le brinda una descripción general del estado de sus baterías. Un mecanismo de notificación de batería baja también está disponible.

El valor devuelto desde la pantalla Baterías es el último conocido en la memoria caché.

Todas las noches, el complemento Z-Wave le pide a cada módulo que actualice el valor de la batería. La próxima vez que se despierte, el módulo envía el valor a Jeedom para que se agregue al caché. Por lo tanto, generalmente debe esperar al menos 24 horas antes de obtener un valor en la pantalla Baterías.

> **Punta**
>
> Por supuesto, es posible actualizar manualmente el valor de la batería a través de la pestaña Valores del módulo, luego esperar el próximo despertador o incluso despertar manualmente el módulo para obtener un aumento inmediato. El intervalo de activación del módulo se define en la pestaña Sistema del módulo. Para optimizar la vida útil de sus baterías, se recomienda espaciar este retraso el mayor tiempo posible. Por 4h, aplique 14400, 12h 43200. Ciertos módulos deben escuchar regularmente los mensajes del controlador, como los termostatos. En este caso, debe pensar en 15 min, es decir, 900. Cada módulo es diferente, por lo que no existe una regla exacta, es caso por caso y según la experiencia.

> **Punta**
>
> La descarga de una batería no es lineal, algunos módulos mostrarán una gran pérdida porcentual en los primeros días de la puesta en marcha, luego no se moverán durante semanas para vaciarse rápidamente una vez pasado el 20%.

## El controlador se está inicializando

Cuando inicia el demonio Z-Wave, si intenta iniciar inmediatamente una inclusión / exclusión, puede recibir este mensaje: \* "El controlador se está inicializando, intente nuevamente en unos minutos"

> **Punta**
>
> Después del inicio del demonio, el controlador pasa a todos los módulos para repetir su entrevista. Este comportamiento es completamente normal en OpenZWave.

Sin embargo, si después de varios minutos (más de 10 minutos) aún tiene este mensaje, ya no es normal.

Tienes que probar los diferentes pasos:

-   Asegúrese de que las luces de la pantalla de salud Jeedom sean verdes.
-   Asegúrese de que la configuración del complemento esté en orden.
-   Asegúrese de haber seleccionado el puerto correcto para la clave ZWave.
-   Asegúrese de que la configuración de su red Jeedom sea correcta. (Atención si ha realizado una restauración de una instalación de bricolaje hacia la imagen oficial, el sufijo / libertad no debería aparecer allí)
-   Mire el registro del complemento para ver si no se ha informado un error.
-   Mira el **Consola** Complemento ZWave, para ver si no se ha informado un error.
-   Lanzar el demonio por **Depurar** mira de nuevo a la **Consola** y registros de complementos.
-   Reiniciar completamente Jeedom.
-   Asegúrese de tener un controlador Z-Wave, Razberry a menudo se confunde con EnOcean (error al realizar el pedido).

Ahora debemos comenzar las pruebas de hardware:

-   El Razberry está bien conectado al puerto GPIO.
-   La alimentación USB es suficiente.

Si el problema persiste, reinicie el controlador:

-   Detenga completamente su Jeedom a través del menú de detención en el perfil de usuario.
-   Desconecta el poder.
-   Retire el dongle USB o Razberry según corresponda, aproximadamente 5 minutos.
-   Vuelva a conectar todo e intente nuevamente.

## El controlador ya no responde

No se transmiten más pedidos a los módulos, pero las devoluciones de estado se envían de vuelta a Jeedom.

La cola de mensajes del controlador puede estar llena. Vea la pantalla de la red Z-Wave si el número de mensajes pendientes solo aumenta.

En este caso, debe reiniciar el Demon Z-Wave.

Si el problema persiste, debe reiniciar el controlador:

-   Detenga completamente su Jeedom a través del menú de detención en el perfil de usuario.
-   Desconecta el poder.
-   Retire el dongle USB o Razberry según corresponda, aproximadamente 5 minutos.
-   Vuelva a conectar todo e intente nuevamente.

## Error durante dependencias

Varios errores pueden ocurrir al actualizar dependencias. Verifique el registro de actualización de dependencias para determinar cuál es exactamente el error. Generalmente, el error está al final del registro en las últimas líneas.

Aquí están los posibles problemas y sus posibles soluciones:

-   no se pudo instalar mercurial - abortar

El paquete mercurial no desea instalar, para corregir el inicio en ssh:

````
    sudo rm /var/lib/dpkg/info/$mercurial* -f
    sudo apt-gy install mercurial
````

-   Las adicciones parecen bloqueadas en un 75%

Con un 75%, este es el comienzo de la compilación de la biblioteca openzwave, así como el envoltorio de python openzwave. Este paso es muy largo, sin embargo, puede ver el progreso a través de la vista de registro de actualización. Entonces solo tienes que ser paciente.

-   Error al compilar la biblioteca openzwave

````
        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed source if appropriate.
        See <file:///usr/share/doc/gcc-4.9/README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targy 'build' failed
        make: *** [build] Error 1
````

Este error puede ocurrir debido a la falta de memoria RAM durante la compilación.

Desde la interfaz de usuario de Jeedom, inicie la compilación de dependencias.

Una vez iniciado, en ssh, detenga estos procesos (consumidores en memoria) :

````
    sudo systemctl stop cron
    sudo systemctl stop apache2
    sudo systemctl stop mysql.
````

Para seguir el progreso de la compilación, ajustamos el archivo de registro openzwave\_update.

````
    tail -f /var/www/html/log/openzwave_update
````

Cuando la compilación se complete y sin error, reinicie los servicios que detuvo

````
sudo systemctl start cron sudo systemctl start apache2 sudo systemctl
start mysql
````

## Usando la tarjeta Razberry en una Raspberry Pi 3

Para usar un controlador Razberry en un Raspberry Pi 3, el controlador Bluetooth interno del Raspberry debe estar desactivado.

Agrega esta línea:

````
    dtoverlay=pi3-miniuart-bt
````

Al final del archivo:

````
    /boot/config.txt
````

Luego reinicie su Frambuesa.

# API HTTP

El complemento Z-Wave proporciona a los desarrolladores y usuarios una API completa para poder operar la red Z-Wave a través de una solicitud HTTP.

Puede usar todos los métodos expuestos por el servidor REST del demonio Z-Wave.

La sintaxis para llamar a las rutas es de esta forma:

URL = ``http://token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/\#ROUTE\#``

-   \#API\_KEY\# corresponde a su clave API, específica a su instalación. Pour la trouver, il faut aller dans le menu « Principal », puis « Administration » y « Configuración », en activant le mode Expert, vous verrez alors une ligne Clef API.
-   \#IP\_JEEDOM\# corresponde a su URL de acceso de Jeedom.
-   \#PORTDEMON\# corresponde al número de puerto especificado en la página de configuración del complemento Z-Wave, de forma predeterminada: 8083.
-   \#ROUTE\# corresponde a la ruta en el servidor REST para ejecutar.

Para conocer todas las rutas, consulte
[Github](https://github.com/jeedom/plugin-openzwave) del complemento Z-Wave.

Example: Para hacer ping al id del nodo 2

URL = ``http://token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ZWaveAPI/Run/devices\[2\].TestNode()``

# FAQ

> **Me sale el error "No hay suficiente espacio en el búfer de flujo"**
>
> Desafortunadamente, este error es hardware, no hay nada que podamos hacer y estamos buscando por el momento cómo forzar un reinicio del demonio en el caso de este error (pero a menudo también es necesario desconectar la clave durante 5 minutos para que vuelva a comenzar)
