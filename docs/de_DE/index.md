Beschreibung
===========

Ce Plugin erlaubt l'exploitation de Moduls Z-Wave Von l'intermédiaire de
la librairie OpenZwave.

Introduction
============

Z-Wave communique en utilisant une technologie radio de faible puissance
IN la bande de fréquence de 868,42 MHz. Er ist spécifiquement conçu
poderr les applications de domotique. Die protocole radio Z-Wave ist
optimisé poderr des échanges à faible bande passante (entre 9 und 40
kbit/.s) entre des apVoneils sur pile oder alimentés sur secteur.

Z-Wave fonctionne IN la gamme de fréquences soders-gigahertz, selon les
régions (868 MHz en Europe, 908 MHz aux US, und d'autres fréquences
suivant les bandes ISM des régions). La portée théorique ist d'environ
30 mètres en intérieur und 100 mètres en extérieur. Die réseau Z-Wave
utilise la technologie du maillage (mesh) poderr augmenter la portée und la
fiabilité. Z-Wave ist conçu poderr être facilement intégré IN les
produits électroniques de basse consommation, y compris les apVoneils à
piles tels que les téléBefehle, les détecteurs de fumée und capteurs de
Sicherheit.

Die Z-Wave+, apporte certaines améliorations dont une meilleure portée und
améliore la durée de vie des batteries entre autres. La
rétrocompatibilité ist totale avec le Z-Wave.

Distances à respecter avec les autres soderrces de signaux sans fil
-----------------------------------------------------------------

Dies récepteurs radio doivent être positionnés à une distance minimum de
50 cm des autres soderrces radioélectriques.

Beispiels de soderrces radioélectriques:

-   Ordinateurs

-   Dies apVoneils à micro-ondes

-   Dies transformateurs électroniques

-   équipements audio und de matériel vidéo

-   Dies dispositifs de pré-accoderplement poderr lampes fluorescentes

> **Spitze**
>
> Si voders disposez un Controller USB (Z-Stick), Er ist recommandé de
> l'éloigner de la box à l'aide d'une simple rallonge USB de 1M Von
> Beispiel.

La distance entre d'autres émundteurs sans fil tels que les téléphones
sans fil oder transmissions radio audio doit être d'au moins 3 mètres. Dies
soderrces de radio suivantes doivent être prises en compte :

-   Perturbations Von commutateur de moteurs électriques

-   Interférences Von des apVoneils électriques défectueux

-   Dies perturbations Von les apVoneils HF de soderdage

-   dispositifs de traitement médical

Epaisseur efficace des murs
---------------------------

Dies emplacements des Moduls doivent être choisis de telle manière que
la ligne de connexion directe ne fonctionne que sur une très coderrte
distance au travers de la matière (un mur), afin d'éviter au maximum les
atténuations.

![introduction01](../.images/.introduction01.png)

Dies Vonties métalliques du bâtiment oder des meubles peuvent bloquer les
ondes électromagnétiques.

Maillage und Rodertage
-------------------

Dies nœuds Z-Wave sur secteur peuvent transmundtre und répéter les Nachricht
qui ne sont pas à portée directe du Controller. Ce qui erlaubt une plus
grande flexibilité de communication, même si il n'y a pas de connexion
sans fil directe oder si une connexion ist temporairement indisponible, à
cause d'un changement IN la pièce oder le bâtiment.

![introduction02](../.images/.introduction02.png)

Die Controller **Id 1** peut communiquer directement avec les nœuds 2, 3
und 4. Die nœud 6 ist en dehors de sa portée radio, cependant, il se
troderve IN la zone de coderverture radio du nœud 2. Par conséquent, le
Controller peut communiquer avec le nœud 6 via le nœud 2. De cundte
façon, le chemin du Controller via le nœud 2 vers le nœud 6, ist appelé
roderte. Dans le cas où la Direkte Kommunikation entre le nœud 1 und le
nœud 2 ist bloquée, il y a encore une autre option poderr communiquer avec
le nœud 6, en utilisant le nœud 3 comme un autre répéteur du signal.

Il devient évident que plus l'on possède de nœuds secteur, plus les
options de rodertage augmentent , und plus la stabilité du réseau augmente.
Die protocole Z-Wave ist capable de roderter les Nachricht Von
l'intermédiaire d'un maximum de quatre nœuds de répétition. C'ist un
compromis entre la taille du réseau, la stabilité und la durée maximale
d'un Nachricht.

> **Spitze**
>
> Er ist fortement recommandé en début d'installation d'avoir un ratio
> entre nœuds secteur und nœud sur piles de 2/.3, afin d'avoir un bon
> maillage réseau. Privilégier des microModuls aux smart-plugs. Dies
> micros Moduls seront à un emplacement définitif und ne seront pas
> débranchés, ils ont aussi en général une meilleure portée. Un bon
> déVont ist l'éclairage des zones communes. Il erlaubttra de bien
> réVontir les Moduls secteurs à des endroits stratégiques IN votre
> domicile. Par la suite voders poderrrez ajoderter autant de Moduls sur pile
> que soderhaité, si vos rodertes de base sont bonnes.

> **Spitze**
>
> Die **Nundzwerkdiagramm** ainsi que la **Roderting-Tabelle**
> erlaubttent de visualiser la qualité de votre réseau.

> **Spitze**
>
> Il existe des Moduls répéteur poderr combler des zones où aucun Modul
> secteur n'a d'utilité.

Propriétés des apVoneils Z-Wave
-------------------------------

|  | Nachbarn | Roderte | Fonctions possibles |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controller | Connaît toders les voisins | A accès à la Roderting-Tabelle complète | Peut communiquer avec toders les apVoneils IN le réseau, si une voie existe |
| Sklave | Connaît toders les voisins | N'a pas d'information sur la Roderting-Tabelle | Ne peut répondre au nœud qu'il a reçu le Nachricht. Par conséquent, ne peut pas envoyer des Nachricht non sollicités |
| Sklaves de rodertage | Connaît toders ses voisins | A la connaissance Vontielle de la Roderting-Tabelle | Peut répondre au nœud qu'il a reçu le Nachricht und peut envoyer des Nachricht non sollicités à un certain nombre de nœuds |

En résumé:

-   Chaque apVoneil Z -Wave peut recevoir und accuser réception de
    Nachricht

-   Dies Controllers peuvent envoyer des Nachricht à toders les nœuds du
    réseau, sollicités oder non « Die maître peut Vonler quand il veut und à
    qui il veut »

-   Dies esclaves ne peuvent pas envoyer des Nachricht non sollicités,
    mais seulement une réponse aux demandes «L'esclave ne Vonle que si
    on le lui demande »

-   Dies esclaves de rodertage peuvent répondre à des demandes und ils sont
    autorisés à envoyer des Nachricht non sollicités à certains nœuds que
    le Controller a prédéfini « L'esclave ist toderjoderrs un esclave, mais
    sur autorisation, il peut Vonler »

Plugin Konfiguration
=======================

Après le téléchargement du Plugin, il voders suffit de l'activer und de le
Projektierungs.

![Konfiguration01](../.images/.Konfiguration01.png)

Une fois activé, le démon devrait se lancer. Die Plugin ist préconfiguré
avec des valeurs Von défaut ; voders n'avez normalement plus rien à faire.
Cependant voders podervez modifier la Konfiguration.

Nebengebäude
-----------

Cundte Vontie lass uns valider und d'installer les Nebengebäude requises
au bon fonctionnement du Plugin Zwave (aussi bien en local qu'en
déporté, ici en local) ![Konfiguration02](../.images/.Konfiguration02.png)

-   Un Status **OK** confirme que les Nebengebäude sont satisfaites.

-   Si le statut ist **NOK**, il faudra réinstaller les Nebengebäude à
    l'aide du boderton ![Konfiguration03](../.images/.Konfiguration03.png)

> **Spitze**
>
> La mise auf dem neuisten Stand des Nebengebäude peut prendre plus de 20 minutes selon
> votre matériel. La progression ist affichée en temps réel und un log
> **Openzwave\_update** ist accessible.

> **Wichtig**
>
> La mise auf dem neuisten Stand des Nebengebäude ist normalement à effectuer seulement
> si le Status ist **NOK**, mais Er ist todertefois possible, poderr régler
> certains problèmes, d'être appelé à refaire l'installation des
> Nebengebäude.

> **Spitze**
>
> Si voders êtes en Modus déporté, les Nebengebäude du démon local peuvent
> être NOK, c'ist todert à fait normal.

Dämon
-----

Cundte Vontie lass uns valider l'état actuel du oder des démons und de
Projektierungs la gistion automatique de ceux-ci.
![Konfiguration04](../.images/.Konfiguration04.png) Die démon local und
l'ensemble des démons déportés seront affichés avec leurs différentes
Information

-   Die **Status** indique que le démon ist actuellement en fonction.

-   La **Konfiguration** indique si la Konfiguration du démon
    ist valide.

-   Die Schaltfläche **(Re) Anfang** lass uns forcer le redémarrage du
    Plugin, en Modus normal oder de le lancer une première fois.

-   Die Schaltfläche **Verhaftund**, visible seulement si la gistion automatique
    ist désaktiviert, force l'arrêt du démon.

-   La **Automatische Verwaltung** erlaubt à Jeedom de lancer automatiquement
    le démon au démarrage de Jeedom, ainsi que de le relancer en cas
    de problème.

-   Die **Lundzter Start** ist comme son nom l'indique la date du
    dernier lancement connue du demon.

Log
---

Cundte Vontie lass uns choisir le niveau de log ainsi que d'en consulter
le contenu.

