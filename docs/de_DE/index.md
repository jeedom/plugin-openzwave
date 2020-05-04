Description
===========

Dieses Plugin ermöglicht die Nutzung von Z-Wave-Modulen durch
die OpenZwave-Bibliothek.

Introduction
============

Z-WAVE kommuniziert mit Low-Power-Funktechnologie
im 868,42 MHz Frequenzband. Es ist speziell entwickelt
für Hausautomationsanwendungen. Das Z-Wave-Funkprotokoll ist
optimiert für den Austausch mit geringer Bandbreite (zwischen 9 und 40)
kbit /. s) zwischen batteriebetriebenen oder netzbetriebenen Geräten.

Z-WAVE arbeitund je nach Frequenzbereich im Sub-Gigahertz-Bereich
Regionen (868 MHz in Europa, 908 MHz in den USA und andere Frequenzen
nach den ISM-Bändern der Regionen). Der theoretische Bereich beträgt ungefähr
30 Meter drinnen und 100 Meter draußen. Das Z-Wave-Netzwerk
nutzt Mesh-Technologie, um die Reichweite zu erhöhen und
Zuverlässigkeit. Z-WAVE lässt sich problemlos integrieren
verbrauchsarme elektronische Produkte, einschließlich
Batterien wie Fernbedienungen, Rauchmelder und
Sicherheit.

Der Z-WAVE + bringt bestimmte Verbesserungen, einschließlich einer besseren Reichweite und
verbessert unter anderem die Akkulaufzeit. Die
volle Abwärtskompatibilität mit dem Z-WAVE.

Mit anderen drahtlosen Signalquellen zu beachtende Entfernungen
-----------------------------------------------------------------

Funkempfänger müssen in einem Mindestabstand von
50 cm von anderen Radioquellen entfernt.

Beispiele für Radioquellen:

-   Ordinateurs

-   Mikrowellengeräte

-   Elektronische Transformatoren

-   Audio- und Videogeräte

-   Vorkopplungsvorrichtungen für Leuchtstofflampen

> **Tip**
>
> Wenn Sie einen USB-Controller (Z-Stick) haben, wird dies empfohlen
> Entfernen Sie es mit einem einfachen 1-M-USB-Verlängerungskabel von der Box
> Beispiel.

Die Entfernung zwischen anderen drahtlosen Sendern wie Telefonen
Drahtlose oder Radio-Audioübertragungen müssen mindestens 3 Meter lang sein. Die
Folgende Funkquellen sollten berücksichtigt werden :

-   Störung durch Schalter von Elektromotoren

-   Störungen durch defekte elektrische Geräte

-   Störungen durch HF-Schweißgeräte

-   medizinische Behandlungsgeräte

Effektive Wandstärke
---------------------------

Die Modulpositionen müssen so gewählt werden, dass
Die direkte Verbindungsleitung funktioniert nur bei sehr kurzen
Abstand durch das Material (eine Wand), um so viel wie möglich zu vermeiden
Milderungen.

![introduction01](../.images/.introduction01.png)

Metallteile von Gebäuvon oder der Möbel können blockieren
elektromagnetische Wellen.

Vernetzung und Routing
-------------------

Netz-Z-Wave-Knoten können Nachrichten senden und wiederholen
die sich nicht in unmittelbarer Nähe der Steuerung befinden. Dies ermöglicht eine mehr
große Flexibilität der Kommunikation, auch wenn keine Verbindung besteht
direkt drahtlos oder wenn eine Verbindung vorübergehend nicht verfügbar ist, zu
wegen einer Veränderung im Raum oder Gebäude.

![introduction02](../.images/.introduction02.png)

Der Controller **Id 1** kann direkt mit den Knoten 2, 3 kommunizieren
und 4. Knoten 6 befindund sich jedoch außerhalb seiner Funkreichweite
im Funkbereich von Knoten 2 gefunden. Daher ist die
Die Steuerung kann über Knoten 2 mit Knoten 6 kommunizieren. Davon
Auf diese Weise wird der Pfad von der Steuerung über Knoten 2 zu Knoten 6 aufgerufen
Straße. In dem Fall, in dem die direkte Kommunikation zwischen Knoten 1 und dem
Knoten 2 ist blockiert, es gibt noch eine weitere Option zur Kommunikation
Knoten 6, wobei Knoten 3 als ein weiterer Signalverstärker verwendund wird.

Es wird deutlich, dass je mehr Sektorknoten Sie haben, desto mehr
Die Routing-Optionen erhöhen sich und die Netzwerkstabilität erhöht sich.
Das Z-Wave-Protokoll kann Nachrichten über weiterleiten
durch maximal vier Wiederholungsknoten. Es ist ein
Kompromiss zwischen Netzwerkgröße, Stabilität und maximaler Dauer
einer Nachricht.

> **Tip**
>
> Es wird dringend empfohlen, zu Beginn der Installation ein Verhältnis festzulegen
> zwischen Sektorknoten und Knoten auf 2/.3 Batterien, um eine gute zu haben
> Netzwerknetz. Bevorzugen Sie MikroModul gegenüber intelligenten Steckern. Die
> MikroModul befinden sich an einem endgültigen Ort und werden es nicht sein
> getrennt haben sie im Allgemeinen auch eine bessere Reichweite. Ein guter
> Abfahrt ist die Beleuchtung der öffentlichen Bereiche. Es wird gut helfen
> Verteilen Sie die BranchenModul an strategischen Standorten in Ihrem
> nach Hause. Dann können Sie beliebig viele Modul zum Stapel hinzufügen
> wie gewünscht, wenn Ihre Grundrouten gut sind.

> **Tip**
>
> Die **Netzwerkdiagramm** sowie die **Routing-Tabelle**
> Mit dieser Option können Sie die Qualität Ihres Netzwerks anzeigen.

> **Tip**
>
> Es gibt Repeater-Module, um Bereiche zu füllen, in denen kein Modul vorhanden ist
> Sektor hat keine Verwendung.

Eigenschaften von Z-Wave-Geräten
-------------------------------

|  | Nachbarn | Straße | Mögliche Funktionen |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controller | Kennt alle Nachbarn | Hat Zugriff auf die vollständige Routing-Tabelle | Kann mit allen Geräten im Netzwerk kommunizieren, wenn ein Kanal vorhanden ist |
| Sklave | Kennt alle Nachbarn | Hat keine Informationen in der Routing-Tabelle | Kann nicht auf den Knoten antworten, von dem die Nachricht empfangen wurde. Daher können keine unerwünschten Nachrichten gesendund werden |
| Sklaven weiterleiten | Kennt alle seine Nachbarn | Mit teilweiser Kenntnis der Routing-Tabelle | Kann auf den Knoten antworten, von dem die Nachricht empfangen wurde, und kann unerwünschte Nachrichten an eine Reihe von Knoten senden |

Zusammenfassend::

-   Jevon Z-Wave-Gerät kann den Empfang empfangen und bestätigen
    messages

-   Controller können Nachrichten an alle Knoten in der senden
    réseau, sollicités oder non « Die maître peut parler quand il veut und à
    wen er will »

-   Slaves können keine unerwünschten Nachrichten senden,
    mais seulement une réponse aux demanvon «L'esclave ne parle que si
    wir fragen ihn »

-   Routing-Slaves können auf Anfragen reagieren und sind es auch
    darf unerwünschte Nachrichten an bestimmte Knoten senden, die
    le Controller a prédéfini « L'esclave ist toujours un esclave, mais
    Auf Genehmigung kann er sprechen »

Plugin Konfiguration
=======================

Nach dem Herunterladen von Plugins müssen Sie es nur noch aktivieren und
configurer.

![Konfiguration01](../.images/.configuration01.png)

Nach der Aktivierung sollte der Dämon starten. Das Plugin ist vorkonfiguriert
mit Standardwerten; Sie haben normalerweise nichts mehr zu tun.
Sie können jedoch die Konfiguration ändern.

Nebengebäude
-----------

In diesem Teil können Sie die erforderlichen Abhängigkeiten überprüfen und installieren
die ordnungsgemäße Funktion von Zwave-Plugins (sowohl lokal als auch
deportiert, hier vor Ort) ![Konfiguration02](../.images/.configuration02.png)

-   Ein Status **OK** bestätigt, dass Abhängigkeiten erfüllt sind.

-   Wenn der Status ist **NOK**, Abhängigkeiten müssen neu installiert werden
    mit der Taste ![Konfiguration03](../.images/.configuration03.png)

> **Tip**
>
> Das Aktualisieren von Abhängigkeiten kann je nach abhängig mehr als 20 Minuten dauern
> dein Material. Der Fortschritt wird in Echtzeit und in einem Protokoll angezeigt
> **Openzwave\_update** ist zugänglich.

> **Important**
>
> Das Aktualisieren von Abhängigkeiten erfolgt normalerweise nur
> wenn das Status ist **NOK**, es ist jedoch möglich, sich anzupassen
> bestimmte Probleme, die aufgerufen werden müssen, um die Installation von zu wiederholen
> Nebengebäude.

> **Tip**
>
> Wenn Sie sich im Remote-Modus befinden, können die Abhängigkeiten von lokalen Dämons
> NOK zu sein, ist völlig normal.

Dämon
-----

