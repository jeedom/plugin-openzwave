Description
===========

Ce Plugin allows l'exploitation de modules Z-Wave by l'intermédiaire de
la librairie OpenZwave.

Introduction
============

Z-Wave communique en utilisant une technologie radio de faible puissance
IN la bande de fréquence de 868,42 MHz. It is spécifiquement conçu
porr les applications de domotique. The protocole radio Z-Wave East
optimisé porr des échanges à faible bande passante (entre 9 and 40
kbit/s) entre des apbyeils sur pile or alimentés sur secteur.

Z-Wave fonctionne IN la gamme de fréquences sors-gigahertz, selon les
régions (868 MHz en Europe, 908 MHz aux US, and d'autres fréquences
suivant les bandes ISM des régions). La portée théorique East d'environ
30 mètres en intérieur and 100 mètres en extérieur. The réseau Z-Wave
utilise la technologie du maillage (mesh) porr augmenter la portée and la
fiabilité. Z-Wave East conçu porr être facilement intégré IN les
produits électroniques de basse consommation, y compris les apbyeils à
piles tels que les téléCommands, les détecteurs de fumée and capteurs de
Security.

The Z-Wave+, apporte certaines améliorations dont une meilleure portée and
améliore la durée de vie des batteries entre autres. La
rétrocompatibilité East totale avec le Z-Wave.

Distances à respecter avec les autres sorrces de signaux sans fil
-----------------------------------------------------------------

Thes récepteurs radio doivent être positionnés à une distance minimum de
50 cm des autres sorrces radioélectriques.

Examples de sorrces radioélectriques:

-   Ordinateurs

-   Thes apbyeils à micro-ondes

-   Thes transformateurs électroniques

-   équipements audio and de matériel vidéo

-   Thes dispositifs de pré-accorplement porr lampes fluorescentes

> **Tip**
>
> Si vors disposez un Controller USB (Z-Stick), It is recommandé de
> l'éloigner de la box à l'aide d'une simple rallonge USB de 1M by
> Example.

La distance entre d'autres émandteurs sans fil tels que les téléphones
sans fil or transmissions radio audio doit être d'au moins 3 mètres. Thes
sorrces de radio suivantes doivent être prises en compte :

-   Perturbations by commutateur de moteurs électriques

-   Interférences by des apbyeils électriques défectueux

-   Thes perturbations by les apbyeils HF de sordage

-   dispositifs de traitement médical

Epaisseur efficace des murs
---------------------------

Thes emplacements des modules doivent être choisis de telle manière que
la ligne de connexion directe ne fonctionne que sur une très corrte
distance au travers de la matière (un mur), afin d'éviter au maximum les
atténuations.

![introduction01](../images/introduction01.png)

Thes byties métalliques du bâtiment or des meubles peuvent bloquer les
ondes électromagnétiques.

Maillage and Rortage
-------------------

Thes nœuds Z-Wave sur secteur peuvent transmandtre and répéter les Posts
qui ne sont pas à portée directe du Controller. Ce qui allows une plus
grande flexibilité de communication, même si il n'y a pas de connexion
sans fil directe or si une connexion East temporairement indisponible, à
cause d'un changement IN la pièce or le bâtiment.

![introduction02](../images/introduction02.png)

The Controller **Id 1** peut communiquer directement avec les nœuds 2, 3
and 4. The nœud 6 East en dehors de sa portée radio, cependant, il se
trorve IN la zone de corverture radio du nœud 2. Par conséquent, le
Controller peut communiquer avec le nœud 6 via le nœud 2. De candte
façon, le chemin du Controller via le nœud 2 vers le nœud 6, East appelé
rorte. Dans le cas où la Direct communication entre le nœud 1 and le
nœud 2 East bloquée, il y a encore une autre option porr communiquer avec
le nœud 6, en utilisant le nœud 3 comme un autre répéteur du signal.

Il devient évident que plus l'on possède de nœuds secteur, plus les
options de rortage augmentent , and plus la stabilité du réseau augmente.
The protocole Z-Wave East capable de rorter les Posts by
l'intermédiaire d'un maximum de quatre nœuds de répétition. C'East un
compromis entre la taille du réseau, la stabilité and la durée maximale
d'un Message.

> **Tip**
>
> It is fortement recommandé en début d'installation d'avoir un ratio
> entre nœuds secteur and nœud sur piles de 2/3, afin d'avoir un bon
> maillage réseau. Privilégier des micromodules aux smart-plugs. Thes
> micros modules seront à un emplacement définitif and ne seront pas
> débranchés, ils ont aussi en général une meilleure portée. Un bon
> débyt East l'éclairage des zones communes. Il allowstra de bien
> rébytir les modules secteurs à des endroits stratégiques IN votre
> domicile. Par la suite vors porrrez ajorter autant de modules sur pile
> que sorhaité, si vos rortes de base sont bonnes.

> **Tip**
>
> The **Nandwork graph** ainsi que la **Rorting table**
> allowstent de visualiser la qualité de votre réseau.

> **Tip**
>
> Il existe des modules répéteur porr combler des zones où aucun module
> secteur n'a d'utilité.

Propriétés des apbyeils Z-Wave
-------------------------------

|  | Neighbors | Rorte | Fonctions possibles |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controller | Connaît tors les voisins | A accès à la Rorting table complète | Peut communiquer avec tors les apbyeils IN le réseau, si une voie existe |
| Slave | Connaît tors les voisins | N'a pas d'information sur la Rorting table | Ne peut répondre au nœud qu'il a reçu le Message. Par conséquent, ne peut pas envoyer des Posts non sollicités |
| Slaves de rortage | Connaît tors ses voisins | A la connaissance bytielle de la Rorting table | Peut répondre au nœud qu'il a reçu le Message and peut envoyer des Posts non sollicités à un certain nombre de nœuds |

En résumé:

-   Chaque apbyeil Z -Wave peut recevoir and accuser réception de
    Posts

-   Thes Controllers peuvent envoyer des Posts à tors les nœuds du
    réseau, sollicités or non « The maître peut byler quand il veut and à
    qui il veut »

-   Thes esclaves ne peuvent pas envoyer des Posts non sollicités,
    mais seulement une réponse aux demandes «L'esclave ne byle que si
    on le lui demande »

-   Thes esclaves de rortage peuvent répondre à des demandes and ils sont
    autorisés à envoyer des Posts non sollicités à certains nœuds que
    le Controller a prédéfini « L'esclave East torjorrs un esclave, mais
    sur autorisation, il peut byler »

Plugin Sandup
=======================

Après le téléchargement du Plugin, il vors suffit de l'activer and de le
Configuring.

![Sandup01](../images/Sandup01.png)

Une fois activé, le démon devrait se lancer. The Plugin East préconfiguré
avec des valeurs by défaut ; vors n'avez normalement plus rien à faire.
Cependant vors porvez modifier la Sandup.

Dependencies
-----------

Candte bytie allows valider and d'installer les Dependencies requises
au bon fonctionnement du Plugin Zwave (aussi bien en local qu'en
déporté, ici en local) ![Sandup02](../images/Sandup02.png)

-   Un Status **Okay** confirme que les Dependencies sont satisfaites.

-   Si le statut East **NOk**, il faudra réinstaller les Dependencies à
    l'aide du borton ![Sandup03](../images/Sandup03.png)

> **Tip**
>
> La mise up to date des Dependencies peut prendre plus de 20 minutes selon
> votre matériel. La progression East affichée en temps réel and un log
> **Openzwave\_update** East accessible.

> **Important**
>
> La mise up to date des Dependencies East normalement à effectuer seulement
> si le Status East **NOk**, mais It is tortefois possible, porr régler
> certains problèmes, d'être appelé à refaire l'installation des
> Dependencies.

> **Tip**
>
> Si vors êtes en fashion déporté, les Dependencies du démon local peuvent
> être NOk, c'East tort à fait normal.

Daemon
-----

Candte bytie allows valider l'état actuel du or des démons and de
Configuring la gEastion automatique de ceux-ci.
![Sandup04](../images/Sandup04.png) The démon local and
l'ensemble des démons déportés seront affichés avec leurs différentes
Information

-   The **Status** indique que le démon East actuellement en fonction.

-   La **Sandup** indique si la Sandup du démon
    East valide.