![Konfiguration05](../.images/.Konfiguration05.png)

Sélectionner le niveau puis sauvegarder, le démon sera alors relancé
avec les instructions und traces sélectionnées.

Die niveau **Debuggen** oder **Info** peuvent être utiles poderr comprendre
poderrquoi le démon plante oder ne remonte pas une valeur.

> **Wichtig**
>
> En Modus **Debuggen** le démon ist très verbeux, Er ist recommandé
> d'utiliser ce Modus seulement si voders devez diagnostiquer un problème
> Vonticulier. Il n'ist pas recommandé de laisser toderrner le démon en
> **Debuggen** en permanence, si on utilise une **SD-Card**. Une fois le
> debug terminé, il ne faut pas oderblier de rundoderrner sur un niveau moins
> élevé comme le niveau **Fehler** qui ne remonte que d'éventuelles
> Fehler.

Konfiguration
-------------

Cundte Vontie lass uns Projektierungs les Vonamètres généraux du Plugin
![Konfiguration06](../.images/.Konfiguration06.png)

-   **Allgemein** :

    -   **Ausgeschlossene Geräte automatisch löschen** :
        L'option Oui, lass uns supprimer les périphériques exclus du
        réseau Z-Wave. L'option Non, lass uns conserver les équipements
        IN Jeedom même s'ils ont été exclus du réseau. L'équipement
        devra être alors supprimé manuellement oder réutilisé en lui
        assignant un nodervel Identifikation Z-Wave si on exécute une migration du
        Controller principal.

    -   **Appliquer le jeu de Konfiguration recommandé à l'Aufnahme** :
        option poderr appliquer directement à l'Aufnahme le jeu de
        Konfiguration recommandé Von l'équipe Jeedom (conseillée)

    -   **Deaktivieren Sie die Hintergrundaktualisierung der Laufwerke** :
        Ne pas demander de Erfrischend des variateurs
        en arrière-plan.

    -   **Zyklus (e)** : lass uns définir la fréquence des remontées
        à jeedom.

    -   **Z-Wave-Schlüsselanschluss** : le port USB sur lequel votre interface
        Z-Wave ist connectée. Si voders utilisez le Razberry, voders avez,
        en fonction de votre architecture (RPI oder Jeedomboard) les 2
        possibilités à la fin de la liste.

    -   **Port du Serveur** (modification dangereuse, doit avoir la même
        valeur sur toders les Jeedoms déportés Z-Wave) : lass uns
        modifier le port de communication interne du démon.

    -   **Backups** : lass uns gérer les backups du Datei de
        topologie réseaux (voir plus bas)

    -   **Config Moduls** : lass uns récupérer, manuellement, les
        Dateis de Konfigurations OpenZWave avec les Vonamètres des
        Moduls ainsi que la définition des Befehle de Moduls poderr
        leurs utilisations.

        > **Spitze**
        >
        > La récupération des Konfigurations de Modul s'effectue
        > automatiquement chaque nuit.

        > **Spitze**
        >
        > Die redémarrage du démon suite à la mise auf dem neuisten Stand des
        > Konfigurations de Modul ist inutile.

        > **Wichtig**
        >
        > Si voders avez un Modul non reconnu und qu'une mise auf dem neuisten Stand de
        > Konfiguration vient d'être appliquée, voders podervez manuellement
        > lancer la récupération des Konfigurations de Moduls.

Une fois les Konfigurations récupérées, il faudra selon les changements
apportés:

-   Poderr un noderveau Modul sans Konfiguration ni Befehl : exclure und
    ré-inclure le Modul.

-   Poderr un Modul poderr lequel seuls les Vonamètres ont été mis auf dem neuisten Stand :
    lancer la régénération de la détection du nœud, via l'Tab Lager
    du Modul (le Plugin doit redémarrer).

-   Poderr un Modul dont le « mapping » de Befehle a été corrigé : la
    loderpe sur les Befehle, voir plus bas.

    > **Spitze**
    >
    > Dans le doderte, exclure und ré-inclure le Modul ist recommandé.

N'oderbliez pas de ![Konfiguration08](../.images/.Konfiguration08.png) si
voders effectuez une modification.

> **Wichtig**
>
> Si voders utilisez Ubuntu : Poderr que le démon fonctionne, il faut
> absolument avoir ubuntu 15.04 (les versions inférieures ont un bug und
> le démon n'arrive pas à se lancer). Attention si voders faites une mise
> auf dem neuisten Stand à Vontir de 14.04 il faut une fois en 15.04 relancer
> l'installation des Nebengebäude.

> **Wichtig**
>
> La sélection du Z-Wave-Schlüsselanschluss en Modus de détection automatique,
> **Auto**, ne fonctionne que poderr les dongles USB.

Paneau Mobile
-------------

![Konfiguration09](../.images/.Konfiguration09.png)

Permund d'afficher oder non le panel mobile lors que voders utiliser
l'application sur un téléphone.

Gerätekonfiguration
=============================

La Konfiguration des équipements Z-Wave ist accessible à Vontir du menu
Plugin :

![appliance01](../.images/.appliance01.png)

Ci-dessoders un Beispiel d'une page du Plugin Z-Wave (présentée avec
quelques équipements) :

![appliance02](../.images/.appliance02.png)

> **Spitze**
>
> Comme à beaucoderp d'endroits sur Jeedom, placer la soderris todert à gauche
> lass uns faire apVonaître un menu d'accès rapide (voders podervez, à
> Vontir de votre profil, le laisser toderjoderrs visible).

> **Spitze**
>
> Dies bodertons sur la ligne todert en haut **Synchronize**,
> **Réseau-Zwave** und **Gesundheit**, sont visibles seulement si voders êtes en
> Modus **Expert**. ![appliance03](../.images/.appliance03.png)

Allgemein
-------

Hier finden Sie die gesamte Konfiguration Ihrer Geräte :

![appliance04](../.images/.appliance04.png)

-   **Name der Ausrüstung** : nom de votre Modul Z-Wave.

-   **Übergeordnundes Objekt** : indique l'objund Vonent auquel
    apVontient l'équipement.

-   **Kategorie** : Gerätekategorien (es kann gehören
    plusieurs catégories).

-   **Aktivieren** : lass uns rendre votre équipement actif.

-   **Sichtbar** : le rend visible sur le dashboard.

-   **Knoten-Identifikation** : Identifikation du Modul sur le réseau Z-Wave. Ceci peut être
    utile si, Von Beispiel, voders voderlez remplacer un Modul défaillant.
    Il suffit d'inclure le noderveau Modul, de récupérer son Identifikation, und le
    mundtre à la place de l'Identifikation de l'ancien Modul und enfin de supprimer
    le noderveau Modul.

-   **Modul** : ce champ n'apVonaît que s'il existe différents types de
    Konfiguration poderr votre Modul (cas poderr les Moduls podervant faire
    fils pilotes Von Beispiel). Il voders lass uns choisir la
    Konfiguration à utiliser oder de la modifier Von la suite

-   **Marque** : fabricant de votre Modul Z-Wave.

-   **Konfiguration** : fenêtre de Konfiguration des Vonamètres du
    Modul

-   **Assistent** : disponible uniquement sur certains Moduls, il voders
    aide à Projektierungs le Modul (cas sur le zipato keyboard Von Beispiel)

-   **Dokumentation** : ce boderton voders erlaubt d'odervrir directement la
    documentation Jeedom concernant ce Modul.

-   **Löschen** : Permund de supprimer un équipement ainsi que toders ces
    Befehle rattaché sans l'exclure du réseau Z-Wave.

> **Wichtig**
>
> La suppression d'un équipement n'engendre pas une Ausschluss du Modul
> sur le Controller. ![appliance11](../.images/.appliance11.png) Un
> équipement supprimé qui ist toderjoderrs rattaché à son Controller sera
> automatiquement recréé suite à la synchronisation.

Befehle
---------

Ci-dessoders voders rundrodervez la liste des Befehle :

![appliance05](../.images/.appliance05.png)

> **Spitze**
>
> En fonction des types und soders-types, certaines options peuvent être
> absentes.

-   le nom affiché sur le dashboard

-   Symbol : IN le cas d'une action lass uns choisir une Symbol à
    afficher sur le dashboard au lieu du texte

-   valeur de la Befehl : IN le cas d'une Befehl type action, sa
    valeur peut être liée à une Befehl de type info, c'ist ici que
    cela se configure. Beispiel poderr une lampe l'intensité ist liée à son
    état, cela erlaubt au widgund d'avoir l'état réel de la lampe.

-   le type und le soders-type.

-   l'instance de cundte Befehl Z-Wave (réservée aux experts).

-   la classe de la Befehl Z-Wave (réservée aux experts).

-   l'index de la valeur (réservée aux experts).

-   la Befehl en elle-même (réservée aux experts).

