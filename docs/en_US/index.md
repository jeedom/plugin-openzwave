Description
===========

This plugin allows the exploitation of Z-Wave modules via
the OpenZwave library.

Introduction
============

Z-Wave communique en utilisant une technologie radio de faible puissance
dans la bande de fréquence de 868,42 MHz. Il est spécifiquement conçu
pour les applications de domotique. Le protocole radio Z-Wave est
optimisé pour des échanges à faible bande passante (entre 9 et 40
kbit/s) entre des appareils sur pile ou alimentés sur secteur.

Z-Wave fonctionne dans la gamme de fréquences sous-gigahertz, selon les
régions (868 MHz en Europe, 908 MHz aux US, et d’autres fréquences
suivant les bandes ISM des régions). La portée théorique est d’environ
30 mètres en intérieur et 100 mètres en extérieur. Le réseau Z-Wave
utilise la technologie du maillage (mesh) pour augmenter la portée et la
fiabilité. Z-Wave est conçu pour être facilement intégré dans les
produits électroniques de basse consommation, y compris les appareils à
piles tels que les télécommandes, les détecteurs de fumée et capteurs de
sécurité.

Le Z-Wave+, apporte certaines améliorations dont une meilleure portée et
améliore la durée de vie des batteries entre autres. La
rétrocompatibilité est totale avec le Z-Wave.

Distances à respecter avec les autres sources de signaux sans fil
-----------------------------------------------------------------

Les récepteurs radio doivent être positionnés à une distance minimum de
50 cm des autres sources radioélectriques.

Examples of radio-electric sources :

-   Computers

-   Microwave devices

-   Electronic transformers

-   équipements audio et de matériel vidéo

-   Les dispositifs de pré-accouplement pour lampes fluorescentes

> **Tip**
>
> Si vous disposez un contrôleur USB (Z-Stick), il est recommandé de
> l’éloigner de la box à l’aide d’une simple rallonge USB de 1M par
> exemple.

La distance entre d’autres émetteurs sans fil tels que les téléphones
sans fil ou transmissions radio audio doit être d’au moins 3 mètres. Les
sources de radio suivantes doivent être prises en compte :

-   Perturbations par commutateur de moteurs électriques

-   Interférences par des appareils électriques défectueux

-   Les perturbations par les appareils HF de soudage

-   dispositifs de traitement médical

Epaisseur efficace des murs
---------------------------

Les emplacements des modules doivent être choisis de telle manière que
la ligne de connexion directe ne fonctionne que sur une très courte
distance au travers de la matière (un mur), afin d’éviter au maximum les
atténuations.

![introduction01](../images/introduction01.png)

Les parties métalliques du bâtiment ou des meubles peuvent bloquer les
ondes électromagnétiques.

Maillage et Routage
-------------------

Les nœuds Z-Wave sur secteur peuvent transmettre et répéter les messages
qui ne sont pas à portée directe du contrôleur. Ce qui permet une plus
grande flexibilité de communication, même si il n’y a pas de connexion
sans fil directe ou si une connexion est temporairement indisponible, à
cause d’un changement dans la pièce ou le bâtiment.

![introduction02](../images/introduction02.png)

Le contrôleur **Id 1** peut communiquer directement avec les nœuds 2, 3
et 4. Le nœud 6 est en dehors de sa portée radio, cependant, il se
trouve dans la zone de couverture radio du nœud 2. Par conséquent, le
contrôleur peut communiquer avec le nœud 6 via le nœud 2. De cette
façon, le chemin du contrôleur via le nœud 2 vers le nœud 6, est appelé
route. Dans le cas où la communication directe entre le nœud 1 et le
nœud 2 est bloquée, il y a encore une autre option pour communiquer avec
le nœud 6, en utilisant le nœud 3 comme un autre répéteur du signal.

Il devient évident que plus l’on possède de nœuds secteur, plus les
options de routage augmentent , et plus la stabilité du réseau augmente.
Le protocole Z-Wave est capable de router les messages par
l’intermédiaire d’un maximum de quatre nœuds de répétition. C’est un
compromis entre la taille du réseau, la stabilité et la durée maximale
d’un message.

> **Tip**
>
> Il est fortement recommandé en début d’installation d’avoir un ratio
> entre nœuds secteur et nœud sur piles de 2/3, afin d’avoir un bon
> maillage réseau. Privilégier des micromodules aux smart-plugs. Les
> micros modules seront à un emplacement définitif et ne seront pas
> débranchés, ils ont aussi en général une meilleure portée. Un bon
> départ est l’éclairage des zones communes. Il permettra de bien
> répartir les modules secteurs à des endroits stratégiques dans votre
> domicile. Par la suite vous pourrez ajouter autant de modules sur pile
> que souhaité, si vos routes de base sont bonnes.

> **Tip**
>
> Le **Graphique du réseau**ainsi que la**table de routage**
> permettent de visualiser la qualité de votre réseau.

> **Tip**
>
> Il existe des modules répéteur pour combler des zones où aucun module
> secteur n’a d’utilité.

Propriétés des appareils Z-Wave
-------------------------------

|  | Voisins | Route | Fonctions possibles |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Contrôleur | Connaît tous les voisins | A accès à la table de routage complète | Peut communiquer avec tous les appareils dans le réseau, si une voie existe |
| Esclave | Connaît tous les voisins | N’a pas d’information sur la table de routage | Ne peut répondre au nœud qu’il a reçu le message. Par conséquent, ne peut pas envoyer des messages non sollicités |
| Esclaves de routage | Connaît tous ses voisins | A la connaissance partielle de la table de routage | Peut répondre au nœud qu’il a reçu le message et peut envoyer des messages non sollicités à un certain nombre de nœuds |

In summary :

-   Chaque appareil Z -Wave peut recevoir et accuser réception de
    messages

-   Les contrôleurs peuvent envoyer des messages à tous les nœuds du
    réseau, sollicités ou non « Le maître peut parler quand il veut et à
    qui il veut »

-   Les esclaves ne peuvent pas envoyer des messages non sollicités,
    mais seulement une réponse aux demandes «L’esclave ne parle que si
    on le lui demande »

-   Les esclaves de routage peuvent répondre à des demandes et ils sont
    autorisés à envoyer des messages non sollicités à certains nœuds que
    le contrôleur a prédéfini « L’esclave est toujours un esclave, mais
    sur autorisation, il peut parler »

Plugin configuration
=======================

Après le téléchargement du plugin, il vous suffit de l’activer et de le
configurer.

![configuration01](../images/configuration01.png)

Une fois activé, le démon devrait se lancer. Le plugin est préconfiguré
avec des valeurs par défaut ; vous n’avez normalement plus rien à faire.
Cependant vous pouvez modifier la configuration.

Dépendances
-----------

Cette partie permet de valider et d’installer les dépendances requises
au bon fonctionnement du plugin Zwave (aussi bien en local qu’en
déporté, ici en local) ![configuration02](../images/configuration02.png)

-   Un Statut **OK** confirme que les dépendances sont satisfaites.

-   Si le statut est **NOK**, il faudra réinstaller les dépendances à
    l’aide du bouton ![configuration03](../images/configuration03.png)

> **Tip**
>
> La mise à jour des dépendances peut prendre plus de 20 minutes selon
> votre matériel. La progression est affichée en temps réel et un log
> **Openzwave\_update** est accessible.

> **Important**
>
> La mise à jour des dépendances est normalement à effectuer seulement
> si le Statut est **NOK**, mais il est toutefois possible, pour régler
> certains problèmes, d’être appelé à refaire l’installation des
> dépendances.

> **Tip**
>
> Si vous êtes en mode déporté, les dépendances du démon local peuvent
> être NOK, c’est tout à fait normal.

Démon
-----

Cette partie permet de valider l’état actuel du ou des démons et de
configurer la gestion automatique de ceux-ci.
![configuration04](../images/configuration04.png) Le démon local et
l’ensemble des démons déportés seront affichés avec leurs différentes
informations

-   Le **Statut** indique que le démon est actuellement en fonction.

-   La **Configuration** indique si la configuration du démon
    est valide.

-   Le bouton **(Re)Démarrer** permet de forcer le redémarrage du
    plugin, en mode normal ou de le lancer une première fois.

-   Le bouton **Arrête**, visible seulement si la gestion automatique
    est désactivée, force l’arrêt du démon.

-   La **Gestion automatique** permet à Jeedom de lancer automatiquement
    le démon au démarrage de Jeedom, ainsi que de le relancer en cas
    de problème.