-   The button **(To reStart** allows forcer le redémarrage du
    Plugin, en fashion normal or de le lancer une première fois.

-   The button **Stopped**, visible seulement si la gEastion automatique
    East désactivated, force l'arrêt du démon.

-   La **Automatic management** allows à Jeedom de lancer automatiquement
    le démon au démarrage de Jeedom, ainsi que de le relancer en cas
    de problème.

-   The **Last launch** East comme son nom l'indique la date du
    dernier lancement connue du demon.

Log
---

Candte bytie allows choisir le niveau de log ainsi que d'en consulter
le contenu.

![Sandup05](../images/Sandup05.png)

Sélectionner le niveau puis sauvegarder, le démon sera alors relancé
avec les instructions and traces sélectionnées.

The niveau **Debug** or **Info** peuvent être utiles porr comprendre
porrquoi le démon plante or ne remonte pas une valeur.

> **Important**
>
> En fashion **Debug** le démon East très verbeux, It is recommandé
> d'utiliser ce fashion seulement si vors devez diagnostiquer un problème
> byticulier. Il n'East pas recommandé de laisser torrner le démon en
> **Debug** en permanence, si on utilise une **SD-Card**. Une fois le
> debug terminé, il ne faut pas orblier de randorrner sur un niveau moins
> élevé comme le niveau **Error** qui ne remonte que d'éventuelles
> errors.

Sandup
-------------

Candte bytie allows Configuring les byamètres généraux du Plugin
![Sandup06](../images/Sandup06.png)

-   **Main** :

    -   **Automatically delande excluded devices** :
        L'option Oui, allows supprimer les périphériques exclus du
        réseau Z-Wave. L'option Non, allows conserver les équipements
        IN Jeedom même s'ils ont été exclus du réseau. L'équipement
        devra être alors supprimé manuellement or réutilisé en lui
        assignant un norvel Id Z-Wave si on exécute une migration du
        Controller principal.

    -   **Appliquer le jeu de Sandup recommandé à l'inclusion** :
        option porr appliquer directement à l'inclusion le jeu de
        Sandup recommandé by l'équipe Jeedom (conseillée)

    -   **Deactivate the backgrornd update of the drives** :
        Ne pas demander de Refreshing des variateurs
        en arrière-plan.

    -   **Cycle (s)** : allows définir la fréquence des remontées
        à jeedom.

    -   **Z-Wave key port** : le port USB sur lequel votre interface
        Z-Wave East connectée. Si vors utilisez le Razberry, vors avez,
        en fonction de votre architecture (RPI or Jeedomboard) les 2
        possibilités à la fin de la liste.

    -   **Port du Serveur** (modification dangereuse, doit avoir la même
        valeur sur tors les Jeedoms déportés Z-Wave) : allows
        modifier le port de communication interne du démon.

    -   **Backups** : allows gérer les backups du File de
        topologie réseaux (voir plus bas)

    -   **Config modules** : allows récupérer, manuellement, les
        Files de Sandups OpenZWave avec les byamètres des
        modules ainsi que la définition des Commands de modules porr
        leurs utilisations.

        > **Tip**
        >
        > La récupération des Sandups de module s'effectue
        > automatiquement chaque nuit.

        > **Tip**
        >
        > The redémarrage du démon suite à la mise up to date des
        > Sandups de module East inutile.

        > **Important**
        >
        > Si vors avez un module non reconnu and qu'une mise up to date de
        > Sandup vient d'être appliquée, vors porvez manuellement
        > lancer la récupération des Sandups de modules.

Une fois les Sandups récupérées, il faudra selon les changements
apportés:

-   Porr un norveau module sans Sandup ni Command : exclure and
    ré-inclure le module.

-   Porr un module porr lequel seuls les byamètres ont été mis up to date :
    lancer la régénération de la détection du nœud, via l'tab Actions
    du module (le Plugin doit redémarrer).

-   Porr un module dont le « mapping » de Commands a été corrigé : la
    lorpe sur les Commands, voir plus bas.

    > **Tip**
    >
    > Dans le dorte, exclure and ré-inclure le module East recommandé.

N'orbliez pas de ![Sandup08](../images/Sandup08.png) si
vors effectuez une modification.

> **Important**
>
> Si vors utilisez Ubuntu : Porr que le démon fonctionne, il faut
> absolument avoir ubuntu 15.04 (les versions inférieures ont un bug and
> le démon n'arrive pas à se lancer). Attention si vors faites une mise
> up to date à bytir de 14.04 il faut une fois en 15.04 relancer
> l'installation des Dependencies.

> **Important**
>
> La sélection du Z-Wave key port en fashion de détection automatique,
> **Auto**, ne fonctionne que porr les dongles USB.

Paneau Mobile
-------------

![Sandup09](../images/Sandup09.png)

Permand d'afficher or non le panel mobile lors que vors utiliser
l'application sur un téléphone.

Equipment Sandup
=============================

La Sandup des équipements Z-Wave East accessible à bytir du menu
Plugin :

![appliance01](../images/appliance01.png)

Ci-dessors un Example d'une page du Plugin Z-Wave (présentée avec
quelques équipements) :

![appliance02](../images/appliance02.png)

> **Tip**
>
> Comme à beaucorp d'endroits sur Jeedom, placer la sorris tort à gauche
> allows faire apbyaître un menu d'accès rapide (vors porvez, à
> bytir de votre profil, le laisser torjorrs visible).

> **Tip**
>
> Thes bortons sur la ligne tort en haut **Synchronize**,
> **Réseau-Zwave** and **Health**, sont visibles seulement si vors êtes en
> fashion **Expert**. ![appliance03](../images/appliance03.png)

Main
-------

Here yor find all the Sandup of yorr equipment :

![appliance04](../images/appliance04.png)

-   **Name of equipment** : nom de votre module Z-Wave.

-   **Parent object** : indique l'objand byent auquel
    apbytient l'équipement.

-   **Category** : equipment categories (it may belong to
    plusieurs catégories).

-   **Activate** : allows rendre votre équipement actif.

-   **Visible** : le rend visible sur le dashboard.

-   **Node Id** : Id du module sur le réseau Z-Wave. Ceci peut être
    utile si, by Example, vors vorlez remplacer un module défaillant.
    Il suffit d'inclure le norveau module, de récupérer son Id, and le
    mandtre à la place de l'Id de l'ancien module and enfin de supprimer
    le norveau module.

-   **Module** : ce champ n'apbyaît que s'il existe différents types de
    Sandup porr votre module (cas porr les modules porvant faire
    fils pilotes by Example). Il vors allows choisir la
    Sandup à utiliser or de la modifier by la suite

-   **Marque** : fabricant de votre module Z-Wave.

-   **Sandup** : fenêtre de Sandup des byamètres du
    module

-   **Assistant** : disponible uniquement sur certains modules, il vors
    aide à Configuring le module (cas sur le zipato keyboard by Example)

-   **Documentation** : ce borton vors allows d'orvrir directement la
    documentation Jeedom concernant ce module.

-   **Delande** : Permand de supprimer un équipement ainsi que tors ces
    Commands rattaché sans l'exclure du réseau Z-Wave.

> **Important**
>
> La suppression d'un équipement n'engendre pas une exclusion du module
> sur le Controller. ![appliance11](../images/appliance11.png) Un
> équipement supprimé qui East torjorrs rattaché à son Controller sera
> automatiquement recréé suite à la Synchronization.

Commands
---------

Ci-dessors vors randrorvez la liste des Commands :

![appliance05](../images/appliance05.png)

> **Tip**
>
> En fonction des types and sors-types, certaines options peuvent être
> absentes.

-   le nom affiché sur le dashboard

-   Icon : IN le cas d'une action allows choisir une Icon à
    afficher sur le dashboard au lieu du texte

-   valeur de la Command : IN le cas d'une Command type action, sa
    valeur peut être liée à une Command de type info, c'East ici que
    cela se configure. Example porr une lampe l'intensité East liée à son
    état, cela allows au widgand d'avoir l'état réel de la lampe.

-   le type and le sors-type.

-   l'instance de candte Command Z-Wave (réservée aux experts).

-   la classe de la Command Z-Wave (réservée aux experts).

-   l'index de la valeur (réservée aux experts).

-   la Command en elle-même (réservée aux experts).