In diesem Teil können Sie den aktuellen Status der Dämonen und überprüfen
Konfigurieren Sie die automatische Verwaltung dieser.
![Konfiguration04](../.images/.configuration04.png) Die démon local et
Alle deportierten Dämonen werden mit ihren unterschiedlichen angezeigt
informations

-   Die **Statut** zeigt an, dass der Dämon gerade läuft.

-   Die **Configuration** Gibt an, ob die Konfiguration von Dämons
    ist gültig.

-   Die Schaltfläche **(Re) Anfang** ermöglicht das Erzwingen von Neustarts des
    Plugin, im normalen Modus oder beim ersten Start.

-   Die Schaltfläche **Verhaftet**, Nur sichtbar, wenn automatische Verwaltung
    ist deaktiviert, zwingt den Dämon anzuhalten.

-   Die **Automatische Verwaltung** ermöglicht Jeedom den automatischen Start
    der Dämon, wenn Jeedom startet, sowie um es für den Fall neu zu starten
    von Problems.

-   Die **Letzter Start** ist, wie der Name schon sagt, das Datum von
    letzter bekannter Start von Dämons.

Log
---

In diesem Teil können Sie die Protokollstufe auswählen und diese einsehen.
der Inhalt.

![Konfiguration05](../.images/.configuration05.png)

Wählen Sie die Ebene aus und speichern Sie sie. Der Dämon wird dann neu gestartet
mit ausgewählten Anweisungen und Spuren.

Das Level **Debug** oder **Info** kann beim Verständnis hilfreich sein
warum der Dämon einen Wert pflanzt oder nicht erhöht.

> **Important**
>
> Im Modus **Debug** Der Dämon ist sehr ausführlich, es wird empfohlen
> Verwenden Sie diesen Modus nur, wenn Sie ein Problem diagnostizieren müssen
> insbesondere. Es wird nicht empfohlen, den Dämon laufen zu lassen
> **Debug** dauerhaft, wenn wir eine verwenden **SD-Card**. Sobald die
> Vergessen Sie nicht, auf eine niedrigere Ebene zurückzukehren
> hoch wie das Niveau **Error** das geht nur auf möglich zurück
> Fehler.

Configuration
-------------

In diesem Teil können Sie die allgemeinen Parameter von Plugins konfigurieren
![Konfiguration06](../.images/.configuration06.png)

-   **Allgemein** :

    -   **Ausgeschlossene Geräte automatisch löschen** :
        Mit der Option Ja können Sie die Geräte löschen, die von der ausgeschlossen sind
        Z-Wave-Netzwerk. Mit der Option Nein können Sie die Ausrüstung behalten
        in Jeedom, auch wenn sie aus dem Netzwerk ausgeschlossen wurden. Die Ausrüstung
        muss manuell gelöscht oder wiederverwendund werden
        Zuweisen einer neuen Z-Wave-ID, wenn Sie die migrieren
        Lead Controller.

    -   **Wenden Sie den empfohlenen Konfigurationssatz für die Aufnahme an** :
        Option zum Anwenden von Satzes von
        vom Jeedom-Team empfohlene Konfiguration (empfohlen)

    -   **Deaktivieren Sie die Hintergrundaktualisierung der Laufwerke** :
        Fordern Sie keine Aktualisierung der Laufwerke an
        im Hintergrund.

    -   **Zyklus (e)** : ermöglicht es, die Häufigkeit der Aufzüge zu definieren
        in Jeedom.

    -   **Z-Wave-Schlüsselanschluss** : der USB-Anschluss, an dem sich Ihre Schnittstelle befindet
        Z-WAVE ist angeschlossen. Wenn Sie die Razberry verwenden, haben Sie,
        Abhängig von Ihrer Architektur (RPI oder Jeedomboard) ist die 2
        Möglichkeiten am Ende der Liste.

    -   **Server-Port** (gefährliche Modifikation, muss das gleiche haben
        Wert auf allen Z-WAVE Remote Jeedoms) : lass uns
        Ändern Sie den internen Kommunikationsport von Dämons.

    -   **Backups** : Mit dieser Option können Sie Sicherungen der Datei verwalten
        Netzwerktopologie (siehe unten)

    -   **Modul konfigurieren** : ermöglicht das manuelle Abrufen von
        OpenZWave-Konfigurationsdateien mit Parametern für
        Modul sowie das Definieren von Modulbefehlen für
        ihre Verwendung.

        > **Tip**
        >
        > Modulkonfigurationen werden abgerufen
        > automatisch jede Nacht.

        > **Tip**
        >
        > Starten Sie den Daemon nach dem Aktualisieren von neu
        > Modulkonfigurationen sind nicht erforderlich.

        > **Important**
        >
        > Wenn Sie ein nicht erkanntes Modul und ein Update von haben
        > Konfiguration wurde gerade angewendet, Sie können manuell
        > Starten Sie das Abrufen von Modulkonfigurationen.

Sobald die Konfigurationen abgerufen wurden, wird es entsprechend den Änderungen dauern
gebracht:

-   Für ein neues Modul ohne Konfiguration oder Steuerung : ausschließen und
    Fügen Sie das Modul wieder hinzu.

-   Für ein Modul, für das nur die Parameter aktualisiert wurden :
    Starten Sie die Regeneration der Knotenerkennung über die Registerkarte Aktionen
    von Moduls (das Plugin muss neu starten).

-   Pour un Modul dont le « mapping » der Ordnungs a été corrigé : la
    Lupe an den Bedienelementen, siehe unten.

    > **Tip**
    >
    > Im Zweifelsfall wird empfohlen, das Modul auszuschließen und erneut einzuschließen.

Vergiss es nicht ![Konfiguration08](../.images/.configuration08.png) si
Sie nehmen eine Änderung vor.

> **Important**
>
> Wenn Sie Ubuntu verwenden : Damit der Dämon funktioniert, müssen Sie
> unbedingt Ubuntu 15 haben.04 (niedrigere Versionen haben einen Fehler und
> der Dämon kann nicht starten). Seien Sie vorsichtig, wenn Sie eine Wette platzieren
> aktuell ab 14.04 es dauert einmal in 15.04 Relaunch
> Installation von Nebengebäuden.

> **Important**
>
> Auswahl von Z-Wave-Schlüsselanschlusses im automatischen Erkennungsmodus,
> **Auto**, funktioniert nur für USB-Dongles.

Mobiles Panel
-------------

![Konfiguration09](../.images/.configuration09.png)

Ermöglicht die Anzeige oder Nichtanzeige von mobilen Panels bei Verwendung
die Anwendung auf einem Telefon.

Gerätekonfiguration
=============================

Die Konfiguration der Z-Wave-Geräte ist über das Menü zugänglich
Plugin :

![appliance01](../.images/.appliance01.png)

Unten finden Sie ein Beispiel für eine Z-Wave-Plugin-Seite (dargestellt mit
einige Geräte) :

![appliance02](../.images/.appliance02.png)

> **Tip**
>
> Platzieren Sie wie an vielen Stellen in Jeedom die Maus ganz links
> ruft ein Schnellzugriffsmenü auf (Sie können unter
> Lassen Sie es in Ihrem Profil immer sichtbar.).

> **Tip**
>
> Die Schaltflächen in der obersten Zeile **Synchroniser**,
> **Zwave Netzwerk** und **Santé**, sind nur sichtbar, wenn Sie in sind
> Modus **Expert**. ![](../.images/.appliance03.png)

Allgemein
-------

Hier finden Sie die gesamte Konfiguration Ihrer Geräte :

![appliance04](../.images/.appliance04.png)

-   **Name der Ausrüstung** : .

-   **Übergeordnetes Objekt** : gibt das übergeordnete Objekt an, zu dem
    gehört Ausrüstung.

-   **Kategorie** : Gerätekategorien (es kann gehören
    mehrere Kategorien).

-   **Activer** : macht Ihre Ausrüstung aktiv.

-   **Visible** : macht es auf dem Dashboard sichtbar.

-   **Knoten-ID** : . 
    .
    
    
    .

-   **Module** : 
    
    . 
    

-   **Marque** : .

-   **Configuration** : 
    module

-   **Assistant** : 
    

-   **Documentation** : 
    .

-   **Supprimer** : 
    .

> **Important**
>
> 
> . ![](../.images/.appliance11.png) Un
> 
> .

Commandes
---------

Nachfolgend finden Sie die Liste der Bestellungen :

![appliance05](../.images/.appliance05.png)

> **Tip**
>
> 
> .

-   Der im Dashboard angezeigte Name

-   Symbol : 
    

-   Bestellwert : 
    
    . 
    .

-   Typ und Subtyp.

-   .

-   .

-   .

-   .

-   "Statusrückmeldungswert "und" Dauer vor Statusrückmeldung" : permet
    Jeedom darauf hinzuweisen, dass nach einer Änderung der Informationen
    Der Wert muss nach der Änderung auf Y, X min zurückkehren. Beispiel : dans
    der Fall eines Anwesenheitsdetektors, der nur während a emittiert
    Anwesenheitserkennung ist es nützlich, zum Beispiel 0 zu setzen
    Wert und 4 in der Dauer, so dass 4 min nach einem Nachweis von
    
    setzt den Wert der Information auf 0 zurück (keine Bewegung mehr erkannt).

-   Chronik : ermöglicht das Historisieren der Daten.

