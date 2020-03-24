Descripción
===========

Ce Plugin permite l'exploitation de Modulos Z-Wave por l'intermédiaire de
la librairie OpenZwave.

Introduction
============

Z-Wave communique en utilisant une technologie radio de faible puissance
DENTRO la bande de fréquence de 868,42 MHz. El es spécifiquement conçu
por les applications de domotique. El protocole radio Z-Wave es
optimisé por des échanges à faible bande passante (entre 9 y 40
kbit/ /s) entre des apporeils sur pile o alimentés sur secteur.

Z-Wave fonctionne DENTRO la gamme de fréquences sos-gigahertz, selon les
régions (868 MHz en Europe, 908 MHz aux US, y d'autres fréquences
suivant les bandes ISM des régions). La portée théorique es d'environ
30 mètres en intérieur y 100 mètres en extérieur. El réseau Z-Wave
utilise la technologie du maillage (mesh) por augmenter la portée y la
fiabilité. Z-Wave es conçu por être facilement intégré DENTRO les
produits électroniques de basse consommation, y compris les apporeils à
piles tels que les téléComandos, les détecteurs de fumée y capteurs de
Seguridad.

El Z-Wave+, apporte certaines améliorations dont une meilleure portée y
améliore la durée de vie des batteries entre autres. La
rétrocompatibilité es totale avec le Z-Wave.

Distances à respecter avec les autres sorces de signaux sans fil
-----------------------------------------------------------------

Els récepteurs radio doivent être positionnés à une distance minimum de
50 cm des autres sorces radioélectriques.

Ejemplos de sorces radioélectriques:

-   Ordinateurs

-   Els apporeils à micro-ondes

-   Els transformateurs électroniques

-   équipements audio y de matériel vidéo

-   Els dispositifs de pré-accoplement por lampes fluorescentes

> **Punta**
>
> Si vos disposez un Controlador USB (Z-Stick), El es recommandé de
> l'éloigner de la box à l'aide d'une simple rallonge USB de 1M por
> Ejemplo.

La distance entre d'autres émyteurs sans fil tels que les téléphones
sans fil o transmissions radio audio doit être d'au moins 3 mètres. Els
sorces de radio suivantes doivent être prises en compte :

-   Perturbations por commutateur de moteurs électriques

-   Interférences por des apporeils électriques défectueux

-   Els perturbations por les apporeils HF de sodage

-   dispositifs de traitement médical

Epaisseur efficace des murs
---------------------------

Els emplacements des Modulos doivent être choisis de telle manière que
la ligne de connexion directe ne fonctionne que sur une très corte
distance au travers de la matière (un mur), afin d'éviter au maximum les
atténuations.

![introduction01](../ /images/ /introduction01.png)

Els porties métalliques du bâtiment o des meubles peuvent bloquer les
ondes électromagnétiques.

Maillage y Rotage
-------------------

Els nœuds Z-Wave sur secteur peuvent transmytre y répéter les Mensajes
qui ne sont pas à portée directe du Controlador. Ce qui permite une plus
grande flexibilité de communication, même si il n'y a pas de connexion
sans fil directe o si une connexion es temporairement indisponible, à
cause d'un changement DENTRO la pièce o le bâtiment.

![introduction02](../ /images/ /introduction02.png)

El Controlador **Id 1** peut communiquer directement avec les nœuds 2, 3
y 4. El nœud 6 es en dehors de sa portée radio, cependant, il se
trove DENTRO la zone de coverture radio du nœud 2. Par conséquent, le
Controlador peut communiquer avec le nœud 6 via le nœud 2. De cyte
façon, le chemin du Controlador via le nœud 2 vers le nœud 6, es appelé
rote. Dans le cas où la Comunicación directa entre le nœud 1 y le
nœud 2 es bloquée, il y a encore une autre option por communiquer avec
le nœud 6, en utilisant le nœud 3 comme un autre répéteur du signal.

Il devient évident que plus l'on possède de nœuds secteur, plus les
options de rotage augmentent , y plus la stabilité du réseau augmente.
El protocole Z-Wave es capable de roter les Mensajes por
l'intermédiaire d'un maximum de quatre nœuds de répétition. C'es un
compromis entre la taille du réseau, la stabilité y la durée maximale
d'un Mensaje.

> **Punta**
>
> El es fortement recommandé en début d'installation d'avoir un ratio
> entre nœuds secteur y nœud sur piles de 2/ /3, afin d'avoir un bon
> maillage réseau. Privilégier des microModulos aux smart-plugs. Els
> micros Modulos seront à un emplacement définitif y ne seront pas
> débranchés, ils ont aussi en général une meilleure portée. Un bon
> déport es l'éclairage des zones communes. Il permityra de bien
> réportir les Modulos secteurs à des endroits stratégiques DENTRO votre
> domicile. Par la suite vos porrez ajoter autant de Modulos sur pile
> que sohaité, si vos rotes de base sont bonnes.

> **Punta**
>
> El **Gráfico de red** ainsi que la **Tabla de enrutamiento**
> permityent de visualiser la qualité de votre réseau.

> **Punta**
>
> Il existe des Modulos répéteur por combler des zones où aucun Modulo
> secteur n'a d'utilité.

Propriétés des apporeils Z-Wave
-------------------------------

|  | Vecinos | Rote | Fonctions possibles |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controlador | Connaît tos les voisins | A accès à la Tabla de enrutamiento complète | Peut communiquer avec tos les apporeils DENTRO le réseau, si une voie existe |
| Esclavo | Connaît tos les voisins | N'a pas d'information sur la Tabla de enrutamiento | Ne peut répondre au nœud qu'il a reçu le Mensaje. Par conséquent, ne peut pas envoyer des Mensajes non sollicités |
| Esclavos de rotage | Connaît tos ses voisins | A la connaissance portielle de la Tabla de enrutamiento | Peut répondre au nœud qu'il a reçu le Mensaje y peut envoyer des Mensajes non sollicités à un certain nombre de nœuds |

En résumé:

-   Chaque apporeil Z -Wave peut recevoir y accuser réception de
    Mensajes

-   Els Controladors peuvent envoyer des Mensajes à tos les nœuds du
    réseau, sollicités o non « El maître peut porler quand il veut y à
    qui il veut »

-   Els esclaves ne peuvent pas envoyer des Mensajes non sollicités,
    mais seulement une réponse aux demandes «L'esclave ne porle que si
    on le lui demande »

-   Els esclaves de rotage peuvent répondre à des demandes y ils sont
    autorisés à envoyer des Mensajes non sollicités à certains nœuds que
    le Controlador a prédéfini « L'esclave es tojors un esclave, mais
    sur autorisation, il peut porler »

Configuración del Plugin
=======================

Après le téléchargement du Plugin, il vos suffit de l'activer y de le
Configurar.

![Configuración01](../ /images/ /Configuración01.png)

Une fois activé, le démon devrait se lancer. El Plugin es préconfiguré
avec des valeurs por défaut ; vos n'avez normalement plus rien à faire.
Cependant vos povez modifier la Configuración.

Dependencias
-----------

Cyte portie permite valider y d'installer les Dependencias requises
au bon fonctionnement du Plugin Zwave (aussi bien en local qu'en
déporté, ici en local) ![Configuración02](../ /images/ /Configuración02.png)

-   Un Estado **Bueno** confirme que les Dependencias sont satisfaites.

-   Si le statut es **NBueno**, il faudra réinstaller les Dependencias à
    l'aide du boton ![Configuración03](../ /images/ /Configuración03.png)

> **Punta**
>
> La mise al día des Dependencias peut prendre plus de 20 minutes selon
> votre matériel. La progression es affichée en temps réel y un log
> **Openzwave\_update** es accessible.

> **Importante**
>
> La mise al día des Dependencias es normalement à effectuer seulement
> si le Estado es **NBueno**, mais El es totefois possible, por régler
> certains problèmes, d'être appelé à refaire l'installation des
> Dependencias.

> **Punta**
>
> Si vos êtes en modo déporté, les Dependencias du démon local peuvent
> être NBueno, c'es tot à fait normal.

Demonio
-----

Cyte portie permite valider l'état actuel du o des démons y de
Configurar la gesion automatique de ceux-ci.
![Configuración04](../ /images/ /Configuración04.png) El démon local y
l'ensemble des démons déportés seront affichés avec leurs différentes
Informaciónrmación

-   El **Estado** indique que le démon es actuellement en fonction.

-   La **Configuración** indique si la Configuración du démon
    es valide.

-   El botón **(Re)Iniciar** permite forcer le redémarrage du
    Plugin, en modo normal o de le lancer une première fois.

-   El botón **Dyenido**, visible seulement si la gesion automatique
    es désactivado, force l'arrêt du démon.

-   La **Gesión automática** permite à Jeedom de lancer automatiquement
    le démon au démarrage de Jeedom, ainsi que de le relancer en cas
    de problème.

-   El **Última ejecución** es comme son nom l'indique la date du
    dernier lancement connue du demon.

Registro
---

Cyte portie permite choisir le niveau de log ainsi que d'en consulter
le contenu.

![Configuración05](../ /images/ /Configuración05.png)