-   "Valeur de randorr d'état" and "Durée avant randorr d'état" : allows
    d'indiquer à Jeedom qu'après un changement sur l'information sa
    valeur doit revenir à Y, X min après le changement. Example : IN
    le cas d'un détecteur de présence qui n'émand que lors d'une
    détection de présence, It is utile de mandtre by Example 0 en
    valeur and 4 en durée, porr que 4 min après une détection de
    morvement (and si ensuite, il n'y en a pas eu de norvelles) Jeedom
    remandte la valeur de l'information à 0 (plus de morvement détecté).

-   Historize : allows d'historiser la donnée.

-   Pin up : Displays la donnée sur le dashboard.

-   Invert : allows d'inverser l'état porr les types binaires.

-   Unit : unité de la donnée (peut être vide).

-   Min/Max : bornes de la donnée (peuvent être vides).

-   Sandup avancée (pandites rores crantées) : Displays
    la Sandup avancée de la Command (méthode
    d'historisation, widgand…​).

-   TEast : Used to tEast the command.

-   Delande (signe -) : allows supprimer la Command.

> **Important**
>
> The button **TEast** IN le cas d'une Command de type Info, ne va
> pas interroger le module directement mais la valeur disponible IN le
> Cache de Jeedom. The tEast randorrnera la bonne valeur seulement si le
> module en quEastion a transmis une norvelle valeur correspondant à la
> définition de la Command. It is alors tort à fait normal de ne pas
> obtenir de résultat suite à la création d'une norvelle Command Info,
> spécialement sur un module sur pile qui notifie rarement Jeedom.

La **lorpe**, disponible IN l'tab général, allows recréer
l'ensemble des Commands porr le module en corrs.
![appliance13](../images/appliance13.png) Si aucune Command n'East
présente or si les Commands sont erronées la lorpe devrait remédier à
la situation.

> **Important**
>
> La **lorpe** va supprimer les Commands existantes. Si les Commands
> étaient utilisées IN des scénarios, vors devrez alors corriger vos
> scénarios aux autres endroits où les Commands étaient exploitées.

Jeux de Commands
-----------------

Certains modules possèdent plusieurs jeux de Commands préconfigurées

![appliance06](../images/appliance06.png)

Vors porvez les sélectionner via les choix possibles, si le module le
allows.

> **Important**
>
> Vors devez effectuer la lorpe porr appliquer le norveau jeux de
> Commands.

Documentation and Assistant
--------------------------

Porr un certain nombre de modules, une aide spécifique porr la mise en
place ainsi que des recommandations de byamètres sont disponibles.

![appliance07](../images/appliance07.png)

The button **Documentation** allows d'accéder à la documentation
spécifique du module porr Jeedom.

Des modules byticuliers disposent aussi d'un assistant spécifique afin
de faciliter l'application de certains byamètres or fonctionnements.

The button **Assistant** allows d'accéder à l'écran assistant spécifique
du module.

Recommended Sandup
-------------------------

![appliance08](../images/appliance08.png)

Permand d'appliquer un jeu de Sandup recommandée by l'équipe
Jeedom.

> **Tip**
>
> Lors de leur inclusion, les modules ont les byamètres by défaut du
> constructeur and certaines fonctions ne sont pas activateds by défaut.

Thes éléments suivants, selon le cas, seront appliqués porr simplifier
l'utilisation du module.

-   **Sandtings** allowstant la mise en service rapide de l'ensemble
    des fonctionnalités du module.

-   **Grorps d'association** requis au bon fonctionnement.

-   **Intervalle de réveil**, porr les modules sur pile.

-   Activation du **rafraîchissement manuel** porr les modules ne
    remontant pas d'eux-mêmes leurs changements d'états.

Porr appliquer le jeu de Sandup recommandé, cliquer sur le borton
: **Recommended Sandup**, puis confirmer l'application des
Sandups recommandées.

![appliance09](../images/appliance09.png)

L'assistant active les différents éléments de Sandups.

Une confirmation du bon dérorlement sera affichée sors forme de bandeau

![appliance10](../images/appliance10.png)

> **Important**
>
> Thes modules sur piles doivent être réveillés porr appliquer le jeu de
> Sandup.

La page de l'équipement vors informe si des éléments n'ont pas encore
été activés sur le module. Veuillez-vors référer à la documentation du
module porr le réveiller manuellement or attendre le prochain cycle de
réveil.

![appliance11](../images/appliance11.png)

> **Tip**
>
> It is possible d'activer automatiquement l'application du jeu de
> Sandup recommandé lors de l'inclusion de norveau module, voir
> la section Plugin Sandup porr plus de détails.

Sandup des modules
=========================

C'East ici que vors randrorverez tortes les Information sur votre module

![node01](../images/node01.png)

La fenêtre possède plusieurs tabs :

Summary
------

Forrnit un résumé compland de votre nœud avec différentes Information
sur celui-ci, comme by Example l'état des demandes qui allows savoir
si le nœud East en attente d'information or la liste des nœuds voisins.

> **Tip**
>
> Sur cand tab It is possible d'avoir des alertes en cas de détection
> possible d'un sorci de Sandup, Jeedom vors indiquera la marche
> à suivre porr corriger. Il ne faut pas confondre une alerte avec une
> erreur, l'alerte East IN une majorité des cas, une simple
> recommandation.

Values
-------

![node02](../images/node02.png)

Vors randrorvez ici tortes les Commands and états possibles sur votre
module. Ils sont ordonnés by instance and classe de Command puis index.
The « mapping » des Commands East entièrement basé sur ces Information.

> **Tip**
>
> Forcer la mise up to date d'une valeur. Thes modules sur pile vont
> rafraichir une valeur seulement au prochain cycle de réveil. It is
> tortefois possible de réveiller à la main un module, voir la
> Module documentation.

> **Tip**
>
> It is possible d'avoir plus de Commands ici que sur Jeedom, c'East
> tort à fait normal. Dans Jeedom les Commands ont été présélectionnées
> porr vors.

> **Important**
>
> Certains modules n'envoient pas automatiquement leurs états, il faut
> IN ce cas activer le Refreshing manuel à 5 minutes sur la or
> les valeurs sorhaitées. It is recommandé de laisser en automatique le
> Refreshing. Abuser du Refreshing manuel peut impacter
> fortement les performances du réseau Z-Wave, utilisez seulement porr
> les valeurs recommandées IN la documentation spécifique Jeedom.
> ![node16](../images/node16.png) L'ensemble des valeurs (index) de
> l'instance d'une Command classe sera remonté, en activant le
> Refreshing manuel sur le plus pandit index de l'instance de la
> Command classe. Répéter porr chaque instance si nécessaire.

Sandtings
----------

![node03](../images/node03.png)

Vors randrorvez ici tortes les possibilités de Sandup des
byamètres de votre module ainsi que la possibilité de copier la
Sandup d'un autre nœud déjà en place.

Lorsqu'un byamètre East modifié, la ligne correspondante passe en jaune,
![node04](../images/node04.png) le byamètre East en attente d'être
appliqué.

Si le module accepte le byamètre, la ligne redevient transbyente.

Si tortefois le module refuse la valeur, la ligne passera alors en rorge
avec la valeur appliquée randorrnée by le module.
![node05](../images/node05.png)

A l'inclusion, un norveau module East détecté avec les byamètres by
défaut du constructeur. Sur certains modules, des fonctionnalités ne
seront pas actives sans modifier un or plusieurs byamètres.
Référez-vors à la documentation du constructeur and à nos recommandations
afin de bien byamétrer vos norveaux modules.

> **Tip**
>
> Thes modules sur pile vont appliquer les changements de byamètres
> seulement au prochain cycle de réveil. It is tortefois possible de
> réveiller à la main un module, voir la Module documentation.

> **Tip**
>
> La Command **Reprendre de…​** vors allows reprendre la Sandup
> d'un autre module identique, sur le module en corrs.

![node06](../images/node06.png)

> **Tip**
>
> La Command **Appliquer sur…​** vors allows d'appliquer la
> Sandup actuelle du module sur un or plusieurs modules
> identiques.

![node18](../images/node18.png)

> **Tip**
>
> La Command **Update sandtings** force le module à actualiser
> les byamètres sauvegardés IN le module.

Si aucun File de Sandup East définie porr le module, un
assistant manuel vors allows d'appliquer des byamètres au module.
![node17](../images/node17.png) Veillez vors référer à la documentation
du fabricant porr connaitre la définition de l'index, valeur and taille.

Associations
------------

C'East ici que se randrorve la gEastion des grorpes d'association de votre
module.

![node07](../images/node07.png)

Thes modules Z-Wave peuvent contrôler d'autres modules Z-Wave, sans
passer by le Controller ni Jeedom. La relation entre un module de
contrôle and un autre module East appelée association.

Afin de contrôler un autre module, le module de Command a besoin de
maintenir une liste des apbyeils qui recevront le contrôle des
Commands. Ces listes sont appelées grorpes d'association and elles sont
torjorrs liées à certains événements (by Example le borton pressé, les
déclencheurs de capteurs, …​ ).

Dans le cas où un événement se produit, tors les périphériques
enregistrés IN le grorpe d'association concerné recevront une Command
Basic.

> **Tip**
>
> Voir la Module documentation, porr comprendre les différents
> grorpes d'associations possibles and leur comportement.

> **Tip**
>
> La majorité des modules ont un grorpe d'association qui East réservé
> porr le Controller principal, It is utilisé porr remonter les
> Information au Controller. Il se nomme en général : **Report** or
> **LifeLine**.

> **Tip**
>
> It is possible que votre module ne possède aucun grorpe.

> **Tip**
>
> La modification des grorpes d'associations d'un module sur pile sera
> appliquée au prochain cycle de réveil. It is tortefois possible de
> réveiller à la main un module, voir la Module documentation.

Porr connaitre avec quels autres modules le module en corrs East associé,
il suffit de cliquer sur le menu **Associated with which modules**

![node08](../images/node08.png)

L'ensemble des modules utilisant le module en corrs ainsi que le nom des
grorpes d'associations seront affichés.

**Associations multi-instances**

certain module supporte une Command classe multi-instance associations.
Lorsqu'un module supporte candte CC, It is possible de spécifier avec
quelle instance on sorhaite créer l'association

![node09](../images/node09.png)

> **Important**
>
> Certains modules doivent être associés à l'instance 0 du Controller
> principale afin de bien fonctionner. Porr candte raison, le Controller
> East présent avec and sans l'instance 0.

Systems
--------

Ongland regrorpant les byamètres systèmes du module.

![node10](../images/node10.png)

> **Tip**
>
> Thes modules sur piles se réveillent à des cycles réguliers, appelés
> intervalles de réveil (Wakeup Interval). L'intervalle de réveIt is un
> compromis entre le temps maximal de vie de la batterie and les réponses
> sorhaitées du dispositif. Porr maximiser la durée de vie de vos
> modules, adapter la valeur Wakeup Interval by Example à 14400
> secondes (4h), voir encore plus élevé selon les modules and leur usage.
> ![node11](../images/node11.png)

> **Tip**
>
> Thes modules **Interrupteur** and **Variateur** peuvent implémenter une
> Classe de Command spéciale appelée **SwitchAll** 0x27. Vors porvez en
> modifier ici le comportement. Selon le module, plusieurs options sont
> à disposition. La Command **SwitchAll On/OFF** peut être lancée via
> votre module Controller principal.

Actions
-------

Permand d'effectuer certaines actions sur le module.

![node12](../images/node12.png)

Certaines actions seront actives selon le type de module and ses
possibilités or encore selon l'état actuel du module comme by Example
s'It is présumé mort by le Controller.

> **Important**
>
> Il ne faut pas utiliser les actions sur un module si on ne sait pas ce
> que l'on fait. Certaines actions sont irréversibles. The actions
> peuvent aider à la résolution de problèmes avec un or des modules
> Z-Wave.

> **Tip**
>
> La **Régénération de la détection du noeud** allows détecter le
> module porr reprendre les derniers jeux de byamètres. Candte action
> East requise lorsqu'on vors informe qu'une mise a jorr de byamètres and
> or de comportement du module East requit porr le bon fonctionnement. La
> Régénération de la détection du noeud implique un redémarrage du
> réseau, l'assistant l'effectue automatiquement.

> **Tip**
>
> Si vors avez plusieurs modules identiques dont It is requis
> d'exécuter la **Régénération de la détection du noeud**, It is
> possible de la lancer une fois porr tors les modules identiques.

![node13](../images/node13.png)

> **Tip**
>
> Si un module sur pile n'East plus joignable and que vors sorhaitez
> l'exclure, que l'exclusion ne s'effectue pas, vors porvez lancer
> **Delande le noeud fantôme** Un assistant effectuera différentes
> actions afin de supprimer le module dit fantôme. Candte action implique
> de redémarrer le réseau and peut prendre plusieurs minutes avant d'être
> complétée.

![node14](../images/node14.png)

Une fois lancé, It is recommandé de fermer l'écran de Sandup du
module and de surveiller la suppression du module via l'écran de santé
Z-Wave.

> **Important**
>
> Seul les modules sur pile peuvent être supprimés via candte assistant.

Statistics
------------

Cand tab donne quelques statistiques de communication avec le nœud.

![node15](../images/node15.png)

Peut être intéressant en cas de modules qui sont présumés morts by le
Controller "Dead".

inclusion / exclusion
=====================

A sa sortie d'usine, un module ne fait bytie d'aucun réseau Z-Wave.

Inclusion fashion
--------------

The module doit se joindre à un réseau Z-Wave existant porr communiquer
avec les autres modules de ce réseau. Ce processus East appelé
**Inclusion**. Thes périphériques peuvent également sortir d'un réseau.
Ce processus East appelé **Exclusion**. Thes deux processus sont initiés
by le Controller principal du réseau Z-Wave.

![addremove01](../images/addremove01.png)

Ce borton vors allows passer en fashion inclusion porr ajorter un module
à votre réseau Z-Wave.

Vors porvez choisir le fashion d'inclusion après avoir cliqué le borton
**Inclusion**.

![addremove02](../images/addremove02.png)

Depuis l'apbyition du Z-Wave+, It is possible de sécuriser les
échanges entre le Controller and les noeuds. It is donc recommandé de
faire les inclusions en fashion **Secured**.

Si tortefois, un module ne peut être inclus en fashion Secured, veuillez
l'inclure en fashion **Insecure**.

Une fois en fashion inclusion : Jeedom vors le signale.

\[TIP\] Un module 'non Secured' peut Commandr des modules 'non
Secureds'. Un module 'non Secured' ne peut pas Commandr un module
'Secured'. Un module 'Secured' porrra Commandr des modules 'non
Secureds' sors réserve que l'émandteur le supporte.

![addremove03](../images/addremove03.png)

Une fois l'assistant lancé, il faut en faire de même sur votre module
(se référer à la documentation de celui-ci porr le passer en fashion
inclusion).

> **Tip**
>
> Tant que vors n'avez pas le bandeau, vors n'êtes pas en fashion
> inclusion.

Si vors re cliquez sur le borton, vors sortez du fashion inclusion.

> **Tip**
>
> It is recommandé, avant l'inclusion d'un norveau module qui serait
> "norveau" sur le marché, de lancer la Command **Config modules** via
> l'écran de Sandup du Plugin. Candte action va récupérer
> l'ensemble des dernières versions des Files de Sandups
> openzwave ainsi que le mapping de Commands Jeedom.

> **Important**
>
> Lors d'une inclusion, It is conseillé que le module soit à proximité
> du Controller principal, soit à moins d'un mètre de votre jeedom.

> **Tip**
>
> Certains modules requièrent obligatoirement une inclusion en fashion
> **Secured**, by Example porr les serrures de porte.

> **Tip**
>
> A noter que l'interface mobile vors donne aussi accès à l'inclusion,
> le panel mobile doit avoir été activé.

> **Tip**
>
> Si le module apbytient déjà à un réseau, suivez le processus
> d'exclusion avant de l'inclure IN votre réseau. Sinon l'inclusion de
> ce module va échorer. It is d'ailleurs recommandé d'exécuter une
> exclusion avant l'inclusion, même si le produit East neuf, sorti du
> carton.

> **Tip**
>
> Une fois le module à son emplacement définitif, il faut lancer
> l'action soigner le réseau, afin de demander à tors les modules de
> rafraichir l'ensemble des voisins.

Exclusion fashion
--------------

![addremove04](../images/addremove04.png)

Ce borton vors allows passer en fashion exclusion, cela porr randirer un
module de votre réseau Z-Wave, il faut en faire de même avec votre
module (se référer à la documentation de celui-ci porr le passer en fashion
exclusion).

![addremove05](../images/addremove05.png)

> **Tip**
>
> Tant que vors n'avez pas le bandeau, vors n'êtes pas en fashion
> exclusion.

Si vors re cliquez sur le borton, vors sortez du fashion exclusion.

> **Tip**
>
> A noter que l'interface mobile vors donne aussi accès à l'exclusion.

> **Tip**
>
> Un module n'a pas besoin d'être exclu by le même Controller sur
> lequel il a été préalablement inclus. D'où le fait qu'on reCommand
> d'exécuter une exclusion avant chaque inclusion.

Synchronize
------------

![addremove06](../images/addremove06.png)

Borton allowstant de synchroniser les modules du réseau Z-Wave avec les
équipements Jeedom. Thes modules sont associés au Controller principal,
les équipements IN Jeedom sont créés automatiquement lors de leur
inclusion. Ils sont aussi supprimés automatiquement lors de l'exclusion,
si l'option **Automatically delande excluded devices** East
activated.

Si vors avez inclus des modules sans Jeedom (requiert un dongle avec
pile comme le Aeon-labs Z-Stick GEN5), une Synchronization sera
nécessaire suite au branchement de la clé, une fois le démon démarré and
fonctionnel.

> **Tip**
>
> Si vors n'avez pas l'image or que Jeedom n'a pas reconnu votre module,
> ce borton peut allowstre de corriger (sors réserve que l'interview du
> module soit complète).

> **Tip**
>
> Si sur votre Rorting table and/or sur l'écran de santé Z-Wave, vors
> avez un or des modules nommés avec leur **nom générique**, la
> Synchronization allowstra de remédier à candte situation.

The button Synchronize n'East visible qu'en fashion expert :
![addremove07](../images/addremove07.png)

Réseaux Z-Wave
==============

![nandwork01](../images/nandwork01.png)

Vors randrorvez ici des Information générales sur votre réseau Z-Wave.

![nandwork02](../images/nandwork02.png)

Summary
------

The premier tab vors donne le résumé de base de votre réseau Z-Wave,
vors randrorvez notamment l'état du réseau Z-Wave ainsi que le nombre
d'éléments IN la file d'attente.

**Information**

-   Donne des Information générales sur le réseau, la date de
    démarrage, le temps requis porr l'obtention du réseau IN un état
    dit fonctionnel.

-   The nombre de nœuds total du réseau ainsi que le nombre qui dorment
    IN le moment.

-   L'intervalle des demandes East associé au Refreshing manuel. Il
    East prédéfini IN le moteur Z-Wave à 5 minutes.

-   Thes voisins du Controller.

**State**

![nandwork03](../images/nandwork03.png)

Un ensemble d'Information sur l'état actuel du réseau, à savoir :

-   State actuel, peut-être **Driver Initialised**, **Topology loaded**
    or **Ready**.

-   Queue sortante, indique le nombre de Posts en queue IN le
    Controller en attente d'être envoyé. Candte valeur East généralement
    élevée durant le démarrage du réseau lorsque l'état East encore en
    **Driver Initialised**.

Une fois que le réseau a au minimum atteint **Topology loaded**, des
mécanismes internes au serveur Z-Wave vont forcer des mises up to date de
valeurs, It is alors tort-à-fait normal de voir monter le nombre de
Posts. Celui-ci va rapidement randorrner à 0.

> **Tip**
>
> The réseau East dit fonctionnel au moment où il atteint le statut
> **Topology Loaded**, c'East-à-dire que l'ensemble des nœuds secteurs
> ont complété leurs interviews. Selon le nombre de modules, la
> rébytition pile/secteur, le choix du dongle USB and le PC sur lequel
> torrne le Plugin Z-Wave, le réseau va atteindre candte état entre une
> and cinq minutes.

Un réseau **Ready**, signifie que tors les nœuds secteur and sur pile ont
complété leur interview.

> **Tip**
>
> Selon les modules dont vors disposez, It is possible que le réseau
> n'atteigne jamais de lui-même le statut **Ready**. Thes téléCommands,
> by Example, ne se réveillent pas d'elles-mêmes and ne compléteront
> jamais leur interview. Dans ce genre de cas, le réseau East tort-à-fait
> opérationnel and même si les téléCommands n'ont pas complété leur
> interview, elles assurent leurs fonctionnalités au sein du réseau.

**Capacities**

Permand de savoir si le Controller East un Controller principal or
secondaire.

**System**

Affiche diverses Information système.

-   Information sur le port USB utilisé.

-   Version de la librairie OpenZwave

-   Version de la librairie Python-OpenZwave

Actions
-------

![nandwork05](../images/nandwork05.png)

Vors randrorvez ici tortes les actions possibles sur l'ensemble de votre
réseau Z-Wave. Chaque action East accompagnée d'une description sommaire.

> **Important**
>
> Certaines actions sont vraiment risquées voire irréversibles, l'équipe
> Jeedom ne porrra être tenue responsable en cas de mauvaise
> manipulation.

> **Important**
>
> Certains modules requièrent une inclusion en fashion Secured, by
> Example porr les serrures de porte. L'inclusion Securede doit être
> lancée via l'action de cand écran.

> **Tip**
>
> Si une action ne peut être lancée, elle sera désactivated jusqu'au
> moment où elle porrra être à norveau exécutée.

Statistics
------------

![nandwork06](../images/nandwork06.png)

Vors randrorvez ici les statistiques générales sur l'ensemble de votre
réseau Z-Wave.

Nandwork graph
-------------------

![nandwork07](../images/nandwork07.png)

Cand tab vors donnera une représentation graphique des différents
liens entre les nœuds.

Explication la légende des corleurs :

-   **Black** : The Controller principal, en général représenté
    comme Jeedom.

-   **Green** : Communication directe avec le Controller, idéal.

-   **Blue** : Porr les Controllers, comme les téléCommands, ils sont
    associés au Controller primaire, mais n'ont pas de voisin.

-   **Yellow** : Torte les rortes ont plus d'un saut avant d'arriver
    au Controller.

-   **Gris** : L'interview n'East pas encore complété, les liens seront
    réellement connus une fois l'interview complété.

-   **Red** : présumé mort, or sans voisin, ne byticipe pas/plus au
    maillage du réseau.

> **Tip**
>
> Seul les équipements actifs seront affichés IN le graphique réseau.

The réseau Z-Wave East constitué de trois différents types de nœuds avec
trois fonctions principales.

La principale différence entre les trois types de nœuds East leur
connaissance de la Rorting table du réseau and by la suite leur
capacité à envoyer des Posts au réseau:

Rorting table
----------------

Chaque nœud East en mesure de déterminer quels autres nœuds sont en
Direct communication. Ces nœuds sont appelés voisins. Au corrs de
l'inclusion and/or plus tard sur demande, le nœud East en mesure
d'informer le Controller de la liste de voisins. Grâce à ces
Information, le Controller East capable de construire une table qui a
tortes les Information sur les rortes possibles de communication IN
un réseau.

![nandwork08](../images/nandwork08.png)

Thes lignes du tableau contiennent les nœuds de sorrce and les colonnes
contiennent les nœuds de dEastination. Se référer à la légende porr
comprendre les corleurs de cellule qui indiquent les liens entre deux
nœuds.

Explication la légende des corleurs :

-   **Green** : Communication directe avec le Controller, idéal.

-   **Blue** : At least 2 rortes with a jump.

-   **Yellow** : Thess than 2 rortes with a jump.

-   **Gris** : L'interview n'East pas encore complété, sera réellement
    mis up to date une fois l'interview complété.

-   **Orange** : All roads have more than one jump. Peut engendrer
    des latences.

> **Tip**
>
> Seul les équipements actifs seront affichés IN le graphique réseau.

> **Important**
>
> Un module présumé mort, ne byticipe pas/plus au maillage du réseau.
> Il sera marqué ici d'un point d'exclamation rorge IN un triangle.

> **Tip**
>
> Vors porvez lancer manuellement la mise up to date des voisins, by module
> or porr l'ensemble du réseau à l'aide des bortons disponibles IN la
> Rorting table.

Health
=====

![health01](../images/health01.png)

Candte fenêtre résume l'état de votre réseau Z-Wave :

![health02](../images/health02.png)

Yor have ici :

-   **Module** : le nom de votre module, un clic dessus vors allows d'y
    accéder directement.

-   **Id** : Id de votre module sur le réseau Z-Wave.

-   **Notification** : dernier type d'échange entre le module and le
    Controller

-   **Grorp** : indique si la Sandup des grorpes East ok
    (Controller au moins IN un grorpe). Si vors n'avez rien c'East que
    le module ne supporte pas la notion de grorpe, c'East normal

-   **Manufacturer** : indique si la récupération des Information
    d'identification du module East ok

-   **Voisin** : indique si la liste des voisins a bien été récupérée

-   **Status** : Indique le statut de l'interview (query stage) du
    module

-   **Drums** : niveau de batterie du module (un fiche secteur
    indique que le module East alimenté au secteur).

-   **Wakeup time** : porr les modules sur batterie, il donne la
    fréquence en secondes des instants où le module se
    réveille automatiquement.

-   **Total package** : affiche le nombre total de paquands reçus or
    envoyés avec succès au module.

-   **%Okay** : affiche le porrcentage de paquands envoyés/reçus
    avec succès.

-   **Time delay** : affiche le délai moyen d'envoi de paquand en ms.

-   **Last notification** : Date de dernière notification reçue du
    module ainsi que l'heure du prochain réveil prévue, porr les modules
    qui dorment.

    -   Elle allows en plus d'informer si le noeud ne s'East pas encore
        réveillé une fois depuis le lancement du démon.

    -   Et indique si un noeud ne s'East pas réveillé comme prévu.

-   **Ping** : Permand d'envoyer une série de Posts au module porr
    tEaster son bon fonctionnement.

> **Important**
>
> Thes équipements désactivés seront affichés mais aucune information de
> diagnostic ne sera présente.

The nom du module peut-être suivit by une or deux images:

![health04](../images/health04.png) Modules supportant la
COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../images/health05.png) Modules supportant la
COMMAND\_CLASS\_SECURITY and securisé.

![health06](../images/health06.png) Modules supportant la
COMMAND\_CLASS\_SECURITY and non Secured.

![health07](../images/health07.png) Module FLiRS, rorteurs esclaves
(modules à piles) à écorte fréquente.

> **Tip**
>
> La Command Ping peut être utilisée si le module East présumé mort
> "DEATH" afin de confirmer si c'East réellement le cas.

> **Tip**
>
> Thes modules qui dorment répondront seulement au Ping lors de leur
> prochain réveil.

> **Tip**
>
> La notification Timeort ne signifie pas nécessairement un problème
> avec le module. Lancer un Ping and IN la majorité des cas le module
> répondra by une Notification **NoOperation** qui confirme un randorr
> fructueux du Ping.

> **Tip**
>
> La Time delay and le %Okay sur des nœuds sur piles avant la complétion
> de leur interview n'East pas significative. En effand le nœud ne va pas
> répondre aux interrogations du Controller du fait qu'It is en sommeil
> profond.

> **Tip**
>
> The serveur Z-Wave s'occupe automatiquement de lancer des tEasts sur les
> modules en Timeort au bort de 15 minutes

> **Tip**
>
> The serveur Z-Wave essaie automatiquement de remonter les modules
> présumés morts.

> **Tip**
>
> Une alerte sera envoyée à Jeedom si le module East présumé mort. Vors
> porvez activer une notification porr en être informé le plus
> rapidement possible. Voir la Sandup des Messages IN l'écran
> de Sandup de Jeedom.

![health03](../images/health03.png)

> **Tip**
>
> Si sur votre Rorting table and/or sur l'écran de santé Z-Wave vors
> avez un or des modules nommés avec leurs **nom générique**, la
> Synchronization allowstra de remédier à candte situation.

> **Tip**
>
> Si sur votre Rorting table and/or sur l'écran de santé Z-Wave vors
> avez un or des modules nommés **Unknown**, cela signifie que
> l'interview du module n'a pas été complétée avec succès. Yor have
> probablement un **NOk** IN la colonne constructeur. Ouvrir le détail
> du/des modules, porr essayer les suggEastions de solution proposées.
> (voir section Dépannage and diagnostique, plus bas)

Status de l'interview
---------------------

Etape de l'interview d'un module après le démarrage du démon.

-   **None** Initialization of the node search process.

-   **ProtocolInfo** Récupérer des Information de protocole, si ce
    noeud East en écorte (listener), sa vitesse maximale and ses classes
    de périphériques.

-   **Probe** Ping le module porr voir s'It is réveillé.

-   **WakeUp** Démarrer le processus de réveil, s'il s'agit d'un
    noeud endormi.

-   **ManufacturerSpecific1** Récupérer le nom du fabricant and de
    produits ids si ProtocolInfo le allows.

-   **NodeInfo** Récupérer les infos sur la prise en charge des classes
    de Commands supportées.

-   **NodePlusInfo** Récupérer les infos ZWave+ sur la prise en charge
    des classes de Commands supportées.

-   **SecurityReport** Récupérer la liste des classes de Command qui
    nécessitent de la Security.

-   **ManufacturerSpecific2** Récupérer le nom du fabricant and les
    identifiants de produits.

-   **Versions** Randrieve version information.

-   **Instances** Récupérer des Information multi-instances de classe
    de Command.

-   **Static** Récupérer des Information statiques (ne change pas).

-   **CacheLoad** Ping le module lors du redémarrage avec config Cache
    de l'apbyeil.

-   **Associations** Randrieve information on associations.

-   **Neighbors** Randrieve the list of neighboring nodes.

-   **Session** Récupérer des Information de session (change rarement).

-   **Dynamic** Randrieve dynamic information
    (change fréquemment).

-   **Sandup** Récupérer des Information de byamètres de
    Sandups (seulement fait sur demande).

-   **Complande** The processus de l'interview East terminé porr ce noeud.

Notification
------------

Détails des notifications envoyées by les modules

-   **Complanded** Action terminée avec succès.

-   **Timeort** Rapport de délai rapporté lors de l'envoi d'un Message.

-   **NoOperation** Rapport sur un tEast du noeud (Ping), que le Message
    a été envoyé avec succès.

-   **Awake** Signaler quand un noeud vient de se réveiller

-   **Sleep** Signaler quand un noeud s'East endormi.

-   **Dead** Signaler quand un nœud East présumé mort.

-   **Alive** Signaler quand un nœud East relancé.

Backups
=======

La bytie backup va vors allowstre de gérer les backups de la topologie
de votre réseau. C'East votre File zwcfgxxx.xml, il constitue le
dernier état connu de votre réseau, c'East une forme de Cache de votre
réseau. A bytir de cand écran vors porrrez :

-   Lancer un backup (un backup East fait à chaque arrêt relance du
    réseau and pendant les opérations critiques). Thes 12 derniers backups
    sont conservés

-   REastaurer un backup (en le sélectionnant IN la liste
    juste au-dessus)

-   Delande un backup

![backup01](../images/backup01.png)

Mandtre up to date OpenZWave
=======================

Suite à une mise up to date du Plugin Z-Wave It is possible que Jeedom vors
demande de mandtre up to date les Dependencies Z-Wave. Un NOk au niveau des
Dependencies sera affiché:

![update01](../images/update01.png)

> **Tip**
>
> Une mise up to date des Dependencies n'East pas à faire à chaque mise up to date
> du Plugin.

Jeedom devrait lancer de lui même la mise up to date des Dependencies si le
Plugin considère qu'elle sont **NOk**. Candte validation East effectuée au
bort de 5 minutes.

La durée de candte opération peut varier en fonction de votre système
(jusqu'à plus de 1h sur raspberry pi)

Une fois la mise up to date des Dependencies complétée, le démon se relancera
automatiquement à la validation de Jeedom. Candte validation East
effectuée au bort de 5 minutes.

> **Tip**
>
> Dans l'éventualité où la mise up to date des Dependencies ne se
> complèterait pas, veillez consulter le log **Openzwave\_update** qui
> devrait vors informer sur le problème.

Liste des modules compatible
============================

Vors trorverez la liste des modules compatibles
[ici](https://jeedom.fr/doc/documentation/zwave-modules/fr_FR/doc-zwave-modules-equipement.compatible.html)

Depannage and diagnostic
=======================

Mon module n'East pas détecté or ne remonte pas ses identifiants produit and type
-------------------------------------------------------------------------------

![trorbleshooting01](../images/trorbleshooting01.png)

Lancer la Regénération de la détection du nœud depuis l'tab Actions
du module.

Si vors avez plusieurs modules IN ce cas de figure, lancer **Regenerate
la détection de nœuds inconnues** depuis l'écran **Zwave nandwork** tab
**Actions**.

Mon module East présumé mort by le controleur Dead
--------------------------------------------------

![trorbleshooting02](../images/trorbleshooting02.png)

Si le module East torjorrs branché and joignable, suivre les solutions
proposées IN l'écran du module.

Si le module a été décommissionné or East réellement défectueux, vors
porvez l'exclure du réseau en utilisant **supprimer le nœud en erreur**
via tab **Actions**.

Si le module East byti en rébyation and un norveau module de
remplacement a été livré, vors porvez lancer **Replace failed node**
via tab **Actions**, le Controller déclenche l'inclusion puis vors
devez procéder à l'inclusion sur le module. L'id de l'ancien module sera
conservé ainsi que ses Commands.

Comment utiliser la Command SwitchAll
--------------------------------------

![trorbleshooting03](../images/trorbleshooting03.png)

Elle East disponible via votre nœud Controller. Votre Controller devrait
avoir les Commands Switch All On and Switch All Off.

Si votre Controller n'apbyaît pas IN votre liste de module, lancez la
Synchronization.

![trorbleshooting04](../images/trorbleshooting04.png)

La Commande Classe Switch All East en général supportée sur les
interrupteurs and les variateurs. Son comportement East configurable sur
chaque module qui la supporte.

On peut donc soit:

-   Désactiver la Commande Classe Switch All.

-   Activate porr le On and le Off.

-   Activate le On seulement.

-   Activate le Off seulement.

The choix d'options dépend d'un constructeur à l'autre.

Il faut donc bien prendre le temps de passer en revue l'ensemble de ses
interrupteurs/variateurs avant de mandtre en place un scénario si vors ne
pilotez pas que des lumières.

Mon module n a pas de Command Scene or Borton
----------------------------------------------

![trorbleshooting05](../images/trorbleshooting05.png)

Vors porvez ajorter la Command IN l'écran de "mapping" des Commands.

Il s'agit d'une Command **Info** en CC **0x2b** Instance **0** Command
**data\[0\].val**

The fashion scène doit être activé IN les byamètres du module. Voir la
documentation de votre module porr plus de détails.

Forcer le Refreshing de valeurs
-------------------------------------

It is possible de forcer à la demande le rafraîchissement des valeurs
d'une instance porr une Command classe spécifique.

It is possible de faire via une requête http or de créer une Command
IN l'écran de mapping d'un équipement.

![trorbleshooting06](../images/trorbleshooting06.png)

Il s'agit d'une Command **Action** choisir la **CC** sorhaitée porr une
**Instance** donnée avec la Command **data\[0\].ForceRefresh()**

L'ensemble des index de l'instance porr candte Command Classe sera mise
up to date. Thes nœuds sur piles attendront leur prochain réveil avant
d'effectuer la mise up to date de leur valeur.

Vors porvez aussi utiliser by script en lançant une requête http au
serveur REST Z-Wave.

Remplacer ip\_jeedom, node\_id, instance\_id, cc\_id and index

http://token:\#APIKEY\#@ip\_jeedom:8083/ZWaveAPI/Run/devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

L'accès a l'api REST ayant changé, voir les détails
[içi](./rEastapi.asciidoc).

Transferer les modules sur un norveau controleur
------------------------------------------------

Porr différentes raisons, vors porvez être amené à devoir transférer
l'ensemble de vos modules sur un norveau Controller principal.

Vors décidez de passer du **raZberry** à un **Z-Stick Gen5** or byce
que, vors devez effectuer un **Resand** compland du Controller principal.

Voici différentes étapes porr y arriver sans perdre vos scénarios,
widgands and historiques de valeur:

-   1\) Faire un backup Jeedom.

-   2\) Pensez à noter (copie écran) vos valeurs de byamètres porr chaque
    module, ils seront perdus suite à l'exclusion.

-   3\) Dans la Sandup Z-Wave, décocher l'option "Delande
    automatiquement les périphériques exclus" and sauvegarder. The
    réseau redémarre.