-   Le **Dernier lancement** est comme son nom l’indique la date du
    dernier lancement connue du demon.

Log
---

Cette partie permet de choisir le niveau de log ainsi que d’en consulter
le contenu.

![configuration05](../images/configuration05.png)

Sélectionner le niveau puis sauvegarder, le démon sera alors relancé
avec les instructions et traces sélectionnées.

Le niveau **Debug**ou**Info** peuvent être utiles pour comprendre
pourquoi le démon plante ou ne remonte pas une valeur.

> **Important**
>
> En mode **Debug** le démon est très verbeux, il est recommandé
> d’utiliser ce mode seulement si vous devez diagnostiquer un problème
> particulier. Il n’est pas recommandé de laisser tourner le démon en
> **Debug**en permanence, si on utilise une**SD-Card**. Une fois le
> debug terminé, il ne faut pas oublier de retourner sur un niveau moins
> élevé comme le niveau **Error** qui ne remonte que d’éventuelles
> erreurs.

Configuration
-------------

Cette partie permet de configurer les paramètres généraux du plugin
![configuration06](../images/configuration06.png)

-   **Général** :

    -   **Supprimer automatiquement les périphériques exclus** :
        L’option Oui, permet de supprimer les périphériques exclus du
        réseau Z-Wave. L’option Non, permet de conserver les équipements
        dans Jeedom même s’ils ont été exclus du réseau. L’équipement
        devra être alors supprimé manuellement ou réutilisé en lui
        assignant un nouvel ID Z-Wave si on exécute une migration du
        contrôleur principal.

    -   **Appliquer le jeu de configuration recommandé à l’inclusion** :
        option pour appliquer directement à l’inclusion le jeu de
        configuration recommandé par l’équipe Jeedom (conseillée)

    -   **Désactiver l’actualisation en arrière-plan des variateurs** :
        Ne pas demander de rafraichissement des variateurs
        en arrière-plan.

    -   **Cycle (s)** : permet de définir la fréquence des remontées
        à jeedom.

    -   **Port clé Z-Wave** : le port USB sur lequel votre interface
        Z-Wave est connectée. Si vous utilisez le Razberry, vous avez,
        en fonction de votre architecture (RPI ou Jeedomboard) les 2
        possibilités à la fin de la liste.

    -   **Port du Serveur** (modification dangereuse, doit avoir la même
        valeur sur tous les Jeedoms déportés Z-Wave) : permet de
        modifier le port de communication interne du démon.

    -   **Backups** : permet de gérer les backups du fichier de
        topologie réseaux (voir plus bas)

    -   **Config modules** : permet de récupérer, manuellement, les
        fichiers de configurations OpenZWave avec les paramètres des
        modules ainsi que la définition des commandes de modules pour
        leurs utilisations.

        > **Tip**
        >
        > La récupération des configurations de module s’effectue
        > automatiquement chaque nuit.

        > **Tip**
        >
        > Le redémarrage du démon suite à la mise à jour des
        > configurations de module est inutile.

        > **Important**
        >
        > Si vous avez un module non reconnu et qu’une mise à jour de
        > configuration vient d’être appliquée, vous pouvez manuellement
        > lancer la récupération des configurations de modules.

Une fois les configurations récupérées, il faudra selon les changements
apportés:

-   Pour un nouveau module sans configuration ni commande : exclure et
    ré-inclure le module.

-   Pour un module pour lequel seuls les paramètres ont été mis à jour :
    lancer la régénération de la détection du nœud, via l’onglet Actions
    du module (le plugin doit redémarrer).

-   Pour un module dont le « mapping » de commandes a été corrigé : la
    loupe sur les commandes, voir plus bas.

    > **Tip**
    >
    > Dans le doute, exclure et ré-inclure le module est recommandé.

N’oubliez pas de ![configuration08](../images/configuration08.png) si
vous effectuez une modification.

> **Important**
>
> Si vous utilisez Ubuntu : Pour que le démon fonctionne, il faut
> absolument avoir ubuntu 15.04 (les versions inférieures ont un bug et
> le démon n’arrive pas à se lancer). Attention si vous faites une mise
> à jour à partir de 14.04 il faut une fois en 15.04 relancer
> l’installation des dépendances.

> **Important**
>
> La sélection du Port clé Z-Wave en mode de détection automatique,
> **Auto**, ne fonctionne que pour les dongles USB.

Paneau Mobile
-------------

![configuration09](../images/configuration09.png)

Permet d’afficher ou non le panel mobile lors que vous utiliser
l’application sur un téléphone.

Configuration des équipements
=============================

La configuration des équipements Z-Wave est accessible à partir du menu
plugin :

![appliance01](../images/appliance01.png)

Ci-dessous un exemple d’une page du plugin Z-Wave (présentée avec
quelques équipements) :

![appliance02](../images/appliance02.png)

> **Tip**
>
> Comme à beaucoup d’endroits sur Jeedom, placer la souris tout à gauche
> permet de faire apparaître un menu d’accès rapide (vous pouvez, à
> partir de votre profil, le laisser toujours visible).

> **Tip**
>
> Les boutons sur la ligne tout en haut **Synchroniser**,
> **Réseau-Zwave**et**Santé**, sont visibles seulement si vous êtes en
> mode **Expert**. ![appliance03](../images/appliance03.png)

Général
-------

You can find here the full configuration of your device :

![appliance04](../images/appliance04.png)

-   **Nom de l’équipement** : nom de votre module Z-Wave.

-   **Objet parent** : indique l’objet parent auquel
    appartient l’équipement.

-   **Category**: categories of equipment (it may belong to
    several categories).

-   **Activer** : permet de rendre votre équipement actif.

-   **Visible**: makes it visible on the dashboard.

-   **Node ID** : ID du module sur le réseau Z-Wave. Ceci peut être
    utile si, par exemple, vous voulez remplacer un module défaillant.
    Il suffit d’inclure le nouveau module, de récupérer son ID, et le
    mettre à la place de l’ID de l’ancien module et enfin de supprimer
    le nouveau module.

-   **Module** : ce champ n’apparaît que s’il existe différents types de
    configuration pour votre module (cas pour les modules pouvant faire
    fils pilotes par exemple). Il vous permet de choisir la
    configuration à utiliser ou de la modifier par la suite

-   **Marque** : fabricant de votre module Z-Wave.

-   **Configuration** : fenêtre de configuration des paramètres du
    module

-   **Assistant** : disponible uniquement sur certains modules, il vous
    aide à configurer le module (cas sur le zipato keyboard par exemple)

-   **Documentation** : ce bouton vous permet d’ouvrir directement la
    documentation Jeedom concernant ce module.

-   **Supprimer** : Permet de supprimer un équipement ainsi que tous ces
    commandes rattaché sans l’exclure du réseau Z-Wave.

> **Important**
>
> La suppression d’un équipement n’engendre pas une exclusion du module
> sur le contrôleur. ![appliance11](../images/appliance11.png) Un
> équipement supprimé qui est toujours rattaché à son contrôleur sera
> automatiquement recréé suite à la synchronisation.

Commandes
---------

Here below you can fond the list of commands :

![appliance05](../images/appliance05.png)

> **Tip**
>
> En fonction des types et sous-types, certaines options peuvent être
> absentes.

-   le nom affiché sur le dashboard

-   icône : dans le cas d’une action permet de choisir une icône à
    afficher sur le dashboard au lieu du texte

-   valeur de la commande : dans le cas d’une commande type action, sa
    valeur peut être liée à une commande de type info, c’est ici que
    cela se configure. Exemple pour une lampe l’intensité est liée à son
    état, cela permet au widget d’avoir l’état réel de la lampe.

-   le type et le sous-type.

-   l’instance de cette commande Z-Wave (réservée aux experts).

-   la classe de la commande Z-Wave (réservée aux experts).

-   l’index de la valeur (réservée aux experts).

-   la commande en elle-même (réservée aux experts).

-   "Valeur de retour d’état" et "Durée avant retour d’état" : permet
    d’indiquer à Jeedom qu’après un changement sur l’information sa
    valeur doit revenir à Y, X min après le changement. Exemple : dans
    le cas d’un détecteur de présence qui n’émet que lors d’une
    détection de présence, il est utile de mettre par exemple 0 en
    valeur et 4 en durée, pour que 4 min après une détection de
    mouvement (et si ensuite, il n’y en a pas eu de nouvelles) Jeedom
    remette la valeur de l’information à 0 (plus de mouvement détecté).

-   Historiser : permet d’historiser la donnée.

-   Afficher : permet d’afficher la donnée sur le dashboard.