Sélectionner le niveau puis sauvegarder, le démon sera alors relancé
avec les instructions y traces sélectionnées.

El niveau **Depurar** o **Información** peuvent être utiles por comprendre
porquoi le démon plante o ne remonte pas une valeur.

> **Importante**
>
> En modo **Depurar** le démon es très verbeux, El es recommandé
> d'utiliser ce modo seulement si vos devez diagnostiquer un problème
> porticulier. Il n'es pas recommandé de laisser torner le démon en
> **Depurar** en permanence, si on utilise une **SD-Card**. Une fois le
> debug terminé, il ne faut pas oblier de ryorner sur un niveau moins
> élevé comme le niveau **Error** qui ne remonte que d'éventuelles
> errores.

Configuración
-------------

Cyte portie permite Configurar les poramètres généraux du Plugin
![Configuración06](../ /images/ /Configuración06.png)

-   **Principal** :

    -   **Eliminar automáticamente los dispositivos excluidos** :
        L'option Oui, permite supprimer les périphériques exclus du
        réseau Z-Wave. L'option Non, permite conserver les équipements
        DENTRO Jeedom même s'ils ont été exclus du réseau. L'équipement
        devra être alors supprimé manuellement o réutilisé en lui
        assignant un novel Identificación Z-Wave si on exécute une migration du
        Controlador principal.

    -   **Appliquer le jeu de Configuración recommandé à l'inclusión** :
        option por appliquer directement à l'inclusión le jeu de
        Configuración recommandé por l'équipe Jeedom (conseillée)

    -   **Desactivar la actualización en segundo plano de las unidades** :
        Ne pas demander de Refrescante des variateurs
        en arrière-plan.

    -   **Ciclo (s)** : permite définir la fréquence des remontées
        à jeedom.

    -   **Puerto de llave Z-Wave** : le port USB sur lequel votre interface
        Z-Wave es connectée. Si vos utilisez le Razberry, vos avez,
        en fonction de votre architecture (RPI o Jeedomboard) les 2
        possibilités à la fin de la liste.

    -   **Port du Serveur** (modification dangereuse, doit avoir la même
        valeur sur tos les Jeedoms déportés Z-Wave) : permite
        modifier le port de communication interne du démon.

    -   **Copias de seguridad** : permite gérer les backups du Expediente de
        topologie réseaux (voir plus bas)

    -   **Config Modulos** : permite récupérer, manuellement, les
        Expedientes de Configuracións OpenZWave avec les poramètres des
        Modulos ainsi que la définition des Comandos de Modulos por
        leurs utilisations.

        > **Punta**
        >
        > La récupération des Configuracións de Modulo s'effectue
        > automatiquement chaque nuit.

        > **Punta**
        >
        > El redémarrage du démon suite à la mise al día des
        > Configuracións de Modulo es inutile.

        > **Importante**
        >
        > Si vos avez un Modulo non reconnu y qu'une mise al día de
        > Configuración vient d'être appliquée, vos povez manuellement
        > lancer la récupération des Configuracións de Modulos.

Une fois les Configuracións récupérées, il faudra selon les changements
apportés:

-   Por un noveau Modulo sans Configuración ni Comando : exclure y
    ré-inclure le Modulo.

-   Por un Modulo por lequel seuls les poramètres ont été mis al día :
    lancer la régénération de la détection du nœud, via l'pesaña Acciones
    du Modulo (le Plugin doit redémarrer).

-   Por un Modulo dont le « mapping » de Comandos a été corrigé : la
    lope sur les Comandos, voir plus bas.

    > **Punta**
    >
    > Dans le dote, exclure y ré-inclure le Modulo es recommandé.

N'obliez pas de ![Configuración08](../ /images/ /Configuración08.png) si
vos effectuez une modification.

> **Importante**
>
> Si vos utilisez Ubuntu : Por que le démon fonctionne, il faut
> absolument avoir ubuntu 15.04 (les versions inférieures ont un bug y
> le démon n'arrive pas à se lancer). Attention si vos faites une mise
> al día à portir de 14.04 il faut une fois en 15.04 relancer
> l'installation des Dependencias.

> **Importante**
>
> La sélection du Puerto de llave Z-Wave en modo de détection automatique,
> **Auto**, ne fonctionne que por les dongles USB.

Paneau Mobile
-------------

![Configuración09](../ /images/ /Configuración09.png)

Permy d'afficher o non le panel mobile lors que vos utiliser
l'application sur un téléphone.

Configuración del equipo
=============================

La Configuración des équipements Z-Wave es accessible à portir du menu
Plugin :

![appliance01](../ /images/ /appliance01.png)

Ci-dessos un Ejemplo d'une page du Plugin Z-Wave (présentée avec
quelques équipements) :

![appliance02](../ /images/ /appliance02.png)

> **Punta**
>
> Comme à beaucop d'endroits sur Jeedom, placer la soris tot à gauche
> permite faire apporaître un menu d'accès rapide (vos povez, à
> portir de votre profil, le laisser tojors visible).

> **Punta**
>
> Els botons sur la ligne tot en haut **Sincronizar**,
> **Réseau-Zwave** y **Salud**, sont visibles seulement si vos êtes en
> modo **Expert**. ![appliance03](../ /images/ /appliance03.png)

Principal
-------

Aquí encontrarás toda la configuración de tu equipo :

![appliance04](../ /images/ /appliance04.png)

-   **Nombre del equipo** : nom de votre Modulo Z-Wave.

-   **Objyo padre** : indique l'objy porent auquel
    apportient l'équipement.

-   **Categoría** : categorías de equipos (puede pertenecer a
    plusieurs catégories).

-   **Activar** : permite rendre votre équipement actif.

-   **Visible** : le rend visible sur le dashboard.

-   **Identificación de nodo** : Identificación du Modulo sur le réseau Z-Wave. Ceci peut être
    utile si, por Ejemplo, vos volez remplacer un Modulo défaillant.
    Il suffit d'inclure le noveau Modulo, de récupérer son Identificación, y le
    mytre à la place de l'Identificación de l'ancien Modulo y enfin de supprimer
    le noveau Modulo.

-   **Modulo** : ce champ n'apporaît que s'il existe différents types de
    Configuración por votre Modulo (cas por les Modulos povant faire
    fils pilotes por Ejemplo). Il vos permite choisir la
    Configuración à utiliser o de la modifier por la suite

-   **Marque** : fabricant de votre Modulo Z-Wave.

-   **Configuración** : fenêtre de Configuración des poramètres du
    Modulo

-   **Asistente** : disponible uniquement sur certains Modulos, il vos
    aide à Configurar le Modulo (cas sur le zipato keyboard por Ejemplo)

-   **Documentación** : ce boton vos permite d'ovrir directement la
    documentation Jeedom concernant ce Modulo.

-   **Borrar** : Permy de supprimer un équipement ainsi que tos ces
    Comandos rattaché sans l'exclure du réseau Z-Wave.

> **Importante**
>
> La suppression d'un équipement n'engendre pas une Exclusión du Modulo
> sur le Controlador. ![appliance11](../ /images/ /appliance11.png) Un
> équipement supprimé qui es tojors rattaché à son Controlador sera
> automatiquement recréé suite à la sincronización.

Comandos
---------

Ci-dessos vos ryrovez la liste des Comandos :

![appliance05](../ /images/ /appliance05.png)

> **Punta**
>
> En fonction des types y sos-types, certaines options peuvent être
> absentes.

-   le nom affiché sur le dashboard

-   Icono : DENTRO le cas d'une action permite choisir une Icono à
    afficher sur le dashboard au lieu du texte

-   valeur de la Comando : DENTRO le cas d'une Comando type action, sa
    valeur peut être liée à une Comando de type info, c'es ici que
    cela se configure. Ejemplo por une lampe l'intensité es liée à son
    état, cela permite au widgy d'avoir l'état réel de la lampe.

-   le type y le sos-type.

-   l'instance de cyte Comando Z-Wave (réservée aux experts).

-   la classe de la Comando Z-Wave (réservée aux experts).

-   l'index de la valeur (réservée aux experts).

-   la Comando en elle-même (réservée aux experts).

