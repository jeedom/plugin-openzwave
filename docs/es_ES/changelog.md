>**Importante**
>
>Como recordatorio si no hay información sobre la actualización, significa que solo se refiere a la actualización de documentación, traducción o texto

# 10/07/2019

- Se corrigió un error al detener al demonio
- Correcciones de errores
- ESTA ACTUALIZACIÓN DEBE RECOMENDAR LAS DEPENDENCIAS (REINICIAR)

# 2019-09-19

- Mostrar corrección de errores

# 09-10-2019

- Se corrigió un problema con la visualización de la tabla de enrutamiento

# 09-09-2019
- Adaptación de dependencias para Debian10 Buster
- Modificación que permite separar las salidas en implantes inteligentes (esta función requiere una recopilación de dependencias)

2019-02-04
===
- ESTA ACTUALIZACIÓN DEBE RECOMENDAR LAS DEPENDENCIAS (REINICIAR)
- Corrección de un error en múltiples instancias de termostatos
- Creación de un nivel de cola en desuso en acciones para actualizaciones
- Adición de muchas confs (como recordatorio, el botón para recuperar confs es útil para estar actualizado sin actualizar el complemento)
- Gestión mejorada de canales multicanal encapsulados
- Adición de CC específico del fabricante
- Instalación simple del interruptor de sonido CC
- Arreglo para la inclusión múltiple de dispositivos <
- Binario CC Switch mejorado
- Introducir parámetros manuales siempre es posible
- Mejora de cola
- Preparación para agregar nuevos CC (notificación en particular)
- Adición de códigos en la alarma CC para el teclado Zipato por el momento
- Corrección del philio en modo seguro que durante los tonos de llamada generó un tiempo de espera de 10 segundos (seguramente es necesario regenerar la detección de la sirena o volver a incluirla)
- Corrección de un error si el nivel de registro es ninguno
- ESTA ACTUALIZACIÓN NECESITA RECOMPILAR LAS DEPENDENCIAS

2018-03-17
===

- Cambio de rama para recuperación de confs durante syncconf (luego de un cambio en la organización de githubs)

2018-01-17 / 2018-01-19
===

-   Nuevas llegadas

    -   Retorno de la posibilidad de sincronizar confs sin actualizar el complemento

    -   Mejoras

    -   Adición de la posibilidad interna de activar actualizaciones en ciertos valores específicos y módulos específicos (utilizados en confesiones de libertad)

    -   Rediseño completo de la función que permite simular un valor en otro comando para evitar ponerlo en un conjunto de módulos pero específicamente (Jeedom internal)

-   Error corregido

    -   Se corrigió un error que causaba que las configuraciones generadas automáticamente estuvieran en el formato anterior y, por lo tanto, no se pudieran usar

    -   Corrección del error de la pérdida del punto de ajuste pendiente en las válvulas termostáticas (va con el punto 2 de las mejoras)

    -   Reducción del tamaño de las imágenes para limitar el tamaño del complemento tanto como sea posible (aproximadamente 500 imágenes)

    -   Eliminación de dependencias más utilizadas, como Mercurial Sphinx, etc

    -   Supresión de la purga de las configuraciones antes de la actualización (evita tener iconos Zwave en lugar de las imágenes en caso de actualizaciones fallidas por tiempo de espera u otro)

2017-08-xx
===


-   Nuevas características

    -   Posibilidad de actualizar pedidos de equipos sin
        eliminar los existentes.

    -   Posibilidad de crear un comando de información sobre los valores de
        Pestaña Sistema.

-   Mejoras / Mejoras

    -   Soporte para nuevos módulos, definiciones de ozw
        y pedidos.

    -   Posibilidad de seleccionar la asociación predeterminada
        (sin instancia) en los módulos que admiten
        asociaciones de instancias múltiples.

    -   Verificación de la validez de los grupos de asociación al final
        de la entrevista.

    -   Recuperación del último nivel de las baterías cuando comienza el demonio.