-   Inverser : permet d’inverser l’état pour les types binaires.

-   Unité : unité de la donnée (peut être vide).

-   Min/Max : bornes de la donnée (peuvent être vides).

-   Advanced configuration (small wheels): displays
    la configuration avancée de la commande (méthode
    d’historisation, widget…​).

-   Tester : permet de tester la commande.

-   Supprimer (signe -) : permet de supprimer la commande.

> **Important**
>
> Le bouton **Tester** dans le cas d’une commande de type Info, ne va
> pas interroger le module directement mais la valeur disponible dans le
> cache de Jeedom. Le test retournera la bonne valeur seulement si le
> module en question a transmis une nouvelle valeur correspondant à la
> définition de la commande. Il est alors tout à fait normal de ne pas
> obtenir de résultat suite à la création d’une nouvelle commande Info,
> spécialement sur un module sur pile qui notifie rarement Jeedom.

La **loupe**, disponible dans l’onglet général, permet de recréer
l’ensemble des commandes pour le module en cours.
![appliance13](../images/appliance13.png) Si aucune commande n’est
présente ou si les commandes sont erronées la loupe devrait remédier à
la situation.

> **Important**
>
> La **loupe** va supprimer les commandes existantes. Si les commandes
> étaient utilisées dans des scénarios, vous devrez alors corriger vos
> scénarios aux autres endroits où les commandes étaient exploitées.

Jeux de Commandes
-----------------

Some modules have multiple pre-configured command sets

![appliance06](../images/appliance06.png)

Vous pouvez les sélectionner via les choix possibles, si le module le
permet.

> **Important**
>
> Vous devez effectuer la loupe pour appliquer le nouveau jeux de
> commandes.

Documentation et Assistant
--------------------------

Pour un certain nombre de modules, une aide spécifique pour la mise en
place ainsi que des recommandations de paramètres sont disponibles.

![appliance07](../images/appliance07.png)

Le bouton **Documentation** permet d’accéder à la documentation
spécifique du module pour Jeedom.

Des modules particuliers disposent aussi d’un assistant spécifique afin
de faciliter l’application de certains paramètres ou fonctionnements.

Le bouton **Assistant** permet d’accéder à l’écran assistant spécifique
du module.

Configuration recommandée
-------------------------

![appliance08](../images/appliance08.png)

Permet d’appliquer un jeu de configuration recommandée par l’équipe
Jeedom.

> **Tip**
>
> Lors de leur inclusion, les modules ont les paramètres par défaut du
> constructeur et certaines fonctions ne sont pas activées par défaut.

Les éléments suivants, selon le cas, seront appliqués pour simplifier
l’utilisation du module.

-   **Paramètres** permettant la mise en service rapide de l’ensemble
    des fonctionnalités du module.

-   **Groupes d’association** requis au bon fonctionnement.

-   **Intervalle de réveil**, pour les modules sur pile.

-   Activation du **rafraîchissement manuel** pour les modules ne
    remontant pas d’eux-mêmes leurs changements d’états.

Pour appliquer le jeu de configuration recommandé, cliquer sur le bouton
: **Configuration recommandée**, puis confirmer l’application des
configurations recommandées.

![appliance09](../images/appliance09.png)

L’assistant active les différents éléments de configurations.

A confirmation of the correct flow will be displayed as a ribbon.

![appliance10](../images/appliance10.png)

> **Important**
>
> Les modules sur piles doivent être réveillés pour appliquer le jeu de
> configuration.

La page de l’équipement vous informe si des éléments n’ont pas encore
été activés sur le module. Veuillez-vous référer à la documentation du
module pour le réveiller manuellement ou attendre le prochain cycle de
réveil.

![appliance11](../images/appliance11.png)

> **Tip**
>
> Il est possible d’activer automatiquement l’application du jeu de
> configuration recommandé lors de l’inclusion de nouveau module, voir
> la section Configuration du plugin pour plus de détails.

Configuration des modules
=========================

C’est ici que vous retrouverez toutes les informations sur votre module

![node01](../images/node01.png)

The screen has different tabs :

Résumé
------

Fournit un résumé complet de votre nœud avec différentes informations
sur celui-ci, comme par exemple l’état des demandes qui permet de savoir
si le nœud est en attente d’information ou la liste des nœuds voisins.

> **Tip**
>
> Sur cet onglet il est possible d’avoir des alertes en cas de détection
> possible d’un souci de configuration, Jeedom vous indiquera la marche
> à suivre pour corriger. Il ne faut pas confondre une alerte avec une
> erreur, l’alerte est dans une majorité des cas, une simple
> recommandation.

Valeurs
-------

![node02](../images/node02.png)

Vous retrouvez ici toutes les commandes et états possibles sur votre
module. Ils sont ordonnés par instance et classe de commande puis index.
Le « mapping » des commandes est entièrement basé sur ces informations.

> **Tip**
>
> Forcer la mise à jour d’une valeur. Les modules sur pile vont
> rafraichir une valeur seulement au prochain cycle de réveil. Il est
> toutefois possible de réveiller à la main un module, voir la
> documentation du module.

> **Tip**
>
> Il est possible d’avoir plus de commandes ici que sur Jeedom, c’est
> tout à fait normal. Dans Jeedom les commandes ont été présélectionnées
> pour vous.

> **Important**
>
> Certains modules n’envoient pas automatiquement leurs états, il faut
> dans ce cas activer le rafraichissement manuel à 5 minutes sur la ou
> les valeurs souhaitées. Il est recommandé de laisser en automatique le
> rafraichissement. Abuser du rafraichissement manuel peut impacter
> fortement les performances du réseau Z-Wave, utilisez seulement pour
> les valeurs recommandées dans la documentation spécifique Jeedom.
> ![node16](../images/node16.png) L’ensemble des valeurs (index) de
> l’instance d’une commande classe sera remonté, en activant le
> rafraichissement manuel sur le plus petit index de l’instance de la
> commande classe. Répéter pour chaque instance si nécessaire.

Paramètres
----------

![node03](../images/node03.png)

Vous retrouvez ici toutes les possibilités de configuration des
paramètres de votre module ainsi que la possibilité de copier la
configuration d’un autre nœud déjà en place.

Lorsqu’un paramètre est modifié, la ligne correspondante passe en jaune,
![node04](../images/node04.png) le paramètre est en attente d’être
appliqué.

If the module accepts the parameter, its line becomes transparent.

Si toutefois le module refuse la valeur, la ligne passera alors en rouge
avec la valeur appliquée retournée par le module.
![node05](../images/node05.png)

A l’inclusion, un nouveau module est détecté avec les paramètres par
défaut du constructeur. Sur certains modules, des fonctionnalités ne
seront pas actives sans modifier un ou plusieurs paramètres.
Référez-vous à la documentation du constructeur et à nos recommandations
afin de bien paramétrer vos nouveaux modules.

> **Tip**
>
> Les modules sur pile vont appliquer les changements de paramètres
> seulement au prochain cycle de réveil. Il est toutefois possible de
> réveiller à la main un module, voir la documentation du module.

> **Tip**
>
> La commande **Reprendre de…​** vous permet reprendre la configuration
> d’un autre module identique, sur le module en cours.

![node06](../images/node06.png)

> **Tip**
>
> La commande **Appliquer sur…​** vous permet d’appliquer la
> configuration actuelle du module sur un ou plusieurs modules
> identiques.

![node18](../images/node18.png)

> **Tip**
>
> La commande **Actualiser les paramètres** force le module à actualiser
> les paramètres sauvegardés dans le module.

Si aucun fichier de configuration est définie pour le module, un
assistant manuel vous permet d’appliquer des paramètres au module.
![node17](../images/node17.png) Veillez vous référer à la documentation
du fabricant pour connaitre la définition de l’index, valeur et taille.

Associations
------------

C’est ici que se retrouve la gestion des groupes d’association de votre
module.

![node07](../images/node07.png)

Les modules Z-Wave peuvent contrôler d’autres modules Z-Wave, sans
passer par le contrôleur ni Jeedom. La relation entre un module de
contrôle et un autre module est appelée association.

Afin de contrôler un autre module, le module de commande a besoin de
maintenir une liste des appareils qui recevront le contrôle des
commandes. Ces listes sont appelées groupes d’association et elles sont
toujours liées à certains événements (par exemple le bouton pressé, les
déclencheurs de capteurs, …​ ).

Dans le cas où un événement se produit, tous les périphériques
enregistrés dans le groupe d’association concerné recevront une commande
Basic.

> **Tip**
>
> Voir la documentation du module, pour comprendre les différents
> groupes d’associations possibles et leur comportement.