-   Anzeige : ermöglicht die Anzeige der Daten im Dashboard.

-   Umgekehrt : .

-   Unit : Dateneinheit (kann leer sein).

-   Min /. max : Datengrenzen (können leer sein).

-   Erweiterte Konfiguration (kleine gekerbte Räder) : Anzeigen
    die erweiterte Konfiguration von Befehls (Methode
    Geschichte, Widget…).

-   Tist : Wird zum Testen von Befehls verwendet.

-   Löschen (unterschreiben -) : ermöglicht das Löschen von Befehls.

> **Important**
>
> Die Schaltfläche **Tester** 
> 
> . 
> 
> . 
> ,
> .

Die **loupe**, 
.
![appliance13](../.images/.appliance13.png) Si aucune Befehl n'est

.

> **Important**
>
> Die **loupe** . 
> 
> .


-----------------



![appliance06](../.images/.appliance06.png)


permet.

> **Important**
>
> 
> Befehle.


--------------------------


.

![appliance07](../.images/.appliance07.png)

Die Schaltfläche **Documentation** 
.


.

Die Schaltfläche **Assistant** 
.

Empfohlene Konfiguration
-------------------------

![appliance08](../.images/.appliance08.png)


Jeedom.

> **Tip**
>
> 
> .


.

-   **Einstellungen** 
    .

-   **** .

-   ****, .

-    **** 
    .


: **Empfohlene Konfiguration**, 
.

![appliance09](../.images/.appliance09.png)

.



![appliance10](../.images/.appliance10.png)

> **Important**
>
> 
> Konfiguration.


. 

.

![](../.images/.appliance11.png)

> **Tip**
>
> 
> 
> .


=========================



![node01](../.images/.node01.png)

 :

Zusammenfassung
------



.

> **Tip**
>
> 
> 
> . 
> 
> .

Valeurs
-------

![node02](../.images/.node02.png)


.
Die « mapping » von Befehle ist entièrement basé sur ces Information.

> **Tip**
>
> . 
> . Er ist
> 
> Moduldokumentation.

> **Tip**
>
> 
> ganz normal. 
> .

> **Important**
>
> 
> 
> . 
> Erfrischend. 
> 
> .
> ![](../.images/.node16.png) 
> 
> 
> . .

Einstellungen
----------

![node03](../.images/.node03.png)



.

,
![node04](../.images/.node04.png) le paramètre ist en attente d'être
appliqué.

.


.
![node05](../.images/.node05.png)


. 
.

.

> **Tip**
>
> 
> . 
> .

> **Tip**
>
>  **** 
> .

![node06](../.images/.node06.png)

> **Tip**
>
>  **** 
> 
> .

![node18](../.images/.node18.png)

> **Tip**
>
>  **Einstellungen aktualisieren** 
> .


.
![node17](../.images/.node17.png) Veillez vous référer à die documentation
.

Associations
------------


module.

![node07](../.images/.node07.png)


. 
.





.



Basic.

> **Tip**
>
> 
> .

> **Tip**
>
> 
> 
> .  : **Report** ou
> **LifeLine**.

> **Tip**
>
> .

> **Tip**
>
> 
> . 
> .

,
 **Verbunden mit welchen Modulen**

![node08](../.images/.node08.png)


.

****

.



![node09](../.images/.node09.png)

> **Important**
>
> 
> Haupt, um gut zu arbeiten. Aus diesem Grund ist die Steuerung
> ist mit und ohne Instanz 0 vorhanden.

Systeme
--------

Registerkarte, die die Systemparameter von Moduls gruppiert.

![node10](../.images/.node10.png)

> **Tip**
>
> Die BatterieModul werden in regelmäßigen Abständen aktiviert
> Weckintervall. Das Weckintervall ist a
> Kompromiss zwischen maximaler Akkulaufzeit und Reaktionen
> vom Gerät gewünscht. Um das Leben Ihres zu maximieren
> Module, passen Sie den Wert von Weckintervalls beispielsweise an 14400 an
> Sekunden (4h), je nach Modul und Verwendung noch höher.
> ![Knoten11](../.images/.node11.png)

> **Tip**
>
> Die Modul **Interrupteur** und **Variateur** kann ein implementieren
> Sonderbestellungsklasse genannt **SwitchAll** 0x27. Du kannst
> Verhalten hier ändern. Je nach Modul gibt es mehrere Möglichkeiten
> verfügbar.  **Alle ein- /. ausschalten** kann über gestartund werden
> Ihr Hauptsteuerungsmodul.

Actions
-------

Ermöglicht das Ausführen bestimmter Aktionen für das Modul.

![node12](../.images/.node12.png)

Bestimmte Aktionen sind je nach Modultyp und dessen Funktion aktiv
Möglichkeiten oder nach dem aktuellen Stand von Moduls wie zum Beispiel
wenn vom Controller für tot gehalten wird.

> **Important**
>
> Verwenden Sie keine Aktionen für ein Modul, wenn Sie nicht wissen, was
> das machen wir. Einige Aktionen sind irreversibel. Aktionen
> kann helfen, Probleme mit einem oder mehreren Modulen zu lösen
> Z-WAVE.

> **Tip**
>
> Die **Regeneration der Knotenerkennung** kann das erkennen
> Modul zum Abrufen von letzten Parametersatzes. Diese Aktion
> ist erforderlich, wenn Sie darüber informiert werden, dass eine Parameteraktualisierung und
> oder das Verhalten von Moduls ist für den ordnungsgemäßen Betrieb erforderlich. Die
> Die Regeneration der Knotenerkennung impliziert einen NeuStart der
> Netzwerk führt der Assistent es automatisch durch.

> **Tip**
>
> Wenn Sie mehrere identische Modul haben, von denen es erforderlich ist
> ausführen **Regeneration der Knotenerkennung**, Er ist
> Es ist möglich, es einmal für alle identischen Modul zu starten.

![node13](../.images/.node13.png)

> **Tip**
>
> Wenn ein Batteriemodul nicht mehr erreichbar ist und Sie möchten
> Ausschließen, dass der Ausschluss nicht stattfindet, können Sie starten
> **Geisterknoten entfernen** Ein Assistent wird anders ausführen
> Aktionen zum Entfernen von sogenannten Ghost-Moduls. Diese Aktion beinhaltet
> Starten Sie das Netzwerk neu und es kann einige Minuten dauern
> abgeschlossen.

![node14](../.images/.node14.png)

Nach dem Start wird empfohlen, den Konfigurationsbildschirm von zu schließen
Modul und überwachen Sie die Entfernung von Moduls über den Integritätsbildschirm
Z-Wave.

> **Important**
>
> Über diesen Assistenten können nur Modul mit Batterie gelöscht werden.

Statistiques
------------

Diese Registerkarte enthält einige Kommunikationsstatistiken mit dem Knoten.

![node15](../.images/.node15.png)

Kann bei Modulen von Interesse sein, die von der
Controller "Tot".

Einschluss /. Ausschluss
=====================

Wenn ein Modul das Werk verlässt, gehört es keinem Z-Wave-Netzwerk an.

Einschlussmodus
--------------

Das Modul muss zur Kommunikation mit einem vorhandenen Z-Wave-Netzwerk verbunden sein
mit den anderen Modulen dieses Netzwerks. Dieser Vorgang wird aufgerufen
**Inclusion**. Geräte können auch ein Netzwerk verlassen.
Dieser Vorgang wird aufgerufen **Exclusion**. Beide Prozesse werden eingeleitet
vom Hauptcontroller von Z-Wave-Netzwerks.

![addremove01](../.images/.addremove01.png)

Mit dieser Schaltfläche können Sie in den Einschlussmodus wechseln, um ein Modul hinzuzufügen
zu Ihrem Z-Wave-Netzwerk.

Sie können den Einschlussmodus auswählen, nachdem Sie auf die Schaltfläche geklickt haben
**Inclusion**.

![addremove02](../.images/.addremove02.png)

Seit dem Erscheinen der Z-WAVE + ist es möglich, die zu sichern
Austausch zwischen dem Controller und den Knoten. Es wird daher empfohlen,
mache Einschlüsse im Modus **Sicher**.

Wenn ein Modul jedoch nicht im sicheren Modus enthalten sein kann, bitte
schließe es in den Modus ein **Nicht sicher**.

Einmal im Einschlussmodus : Jeedom sagt es dir.

\ [TIPP \] Ein Modul 'nicht sicher' kann Modul 'nicht' bestellen
sicher '. Ein 'ungesichertes' Modul kann kein Modul bestellen
'sicher '. Ein "sicheres" Modul kann Modul nicht bestellen
sicher ', sofern der Sender dies unterstützt.

![addremove03](../.images/.addremove03.png)

Sobald der Assistent gestartund ist, müssen Sie dasselbe auf Ihrem Modul tun
(Informationen zum Umschalten in den Modus finden Sie in der Dokumentation
inclusion).

> **Tip**
>
> Bis Sie das Stirnband haben, sind Sie nicht im Modus
> Aufnahme.

Wenn Sie erneut auf die Schaltfläche klicken, verlassen Sie den Einschlussmodus.