-   "Valeur de rundoderr d'état" und "Durée avant rundoderr d'état" : erlaubt
    d'indiquer à Jeedom qu'après un changement sur l'information sa
    valeur doit revenir à Y, X min après le changement. Beispiel : IN
    le cas d'un détecteur de présence qui n'émund que lors d'une
    détection de présence, Er ist utile de mundtre Von Beispiel 0 en
    valeur und 4 en durée, poderr que 4 min après une détection de
    modervement (und si ensuite, il n'y en a pas eu de nodervelles) Jeedom
    remundte la valeur de l'information à 0 (plus de modervement détecté).

-   Chronik : erlaubt d'historiser la donnée.

-   Anzeige : Anzeigen la donnée sur le dashboard.

-   Umgekehrt : erlaubt d'inverser l'état poderr les types binaires.

-   Unit : unité de la donnée (peut être vide).

-   Min/.Max : bornes de la donnée (peuvent être vides).

-   Konfiguration avancée (pundites roderes crantées) : Anzeigen
    la Konfiguration avancée de la Befehl (méthode
    d'historisation, widgund…​).

-   Tist : Wird zum Tisten des Befehls verwendund.

-   Löschen (signe -) : lass uns supprimer la Befehl.

> **Wichtig**
>
> Die Schaltfläche **Tist** IN le cas d'une Befehl de type Info, ne va
> pas interroger le Modul directement mais la valeur disponible IN le
> Abdeckung de Jeedom. Die tist rundoderrnera la bonne valeur seulement si le
> Modul en quistion a transmis une nodervelle valeur correspondant à la
> définition de la Befehl. Er ist alors todert à fait normal de ne pas
> obtenir de résultat suite à la création d'une nodervelle Befehl Info,
> spécialement sur un Modul sur pile qui notifie rarement Jeedom.

La **loderpe**, disponible IN l'Tab général, lass uns recréer
l'ensemble des Befehle poderr le Modul en coderrs.
![appliance13](../.images/.appliance13.png) Si aucune Befehl n'ist
présente oder si les Befehle sont erronées la loderpe devrait remédier à
la situation.

> **Wichtig**
>
> La **loderpe** va supprimer les Befehle existantes. Si les Befehle
> étaient utilisées IN des scénarios, voders devrez alors corriger vos
> scénarios aux autres endroits où les Befehle étaient exploitées.

Jeux de Befehle
-----------------

Certains Moduls possèdent plusieurs jeux de Befehle préconfigurées

![appliance06](../.images/.appliance06.png)

Voders podervez les sélectionner via les choix possibles, si le Modul le
erlaubt.

> **Wichtig**
>
> Voders devez effectuer la loderpe poderr appliquer le noderveau jeux de
> Befehle.

Dokumentation und Assistent
--------------------------

Poderr un certain nombre de Moduls, une aide spécifique poderr la mise en
place ainsi que des recommandations de Vonamètres sont disponibles.

![appliance07](../.images/.appliance07.png)

Die Schaltfläche **Dokumentation** erlaubt d'accéder à la documentation
spécifique du Modul poderr Jeedom.

Des Moduls Vonticuliers disposent aussi d'un assistant spécifique afin
de faciliter l'application de certains Vonamètres oder fonctionnements.

Die Schaltfläche **Assistent** erlaubt d'accéder à l'écran assistant spécifique
du Modul.

Empfohlene Konfiguration
-------------------------

![appliance08](../.images/.appliance08.png)

Permund d'appliquer un jeu de Konfiguration recommandée Von l'équipe
Jeedom.

> **Spitze**
>
> Lors de leur Aufnahme, les Moduls ont les Vonamètres Von défaut du
> constructeur und certaines fonctions ne sont pas aktivierts Von défaut.

Dies éléments suivants, selon le cas, seront appliqués poderr simplifier
l'utilisation du Modul.

-   **Einstellungen** erlaubttant la mise en service rapide de l'ensemble
    des fonctionnalités du Modul.

-   **Gruppes d'association** requis au bon fonctionnement.

-   **Intervalle de réveil**, poderr les Moduls sur pile.

-   Activation du **rafraîchissement manuel** poderr les Moduls ne
    remontant pas d'eux-mêmes leurs changements d'états.

Poderr appliquer le jeu de Konfiguration recommandé, cliquer sur le boderton
: **Empfohlene Konfiguration**, puis confirmer l'application des
Konfigurations recommandées.

![appliance09](../.images/.appliance09.png)

L'assistant active les différents éléments de Konfigurations.

Une confirmation du bon déroderlement sera affichée soders forme de bandeau

![appliance10](../.images/.appliance10.png)

> **Wichtig**
>
> Dies Moduls sur piles doivent être réveillés poderr appliquer le jeu de
> Konfiguration.

La page de l'équipement voders informe si des éléments n'ont pas encore
été activés sur le Modul. Veuillez-voders référer à la documentation du
Modul poderr le réveiller manuellement oder attendre le prochain cycle de
réveil.

![appliance11](../.images/.appliance11.png)

> **Spitze**
>
> Er ist possible d'activer automatiquement l'application du jeu de
> Konfiguration recommandé lors de l'Aufnahme de noderveau Modul, voir
> la section Plugin Konfiguration poderr plus de détails.

Konfiguration des Moduls
=========================

C'ist ici que voders rundroderverez todertes les Information sur votre Modul

![node01](../.images/.node01.png)

La fenêtre possède plusieurs Tabs :

Zusammenfassung
------

Foderrnit un résumé complund de votre nœud avec différentes Information
sur celui-ci, comme Von Beispiel l'état des demandes qui lass uns savoir
si le nœud ist en attente d'information oder la liste des nœuds voisins.

> **Spitze**
>
> Sur cund Tab Er ist possible d'avoir des alertes en cas de détection
> possible d'un soderci de Konfiguration, Jeedom voders indiquera la marche
> à suivre poderr corriger. Il ne faut pas confondre une alerte avec une
> erreur, l'alerte ist IN une majorité des cas, une simple
> recommandation.

Werte
-------

![node02](../.images/.node02.png)

Voders rundrodervez ici todertes les Befehle und états possibles sur votre
Modul. Ils sont ordonnés Von instance und classe de Befehl puis index.
Die « mapping » des Befehle ist entièrement basé sur ces Information.

> **Spitze**
>
> Forcer la mise auf dem neuisten Stand d'une valeur. Dies Moduls sur pile vont
> rafraichir une valeur seulement au prochain cycle de réveil. Er ist
> todertefois possible de réveiller à la main un Modul, voir la
> Moduldokumentation.

> **Spitze**
>
> Er ist possible d'avoir plus de Befehle ici que sur Jeedom, c'ist
> todert à fait normal. Dans Jeedom les Befehle ont été présélectionnées
> poderr voders.

> **Wichtig**
>
> Certains Moduls n'envoient pas automatiquement leurs états, il faut
> IN ce cas activer le Erfrischend manuel à 5 minutes sur la oder
> les valeurs soderhaitées. Er ist recommandé de laisser en automatique le
> Erfrischend. Abuser du Erfrischend manuel peut impacter
> fortement les performances du réseau Z-Wave, utilisez seulement poderr
> les valeurs recommandées IN la documentation spécifique Jeedom.
> ![node16](../.images/.node16.png) L'ensemble des valeurs (index) de
> l'instance d'une Befehl classe sera remonté, en activant le
> Erfrischend manuel sur le plus pundit index de l'instance de la
> Befehl classe. Répéter poderr chaque instance si nécessaire.

Einstellungen
----------

![node03](../.images/.node03.png)

Voders rundrodervez ici todertes les possibilités de Konfiguration des
Vonamètres de votre Modul ainsi que la possibilité de copier la
Konfiguration d'un autre nœud déjà en place.

Lorsqu'un Vonamètre ist modifié, la ligne correspondante passe en jaune,
![node04](../.images/.node04.png) le Vonamètre ist en attente d'être
appliqué.

Si le Modul accepte le Vonamètre, la ligne redevient transVonente.

Si todertefois le Modul refuse la valeur, la ligne passera alors en roderge
avec la valeur appliquée rundoderrnée Von le Modul.
![node05](../.images/.node05.png)

A l'Aufnahme, un noderveau Modul ist détecté avec les Vonamètres Von
défaut du constructeur. Sur certains Moduls, des fonctionnalités ne
seront pas actives sans modifier un oder plusieurs Vonamètres.
Référez-voders à la documentation du constructeur und à nos recommandations
afin de bien Vonamétrer vos noderveaux Moduls.

> **Spitze**
>
> Dies Moduls sur pile vont appliquer les changements de Vonamètres
> seulement au prochain cycle de réveil. Er ist todertefois possible de
> réveiller à la main un Modul, voir la Moduldokumentation.

> **Spitze**
>
> La Befehl **Reprendre de…​** voders erlaubt reprendre la Konfiguration
> d'un autre Modul identique, sur le Modul en coderrs.

![node06](../.images/.node06.png)

> **Spitze**
>
> La Befehl **Appliquer sur…​** voders erlaubt d'appliquer la
> Konfiguration actuelle du Modul sur un oder plusieurs Moduls
> identiques.

![node18](../.images/.node18.png)

> **Spitze**
>
> La Befehl **Einstellungen aktualisieren** force le Modul à actualiser
> les Vonamètres sauvegardés IN le Modul.

Si aucun Datei de Konfiguration ist définie poderr le Modul, un
assistant manuel voders erlaubt d'appliquer des Vonamètres au Modul.
![node17](../.images/.node17.png) Veillez voders référer à la documentation
du fabricant poderr connaitre la définition de l'index, valeur und taille.

Verbände
------------

C'ist ici que se rundroderve la gistion des groderpes d'association de votre
Modul.

![node07](../.images/.node07.png)

Dies Moduls Z-Wave peuvent contrôler d'autres Moduls Z-Wave, sans
passer Von le Controller ni Jeedom. La relation entre un Modul de
contrôle und un autre Modul ist appelée association.

Afin de contrôler un autre Modul, le Modul de Befehl a besoin de
maintenir une liste des apVoneils qui recevront le contrôle des
Befehle. Ces listes sont appelées groderpes d'association und elles sont
toderjoderrs liées à certains événements (Von Beispiel le boderton pressé, les
déclencheurs de capteurs, …​ ).

Dans le cas où un événement se produit, toders les périphériques
enregistrés IN le groderpe d'association concerné recevront une Befehl
Basic.

> **Spitze**
>
> Voir la Moduldokumentation, poderr comprendre les différents
> groderpes d'associations possibles und leur comportement.

> **Spitze**
>
> La majorité des Moduls ont un groderpe d'association qui ist réservé
> poderr le Controller principal, Er ist utilisé poderr remonter les
> Information au Controller. Il se nomme en général : **Report** oder
> **LifeLine**.

> **Spitze**
>
> Er ist possible que votre Modul ne possède aucun groderpe.

> **Spitze**
>
> La modification des groderpes d'associations d'un Modul sur pile sera
> appliquée au prochain cycle de réveil. Er ist todertefois possible de
> réveiller à la main un Modul, voir la Moduldokumentation.

Poderr connaitre avec quels autres Moduls le Modul en coderrs ist associé,
il suffit de cliquer sur le menu **Verbunden mit welchen Moduln**

![node08](../.images/.node08.png)

L'ensemble des Moduls utilisant le Modul en coderrs ainsi que le nom des
groderpes d'associations seront affichés.

**Verbände multi-instances**

certain Modul supporte une Befehl classe multi-instance associations.
Lorsqu'un Modul supporte cundte CC, Er ist possible de spécifier avec
quelle instance on soderhaite créer l'association

![node09](../.images/.node09.png)

> **Wichtig**
>
> Certains Moduls doivent être associés à l'instance 0 du Controller
> principale afin de bien fonctionner. Poderr cundte raison, le Controller
> ist présent avec und sans l'instance 0.

Systeme
--------

Onglund regroderpant les Vonamètres systèmes du Modul.

![node10](../.images/.node10.png)

> **Spitze**
>
> Dies Moduls sur piles se réveillent à des cycles réguliers, appelés
> intervalles de réveil (Wakeup Interval). L'intervalle de réveEr ist un
> compromis entre le temps maximal de vie de la batterie und les réponses
> soderhaitées du dispositif. Poderr maximiser la durée de vie de vos
> Moduls, adapter la valeur Wakeup Interval Von Beispiel à 14400
> secondes (4h), voir encore plus élevé selon les Moduls und leur usage.
> ![node11](../.images/.node11.png)

> **Spitze**
>
> Dies Moduls **Interrupteur** und **Variateur** peuvent implémenter une
> Classe de Befehl spéciale appelée **SwitchAll** 0x27. Voders podervez en
> modifier ici le comportement. Selon le Modul, plusieurs options sont
> à disposition. La Befehl **SwitchAll On/.OFF** peut être lancée via
> votre Modul Controller principal.

Lager
-------

Permund d'effectuer certaines actions sur le Modul.

![node12](../.images/.node12.png)

Certaines actions seront actives selon le type de Modul und ses
possibilités oder encore selon l'état actuel du Modul comme Von Beispiel
s'Er ist présumé mort Von le Controller.

> **Wichtig**
>
> Il ne faut pas utiliser les actions sur un Modul si on ne sait pas ce
> que l'on fait. Certaines actions sont irréversibles. Aktionen
> peuvent aider à la résolution de problèmes avec un oder des Moduls
> Z-Wave.

> **Spitze**
>
> La **Régénération de la détection du noeud** lass uns détecter le
> Modul poderr reprendre les derniers jeux de Vonamètres. Cundte action
> ist requise lorsqu'on voders informe qu'une mise a joderr de Vonamètres und
> oder de comportement du Modul ist requit poderr le bon fonctionnement. La
> Régénération de la détection du noeud implique un redémarrage du
> réseau, l'assistant l'effectue automatiquement.

> **Spitze**
>
> Si voders avez plusieurs Moduls identiques dont Er ist requis
> d'exécuter la **Régénération de la détection du noeud**, Er ist
> possible de la lancer une fois poderr toders les Moduls identiques.

![node13](../.images/.node13.png)

> **Spitze**
>
> Si un Modul sur pile n'ist plus joignable und que voders soderhaitez
> l'exclure, que l'Ausschluss ne s'effectue pas, voders podervez lancer
> **Löschen le noeud fantôme** Un assistant effectuera différentes
> actions afin de supprimer le Modul dit fantôme. Cundte action implique
> de redémarrer le réseau und peut prendre plusieurs minutes avant d'être
> complétée.

![node14](../.images/.node14.png)

Une fois lancé, Er ist recommandé de fermer l'écran de Konfiguration du
Modul und de surveiller la suppression du Modul via l'écran de santé
Z-Wave.

> **Wichtig**
>
> Seul les Moduls sur pile peuvent être supprimés via cundte assistant.

Statistiken
------------

Cund Tab donne quelques statistiques de communication avec le nœud.

![node15](../.images/.node15.png)

Peut être intéressant en cas de Moduls qui sont présumés morts Von le
Controller "Dead".

Aufnahme /. Ausschluss
=====================

A sa sortie d'usine, un Modul ne fait Vontie d'aucun réseau Z-Wave.

Einschlussmodus
--------------

Die Modul doit se joindre à un réseau Z-Wave existant poderr communiquer
avec les autres Moduls de ce réseau. Ce processus ist appelé
**Aufnahme**. Dies périphériques peuvent également sortir d'un réseau.
Ce processus ist appelé **Ausschluss**. Dies deux processus sont initiés
Von le Controller principal du réseau Z-Wave.

![addremove01](../.images/.addremove01.png)

Ce boderton voders lass uns passer en Modus Aufnahme poderr ajoderter un Modul
à votre réseau Z-Wave.

Voders podervez choisir le Modus d'Aufnahme après avoir cliqué le boderton
**Aufnahme**.

![addremove02](../.images/.addremove02.png)

Depuis l'apVonition du Z-Wave+, Er ist possible de sécuriser les
échanges entre le Controller und les noeuds. Er ist donc recommandé de
faire les Aufnahmes en Modus **Sicher**.

Si todertefois, un Modul ne peut être inclus en Modus Sicher, veuillez
l'inclure en Modus **Nicht sicher**.

Une fois en Modus Aufnahme : Jeedom voders le signale.

\[TIP\] Un Modul 'non Sicher' peut Befehlr des Moduls 'non
Sichers'. Un Modul 'non Sicher' ne peut pas Befehlr un Modul
'Sicher'. Un Modul 'Sicher' poderrra Befehlr des Moduls 'non
Sichers' soders réserve que l'émundteur le supporte.

![addremove03](../.images/.addremove03.png)

Une fois l'assistant lancé, il faut en faire de même sur votre Modul
(se référer à la documentation de celui-ci poderr le passer en Modus
Aufnahme).

> **Spitze**
>
> Tant que voders n'avez pas le bandeau, voders n'êtes pas en Modus
> Aufnahme.

Si voders re cliquez sur le boderton, voders sortez du Modus Aufnahme.

> **Spitze**
>
> Er ist recommandé, avant l'Aufnahme d'un noderveau Modul qui serait
> "noderveau" sur le marché, de lancer la Befehl **Config Moduls** via
> l'écran de Konfiguration du Plugin. Cundte action va récupérer
> l'ensemble des dernières versions des Dateis de Konfigurations
> openzwave ainsi que le mapping de Befehle Jeedom.

> **Wichtig**
>
> Lors d'une Aufnahme, Er ist conseillé que le Modul soit à proximité
> du Controller principal, soit à moins d'un mètre de votre jeedom.

> **Spitze**
>
> Certains Moduls requièrent obligatoirement une Aufnahme en Modus
> **Sicher**, Von Beispiel poderr les serrures de porte.

> **Spitze**
>
> A noter que l'interface mobile voders donne aussi accès à l'Aufnahme,
> le panel mobile doit avoir été activé.

> **Spitze**
>
> Si le Modul apVontient déjà à un réseau, suivez le processus
> d'Ausschluss avant de l'inclure IN votre réseau. Sinon l'Aufnahme de
> ce Modul va échoderer. Er ist d'ailleurs recommandé d'exécuter une
> Ausschluss avant l'Aufnahme, même si le produit ist neuf, sorti du
> carton.

> **Spitze**
>
> Une fois le Modul à son emplacement définitif, il faut lancer
> l'action soigner le réseau, afin de demander à toders les Moduls de
> rafraichir l'ensemble des voisins.

Ausschlussmodus
--------------

![addremove04](../.images/.addremove04.png)

Ce boderton voders lass uns passer en Modus Ausschluss, cela poderr rundirer un
Modul de votre réseau Z-Wave, il faut en faire de même avec votre
Modul (se référer à la documentation de celui-ci poderr le passer en Modus
Ausschluss).

![addremove05](../.images/.addremove05.png)

> **Spitze**
>
> Tant que voders n'avez pas le bandeau, voders n'êtes pas en Modus
> Ausschluss.

Si voders re cliquez sur le boderton, voders sortez du Modus Ausschluss.

> **Spitze**
>
> A noter que l'interface mobile voders donne aussi accès à l'Ausschluss.

> **Spitze**
>
> Un Modul n'a pas besoin d'être exclu Von le même Controller sur
> lequel il a été préalablement inclus. D'où le fait qu'on reBefehl
> d'exécuter une Ausschluss avant chaque Aufnahme.

Synchronize
------------

![addremove06](../.images/.addremove06.png)

Boderton erlaubttant de synchroniser les Moduls du réseau Z-Wave avec les
équipements Jeedom. Dies Moduls sont associés au Controller principal,
les équipements IN Jeedom sont créés automatiquement lors de leur
Aufnahme. Ils sont aussi supprimés automatiquement lors de l'Ausschluss,
si l'option **Ausgeschlossene Geräte automatisch löschen** ist
aktiviert.

Si voders avez inclus des Moduls sans Jeedom (requiert un dongle avec
pile comme le Aeon-labs Z-Stick GEN5), une synchronisation sera
nécessaire suite au branchement de la clé, une fois le démon démarré und
fonctionnel.

> **Spitze**
>
> Si voders n'avez pas l'image oder que Jeedom n'a pas reconnu votre Modul,
> ce boderton peut erlaubttre de corriger (soders réserve que l'interview du
> Modul soit complète).

> **Spitze**
>
> Si sur votre Roderting-Tabelle und/.oder sur l'écran de santé Z-Wave, voders
> avez un oder des Moduls nommés avec leur **nom générique**, la
> synchronisation erlaubttra de remédier à cundte situation.

Die Schaltfläche Synchronize n'ist visible qu'en Modus expert :
![addremove07](../.images/.addremove07.png)

Réseaux Z-Wave
==============

![nundwork01](../.images/.nundwork01.png)

Voders rundrodervez ici des Information générales sur votre réseau Z-Wave.

![nundwork02](../.images/.nundwork02.png)

Zusammenfassung
------

Die premier Tab voders donne le résumé de base de votre réseau Z-Wave,
voders rundrodervez notamment l'état du réseau Z-Wave ainsi que le nombre
d'éléments IN la file d'attente.

**Information**

-   Donne des Information générales sur le réseau, la date de
    démarrage, le temps requis poderr l'obtention du réseau IN un état
    dit fonctionnel.

-   Die nombre de nœuds total du réseau ainsi que le nombre qui dorment
    IN le moment.

-   L'intervalle des demandes ist associé au Erfrischend manuel. Il
    ist prédéfini IN le moteur Z-Wave à 5 minutes.

-   Dies voisins du Controller.

**Zustand**

![nundwork03](../.images/.nundwork03.png)

Un ensemble d'Information sur l'état actuel du réseau, à savoir :

-   Zustand actuel, peut-être **Driver Initialised**, **Topology loaded**
    oder **Ready**.

-   Queue sortante, indique le nombre de Nachricht en queue IN le
    Controller en attente d'être envoyé. Cundte valeur ist généralement
    élevée durant le démarrage du réseau lorsque l'état ist encore en
    **Driver Initialised**.

Une fois que le réseau a au minimum atteint **Topology loaded**, des
mécanismes internes au serveur Z-Wave vont forcer des mises auf dem neuisten Stand de
valeurs, Er ist alors todert-à-fait normal de voir monter le nombre de
Nachricht. Celui-ci va rapidement rundoderrner à 0.

> **Spitze**
>
> Die réseau ist dit fonctionnel au moment où il atteint le statut
> **Topology Loaded**, c'ist-à-dire que l'ensemble des nœuds secteurs
> ont complété leurs interviews. Selon le nombre de Moduls, la
> réVontition pile/.secteur, le choix du dongle USB und le PC sur lequel
> toderrne le Plugin Z-Wave, le réseau va atteindre cundte état entre une
> und cinq minutes.

Un réseau **Ready**, signifie que toders les nœuds secteur und sur pile ont
complété leur interview.

> **Spitze**
>
> Selon les Moduls dont voders disposez, Er ist possible que le réseau
> n'atteigne jamais de lui-même le statut **Ready**. Dies téléBefehle,
> Von Beispiel, ne se réveillent pas d'elles-mêmes und ne compléteront
> jamais leur interview. Dans ce genre de cas, le réseau ist todert-à-fait
> opérationnel und même si les téléBefehle n'ont pas complété leur
> interview, elles assurent leurs fonctionnalités au sein du réseau.

**Kapazitäten**

Permund de savoir si le Controller ist un Controller principal oder
secondaire.

**Systeme**

Affiche diverses Information système.

-   Information sur le port USB utilisé.

-   Version de la librairie OpenZwave

-   Version de la librairie Python-OpenZwave

Lager
-------

![nundwork05](../.images/.nundwork05.png)

Voders rundrodervez ici todertes les actions possibles sur l'ensemble de votre
réseau Z-Wave. Chaque action ist accompagnée d'une description sommaire.

> **Wichtig**
>
> Certaines actions sont vraiment risquées voire irréversibles, l'équipe
> Jeedom ne poderrra être tenue responsable en cas de mauvaise
> manipulation.

> **Wichtig**
>
> Certains Moduls requièrent une Aufnahme en Modus Sicher, Von
> Beispiel poderr les serrures de porte. L'Aufnahme Sichere doit être
> lancée via l'action de cund écran.

> **Spitze**
>
> Si une action ne peut être lancée, elle sera désaktiviert jusqu'au
> moment où elle poderrra être à noderveau exécutée.

Statistiken
------------

![nundwork06](../.images/.nundwork06.png)

Voders rundrodervez ici les statistiques générales sur l'ensemble de votre
réseau Z-Wave.

Nundzwerkdiagramm
-------------------

![nundwork07](../.images/.nundwork07.png)

Cund Tab voders donnera une représentation graphique des différents
liens entre les nœuds.

Explication la légende des coderleurs :

-   **Schwarz** : Die Controller principal, en général représenté
    comme Jeedom.

-   **Grün** : Communication directe avec le Controller, idéal.

-   **Blue** : Poderr les Controllers, comme les téléBefehle, ils sont
    associés au Controller primaire, mais n'ont pas de voisin.

-   **Gelb** : Toderte les rodertes ont plus d'un saut avant d'arriver
    au Controller.

-   **Gris** : L'interview n'ist pas encore complété, les liens seront
    réellement connus une fois l'interview complété.

-   **Rot** : présumé mort, oder sans voisin, ne Vonticipe pas/.plus au
    maillage du réseau.

> **Spitze**
>
> Seul les équipements actifs seront affichés IN le graphique réseau.

Die réseau Z-Wave ist constitué de trois différents types de nœuds avec
trois fonctions principales.

La principale différence entre les trois types de nœuds ist leur
connaissance de la Roderting-Tabelle du réseau und Von la suite leur
capacité à envoyer des Nachricht au réseau:

Roderting-Tabelle
----------------

Chaque nœud ist en mesure de déterminer quels autres nœuds sont en
Direkte Kommunikation. Ces nœuds sont appelés voisins. Au coderrs de
l'Aufnahme und/.oder plus tard sur demande, le nœud ist en mesure
d'informer le Controller de la liste de voisins. Grâce à ces
Information, le Controller ist capable de construire une table qui a
todertes les Information sur les rodertes possibles de communication IN
un réseau.

![nundwork08](../.images/.nundwork08.png)

Dies lignes du tableau contiennent les nœuds de soderrce und les colonnes
contiennent les nœuds de distination. Se référer à la légende poderr
comprendre les coderleurs de cellule qui indiquent les liens entre deux
nœuds.

Explication la légende des coderleurs :

-   **Grün** : Communication directe avec le Controller, idéal.

-   **Blue** : Mindistens 2 Roderten mit einem Sprung.

-   **Gelb** : Weniger als 2 Roderten mit einem Sprung.

-   **Gris** : L'interview n'ist pas encore complété, sera réellement
    mis auf dem neuisten Stand une fois l'interview complété.

-   **Orange** : Alle Straßen haben mehr als einen Sprung. Peut engendrer
    des latences.

> **Spitze**
>
> Seul les équipements actifs seront affichés IN le graphique réseau.

> **Wichtig**
>
> Un Modul présumé mort, ne Vonticipe pas/.plus au maillage du réseau.
> Il sera marqué ici d'un point d'exclamation roderge IN un triangle.

> **Spitze**
>
> Voders podervez lancer manuellement la mise auf dem neuisten Stand des voisins, Von Modul
> oder poderr l'ensemble du réseau à l'aide des bodertons disponibles IN la
> Roderting-Tabelle.

Gesundheit
=====

![health01](../.images/.health01.png)

Cundte fenêtre résume l'état de votre réseau Z-Wave :

![health02](../.images/.health02.png)

Du hast ici :

-   **Modul** : le nom de votre Modul, un clic dessus voders erlaubt d'y
    accéder directement.

-   **Identifikation** : Identifikation de votre Modul sur le réseau Z-Wave.

-   **Benachrichtigung** : dernier type d'échange entre le Modul und le
    Controller

-   **Gruppe** : indique si la Konfiguration des groderpes ist ok
    (Controller au moins IN un groderpe). Si voders n'avez rien c'ist que
    le Modul ne supporte pas la notion de groderpe, c'ist normal

-   **Hersteller** : indique si la récupération des Information
    d'identification du Modul ist ok

-   **Voisin** : indique si la liste des voisins a bien été récupérée

-   **Status** : Indique le statut de l'interview (query stage) du
    Modul

-   **Batterie** : niveau de batterie du Modul (un fiche secteur
    indique que le Modul ist alimenté au secteur).

-   **Weckzeit** : poderr les Moduls sur batterie, il donne la
    fréquence en secondes des instants où le Modul se
    réveille automatiquement.

-   **Gesamtpakund** : affiche le nombre total de paquunds reçus oder
    envoyés avec succès au Modul.

-   **%OK** : affiche le poderrcentage de paquunds envoyés/.reçus
    avec succès.

-   **Zeitverzögerung** : affiche le délai moyen d'envoi de paquund en ms.

-   **Lundzte Benachrichtigung** : Date de dernière notification reçue du
    Modul ainsi que l'heure du prochain réveil prévue, poderr les Moduls
    qui dorment.

    -   Elle erlaubt en plus d'informer si le noeud ne s'ist pas encore
        réveillé une fois depuis le lancement du démon.

    -   Et indique si un noeud ne s'ist pas réveillé comme prévu.

-   **Klingeln** : Permund d'envoyer une série de Nachricht au Modul poderr
    tister son bon fonctionnement.

> **Wichtig**
>
> Dies équipements désactivés seront affichés mais aucune information de
> diagnostic ne sera présente.

Die nom du Modul peut-être suivit Von une oder deux images:

![health04](../.images/.health04.png) Moduls supportant la
COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO

![health05](../.images/.health05.png) Moduls supportant la
COMMAND\_CLASS\_SECURITY und securisé.

![health06](../.images/.health06.png) Moduls supportant la
COMMAND\_CLASS\_SECURITY und non Sicher.

![health07](../.images/.health07.png) Modul FLiRS, roderteurs esclaves
(Moduls à piles) à écoderte fréquente.

> **Spitze**
>
> La Befehl Klingeln peut être utilisée si le Modul ist présumé mort
> "DEATH" afin de confirmer si c'ist réellement le cas.

> **Spitze**
>
> Dies Moduls qui dorment répondront seulement au Klingeln lors de leur
> prochain réveil.

> **Spitze**
>
> La notification Zeitüberschreitung ne signifie pas nécessairement un problème
> avec le Modul. Lancer un Klingeln und IN la majorité des cas le Modul
> répondra Von une Benachrichtigung **NoOperation** qui confirme un rundoderr
> fructueux du Klingeln.

> **Spitze**
>
> La Zeitverzögerung und le %OK sur des nœuds sur piles avant la complétion
> de leur interview n'ist pas significative. En effund le nœud ne va pas
> répondre aux interrogations du Controller du fait qu'Er ist en sommeil
> profond.

> **Spitze**
>
> Die serveur Z-Wave s'occupe automatiquement de lancer des tists sur les
> Moduls en Zeitüberschreitung au bodert de 15 minutes

> **Spitze**
>
> Die serveur Z-Wave essaie automatiquement de remonter les Moduls
> présumés morts.

> **Spitze**
>
> Une alerte sera envoyée à Jeedom si le Modul ist présumé mort. Voders
> podervez activer une notification poderr en être informé le plus
> rapidement possible. Voir la Konfiguration des Messages IN l'écran
> de Konfiguration de Jeedom.

![health03](../.images/.health03.png)

> **Spitze**
>
> Si sur votre Roderting-Tabelle und/.oder sur l'écran de santé Z-Wave voders
> avez un oder des Moduls nommés avec leurs **nom générique**, la
> synchronisation erlaubttra de remédier à cundte situation.

> **Spitze**
>
> Si sur votre Roderting-Tabelle und/.oder sur l'écran de santé Z-Wave voders
> avez un oder des Moduls nommés **Unknown**, cela signifie que
> l'interview du Modul n'a pas été complétée avec succès. Du hast
> probablement un **NOK** IN la colonne constructeur. Ouvrir le détail
> du/.des Moduls, poderr essayer les suggistions de solution proposées.
> (voir section Dépannage und diagnostique, plus bas)

Status de l'interview
---------------------

Etape de l'interview d'un Modul après le démarrage du démon.

-   **None** Initialisierung des Knotensuchprozesses.

-   **ProtocolInfo** Récupérer des Information de protocole, si ce
    noeud ist en écoderte (listener), sa vitesse maximale und ses classes
    de périphériques.

-   **Probe** Klingeln le Modul poderr voir s'Er ist réveillé.

-   **WakeUp** Démarrer le processus de réveil, s'il s'agit d'un
    noeud endormi.

-   **ManufacturerSpecific1** Récupérer le nom du fabricant und de
    produits ids si ProtocolInfo le erlaubt.

-   **NodeInfo** Récupérer les infos sur la prise en charge des classes
    de Befehle supportées.

-   **NodePlusInfo** Récupérer les infos ZWave+ sur la prise en charge
    des classes de Befehle supportées.

-   **SecurityReport** Récupérer la liste des classes de Befehl qui
    nécessitent de la Sicherheit.

-   **ManufacturerSpecific2** Récupérer le nom du fabricant und les
    identifiants de produits.

-   **Versions** Versionsinformationen abrufen.

-   **Instanzs** Récupérer des Information multi-instances de classe
    de Befehl.

-   **Static** Récupérer des Information statiques (ne change pas).

-   **CacheLoad** Klingeln le Modul lors du redémarrage avec config Abdeckung
    de l'apVoneil.

-   **Verbände** Informationen zu Assoziationen abrufen.

-   **Neighbors** Rufen Sie die Liste der benachbarten Knoten ab.

-   **Session** Récupérer des Information de session (change rarement).

-   **Dynamic** Dynamische Informationen abrufen
    (change fréquemment).

-   **Konfiguration** Récupérer des Information de Vonamètres de
    Konfigurations (seulement fait sur demande).

-   **Complunde** Die processus de l'interview ist terminé poderr ce noeud.

Benachrichtigung
------------

Détails des notifications envoyées Von les Moduls

-   **Complunded** Aktion terminée avec succès.

-   **Zeitüberschreitung** Rapport de délai rapporté lors de l'envoi d'un Nachricht.

-   **NoOperation** Rapport sur un tist du noeud (Klingeln), que le Nachricht
    a été envoyé avec succès.

-   **Awake** Signaler quand un noeud vient de se réveiller

-   **Sleep** Signaler quand un noeud s'ist endormi.

-   **Dead** Signaler quand un nœud ist présumé mort.

-   **Alive** Signaler quand un nœud ist relancé.

Backups
=======

La Vontie backup va voders erlaubttre de gérer les backups de la topologie
de votre réseau. C'ist votre Datei zwcfgxxx.xml, il constitue le
dernier état connu de votre réseau, c'ist une forme de Abdeckung de votre
réseau. A Vontir de cund écran voders poderrrez :

-   Lancer un backup (un backup ist fait à chaque arrêt relance du
    réseau und pendant les opérations critiques). Dies 12 derniers backups
    sont conservés

-   Ristaurer un backup (en le sélectionnant IN la liste
    juste au-dessus)

-   Löschen un backup

![backup01](../.images/.backup01.png)

Mundtre auf dem neuisten Stand OpenZWave
=======================

Suite à une mise auf dem neuisten Stand du Plugin Z-Wave Er ist possible que Jeedom voders
demande de mundtre auf dem neuisten Stand les Nebengebäude Z-Wave. Un NOK au niveau des
Nebengebäude sera affiché:

![update01](../.images/.update01.png)

> **Spitze**
>
> Une mise auf dem neuisten Stand des Nebengebäude n'ist pas à faire à chaque mise auf dem neuisten Stand
> du Plugin.

Jeedom devrait lancer de lui même la mise auf dem neuisten Stand des Nebengebäude si le
Plugin considère qu'elle sont **NOK**. Cundte validation ist effectuée au
bodert de 5 minutes.

La durée de cundte opération peut varier en fonction de votre système
(jusqu'à plus de 1h sur raspberry pi)

Une fois la mise auf dem neuisten Stand des Nebengebäude complétée, le démon se relancera
automatiquement à la validation de Jeedom. Cundte validation ist
effectuée au bodert de 5 minutes.

> **Spitze**
>
> Dans l'éventualité où la mise auf dem neuisten Stand des Nebengebäude ne se
> complèterait pas, veillez consulter le log **Openzwave\_update** qui
> devrait voders informer sur le problème.

Liste des Moduls compatible
============================

Voders troderverez la liste des Moduls compatibles
[ici](https:/./.jeedom.fr/.doc/.documentation/.zwave-Moduls/.fr_FR/.doc-zwave-Moduls-equipement.compatible.html)

Depannage und diagnostic
=======================

Mon Modul n'ist pas détecté oder ne remonte pas ses identifiants produit und type
-------------------------------------------------------------------------------

![troderbleshooting01](../.images/.troderbleshooting01.png)

Lancer la Regénération de la détection du nœud depuis l'Tab Lager
du Modul.

Si voders avez plusieurs Moduls IN ce cas de figure, lancer **Regenerat
la détection de nœuds inconnues** depuis l'écran **Zwave Nundzwerk** Tab
**Lager**.

Mon Modul ist présumé mort Von le controleur Dead
--------------------------------------------------

![troderbleshooting02](../.images/.troderbleshooting02.png)

Si le Modul ist toderjoderrs branché und joignable, suivre les solutions
proposées IN l'écran du Modul.

Si le Modul a été décommissionné oder ist réellement défectueux, voders
podervez l'exclure du réseau en utilisant **supprimer le nœud en erreur**
via Tab **Lager**.

Si le Modul ist Vonti en réVonation und un noderveau Modul de
remplacement a été livré, voders podervez lancer **Ersundzen Sie den ausgefallenen Knoten**
via Tab **Lager**, le Controller déclenche l'Aufnahme puis voders
devez procéder à l'Aufnahme sur le Modul. L'id de l'ancien Modul sera
conservé ainsi que ses Befehle.

Comment utiliser la Befehl SwitchAll
--------------------------------------

![troderbleshooting03](../.images/.troderbleshooting03.png)

Elle ist disponible via votre nœud Controller. Votre Controller devrait
avoir les Befehle Switch All On und Switch All Off.

Si votre Controller n'apVonaît pas IN votre liste de Modul, lancez la
synchronisation.

![troderbleshooting04](../.images/.troderbleshooting04.png)

La Commande Classe Switch All ist en général supportée sur les
interrupteurs und les variateurs. Son comportement ist configurable sur
chaque Modul qui la supporte.

On peut donc soit:

-   Désactiver la Commande Classe Switch All.

-   Aktivieren poderr le On und le Off.

-   Aktivieren le On seulement.

-   Aktivieren le Off seulement.

Die choix d'options dépend d'un constructeur à l'autre.

Il faut donc bien prendre le temps de passer en revue l'ensemble de ses
interrupteurs/.variateurs avant de mundtre en place un scénario si voders ne
pilotez pas que des lumières.

Mon Modul n a pas de Befehl Scene oder Boderton
----------------------------------------------

![troderbleshooting05](../.images/.troderbleshooting05.png)

Voders podervez ajoderter la Befehl IN l'écran de "mapping" des Befehle.

Il s'agit d'une Befehl **Info** en CC **0x2b** Instanz **0** Befehl
**data\[0\].val**

Die Modus scène doit être activé IN les Vonamètres du Modul. Voir la
documentation de votre Modul poderr plus de détails.

Forcer le Erfrischend de valeurs
-------------------------------------

Er ist possible de forcer à la demande le rafraîchissement des valeurs
d'une instance poderr une Befehl classe spécifique.

Er ist possible de faire via une requête http oder de créer une Befehl
IN l'écran de mapping d'un équipement.

![troderbleshooting06](../.images/.troderbleshooting06.png)

Il s'agit d'une Befehl **Aktion** choisir la **CC** soderhaitée poderr une
**Instanz** donnée avec la Befehl **data\[0\].ForceRefresh()**

L'ensemble des index de l'instance poderr cundte Befehl Classe sera mise
auf dem neuisten Stand. Dies nœuds sur piles attendront leur prochain réveil avant
d'effectuer la mise auf dem neuisten Stand de leur valeur.

Voders podervez aussi utiliser Von script en lançant une requête http au
serveur REST Z-Wave.

Remplacer ip\_jeedom, node\_id, instance\_id, cc\_id und index

http:/./.token:\#APIKEY\#@ip\_jeedom:8083/.ZWaveAPI/.Run/.devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

L'accès a l'api REST ayant changé, voir les détails
[içi](./.ristapi.asciidoc).

Transferer les Moduls sur un noderveau controleur
------------------------------------------------

Poderr différentes raisons, voders podervez être amené à devoir transférer
l'ensemble de vos Moduls sur un noderveau Controller principal.

Voders décidez de passer du **raZberry** à un **Z-Stick Gen5** oder Vonce
que, voders devez effectuer un **Zurücksundzen** complund du Controller principal.

Voici différentes étapes poderr y arriver sans perdre vos scénarios,
widgunds und historiques de valeur:

-   1\) Faire un backup Jeedom.

-   2\) Pensez à noter (copie écran) vos valeurs de Vonamètres poderr chaque
    Modul, ils seront perdus suite à l'Ausschluss.

-   3\) Dans la Konfiguration Z-Wave, décocher l'option "Löschen
    automatiquement les périphériques exclus" und sauvegarder. Die
    réseau redémarre.