> **Tip**
>
> La majorité des modules ont un groupe d’association qui est réservé
> pour le contrôleur principal, il est utilisé pour remonter les
> informations au contrôleur. Il se nomme en général : **Report** ou
> **LifeLine**.

> **Tip**
>
> Il est possible que votre module ne possède aucun groupe.

> **Tip**
>
> La modification des groupes d’associations d’un module sur pile sera
> appliquée au prochain cycle de réveil. Il est toutefois possible de
> réveiller à la main un module, voir la documentation du module.

Pour connaitre avec quels autres modules le module en cours est associé,
il suffit de cliquer sur le menu **Associé à quels modules**

![node08](../images/node08.png)

L’ensemble des modules utilisant le module en cours ainsi que le nom des
groupes d’associations seront affichés.

**Associations multi-instances**

certain module supporte une commande classe multi-instance associations.
Lorsqu’un module supporte cette CC, il est possible de spécifier avec
quelle instance on souhaite créer l’association

![node09](../images/node09.png)

> **Important**
>
> Certains modules doivent être associés à l’instance 0 du contrôleur
> principale afin de bien fonctionner. Pour cette raison, le contrôleur
> est présent avec et sans l’instance 0.

Systèmes
--------

Tab grouping the system parameters of the module.

![node10](../images/node10.png)

> **Tip**
>
> Les modules sur piles se réveillent à des cycles réguliers, appelés
> intervalles de réveil (Wakeup Interval). L’intervalle de réveil est un
> compromis entre le temps maximal de vie de la batterie et les réponses
> souhaitées du dispositif. Pour maximiser la durée de vie de vos
> modules, adapter la valeur Wakeup Interval par exemple à 14400
> secondes (4h), voir encore plus élevé selon les modules et leur usage.
> ![node11](../images/node11.png)

> **Tip**
>
> Les modules **Interrupteur**et**Variateur** peuvent implémenter une
> Classe de commande spéciale appelée **SwitchAll** 0x27. Vous pouvez en
> modifier ici le comportement. Selon le module, plusieurs options sont
> à disposition. La commande **SwitchAll On/OFF** peut être lancée via
> votre module contrôleur principal.

Actions
-------

Permet d’effectuer certaines actions sur le module.

![node12](../images/node12.png)

Certaines actions seront actives selon le type de module et ses
possibilités ou encore selon l’état actuel du module comme par exemple
s’il est présumé mort par le contrôleur.

> **Important**
>
> Il ne faut pas utiliser les actions sur un module si on ne sait pas ce
> que l’on fait. Certaines actions sont irréversibles. Les actions
> peuvent aider à la résolution de problèmes avec un ou des modules
> Z-Wave.

> **Tip**
>
> La **Régénération de la détection du noeud** permet de détecter le
> module pour reprendre les derniers jeux de paramètres. Cette action
> est requise lorsqu’on vous informe qu’une mise a jour de paramètres et
> ou de comportement du module est requit pour le bon fonctionnement. La
> Régénération de la détection du noeud implique un redémarrage du
> réseau, l’assistant l’effectue automatiquement.

> **Tip**
>
> Si vous avez plusieurs modules identiques dont il est requis
> d’exécuter la **Régénération de la détection du noeud**, il est
> possible de la lancer une fois pour tous les modules identiques.

![node13](../images/node13.png)

> **Tip**
>
> Si un module sur pile n’est plus joignable et que vous souhaitez
> l’exclure, que l’exclusion ne s’effectue pas, vous pouvez lancer
> **Supprimer le noeud fantôme** Un assistant effectuera différentes
> actions afin de supprimer le module dit fantôme. Cette action implique
> de redémarrer le réseau et peut prendre plusieurs minutes avant d’être
> complétée.

![node14](../images/node14.png)

Une fois lancé, il est recommandé de fermer l’écran de configuration du
module et de surveiller la suppression du module via l’écran de santé
Z-Wave.

> **Important**
>
> Seul les modules sur pile peuvent être supprimés via cette assistant.

Statistiques
------------

This tab displays communication statistics with the node. 

![node15](../images/node15.png)

Peut être intéressant en cas de modules qui sont présumés morts par le
contrôleur "Dead".

inclusion / exclusion
=====================

A sa sortie d’usine, un module ne fait partie d’aucun réseau Z-Wave.

Mode inclusion
--------------

Le module doit se joindre à un réseau Z-Wave existant pour communiquer
avec les autres modules de ce réseau. Ce processus est appelé
**Inclusion**. Les périphériques peuvent également sortir d’un réseau.
Ce processus est appelé **Exclusion**. Les deux processus sont initiés
par le contrôleur principal du réseau Z-Wave.

![addremove01](../images/addremove01.png)

Ce bouton vous permet de passer en mode inclusion pour ajouter un module
à votre réseau Z-Wave.

Vous pouvez choisir le mode d’inclusion après avoir cliqué le bouton
**Inclusion**.

![addremove02](../images/addremove02.png)

Depuis l’apparition du Z-Wave+, il est possible de sécuriser les
échanges entre le contrôleur et les noeuds. Il est donc recommandé de
faire les inclusions en mode **Sécurisé**.

Si toutefois, un module ne peut être inclus en mode sécurisé, veuillez
l’inclure en mode **Non sécurisé**.

When inclusion mode started, Jeedom lets you know.

\[TIP\] Un module 'non sécurisé' peut commander des modules 'non
sécurisés'. Un module 'non sécurisé' ne peut pas commander un module
'sécurisé'. Un module 'sécurisé' pourra commander des modules 'non
sécurisés' sous réserve que l’émetteur le supporte.

![addremove03](../images/addremove03.png)

Une fois l’assistant lancé, il faut en faire de même sur votre module
(se référer à la documentation de celui-ci pour le passer en mode
inclusion).

> **Tip**
>
> Tant que vous n’avez pas le bandeau, vous n’êtes pas en mode
> inclusion.

Si vous re cliquez sur le bouton, vous sortez du mode inclusion.

> **Tip**
>
> Il est recommandé, avant l’inclusion d’un nouveau module qui serait
> "nouveau" sur le marché, de lancer la commande **Config modules** via
> l’écran de configuration du plugin. Cette action va récupérer
> l’ensemble des dernières versions des fichiers de configurations
> openzwave ainsi que le mapping de commandes Jeedom.

> **Important**
>
> Lors d’une inclusion, il est conseillé que le module soit à proximité
> du contrôleur principal, soit à moins d’un mètre de votre jeedom.

> **Tip**
>
> Certains modules requièrent obligatoirement une inclusion en mode
> **sécurisé**, par exemple pour les serrures de porte.

> **Tip**
>
> A noter que l’interface mobile vous donne aussi accès à l’inclusion,
> le panel mobile doit avoir été activé.

> **Tip**
>
> Si le module appartient déjà à un réseau, suivez le processus
> d’exclusion avant de l’inclure dans votre réseau. Sinon l’inclusion de
> ce module va échouer. Il est d’ailleurs recommandé d’exécuter une
> exclusion avant l’inclusion, même si le produit est neuf, sorti du
> carton.

> **Tip**
>
> Une fois le module à son emplacement définitif, il faut lancer
> l’action soigner le réseau, afin de demander à tous les modules de
> rafraichir l’ensemble des voisins.

Mode exclusion
--------------

![addremove04](../images/addremove04.png)

Ce bouton vous permet de passer en mode exclusion, cela pour retirer un
module de votre réseau Z-Wave, il faut en faire de même avec votre
module (se référer à la documentation de celui-ci pour le passer en mode
exclusion).

![addremove05](../images/addremove05.png)

> **Tip**
>
> Tant que vous n’avez pas le bandeau, vous n’êtes pas en mode
> exclusion.

Si vous re cliquez sur le bouton, vous sortez du mode exclusion.

> **Tip**
>
> A noter que l’interface mobile vous donne aussi accès à l’exclusion.

> **Tip**
>
> Un module n’a pas besoin d’être exclu par le même contrôleur sur
> lequel il a été préalablement inclus. D’où le fait qu’on recommande
> d’exécuter une exclusion avant chaque inclusion.

Synchroniser
------------

![addremove06](../images/addremove06.png)

Bouton permettant de synchroniser les modules du réseau Z-Wave avec les
équipements Jeedom. Les modules sont associés au contrôleur principal,
les équipements dans Jeedom sont créés automatiquement lors de leur
inclusion. Ils sont aussi supprimés automatiquement lors de l’exclusion,
si l’option **Supprimer automatiquement les périphériques exclus** est
activée.