> **Tip**
>
> Es wird empfohlen, vor der Aufnahme eines neuen Moduls das zu sein
> "neu "auf dem Markt, um die Bestellung zu starten **Modul konfigurieren** via
> Plugin-Konfigurationsbildschirm. Diese Aktion wird wiederhergestellt
> alle neuesten Versionen der Konfigurationsdateien
> openzwave und die Jeedom-Befehlszuordnung.

> **Important**
>
> Während einer Aufnahme wird empfohlen, dass sich das Modul in der Nähe befindet
> vom Hauptcontroller, weniger als einen Meter von Ihrem Jeedom entfernt.

> **Tip**
>
> Einige Modul erfordern eine Aufnahme in den Modus
> **Sicher**, zum Beispiel für Türschlösser.

> **Tip**
>
> Beachten Sie, dass Sie über die mobile Oberfläche auch auf die Aufnahme zugreifen können,
> Das mobile Panel muss aktiviert sein.

> **Tip**
>
> Wenn das Modul bereits zu einem Netzwerk gehört, befolgen Sie den Vorgang
> Ausschluss, bevor Sie es in Ihr Netzwerk aufnehmen. Ansonsten die Aufnahme von
> Dieses Modul wird fehlschlagen. Es wird auch empfohlen, a
> Ausschluss vor Aufnahme, auch wenn das Produkt neu ist, aus
> Karton.

> **Tip**
>
> Sobald sich das Modul an seinem endgültigen Speicherort befindet, müssen Sie es starten
> Die Aktion kümmert sich um das Netzwerk, um alle Modul von zu fragen
> Aktualisiere alle Nachbarn.

Ausschlussmodus
--------------

![addremove04](../.images/.addremove04.png)

Mit dieser Schaltfläche können Sie in den Ausschlussmodus wechseln, um a zu entfernen
Modul Ihres Z-Wave-Netzwerks müssen Sie dasselbe mit Ihrem tun
Modul (Informationen zum Umschalten in den Modus finden Sie in der Dokumentation
exclusion).

![addremove05](../.images/.addremove05.png)

> **Tip**
>
> Bis Sie das Stirnband haben, sind Sie nicht im Modus
> Ausschluss.

Wenn Sie erneut auf die Schaltfläche klicken, wird der Ausschlussmodus beendet.

> **Tip**
>
> Beachten Sie, dass Sie über die mobile Oberfläche auch auf den Ausschluss zugreifen können.

> **Tip**
>
> Ein Modul muss nicht von derselben Steuerung an ausgeschlossen werden
> was es zuvor enthalten war. Daher die Tatsache, dass wir empfehlen
> Führen Sie vor jedem Einschluss einen Ausschluss aus.

Synchroniser
------------

![addremove06](../.images/.addremove06.png)

Schaltfläche zum Synchronisieren der Modul von Z-Wave-Netzwerks mit dem
Jeedom Ausrüstung. Die Modul sind der Hauptsteuerung zugeordnet,
Die Ausrüstung in Jeedom wird automatisch erstellt, wenn sie vorhanden ist
Einbeziehung. Sie werden auch automatisch gelöscht, wenn sie ausgeschlossen werden.,
wenn die Option **Ausgeschlossene Geräte automatisch löschen** est
aktiviert.

Wenn Sie Modul ohne Jeedom enthalten haben (erfordert einen Dongle mit
Batterie wie der Aeon-labs Z-Stick GEN5), Synchronisation wird sein
notwendig nach dem Einstecken von Schlüssels, sobald der Daemon gestartund ist und
fonctionnel.

> **Tip**
>
> Wenn Sie das Bild nicht haben oder Jeedom Ihr Modul nicht erkannt hat,
> Diese Schaltfläche kann zur Korrektur verwendund werden (vorausgesetzt, das Interview mit dem
> Modul ist abgeschlossen).

> **Tip**
>
> Wenn Sie sich in Ihrer Routing-Tabelle und /. oder auf dem Z-Wave-Integritätsbildschirm befinden, sind Sie
> haben ein oder mehrere Modul mit ihrem Namen **Gattungsname**, la
> Durch die Synchronisierung wird diese Situation behoben.

Die Schaltfläche Synchronisieren ist nur im Expertenmodus sichtbar :
![addremove07](../.images/.addremove07.png)

Z-Wave-Netzwerke
==============

![network01](../.images/.network01.png)

Hier finden Sie allgemeine Informationen zu Ihrem Z-Wave-Netzwerk.

![network02](../.images/.network02.png)

Zusammenfassung
------

Auf der ersten Registerkarte finden Sie eine grundlegende Zusammenfassung Ihres Z-Wave-Netzwerks,
Sie finden insbesondere den Status von Z-Wave-Netzwerks sowie die Nummer
Elemente in der Warteschlange.

**Informations**

-   Gibt allgemeine Informationen über das Netzwerk, das Datum von
    Start, die Zeit, die erforderlich ist, um das Netzwerk in einem Zustand zu erhalten
    sagt funktional.

-   Die Gesamtzahl der Knoten im Netzwerk sowie die Anzahl der schlafenden Knoten
    im Moment.

-   Das Anforderungsintervall ist mit der manuellen Aktualisierung verbunden. Er
    ist im Z-Wave-Motor nach 5 Minuten voreingestellt.

-   Die Nachbarn von Controllers.

**Etat**

![network03](../.images/.network03.png)

Eine Reihe von Informationen über den aktuellen Status von Netzwerks, nämlich :

-   Aktueller Zustand vielleicht **Treiber initialisiert**, **Topologie geladen**
    oder **Ready**.

-   Ausgehender Schwanz, gibt die Anzahl der Nachrichten an, die in der Warteschlange stehen
    Controller wartund darauf, gesendund zu werden. Dieser Wert ist im Allgemeinen
    hoch während von Netzwerkstarts, wenn der Status noch aktiv ist
    **Treiber initialisiert**.

Sobald das Netzwerk mindestens erreicht hat **Topologie geladen**, des
Mechanismen innerhalb von Z-Wave-Servers erzwingen Aktualisierungen von
Werte, dann ist es völlig normal, die Anzahl der zu sehen
Nachrichten. Dies wird schnell auf 0 zurückkehren.

> **Tip**
>
> Das Netzwerk soll funktionsfähig sein, wenn es den Status erreicht
> **Topologie geladen**, das heißt, dass die Menge der Sektorknoten
> haben ihre Interviews abgeschlossen. Abhängig von der Anzahl der Modul wird die
> Batterie- /. Sektorverteilung, die Wahl von USB-Dongles und von PCs, auf dem
> Wenn das Z-Wave-Plugin aktiviert wird, erreicht das Netzwerk diesen Status zwischen a
> und fünf Minuten.

Ein Netzwerk **Ready**, bedeutet, dass alle Sektor- und Stapelknoten haben
beendete ihr Interview.

> **Tip**
>
> Abhängig von Ihren Modulen ist es möglich, dass das Netzwerk
> erreicht nie den Status von selbst **Ready**. Die Fernbedienungen,
> Wachen Sie zum Beispiel nicht alleine auf und ergänzen Sie sich nicht
> niemals ihr Interview. In diesem Fall ist das Netzwerk vollständig
> betriebsbereit und auch wenn die Fernbedienungen ihre nicht abgeschlossen haben
> Interview stellen sie ihre Funktionalität innerhalb von Netzwerks sicher.

**Kapazitäten**

Wird verwendet, um herauszufinden, ob der Controller ein Hauptcontroller ist oder
secondaire.

**Systeme**

Zeigt verschiedene Systeminformationen an.

-   Informationen zum verwendeten USB-Anschluss.

-   OpenZwave-Bibliotheksversion

-   Version der Python-OpenZwave-Bibliothek

Actions
-------

![network05](../.images/.network05.png)

Hier finden Sie alle möglichen Aktionen für alle Ihre
Z-Wave-Netzwerk. Jede Aktion wird von einer kurzen Beschreibung begleitet.

> **Important**
>
> Einige Aktionen sind wirklich riskant oder sogar irreversibel, das Team
> Jeedom kann im schlimmsten Fall nicht zur Verantwortung gezogen werden
> Manipulation.

> **Important**
>
> Einige Modul müssen im sicheren Modus von enthalten sein
> Beispiel für Türschlösser. Sichere Inklusion muss sein
> über die Aktion dieses Bildschirms gestartet.

> **Tip**
>
> Wenn eine Aktion nicht gestartund werden kann, wird sie bis deaktiviert
> wenn es wieder ausgeführt werden kann.

Statistiques
------------

![network06](../.images/.network06.png)

Hier finden Sie allgemeine Statistiken für alle Ihre
Z-Wave-Netzwerk.

Netzwerkdiagramm
-------------------

![network07](../.images/.network07.png)

Diese Registerkarte gibt Ihnen eine grafische Darstellung der verschiedenen
Verbindungen zwischen Knoten.

Erklärung der Farblegende :

-   **Noir** : Der Hauptcontroller, allgemein vertreten
    wie Jeedom.

-   **Vert** : Direkte Kommunikation mit dem Controller, ideal.

-   **Blue** : Für Steuerungen wie Fernbedienungen sind sie
    mit dem primären Controller verbunden, haben aber keinen Nachbarn.

-   **Jaune** : Alle Straßen haben mehr als einen Sprung vor der Ankunft
    an die Steuerung.

-   **Gris** : Das Interview ist noch nicht abgeschlossen, die Links werden sein
    wirklich bekannt, sobald das Interview abgeschlossen ist.