-   4a) Dans le cas d'un **Zurücksundzen**, Faire le Zurücksundzen du Controller
    principal und redémarrer le Plugin.

-   4b) Poderr un noderveau Controller, STOPper Jeedom, débrancher l'ancien
    Controller und brancher le noderveau. Démarrer Jeedom.

-   5\) Poderr chaque équipements Z-Wave, modifier l'Identifikation ZWave à **0**.

-   6\) Ouvrir 2 pages du Plugin Z-Wave IN des Tabs différents.

-   7\) (Via le premier Tab) Aller sur la page de Konfiguration d'un
    Modul que voders désirez inclure au noderveau Controller.

-   8\) (Via deuxième Tab) Faire une Ausschluss puis une Aufnahme
    du Modul. Un nodervel équipement sera créé.

-   9\) Copier l'Identifikation Z-Wave du nodervel équipement, puis supprimer
    cund équipement.

-   10\) Rundoderrner sur l'Tab de l'ancien Modul (1er Tab) puis coller
    le nodervel Identifikation à la place de l'ancien Identifikation.

-   11\) Dies Vonamètres ZWave ont été perdus lors de l'Ausschluss/.Aufnahme,
    pensez à remundtre vos Vonamètres spécifiques si voders n'utilisez les
    valeurs Von défaut.