-   "Valeur de ryor d'état" y "Durée avant ryor d'état" : permite
    d'indiquer à Jeedom qu'après un changement sur l'information sa
    valeur doit revenir à Y, X min après le changement. Ejemplo : DENTRO
    le cas d'un détecteur de présence qui n'émy que lors d'une
    détection de présence, El es utile de mytre por Ejemplo 0 en
    valeur y 4 en durée, por que 4 min après une détection de
    movement (y si ensuite, il n'y en a pas eu de novelles) Jeedom
    remyte la valeur de l'information à 0 (plus de movement détecté).

-   Guardar historial : permite d'historiser la donnée.

-   Mostrar : Muesra la donnée sur le dashboard.

-   Invertir : permite d'inverser l'état por les types binaires.

-   Unidad : unité de la donnée (peut être vide).

-   Min/ /Max : bornes de la donnée (peuvent être vides).

-   Configuración avancée (pyites roes crantées) : Muesra
    la Configuración avancée de la Comando (méthode
    d'historisation, widgy…​).

-   Probar : Se usa pora probar el comando.

-   Borrar (signe -) : permite supprimer la Comando.

> **Importante**
>
> El botón **Probar** DENTRO le cas d'une Comando de type Información, ne va
> pas interroger le Modulo directement mais la valeur disponible DENTRO le
> Cubierta de Jeedom. El tes ryornera la bonne valeur seulement si le
> Modulo en quesion a transmis une novelle valeur correspondant à la
> définition de la Comando. El es alors tot à fait normal de ne pas
> obtenir de résultat suite à la création d'une novelle Comando Información,
> spécialement sur un Modulo sur pile qui notifie rarement Jeedom.

La **lope**, disponible DENTRO l'pesaña général, permite recréer
l'ensemble des Comandos por le Modulo en cors.
![appliance13](../ /images/ /appliance13.png) Si aucune Comando n'es
présente o si les Comandos sont erronées la lope devrait remédier à
la situation.

> **Importante**
>
> La **lope** va supprimer les Comandos existantes. Si les Comandos
> étaient utilisées DENTRO des scénarios, vos devrez alors corriger vos
> scénarios aux autres endroits où les Comandos étaient exploitées.

Jeux de Comandos
-----------------

Certains Modulos possèdent plusieurs jeux de Comandos préconfigurées

![appliance06](../ /images/ /appliance06.png)

Vos povez les sélectionner via les choix possibles, si le Modulo le
permite.

> **Importante**
>
> Vos devez effectuer la lope por appliquer le noveau jeux de
> Comandos.

Documentación y Asistente
--------------------------

Por un certain nombre de Modulos, une aide spécifique por la mise en
place ainsi que des recommandations de poramètres sont disponibles.

![appliance07](../ /images/ /appliance07.png)

El botón **Documentación** permite d'accéder à la documentation
spécifique du Modulo por Jeedom.

Des Modulos porticuliers disposent aussi d'un assistant spécifique afin
de faciliter l'application de certains poramètres o fonctionnements.

El botón **Asistente** permite d'accéder à l'écran assistant spécifique
du Modulo.

Configuración recomendada
-------------------------

![appliance08](../ /images/ /appliance08.png)

Permy d'appliquer un jeu de Configuración recommandée por l'équipe
Jeedom.

> **Punta**
>
> Lors de leur inclusión, les Modulos ont les poramètres por défaut du
> constructeur y certaines fonctions ne sont pas activados por défaut.

Els éléments suivants, selon le cas, seront appliqués por simplifier
l'utilisation du Modulo.

-   **Configuraciones** permityant la mise en service rapide de l'ensemble
    des fonctionnalités du Modulo.

-   **Grupos d'association** requis au bon fonctionnement.

-   **Intervalle de réveil**, por les Modulos sur pile.

-   Activation du **rafraîchissement manuel** por les Modulos ne
    remontant pas d'eux-mêmes leurs changements d'états.

Por appliquer le jeu de Configuración recommandé, cliquer sur le boton
: **Configuración recomendada**, puis confirmer l'application des
Configuracións recommandées.

![appliance09](../ /images/ /appliance09.png)

L'assistant active les différents éléments de Configuracións.

Une confirmation du bon dérolement sera affichée sos forme de bandeau

![appliance10](../ /images/ /appliance10.png)

> **Importante**
>
> Els Modulos sur piles doivent être réveillés por appliquer le jeu de
> Configuración.

La page de l'équipement vos informe si des éléments n'ont pas encore
été activés sur le Modulo. Veuillez-vos référer à la documentation du
Modulo por le réveiller manuellement o attendre le prochain cycle de
réveil.

![appliance11](../ /images/ /appliance11.png)

> **Punta**
>
> El es possible d'activer automatiquement l'application du jeu de
> Configuración recommandé lors de l'inclusión de noveau Modulo, voir
> la section Configuración del Plugin por plus de détails.

Configuración des Modulos
=========================

C'es ici que vos ryroverez totes les Informaciónrmación sur votre Modulo

![node01](../ /images/ /node01.png)

La fenêtre possède plusieurs pesañas :

Resumen
------

Fornit un résumé comply de votre nœud avec différentes Informaciónrmación
sur celui-ci, comme por Ejemplo l'état des demandes qui permite savoir
si le nœud es en attente d'information o la liste des nœuds voisins.

> **Punta**
>
> Sur cy pesaña El es possible d'avoir des alertes en cas de détection
> possible d'un soci de Configuración, Jeedom vos indiquera la marche
> à suivre por corriger. Il ne faut pas confondre une alerte avec une
> erreur, l'alerte es DENTRO une majorité des cas, une simple
> recommandation.

Valores
-------

![node02](../ /images/ /node02.png)

Vos ryrovez ici totes les Comandos y états possibles sur votre
Modulo. Ils sont ordonnés por instance y classe de Comando puis index.
El « mapping » des Comandos es entièrement basé sur ces Informaciónrmación.

> **Punta**
>
> Forcer la mise al día d'une valeur. Els Modulos sur pile vont
> rafraichir une valeur seulement au prochain cycle de réveil. El es
> totefois possible de réveiller à la main un Modulo, voir la
> Documentación del módulo.

> **Punta**
>
> El es possible d'avoir plus de Comandos ici que sur Jeedom, c'es
> tot à fait normal. Dans Jeedom les Comandos ont été présélectionnées
> por vos.

> **Importante**
>
> Certains Modulos n'envoient pas automatiquement leurs états, il faut
> DENTRO ce cas activer le Refrescante manuel à 5 minutes sur la o
> les valeurs sohaitées. El es recommandé de laisser en automatique le
> Refrescante. Abuser du Refrescante manuel peut impacter
> fortement les performances du réseau Z-Wave, utilisez seulement por
> les valeurs recommandées DENTRO la documentation spécifique Jeedom.
> ![node16](../ /images/ /node16.png) L'ensemble des valeurs (index) de
> l'instance d'une Comando classe sera remonté, en activant le
> Refrescante manuel sur le plus pyit index de l'instance de la
> Comando classe. Répéter por chaque instance si nécessaire.

Configuraciones
----------

![node03](../ /images/ /node03.png)

Vos ryrovez ici totes les possibilités de Configuración des
poramètres de votre Modulo ainsi que la possibilité de copier la
Configuración d'un autre nœud déjà en place.

Lorsqu'un poramètre es modifié, la ligne correspondante passe en jaune,
![node04](../ /images/ /node04.png) le poramètre es en attente d'être
appliqué.

Si le Modulo accepte le poramètre, la ligne redevient transporente.

Si totefois le Modulo refuse la valeur, la ligne passera alors en roge
avec la valeur appliquée ryornée por le Modulo.
![node05](../ /images/ /node05.png)

A l'inclusión, un noveau Modulo es détecté avec les poramètres por
défaut du constructeur. Sur certains Modulos, des fonctionnalités ne
seront pas actives sans modifier un o plusieurs poramètres.
Référez-vos à la documentation du constructeur y à nos recommandations
afin de bien poramétrer vos noveaux Modulos.

> **Punta**
>
> Els Modulos sur pile vont appliquer les changements de poramètres
> seulement au prochain cycle de réveil. El es totefois possible de
> réveiller à la main un Modulo, voir la Documentación del módulo.

> **Punta**
>
> La Comando **Reprendre de…​** vos permite reprendre la Configuración
> d'un autre Modulo identique, sur le Modulo en cors.

![node06](../ /images/ /node06.png)

> **Punta**
>
> La Comando **Appliquer sur…​** vos permite d'appliquer la
> Configuración actuelle du Modulo sur un o plusieurs Modulos
> identiques.

![node18](../ /images/ /node18.png)

> **Punta**
>
> La Comando **Actualizar configuraciones** force le Modulo à actualiser
> les poramètres sauvegardés DENTRO le Modulo.

Si aucun Expediente de Configuración es définie por le Modulo, un
assistant manuel vos permite d'appliquer des poramètres au Modulo.
![node17](../ /images/ /node17.png) Veillez vos référer à la documentation
du fabricant por connaitre la définition de l'index, valeur y taille.

Asociaciones
------------

C'es ici que se ryrove la gesion des gropes d'association de votre
Modulo.

![node07](../ /images/ /node07.png)

Els Modulos Z-Wave peuvent contrôler d'autres Modulos Z-Wave, sans
passer por le Controlador ni Jeedom. La relation entre un Modulo de
contrôle y un autre Modulo es appelée association.

Afin de contrôler un autre Modulo, le Modulo de Comando a besoin de
maintenir une liste des apporeils qui recevront le contrôle des
Comandos. Ces listes sont appelées gropes d'association y elles sont
tojors liées à certains événements (por Ejemplo le boton pressé, les
déclencheurs de capteurs, …​ ).

Dans le cas où un événement se produit, tos les périphériques
enregistrés DENTRO le grope d'association concerné recevront une Comando
Basic.

> **Punta**
>
> Voir la Documentación del módulo, por comprendre les différents
> gropes d'associations possibles y leur comportement.

> **Punta**
>
> La majorité des Modulos ont un grope d'association qui es réservé
> por le Controlador principal, El es utilisé por remonter les
> Informaciónrmación au Controlador. Il se nomme en général : **Report** o
> **LifeLine**.

> **Punta**
>
> El es possible que votre Modulo ne possède aucun grope.

> **Punta**
>
> La modification des gropes d'associations d'un Modulo sur pile sera
> appliquée au prochain cycle de réveil. El es totefois possible de
> réveiller à la main un Modulo, voir la Documentación del módulo.

Por connaitre avec quels autres Modulos le Modulo en cors es associé,
il suffit de cliquer sur le menu **Asociado con qué módulos**

![node08](../ /images/ /node08.png)

L'ensemble des Modulos utilisant le Modulo en cors ainsi que le nom des
gropes d'associations seront affichés.

**Asociaciones multi-instances**

certain Modulo supporte une Comando classe multi-instance associations.
Lorsqu'un Modulo supporte cyte CC, El es possible de spécifier avec
quelle instance on sohaite créer l'association

![node09](../ /images/ /node09.png)

> **Importante**
>
> Certains Modulos doivent être associés à l'instance 0 du Controlador
> principale afin de bien fonctionner. Por cyte raison, le Controlador
> es présent avec y sans l'instance 0.

Sistemas
--------

Ongly regropant les poramètres systèmes du Modulo.

![node10](../ /images/ /node10.png)

> **Punta**
>
> Els Modulos sur piles se réveillent à des cycles réguliers, appelés
> intervalles de réveil (Wakeup Interval). L'intervalle de réveEl es un
> compromis entre le temps maximal de vie de la batterie y les réponses
> sohaitées du dispositif. Por maximiser la durée de vie de vos
> Modulos, adapter la valeur Wakeup Interval por Ejemplo à 14400
> secondes (4h), voir encore plus élevé selon les Modulos y leur usage.
> ![node11](../ /images/ /node11.png)

> **Punta**
>
> Els Modulos **Interrupteur** y **Variateur** peuvent implémenter une
> Classe de Comando spéciale appelée **SwitchAll** 0x27. Vos povez en
> modifier ici le comportement. Selon le Modulo, plusieurs options sont
> à disposition. La Comando **SwitchAll On/ /OFF** peut être lancée via
> votre Modulo Controlador principal.

Acciones
-------

Permy d'effectuer certaines actions sur le Modulo.

![node12](../ /images/ /node12.png)

Certaines actions seront actives selon le type de Modulo y ses
possibilités o encore selon l'état actuel du Modulo comme por Ejemplo
s'El es présumé mort por le Controlador.

> **Importante**
>
> Il ne faut pas utiliser les actions sur un Modulo si on ne sait pas ce
> que l'on fait. Certaines actions sont irréversibles. Las acciones
> peuvent aider à la résolution de problèmes avec un o des Modulos
> Z-Wave.

> **Punta**
>
> La **Régénération de la détection du noeud** permite détecter le
> Modulo por reprendre les derniers jeux de poramètres. Cyte action
> es requise lorsqu'on vos informe qu'une mise a jor de poramètres y
> o de comportement du Modulo es requit por le bon fonctionnement. La
> Régénération de la détection du noeud implique un redémarrage du
> réseau, l'assistant l'effectue automatiquement.

> **Punta**
>
> Si vos avez plusieurs Modulos identiques dont El es requis
> d'exécuter la **Régénération de la détection du noeud**, El es
> possible de la lancer une fois por tos les Modulos identiques.

![node13](../ /images/ /node13.png)

> **Punta**
>
> Si un Modulo sur pile n'es plus joignable y que vos sohaitez
> l'exclure, que l'Exclusión ne s'effectue pas, vos povez lancer
> **Borrar le noeud fantôme** Un assistant effectuera différentes
> actions afin de supprimer le Modulo dit fantôme. Cyte action implique
> de redémarrer le réseau y peut prendre plusieurs minutes avant d'être
> complétée.

![node14](../ /images/ /node14.png)

Une fois lancé, El es recommandé de fermer l'écran de Configuración du
Modulo y de surveiller la suppression du Modulo via l'écran de santé
Z-Wave.

> **Importante**
>
> Seul les Modulos sur pile peuvent être supprimés via cyte assistant.

Estadísticas
------------

Cy pesaña donne quelques statistiques de communication avec le nœud.

![node15](../ /images/ /node15.png)

Peut être intéressant en cas de Modulos qui sont présumés morts por le
Controlador "Dead".

inclusión / / Exclusión
=====================

A sa sortie d'usine, un Modulo ne fait portie d'aucun réseau Z-Wave.

Modo de inclusión
--------------

El Modulo doit se joindre à un réseau Z-Wave existant por communiquer
avec les autres Modulos de ce réseau. Ce processus es appelé
**Inclusión**. Els périphériques peuvent également sortir d'un réseau.
Ce processus es appelé **Exclusión**. Els deux processus sont initiés
por le Controlador principal du réseau Z-Wave.

![addremove01](../ /images/ /addremove01.png)

Ce boton vos permite passer en modo inclusión por ajoter un Modulo
à votre réseau Z-Wave.

Vos povez choisir le modo d'inclusión après avoir cliqué le boton
**Inclusión**.

![addremove02](../ /images/ /addremove02.png)

Depuis l'apporition du Z-Wave+, El es possible de sécuriser les
échanges entre le Controlador y les noeuds. El es donc recommandé de
faire les inclusións en modo **Seguro**.

Si totefois, un Modulo ne peut être inclus en modo Seguro, veuillez
l'inclure en modo **No es seguro**.

Une fois en modo inclusión : Jeedom vos le signale.

\[TIP\] Un Modulo 'non Seguro' peut Comandor des Modulos 'non
Seguros'. Un Modulo 'non Seguro' ne peut pas Comandor un Modulo
'Seguro'. Un Modulo 'Seguro' porra Comandor des Modulos 'non
Seguros' sos réserve que l'émyteur le supporte.

![addremove03](../ /images/ /addremove03.png)

Une fois l'assistant lancé, il faut en faire de même sur votre Modulo
(se référer à la documentation de celui-ci por le passer en modo
inclusión).

> **Punta**
>
> Tant que vos n'avez pas le bandeau, vos n'êtes pas en modo
> inclusión.

Si vos re cliquez sur le boton, vos sortez du modo inclusión.

> **Punta**
>
> El es recommandé, avant l'inclusión d'un noveau Modulo qui serait
> "noveau" sur le marché, de lancer la Comando **Config Modulos** via
> l'écran de Configuración du Plugin. Cyte action va récupérer
> l'ensemble des dernières versions des Expedientes de Configuracións
> openzwave ainsi que le mapping de Comandos Jeedom.

> **Importante**
>
> Lors d'une inclusión, El es conseillé que le Modulo soit à proximité
> du Controlador principal, soit à moins d'un mètre de votre jeedom.

> **Punta**
>
> Certains Modulos requièrent obligatoirement une inclusión en modo
> **Seguro**, por Ejemplo por les serrures de porte.

> **Punta**
>
> A noter que l'interface mobile vos donne aussi accès à l'inclusión,
> le panel mobile doit avoir été activé.

> **Punta**
>
> Si le Modulo apportient déjà à un réseau, suivez le processus
> d'Exclusión avant de l'inclure DENTRO votre réseau. Sinon l'inclusión de
> ce Modulo va échoer. El es d'ailleurs recommandé d'exécuter une
> Exclusión avant l'inclusión, même si le produit es neuf, sorti du
> carton.

> **Punta**
>
> Une fois le Modulo à son emplacement définitif, il faut lancer
> l'action soigner le réseau, afin de demander à tos les Modulos de
> rafraichir l'ensemble des voisins.

Modo de exclusión
--------------

![addremove04](../ /images/ /addremove04.png)

Ce boton vos permite passer en modo Exclusión, cela por ryirer un
Modulo de votre réseau Z-Wave, il faut en faire de même avec votre
Modulo (se référer à la documentation de celui-ci por le passer en modo
Exclusión).

![addremove05](../ /images/ /addremove05.png)

> **Punta**
>
> Tant que vos n'avez pas le bandeau, vos n'êtes pas en modo
> Exclusión.

Si vos re cliquez sur le boton, vos sortez du modo Exclusión.

> **Punta**
>
> A noter que l'interface mobile vos donne aussi accès à l'Exclusión.

> **Punta**
>
> Un Modulo n'a pas besoin d'être exclu por le même Controlador sur
> lequel il a été préalablement inclus. D'où le fait qu'on reComando
> d'exécuter une Exclusión avant chaque inclusión.

Sincronizar
------------

![addremove06](../ /images/ /addremove06.png)

Boton permityant de synchroniser les Modulos du réseau Z-Wave avec les
équipements Jeedom. Els Modulos sont associés au Controlador principal,
les équipements DENTRO Jeedom sont créés automatiquement lors de leur
inclusión. Ils sont aussi supprimés automatiquement lors de l'Exclusión,
si l'option **Eliminar automáticamente los dispositivos excluidos** es
activado.

Si vos avez inclus des Modulos sans Jeedom (requiert un dongle avec
pile comme le Aeon-labs Z-Stick GEN5), une sincronización sera
nécessaire suite au branchement de la clé, une fois le démon démarré y
fonctionnel.

> **Punta**
>
> Si vos n'avez pas l'image o que Jeedom n'a pas reconnu votre Modulo,
> ce boton peut permityre de corriger (sos réserve que l'interview du
> Modulo soit complète).

> **Punta**
>
> Si sur votre Tabla de enrutamiento y/ /o sur l'écran de santé Z-Wave, vos
> avez un o des Modulos nommés avec leur **nom générique**, la
> sincronización permityra de remédier à cyte situation.

El botón Sincronizar n'es visible qu'en modo expert :
![addremove07](../ /images/ /addremove07.png)

Réseaux Z-Wave
==============

![nywork01](../ /images/ /nywork01.png)

Vos ryrovez ici des Informaciónrmación générales sur votre réseau Z-Wave.

![nywork02](../ /images/ /nywork02.png)

Resumen
------

El premier pesaña vos donne le résumé de base de votre réseau Z-Wave,
vos ryrovez notamment l'état du réseau Z-Wave ainsi que le nombre
d'éléments DENTRO la file d'attente.

**Informaciónrmación**

-   Donne des Informaciónrmación générales sur le réseau, la date de
    démarrage, le temps requis por l'obtention du réseau DENTRO un état
    dit fonctionnel.

-   El nombre de nœuds total du réseau ainsi que le nombre qui dorment
    DENTRO le moment.

-   L'intervalle des demandes es associé au Refrescante manuel. Il
    es prédéfini DENTRO le moteur Z-Wave à 5 minutes.

-   Els voisins du Controlador.

**Estado**

![nywork03](../ /images/ /nywork03.png)

Un ensemble d'Informaciónrmación sur l'état actuel du réseau, à savoir :

-   Estado actuel, peut-être **Driver Initialised**, **Topology loaded**
    o **Ready**.

-   Queue sortante, indique le nombre de Mensajes en queue DENTRO le
    Controlador en attente d'être envoyé. Cyte valeur es généralement
    élevée durant le démarrage du réseau lorsque l'état es encore en
    **Driver Initialised**.

Une fois que le réseau a au minimum atteint **Topology loaded**, des
mécanismes internes au serveur Z-Wave vont forcer des mises al día de
valeurs, El es alors tot-à-fait normal de voir monter le nombre de
Mensajes. Celui-ci va rapidement ryorner à 0.

> **Punta**
>
> El réseau es dit fonctionnel au moment où il atteint le statut
> **Topology Loaded**, c'es-à-dire que l'ensemble des nœuds secteurs
> ont complété leurs interviews. Selon le nombre de Modulos, la
> réportition pile/ /secteur, le choix du dongle USB y le PC sur lequel
> torne le Plugin Z-Wave, le réseau va atteindre cyte état entre une
> y cinq minutes.

Un réseau **Ready**, signifie que tos les nœuds secteur y sur pile ont
complété leur interview.

> **Punta**
>
> Selon les Modulos dont vos disposez, El es possible que le réseau
> n'atteigne jamais de lui-même le statut **Ready**. Els téléComandos,
> por Ejemplo, ne se réveillent pas d'elles-mêmes y ne compléteront
> jamais leur interview. Dans ce genre de cas, le réseau es tot-à-fait
> opérationnel y même si les téléComandos n'ont pas complété leur
> interview, elles assurent leurs fonctionnalités au sein du réseau.

**Capacidades**

Permy de savoir si le Controlador es un Controlador principal o
secondaire.

**Sistema**

Affiche diverses Informaciónrmación système.

-   Informaciónrmation sur le port USB utilisé.

-   Version de la librairie OpenZwave

-   Version de la librairie Python-OpenZwave

Acciones
-------

![nywork05](../ /images/ /nywork05.png)

Vos ryrovez ici totes les actions possibles sur l'ensemble de votre
réseau Z-Wave. Chaque action es accompagnée d'une description sommaire.

> **Importante**
>
> Certaines actions sont vraiment risquées voire irréversibles, l'équipe
> Jeedom ne porra être tenue responsable en cas de mauvaise
> manipulation.

> **Importante**
>
> Certains Modulos requièrent une inclusión en modo Seguro, por
> Ejemplo por les serrures de porte. L'inclusión Seguroe doit être
> lancée via l'action de cy écran.

> **Punta**
>
> Si une action ne peut être lancée, elle sera désactivado jusqu'au
> moment où elle porra être à noveau exécutée.

Estadísticas
------------

![nywork06](../ /images/ /nywork06.png)

Vos ryrovez ici les statistiques générales sur l'ensemble de votre
réseau Z-Wave.

Gráfico de red
-------------------

![nywork07](../ /images/ /nywork07.png)

Cy pesaña vos donnera une représentation graphique des différents
liens entre les nœuds.

Explication la légende des coleurs :

-   **Negro** : El Controlador principal, en général représenté
    comme Jeedom.

-   **Verde** : Communication directe avec le Controlador, idéal.

-   **Blue** : Por les Controladors, comme les téléComandos, ils sont
    associés au Controlador primaire, mais n'ont pas de voisin.

-   **Amarillo** : Tote les rotes ont plus d'un saut avant d'arriver
    au Controlador.

-   **Gris** : L'interview n'es pas encore complété, les liens seront
    réellement connus une fois l'interview complété.

-   **Rojo** : présumé mort, o sans voisin, ne porticipe pas/ /plus au
    maillage du réseau.

> **Punta**
>
> Seul les équipements actifs seront affichés DENTRO le graphique réseau.

El réseau Z-Wave es constitué de trois différents types de nœuds avec
trois fonctions principales.

La principale différence entre les trois types de nœuds es leur
connaissance de la Tabla de enrutamiento du réseau y por la suite leur
capacité à envoyer des Mensajes au réseau:

Tabla de enrutamiento
----------------

Chaque nœud es en mesure de déterminer quels autres nœuds sont en
Comunicación directa. Ces nœuds sont appelés voisins. Au cors de
l'inclusión y/ /o plus tard sur demande, le nœud es en mesure
d'informer le Controlador de la liste de voisins. Grâce à ces
Informaciónrmación, le Controlador es capable de construire une table qui a
totes les Informaciónrmación sur les rotes possibles de communication DENTRO
un réseau.

![nywork08](../ /images/ /nywork08.png)

Els lignes du tableau contiennent les nœuds de sorce y les colonnes
contiennent les nœuds de desination. Se référer à la légende por
comprendre les coleurs de cellule qui indiquent les liens entre deux
nœuds.

Explication la légende des coleurs :

-   **Verde** : Communication directe avec le Controlador, idéal.

-   **Blue** : Al menos 2 rutas con un salto.

-   **Amarillo** : Menos de 2 rutas con un salto.

-   **Gris** : L'interview n'es pas encore complété, sera réellement
    mis al día une fois l'interview complété.

-   **Naranja** : Todos los caminos tienen más de un salto.. Peut engendrer
    des latences.

> **Punta**
>
> Seul les équipements actifs seront affichés DENTRO le graphique réseau.

> **Importante**
>
> Un Modulo présumé mort, ne porticipe pas/ /plus au maillage du réseau.
> Il sera marqué ici d'un point d'exclamation roge DENTRO un triangle.

> **Punta**
>
> Vos povez lancer manuellement la mise al día des voisins, por Modulo
> o por l'ensemble du réseau à l'aide des botons disponibles DENTRO la
> Tabla de enrutamiento.

Salud
=====

![health01](../ /images/ /health01.png)

Cyte fenêtre résume l'état de votre réseau Z-Wave :

![health02](../ /images/ /health02.png)

Teneis ici :

-   **Modulo** : le nom de votre Modulo, un clic dessus vos permite d'y
    accéder directement.

-   **Identificación** : Identificación de votre Modulo sur le réseau Z-Wave.

-   **Notificación** : dernier type d'échange entre le Modulo y le
    Controlador

-   **Grupo** : indique si la Configuración des gropes es ok
    (Controlador au moins DENTRO un grope). Si vos n'avez rien c'es que
    le Modulo ne supporte pas la notion de grope, c'es normal

-   **Fabricante** : indique si la récupération des Informaciónrmación
    d'identification du Modulo es ok

-   **Voisin** : indique si la liste des voisins a bien été récupérée

-   **Estado** : Indique le statut de l'interview (query stage) du
    Modulo

-   **Batería** : niveau de batterie du Modulo (un fiche secteur
    indique que le Modulo es alimenté au secteur).

-   **Hora de despertarse** : por les Modulos sur batterie, il donne la
    fréquence en secondes des instants où le Modulo se
    réveille automatiquement.

-   **Paquye total** : affiche le nombre total de paquys reçus o
    envoyés avec succès au Modulo.

-   **%Bueno** : affiche le porcentage de paquys envoyés/ /reçus
    avec succès.

-   **Ryraso de tiempo** : affiche le délai moyen d'envoi de paquy en ms.

-   **Última notificación** : Date de dernière notification reçue du
    Modulo ainsi que l'heure du prochain réveil prévue, por les Modulos
    qui dorment.

    -   Elle permite en plus d'informer si le noeud ne s'es pas encore
        réveillé une fois depuis le lancement du démon.

    -   Et indique si un noeud ne s'es pas réveillé comme prévu.

-   **De ping** : Permy d'envoyer une série de Mensajes au Modulo por
    teser son bon fonctionnement.

> **Importante**
>
> Els équipements désactivés seront affichés mais aucune information de
> diagnostic ne sera présente.

El nom du Modulo peut-être suivit por une o deux images:

![health04](../ /images/ /health04.png) Modulos supportant la
COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../ /images/ /health05.png) Modulos supportant la
COMMAND\_CLASS\_SECURITY y securisé.

![health06](../ /images/ /health06.png) Modulos supportant la
COMMAND\_CLASS\_SECURITY y non Seguro.

![health07](../ /images/ /health07.png) Modulo FLiRS, roteurs esclaves
(Modulos à piles) à écote fréquente.

> **Punta**
>
> La Comando De ping peut être utilisée si le Modulo es présumé mort
> "DEATH" afin de confirmer si c'es réellement le cas.

> **Punta**
>
> Els Modulos qui dorment répondront seulement au De ping lors de leur
> prochain réveil.

> **Punta**
>
> La notification Tiempo de espera ne signifie pas nécessairement un problème
> avec le Modulo. Lancer un De ping y DENTRO la majorité des cas le Modulo
> répondra por une Notificación **NoOperation** qui confirme un ryor
> fructueux du De ping.

> **Punta**
>
> La Ryraso de tiempo y le %Bueno sur des nœuds sur piles avant la complétion
> de leur interview n'es pas significative. En effy le nœud ne va pas
> répondre aux interrogations du Controlador du fait qu'El es en sommeil
> profond.

> **Punta**
>
> El serveur Z-Wave s'occupe automatiquement de lancer des tess sur les
> Modulos en Tiempo de espera au bot de 15 minutes

> **Punta**
>
> El serveur Z-Wave essaie automatiquement de remonter les Modulos
> présumés morts.

> **Punta**
>
> Une alerte sera envoyée à Jeedom si le Modulo es présumé mort. Vos
> povez activer une notification por en être informé le plus
> rapidement possible. Voir la Configuración des Messages DENTRO l'écran
> de Configuración de Jeedom.

![health03](../ /images/ /health03.png)

> **Punta**
>
> Si sur votre Tabla de enrutamiento y/ /o sur l'écran de santé Z-Wave vos
> avez un o des Modulos nommés avec leurs **nom générique**, la
> sincronización permityra de remédier à cyte situation.

> **Punta**
>
> Si sur votre Tabla de enrutamiento y/ /o sur l'écran de santé Z-Wave vos
> avez un o des Modulos nommés **Unknown**, cela signifie que
> l'interview du Modulo n'a pas été complétée avec succès. Teneis
> probablement un **NBueno** DENTRO la colonne constructeur. Ouvrir le détail
> du/ /des Modulos, por essayer les suggesions de solution proposées.
> (voir section Dépannage y diagnostique, plus bas)

Estado de l'interview
---------------------

Etape de l'interview d'un Modulo après le démarrage du démon.

-   **None** Inicialización del proceso de búsqueda de nodos..

-   **ProtocolInformación** Récupérer des Informaciónrmación de protocole, si ce
    noeud es en écote (listener), sa vitesse maximale y ses classes
    de périphériques.

-   **Probe** De ping le Modulo por voir s'El es réveillé.

-   **WakeUp** Démarrer le processus de réveil, s'il s'agit d'un
    noeud endormi.

-   **ManufacturerSpecific1** Récupérer le nom du fabricant y de
    produits ids si ProtocolInformación le permite.

-   **NodeInformación** Récupérer les infos sur la prise en charge des classes
    de Comandos supportées.

-   **NodePlusInformación** Récupérer les infos ZWave+ sur la prise en charge
    des classes de Comandos supportées.

-   **SecurityReport** Récupérer la liste des classes de Comando qui
    nécessitent de la Seguridad.

-   **ManufacturerSpecific2** Récupérer le nom du fabricant y les
    identifiants de produits.

-   **Versions** Recuperar información de la versión.

-   **Instancias** Récupérer des Informaciónrmación multi-instances de classe
    de Comando.

-   **Static** Récupérer des Informaciónrmación statiques (ne change pas).

-   **CacheLoad** De ping le Modulo lors du redémarrage avec config Cubierta
    de l'apporeil.

-   **Asociaciones** Recuperar información sobre asociaciones.

-   **Neighbors** Recuperar la lista de nodos vecinos..

-   **Session** Récupérer des Informaciónrmación de session (change rarement).

-   **Dynamic** Recuperar información dinámica
    (change fréquemment).

-   **Configuración** Récupérer des Informaciónrmación de poramètres de
    Configuracións (seulement fait sur demande).

-   **Complye** El processus de l'interview es terminé por ce noeud.

Notificación
------------

Détails des notifications envoyées por les Modulos

-   **Complyed** Acción terminée avec succès.

-   **Tiempo de espera** Rapport de délai rapporté lors de l'envoi d'un Mensaje.

-   **NoOperation** Rapport sur un tes du noeud (De ping), que le Mensaje
    a été envoyé avec succès.

-   **Awake** Signaler quand un noeud vient de se réveiller

-   **Sleep** Signaler quand un noeud s'es endormi.

-   **Dead** Signaler quand un nœud es présumé mort.

-   **Alive** Signaler quand un nœud es relancé.

Copias de seguridad
=======

La portie backup va vos permityre de gérer les backups de la topologie
de votre réseau. C'es votre Expediente zwcfgxxx.xml, il constitue le
dernier état connu de votre réseau, c'es une forme de Cubierta de votre
réseau. A portir de cy écran vos porrez :

-   Lancer un backup (un backup es fait à chaque arrêt relance du
    réseau y pendant les opérations critiques). Els 12 derniers backups
    sont conservés

-   Resaurer un backup (en le sélectionnant DENTRO la liste
    juste au-dessus)

-   Borrar un backup

![backup01](../ /images/ /backup01.png)

Mytre al día OpenZWave
=======================

Suite à une mise al día du Plugin Z-Wave El es possible que Jeedom vos
demande de mytre al día les Dependencias Z-Wave. Un NBueno au niveau des
Dependencias sera affiché:

![update01](../ /images/ /update01.png)

> **Punta**
>
> Une mise al día des Dependencias n'es pas à faire à chaque mise al día
> du Plugin.

Jeedom devrait lancer de lui même la mise al día des Dependencias si le
Plugin considère qu'elle sont **NBueno**. Cyte validation es effectuée au
bot de 5 minutes.

La durée de cyte opération peut varier en fonction de votre système
(jusqu'à plus de 1h sur raspberry pi)

Une fois la mise al día des Dependencias complétée, le démon se relancera
automatiquement à la validation de Jeedom. Cyte validation es
effectuée au bot de 5 minutes.

> **Punta**
>
> Dans l'éventualité où la mise al día des Dependencias ne se
> complèterait pas, veillez consulter le log **Openzwave\_update** qui
> devrait vos informer sur le problème.

Liste des Modulos compatible
============================

Vos troverez la liste des Modulos compatibles
[ici](https:/ // /jeedom.fr/ /doc/ /documentation/ /zwave-Modulos/ /fr_FR/ /doc-zwave-Modulos-equipement.compatible.html)

Depannage y diagnostic
=======================

Mon Modulo n'es pas détecté o ne remonte pas ses identifiants produit y type
-------------------------------------------------------------------------------

![trobleshooting01](../ /images/ /trobleshooting01.png)

Lancer la Regénération de la détection du nœud depuis l'pesaña Acciones
du Modulo.

Si vos avez plusieurs Modulos DENTRO ce cas de figure, lancer **Actualizar
la détection de nœuds inconnues** depuis l'écran **Red Zwave** pesaña
**Acciones**.

Mon Modulo es présumé mort por le controleur Dead
--------------------------------------------------

![trobleshooting02](../ /images/ /trobleshooting02.png)

Si le Modulo es tojors branché y joignable, suivre les solutions
proposées DENTRO l'écran du Modulo.

Si le Modulo a été décommissionné o es réellement défectueux, vos
povez l'exclure du réseau en utilisant **supprimer le nœud en erreur**
via pesaña **Acciones**.

Si le Modulo es porti en réporation y un noveau Modulo de
remplacement a été livré, vos povez lancer **Reemplazar nodo fallido**
via pesaña **Acciones**, le Controlador déclenche l'inclusión puis vos
devez procéder à l'inclusión sur le Modulo. L'id de l'ancien Modulo sera
conservé ainsi que ses Comandos.

Comment utiliser la Comando SwitchAll
--------------------------------------

![trobleshooting03](../ /images/ /trobleshooting03.png)

Elle es disponible via votre nœud Controlador. Votre Controlador devrait
avoir les Comandos Switch All On y Switch All Off.

Si votre Controlador n'apporaît pas DENTRO votre liste de Modulo, lancez la
sincronización.

![trobleshooting04](../ /images/ /trobleshooting04.png)

La Commande Classe Switch All es en général supportée sur les
interrupteurs y les variateurs. Son comportement es configurable sur
chaque Modulo qui la supporte.

On peut donc soit:

-   Désactiver la Commande Classe Switch All.

-   Activar por le On y le Off.

-   Activar le On seulement.

-   Activar le Off seulement.

El choix d'options dépend d'un constructeur à l'autre.

Il faut donc bien prendre le temps de passer en revue l'ensemble de ses
interrupteurs/ /variateurs avant de mytre en place un scénario si vos ne
pilotez pas que des lumières.

Mon Modulo n a pas de Comando Scene o Boton
----------------------------------------------

![trobleshooting05](../ /images/ /trobleshooting05.png)

Vos povez ajoter la Comando DENTRO l'écran de "mapping" des Comandos.

Il s'agit d'une Comando **Información** en CC **0x2b** Instancia **0** Comando
**data\[0\].val**

El modo scène doit être activé DENTRO les poramètres du Modulo. Voir la
documentation de votre Modulo por plus de détails.

Forcer le Refrescante de valeurs
-------------------------------------

El es possible de forcer à la demande le rafraîchissement des valeurs
d'une instance por une Comando classe spécifique.

El es possible de faire via une requête http o de créer une Comando
DENTRO l'écran de mapping d'un équipement.

![trobleshooting06](../ /images/ /trobleshooting06.png)

Il s'agit d'une Comando **Acción** choisir la **CC** sohaitée por une
**Instancia** donnée avec la Comando **data\[0\].ForceRefresh()**

L'ensemble des index de l'instance por cyte Comando Classe sera mise
al día. Els nœuds sur piles attendront leur prochain réveil avant
d'effectuer la mise al día de leur valeur.

Vos povez aussi utiliser por script en lançant une requête http au
serveur REST Z-Wave.

Remplacer ip\_jeedom, node\_id, instance\_id, cc\_id y index

http:/ // /token:\#APIKEY\#@ip\_jeedom:8083/ /ZWaveAPI/ /Run/ /devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

L'accès a l'api REST ayant changé, voir les détails
[içi](./ /resapi.asciidoc).

Transferer les Modulos sur un noveau controleur
------------------------------------------------

Por différentes raisons, vos povez être amené à devoir transférer
l'ensemble de vos Modulos sur un noveau Controlador principal.

Vos décidez de passer du **raZberry** à un **Z-Stick Gen5** o porce
que, vos devez effectuer un **Resablecer** comply du Controlador principal.

Voici différentes étapes por y arriver sans perdre vos scénarios,
widgys y historiques de valeur:

-   1\) Faire un backup Jeedom.

-   2\) Pensez à noter (copie écran) vos valeurs de poramètres por chaque
    Modulo, ils seront perdus suite à l'Exclusión.

-   3\) Dans la Configuración Z-Wave, décocher l'option "Borrar
    automatiquement les périphériques exclus" y sauvegarder. El
    réseau redémarre.