-   **Rouge** : Vermutlich tot oder ohne Nachbarn, nimmt nicht /. nicht mehr an teil
    Netzwerknetz.

> **Tip**
>
> Im Netzwerkdiagramm werden nur aktive Geräte angezeigt.

Das Z-Wave-Netzwerk besteht aus drei verschiedenen Knotentypen mit
drei Hauptfunktionen.

Der Hauptunterschied zwischen den drei Knotentypen besteht in ihren
Kenntnis der Netzwerk-Routing-Tabelle und danach ihrer
Fähigkeit, Nachrichten an das Netzwerk zu senden:

Routing-Tabelle
----------------

Jeder Knoten kann bestimmen, in welchen anderen Knoten sich befinden
Direkte Kommunikation. Diese Knoten werden Nachbarn genannt. Während
Aufnahme und /. oder später auf Anfrage kann der Knoten
den Controller über die Liste der Nachbarn zu informieren. Dank diesen
Informationen kann der Controller eine Tabelle erstellen, die hat
alle Informationen zu möglichen Kommunikationswegen in
ein Netzwerk.

![network08](../.images/.network08.png)

Die Zeilen der Tabelle enthalten die Quellknoten und die Spalten
Zielknoten enthalten. Siehe die Legende für
Verstehe die Zellenfarben, die die Verbindungen zwischen zwei anzeigen
Knoten.

Erklärung der Farblegende :

-   **Vert** : Direkte Kommunikation mit dem Controller, ideal.

-   **Blue** : Mindestens 2 Routen mit einem Sprung.

-   **Jaune** : Weniger als 2 Routen mit einem Sprung.

-   **Gris** : Das Interview ist noch nicht abgeschlossen, wird es tatsächlich sein
    aktualisiert, nachdem das Interview abgeschlossen ist.

-   **Orange** : Alle Straßen haben mehr als einen Sprung. Kann verursachen
    Latenzen.

> **Tip**
>
> Im Netzwerkdiagramm werden nur aktive Geräte angezeigt.

> **Important**
>
> Ein Modul, von dem angenommen wird, dass es tot ist, nimmt nicht mehr an der Vernetzung von Netzwerks teil.
> Es wird hier mit einem roten Ausrufezeichen in einem Dreieck markiert.

> **Tip**
>
> Sie können die Nachbaraktualisierung manuell nach Modulen starten
> oder für das gesamte Netzwerk mit den Schaltflächen in der
> Routing-Tabelle.

Santé
=====

![health01](../.images/.health01.png)

Dieses Fenster fasst den Status Ihres Z-Wave-Netzwerks zusammen :

![health02](../.images/.health02.png)

Du hast hier :

-   **Module** : Wenn Sie den Namen Ihres Moduls anklicken, können Sie dies tun
    Zugriff direkt.

-   **ID** : Identifikation Ihres Moduls im Z-Wave-Netzwerk.

-   **Notification** : letzte Art von Austauschs zwischen dem Modul und dem
    Controller

-   **Groupe** : Gibt an, ob die Gruppenkonfiguration in Ordnung ist
    (Controller mindestens in einer Gruppe). Wenn Sie nichts haben, liegt es daran
    Das Modul unterstützt den Begriff der Gruppe nicht, dies ist normal

-   **Constructeur** : Gibt an, ob Informationen abgerufen werden
    Modulidentifikation ist ok

-   **Voisin** : Gibt an, ob die Liste der Nachbarn abgerufen wurde

-   **Statut** : Zeigt den Status von Interviews (Abfragephase) des
    module

-   **Batterie** : Batteriestand von Moduls (ein Netzstecker
    zeigt an, dass das Modul über das Stromnetz mit Strom versorgt wird).

-   **Weckzeit** : für BatterieModul gibt es die
    Frequenz in Sekunden der Momente, in denen das Modul
    automatisch aufwachen.

-   **Gesamtpaket** : Zeigt die Gesamtzahl der empfangenen Pakete an oder
    erfolgreich an das Modul gesendet.

-   **%OK** : Zeigt den Prozentsatz der gesendeten /. empfangenen Pakete an
    erfolgreich.

-   **Temporisation** : Zeigt die durchschnittliche Paketversandverzögerung in ms an.

-   **Letzte Benachrichtigung** : Datum der letzten Benachrichtigung von
    Modul und die nächste geplante Weckzeit für Module
    die schlafen.

    -   Sie können auch informieren, wenn der Knoten noch nicht vorhanden ist
        ist seit dem Start von Dämons einmal aufgewacht.

    -   Und zeigt an, ob ein Knoten nicht wie erwartund aufgewacht ist.

-   **Ping** : Senden Sie eine Reihe von Nachrichten an das Modul an
    Testen Sie die ordnungsgemäße Funktion.

> **Important**
>
> Deaktivierte Geräte werden angezeigt, aber keine Informationen von
> Diagnose wird nur vorhanden sein.

Dem Namen von Moduls können ein oder zwei Bilder folgen:

![health04](../.images/.health04.png) Modules supportant la
BEFEHL\_KLASSE\_ZWAVE\_PLUS\_INFO

![health05](../.images/.health05.png) Modules supportant la
BEFEHL\_KLASSE\_SICHERHEIT und sicher.

![health06](../.images/.health06.png) Modules supportant la
BEFEHL\_KLASSE\_SICHERHEIT und nicht sicher.

![health07](../.images/.health07.png) Modul FLiRS, routeurs esclaves
(Batteriemodule) mit häufigem Hören.

> **Tip**
>
> Der Ping-Befehl kann verwendund werden, wenn das Modul als tot angenommen wird
> "DEATH "um zu bestätigen, ob dies wirklich der Fall ist.

> **Tip**
>
> Ruhende Modul reagieren nur dann auf Ping, wenn
> als nächstes aufwachen.

> **Tip**
>
> Timeout-Benachrichtigung bedeutund nicht unbedingt ein Problem
> mit dem Modul. Klingeln und in den meisten Fällen das Modul
> wird mit einer Benachrichtigung antworten **NoOperation** was eine Rückkehr bestätigt
> fruchtbarer Klingeln.

> **Tip**
>
> Zeitüberschreitung und% OK auf Knoten mit Batterien vor Abschluss
> von ihrem Interview ist nicht signifikant. In der Tat geht der Knoten nicht
> Beantworten Sie die Fragen von Controllers, ob er schläft
> tief.

> **Tip**
>
> Der Z-Wave-Server sorgt automatisch dafür, dass Tests auf dem Server gestartund werden
> Timeout-Modul nach 15 Minuten

> **Tip**
>
> Der Z-Wave-Server versucht automatisch, Modul erneut bereitzustellen
> vermutlich tot.

> **Tip**
>
> Eine Warnung wird an Jeedom gesendet, wenn das Modul als tot angenommen wird. Sie
> kann eine Benachrichtigung aktivieren, um am meisten informiert zu werden
> schnell möglich. Siehe die Nachrichtenkonfiguration auf dem Bildschirm
> Jeedom-Konfiguration.

![health03](../.images/.health03.png)

> **Tip**
>
> Wenn Sie sich in Ihrer Routing-Tabelle und /. oder auf dem Z-Wave-Integritätsbildschirm befinden
> haben ein oder mehrere Modul mit ihrem Namen **Gattungsname**, la
> Durch die Synchronisierung wird diese Situation behoben.

> **Tip**
>
> Wenn Sie sich in Ihrer Routing-Tabelle und /. oder auf dem Z-Wave-Integritätsbildschirm befinden
> ein oder mehrere Modul benannt haben **Unknown**, das heißt
> Das Modulinterview wurde nicht erfolgreich abgeschlossen. Du hast
> wahrscheinlich ein **NOK** in der Konstruktorspalte. Öffnen Sie das Detail
> der Module, um die vorgeschlagenen Lösungen auszuprobieren.
> (siehe Abschnitt Fehlerbehebung und Diagnose unten)

Interviewstatus
---------------------

Schritt von Interviewens eines Moduls nach dem Starten von Daemons.

-   **None** Initialisierung von Knotensuchprozesses.

-   **ProtocolInfo** Rufen Sie in diesem Fall Protokollinformationen ab
    Der Knoten hört zu (Listener), seine maximale Geschwindigkeit und seine Klassen
    von Peripheriegeräten.

-   **Probe** Pingen Sie das Modul an, um festzustellen, ob es wach ist.

-   **WakeUp** Starten Sie den Aufweckvorgang, falls es sich um einen handelt
    Schlafknoten.

-   **ManufacturerSpecific1** Rufen Sie den Namen von Herstellers ab und
    ID-Produkte, wenn ProtocolInfo dies zulässt.

-   **NodeInfo** Informationen zur Klassenverwaltung abrufen
    unterstützte Befehle.

-   **NodePlusInfo** Rufen Sie ZWave + -Informationen zum Support ab
    unterstützte Befehlsklassen.

-   **SecurityReport** Rufen Sie die Liste der Auftragsklassen ab, die
    erfordern Sicherheit.

-   **ManufacturerSpecific2** Rufen Sie den Namen von Herstellers und die
    Produktkennungen.

-   **Versions** Versionsinformationen abrufen.

-   **Instances** Abrufen von Klasseninformationen für mehrere Instanzen
    der Ordnung.