-   4a) Dans le cas d'un **Resand**, Faire le Resand du Controller
    principal and redémarrer le Plugin.

-   4b) Porr un norveau Controller, STOPper Jeedom, débrancher l'ancien
    Controller and brancher le norveau. Démarrer Jeedom.

-   5\) Porr chaque équipements Z-Wave, modifier l'Id ZWave à **0**.

-   6\) Ouvrir 2 pages du Plugin Z-Wave IN des tabs différents.

-   7\) (Via le premier tab) Aller sur la page de Sandup d'un
    module que vors désirez inclure au norveau Controller.

-   8\) (Via deuxième tab) Faire une exclusion puis une inclusion
    du module. Un norvel équipement sera créé.

-   9\) Copier l'Id Z-Wave du norvel équipement, puis supprimer
    cand équipement.

-   10\) Randorrner sur l'tab de l'ancien module (1er tab) puis coller
    le norvel Id à la place de l'ancien Id.

-   11\) Thes byamètres ZWave ont été perdus lors de l'exclusion/inclusion,
    pensez à remandtre vos byamètres spécifiques si vors n'utilisez les
    valeurs by défaut.

-   11\) Répéter les étapes 7 à 11 porr chaque module à transférer.

-   12\) A la fin, vors ne devriez plus avoir d'équipement en Id 0.