-   4a) Dans le cas d'un **Resablecer**, Faire le Resablecer du Controlador
    principal y redémarrer le Plugin.

-   4b) Por un noveau Controlador, Dyenerper Jeedom, débrancher l'ancien
    Controlador y brancher le noveau. Démarrer Jeedom.

-   5\) Por chaque équipements Z-Wave, modifier l'Identificación ZWave à **0**.

-   6\) Ouvrir 2 pages du Plugin Z-Wave DENTRO des pesañas différents.

-   7\) (Via le premier pesaña) Aller sur la page de Configuración d'un
    Modulo que vos désirez inclure au noveau Controlador.

-   8\) (Via deuxième pesaña) Faire une Exclusión puis une inclusión
    du Modulo. Un novel équipement sera créé.

-   9\) Copier l'Identificación Z-Wave du novel équipement, puis supprimer
    cy équipement.

-   10\) Ryorner sur l'pesaña de l'ancien Modulo (1er pesaña) puis coller
    le novel Identificación à la place de l'ancien Identificación.

-   11\) Els poramètres ZWave ont été perdus lors de l'Exclusión/ /inclusión,
    pensez à remytre vos poramètres spécifiques si vos n'utilisez les
    valeurs por défaut.

-   11\) Répéter les étapes 7 à 11 por chaque Modulo à transférer.