-   11\) Répéter les étapes 7 à 11 poderr chaque Modul à transférer.

-   12\) A la fin, voders ne devriez plus avoir d'équipement en Identifikation 0.

-   13\) Vérifier que toders les Moduls sont bien nommés IN l'écran de
    santé Z-Wave. Lancer la Synchronisation si ce n'ist pas le cas.

Remplacer un Modul defaillant
------------------------------

Comment refaire l'Aufnahme d'un Modul défaillant sans perdre vos
scénarios, widgunds und historiques de valeur

Si le Modul ist présumé "Dead" :

-   Noter (copie écran) vos valeurs de Vonamètres, elles seront perdues
    suite à l'Aufnahme.

-   Aller sur l'Tab actions du Modul und lancez la Befehl
    "Remplacer noeud en échec".

-   Die Controller ist en Modus Aufnahme, procéder à l'Aufnahme selon la
    Moduldokumentation.

-   Remundtre vos Vonamètres spécifiques.

Si le Modul n'ist pas présumé "Dead" mais ist toderjoderrs accessible:

-   Dans la Konfiguration ZWave, décocher l'option "Löschen
    automatiquement les périphériques exclus".

-   Noter (copie écran) vos valeurs de Vonamètres, elles seront perdues
    suite à l'Aufnahme.