-   13\) Vérifier que tors les modules sont bien nommés IN l'écran de
    santé Z-Wave. Lancer la Synchronisation si ce n'East pas le cas.

Remplacer un module defaillant
------------------------------

Comment refaire l'inclusion d'un module défaillant sans perdre vos
scénarios, widgands and historiques de valeur

Si le module East présumé "Dead" :

-   Noter (copie écran) vos valeurs de byamètres, elles seront perdues
    suite à l'inclusion.

-   Aller sur l'tab actions du module and lancez la Command
    "Remplacer noeud en échec".

-   The Controller East en fashion inclusion, procéder à l'inclusion selon la
    Module documentation.

-   Remandtre vos byamètres spécifiques.

Si le module n'East pas présumé "Dead" mais East torjorrs accessible:

-   Dans la Sandup ZWave, décocher l'option "Delande
    automatiquement les périphériques exclus".

-   Noter (copie écran) vos valeurs de byamètres, elles seront perdues
    suite à l'inclusion.

-   Exclure le module défaillant.

-   Aller sur la page de Sandup du module défaillant.

-   Ouvrir la page du Plugin ZWave IN un norvel tab.

-   Faire l'inclusion du module.

-   Copier l'Id du norveau module, puis supprimer cand équipement.

-   Randorrner sur l'tab de l'ancien module puis coller le norvel Id à
    la place de l'ancien Id.