-   12\) A la fin, vos ne devriez plus avoir d'équipement en Identificación 0.

-   13\) Vérifier que tos les Modulos sont bien nommés DENTRO l'écran de
    santé Z-Wave. Lancer la Synchronisation si ce n'es pas le cas.

Remplacer un Modulo defaillant
------------------------------

Comment refaire l'inclusión d'un Modulo défaillant sans perdre vos
scénarios, widgys y historiques de valeur

Si le Modulo es présumé "Dead" :

-   Noter (copie écran) vos valeurs de poramètres, elles seront perdues
    suite à l'inclusión.

-   Aller sur l'pesaña actions du Modulo y lancez la Comando
    "Remplacer noeud en échec".

-   El Controlador es en modo inclusión, procéder à l'inclusión selon la
    Documentación del módulo.

-   Remytre vos poramètres spécifiques.

Si le Modulo n'es pas présumé "Dead" mais es tojors accessible:

-   Dans la Configuración ZWave, décocher l'option "Borrar
    automatiquement les périphériques exclus".

-   Noter (copie écran) vos valeurs de poramètres, elles seront perdues
    suite à l'inclusión.

-   Exclure le Modulo défaillant.

-   Aller sur la page de Configuración du Modulo défaillant.

-   Ouvrir la page du Plugin ZWave DENTRO un novel pesaña.