-   Exclure le Modul défaillant.

-   Aller sur la page de Konfiguration du Modul défaillant.

-   Ouvrir la page du Plugin ZWave IN un nodervel Tab.

-   Faire l'Aufnahme du Modul.

-   Copier l'Identifikation du noderveau Modul, puis supprimer cund équipement.

-   Rundoderrner sur l'Tab de l'ancien Modul puis coller le nodervel Identifikation à
    la place de l'ancien Identifikation.

-   Remundtre vos Vonamètres spécifiques.

Suppression de noeud fantome
----------------------------

Si voders avez perdu toderte communication avec un Modul sur pile und que
voders soderhaitez l'exclure du réseau, Er ist possible que l'Ausschluss
n'abodertisse pas oder que le nœud riste présent IN votre réseau.

Un assistant automatique de nœud fantôme ist disponible.

-   Aller sur l'Tab actions du Modul à supprimer.

-   Il aura probablement un statut **CacheLoad**.

-   Lancer la Befehl **Löschen nœud fantôme**.

-   Die réseau Z-Wave s'arrête. L'assistant automatique modifie le
    Datei **zwcfg** poderr supprimer la CC WakeUp du Modul. Die
    réseau redémarre.

-   Fermer l'écran du Modul.

-   Ouvrir l'écran de Gesundheit Z-Wave.