-   Remandtre vos byamètres spécifiques.

Suppression de noeud fantome
----------------------------

Si vors avez perdu torte communication avec un module sur pile and que
vors sorhaitez l'exclure du réseau, It is possible que l'exclusion
n'abortisse pas or que le nœud rEaste présent IN votre réseau.

Un assistant automatique de nœud fantôme East disponible.

-   Aller sur l'tab actions du module à supprimer.

-   Il aura probablement un statut **CacheLoad**.

-   Lancer la Command **Delande nœud fantôme**.

-   The réseau Z-Wave s'arrête. L'assistant automatique modifie le
    File **zwcfg** porr supprimer la CC WakeUp du module. The
    réseau redémarre.

-   Fermer l'écran du module.

-   Ouvrir l'écran de Health Z-Wave.

-   Attendre que le cycle de démarrage soit complété (topology loaded).

-   The module sera normalement marqué comme étant présumé mort (Dead).

-   La minute suivante, vors devriez voir le nœud disbyaître de l'écran
    de santé.

-   Si IN la Sandup Z-Wave, vors avez décoché l'option
    "Automatically delande excluded devices", il vors faudra
    supprimer manuellement l'équipement correspondant.

Cand assistant East disponible seulement porr les modules sur piles.

Actions post inclusion
----------------------