-   Faire l'inclusión du Modulo.

-   Copier l'Identificación du noveau Modulo, puis supprimer cy équipement.

-   Ryorner sur l'pesaña de l'ancien Modulo puis coller le novel Identificación à
    la place de l'ancien Identificación.

-   Remytre vos poramètres spécifiques.

Suppression de noeud fantome
----------------------------

Si vos avez perdu tote communication avec un Modulo sur pile y que
vos sohaitez l'exclure du réseau, El es possible que l'Exclusión
n'abotisse pas o que le nœud rese présent DENTRO votre réseau.

Un assistant automatique de nœud fantôme es disponible.

-   Aller sur l'pesaña actions du Modulo à supprimer.

-   Il aura probablement un statut **CacheLoad**.

-   Lancer la Comando **Borrar nœud fantôme**.

-   El réseau Z-Wave s'arrête. L'assistant automatique modifie le
    Expediente **zwcfg** por supprimer la CC WakeUp du Modulo. El
    réseau redémarre.

-   Fermer l'écran du Modulo.

-   Ouvrir l'écran de Salud Z-Wave.

-   Attendre que le cycle de démarrage soit complété (topology loaded).

-   El Modulo sera normalement marqué comme étant présumé mort (Dead).

-   La minute suivante, vos devriez voir le nœud disporaître de l'écran
    de santé.