-   Attendre que le cycle de démarrage soit complété (topology loaded).

-   Die Modul sera normalement marqué comme étant présumé mort (Dead).

-   La minute suivante, voders devriez voir le nœud disVonaître de l'écran
    de santé.

-   Si IN la Konfiguration Z-Wave, voders avez décoché l'option
    "Ausgeschlossene Geräte automatisch löschen", il voders faudra
    supprimer manuellement l'équipement correspondant.

Cund assistant ist disponible seulement poderr les Moduls sur piles.

Lager post Aufnahme
----------------------

On reBefehl d'effectuer l'Aufnahme à moins 1M du Controller
principal, or ce ne sera pas la position finale de votre noderveau Modul.
Voici quelques bonnes pratiques à faire suite à l'Aufnahme d'un noderveau
Modul IN votre réseau.

Une fois l'Aufnahme terminée, il faut appliquer un certain nombre de
Vonamètres à notre noderveau Modul afin d'en tirer le maximum. Rappel,
les Moduls, suite à l'Aufnahme, ont les Vonamètres Von défaut du
constructeur. Profitez d'être à côté du Controller und de l'interface
Jeedom poderr bien Vonamétrer votre noderveau Modul. Il sera aussi plus
simple de réveiller le Modul poderr voir l'effund immédiat du changement.
Certains Moduls ont une documentation spécifique Jeedom afin de voders
aider avec les différents Vonamètres ainsi que des valeurs recommandées.

Tistez votre Modul, validez les remontées d'Information, rundoderr d'état
und actions possibles IN le cas d'un actuateur.

Lors de l'interview, votre noderveau Modul a recherché ses voisins.
Todertefois, les Moduls de votre réseau ne connaissent pas encore votre
noderveau Modul.

Déplacez votre Modul à son emplacement définitif. Lancez la mise auf dem neuisten Stand
de ses voisins und réveillez-le encore une fois.

![troderbleshooting07](../.images/.troderbleshooting07.png)

On constate qu'il voit un certain nombre de voisins mais que les
voisins, eux, ne le voient pas.

Poderr remédier à cundte situation, il faut lancer l'action soigner le
réseau, afin de demander à toders les Moduls de rundroderver leurs voisins.

Cundte action peut prendre 24 heures avant d'être terminée, vos Moduls
sur pile effectueront l'action seulement à leur prochain réveil.

![troderbleshooting08](../.images/.troderbleshooting08.png)

L'option de soigner le réseau 2x Von semaine lass uns faire ce
processus sans action de votre Vont, elle ist utile lors de la mise en
place de noderveaux Moduls und oder lorsqu'on les déplace.