Si vous avez inclus des modules sans Jeedom (requiert un dongle avec
pile comme le Aeon-labs Z-Stick GEN5), une synchronisation sera
nécessaire suite au branchement de la clé, une fois le démon démarré et
fonctionnel.

> **Tip**
>
> Si vous n’avez pas l’image ou que Jeedom n’a pas reconnu votre module,
> ce bouton peut permettre de corriger (sous réserve que l’interview du
> module soit complète).

> **Tip**
>
> Si sur votre table de routage et/ou sur l’écran de santé Z-Wave, vous
> avez un ou des modules nommés avec leur **nom générique**, la
> synchronisation permettra de remédier à cette situation.

Le bouton Synchroniser n’est visible qu’en mode expert :
![addremove07](../images/addremove07.png)

Réseaux Z-Wave
==============

![network01](../images/network01.png)

You will find here general information on your Z-Wave network.

![network02](../images/network02.png)

Résumé
------

Le premier onglet vous donne le résumé de base de votre réseau Z-Wave,
vous retrouvez notamment l’état du réseau Z-Wave ainsi que le nombre
d’éléments dans la file d’attente.

**Informations**

-   Donne des informations générales sur le réseau, la date de
    démarrage, le temps requis pour l’obtention du réseau dans un état
    dit fonctionnel.

-   Le nombre de nœuds total du réseau ainsi que le nombre qui dorment
    dans le moment.

-   L’intervalle des demandes est associé au rafraichissement manuel. Il
    est prédéfini dans le moteur Z-Wave à 5 minutes.

-   Les voisins du contrôleur.

**Etat**

![network03](../images/network03.png)

Un ensemble d’informations sur l’état actuel du réseau, à savoir :

-   Etat actuel, peut-être **Driver Initialised**, **Topology loaded**
    ou **Ready**.

-   Queue sortante, indique le nombre de messages en queue dans le
    contrôleur en attente d’être envoyé. Cette valeur est généralement
    élevée durant le démarrage du réseau lorsque l’état est encore en
    **Driver Initialised**.

Une fois que le réseau a au minimum atteint **Topology loaded**, des
mécanismes internes au serveur Z-Wave vont forcer des mises à jour de
valeurs, il est alors tout-à-fait normal de voir monter le nombre de
messages. Celui-ci va rapidement retourner à 0.

> **Tip**
>
> Le réseau est dit fonctionnel au moment où il atteint le statut
> **Topology Loaded**, c’est-à-dire que l’ensemble des nœuds secteurs
> ont complété leurs interviews. Selon le nombre de modules, la
> répartition pile/secteur, le choix du dongle USB et le PC sur lequel
> tourne le plugin Z-Wave, le réseau va atteindre cette état entre une
> et cinq minutes.

Un réseau **Ready**, signifie que tous les nœuds secteur et sur pile ont
complété leur interview.

> **Tip**
>
> Selon les modules dont vous disposez, il est possible que le réseau
> n’atteigne jamais de lui-même le statut **Ready**. Les télécommandes,
> par exemple, ne se réveillent pas d’elles-mêmes et ne compléteront
> jamais leur interview. Dans ce genre de cas, le réseau est tout-à-fait
> opérationnel et même si les télécommandes n’ont pas complété leur
> interview, elles assurent leurs fonctionnalités au sein du réseau.

**Capacités**

Permet de savoir si le contrôleur est un contrôleur principal ou
secondaire.

**Système**

Displays miscellaneous system information.

-   Information sur le port USB utilisé.

-   Version de la librairie OpenZwave

-   Version de la librairie Python-OpenZwave

Actions
-------

![network05](../images/network05.png)

Vous retrouvez ici toutes les actions possibles sur l’ensemble de votre
réseau Z-Wave. Chaque action est accompagnée d’une description sommaire.

> **Important**
>
> Certaines actions sont vraiment risquées voire irréversibles, l’équipe
> Jeedom ne pourra être tenue responsable en cas de mauvaise
> manipulation.

> **Important**
>
> Certains modules requièrent une inclusion en mode sécurisé, par
> exemple pour les serrures de porte. L’inclusion sécurisée doit être
> lancée via l’action de cet écran.

> **Tip**
>
> Si une action ne peut être lancée, elle sera désactivée jusqu’au
> moment où elle pourra être à nouveau exécutée.

Statistiques
------------

![network06](../images/network06.png)

Vous retrouvez ici les statistiques générales sur l’ensemble de votre
réseau Z-Wave.

Graphique du réseau
-------------------

![network07](../images/network07.png)

Cet onglet vous donnera une représentation graphique des différents
liens entre les nœuds.

Color codes :

-   **Noir** : Le contrôleur principal, en général représenté
    comme Jeedom.

-   **Vert** : Communication directe avec le contrôleur, idéal.

-   **Blue** : Pour les contrôleurs, comme les télécommandes, ils sont
    associés au contrôleur primaire, mais n’ont pas de voisin.

-   **Jaune** : Toute les routes ont plus d’un saut avant d’arriver
    au contrôleur.

-   **Gris** : L’interview n’est pas encore complété, les liens seront
    réellement connus une fois l’interview complété.

-   **Rouge** : présumé mort, ou sans voisin, ne participe pas/plus au
    maillage du réseau.

> **Tip**
>
> Seul les équipements actifs seront affichés dans le graphique réseau.

Le réseau Z-Wave est constitué de trois différents types de nœuds avec
trois fonctions principales.

La principale différence entre les trois types de nœuds est leur
connaissance de la table de routage du réseau et par la suite leur
capacité à envoyer des messages au réseau:

Table de routage
----------------

Chaque nœud est en mesure de déterminer quels autres nœuds sont en
communication directe. Ces nœuds sont appelés voisins. Au cours de
l’inclusion et/ou plus tard sur demande, le nœud est en mesure
d’informer le contrôleur de la liste de voisins. Grâce à ces
informations, le contrôleur est capable de construire une table qui a
toutes les informations sur les routes possibles de communication dans
un réseau.

![network08](../images/network08.png)

Les lignes du tableau contiennent les nœuds de source et les colonnes
contiennent les nœuds de destination. Se référer à la légende pour
comprendre les couleurs de cellule qui indiquent les liens entre deux
nœuds.

Color codes :

-   **Vert** : Communication directe avec le contrôleur, idéal.

-   **Blue** : Au moins 2 routes avec un saut.

-   **Jaune** : Moins de 2 routes avec un saut.

-   **Gris** : L’interview n’est pas encore complété, sera réellement
    mis à jour une fois l’interview complété.

-   **Orange** : Toutes les routes ont plus d’un saut. Peut engendrer
    des latences.

> **Tip**
>
> Seul les équipements actifs seront affichés dans le graphique réseau.

> **Important**
>
> Un module présumé mort, ne participe pas/plus au maillage du réseau.
> Il sera marqué ici d’un point d’exclamation rouge dans un triangle.

> **Tip**
>
> Vous pouvez lancer manuellement la mise à jour des voisins, par module
> ou pour l’ensemble du réseau à l’aide des boutons disponibles dans la
> table de routage.

Santé
=====

![health01](../images/health01.png)

Cette fenêtre résume l’état de votre réseau Z-Wave :

![health02](../images/health02.png)

You have here :

-   **Module** : le nom de votre module, un clic dessus vous permet d’y
    accéder directement.

-   **ID** : ID de votre module sur le réseau Z-Wave.

-   **Notification** : dernier type d’échange entre le module et le
    contrôleur

-   **Groupe** : indique si la configuration des groupes est ok
    (contrôleur au moins dans un groupe). Si vous n’avez rien c’est que
    le module ne supporte pas la notion de groupe, c’est normal

-   **Constructeur** : indique si la récupération des informations
    d’identification du module est ok

-   **Voisin** : indique si la liste des voisins a bien été récupérée

-   **Statut** : Indique le statut de l’interview (query stage) du
    module

-   **Batterie** : niveau de batterie du module (un fiche secteur
    indique que le module est alimenté au secteur).

-   **Wakeup time** : pour les modules sur batterie, il donne la
    fréquence en secondes des instants où le module se
    réveille automatiquement.

-   **Paquet total** : affiche le nombre total de paquets reçus ou
    envoyés avec succès au module.

-   **%OK** : affiche le pourcentage de paquets envoyés/reçus
    avec succès.

-   **Temporisation** : affiche le délai moyen d’envoi de paquet en ms.