-   **Static** Statische Informationen abrufen (ändert sich nicht).

-   **CacheLoad** Pingen Sie das Modul beim NeuStart mit dem KonfigurationsAbdeckung an
    von Geräts.

-   **Associations** Informationen zu Assoziationen abrufen.

-   **Neighbors** Rufen Sie die Liste der benachbarten Knoten ab.

-   **Session** Sitzungsinformationen abrufen (Änderungen selten).

-   **Dynamic** Dynamische Informationen abrufen
    (ändert sich häufig).

-   **Configuration** Parameterinformationen abrufen von
    Konfigurationen (nur auf Anfrage).

-   **Complete** Der Interviewprozess für diesen Knoten ist abgeschlossen.

Notification
------------

Details zu Benachrichtigungen, die von Modulen gesendund werden

-   **Completed** Aktion erfolgreich abgeschlossen.

-   **Timeout** Verzögerungsbericht beim Senden einer Nachricht gemeldet.

-   **NoOperation** Berichten Sie bei einem Knotentist (Ping), dass die Nachricht
    wurde erfolgreich gesendet.

-   **Awake** Melden Sie, wenn ein Knoten gerade aufgewacht ist

-   **Sleep** Melden Sie, wenn ein Knoten eingeschlafen ist.

-   **Dead** Melden Sie, wenn ein Knoten als tot angenommen wird.

-   **Alive** Bericht, wenn ein Knoten neu gestartund wird.

Backups
=======

Mit dem Sicherungsteil können Sie die Sicherungen der Topologie verwalten
von Ihrem Netzwerk. Dies ist Ihre zwcfgxxx-Datei.xml, es ist das
Der letzte bekannte Status Ihres Netzwerks ist eine Art Cache Ihres Netzwerks
Netzwerk. Von diesem Bildschirm aus können Sie :

-   Starten Sie eine Sicherung (bei jedem Stopp wird eine Sicherung erstellt
    Netzwerk und während kritischer Operationen). Die letzten 12 Backups
    gehalten werden

-   Stellen Sie eine Sicherung wieder her (indem Sie sie aus der Liste auswählen
    gerade oben)

-   Löschen Sie eine Sicherung

![backup01](../.images/.backup01.png)

Aktualisieren Sie OpenZWave
=======================

Nach einem Update von Z-Wave-Plugins ist es möglich, dass Jeedom dies tut
Anforderung zum Aktualisieren von Z-Wave-Abhängigkeiten. Ein NOK auf dem Niveau von
Abhängigkeiten werden angezeigt:

![update01](../.images/.update01.png)

> **Tip**
>
> Eine Aktualisierung der Abhängigkeiten ist nicht bei jeder Aktualisierung durchzuführen
> Plugin.

Jeedom sollte das Abhängigkeitsupdate selbst starten, wenn das
Plugin betrachtet, dass sie sind **NOK**. Diese Validierung wird am durchgeführt
nach 5 Minuten.

Die Dauer dieses Vorgangs kann je nach System variieren
(bis zu mehr als 1 Stunde auf Himbeer-Pi)

Sobald die Aktualisierung der Abhängigkeiten abgeschlossen ist, wird der Dämon neu gestartet
automatisch nach Validierung von Jeedom. Diese Validierung ist
nach 5 Minuten erledigt.

> **Tip**
>
> Für den Fall, dass keine Aktualisierungsabhängigkeiten auftreten
> nicht vollständig, bitte konsultieren Sie das Protokoll **Openzwave\_update** qui
> sollte Sie über das Problem informieren.

Liste kompatibler Module
============================

Sie finden die Liste der kompatiblen Module
[hier](https:/./.jeedom.fr/.doc/.documentation/.zwave-modules/.fr_FR/.doc-zwave-modules-equipement.compatible.html)

Fehlerbehebung und Diagnose
=======================

Mein Modul wird nicht erkannt oder enthält keine Produkt- und Typkennungen
-------------------------------------------------------------------------------

![troubleshooting01](../.images/.troubleshooting01.png)

Starten Sie die Regeneration der Knotenerkennung auf der Registerkarte Aktionen
.

Wenn Sie in diesem Szenario mehrere Modul haben, starten Sie **Regenerat
Erkennung unbekannter Knoten** vom Bildschirm **Zwave Netzwerk** onglet
**Actions**.

Mein Modul wird vom Dead-Controller als tot angenommen
--------------------------------------------------

![troubleshooting02](../.images/.troubleshooting02.png)

Wenn das Modul noch angeschlossen und erreichbar ist, befolgen Sie die Lösungen
im Modulbildschirm vorgeschlagen.

Wenn das Modul abgebrochen wurde oder wirklich defekt ist, Sie
kann es mit aus dem Netzwerk ausschließen **Löschen Sie den fehlerhaften Knoten**
über tab **Actions**.

Wenn das Modul repariert wurde und ein neues Modul
Ersatz wurde geliefert, den Sie starten können **Ersetzen Sie den ausgefallenen Knoten**
über tab **Actions**, Der Controller löst dann die Aufnahme aus
muss mit der Aufnahme in das Modul fortfahren. Die Identifikation von alten Moduls lautet
gehalten sowie seine Befehle.

Verwendung von SwitchAll-Befehls
--------------------------------------

![troubleshooting03](../.images/.troubleshooting03.png)

Es ist über Ihren Controller-Knoten verfügbar. Ihr Controller sollte
haben die Befehle Alle einschalten und Alle ausschalten.

Wenn Ihr Controller nicht in Ihrer Modulliste angezeigt wird, starten Sie die
synchronisation.

![troubleshooting04](../.images/.troubleshooting04.png)

Der Befehl Alle Klassen wechseln wird im Allgemeinen unterstützt
Schalter und Dimmer. Sein Verhalten ist auf konfigurierbar
jevon Modul, das es unterstützt.

So können wir auch:

-   Deaktivieren Sie den Befehl Alle Klassen wechseln.

-   Aktivieren Sie für Ein und Aus.

-   Nur ein aktivieren.

-   Nur Aus aktivieren.

Die Auswahl der Optionen hängt vom Hersteller ab.

Sie müssen sich also die Zeit nehmen, um alle zu überprüfen
schaltund /. dimmert vor dem Einrichten eines Szenarios, wenn Sie dies nicht tun
nicht nur Kontrollleuchten.

Mein Modul verfügt nicht über einen Szenen- oder Schaltflächenbefehl
----------------------------------------------

![troubleshooting05](../.images/.troubleshooting05.png)

Sie können den Befehl im Befehlszuordnungsbildschirm hinzufügen.

Dies ist eine Bestellung **Info** in CC **0x2b** Instanz **0** commande
**Daten \ [0 \]. val**

Der Szenenmodus muss in den Moduleinstellungen aktiviert sein. Siehe die
Dokumentation Ihres Moduls für weitere Details.

Aktualisierungswerte erzwingen
-------------------------------------

Es ist möglich, auf Anfrage die Aktualisierung der Werte zu erzwingen
eine Instanz für einen bestimmten Klassenbefehl.

Es ist möglich, über eine http-Anfrage oder eine Bestellung zu erstellen
im Gerätezuordnungsbildschirm.

![troubleshooting06](../.images/.troubleshooting06.png)

Dies ist eine Bestellung **Action** Wählen Sie die **CC** gewünscht für a
**Instance** mit dem Befehl gegeben **data \ [0 \]. ForceRefresh ()**

Alle Instanzindizes für diesen Klassenbefehl werden abgelegt
auf dem neuesten Stand. Die Knoten an den Batterien warten auf ihr nächstes Erwachen
aktualisieren ihren Wert.

Sie können es auch per Skript verwenden, indem Sie eine http-Anfrage an senden
Z-WAVE REST-Server.

Ersetzen Sie ip\_jeedom, node\_id, instance\_id, cc\_id und index

http:/./.token:\#APIKEY\#@ip\_jeedom:8083/.ZWaveAPI/.Run/.devicesnode\_id.instances\[instance\_id\].commandClasses\[cc\_id\].data\[index\].ForceRefresh()

Der Zugriff auf die REST-API wurde geändert (siehe Details)
[hier](./.restapi.asciidoc).

Übertragen Sie die Modul auf eine neue Steuerung
------------------------------------------------

Aus verschiedenen Gründen müssen Sie möglicherweise übertragen
Alle Ihre Modul auf einem neuen Hauptcontroller.

Sie entscheiden sich zu gehen **raZberry** zu einem **Z-Stick Gen5** oder weil
dass Sie eine durchführen müssen **Reset** komplett von Hauptsteuerung.

Hier sind verschiedene Schritte, um dorthin zu gelangen, ohne Ihre Szenarien zu verlieren,
Wert Widgets und Verlauf:

-   1 \) Erstellen Sie ein Jeedom-Backup.

-   2 \) Denken Sie daran, Ihre Parameterwerte für jeden aufzuschreiben (Screenshot)
    Modul gehen sie durch Ausschluss verloren.

-   3 \) Deaktivieren Sie in der Z-Wave-Konfiguration "Löschen"
    Geräte automatisch ausschließen "und sichern.
    Netzwerk startund neu.

-   4a) Im Fall von a **Reset**, Setzen Sie den Controller zurück
    Haupt und starten Sie das Plugin neu.