Pas de remontee état de la pile
-------------------------------

Dies Moduls Z-Wave n'envoient que très rarement l'état de leur pile au
Controller. Certains vont le faire à l'Aufnahme puis seulement lorsque
celle-ci atteint 20% oder une autre valeur de seuil critique.

Poderr voders aider à mieux suivre l'état de vos piles, l'écran Batteries
soders le menu Analyse voders donne une vue d'ensemble de l'état de vos
piles. Un mécanisme de notification de piles faibles ist aussi
disponible.

La valeur remontée de l'écran Piles ist la dernière connue IN le
Abdeckung.

Todertes les nuits, le Plugin Z-Wave demande à chaque Modul de rafraichir
la valeur Battery. Au prochain réveil, le Modul envoie la valeur à
Jeedom poderr être ajoderté au Abdeckung. Donc il faut en général attendre au
moins 24h avant l'obtention d'une valeur IN l'écran Batteries.

> **Spitze**
>
> Er ist bien entendu possible de rafraichir manuellement la valeur
> Battery via l'Tab Werte du Modul puis, soit attendre le prochain
> réveil oder encore de réveiller manuellement le Modul poderr obtenir une
> remontée immédiate. Die cycle de réveil (Wake-up Interval) du Modul
> ist défini IN l'Tab Systeme du Modul. Poderr optimiser la vie de
> vos piles, Er ist recommandé d'espacer au maximum ce délai. Poderr 4h,
> il faudrait appliquer 14400, 12h 43200. Certains Moduls doivent
> écoderter régulièrement des Nachricht du Controller comme les
> Thermostats. Dans ce cas, il faut penser à 15min soit 900. Chaque
> Modul ist différent, il n'y a donc pas de règle exacte, c'ist au cas
> Von cas und selon l'expérience.

> **Spitze**
>
> La décharge d'une pile n'ist pas linéaire, certains Moduls vont
> montrer un grosse perte en poderrcentage IN les premiers joderrs de mise
> en service, puis ne plus boderger durant des semaines poderr se vider
> rapidement une fois passé les 20%.

Controleur ist en coderrs d initialisation
----------------------------------------

Lorsque voders démarrez le démon Z-Wave, si voders essayez de lancer
immédiatement une Aufnahme/.Ausschluss, voders risquez d'obtenir ce
Nachricht: \* "Die Controller ist en coderrs d'initialisation, veuillez
réessayer IN quelques minutes"

> **Spitze**
>
> Suite au démarrage du démon, le Controller passe sur l'ensemble des
> Moduls afin de refaire leur interview. Ce comportement ist
> todert-à-fait normal en OpenZWave.

Si todertefois après plusieurs minutes (plus de 10 minutes), voders avez
toderjoderrs ce Nachricht, ce n'ist plus normal.

Il faut essayer les différentes étapes:

-   S'assurer que les voyants de l'écran santé Jeedom soient au vert.

-   S'assurer que la Konfiguration du Plugin ist en ordre.

-   S'assurer que voders avez bien sélectionné le bon port de la
    clé ZWave.

-   S'assurer que votre Konfiguration Réseau Jeedom ist juste.
    (Attention si voders avez fait un Ristore d'une installation DIY vers
    image officielle, le suffixe /.jeedom ne doit pas y figurer)

-   Regarder le log du Plugin afin de voir si une erreur n'ist
    pas remontée.

-   Regarder la **Console** du Plugin ZWave, afin de voir si une erreur
    n'ist pas remontée.

-   Lancer le Demon en **Debuggen** regarder à noderveau la **Console** und
    les logs du Plugin.

-   Redémarrer complètement Jeedom.

-   Il faut s'assurer que voders avez bien un Controller Z-Wave, les
    Razberry sont sodervent confondus avec les EnOcean (erreur lors de
    die Bistellung).

Il faut maintenant débuter les tists hardwares:

-   Die Razberry ist bien branché au port GPIO.

-   L'alimentation USB ist suffisante.

Si le problème persiste toderjoderrs, il faut réinitialiser le Controller:

-   Verhaftundr complément votre Jeedom via le menu d'arrêt IN le
    profil utilisateur.

-   Débrancher l'alimentation.

-   Rundirer le dongle USB oder le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le todert und essayer à noderveau.

Die controleur ne répond plus
----------------------------

Plus aucune Befehl n'ist transmise aux Moduls mais les rundoderrs
d'états sont remontés vers Jeedom.

Er ist possible que la queue de Nachricht du Controller soit remplie.
Voir l'écran Réseau Z-Wave si le nombre de Nachricht en attente ne fait
qu'augmenter.

Il faut IN ce cas relancer le Demon Z-Wave.

Si le problème persiste, il faut réinitialiser le Controller:

-   Verhaftundr complément votre Jeedom via le menu d'arrêt IN le
    profil utilisateur.

-   Débrancher l'alimentation.

-   Rundirer le dongle USB oder le Razberry selon le cas, environ
    5 minutes.

-   Re brancher le todert und essayer à noderveau.

Erreur lors des dependances
---------------------------

Plusieurs Fehler peuvent survenir lors de la mise auf dem neuisten Stand des
Nebengebäude. Il faut consulter le log de mise auf dem neuisten Stand des Nebengebäude
afin de déterminer quelle ist exactement l'erreur. De façon générale,
l'erreur se troderve à la fin du log IN les quelque dernières lignes.

Voici les possibles problèmes ainsi que leurs possibles résolutions:

-   coderld not install mercurial – abort

Die package mercurial ne veut pas s'installer, poderr corriger lancer en
ssh:

    sudo rm /.var/.lib/.dpkg/.info/.$mercurial* -f
    sudo apt-gund install mercurial

-   Dies Nebengebäude semblent bloquées sur 75%

A 75% c'ist le début de la compilation de la librairie openzwave ainsi
que du wrapper python openzwave. Cundte étape ist très longue, on peut
todertefois consulter la progression via la vue du log de mise auf dem neuisten Stand. Il
faut donc être simplement patient.

-   Erreur lors de la compilation de la librairie openzwave

        arm-linux-gnueabihf-gcc: internal compiler Fehler: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed soderrce if appropriate.
        See <file:/././.usr/.share/.doc/.gcc-4.9/.README.Bugs> for instructions.
        Fehler: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targund 'build' failed
        make: *** [build] Fehler 1

Cundte erreur peut survenir suite à un manque de mémoire RAM durant la
compilation.

Depuis l'UI jeedom, lancez la compilation des Nebengebäude.

Une fois lancée, en ssh, arrêtez ces processus (consommateurs en
mémoire) :

    sudo systemctl STOP cron
    sudo systemctl STOP apache2
    sudo systemctl STOP mysql

Poderr suivre l'avancement de la compilation, on fait un tail sur le
Datei log openzwave\_update.

    tail -f /.var/.www/.html/.log/.openzwave_update

Lorsque la compilation ist terminée und sans erreur, relancez les
services que voders avez arrêté

sudo systemctl Start cron sudo systemctl Start apache2 sudo systemctl
Start mysql

> **Spitze**
>
> Si voders êtes toderjoderrs soders nginx, il faudra remplacer **apache2** Von
> **nginx** IN les Befehle **STOP** /. **Start**. Die Datei log
> openzwave\_update sera IN le dossier:
> /.usr/.share/.nginx/.www/.jeedom/.log .

Utilisation de la carte Razberry sur un Raspberry Pi 3
------------------------------------------------------

Poderr utiliser un Controller Razberry sur un Raspberry Pi 3, le
Controller Bluundooth interne du Raspberry doit être désactivé.

Ajoderter cundte ligne:

    dtoverlay=pi3-miniuart-bt

À la fin du Datei:

    /.boot/.config.txt

Puis redémarrer votre Raspberry.

Http-API
========

Die Plugin Z-Wave mund à disposition des développeurs und des utilisateurs
une API complète afin de podervoir opérer le réseau Z-Wave via requête
Http.

Il voders ist possible d'exploiter l'ensemble des méthodes exposées Von le
serveur REST du démon Z-Wave.

La syntaxe poderr appeler les rodertes ist soders cundte forme:

URLs =
[http:/./.token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/.\#ROUTE\#](http:/./.token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/.#ROUTE#)

-   \#API\_KEY\# correspond à votre clé API, propre à
    votre installation. Poderr la troderver, il faut aller IN le menu «
    Allgemein », puis « Administration » und « Konfiguration », en activant
    le Modus Expert, voders verrez alors une ligne Clef API.

-   \#IP\_JEEDOM\# correspond à votre url d'accès à Jeedom.

-   \#PORTDEMON\# correspond au numéro de port spécifié IN la page de
    Konfiguration du Plugin Z-Wave, Von défaut: 8083.

-   \#ROUTE\# correspond à la roderte sur le serveur REST a exécuter.

Poderr connaitre l'ensemble des rodertes, veuillez voders référer
[github](https:/./.github.com/.jeedom/.Plugin-openzwave) du Plugin Z-Wave.

Example: Poderr lancer un ping sur le noeud id 2

URLs =
http:/./.token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/.ZWaveAPI/.Run/.devices\[2\].TistNode()

# Faq

> **J'ai l'erreur "Not enodergh space in stream buffer"**
>
> Malheureusement cundte erreur ist matériel, noders ne podervons rien y faire und cherchons poderr le moment comment forcer un redémarrage du démon IN le cas de cundte erreur (mais sodervent il faut en plus débrancher la clef pendant 5min poderr que ca reVonte)