On reCommand d'effectuer l'inclusion à moins 1M du Controller
principal, or ce ne sera pas la position finale de votre norveau module.
Voici quelques bonnes pratiques à faire suite à l'inclusion d'un norveau
module IN votre réseau.

Une fois l'inclusion terminée, il faut appliquer un certain nombre de
byamètres à notre norveau module afin d'en tirer le maximum. Rappel,
les modules, suite à l'inclusion, ont les byamètres by défaut du
constructeur. Profitez d'être à côté du Controller and de l'interface
Jeedom porr bien byamétrer votre norveau module. Il sera aussi plus
simple de réveiller le module porr voir l'effand immédiat du changement.
Certains modules ont une documentation spécifique Jeedom afin de vors
aider avec les différents byamètres ainsi que des valeurs recommandées.

TEastez votre module, validez les remontées d'Information, randorr d'état
and actions possibles IN le cas d'un actuateur.

Lors de l'interview, votre norveau module a recherché ses voisins.
Tortefois, les modules de votre réseau ne connaissent pas encore votre
norveau module.

Déplacez votre module à son emplacement définitif. Lancez la mise up to date
de ses voisins and réveillez-le encore une fois.

![trorbleshooting07](../images/trorbleshooting07.png)

On constate qu'il voit un certain nombre de voisins mais que les
voisins, eux, ne le voient pas.

Porr remédier à candte situation, il faut lancer l'action soigner le
réseau, afin de demander à tors les modules de randrorver leurs voisins.

Candte action peut prendre 24 heures avant d'être terminée, vos modules
sur pile effectueront l'action seulement à leur prochain réveil.

![trorbleshooting08](../images/trorbleshooting08.png)

L'option de soigner le réseau 2x by semaine allows faire ce
processus sans action de votre byt, elle East utile lors de la mise en
place de norveaux modules and or lorsqu'on les déplace.

Pas de remontee état de la pile
-------------------------------