-   **Dernière notification** : Date de dernière notification reçue du
    module ainsi que l’heure du prochain réveil prévue, pour les modules
    qui dorment.

    -   Elle permet en plus d’informer si le noeud ne s’est pas encore
        réveillé une fois depuis le lancement du démon.

    -   Et indique si un noeud ne s’est pas réveillé comme prévu.

-   **Ping** : Permet d’envoyer une série de messages au module pour
    tester son bon fonctionnement.

> **Important**
>
> Les équipements désactivés seront affichés mais aucune information de
> diagnostic ne sera présente.

The name of the module can be followed by one or two images :

![health04](../images/health04.png) Modules supportant la
COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../images/health05.png) Modules supportant la
COMMAND\_CLASS\_SECURITY et securisé.

![health06](../images/health06.png) Modules supportant la
COMMAND\_CLASS\_SECURITY et non sécurisé.

![health07](../images/health07.png) Module FLiRS, routeurs esclaves
(modules à piles) à écoute fréquente.

> **Tip**
>
> La commande Ping peut être utilisée si le module est présumé mort
> "DEATH" afin de confirmer si c’est réellement le cas.

> **Tip**
>
> Les modules qui dorment répondront seulement au Ping lors de leur
> prochain réveil.

> **Tip**
>
> La notification Timeout ne signifie pas nécessairement un problème
> avec le module. Lancer un Ping et dans la majorité des cas le module
> répondra par une Notification **NoOperation** qui confirme un retour
> fructueux du Ping.

> **Tip**
>
> La Temporisation et le %OK sur des nœuds sur piles avant la complétion
> de leur interview n’est pas significative. En effet le nœud ne va pas
> répondre aux interrogations du contrôleur du fait qu’il est en sommeil
> profond.

> **Tip**
>
> Le serveur Z-Wave s’occupe automatiquement de lancer des tests sur les
> modules en Timeout au bout de 15 minutes

> **Tip**
>
> Le serveur Z-Wave essaie automatiquement de remonter les modules
> présumés morts.

> **Tip**
>
> Une alerte sera envoyée à Jeedom si le module est présumé mort. Vous
> pouvez activer une notification pour en être informé le plus
> rapidement possible. Voir la configuration des Messages dans l’écran
> de Configuration de Jeedom.

![health03](../images/health03.png)

> **Tip**
>
> Si sur votre table de routage et/ou sur l’écran de santé Z-Wave vous
> avez un ou des modules nommés avec leurs **nom générique**, la
> synchronisation permettra de remédier à cette situation.

> **Tip**
>
> Si sur votre table de routage et/ou sur l’écran de santé Z-Wave vous
> avez un ou des modules nommés **Unknown**, cela signifie que
> l’interview du module n’a pas été complétée avec succès. Vous avez
> probablement un **NOK** dans la colonne constructeur. Ouvrir le détail
> du/des modules, pour essayer les suggestions de solution proposées.
> (voir section Dépannage et diagnostique, plus bas)

Statut de l’interview
---------------------

Etape de l’interview d’un module après le démarrage du démon.

-   **None** Initialisation du processus de recherche de noeud.

-   **ProtocolInfo** Récupérer des informations de protocole, si ce
    noeud est en écoute (listener), sa vitesse maximale et ses classes
    de périphériques.

-   **Probe** Ping le module pour voir s’il est réveillé.

-   **WakeUp** Démarrer le processus de réveil, s’il s’agit d’un
    noeud endormi.

-   **ManufacturerSpecific1** Récupérer le nom du fabricant et de
    produits ids si ProtocolInfo le permet.

-   **NodeInfo** Récupérer les infos sur la prise en charge des classes
    de commandes supportées.

-   **NodePlusInfo** Récupérer les infos ZWave+ sur la prise en charge
    des classes de commandes supportées.

-   **SecurityReport** Récupérer la liste des classes de commande qui
    nécessitent de la sécurité.

-   **ManufacturerSpecific2** Récupérer le nom du fabricant et les
    identifiants de produits.

-   **Versions** Récupérer des informations de version.

-   **Instances** Récupérer des informations multi-instances de classe
    de commande.

-   **Static** Récupérer des informations statiques (ne change pas).

-   **CacheLoad** Ping le module lors du redémarrage avec config cache
    de l’appareil.

-   **Associations** Récupérer des informations sur les associations.

-   **Neighbors** Récupérer la liste des noeuds voisins.

-   **Session** Récupérer des informations de session (change rarement).

-   **Dynamic** Récupérer des informations dynamiques
    (change fréquemment).

-   **Configuration** Récupérer des informations de paramètres de
    configurations (seulement fait sur demande).

-   **Complete** Le processus de l’interview est terminé pour ce noeud.

Notification
------------

Details of the notifications sent by the modules.

-   **Completed** Action terminée avec succès.

-   **Timeout** Rapport de délai rapporté lors de l’envoi d’un message.

-   **NoOperation** Rapport sur un test du noeud (Ping), que le message
    a été envoyé avec succès.

-   **Awake** Signaler quand un noeud vient de se réveiller

-   **Sleep** Signaler quand un noeud s’est endormi.

-   **Dead** Signaler quand un nœud est présumé mort.

-   **Alive** Signaler quand un nœud est relancé.

Backups
=======

La partie backup va vous permettre de gérer les backups de la topologie
de votre réseau. C’est votre fichier zwcfgxxx.xml, il constitue le
dernier état connu de votre réseau, c’est une forme de cache de votre
réseau. A partir de cet écran vous pourrez :

-   Lancer un backup (un backup est fait à chaque arrêt relance du
    réseau et pendant les opérations critiques). Les 12 derniers backups
    sont conservés

-   Restaurer un backup (en le sélectionnant dans la liste
    juste au-dessus)

-   Supprimer un backup

![backup01](../images/backup01.png)

Mettre à jour OpenZWave
=======================

Suite à une mise à jour du plugin Z-Wave il est possible que Jeedom vous
demande de mettre à jour les dépendances Z-Wave. Un NOK au niveau des
dépendances sera affiché:

![update01](../images/update01.png)

> **Tip**
>
> Une mise à jour des dépendances n’est pas à faire à chaque mise à jour
> du plugin.

Jeedom devrait lancer de lui même la mise à jour des dépendances si le
plugin considère qu’elle sont **NOK**. Cette validation est effectuée au
bout de 5 minutes.

La durée de cette opération peut varier en fonction de votre système
(jusqu’à plus de 1h sur raspberry pi)

Une fois la mise à jour des dépendances complétée, le démon se relancera
automatiquement à la validation de Jeedom. Cette validation est
effectuée au bout de 5 minutes.

> **Tip**
>
> Dans l’éventualité où la mise à jour des dépendances ne se
> complèterait pas, veillez consulter le log **Openzwave\_update** qui
> devrait vous informer sur le problème.

Liste des modules compatible
============================

