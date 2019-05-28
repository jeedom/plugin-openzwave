04-02-2019
===
- CETTE MAJ NECESSITE DE RECOMPILER LES DEPENDANCES (RELANCER)
- Correction d'un bug sur les multiinstances des thermostats
- Création d'un niveau de queue dépriorisé sur les actions pour les refreshs
- Rajout de nombreuses confs (pour rappel le bouton récupérer les confs est utile pour être à jour sans mettre à jour le plugin)
- Amélioration de la gestion des multichannels encapsulés
- Rajout de la CC manufacturer specific
- Mise en place simple de la CC Soundswitch
- Correction de l'inclusion Multiples des devices&lt
- Amélioration de la CC Switch Binary
- La saisie de paramétre manuel est toujours possible
- Amélioration de la queue
- Préparation pour rajout nouvelles CCs (notification notamment)
- Rajout des codes sur la CC alarme pour clavier Zipato pour le moment
- Correction de la philio en mode sécurisée qui lors des sonneries générait un timeout de 10 secondes (il faut surement regénerer la détection de la sirène ou la ré-inclure)
- Correction d'un bug si le niveau de log est sur aucun
- CETTE MAJ NECESSITE DE RECOMPILER LES DEPENDANCES

17-03-2018
===

- Changement de la branche pour la récupération des confs lors du syncconf (suite a changement de l'organisation des githubs)

17-01-2018 / 19-01-2018
===

-   Nouveautés

    -   Retour de la possibilité de synchroniser les confs sans mettre à jour le plugin

    -   Améliorations

    -   Rajout de la possibilité en interne de declencher des refreshs sur certaines valeurs spécifiques et modules spécifiques (utilisé dans les confs jeedom)

    -   Refonte complète de la fonction permettant de simuler une valeur sur une autre commande pour éviter de la mettre pour un ensemble de module mais spécifiquement (interne Jeedom)

-   Bug fixes

    -   Correction d’un bug qui faisait que les confs auto générés étaient à l’ancien format et donc inutilisable

    -   Correction du bug de la perte du consigne pending sur les vannes thermostatiques (va avec le point 2 des améliorations)

    -   Réduction de la taille des images pour limiter au plus la taille du plugin (environ 500 images)

    -   Suppression de dépendances plus utilisées tel que Mercurial Sphinx etc…​

    -   Suppression de la purge des configurations avant update (évite d’avoir des icones Zwave en lieu et place des images en cas de mises a jours non aboutis pour timeout ou autre)

2017-08-xx
===


-   Neue Eigenschaften

    -   Possibilité de rafraichir les commandes d’un équipement sans
        supprimer les existantes.

    -   Possibilité de créer une commande information sur les valeurs de
        l’onglet Système.

-   Improvements/Enhancements

    -   Prise en charge de nouveaux modules, définitions ozw
        et commandes.

    -   Possibilité de sélectionner l’association par défaut
        (sans instance) sur les modules supportant les
        associations multi-instances.

    -   Vérification de la validité des groupes d’associations à la fin
        de l’interview.

    -   Récupération du dernier niveau des piles au démarrage du démon.

-   Fehlerbehebungen

    -   Correction de la migration de l’info Batterie.

    -   Correction de la remontée de l’info Batterie dans
        l’écran Equipements.

    -   Restauration du type de piles dans les configurations
        de modules.

    -   Correction des actions sur les valeurs de type bouton dans
        l’écran du module.

    -   Correction de la récupération des traductions de paramètres.

    -   Correction erreur vide sur modification de valeurs de type RAW
        (code RFid).

    -   Correction de l’affichage des valeurs en attente
        d’être appliqué.

    -   Suppression de la notification du changement de valeur avant
        qu’elle ne soit appliquée.

    -   Ne plus afficher le cadenas dans l’écran du module si le module
        ne supporte pas la Classe de Commande Sécurité.

    -   Application du rafraichissement manuel dans les
        paramètres recommandés.

    -   Assistant de gestion des badges pour les lecteurs RFID.

    -   Correction de l’assistant de détection de modules inconnus.

    -   Correction des assistants de "Reprendre de.." et "Appliquer
        sur…​" dans l’onglet paramètres.

2017-06-20
===

-   Neue Eigenschaften

    -   keine Änderung

-   Improvements/Enhancements

    -   Ajout l’ensemble des configurations de modules au
        nouveau format.

-   Fehlerbehebungen

    -   Ne pas tester si un nodeId existe lors de la suppression
        d’un association.

    -   Restauration de la notification de consigne en attente sur
        les thermostats.

    -   Envoi de la Scène Activation en instance 1.

    -   Ne plus afficher le cadenas dans l’écran de santé sur les
        modules ne supportant pas la Classe de Commande Securité.

    -   Répétition de valeur sur les télécommandes avant la fin de
        l’interview (kyefob, minimote).

    -   Modifier un paramètre de type liste par valeur via une
        commande Action.

    -   Modifier un paramètre sur un module sans configuration définie.

2017-06-13
===

-   Neue Eigenschaften

    -   N/A

-   Improvements/Enhancements

    -   Ajout de configuration de module Fibaro US

-   Fehlerbehebungen

    -   keine Änderung

2017-05-31
===

-   Neue Eigenschaften

    -   keine Änderung

-   Improvements/Enhancements

    -   keine Änderung

-   Fehlerbehebungen

    -   Correction de l’assignation des valeurs au format RAW des codes
        pour lecteur RFid.

2017-05-23
===

-   Neue Eigenschaften

    -   Suppression du mode maître / esclave. Remplacé par le plugin
        jeedom link.

    -   Utilisation d’une clé API privée au plugin ZWave.

    -   Nouveau format des fichiers de configuration dans le mapping de
        commande avec jeedom.

    -   Conversion automatique des commandes existantes au nouveau
        format lors de l’installation du plugin.

    -   Ajout du support de la Classe de Commande Central Scene.

    -   Ajout du support de la Classe de Commande Barrier Operator.

-   Improvements/Enhancements

    -   Refonte complète du serveur REST utilisation de TORNADO.

        -   Modification de l’ensemble des routes existantes, les
            scripts devront être adaptés si utilisation de l’API ZWave.

        -   Renforcement de la sécurité, seul des appels sont écouté sur
            le serveur REST.

        -   Utilisation de la clé API ZWave requise pour lancer des
            requêtes REST.

    -   Désactivation (temporaire) des tests sanitaires.

    -   Désactivation (temporaire) du moteur de mise à jour des
        configurations de modules.

    -   Désactivation de la fonction Soigner le réseau automatiquement
        deux fois par semaine (diminution des échanges avec
        le contrôleur).

    -   Optimisations du code de la bibliothèque openzwave.

        -   Fibaro FGK101 n’a plus à compléter l’interview pour annoncer
            un changement d’état.

        -   La commande bouton relâcher (Stop d’un volet) ne force plus
            la mise à jour de l’ensemble des valeurs du module
            (diminution de la file de messages).

        -   Possibilité de notifier des valeurs dans la Classe de
            Commande Alarm (sélection de la sonnerie sur les sirènes)

    -   Plus de demande journalière du niveau des piles (moins de
        messages, économie sur les piles).

    -   Le niveau des piles est directement envoyé à l’écran de pile sur
        réception de rapport du niveau.

-   Fehlerbehebungen

    -   Rafraîchissement de l’ensemble des instances suite à un
        broadcast de la CC Switch ALL.

2016-08-26
===

-   Neue Eigenschaften

    -   Aucune

-   Improvements/Enhancements

    -   Détection du RPI3 dans la mise à jour des dépendances.

    -   Activer le mode d’inclusion en non-sécurisé par défaut.

-   Fehlerbehebungen

    -   Test des informations constructeur dans l’écran de santé ne
        remonte plus des NOK.

    -   Perte des cases-à-cocher dans l’onglet Commandes de la
        page équipement.

2016-08-17
===

-   Neue Eigenschaften

    -   Relance du demon si détection du contrôleur en timeout lors de
        l’initialisation du contrôleur.

-   Improvements/Enhancements

    -   Mise à jour de la librairie OpenZWave 1.4.2088.

    -   Correction de l’orthographe.

    -   Refonte de l’écran équipements avec onglets.

-   Fehlerbehebungen

    -   Problème d’affichage de certains modules sur la table de routage
        et Graph réseau.

    -   Modules Vision Secure qui ne retournent pas en veille
        durant l’interview.

    -   Installation des dépendances en boucle (problème coté github).

2016-07-11
===

-   Neue Eigenschaften

    -   Prise en charge de la restauration du dernier niveau connue sur
        les dimmer.

    -   Distinction des modules FLiRS dans l’écran de santé.

    -   Ajout de la demande de mise à jour des routes de retour
        au contrôleur.

    -   Assistant pour appliquer les paramètres de configuration d’un
        module à plusieurs autres modules.

    -   Identification du Zwave+ des modules supportant
        la COMMAND\_CLASS\_ZWAVE\_PLUS\_INFO.

    -   Affichage de l’état de sécurité des modules supportant
        la COMMAND\_CLASS\_SECURITY.

    -   Ajout de la possibilité de sélectionner l’instance 0 du
        contrôleur pour les associations multi-instances.

    -   Sécurisation de l’ensemble des appels au serveur REST.

    -   Détection automatique du dongle, dans la page de configuration
        du plugin.

    -   Dialogue d’inclusion avec le choix du mode d’inclusion pour
        simplifier l’inclusion sécurisée.

    -   Prise en compte des équipements désactivés au sein du
        moteur Z-Wave.

        -   Affichage grisé dans l’écran de santé sans analyse sur
            le nœud.

        -   Masquée dans la Table réseau et Graphique réseau.

        -   Nœuds désactivés, excluent des tests sanitaires.

-   Improvements/Enhancements

    -   Optimisation des contrôles sanitaires.

    -   Optimisation du graphique réseau.

    -   Amélioration de la détection du contrôleur principal pour le
        test des groupes.

    -   Mise à jour de la librairie OpenZWave 1.4.296.

    -   Optimisation du rafraichissement en arrière-plan des variateurs.

    -   Optimisation du rafraichissement en arrière-plan pour
        les moteurs.

    -   Adaptation pour la version Jeedom core 2.3

    -   Ecran de santé, modification de nom de colonne et avertissement
        en cas de non communication avec un module.

    -   Optimisation du serveur REST.

    -   Correction de l’orthographe des écrans, merci @Juan-Pedro
        aka: kiko.

    -   Mise à jour de la documentation du plugin.

-   Fehlerbehebungen

    -   Correction de possible problèmes lors de la mise à jour des
        configurations de modules.

    -   Graphique réseau, calcul des sauts sur l’id du contrôleur
        principal et non assumer l’ID 1.

    -   Gestion du bouton ajouter une association groupe.

    -   Affichage des valeurs False dans l’onglet Configuration.

    -   Ne plus assumer la date du jour sur l’état des piles si pas reçu
        de rapport de l’équipement.

2016-05-30
===

-   Neue Eigenschaften

    -   Ajout d’une option pour activer/désactiver les contrôles
        sanitaires sur l’ensemble des modules.

    -   Ajout d’un onglet Notifications pour visualiser les dernières 25
        notifications du contrôleur.

    -   Ajout d’une route pour récupérer la santé d’un noeud.
        ip\_jeedom:8083/ZWaveAPI/Run/devices\[node\_id\].GetHealth()

    -   Ajout d’une route pour récupérer la dernière notification
        d’un noeud.
        ip\_jeedom:8083/ZWaveAPI/Run/devices\[node\_id\].GetLastNotification()

-   Improvements/Enhancements

    -   Permettre la sélection des modules FLiRS lors des
        associations directes.

    -   Permettre la sélection de toutes les instances des modules lors
        des associations directes.

    -   Mise à jour du wrapper python OpenZWave en version 0.3.0.

    -   Mise à jour de la librairie OpenZWave 1.4.248.

    -   Ne pas afficher d’avertissement de wakeup expiré pour les
        modules sur piles alimentées par secteur.

    -   Validation qu’un module est identique au niveau ids pour
        permettre la copie des paramètres.

    -   Simplification de l’assistant de copie des paramètres.

    -   Masquer des valeurs de l’onglet système qui n’ont pas lieu
        d’être affichées.

    -   Affichage de la description des capacités du contrôleur.

    -   Mise à jour de la documentation.

    -   Correction de l’orthographe de la documentation, merci
        @Juan-Pedro aka: kiko.

-   Fehlerbehebungen

    -   Correction orthographe.

    -   Correction de l’inclusion en mode sécurisé.

    -   Correction de l’appel asynchrone. (error: \[Errno 32\]
        Broken pipe)

2016-05-04
===

-   Neue Eigenschaften

    -   Ajout d’option pour désactiver l’actualisation en arrière-plan
        des variateurs.

    -   Affichage des associations avec qui un module est en association
        (find usage).

    -   Ajout du support de la CC MULTI\_INSTANCE\_ASSOCIATION.

    -   Ajout d’une notification info lors de l’application de
        Set\_Point afin de pourvoir exploiter la consigne demandée sous
        forme de cmd info.

    -   Ajout d’un assistant de configuration recommandée.

    -   Ajout d’option pour activer/désactiver l’assistant de
        configuration recommandée lors de l’inclusion de
        nouveaux modules.

    -   Ajout d’option pour activer/désactiver la mise à jour des
        configurations des modules chaque nuit.

    -   Ajout d’une route pour gérer les multi instances associations.

    -   Ajout des Query Stage manquants.

    -   Ajout de la validation de la sélection du Dongle USB au
        démarrage du démon.

    -   Ajout de la validation et test du callback au démarrage
        du démon.

    -   Ajout d’une option pour désactiver la mise à jour automatique
        des config de module.

    -   Ajout d’une route pour modifier à l’exécution les traces de log
        du serveur REST. Note: aucun effect sur le niveau OpenZWave.
        <http://ip_jeedom:8083/ZWaveAPI/Run/ChangeLogLevel(level>) level
        ⇒ 40:Error, 20: Debug 10 Info

-   Improvements/Enhancements

    -   Mise à jour du wrapper python OpenZWave en version 0.3.0b9.

    -   Mise en évidence des groupes d’associations qui sont en attente
        d’être appliqués.

    -   Mise à jour de la librairie OpenZWave 1.4.167.

    -   Modification du système d’association directe.

    -   Mise à jour de la documentation

    -   Possibilité de lancer la régénération de la détection du nœud
        pour l’ensemble des modules identiques (marque et modèle).

    -   Affichage dans l’écran de santé si des éléments de configuration
        ne sont pas appliqués.

    -   Affichage dans l’écran d’équipement si des éléments de
        configuration ne sont pas appliqués.

    -   Affichage dans l’écran de santé si un module sur piles ne s’est
        jamais réveillé.

    -   Affichage dans l’écran de santé si un module sur piles a dépassé
        le temps du réveil prévu.

    -   Ajout de traces lors d’erreur de notifications.

    -   Meilleure remontée de l’état des piles.

    -   Conformité du résumé / santé pour les thermostats sur piles.

    -   Meilleur détection de modules sur piles.

    -   Optimisation du mode Debug pour le serveur REST.

    -   Forcer une actualisation de l’état des interrupteurs et dimer
        suite à l’envoi d’une commande switch all.

-   Fehlerbehebungen

    -   Correction de la découverte des groupes d’associations.

    -   Correction de l’erreur "Exception KeyError: (91,) in
        'libopenzwave.notif\_callback' ignored".

    -   Correction de la sélection de la documentation de module pour
        les modules avec plusieurs profils.

    -   Gestion des boutons action du module.

    -   Correction de description de nom générique de class.

    -   Correction de la sauvegarde du fichier zwcfg.

2016-03-01
===

-   Neue Eigenschaften

    -   Ajout du bouton Configuration via l’écran de gestion
        des équipements.

    -   Ajout des nouveaux états de l’interview de module.

    -   Modification de libellés dans les UI.

-   Improvements/Enhancements

    -   Meilleur gestion des boutons Actions de modules.

    -   Documentation Ajout de sections.

    -   Optimisation du mécanisme de détection d’état du démon.

    -   Mécanisme de protestation lors de la récupération de la
        description des paramètres s’il contient des caractères
        non valides.

    -   Ne plus remonter les informations de l’état de la pile sur un
        module branché sur secteur.

    -   Mise à jour de la documentation.

-   Fehlerbehebungen

    -   Documentation Corrections orthographiques et grammaticales.

    -   Validation du contenu du fichier zwcfg avant de l’appliquer.

    -   Correction de l’installation.

2016-02-12
===

-   Improvements/Enhancements

    -   Pas d’alerte de nœud mort si celui-ci est désactivé.

-   Fehlerbehebungen

    -   Correction fil pilote Fibaro retour d’état.

    -   Correction d’un bug qui recréer les commandes lors de la mise
        à jour.

2016.02.09
===

-   Neue Eigenschaften

    -   Ajout du push notification en case de node\_event, permet la
        mise en place d’une cmd info en CC 0x20 pour récupérer des
        événement sur les nodes.

    -   Ajout de la route ForceRefresh
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ForceRefresh()
        pouvant être utilisée dans les commandes.

    -   Ajout du route SwitchAll
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[1\].commandClasses\[0xF0\].SwitchAll(&lt;int:state&gt;)
        disponible via le contrôleur principal.

    -   Ajout de la route ToggleSwitch
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ToggleSwitch()
        pouvant être utilisée dans les commandes.

    -   Ajout d’une push notification en cas de noeud présumé mort.

    -   Ajout de la commande “refresh all parameters” dans
        l’onglet Paramètres.

    -   Ajout de l’information du paramètre en attente d’être appliqué.

    -   Ajout de notification réseau.

    -   Ajout d’une légende dans le graphe réseau.

    -   Ajout de la fonction soigner réseau via la table de routage.

    -   Suppression automatique de nœud fantôme en un seul click.

    -   Gestion des actions sur nœud selon l’état du noeud et le type.

    -   Gestion des actions réseau selon l’état du réseau.

    -   Mise à jour de la configuration de module automatique toutes
        les nuits.

-   Improvements/Enhancements

    -   Refactoring complet du code du serveur REST, optimisation de
        vitesse de démarrage, lisibilité, respect de convention
        de nommage.

    -   Mise à l’équerre des logs.

    -   Simplification de la gestion du refresh manuel 5min avec
        possibilité d’appliquer sur les nœuds sur piles.

    -   Mise à jour de la librairie OpenZWave en 1.4

    -   Modification du test sanitaire pour réanimer les nœuds présumés
        morts plus facilement sans actions utilisateurs.

    -   Utilisation de couleurs vives de la table de routage et du
        graphe réseau.

    -   Uniformisation des couleurs de la table de routage et du
        graphe réseau.

    -   Optimisation des informations de la page de santé Z-Wave selon
        l’état de l’interview.

    -   Meilleur gestion des paramètres en lecture seule ou en écriture
        seule dans l’onglet Paramètres.

    -   Amélioration des warning sur les thermostats sur piles.

-   Fehlerbehebungen

    -   Température convertie en Celsius retourne l’unité C à la place
        de F.

    -   Correction du rafraîchissement des valeurs au démarrage.

    -   Correction du Refresh par valeur dans l’onglet Valeurs.

    -   Correction des noms génériques des modules.

    -   Correction du ping sur les nœuds en Timeout lors du
        test sanitaire.