-   Error corregido

    -   Corrección de la migración de la información de la batería.

    -   Corrección de la retroalimentación de información de la batería en
        la pantalla del equipo.

    -   Restauración del tipo de batería en configuraciones
        de módulos.

    -   Corrección de acciones en valores de tipo de botón en
        pantalla del módulo.

    -   Corrección de la recuperación de las traducciones de parámetros.

    -   Corrección de error vacío en la modificación de valores de tipo RAW
        (Código RFid).

    -   Visualización fija de valores pendientes
        para ser aplicado.

    -   Supresión de notificación de cambio de valor antes
        que no se aplica.

    -   Ya no muestra el candado en la pantalla del módulo si el módulo
        no es compatible con la clase de comando de seguridad.

    -   Aplicación de actualización manual en
        ajustes recomendados.

    -   Asistente de gestión de credenciales para lectores RFID.

    -   Corrección del asistente de detección de módulos desconocidos.

    -   Corrección de los asistentes de "Reanudar desde ..." y "Aplicar
        en ... "en la pestaña de configuración.

2017-06-20
===

-   Nuevas características

    -   N / A

-   Mejoras / Mejoras

    -   Agregue todas las configuraciones de módulos a
        nuevo formato.

-   Error corregido

    -   No pruebe si existe un nodeId durante la eliminación
        de una asociación.

    -   Restaurar la notificación de depósito pendiente en
        termostatos.

    -   Envío Pendiente Activación Escena 1.

    -   Ya no se muestra el candado en la pantalla de salud en
        módulos que no admiten la clase de comando de seguridad.

    -   Repetición de valor en los controles remotos antes del final de
        la entrevista (kyefob, minimote).

    -   Modificar un parámetro de la lista de tipos por valor mediante un
        Comando de acción.

    -   Modificar un parámetro en un módulo sin configuración definida.

2017-06-13
===

-   Nuevas características

    -   N / A

-   Mejoras / Mejoras

    -   Adición de la configuración del módulo Fibaro US

-   Error corregido

    -   N / A

2017-05-31
===

-   Nuevas características

    -   N / A

-   Mejoras / Mejoras

    -   N / A

-   Error corregido

    -   Corrección de la asignación de valores en formato RAW de códigos
        para lector RFid.

2017-05-23
===

-   Nuevas características

    -   Eliminación del modo maestro / esclavo. Reemplazado por plugin
        Enlace de libertad.

    -   Uso de una clave API privada para el complemento ZWave.

    -   Nuevo formato de los archivos de configuración en el mapeo de
        orden con libertad.

    -   Conversión automática de pedidos existentes a nuevos
        formato al instalar el complemento.

    -   Se agregó soporte para la clase de comando de escena central.

    -   Se agregó soporte para la clase de comando de operador de barrera.

-   Mejoras / Mejoras

    -   Revisión completa del servidor REST usando TORNADO.

        -   Modificación de todos los caminos existentes,
            los scripts deberán adaptarse si se utiliza la API de ZWave.

        -   Refuerzo de la seguridad, solo se escuchan llamadas en
            el servidor REST.

        -   Usar la clave API ZWave requerida para iniciar
            Solicitudes REST.

    -   Inhabilitar pruebas de salud (temporales).

    -   Desactivación (temporal) del motor de actualización
        configuraciones de módulos.

    -   Desactivación automática de la función Heal Network
        dos veces por semana (disminución en intercambios con
        el controlador).

    -   Optimizaciones de código de biblioteca Openzwave.

        -   Fibaro FGK101 ya no tiene que completar la entrevista para anunciar
            un cambio de estado.

        -   El comando del botón de liberación (detener un obturador) ya no fuerza
            actualizar todos los valores del módulo
            (disminución en la cola de mensajes).

        -   Posibilidad de notificar valores en la Clase de
            Comando de alarma (selección de tono de llamada en sirenas)

    -   Más demanda diaria de nivel de batería (menos de
        mensajes, ahorro de baterías).

    -   El nivel de la batería se envía directamente a la pantalla de la batería en
        informe de nivel de recepción.

-   Error corregido

    -   Actualización de todas las instancias después de un
        CC Switch ALL broadcast.