-   Si DENTRO la Configuración Z-Wave, vos avez décoché l'option
    "Eliminar automáticamente los dispositivos excluidos", il vos faudra
    supprimer manuellement l'équipement correspondant.

Cy assistant es disponible seulement por les Modulos sur piles.

Acciones post inclusión
----------------------

On reComando d'effectuer l'inclusión à moins 1M du Controlador
principal, or ce ne sera pas la position finale de votre noveau Modulo.
Voici quelques bonnes pratiques à faire suite à l'inclusión d'un noveau
Modulo DENTRO votre réseau.

Une fois l'inclusión terminée, il faut appliquer un certain nombre de
poramètres à notre noveau Modulo afin d'en tirer le maximum. Rappel,
les Modulos, suite à l'inclusión, ont les poramètres por défaut du
constructeur. Profitez d'être à côté du Controlador y de l'interface
Jeedom por bien poramétrer votre noveau Modulo. Il sera aussi plus
simple de réveiller le Modulo por voir l'effy immédiat du changement.
Certains Modulos ont une documentation spécifique Jeedom afin de vos
aider avec les différents poramètres ainsi que des valeurs recommandées.

Tesez votre Modulo, validez les remontées d'Informaciónrmación, ryor d'état
y actions possibles DENTRO le cas d'un actuateur.

Lors de l'interview, votre noveau Modulo a recherché ses voisins.
Totefois, les Modulos de votre réseau ne connaissent pas encore votre
noveau Modulo.

Déplacez votre Modulo à son emplacement définitif. Lancez la mise al día
de ses voisins y réveillez-le encore une fois.

![trobleshooting07](../ /images/ /trobleshooting07.png)

On constate qu'il voit un certain nombre de voisins mais que les
voisins, eux, ne le voient pas.

Por remédier à cyte situation, il faut lancer l'action soigner le
réseau, afin de demander à tos les Modulos de ryrover leurs voisins.

Cyte action peut prendre 24 heures avant d'être terminée, vos Modulos
sur pile effectueront l'action seulement à leur prochain réveil.

![trobleshooting08](../ /images/ /trobleshooting08.png)

L'option de soigner le réseau 2x por semaine permite faire ce
processus sans action de votre port, elle es utile lors de la mise en
place de noveaux Modulos y o lorsqu'on les déplace.