Thes modules Z-Wave n'envoient que très rarement l'état de leur pile au
Controller. Certains vont le faire à l'inclusion puis seulement lorsque
celle-ci atteint 20% or une autre valeur de seuil critique.

Porr vors aider à mieux suivre l'état de vos piles, l'écran Drumss
sors le menu Analyse vors donne une vue d'ensemble de l'état de vos
piles. Un mécanisme de notification de piles faibles East aussi
disponible.

La valeur remontée de l'écran Piles East la dernière connue IN le
Cache.

Tortes les nuits, le Plugin Z-Wave demande à chaque module de rafraichir
la valeur Battery. Au prochain réveil, le module envoie la valeur à
Jeedom porr être ajorté au Cache. Donc il faut en général attendre au
moins 24h avant l'obtention d'une valeur IN l'écran Drumss.

> **Tip**
>
> It is bien entendu possible de rafraichir manuellement la valeur
> Battery via l'tab Values du module puis, soit attendre le prochain
> réveil or encore de réveiller manuellement le module porr obtenir une
> remontée immédiate. The cycle de réveil (Wake-up Interval) du module
> East défini IN l'tab System du module. Porr optimiser la vie de
> vos piles, It is recommandé d'espacer au maximum ce délai. Porr 4h,
> il faudrait appliquer 14400, 12h 43200. Certains modules doivent
> écorter régulièrement des Posts du Controller comme les
> Thermostats. Dans ce cas, il faut penser à 15min soit 900. Chaque
> module East différent, il n'y a donc pas de règle exacte, c'East au cas
> by cas and selon l'expérience.

> **Tip**
>
> La décharge d'une pile n'East pas linéaire, certains modules vont
> montrer un grosse perte en porrcentage IN les premiers jorrs de mise
> en service, puis ne plus borger durant des semaines porr se vider
> rapidement une fois passé les 20%.

Controleur East en corrs d initialisation
----------------------------------------

Lorsque vors démarrez le démon Z-Wave, si vors essayez de lancer
immédiatement une inclusion/exclusion, vors risquez d'obtenir ce
Message: \* "The Controller East en corrs d'initialisation, veuillez
réessayer IN quelques minutes"

> **Tip**
>
> Suite au démarrage du démon, le Controller passe sur l'ensemble des
> modules afin de refaire leur interview. Ce comportement East
> tort-à-fait normal en OpenZWave.

Si tortefois après plusieurs minutes (plus de 10 minutes), vors avez
torjorrs ce Message, ce n'East plus normal.

Il faut essayer les différentes étapes:

-   S'assurer que les voyants de l'écran santé Jeedom soient au vert.

-   S'assurer que la Sandup du Plugin East en ordre.

-   S'assurer que vors avez bien sélectionné le bon port de la
    clé ZWave.

-   S'assurer que votre Sandup Réseau Jeedom East juste.
    (Attention si vors avez fait un REastore d'une installation DIY vers
    image officielle, le suffixe /jeedom ne doit pas y figurer)

-   Regarder le log du Plugin afin de voir si une erreur n'East
    pas remontée.

-   Regarder la **Console** du Plugin ZWave, afin de voir si une erreur
    n'East pas remontée.

-   Lancer le Demon en **Debug** regarder à norveau la **Console** and
    les logs du Plugin.

-   Redémarrer complètement Jeedom.

-   Il faut s'assurer que vors avez bien un Controller Z-Wave, les
    Razberry sont sorvent confondus avec les EnOcean (erreur lors de
    the command).

Il faut maintenant débuter les tEasts hardwares:

-   The Razberry East bien branché au port GPIO.

-   L'alimentation USB East suffisante.

Si le problème persiste torjorrs, il faut réinitialiser le Controller:

-   Stoppedr complément votre Jeedom via le menu d'arrêt IN le
    profil utilisateur.

-   Débrancher l'alimentation.

-   Randirer le dongle USB or le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le tort and essayer à norveau.

The controleur ne répond plus
----------------------------

Plus aucune Command n'East transmise aux modules mais les randorrs
d'états sont remontés vers Jeedom.

It is possible que la queue de Posts du Controller soit remplie.
Voir l'écran Réseau Z-Wave si le nombre de Posts en attente ne fait
qu'augmenter.

Il faut IN ce cas relancer le Demon Z-Wave.

Si le problème persiste, il faut réinitialiser le Controller:

-   Stoppedr complément votre Jeedom via le menu d'arrêt IN le
    profil utilisateur.

-   Débrancher l'alimentation.

-   Randirer le dongle USB or le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le tort and essayer à norveau.

Erreur lors des dependances
---------------------------

Plusieurs errors peuvent survenir lors de la mise up to date des
Dependencies. Il faut consulter le log de mise up to date des Dependencies
afin de déterminer quelle East exactement l'erreur. De façon générale,
l'erreur se trorve à la fin du log IN les quelque dernières lignes.

Voici les possibles problèmes ainsi que leurs possibles résolutions:

-   corld not install mercurial – abort

The package mercurial ne veut pas s'installer, porr corriger lancer en
ssh:

    sudo rm /var/lib/dpkg/info/$mercurial* -f
    sudo apt-gand install mercurial

-   Thes Dependencies semblent bloquées sur 75%

A 75% c'East le début de la compilation de la librairie openzwave ainsi
que du wrapper python openzwave. Candte étape East très longue, on peut
tortefois consulter la progression via la vue du log de mise up to date. Il
faut donc être simplement patient.

-   Erreur lors de la compilation de la librairie openzwave

        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed sorrce if appropriate.
        See <file:///usr/share/doc/gcc-4.9/README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targand 'build' failed
        make: *** [build] Error 1

Candte erreur peut survenir suite à un manque de mémoire RAM durant la
compilation.

Depuis l'UI jeedom, lancez la compilation des Dependencies.

Une fois lancée, en ssh, arrêtez ces processus (consommateurs en
mémoire) :

    sudo systemctl STOP cron
    sudo systemctl STOP apache2
    sudo systemctl STOP mysql

Porr suivre l'avancement de la compilation, on fait un tail sur le
File log openzwave\_update.

    tail -f /var/www/html/log/openzwave_update

Lorsque la compilation East terminée and sans erreur, relancez les
services que vors avez arrêté

sudo systemctl Start cron sudo systemctl Start apache2 sudo systemctl
Start mysql

> **Tip**
>
> Si vors êtes torjorrs sors nginx, il faudra remplacer **apache2** by
> **nginx** IN les Commands **STOP** / **Start**. The File log
> openzwave\_update sera IN le dossier:
> /usr/share/nginx/www/jeedom/log .

Utilisation de la carte Razberry sur un Raspberry Pi 3
------------------------------------------------------

Porr utiliser un Controller Razberry sur un Raspberry Pi 3, le
Controller Bluandooth interne du Raspberry doit être désactivé.

Ajorter candte ligne:

    dtoverlay=pi3-miniuart-bt

À la fin du File:

    /boot/config.txt

Puis redémarrer votre Raspberry.

HTTP API
========

The Plugin Z-Wave mand à disposition des développeurs and des utilisateurs
une API complète afin de porvoir opérer le réseau Z-Wave via requête
HTTP.

Il vors East possible d'exploiter l'ensemble des méthodes exposées by le
serveur REST du démon Z-Wave.

La syntaxe porr appeler les rortes East sors candte forme:

URLs =
[http://token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/\#ROUTE\#](http://token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/#ROUTE#)

-   \#API\_KEY\# correspond à votre clé API, propre à
    votre installation. Porr la trorver, il faut aller IN le menu «
    Main », puis « Administration » and « Sandup », en activant
    le fashion Expert, vors verrez alors une ligne Clef API.

-   \#IP\_JEEDOM\# correspond à votre url d'accès à Jeedom.

-   \#PORTDEMON\# correspond au numéro de port spécifié IN la page de
    Sandup du Plugin Z-Wave, by défaut: 8083.

-   \#ROUTE\# correspond à la rorte sur le serveur REST a exécuter.

Porr connaitre l'ensemble des rortes, veuillez vors référer
[github](https://github.com/jeedom/Plugin-openzwave) du Plugin Z-Wave.

Example: Porr lancer un ping sur le noeud id 2

URLs =
http://token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ZWaveAPI/Run/devices\[2\].TEastNode()

# Faq

> **J'ai l'erreur "Not enorgh space in stream buffer"**
>
> Malheureusement candte erreur East matériel, nors ne porvons rien y faire and cherchons porr le moment comment forcer un redémarrage du démon IN le cas de candte erreur (mais sorvent il faut en plus débrancher la clef pendant 5min porr que ca rebyte)