2016-08-26
===

-   Nuevas características

    -   Aucune

-   Mejoras / Mejoras

    -   Detección de RPI3 en actualización de dependencia.

    -   Active el modo de inclusión no seguro predeterminado.

-   Error corregido

    -   Prueba la información del fabricante en la pantalla de estado
        no más NOK.

    -   Pérdida de casillas de verificación en la pestaña Comandos de la
        página de equipos.

2016-08-17
===

-   Nuevas características

    -   Relanzamiento del demonio si la detección del controlador en tiempo de espera durante
        inicialización del controlador.

-   Mejoras / Mejoras

    -   Actualización de la biblioteca OpenZWave 1.4.2088.

    -   Corrección ortográfica.

    -   Rediseño de la pantalla del equipo con pestañas.

-   Error corregido

    -   Problema al mostrar ciertos módulos en la tabla de enrutamiento
        y gráfico de red.

    -   Módulos Vision Secure que no vuelven al modo de espera
        durante la entrevista.

    -   Instalación de dependencias en bucle (problema del lado de github).

2016-07-11
===

-   Nuevas características

    -   Soporte para la restauración del último nivel conocido en
        atenuarlos.

    -   Distinción de módulos FLiRS en la pantalla de salud.

    -   Solicitud agregada para actualizar las rutas de regreso
        al controlador.

    -   Asistente para aplicar los parámetros de configuración de un
        módulo a varios otros módulos.

    -   Identificación de los módulos de soporte Zwave +
        MANDO\_CLASE\_ZWAVE\_PLUS\_INFO.

    -   Visualización del estado de seguridad de los módulos que admiten
        MANDO\_CLASE\_SEGURIDAD.

    -   Adición de la posibilidad de seleccionar la instancia 0 del
        controlador para asociaciones de instancias múltiples.

    -   Asegurar todas las llamadas al servidor REST.

    -   Detección automática de dongle, en la página de configuración
        plugin.

    -   Diálogo de inclusión con opción de modo de inclusión para
        simplificar la inclusión segura.

    -   Teniendo en cuenta los equipos desactivados dentro del
        Motor de onda Z.

        -   Pantalla gris en la pantalla de estado sin análisis en
            nodo.

        -   Oculto en la tabla de red y el gráfico de red.

        -   Nodos deshabilitados, excluir pruebas de salud.

-   Mejoras / Mejoras

    -   Optimización de controles sanitarios.

    -   Red de optimización de gráficos.

    -   Detección mejorada del controlador principal para
        prueba grupal.

    -   Actualización a la biblioteca OpenZWave 1.4.296.

    -   Optimización de la refrigeración de fondo de las unidades.

    -   Actualización de fondo optimizada para
        los motores.

    -   Adaptación para Jeedom core 2.3

    -   Pantalla de estado, modificación del nombre de columna y advertencia
        en caso de no comunicación con un módulo.

    -   Optimización del servidor REST.

    -   Corrección de la ortografía de las pantallas, gracias @ Juan-Pedro
        aka: kiko.

    -   Actualización de la documentación del complemento.

-   Error corregido

    -   Corrección de posibles problemas al actualizar
        configuraciones de módulos.

    -   Gráfico de red, cálculo de saltos en la identificación del controlador
        principal y no asumir ID 1.

    -   Gestión del botón agregar una asociación grupal.

    -   Visualización de valores falsos en la pestaña Configuración.

    -   Ya no asume la fecha actual del estado de las baterías si no se recibe
        informe de equipo.

2016-05-30
===

-   Nuevas características

    -   Opción agregada para habilitar / deshabilitar controles
        sanitario en todos los módulos.

    -   Agregar una pestaña de Notificaciones para ver los últimos 25
        notificaciones del controlador.

    -   Agregar una ruta para recuperar la salud de un nodo.
        ip\_jeedom:8083 / ZWaveAPI / Run / devices \ [node\_id \]. GetHealth ()

    -   Agregar una ruta para recuperar la última notificación
        de un nudo.
        ip\_jeedom:8083 / ZWaveAPI / Run / devices \ [node\_id \]. GetLastNotification ()