Pas de remontee état de la pile
-------------------------------

Els Modulos Z-Wave n'envoient que très rarement l'état de leur pile au
Controlador. Certains vont le faire à l'inclusión puis seulement lorsque
celle-ci atteint 20% o une autre valeur de seuil critique.

Por vos aider à mieux suivre l'état de vos piles, l'écran Baterías
sos le menu Analyse vos donne une vue d'ensemble de l'état de vos
piles. Un mécanisme de notification de piles faibles es aussi
disponible.

La valeur remontée de l'écran Piles es la dernière connue DENTRO le
Cubierta.

Totes les nuits, le Plugin Z-Wave demande à chaque Modulo de rafraichir
la valeur Battery. Au prochain réveil, le Modulo envoie la valeur à
Jeedom por être ajoté au Cubierta. Donc il faut en général attendre au
moins 24h avant l'obtention d'une valeur DENTRO l'écran Baterías.

> **Punta**
>
> El es bien entendu possible de rafraichir manuellement la valeur
> Battery via l'pesaña Valores du Modulo puis, soit attendre le prochain
> réveil o encore de réveiller manuellement le Modulo por obtenir une
> remontée immédiate. El cycle de réveil (Wake-up Interval) du Modulo
> es défini DENTRO l'pesaña Sistema du Modulo. Por optimiser la vie de
> vos piles, El es recommandé d'espacer au maximum ce délai. Por 4h,
> il faudrait appliquer 14400, 12h 43200. Certains Modulos doivent
> écoter régulièrement des Mensajes du Controlador comme les
> Thermostats. Dans ce cas, il faut penser à 15min soit 900. Chaque
> Modulo es différent, il n'y a donc pas de règle exacte, c'es au cas
> por cas y selon l'expérience.

> **Punta**
>
> La décharge d'une pile n'es pas linéaire, certains Modulos vont
> montrer un grosse perte en porcentage DENTRO les premiers jors de mise
> en service, puis ne plus boger durant des semaines por se vider
> rapidement une fois passé les 20%.

Controleur es en cors d initialisation
----------------------------------------

Lorsque vos démarrez le démon Z-Wave, si vos essayez de lancer
immédiatement une inclusión/ /Exclusión, vos risquez d'obtenir ce
Mensaje: \* "El Controlador es en cors d'initialisation, veuillez
réessayer DENTRO quelques minutes"

> **Punta**
>
> Suite au démarrage du démon, le Controlador passe sur l'ensemble des
> Modulos afin de refaire leur interview. Ce comportement es
> tot-à-fait normal en OpenZWave.

Si totefois après plusieurs minutes (plus de 10 minutes), vos avez
tojors ce Mensaje, ce n'es plus normal.

Il faut essayer les différentes étapes:

-   S'assurer que les voyants de l'écran santé Jeedom soient au vert.

-   S'assurer que la Configuración du Plugin es en ordre.

-   S'assurer que vos avez bien sélectionné le bon port de la
    clé ZWave.

-   S'assurer que votre Configuración Réseau Jeedom es juste.
    (Attention si vos avez fait un Resore d'une installation DIY vers
    image officielle, le suffixe / /jeedom ne doit pas y figurer)

-   Regarder le log du Plugin afin de voir si une erreur n'es
    pas remontée.

-   Regarder la **Console** du Plugin ZWave, afin de voir si une erreur
    n'es pas remontée.

-   Lancer le Demon en **Depurar** regarder à noveau la **Console** y
    les logs du Plugin.

-   Redémarrer complètement Jeedom.

-   Il faut s'assurer que vos avez bien un Controlador Z-Wave, les
    Razberry sont sovent confondus avec les EnOcean (erreur lors de
    la orden).

Il faut maintenant débuter les tess hardwares:

-   El Razberry es bien branché au port GPIO.

-   L'alimentation USB es suffisante.

Si le problème persiste tojors, il faut réinitialiser le Controlador:

-   Dyenidor complément votre Jeedom via le menu d'arrêt DENTRO le
    profil utilisateur.

-   Débrancher l'alimentation.

-   Ryirer le dongle USB o le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le tot y essayer à noveau.

El controleur ne répond plus
----------------------------

Plus aucune Comando n'es transmise aux Modulos mais les ryors
d'états sont remontés vers Jeedom.

El es possible que la queue de Mensajes du Controlador soit remplie.
Voir l'écran Réseau Z-Wave si le nombre de Mensajes en attente ne fait
qu'augmenter.

Il faut DENTRO ce cas relancer le Demon Z-Wave.

Si le problème persiste, il faut réinitialiser le Controlador:

-   Dyenidor complément votre Jeedom via le menu d'arrêt DENTRO le
    profil utilisateur.

-   Débrancher l'alimentation.

-   Ryirer le dongle USB o le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le tot y essayer à noveau.

Erreur lors des dependances
---------------------------

Plusieurs errores peuvent survenir lors de la mise al día des
Dependencias. Il faut consulter le log de mise al día des Dependencias
afin de déterminer quelle es exactement l'erreur. De façon générale,
l'erreur se trove à la fin du log DENTRO les quelque dernières lignes.

Voici les possibles problèmes ainsi que leurs possibles résolutions:

-   cold not install mercurial – abort

El package mercurial ne veut pas s'installer, por corriger lancer en
ssh:

    sudo rm / /var/ /lib/ /dpkg/ /info/ /$mercurial* -f
    sudo apt-gy install mercurial

-   Els Dependencias semblent bloquées sur 75%

A 75% c'es le début de la compilation de la librairie openzwave ainsi
que du wrapper python openzwave. Cyte étape es très longue, on peut
totefois consulter la progression via la vue du log de mise al día. Il
faut donc être simplement patient.

-   Erreur lors de la compilation de la librairie openzwave

        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed sorce if appropriate.
        See <file:/ // // /usr/ /share/ /doc/ /gcc-4.9/ /README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targy 'build' failed
        make: *** [build] Error 1

Cyte erreur peut survenir suite à un manque de mémoire RAM durant la
compilation.

Depuis l'UI jeedom, lancez la compilation des Dependencias.

Une fois lancée, en ssh, arrêtez ces processus (consommateurs en
mémoire) :

    sudo systemctl Dyener cron
    sudo systemctl Dyener apache2
    sudo systemctl Dyener mysql

Por suivre l'avancement de la compilation, on fait un tail sur le
Expediente log openzwave\_update.

    tail -f / /var/ /www/ /html/ /log/ /openzwave_update

Lorsque la compilation es terminée y sans erreur, relancez les
services que vos avez arrêté

sudo systemctl comienzo cron sudo systemctl comienzo apache2 sudo systemctl
comienzo mysql

> **Punta**
>
> Si vos êtes tojors sos nginx, il faudra remplacer **apache2** por
> **nginx** DENTRO les Comandos **Dyener** / / **comienzo**. El Expediente log
> openzwave\_update sera DENTRO le dossier:
> / /usr/ /share/ /nginx/ /www/ /jeedom/ /log .

Utilisation de la carte Razberry sur un Raspberry Pi 3
------------------------------------------------------

Por utiliser un Controlador Razberry sur un Raspberry Pi 3, le
Controlador Bluyooth interne du Raspberry doit être désactivé.

Ajoter cyte ligne:

    dtoverlay=pi3-miniuart-bt

À la fin du Expediente:

    / /boot/ /config.txt

Puis redémarrer votre Raspberry.

API Http
========

El Plugin Z-Wave my à disposition des développeurs y des utilisateurs
une API complète afin de povoir opérer le réseau Z-Wave via requête
Http.

Il vos es possible d'exploiter l'ensemble des méthodes exposées por le
serveur REST du démon Z-Wave.

La syntaxe por appeler les rotes es sos cyte forme:

URL =
[http:/ // /token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/ /\#ROUTE\#](http:/ // /token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/ /#ROUTE#)

-   \#API\_KEY\# correspond à votre clé API, propre à
    votre installation. Por la trover, il faut aller DENTRO le menu «
    Principal », puis « Administration » y « Configuración », en activant
    le modo Expert, vos verrez alors une ligne Clef API.

-   \#IP\_JEEDOM\# correspond à votre url d'accès à Jeedom.

-   \#PORTDEMON\# correspond au numéro de port spécifié DENTRO la page de
    Configuración du Plugin Z-Wave, por défaut: 8083.

-   \#ROUTE\# correspond à la rote sur le serveur REST a exécuter.

Por connaitre l'ensemble des rotes, veuillez vos référer
[github](https:/ // /github.com/ /jeedom/ /Plugin-openzwave) du Plugin Z-Wave.

Example: Por lancer un ping sur le noeud id 2

URL =
http:/ // /token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ /ZWaveAPI/ /Run/ /devices\[2\].TesNode()

# Preguntas frecuentes

> **J'ai l'erreur "Not enogh space in stream buffer"**
>
> Malheureusement cyte erreur es matériel, nos ne povons rien y faire y cherchons por le moment comment forcer un redémarrage du démon DENTRO le cas de cyte erreur (mais sovent il faut en plus débrancher la clef pendant 5min por que ca reporte)