-   4b) Stoppen Sie für einen neuen Controller Jeedom und trennen Sie den alten
    Controller und stecken Sie den neuen ein. Starten Sie Jeedom.

-   5 \) Ändern Sie für jevon Z-Wave-Gerät die ZWave-Identifikation in **0**.

-   6 \) Öffnen Sie 2 Seiten von Z-Wave-Plugins auf verschiedenen Registerkarten.

-   7 \) (Über die erste Registerkarte) Gehen Sie zur Konfigurationsseite von a
    Modul, das Sie in den neuen Controller aufnehmen möchten.

-   8 \) (Über die zweite Registerkarte) Ausschließen und dann einschließen
    . Neue Ausrüstung wird erstellt.

-   9 \) Kopieren Sie die Z-Wave-Identifikation von neuen Geräts und löschen Sie sie
    diese Ausrüstung.

-   10 \) Kehren Sie zur Registerkarte von alten Moduls (1. Registerkarte) zurück und fügen Sie sie ein
    die neue Identifikation anstelle der alten Identifikation.

-   11 \) ZWave-Parameter gingen beim Ausschluss /. Einschluss verloren,
    Denken Sie daran, Ihre spezifischen Einstellungen zurückzusetzen, wenn Sie das nicht verwenden
    Standardwerte.

-   11 \) Wiederholen Sie die Schritte 7 bis 11 für jevon zu übertragende Modul.

-   12 \) Am Ende sollten Sie keine Ausrüstung mehr in Identifikation 0 haben.

-   13 \) Überprüfen Sie, ob alle Modul auf dem Bildschirm von korrekt benannt sind
    Gesundheit Z-WAVE. Starten Sie die Synchronisierung, wenn dies nicht der Fall ist.

Ersetzen Sie ein fehlerhaftes Modul
------------------------------

So wiederholen Sie die Aufnahme eines fehlerhaften Moduls, ohne Ihr Modul zu verlieren
Wertszenarien, Widgets und Verlauf

Wenn angenommen wird, dass das Modul "Tot" ist" :

-   Beachten Sie (Screenshot) Ihre Parameterwerte, sie gehen verloren
    nach Aufnahme.

-   Gehen Sie zur Registerkarte Aktionen von Moduls und starten Sie den Befehl
    "Ersetzen Sie den ausgefallenen Knoten".

-   Der Controller befindund sich im Einschlussmodus. Fahren Sie mit dem Einschluss gemäß dem fort
    Moduldokumentation.

-   Setzen Sie Ihre spezifischen Parameter zurück.

Wenn das Modul nicht als "tot" angesehen wird, aber dennoch zugänglich ist:

-   Deaktivieren Sie in der ZWave-Konfiguration das Kontrollkästchen "Löschen"
    automatisch ausgeschlossene Geräte".

-   Beachten Sie (Screenshot) Ihre Parameterwerte, sie gehen verloren
    nach Aufnahme.

-   Schließen Sie das fehlerhafte Modul aus.

-   Gehen Sie zur Konfigurationsseite von fehlerhaften Moduls.

-   Öffnen Sie die ZWave-Plugin-Seite in einem neuen Tab.

-   Schließen Sie das Modul ein.

-   Kopieren Sie die Identifikation von neuen Moduls und löschen Sie dieses Gerät.

-   Kehren Sie zur Registerkarte von alten Moduls zurück und fügen Sie die neue Identifikation in ein
    der Ort von alten Ausweises.

-   Setzen Sie Ihre spezifischen Parameter zurück.

Entfernen von Geisterknotens
----------------------------

Wenn Sie die Kommunikation mit einem batteriebetriebenen Modul verloren haben und
Wenn Sie es aus dem Netzwerk ausschließen möchten, ist es möglich, dass der Ausschluss
ist nicht erfolgreich oder der Knoten bleibt in Ihrem Netzwerk vorhanden.

Der automatische Ghost Node-Assistent ist verfügbar.

-   Gehen Sie zur Registerkarte Aktionen von zu löschenden Moduls.

-   Er wird wahrscheinlich einen Status haben **CacheLoad**.

-   Befehl starten **Geisterknoten entfernen**.

-   Das Z-Wave-Netzwerk stoppt. Der automatische Assistent ändert die
    Datei **zwcfg** um das CC Aufwachen aus dem Modul zu entfernen. Die
    Netzwerk startund neu.

-   Schließen Sie den Modulbildschirm.

-   Öffnen Sie den Bildschirm Z-WAVE Health.

-   Warten Sie, bis der Startzyklus abgeschlossen ist (Topologie geladen)..

-   Das Modul wird normalerweise als tot markiert.

-   In der nächsten Minute sollte der Knoten vom Bildschirm verschwinden
    Gesundheit.

-   In der Z-Wave-Konfiguration haben Sie die Option deaktiviert
    "Ausgeschlossene Geräte automatisch entfernen ", müssen Sie
    Löschen Sie die entsprechenden Geräte manuell.

Dieser Assistent ist nur für BatterieModul verfügbar.

Aktionen nach der Aufnahme
----------------------

Es wird empfohlen, den Einschluss mindestens 1 M vom Controller entfernt durchzuführen
main, aber es wird nicht die endgültige Position Ihres neuen Moduls sein.
Im Folgenden finden Sie einige bewährte Methoden, die nach der Aufnahme einer neuen Vorgehensweise zu befolgen sind
Modul in Ihrem Netzwerk.

Sobald die Aufnahme abgeschlossen ist, wird eine Reihe von
Parameter für unser neues Modul, um das Beste daraus zu machen. Erinnerung,
Modul haben nach der Aufnahme die Standardeinstellungen von
Konstruktor. Genießen Sie es, neben dem Controller und der Schnittstelle zu sein
Jeedom, um Ihr neues Modul richtig zu konfigurieren. Es wird auch mehr sein
Einfach, das Modul zu aktivieren, um die unmittelbaren Auswirkungen der Änderung zu sehen.
Einige Modul verfügen über eine spezielle Jeedom-Dokumentation
Hilfe bei verschiedenen Parametern sowie empfohlenen Werten.

Testen Sie Ihr Modul, validieren Sie Informations- und Statusrückmeldungen
und mögliche Aktionen im Fall eines Aktuators.

Während von Interviews suchte Ihr neues Modul nach seinen Nachbarn.
Die Modul in Ihrem Netzwerk kennen Ihre jedoch noch nicht
neues Modul.

Bewegen Sie Ihr Modul an seinen endgültigen Standort. Starten Sie das Update
seiner Nachbarn und wecke ihn wieder auf.

![troubleshooting07](../.images/.troubleshooting07.png)

Wir sehen, dass er eine bestimmte Anzahl von Nachbarn sieht, aber dass die
Nachbarn sehen es nicht.

Um dieser Situation abzuhelfen, müssen Maßnahmen zur Behandlung der
Netzwerk, um alle Modul zu bitten, ihre Nachbarn zu finden.

Diese Aktion kann 24 Stunden dauern, bis Ihre Modul fertig sind
Bei eingeschalteter Batterie wird die Aktion erst beim nächsten Aufwachen ausgeführt.

![troubleshooting08](../.images/.troubleshooting08.png)

Mit der Option, das Netzwerk zweimal pro Woche zu behandeln, können Sie dies tun
Prozess ohne Ihr Zutun, es ist nützlich beim Einrichten
platziert neue Modul und oder wenn sie verschoben werden.

Keine Rückmeldung zum Batteriezustand
-------------------------------

Z-Wave-Modul senden sehr selten ihren Batteriestatus an die
Controller. Einige werden es dann bei Aufnahme nur dann tun, wenn
Dies erreicht 20% oder einen anderen kritischen Schwellenwert.

Um den Status Ihrer Batterien besser überwachen zu können, wird der Bildschirm Batterien angezeigt
Im Menü Analyse erhalten Sie einen Überblick über den Status Ihres
Batterien. Ein Benachrichtigungsmechanismus für niedrigen Batteriestand ist ebenfalls vorhanden
disponible.

Der vom Bildschirm "Batterien" zurückgegebene Wert ist der letzte im
cache.

Jede Nacht fordert das Z-Wave-Plugin jevon Modul zur Aktualisierung auf
Batteriewert. Beim nächsten Aufwachen sendund das Modul den Wert an
Jeedom, das dem Cache hinzugefügt werden soll. Also muss man normalerweise warten bis
mindestens 24 Stunden, bevor ein Wert auf dem Bildschirm Batterien angezeigt wird.

> **Tip**
>
> Es ist natürlich möglich, den Wert manuell zu aktualisieren
> Batterie über die Registerkarte Werte von Moduls und warten Sie entweder auf die nächste
> Alarm oder manuelles Aufwecken von Moduls, um a
> sofortige Genesung. Das Weckintervall von Moduls
> wird auf der Registerkarte System von Moduls definiert. Um das Leben von zu optimieren
> Bei Ihren Batterien wird empfohlen, diese Verzögerung so weit wie möglich zu platzieren. Für 4h,
> gelten 14400, 12h 43200. Einige Modul müssen
> Hören Sie regelmäßig Nachrichten von der Steuerung wie z
> Thermostate. In diesem Fall muss man an 15 Minuten oder 900 Minuten denken
> Modul ist anders, daher gibt es keine genaue Regel, dies ist der Fall
> nach Fall und Erfahrung.