-   Mejoras / Mejoras

    -   Permitir la selección de módulos FLiRS durante
        asociaciones directas.

    -   Permitir la selección de todas las instancias de módulos durante
        asociaciones directas.

    -   Actualización del contenedor Python de OpenZWave a la versión 0.3.0.

    -   Actualización de la biblioteca OpenZWave 1.4.248.

    -   No muestre una advertencia de activación caducada para
        módulos alimentados por batería.

    -   Validación de que un módulo es idéntico a nivel de ID para
        permitir la copia de parámetros.

    -   Simplificación del asistente para copiar parámetros.

    -   Ocultar valores de pestaña del sistema no existentes
        para ser exhibido.

    -   Visualización de la descripción de las capacidades del controlador.

    -   Actualización de la documentación.

    -   Corrección de la ortografía de la documentación, gracias
        @Juan-Pedro aka: kiko.

-   Error corregido

    -   Corrección ortográfica.

    -   Se corrigió la inclusión en modo seguro.

    -   Corrección de llamada asincrónica. (error: \ [Errno 32 \]
        Tubo roto)

2016-05-04
===

-   Nuevas características

    -   Opción agregada para desactivar la actualización de fondo
        atenuadores.

    -   Visualización de asociaciones con las que está asociado un módulo
        (encontrar uso).

    -   Soporte agregado para CC MULTI\_INSTANCE\_ASSOCIATION.

    -   Agregar una notificación de información al aplicar
        Establezca\_Point para utilizar el punto de ajuste solicitado en
        formulario de información de cmd.

    -   Agregar un asistente de configuración recomendado.

    -   Agregar opción para activar / desactivar el asistente
        configuración recomendada cuando se incluye
        nuevos módulos.

    -   Agregar opción para activar / desactivar la actualización de
        configuraciones de módulos cada noche.

    -   Adición de una ruta para gestionar múltiples instancias de asociación.

    -   Agregar etapa de consulta faltante.

    -   Se agregó validación de la selección del Dongle USB al
        comenzando el demonio.

    -   Adición de validación y prueba de devolución de llamada al inicio
        del demonio.

    -   Opción agregada para desactivar la actualización automática
        configuración del módulo.

    -   Agregar una ruta para modificar los seguimientos de registro en tiempo de ejecución
        el servidor REST. Note: sin efecto en el nivel OpenZWave.
        <http://ip_jeedom:8083/ZWaveAPI/Run/ChangeLogLevel(level>) level
        ⇒ 40:Error 20: Información de depuración 10

-   Mejoras / Mejoras

    -   Actualización del contenedor Python OpenZWave a la versión 0.3.0b9.

    -   Destacando grupos de asociaciones pendientes
        para ser aplicado.

    -   Actualización a la biblioteca OpenZWave 1.4.167.

    -   Modificación del sistema de asociación directa.

    -   Actualización de la documentación

    -   Capacidad para comenzar la regeneración de la detección de nodos
        para todos los módulos idénticos (marca y modelo).

    -   Mostrar en la pantalla de estado si hay elementos de configuración
        no se aplican.

    -   Mostrar en la pantalla del equipo si elementos de
        la configuración no se aplica.

    -   Mostrar en la pantalla de estado si un módulo de batería no tiene
        nunca desperté.

    -   Mostrar en la pantalla de estado si un módulo de batería ha excedido
        la hora de despertar esperada.

    -   Agregar trazas en caso de error de notificación.

    -   Mejor recuperación del estado de la batería.

    -   Resumen / cumplimiento de la salud para termostatos de batería.

    -   Mejor detección de módulos en baterías.

    -   Optimización del modo de depuración para el servidor REST.

    -   Forzar una actualización del estado del interruptor y el dímero
        después del envío de un comando switch all.