Vous trouverez la liste des modules compatibles
[ici](https://jeedom.fr/doc/documentation/zwave-modules/fr_FR/doc-zwave-modules-equipement.compatible.html)

Depannage et diagnostic
=======================

Mon module n’est pas détecté ou ne remonte pas ses identifiants produit et type
-------------------------------------------------------------------------------

![troubleshooting01](../images/troubleshooting01.png)

Lancer la Regénération de la détection du nœud depuis l’onglet Actions
du module.

Si vous avez plusieurs modules dans ce cas de figure, lancer **Regénérer
la détection de nœuds inconnues**depuis l’écran**Réseau ZWave** onglet
**Actions**.

Mon module est présumé mort par le controleur Dead
--------------------------------------------------

![troubleshooting02](../images/troubleshooting02.png)

Si le module est toujours branché et joignable, suivre les solutions
proposées dans l’écran du module.

Si le module a été décommissionné ou est réellement défectueux, vous
pouvez l’exclure du réseau en utilisant **supprimer le nœud en erreur**
via onglet **Actions**.

Si le module est parti en réparation et un nouveau module de
remplacement a été livré, vous pouvez lancer **Remplacer nœud en échec**
via onglet **Actions**, le contrôleur déclenche l’inclusion puis vous
devez procéder à l’inclusion sur le module. L’id de l’ancien module sera
conservé ainsi que ses commandes.

Comment utiliser la commande SwitchAll
--------------------------------------

![troubleshooting03](../images/troubleshooting03.png)

Elle est disponible via votre nœud contrôleur. Votre contrôleur devrait
avoir les commandes Switch All On et Switch All Off.

Si votre contrôleur n’apparaît pas dans votre liste de module, lancez la
synchronisation.

![troubleshooting04](../images/troubleshooting04.png)

La Commande Classe Switch All est en général supportée sur les
interrupteurs et les variateurs. Son comportement est configurable sur
chaque module qui la supporte.

One can either :

-   Désactiver la Commande Classe Switch All.

-   Activer pour le On et le Off.

-   Activer le On seulement.

-   Activer le Off seulement.

Le choix d’options dépend d’un constructeur à l’autre.

Il faut donc bien prendre le temps de passer en revue l’ensemble de ses
interrupteurs/variateurs avant de mettre en place un scénario si vous ne
pilotez pas que des lumières.

Mon module n a pas de commande Scene ou Bouton
----------------------------------------------

![troubleshooting05](../images/troubleshooting05.png)

Vous pouvez ajouter la commande dans l’écran de "mapping" des commandes.

Il s’agit d’une commande **Info**en CC**0x2b**Instance**0** commande
**data\[0\].val**

Le mode scène doit être activé dans les paramètres du module. Voir la
documentation de votre module pour plus de détails.

Forcer le rafraichissement de valeurs
-------------------------------------

Il est possible de forcer à la demande le rafraîchissement des valeurs
d’une instance pour une commande classe spécifique.

Il est possible de faire via une requête http ou de créer une commande
dans l’écran de mapping d’un équipement.

![troubleshooting06](../images/troubleshooting06.png)

Il s’agit d’une commande **Action**choisir la**CC** souhaitée pour une
**Instance**donnée avec la commande**data\[0\].ForceRefresh()**

L’ensemble des index de l’instance pour cette commande Classe sera mise
à jour. Les nœuds sur piles attendront leur prochain réveil avant
d’effectuer la mise à jour de leur valeur.

Vous pouvez aussi utiliser par script en lançant une requête http au
serveur REST Z-Wave.

Remplacer ip\_jeedom, node\_id, instance\_id, cc\_id et index

http://token:\#APIKEY\#@ip\_jeedom:8083/ZWaveAPI/Run/devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

L’accès a l’api REST ayant changé, voir les détails
[içi](./restapi.asciidoc).

Transferer les modules sur un nouveau controleur
------------------------------------------------

Pour différentes raisons, vous pouvez être amené à devoir transférer
l’ensemble de vos modules sur un nouveau contrôleur principal.

Vous décidez de passer du **raZberry**à un**Z-Stick Gen5** ou parce
que, vous devez effectuer un **Reset** complet du contrôleur principal.

Voici différentes étapes pour y arriver sans perdre vos scénarios,
widgets et historiques de valeur:

-   1\) Faire un backup Jeedom.

-   2\) Pensez à noter (copie écran) vos valeurs de paramètres pour chaque
    module, ils seront perdus suite à l’exclusion.

-   3\) Dans la configuration Z-Wave, décocher l’option "Supprimer
    automatiquement les périphériques exclus" et sauvegarder. Le
    réseau redémarre.

-   4a) Dans le cas d’un **Reset**, Faire le Reset du contrôleur
    principal et redémarrer le plugin.

-   4b) Pour un nouveau contrôleur, stopper Jeedom, débrancher l’ancien
    contrôleur et brancher le nouveau. Démarrer Jeedom.

-   5\) Pour chaque équipements Z-Wave, modifier l’ID ZWave à **0**.

-   6\) Ouvrir 2 pages du plugin Z-Wave dans des onglets différents.

-   7\) (Via le premier onglet) Aller sur la page de configuration d’un
    module que vous désirez inclure au nouveau contrôleur.

-   8\) (Via deuxième onglet) Faire une exclusion puis une inclusion
    du module. Un nouvel équipement sera créé.

-   9\) Copier l’ID Z-Wave du nouvel équipement, puis supprimer
    cet équipement.

-   10\) Retourner sur l’onglet de l’ancien module (1er onglet) puis coller
    le nouvel ID à la place de l’ancien ID.

-   11\) Les paramètres ZWave ont été perdus lors de l’exclusion/inclusion,
    pensez à remettre vos paramètres spécifiques si vous n’utilisez les
    valeurs par défaut.

-   11\) Répéter les étapes 7 à 11 pour chaque module à transférer.

-   12\) A la fin, vous ne devriez plus avoir d’équipement en ID 0.

-   13\) Vérifier que tous les modules sont bien nommés dans l’écran de
    santé Z-Wave. Lancer la Synchronisation si ce n’est pas le cas.

Remplacer un module defaillant
------------------------------

Comment refaire l’inclusion d’un module défaillant sans perdre vos
scénarios, widgets et historiques de valeur

If the module is presumed "Dead" :

-   Noter (copie écran) vos valeurs de paramètres, elles seront perdues
    suite à l’inclusion.

-   Aller sur l’onglet actions du module et lancez la commande
    "Remplacer noeud en échec".

-   Le contrôleur est en mode inclusion, procéder à l’inclusion selon la
    documentation du module.

-   Remettre vos paramètres spécifiques.

Si le module n’est pas présumé "Dead" mais est toujours accessible:

-   Dans la configuration ZWave, décocher l’option "Supprimer
    automatiquement les périphériques exclus".

-   Noter (copie écran) vos valeurs de paramètres, elles seront perdues
    suite à l’inclusion.

-   Exclure le module défaillant.

-   Aller sur la page de configuration du module défaillant.

-   Ouvrir la page du plugin ZWave dans un nouvel onglet.

-   Faire l’inclusion du module.

-   Copier l’ID du nouveau module, puis supprimer cet équipement.

-   Retourner sur l’onglet de l’ancien module puis coller le nouvel ID à
    la place de l’ancien ID.

-   Remettre vos paramètres spécifiques.

Suppression de noeud fantome
----------------------------

Si vous avez perdu toute communication avec un module sur pile et que
vous souhaitez l’exclure du réseau, il est possible que l’exclusion
n’aboutisse pas ou que le nœud reste présent dans votre réseau.

A ghost module automatic wizard is available.

-   Aller sur l’onglet actions du module à supprimer.

-   Il aura probablement un statut **CacheLoad**.

-   Lancer la commande **Supprimer nœud fantôme**.

-   Le réseau Z-Wave s’arrête. L’assistant automatique modifie le
    fichier **zwcfg** pour supprimer la CC WakeUp du module. Le
    réseau redémarre.

-   Fermer l’écran du module.

-   Ouvrir l’écran de Santé Z-Wave.

-   Attendre que le cycle de démarrage soit complété (topology loaded).

-   Le module sera normalement marqué comme étant présumé mort (Dead).

-   La minute suivante, vous devriez voir le nœud disparaître de l’écran
    de santé.

-   Si dans la configuration Z-Wave, vous avez décoché l’option
    "Supprimer automatiquement les périphériques exclus", il vous faudra
    supprimer manuellement l’équipement correspondant.

Cet assistant est disponible seulement pour les modules sur piles.

Actions post inclusion
----------------------

On recommande d’effectuer l’inclusion à moins 1M du contrôleur
principal, or ce ne sera pas la position finale de votre nouveau module.
Voici quelques bonnes pratiques à faire suite à l’inclusion d’un nouveau
module dans votre réseau.

Une fois l’inclusion terminée, il faut appliquer un certain nombre de
paramètres à notre nouveau module afin d’en tirer le maximum. Rappel,
les modules, suite à l’inclusion, ont les paramètres par défaut du
constructeur. Profitez d’être à côté du contrôleur et de l’interface
Jeedom pour bien paramétrer votre nouveau module. Il sera aussi plus
simple de réveiller le module pour voir l’effet immédiat du changement.
Certains modules ont une documentation spécifique Jeedom afin de vous
aider avec les différents paramètres ainsi que des valeurs recommandées.

Testez votre module, validez les remontées d’informations, retour d’état
et actions possibles dans le cas d’un actuateur.

Lors de l’interview, votre nouveau module a recherché ses voisins.
Toutefois, les modules de votre réseau ne connaissent pas encore votre
nouveau module.

Déplacez votre module à son emplacement définitif. Lancez la mise à jour
de ses voisins et réveillez-le encore une fois.

![troubleshooting07](../images/troubleshooting07.png)

On constate qu’il voit un certain nombre de voisins mais que les
voisins, eux, ne le voient pas.

Pour remédier à cette situation, il faut lancer l’action soigner le
réseau, afin de demander à tous les modules de retrouver leurs voisins.

Cette action peut prendre 24 heures avant d’être terminée, vos modules
sur pile effectueront l’action seulement à leur prochain réveil.

![troubleshooting08](../images/troubleshooting08.png)

L’option de soigner le réseau 2x par semaine permet de faire ce
processus sans action de votre part, elle est utile lors de la mise en
place de nouveaux modules et ou lorsqu’on les déplace.