> **Tip**
>
> Die Entladung einer Batterie ist nicht linear, einige Modul werden
> zeigen einen großen prozentualen Verlust in den ersten Tagen der Wette
> im Betrieb, dann wochenlang nicht zum Entleeren bewegen
> schnell einmal nach 20%.

Controller wird initialisiert
----------------------------------------

Wenn Sie den Z-Wave-Daemon starten und versuchen, ihn zu starten
Sofort ein Einschluss /. Ausschluss, riskieren Sie dies
message: \* "Der Controller wird bitte initialisiert
Versuchen Sie es in wenigen Minuten erneut"

> **Tip**
>
> Nach dem Start von Dämons wechselt der Controller zu allen
> Module, um ihr Interview zu wiederholen. Dieses Verhalten ist
> völlig normal in OpenZWave.

Wenn jedoch nach einigen Minuten (mehr als 10 Minuten), haben Sie
Trotzdem ist diese Nachricht nicht mehr normal.

Sie müssen die verschiedenen Schritte ausprobieren:

-   Stellen Sie sicher, dass die Anzeigen von Jeedom-Gesundheitsbildschirms grün leuchten.

-   Stellen Sie sicher, dass die Plugin-Konfiguration in Ordnung ist.

-   Stellen Sie sicher, dass Sie den richtigen Port für das ausgewählt haben
    ZWave-Taste.

-   Stellen Sie sicher, dass Ihre Jeedom Network-Konfiguration korrekt ist.
    (Achtung, wenn Sie eine Wiederherstellung von einer DIY-Installation zu gemacht haben
    offizielles Bild, Suffix /. Jeedom sollte nicht enthalten sein)

-   Überprüfen Sie im Plugin-Protokoll, ob ein Fehler vorliegt
    nicht auf.

-   Beobachten Sie die **Console** ZWave Plugin, um zu sehen, ob ein Fehler vorliegt
    ging nicht hoch.

-   Starten Sie den Dämon mit **Debug** schau nochmal auf die **Console** et
    Plugin-Protokolle.

-   Starten Sie Jeedom vollständig neu.

-   Stellen Sie sicher, dass Sie einen Z-Wave-Controller haben
    Razberry werden oft mit EnOcean verwechselt (Fehler während
    die Bestellung).

Wir müssen jetzt die Hardwaretests starten:

-   Der Razberry ist gut mit dem GPIO-Port verbunden.

-   USB-Strom ist ausreichend.

Wenn das Problem weiterhin besteht, setzen Sie den Controller zurück:

-   Stoppen Sie Ihr Jeedom vollständig über das Stoppmenü in der
    Benutzerprofil.

-   Trennen Sie die Stromversorgung.

-   Entfernen Sie ungefähr den USB-Dongle oder Razberry
    5 Minuten.

-   Verbinden Sie alles erneut und versuchen Sie es erneut.

Der Controller antwortund nicht mehr
----------------------------

Es werden keine Bestellungen mehr an die Modul gesendet, sondern zurückgegeben
von Staaten ging in Richtung Jeedom.

Die Controller-Nachrichtenwarteschlange ist möglicherweise voll.
Zeigen Sie den Bildschirm Z-Wave-Netzwerk an, wenn die Anzahl der ausstehenden Nachrichten nicht stimmt
qu'augmenter.

In diesem Fall müssen Sie den Demon Z-WAVE neu starten.

Wenn das Problem weiterhin besteht, müssen Sie den Controller zurücksetzen:

-   Stoppen Sie Ihr Jeedom vollständig über das Stoppmenü in der
    Benutzerprofil.

-   Trennen Sie die Stromversorgung.

-   Entfernen Sie ungefähr den USB-Dongle oder Razberry
    5 Minuten.

-   Verbinden Sie alles erneut und versuchen Sie es erneut.

Fehler bei Abhängigkeiten
---------------------------

Beim Aktualisieren können mehrere Fehler auftreten
Nebengebäude. Sie müssen das Abhängigkeitsaktualisierungsprotokoll konsultieren
um festzustellen, was genau der Fehler ist. Im Allgemeinen,
Der Fehler befindund sich am Ende von Protokolls in den letzten Zeilen.

Hier sind die möglichen Probleme und ihre möglichen Lösungen:

-   konnte mercurial - abort nicht installieren

Das mercurial-Pakund möchte nicht installiert werden, um den Start in zu korrigieren
ssh:

    sudo rm /. var /. lib /. dpkg /. info /. $ mercurial * -f
    sudo apt-gund install mercurial

-   Abhängigkeiten scheinen bei 75% blockiert zu sein

Mit 75% ist dies auch der Beginn der Kompilierung der Openzwave-Bibliothek
Openzwave Python Wrapper. Dieser Schritt ist sehr lang, wir können
Konsultieren Sie den Fortschritt jedoch über die Ansicht von Aktualisierungsprotokolls. Er
Also sei einfach geduldig.

-   Fehler beim Kompilieren der Openzwave-Bibliothek

        arm-linux-gnueabihf-gcc: interner Compilerfehler: Getötund (Programm cc1plus)
        Bitte reichen Sie einen vollständigen Fehlerbericht ein,
        gegebenenfalls mit vorverarbeiteter Quelle.
        Siehe <file:/././.usr/.share/.doc/.gcc-4.9/.README.Bugs> für Anweisungen.
        error: Befehl 'arm-linux-gnueabihf-gcc' schlug mit Exit-Status 4 fehl
        Makefile:266: Rezept für Ziel 'Build' fehlgeschlagen
        make: *** [build] Fehler 1

Dieser Fehler kann aufgrund eines Mangels an RAM-Speicher während des
compilation.

Starten Sie über die Jeedom-Benutzeroberfläche die Kompilierung von Abhängigkeiten.

Stoppen Sie diese Prozesse nach dem Start in SSH (Verbraucher in
Speicher) :

    sudo systemctl STOP cron
    sudo systemctl STOP apache2
    sudo systemctl STOP mysql

Um den Fortschritt der Zusammenstellung zu verfolgen, passen wir die
openzwave\_update-Protokolldatei.

    tail -f /. var /. www /. html /. log /. openzwave_update

Wenn die Kompilierung abgeschlossen und fehlerfrei ist, starten Sie die
Dienste, die Sie gestoppt haben

sudo systemctl Start cron sudo systemctl Start apache2 sudo systemctl
starte mysql

> **Tip**
>
> Wenn Sie noch auf Nginx sind, müssen Sie ersetzen **apache2** par
> **nginx** in Bestellungen **stop** /. **start**. Die Protokolldatei
> openzwave\_update befindund sich im Ordner:
> /. usr /. share /. Nginx /. www /. jeedom /. log .

Verwenden der Razberry-Karte auf einem Raspberry Pi 3
------------------------------------------------------

Um einen Razberry-Controller auf einem Raspberry Pi 3 zu verwenden, muss der
Der interne Bluetooth-Controller von Raspberry muss deaktiviert sein.

Fügen Sie diese Zeile hinzu:

    dtoverlay = pi3-miniuart-bt

Am Ende der Datei:

    /.boot/.config.txt

Starten Sie dann Ihre Himbeere neu.

HTTP-API
========

Das Z-Wave-Plugin bietund Entwicklern und Benutzern
eine vollständige API, um das Z-Wave-Netzwerk auf Anfrage zu betreiben
HTTP.

Sie können alle von der
REST-Server von Z-Wave-Daemons.

Die Syntax zum Aufrufen von Routen liegt in dieser Form vor:

URLs =
[http:/./.token:\#APIKEY\#@\#IP\_JEEDOM\#:\#PORTDEMON\#/.\#ROUTE\#](http:/./.token:#APIKEY#@#IP_JEEDOM#:#PORTDEMON#/.#ROUTE#)

-   \#API\_KEY \# entspricht Ihrem API-Schlüssel, spezifisch für
    Ihre Installation. Um es zu finden, gehen Sie zum Menü «
    Allgemein », puis « Administration » und « Konfiguration », en activant
    Im Expertenmodus wird dann eine API-Schlüsselzeile angezeigt.

-   \#IP\_JEEDOM \# entspricht Ihrer Jeedom-Zugriffs-URL.

-   \#PORTDEMON \# entspricht der auf der Seite angegebenen Portnummer
    Standardmäßig Konfiguration von Z-Wave-Plugins: 8083.

-   \#ROUTE \# entspricht der Straße auf dem auszuführenden REST-Server.

Um alle Routen zu kennen, beziehen Sie sich bitte
[Github](https:/./.github.com/.jeedom/.plugin-openzwave) von Z-WAVE Plugins.

Example: So pingen Sie die Knoten-Identifikation 2

URLs =
http:/./.token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/.ZWaveAPI/.Run/.devices\[2\].TestNode()

# FAQ

> **Ich erhalte die Fehlermeldung "Nicht genügend Speicherplatz im Stream-Puffer"**
>
> Leider handelt es sich bei diesem Fehler um Hardware, es gibt nichts, was wir tun können, und wir suchen derzeit nach Möglichkeiten, um im Falle dieses Fehlers einen NeuStart von Dämons zu erzwingen (häufig ist es jedoch auch erforderlich, den Schlüssel 5 Minuten lang abzuziehen, damit er erneut gestartund wird).