-   Error corregido

    -   Descubrimiento fijo de grupos de asociación.

    -   Corrección del error "Exception KeyError: (91,) en
        'libopenzwave.notif\_callback 'ignorado".

    -   Corrección de la selección de documentación del módulo para
        módulos con múltiples perfiles.

    -   Gestión de los botones de acción del módulo.

    -   Corrección de la descripción del nombre genérico de la clase.

    -   Corrección de la copia de seguridad del archivo zwcfg.

2016-03-01
===

-   Nuevas características

    -   Agregar el botón Configuración a través de la pantalla de administración
        equipo.

    -   Adición de nuevos estados de entrevista de módulo.

    -   Edición de etiquetas en IU.

-   Mejoras / Mejoras

    -   Mejor gestión de los botones de acciones del módulo.

    -   Agregar secciones de documentación.

    -   Optimización del mecanismo de detección del estado del demonio.

    -   Mecanismo de protesta durante la recuperación de la
        Descripción de los parámetros si contiene caracteres
        no valido.

    -   Nunca regrese a la información del estado de la batería en un
        módulo conectado a la red.

    -   Actualización de la documentación.

-   Error corregido

    -   Documentación Ortografía y correcciones gramaticales.

    -   Validación del contenido del archivo zwcfg antes de aplicarlo.

    -   Corrección de la instalación.

2016-02-12
===

-   Mejoras / Mejoras

    -   No hay alerta de nodo muerto si está deshabilitado.

-   Error corregido

    -   Corrección del retorno del estado del cable piloto de Fibaro.

    -   Corrección de un error que recrea los comandos durante la configuración
        al día.

2016.02.09
===

-   Nuevas características

    -   La adición de notificaciones push en el nodo\_event case, permite
        implementación de una información de cmd en CC 0x20 para recuperar
        evento en nodos.

    -   Ruta ForceRefresh agregada
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ForceRefresh()
        se puede usar en pedidos.

    -   Agregar la ruta SwitchAll
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[1\].commandClasses\[0xF0\].SwitchAll(&lt;int:state&gt;)
        disponible a través del controlador principal.

    -   Agregar la ruta ToggleSwitch
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ToggleSwitch()
        se puede usar en pedidos.

    -   Adición de una notificación push en caso de presunto nodo muerto.

    -   Ajout de la commande “refresh all parameters” dans
        la pestaña Configuración.

    -   Adición de la información del parámetro a la espera de ser aplicada.

    -   Agregar notificación de red.

    -   Adición de una leyenda en el gráfico de red.

    -   Adición de la función de cuidado de red a través de la tabla de enrutamiento.

    -   Eliminación automática de nodos fantasma con solo un clic.

    -   Gestión de acciones en nodo según el estado del nodo y el tipo.

    -   Gestión de acciones de red según el estado de la red.

    -   Actualización de la configuración automática del módulo todo
        las noches.

-   Mejoras / Mejoras

    -   Refactorización completa del código del servidor REST, optimización de
        velocidad de inicio, legibilidad, cumplimiento de la convención
        nombrando.

    -   Troncos cuadrados.

    -   Simplificación de la gestión de actualización manual de 5 minutos con
        posibilidad de aplicar en nodos con baterías.

    -   Actualización de la biblioteca OpenZWave en 1.4

    -   Modificación de la prueba de salud para revivir los presuntos nodos
        muerto más fácilmente sin las acciones del usuario.

    -   Uso de colores brillantes en la tabla de enrutamiento y
        gráfico de red.

    -   Estandarización de los colores de la tabla de enrutamiento y el
        gráfico de red.

    -   Optimización de la información en la página de salud Z-Wave de acuerdo con
        el estado de la entrevista.

    -   Mejor gestión de los parámetros de solo lectura o escritura
        solo en la pestaña Configuración.

    -   Advertencia mejorada en termostatos de batería.

-   Error corregido

    -   La temperatura convertida a Celsius devuelve la unidad C en su lugar
        de F.

    -   Corrección de la actualización de valores al inicio.

    -   Corrección de la actualización por valor en la pestaña Valores.

    -   Corrección de nombres genéricos de módulos.

    -   Corrección del ping en los nodos en Timeout durante el
        prueba de salud.