Pas de remontee état de la pile
-------------------------------

Les modules Z-Wave n’envoient que très rarement l’état de leur pile au
contrôleur. Certains vont le faire à l’inclusion puis seulement lorsque
celle-ci atteint 20% ou une autre valeur de seuil critique.

Pour vous aider à mieux suivre l’état de vos piles, l’écran Batteries
sous le menu Analyse vous donne une vue d’ensemble de l’état de vos
piles. Un mécanisme de notification de piles faibles est aussi
disponible.

La valeur remontée de l’écran Piles est la dernière connue dans le
cache.

Toutes les nuits, le plugin Z-Wave demande à chaque module de rafraichir
la valeur Battery. Au prochain réveil, le module envoie la valeur à
Jeedom pour être ajouté au cache. Donc il faut en général attendre au
moins 24h avant l’obtention d’une valeur dans l’écran Batteries.

> **Tip**
>
> Il est bien entendu possible de rafraichir manuellement la valeur
> Battery via l’onglet Valeurs du module puis, soit attendre le prochain
> réveil ou encore de réveiller manuellement le module pour obtenir une
> remontée immédiate. Le cycle de réveil (Wake-up Interval) du module
> est défini dans l’onglet Système du module. Pour optimiser la vie de
> vos piles, il est recommandé d’espacer au maximum ce délai. Pour 4h,
> il faudrait appliquer 14400, 12h 43200. Certains modules doivent
> écouter régulièrement des messages du contrôleur comme les
> Thermostats. Dans ce cas, il faut penser à 15min soit 900. Chaque
> module est différent, il n’y a donc pas de règle exacte, c’est au cas
> par cas et selon l’expérience.

> **Tip**
>
> La décharge d’une pile n’est pas linéaire, certains modules vont
> montrer un grosse perte en pourcentage dans les premiers jours de mise
> en service, puis ne plus bouger durant des semaines pour se vider
> rapidement une fois passé les 20%.

Controleur est en cours d initialisation
----------------------------------------

Lorsque vous démarrez le démon Z-Wave, si vous essayez de lancer
immédiatement une inclusion/exclusion, vous risquez d’obtenir ce
message: \* "Le contrôleur est en cours d’initialisation, veuillez
réessayer dans quelques minutes"

> **Tip**
>
> Suite au démarrage du démon, le contrôleur passe sur l’ensemble des
> modules afin de refaire leur interview. Ce comportement est
> tout-à-fait normal en OpenZWave.

Si toutefois après plusieurs minutes (plus de 10 minutes), vous avez
toujours ce message, ce n’est plus normal.

You have to then try the following steps :

-   S’assurer que les voyants de l’écran santé Jeedom soient au vert.

-   S’assurer que la configuration du plugin est en ordre.

-   S’assurer que vous avez bien sélectionné le bon port de la
    clé ZWave.

-   S’assurer que votre configuration Réseau Jeedom est juste.
    (Attention si vous avez fait un Restore d’une installation DIY vers
    image officielle, le suffixe /jeedom ne doit pas y figurer)

-   Regarder le log du plugin afin de voir si une erreur n’est
    pas remontée.

-   Regarder la **Console** du plugin ZWave, afin de voir si une erreur
    n’est pas remontée.

-   Lancer le Demon en **Debug**regarder à nouveau la**Console** et
    les logs du plugin.

-   Redémarrer complètement Jeedom.

-   Il faut s’assurer que vous avez bien un contrôleur Z-Wave, les
    Razberry sont souvent confondus avec les EnOcean (erreur lors de
    la commande).

* Then proceed to hardware testing :

-   Le Razberry est bien branché au port GPIO.

-   L’alimentation USB est suffisante.

If you still have a problem, you have to reset the controller.

-   Arrêter complément votre Jeedom via le menu d’arrêt dans le
    profil utilisateur.

-   Débrancher l’alimentation.

-   Retirer le dongle USB ou le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le tout et essayer à nouveau.

Le controleur ne répond plus
----------------------------

Plus aucune commande n’est transmise aux modules mais les retours
d’états sont remontés vers Jeedom.

Il est possible que la queue de messages du contrôleur soit remplie.
Voir l’écran Réseau Z-Wave si le nombre de messages en attente ne fait
qu’augmenter.

If so, you have to restart the Z-Wave daemon.

If this keeps happening, you have to reset the controller.

-   Arrêter complément votre Jeedom via le menu d’arrêt dans le
    profil utilisateur.

-   Débrancher l’alimentation.

-   Retirer le dongle USB ou le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le tout et essayer à nouveau.

Erreur lors des dependances
---------------------------

Plusieurs erreurs peuvent survenir lors de la mise à jour des
dépendances. Il faut consulter le log de mise à jour des dépendances
afin de déterminer quelle est exactement l’erreur. De façon générale,
l’erreur se trouve à la fin du log dans les quelque dernières lignes.

Here is a list of some errors and their possible remediations :

-   could not install mercurial – abort

Le package mercurial ne veut pas s’installer, pour corriger lancer en
ssh:

    sudo rm /var/lib/dpkg/info/$mercurial* -f
    sudo apt-get install mercurial

-   Les dépendances semblent bloquées sur 75%

A 75% c’est le début de la compilation de la librairie openzwave ainsi
que du wrapper python openzwave. Cette étape est très longue, on peut
toutefois consulter la progression via la vue du log de mise à jour. Il
faut donc être simplement patient.

-   Erreur lors de la compilation de la librairie openzwave

        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed source if appropriate.
        See <file:///usr/share/doc/gcc-4.9/README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for target 'build' failed
        make: *** [build] Error 1

Cette erreur peut survenir suite à un manque de mémoire RAM durant la
compilation.

Depuis l’UI jeedom, lancez la compilation des dépendances.

Une fois lancée, en ssh, arrêtez ces processus (consommateurs en
mémoire) :

    sudo systemctl stop cron
    sudo systemctl stop apache2
    sudo systemctl stop mysql

Pour suivre l’avancement de la compilation, on fait un tail sur le
fichier log openzwave\_update.

    tail -f /var/www/html/log/openzwave_update

Lorsque la compilation est terminée et sans erreur, relancez les
services que vous avez arrêté

sudo systemctl start cron sudo systemctl start apache2 sudo systemctl
start mysql

> **Tip**
>
> Si vous êtes toujours sous nginx, il faudra remplacer **apache2** par
> **nginx**dans les commandes**stop**/**start**. Le fichier log
> openzwave\_update sera dans le dossier:
> /usr/share/nginx/www/jeedom/log .

Utilisation de la carte Razberry sur un Raspberry Pi 3
------------------------------------------------------

Pour utiliser un contrôleur Razberry sur un Raspberry Pi 3, le
contrôleur Bluetooth interne du Raspberry doit être désactivé.

add this line :

    dtoverlay=pi3-miniuart-bt

at the end of the file :

    /boot/config.txt

and restart the RPI3

API HTTP
========

Le plugin Z-Wave met à disposition des développeurs et des utilisateurs
une API complète afin de pouvoir opérer le réseau Z-Wave via requête
HTTP.

Il vous est possible d’exploiter l’ensemble des méthodes exposées par le
serveur REST du démon Z-Wave.

The syntax to invoke routes is as follows :

URL =
[http://token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/\#ROUTE\#](http://token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/#ROUTE#)

-   \#API\_KEY\# correspond à votre clé API, propre à
    votre installation. Pour la trouver, il faut aller dans le menu «
    Général », puis « Administration » et « Configuration », en activant
    le mode Expert, vous verrez alors une ligne Clef API.

-   \#IP\_JEEDOM\# correspond à votre url d’accès à Jeedom.

-   \#PORTDEMON\# correspond au numéro de port spécifié dans la page de
    configuration du plugin Z-Wave, par défaut: 8083.

-   \#ROUTE\# correspond à la route sur le serveur REST a exécuter.

Pour connaitre l’ensemble des routes, veuillez vous référer
[github](https://github.com/jeedom/plugin-openzwave) du plugin Z-Wave.

Example: Pour lancer un ping sur le noeud id 2

URL =
http://token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ZWaveAPI/Run/devices\[2\].TestNode()

# FAQ

> **J'ai l'erreur "Not enough space in stream buffer"**
>
> Malheureusement cette erreur est matériel, nous ne pouvons rien y faire et cherchons pour le moment comment forcer un redémarrage du démon dans le cas de cette erreur (mais souvent il faut en plus débrancher la clef pendant 5min pour que ca reparte)
