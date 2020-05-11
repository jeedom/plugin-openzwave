# OpenZWave Plugin

Dieses Plugin ermöglicht die Nutzung von Z-Wave-Modulen über die OpenZwave-Bibliothek.

# Introduction

Z-Wave kommuniziert mit Low-Power-Funktechnologie im Frequenzband 868,42 MHz. Es wurde speziell für Hausautomationsanwendungen entwickelt. Das Z-Wave-Funkprotokoll ist für den Austausch mit geringer Bandbreite (zwischen 9 und 40 kbit / s) zwischen Geräten mit Batterie oder Netzstrom optimiert.

Z-Wave arbeitet nach Regionen im Sub-Gigahertz-Frequenzbereich (868 MHz in Europa, 908 MHz in den USA und andere Frequenzen gemäß den ISM-Bändern der Regionen).. Die theoretische Reichweite beträgt etwa 30 Meter in Innenräumen und 100 Meter im Freien. Das Z-Wave-Netzwerk verwendet Mesh-Technologie, um die Reichweite und Zuverlässigkeit zu erhöhen. Z-Wave lässt sich problemlos in elektronische Produkte mit geringem Stromverbrauch integrieren, einschließlich batteriebetriebener Geräte wie Fernbedienungen, Rauchmelder und Sicherheitssensoren.

Der Z-Wave + bringt bestimmte Verbesserungen, einschließlich einer besseren Reichweite, und verbessert unter anderem die Lebensdauer der Batterien. Volle Abwärtskompatibilität mit dem Z-Wave.

## Mit anderen drahtlosen Signalquellen zu beachtende Entfernungen

Funkempfänger müssen in einem Mindestabstand von 50 cm zu anderen Funkquellen aufgestellt werden.

Beispiele für Radioquellen:

-   Ordinateurs
-   Mikrowellengeräte
-   Elektronische Transformatoren
-   Audio- und Videogeräte
-   Vorkopplungsvorrichtungen für Leuchtstofflampen

> **Tip**
>
> Wenn Sie einen USB-Controller (Z-Stick) haben, wird empfohlen, ihn mit einem einfachen USB-Verlängerungskabel von beispielsweise 1 m von der Box zu entfernen.

Der Abstand zwischen anderen drahtlosen Sendern wie schnurlosen Telefonen oder Radio-Audioübertragungen sollte mindestens 3 Meter betragen. Die folgenden Funkquellen sollten berücksichtigt werden :

-   Störung durch Schalter von Elektromotoren
-   Störungen durch defekte elektrische Geräte
-   Störungen durch HF-Schweißgeräte
-   medizinische Behandlungsgeräte

## Effektive Wandstärke

Die Positionen der Module müssen so gewählt werden, dass die direkte Verbindungsleitung nur über einen sehr kurzen Abstand durch das Material (eine Wand) funktioniert, um eine Dämpfung so weit wie möglich zu vermeiden..

![introduction01](../images/introduction01.png)

Metallteile des Gebäudes oder der Möbel können elektromagnetische Wellen blockieren.

## Vernetzung und Routing

Netz-Z-Wave-Knoten können Nachrichten senden und wiederholen, die sich nicht in direkter Reichweite des Controllers befinden. Dies ermöglicht eine größere Flexibilität der Kommunikation, selbst wenn keine direkte drahtlose Verbindung besteht oder wenn eine Verbindung aufgrund einer Änderung im Raum oder Gebäude vorübergehend nicht verfügbar ist.

![introduction02](../images/introduction02.png)

Der Controller **Id 1** kann direkt mit den Knoten 2, 3 und 4 kommunizieren. Knoten 6 befindet sich außerhalb seiner Funkreichweite, befindet sich jedoch im Funkabdeckungsbereich von Knoten 2. Daher kann die Steuerung über Knoten 2 mit Knoten 6 kommunizieren. Auf diese Weise wird der Pfad der Steuerung über Knoten 2 zu Knoten 6 als Route bezeichnet. Falls die direkte Kommunikation zwischen Knoten 1 und Knoten 2 blockiert ist, gibt es noch eine weitere Option zur Kommunikation mit Knoten 6, wobei Knoten 3 als weiterer Signalverstärker verwendet wird.

Es wird deutlich, dass je mehr Sektorknoten Sie haben, desto mehr Routing-Optionen und desto mehr Netzwerkstabilität.. Das Z-Wave-Protokoll kann Nachrichten über bis zu vier Wiederholungsknoten weiterleiten. Dies ist ein Kompromiss zwischen der Größe des Netzwerks, der Stabilität und der maximalen Dauer einer Nachricht..

> **Tip**
>
> Es wird dringend empfohlen, zu Beginn der Installation ein Verhältnis zwischen Sektorknoten und Knoten bei Batterien von 2/3 zu verwenden, um ein gutes Netzwerknetz zu erhalten. Bevorzugen Sie Mikromodule gegenüber intelligenten Steckern. Die Mikromodule befinden sich an einem endgültigen Ort und werden nicht getrennt. Sie haben im Allgemeinen auch eine bessere Reichweite. Ein guter Anfang ist die Beleuchtung der öffentlichen Bereiche. Auf diese Weise können Sie die Sektormodule an strategischen Standorten in Ihrem Zuhause ordnungsgemäß verteilen. Dann können Sie beliebig viele Module zum Stapel hinzufügen, wenn Ihre Basisrouten gut sind.

> **Tip**
>
> Die **Netzwerkdiagramm** sowie die **Routing-Tabelle** Mit dieser Option können Sie die Qualität Ihres Netzwerks anzeigen.

> **Tip**
>
> Es gibt Repeater-Module, um Bereiche zu füllen, in denen kein Sektormodul nützlich ist.

## Eigenschaften von Z-Wave-Geräten

|  | Nachbarn | Straße | Mögliche Funktionen |
|---------------------|:------------------------:|:--------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------:|
| Controller | Kennt alle Nachbarn | Hat Zugriff auf die vollständige Routing-Tabelle | Kann mit allen Geräten im Netzwerk kommunizieren, wenn ein Kanal vorhanden ist |
| Sklave | Kennt alle Nachbarn | Hat keine Informationen in der Routing-Tabelle | Kann nicht auf den Knoten antworten, von dem die Nachricht empfangen wurde. Daher können keine unerwünschten Nachrichten gesendet werden |
| Sklaven weiterleiten | Kennt alle seine Nachbarn | Mit teilweiser Kenntnis der Routing-Tabelle | Kann auf den Knoten antworten, von dem die Nachricht empfangen wurde, und kann unerwünschte Nachrichten an eine Reihe von Knoten senden |

Zusammenfassend::

-   Jedes Z-Wave-Gerät kann Nachrichten empfangen und bestätigen
-   Les contrôleurs peuvent envoyer des messages à tous les nœuds du réseau, sollicités oder non « Die maître peut parler quand il veut und à qui il veut »
-   Les esclaves ne peuvent pas envoyer des messages non sollicités, mais seulement une réponse aux demandes «L'esclave ne parle que si on le lui demande »
-   Les esclaves de routage peuvent répondre à des demandes und ils sont autorisés à envoyer des messages non sollicités à certains nœuds que le contrôleur a prédéfini « L'esclave est toujours un esclave, mais sur autorisation, il peut parler »

# Plugin Konfiguration

Nach dem Herunterladen des Plugins müssen Sie es nur noch aktivieren und konfigurieren.

![configuration01](../images/configuration01.png)

Nach der Aktivierung sollte der Dämon starten. Das Plugin ist mit Standardwerten vorkonfiguriert. Sie haben normalerweise nichts mehr zu tun. Sie können jedoch die Konfiguration ändern.

## Nebengebäude

In diesem Teil können Sie die Abhängigkeiten überprüfen und installieren, die für das ordnungsgemäße Funktionieren des Zwave-Plugins erforderlich sind (sowohl lokal als auch remote, hier lokal). ![Konfiguration02](../images/configuration02.png)

-   Ein Statut **OK** bestätigt, dass Abhängigkeiten erfüllt sind.
-   Wenn der Status ist **NOK**, Abhängigkeiten müssen über die Schaltfläche neu installiert werden ![Konfiguration03](../images/configuration03.png)

> **Tip**
>
> Das Aktualisieren von Abhängigkeiten kann je nach Hardware mehr als 20 Minuten dauern. Der Fortschritt wird in Echtzeit und in einem Protokoll angezeigt **Openzwave\_update** ist zugänglich.

> **Important**
>
> Das Aktualisieren von Abhängigkeiten darf normalerweise nur durchgeführt werden, wenn der Status lautet **NOK**, Es ist jedoch möglich, bestimmte Probleme zu lösen und die Installation von Abhängigkeiten zu wiederholen.

> **Tip**
>
> Wenn Sie sich im Remote-Modus befinden, können die Abhängigkeiten des lokalen Dämons NOK sein. Dies ist völlig normal.

## Dämon

In diesem Teil können Sie den aktuellen Status der Dämonen überprüfen und deren automatische Verwaltung konfigurieren.. ![Konfiguration04](../images/configuration04.png) Der lokale Dämon und alle deportierten Dämonen werden mit ihren unterschiedlichen Informationen angezeigt

-   Die **Statut** zeigt an, dass der Dämon gerade läuft.
-   Die **Configuration** Gibt an, ob die Konfiguration des Dämons gültig ist.
-   Die Schaltfläche **(Re) Anfang** Ermöglicht das Erzwingen des Neustarts des Plugins im normalen Modus oder das erstmalige Starten.
-   Die Schaltfläche **Verhaftet**, Nur sichtbar, wenn die automatische Verwaltung deaktiviert ist, zwingt den Dämon zum Stoppen.
-   Die **Automatische Verwaltung** ermöglicht Jeedom, den Daemon beim Start von Jeedom automatisch zu starten und ihn im Falle eines Problems neu zu starten.
-   Die **Letzter Start** ist, wie sein Name das Datum des letzten bekannten Starts des Dämons angibt.

## Log

In diesem Teil können Sie die Protokollebene auswählen und deren Inhalt einsehen..

![configuration05](../images/configuration05.png)

Wählen Sie die Ebene aus und speichern Sie sie. Der Dämon wird dann mit den ausgewählten Anweisungen und Traces neu gestartet.

Das Level **Debug** oder **Info** kann nützlich sein, um zu verstehen, warum der Dämon einen Wert pflanzt oder nicht.

> **Important**
>
> Im Modus **Debug** Der Dämon ist sehr ausführlich. Es wird empfohlen, diesen Modus nur zu verwenden, wenn Sie ein bestimmtes Problem diagnostizieren müssen. Es wird nicht empfohlen, den Dämon laufen zu lassen **Debug** dauerhaft, wenn wir eine verwenden **SD-Card**. Vergessen Sie nach dem Debug nicht, zu einer niedrigeren Ebene wie der Ebene zurückzukehren **Error** das geht nur auf mögliche fehler zurück.

## Configuration

In diesem Teil können Sie die allgemeinen Parameter des Plugins konfigurieren ![Konfiguration06](../images/configuration06.png)

-   **Allgemein** :
    -   **Ausgeschlossene Geräte automatisch löschen** :Mit der Option Ja können Sie Geräte löschen, die vom Z-Wave-Netzwerk ausgeschlossen sind. Mit der Option Nein können Sie die Geräte in Jeedom behalten, auch wenn sie aus dem Netzwerk ausgeschlossen wurden. Die Ausrüstung
        muss dann manuell gelöscht oder durch Zuweisen einer neuen Z-Wave-ID wiederverwendet werden, wenn Sie vom Hauptcontroller migrieren.
    -   **Wenden Sie den empfohlenen Konfigurationssatz für die Aufnahme an** : Option zum direkten Anwenden des vom Jeedom-Team empfohlenen Konfigurationssatzes zur Aufnahme (empfohlen)
    -   **Deaktivieren Sie die Hintergrundaktualisierung der Laufwerke** : Bitten Sie nicht um eine Aktualisierung der Laufwerke im Hintergrund.
    -   **Zyklus (e)** : ermöglicht es, die Häufigkeit von Aufzügen zur Freiheit zu definieren.
    -   **Z-Wave-Schlüsselanschluss** : Der USB-Anschluss, an den Ihre Z-Wave-Schnittstelle angeschlossen ist. Wenn Sie den Razberry verwenden, haben Sie je nach Ihrer Architektur (RPI oder Jeedomboard) die 2 Möglichkeiten am Ende der Liste.
    -   **Server-Port** (gefährliche Änderung, muss auf allen Z-Wave Remote Jeedoms den gleichen Wert haben) : Ermöglicht das Ändern des internen Kommunikationsports des Dämons.
    -   **Backups** : ermöglicht die Verwaltung von Sicherungen der Netzwerktopologiedatei (siehe unten)
    -   **Module konfigurieren** : ermöglicht die manuelle Wiederherstellung der OpenZWave-Konfigurationsdateien mit den Parametern der Module sowie der Definition der Befehle der Module für deren Verwendung.

        > **Tip**
        >
        > Modulkonfigurationen werden jede Nacht automatisch abgerufen.

        > **Tip**
        >
        > Ein Neustart des Daemons nach dem Aktualisieren der Modulkonfigurationen ist nutzlos.

        > **Important**
        >
        > Wenn Sie ein nicht erkanntes Modul haben und gerade ein Konfigurationsupdate angewendet wurde, können Sie die Wiederherstellung von Modulkonfigurationen manuell starten.

Sobald die Konfigurationen abgerufen wurden, abhängig von den vorgenommenen Änderungen:

-   Für ein neues Modul ohne Konfiguration oder Steuerung : Schließen Sie das Modul aus und schließen Sie es erneut ein.
-   Für ein Modul, für das nur die Parameter aktualisiert wurden : Starten Sie die Regeneration der Knotenerkennung über die Registerkarte Aktionen des Moduls (das Plugin muss neu gestartet werden)..
-   Pour un module dont le « mapping » de commandes a été corrigé : die Lupe an den Bedienelementen siehe unten.

    > **Tip**
    >
    > Im Zweifelsfall wird empfohlen, das Modul auszuschließen und erneut einzuschließen.

Vergiss es nicht ![Konfiguration08](../images/configuration08.png) wenn Sie eine Änderung vornehmen.

> **Important**
>
> Wenn Sie Ubuntu verwenden : Damit der Daemon funktioniert, muss Ubuntu 15 vorhanden sein.04 (niedrigere Versionen haben einen Fehler und der Daemon kann nicht gestartet werden). Seien Sie vorsichtig, wenn Sie von 14 aktualisieren.04 es dauert einmal in 15.04 Starten Sie die Installation von Abhängigkeiten neu.

> **Important**
>
> Auswahl des Z-Wave-Schlüsselanschlusses im automatischen Erkennungsmodus, **Auto**, funktioniert nur für USB-Dongles.

## Mobiles Panel

![configuration09](../images/configuration09.png)

Ermöglicht das Anzeigen oder Nicht-Anzeigen des mobilen Panels, wenn Sie die Anwendung auf einem Telefon verwenden.

# Gerätekonfiguration

Auf die Konfiguration der Z-Wave-Geräte kann über das Plugin-Menü zugegriffen werden :

![appliance01](../images/appliance01.png)

Unten ein Beispiel einer Z-Wave-Plugin-Seite (mit einigen Geräten) :

![appliance02](../images/appliance02.png)

> **Tip**
>
> Wie an vielen Stellen in Jeedom wird durch Platzieren der Maus ganz links ein Schnellzugriffsmenü angezeigt (Sie können es in Ihrem Profil immer sichtbar lassen)..

> **Tip**
>
> Die Schaltflächen in der obersten Zeile **Synchroniser**, **Zwave Netzwerk** und **Santé**, sind nur sichtbar, wenn Sie sich im Modus befinden **Expert**. ![Gerät03](../images/appliance03.png)

## Allgemein

Hier finden Sie die gesamte Konfiguration Ihrer Geräte :

![appliance04](../images/appliance04.png)

-   **Name der Ausrüstung** : Name Ihres Z-Wave-Moduls.
-   **Übergeordnetes Objekt** : Gibt das übergeordnete Objekt an, zu dem das Gerät gehört.
-   **Kategorie** : Gerätekategorien (es kann zu mehreren Kategorien gehören).
-   **Activer** : macht Ihre Ausrüstung aktiv.
-   **Visible** : macht es auf dem Dashboard sichtbar.
-   **Knoten-ID** : Modul-ID im Z-Wave-Netzwerk. Dies kann nützlich sein, wenn Sie beispielsweise ein fehlerhaftes Modul ersetzen möchten. Fügen Sie einfach das neue Modul hinzu, rufen Sie seine ID ab, setzen Sie es anstelle der ID des alten Moduls ein und löschen Sie schließlich das neue Modul.
-   **Module** : Dieses Feld wird nur angezeigt, wenn für Ihr Modul unterschiedliche Konfigurationstypen vorhanden sind (z. B. für Module, die Pilotdrähte herstellen können).. Hier können Sie die zu verwendende Konfiguration auswählen oder später ändern

-   **Marque** : Hersteller Ihres Z-Wave-Moduls.
-   **Configuration** : Konfigurationsfenster für Moduleinstellungen
-   **Assistant** : Es ist nur für bestimmte Module verfügbar und hilft Ihnen bei der Konfiguration des Moduls (z. B. bei der Zipato-Tastatur).
-   **Documentation** : Mit dieser Schaltfläche können Sie die Jeedom-Dokumentation zu diesem Modul direkt öffnen.
-   **Supprimer** : Ermöglicht das Löschen eines Geräts und aller dieser angehängten Befehle, ohne es aus dem Z-Wave-Netzwerk auszuschließen.

> **Important**
>
> Das Löschen von Geräten führt nicht zum Ausschluss des Moduls von der Steuerung. ![Gerät11](../images/appliance11.png) Gelöschte Geräte, die noch an den Controller angeschlossen sind, werden nach der Synchronisierung automatisch neu erstellt.

## Commandes

Nachfolgend finden Sie die Liste der Bestellungen :

![appliance05](../images/appliance05.png)

> **Tip**
>
> Abhängig von den Typen und Untertypen fehlen möglicherweise einige Optionen.

-   Der im Dashboard angezeigte Name
-   Symbol : Im Falle einer Aktion können Sie ein Symbol auswählen, um
    Anzeige auf dem Dashboard anstelle von Text
-   Bestellwert : Im Fall eines Befehls vom Typ Aktion ist sein
    value kann mit einem Befehl vom Typ info verknüpft werden
    es ist konfiguriert. Beispiel für eine Lampe ist die Intensität mit ihrer verknüpft
    Zustand, dies ermöglicht dem Widget, den tatsächlichen Zustand der Lampe zu haben.
-   Typ und Subtyp.
-   die Instanz dieses Z-Wave-Befehls (für Experten reserviert).
-   die Klasse der Z-Wave-Steuerung (Experten vorbehalten).
-   der Wertindex (für Experten reserviert).
-   die Bestellung selbst (für Experten reserviert).
-   "Statusrückmeldungswert "und" Dauer vor Statusrückmeldung" : ermöglicht es Jeedom anzuzeigen, dass nach einer Änderung der Informationen der Wert auf Y, X min nach der Änderung zurückkehren muss. Beispiel : Bei einem Anwesenheitsdetektor, der nur während einer Anwesenheitserkennung emittiert, ist es sinnvoll, beispielsweise 0 in Wert und 4 in Dauer einzustellen, so dass 4 min nach einer Bewegungserkennung (und wenn dann) , es gab keine neuen) Jeedom setzt den Wert der Informationen auf 0 zurück (mehr Bewegung erkannt).
-   Chronik : ermöglicht das Historisieren der Daten.
-   Anzeige : ermöglicht die Anzeige der Daten im Dashboard.
-   Umgekehrt : Ermöglicht das Invertieren des Status für Binärtypen.
-   Unit : Dateneinheit (kann leer sein).
-   Min / max : Datengrenzen (können leer sein).
-   Erweiterte Konfiguration (kleine gekerbte Räder) : Zeigt die erweiterte Konfiguration des Befehls an (Protokollierungsmethode, Widget usw.).

-   Test : Wird zum Testen des Befehls verwendet.
-   Löschen (unterschreiben -) : ermöglicht das Löschen des Befehls.

> **Important**
>
> Die Schaltfläche **Tester** Im Fall eines Befehls vom Typ Info wird das Modul nicht direkt abgefragt, sondern der im Jeedom-Cache verfügbare Wert. Der Test gibt nur dann den korrekten Wert zurück, wenn das betreffende Modul einen neuen Wert gesendet hat, der der Definition des Befehls entspricht. .

Die **loupe**, . ![](../images/appliance13.png) .

> **Important**
>
> Die **loupe** löscht bestehende Bestellungen. .

## Befehlsspiele

Einige Module verfügen über mehrere vorkonfigurierte Befehlssätze

![appliance06](../images/appliance06.png)

.

> **Important**
>
> .

## Dokumentation und Assistent

.

![appliance07](../images/appliance07.png)

Die Schaltfläche **Documentation** .

.

Die Schaltfläche **Assistant** .

## Empfohlene Konfiguration

![appliance08](../images/appliance08.png)

.

> **Tip**
>
> .

.

-   **Einstellungen** .
-   **Vereinsgruppen** für den ordnungsgemäßen Betrieb erforderlich.
-   **Weckintervall**, für Module auf Batterie.
-   Aktivierung von **manuelle Aktualisierung** .

Klicken Sie auf die Schaltfläche, um den empfohlenen Konfigurationssatz anzuwenden : **Empfohlene Konfiguration**, .

![appliance09](../images/appliance09.png)

Der Assistent aktiviert die verschiedenen Konfigurationselemente.

Eine Bestätigung des guten Fortschritts wird in Form eines Banners angezeigt

![appliance10](../images/appliance10.png)

> **Important**
>
> .

. .

![Gerät11](../images/appliance11.png)

> **Tip**
>
> .

# Konfiguration von Modulen

Hier finden Sie alle Informationen zu Ihrem Modul

![node01](../images/node01.png)

Das Fenster hat mehrere Registerkarten :

## Zusammenfassung

.

> **Tip**
>
> . .

## Valeurs

![node02](../images/node02.png)

. . Die « mapping » des commandes est entièrement basé sur ces informations.

> **Tip**
>
> Aktualisierung eines Werts erzwingen. . .

> **Tip**
>
> . .

> **Important**
>
> . . . ![Knoten16](../images/node16.png) . Wiederholen Sie dies bei Bedarf für jede Instanz.

## Einstellungen

![node03](../images/node03.png)

.

Wenn ein Parameter geändert wird, wird die entsprechende Zeile gelb, ![](../images/node04.png) .

Wenn das Modul den Parameter akzeptiert, wird die Linie transparent.

. ![](../images/node05.png)

. . .

> **Tip**
>
> . .

> **Tip**
>
> Die Bestellung **Lebenslauf von ...** .

![node06](../images/node06.png)

> **Tip**
>
> Die Bestellung **Bewerben auf ...** .

![node18](../images/node18.png)

> **Tip**
>
> Die Bestellung **Einstellungen aktualisieren** .

. ![](../images/node17.png) .

##Associations

.

![node07](../images/node07.png)

. .

. .

.

> **Tip**
>
> .

> **Tip**
>
> . Es wird allgemein genannt : **Report** oder **LifeLine**.

> **Tip**
>
> Ihr Modul hat möglicherweise keine Gruppen.

> **Tip**
>
> . .

 **Verbunden mit welchen Modulen**

![node08](../images/node08.png)

.

**Assoziationen mit mehreren Instanzen**

Einige Module unterstützen einen Klassenbefehl für Assoziationen mit mehreren Instanzen. 

![node09](../images/node09.png)

> **Important**
>
> . .

## Systeme

Registerkarte, die die Systemparameter des Moduls gruppiert.

![node10](../images/node10.png)

> **Tip**
>
> . . . ![Knoten11](../images/node11.png)

> **Tip**
>
> Die Module **Interrupteur** und **Variateur**  **SwitchAll** . . Die Bestellung **Alle ein- / ausschalten** .

## Actions

Ermöglicht das Ausführen bestimmter Aktionen für das Modul.

![node12](../images/node12.png)

.

> **Important**
>
> . Einige Aktionen sind irreversibel. .

> **Tip**
>
> Die **Regeneration der Knotenerkennung** . . .

> **Tip**
>
>  **Regeneration der Knotenerkennung**, .

![node13](../images/node13.png)

> **Tip**
>
>  **Geisterknoten entfernen** . .

![node14](../images/node14.png)

.

> **Important**
>
> Über diesen Assistenten können nur Module mit Batterie gelöscht werden.

## Statistiques

Diese Registerkarte enthält einige Kommunikationsstatistiken mit dem Knoten.

![node15](../images/node15.png)

".

# Einschluss / Ausschluss

Wenn ein Modul das Werk verlässt, gehört es keinem Z-Wave-Netzwerk an.

## Einschlussmodus

. Dieser Vorgang wird aufgerufen **Inclusion**. Geräte können auch ein Netzwerk verlassen. Dieser Vorgang wird aufgerufen **Exclusion**. .

![addremove01](../images/addremove01.png)

.

Sie können den Einschlussmodus auswählen, nachdem Sie auf die Schaltfläche geklickt haben
**Inclusion**.

![addremove02](../images/addremove02.png)

.  **Sicher**.

 **Nicht sicher**.

Einmal im Einschlussmodus : Jeedom sagt es dir.

>**Tip**
>
>'. '. .

![addremove03](../images/addremove03.png)

.

> **Tip**
>
> .

Wenn Sie erneut auf die Schaltfläche klicken, verlassen Sie den Einschlussmodus.

> **Tip**
>
>  **Module konfigurieren** . .

> **Important**
>
> .

> **Tip**
>
> Einige Module erfordern eine Aufnahme in den Modus **Sicher**, zum Beispiel für Türschlösser.

> **Tip**
>
> .

> **Tip**
>
> . . .

> **Tip**
>
> .

## Ausschlussmodus

![addremove04](../images/addremove04.png)

.

![addremove05](../images/addremove05.png)

> **Tip**
>
> .

Wenn Sie erneut auf die Schaltfläche klicken, wird der Ausschlussmodus beendet.

> **Tip**
>
> Beachten Sie, dass Sie über die mobile Oberfläche auch auf den Ausschluss zugreifen können.

> **Tip**
>
> . .

## Synchroniser

![addremove06](../images/addremove06.png)

. .  **Ausgeschlossene Geräte automatisch löschen** .

.

> **Tip**
>
> .

> **Tip**
>
>  **Gattungsname**, .

Die Schaltfläche Synchronisieren ist nur im Expertenmodus sichtbar :
![addremove07](../images/addremove07.png)

# Z-Wave-Netzwerke

![network01](../images/network01.png)

Hier finden Sie allgemeine Informationen zu Ihrem Z-Wave-Netzwerk.

![network02](../images/network02.png)

## Zusammenfassung

.

**Informations**

-   .
-   .
-   . .
-   Die Nachbarn des Controllers.

**Etat**

![network03](../images/network03.png)

Eine Reihe von Informationen über den aktuellen Status des Netzwerks, nämlich :

-   Aktueller Zustand vielleicht **Treiber initialisiert**, **Topologie geladen** oder **Ready**.
-   .  **Treiber initialisiert**.

Sobald das Netzwerk mindestens erreicht hat **Topologie geladen**, . .

> **Tip**
>
> Das Netzwerk soll funktionsfähig sein, wenn es den Status erreicht **Topologie geladen**, . .

Ein Netzwerk **Ready**, .

> **Tip**
>
>  **Ready**. . .

**Kapazitäten**

.

**Systeme**

Zeigt verschiedene Systeminformationen an.

-   Informationen zum verwendeten USB-Anschluss.
-   OpenZwave-Bibliotheksversion
-   Version der Python-OpenZwave-Bibliothek

## Actions

![network05](../images/network05.png)

. Jede Aktion wird von einer kurzen Beschreibung begleitet.

> **Important**
>
> .

> **Important**
>
> . .

> **Tip**
>
> .

## Statistiques

![network06](../images/network06.png)

.

## Netzwerkdiagramm

![network07](../images/network07.png)

.

Erklärung der Farblegende :

-   **Noir** : .
-   **Vert** : Direkte Kommunikation mit dem Controller, ideal.
-   **Blue** : .
-   **Jaune** : .
-   **Gris** : .
-   **Rouge** : .

> **Tip**
>
> Im Netzwerkdiagramm werden nur aktive Geräte angezeigt.

.

.

## Routing-Tabelle

. Diese Knoten werden Nachbarn genannt. . .

![network08](../images/network08.png)

. .

Erklärung der Farblegende :

-   **Vert** : Direkte Kommunikation mit dem Controller, ideal.
-   **Blue** : Mindestens 2 Routen mit einem Sprung.
-   **Jaune** : Weniger als 2 Routen mit einem Sprung.
-   **Gris** : .
-   **Orange** : Alle Straßen haben mehr als einen Sprung. .

> **Tip**
>
> Im Netzwerkdiagramm werden nur aktive Geräte angezeigt.

> **Important**
>
> Ein Modul, von dem angenommen wird, dass es tot ist, nimmt nicht mehr an der Vernetzung des Netzwerks teil. Es wird hier mit einem roten Ausrufezeichen in einem Dreieck markiert.

> **Tip**
>
> .

# Santé

![health01](../images/health01.png)

Dieses Fenster fasst den Status Ihres Z-Wave-Netzwerks zusammen :

![health02](../images/health02.png)

Du hast hier :

-   **Module** : .
-   **ID** : ID Ihres Moduls im Z-Wave-Netzwerk.
-   **Notification** : 
-   **Groupe** : . 
-   **Constructeur** : 
-   **Voisin** : Gibt an, ob die Liste der Nachbarn abgerufen wurde
-   **Statut** : 
-   **Batterie** : .
-   **Weckzeit** : .
-   **Gesamtpaket** : .
-   **%OK** : .
-   **Temporisation** : Zeigt die durchschnittliche Paketversandverzögerung in ms an.
-   **Letzte Benachrichtigung** : .
    -   .
    -   Und zeigt an, ob ein Knoten nicht wie erwartet aufgewacht ist.
-   **Ping** : .

> **Important**
>
> .

Dem Namen des Moduls können ein oder zwei Bilder folgen:

![health04](../images/health04.png) Modules supportant la COMMAND\._CLASS\._ZWAVE\._PLUS\._INFO

![health05](../images/health05.png) Modules supportant la COMMAND\._CLASS\._SECURITY und securisé.

![health06](../images/health06.png) Modules supportant la COMMAND\._CLASS\._SECURITY und non Sicher.

![health07](../images/health07.png) Modul FLiRS, routeurs esclaves (modules à piles) à écoute fréquente.

> **Tip**
>
> .

> **Tip**
>
> .

> **Tip**
>
> .  **NoOperation** .

> **Tip**
>
> . .

> **Tip**
>
> 

> **Tip**
>
> .

> **Tip**
>
> . . .

![health03](../images/health03.png)

> **Tip**
>
>  **Gattungsname**, .

> **Tip**
>
>  **Unknown**, .  **NOK** in der Konstruktorspalte. .

## Interviewstatus

Schritt des Interviewens eines Moduls nach dem Starten des Daemons.

-   **None** Initialisierung des Knotensuchprozesses.
-   **ProtocolInfo** .
-   **Probe** Pingen Sie das Modul an, um festzustellen, ob es wach ist.
-   **WakeUp** .
-   **ManufacturerSpecific1** .
-   **NodeInfo** Informationen zur Unterstützung unterstützter Befehlsklassen abrufen.
-   **NodePlusInfo** Rufen Sie ZWave + -Informationen zur Unterstützung unterstützter Befehlsklassen ab.
-   **SecurityReport** Rufen Sie die Liste der Auftragsklassen ab, für die Sicherheit erforderlich ist.
-   **ManufacturerSpecific2** Rufen Sie den Namen des Herstellers und die Produktkennungen ab.
-   **Versions** Versionsinformationen abrufen.
-   **Instances** Informationen zur Befehlsklasse für mehrere Instanzen abrufen.
-   **Static** Statische Informationen abrufen (ändert sich nicht).
-   **CacheLoad** .
-   **Associations** Informationen zu Assoziationen abrufen.
-   **Neighbors** Rufen Sie die Liste der benachbarten Knoten ab.
-   **Session** Sitzungsinformationen abrufen (Änderungen selten).
-   **Dynamic** .
-   **Configuration** .
-   **Complete** Der Interviewprozess für diesen Knoten ist abgeschlossen.

## Notification

Details zu Benachrichtigungen, die von Modulen gesendet werden

-   **Completed** Aktion erfolgreich abgeschlossen.
-   **Timeout** Verzögerungsbericht beim Senden einer Nachricht gemeldet.
-   **NoOperation** .
-   **Awake** Melden Sie, wenn ein Knoten gerade aufgewacht ist
-   **Sleep** Melden Sie, wenn ein Knoten eingeschlafen ist.
-   **Dead** Melden Sie, wenn ein Knoten als tot angenommen wird.
-   **Alive** Bericht, wenn ein Knoten neu gestartet wird.

# Backups

. Dies ist Ihre zwcfgxxx-Datei..  :

-   . 
-   
-   Löschen Sie eine Sicherung

![backup01](../images/backup01.png)

# Aktualisieren Sie OpenZWave

. :

![update01](../images/update01.png)

> **Tip**
>
> .

Jeedom sollte das Abhängigkeitsupdate selbst starten, wenn das Plugin dies für richtig hält **NOK**. Diese Validierung erfolgt nach 5 Minuten.

Die Dauer dieses Vorgangs kann je nach System variieren (bis zu mehr als 1 Stunde bei Himbeer-Pi).

Sobald die Aktualisierung der Abhängigkeiten abgeschlossen ist, wird der Dämon nach der Validierung von Jeedom automatisch neu gestartet. Diese Validierung erfolgt nach 5 Minuten.

> **Tip**
>
> Für den Fall, dass die Aktualisierung der Abhängigkeiten nicht abgeschlossen ist, konsultieren Sie bitte das Protokoll **Openzwave\_update** Wer sollte Sie über das Problem informieren.

# Liste kompatibler Module

Sie finden die Liste der kompatiblen Module
[hier](https://doc.jeedom.com/de_DE/zwave/equipement.compatible)

# Fehlerbehebung und Diagnose

## Mein Modul wird nicht erkannt oder enthält keine Produkt- und Typkennungen

![troubleshooting01](../images/troubleshooting01.png)

Starten Sie die Regeneration der Knotenerkennung auf der Registerkarte Aktionen des Moduls.

Wenn Sie in diesem Szenario mehrere Module haben, starten Sie **Regenerieren Sie die Erkennung unbekannter Knoten** vom Bildschirm **Zwave Netzwerk** Tab **Actions**.

## Mein Modul wird vom Dead-Controller als tot angenommen

![troubleshooting02](../images/troubleshooting02.png)

Wenn das Modul noch angeschlossen und erreichbar ist, befolgen Sie die im Modulbildschirm vorgeschlagenen Lösungen.

Wenn das Modul abgebrochen wurde oder wirklich defekt ist, können Sie es mit aus dem Netzwerk ausschließen **Löschen Sie den fehlerhaften Knoten** via tab **Actions**.

Wenn das Modul repariert und ein neues Ersatzmodul geliefert wurde, können Sie es starten **Ersetzen Sie den ausgefallenen Knoten** via tab **Actions**, Wenn der Controller die Aufnahme auslöst, müssen Sie mit der Aufnahme auf dem Modul fortfahren. Die ID des alten Moduls sowie seine Befehle werden beibehalten.

## Verwendung des SwitchAll-Befehls

![troubleshooting03](../images/troubleshooting03.png)

Es ist über Ihren Controller-Knoten verfügbar. Ihr Controller sollte über die Befehle Alle einschalten und Alle ausschalten verfügen.

Wenn Ihr Controller nicht in Ihrer Modulliste angezeigt wird, starten Sie die Synchronisierung.

![troubleshooting04](../images/troubleshooting04.png)

Class Switch All Command wird im Allgemeinen auf Switches und Laufwerken unterstützt. Das Verhalten kann auf jedem Modul konfiguriert werden, das es unterstützt.

So können wir auch:

-   Deaktivieren Sie den Befehl Alle Klassen wechseln.
-   Aktivieren Sie für Ein und Aus.
-   Nur ein aktivieren.
-   Nur Aus aktivieren.

Die Auswahl der Optionen hängt vom Hersteller ab.

Sie müssen sich daher die Zeit nehmen, alle Schalter / Dimmer zu überprüfen, bevor Sie ein Szenario einrichten, wenn Sie nicht nur Lichter steuern.

## Mein Modul verfügt nicht über einen Szenen- oder Schaltflächenbefehl

![troubleshooting05](../images/troubleshooting05.png)

Sie können den Befehl im Befehlszuordnungsbildschirm hinzufügen.

Dies ist eine Bestellung **Info** in CC **0x2b** Instanz **0** commande
**Daten \ [0 \]. val**

Der Szenenmodus muss in den Moduleinstellungen aktiviert sein. Weitere Informationen finden Sie in der Dokumentation zu Ihrem Modul..

## Aktualisierungswerte erzwingen

Es ist möglich, die Anforderung zu zwingen, die Werte einer Instanz für einen bestimmten Klassenbefehl zu aktualisieren.

Es ist möglich, dies über eine http-Anfrage zu tun oder eine Bestellung im Gerätezuordnungsbildschirm zu erstellen.

![troubleshooting06](../images/troubleshooting06.png)

Dies ist eine Bestellung **Action** Wählen Sie die **CC** gewünscht für a **Instance** mit dem Befehl gegeben **data \ [0 \]. ForceRefresh ()**

Alle Instanzindizes für diesen Klassenbefehl werden aktualisiert. Die Knoten der Batterien warten auf ihr nächstes Erwachen, bevor sie die Aktualisierung ihres Werts durchführen.

Sie können die Verwendung auch per Skript verwenden, indem Sie eine http-Anforderung an den Z-Wave-REST-Server senden.
Ersetzen Sie ip\_jeedom, node\_id, instance\_id, cc\_id und index

``http://token:\.#APIKEY\.#@ip\._jeedom:8083/ZWaveAPI/Run/devicesnode\._id.instances\.[instance\._id\.].commandClasses\.[cc\._id\.].data\.[index\.].ForceRefresh()``

## Übertragen Sie die Module auf eine neue Steuerung

Aus verschiedenen Gründen müssen Sie möglicherweise alle Ihre Module auf einen neuen Hauptcontroller übertragen.

Sie entscheiden sich zu gehen **raZberry** zu einem **Z-Stick Gen5** oder weil Sie eine durchführen müssen **Reset** komplett von Hauptsteuerung.

Hier sind verschiedene Schritte, um dorthin zu gelangen, ohne Ihre wertvollen Szenarien, Widgets und den Verlauf zu verlieren:

-   1 \) Erstellen Sie ein Jeedom-Backup.
-   2 \) Denken Sie daran, Ihre Parameterwerte für jedes Modul aufzuschreiben (Screenshot). Sie gehen nach dem Ausschluss verloren.
-   3 \) Deaktivieren Sie in der Z-Wave-Konfiguration die Option "Ausgeschlossene Geräte automatisch löschen" und speichern Sie sie. Neustart des Netzwerks.
-   4a) Im Fall von a **Reset**, Setzen Sie den Hauptcontroller zurück und starten Sie das Plugin neu.
-   4b) Stoppen Sie für einen neuen Controller Jeedom, trennen Sie den alten Controller und schließen Sie den neuen an. Starten Sie Jeedom.
-   5 \) Ändern Sie für jedes Z-Wave-Gerät die ZWave-ID in **0**.
-   6 \) Öffnen Sie 2 Seiten des Z-Wave-Plugins auf verschiedenen Registerkarten.
-   7 \) (Über die erste Registerkarte) Wechseln Sie zur Konfigurationsseite eines Moduls, das Sie in den neuen Controller aufnehmen möchten.
-   8 \) (Über die zweite Registerkarte) Schließen Sie das Modul aus und schließen Sie es ein. Neue Ausrüstung wird erstellt.
-   9 \) Kopieren Sie die Z-Wave-ID des neuen Geräts und löschen Sie dieses Gerät.
-   10 \) Kehren Sie zur Registerkarte des alten Moduls (1. Registerkarte) zurück und fügen Sie die neue ID anstelle der alten ID ein.
-   11 \) Die ZWave-Parameter gingen beim Ausschluss / Einschluss verloren. Denken Sie daran, Ihre spezifischen Parameter zurückzusetzen, wenn Sie nicht die Standardwerte verwenden.
-   11 \) Wiederholen Sie die Schritte 7 bis 11 für jedes zu übertragende Modul.
-   12 \) Am Ende sollten Sie keine Ausrüstung mehr in ID 0 haben.
-   13 \) Überprüfen Sie, ob alle Module im Z-Wave-Integritätsbildschirm korrekt benannt sind. Starten Sie die Synchronisierung, wenn dies nicht der Fall ist.

## Ersetzen Sie ein fehlerhaftes Modul

So wiederholen Sie die Aufnahme eines fehlerhaften Moduls, ohne Ihre Wertszenarien, Widgets und Historien zu verlieren

Wenn angenommen wird, dass das Modul "Tot" ist" :

-   Beachten Sie (Screenshot) Ihre Parameterwerte, diese gehen nach der Aufnahme verloren.
-   Gehen Sie zur Registerkarte Aktionen des Moduls und starten Sie den Befehl "Fehlerhaften Knoten ersetzen"".
-   Der Controller befindet sich im Einschlussmodus. Fahren Sie mit der Aufnahme gemäß der Moduldokumentation fort.
-   Setzen Sie Ihre spezifischen Parameter zurück.

Wenn das Modul nicht als "tot" angesehen wird, aber dennoch zugänglich ist:

-   Deaktivieren Sie in der ZWave-Konfiguration die Option "Ausgeschlossene Geräte automatisch entfernen"".
-   Beachten Sie (Screenshot) Ihre Parameterwerte, diese gehen nach der Aufnahme verloren.
-   Schließen Sie das fehlerhafte Modul aus.
-   Gehen Sie zur Konfigurationsseite des fehlerhaften Moduls.
-   Öffnen Sie die ZWave-Plugin-Seite in einem neuen Tab.
-   Schließen Sie das Modul ein.
-   Kopieren Sie die ID des neuen Moduls und löschen Sie dieses Gerät.
-   Kehren Sie zur Registerkarte des alten Moduls zurück und fügen Sie die neue ID anstelle der alten ID ein.
-   Setzen Sie Ihre spezifischen Parameter zurück.

## Entfernen des Geisterknotens

Wenn Sie die gesamte Kommunikation mit einem Modul im Akkubetrieb verloren haben und es aus dem Netzwerk ausschließen möchten, ist der Ausschluss möglicherweise nicht erfolgreich oder der Knoten bleibt in Ihrem Netzwerk vorhanden.

Der automatische Ghost Node-Assistent ist verfügbar.

-   Gehen Sie zur Registerkarte Aktionen des zu löschenden Moduls.
-   Er wird wahrscheinlich einen Status haben **CacheLoad**.
-   Befehl starten **Geisterknoten entfernen**.
-   Das Z-Wave-Netzwerk stoppt. Der automatische Assistent ändert die Datei **zwcfg** um CC WakeUp aus dem Modul zu entfernen. Neustart des Netzwerks.
-   Schließen Sie den Modulbildschirm.
-   Öffnen Sie den Bildschirm Z-Wave Health.
-   Warten Sie, bis der Startzyklus abgeschlossen ist (Topologie geladen)..
-   Das Modul wird normalerweise als tot markiert.
-   In der nächsten Minute sollte der Knoten vom Integritätsbildschirm verschwinden.
-   Wenn Sie in der Z-Wave-Konfiguration die Option "Ausgeschlossene Geräte automatisch löschen" deaktiviert haben, müssen Sie die entsprechenden Geräte manuell löschen.

Dieser Assistent ist nur für Batteriemodule verfügbar.

## Aktionen nach der Aufnahme

Es wird empfohlen, den Einschluss mindestens 1 m vom Hauptcontroller entfernt durchzuführen, da dies sonst nicht die endgültige Position Ihres neuen Moduls ist. Nach der Aufnahme eines neuen Moduls in Ihr Netzwerk sollten Sie einige bewährte Methoden befolgen.

Sobald die Aufnahme abgeschlossen ist, müssen wir eine bestimmte Anzahl von Parametern auf unser neues Modul anwenden, um das Beste daraus zu machen.. Zur Erinnerung: Die Module haben nach der Aufnahme die Standardeinstellungen des Herstellers. Nutzen Sie die Möglichkeit, sich neben dem Jeedom-Controller und der Schnittstelle zu befinden, um Ihr neues Modul ordnungsgemäß zu konfigurieren. Es ist auch einfacher, das Modul zu aktivieren, um die unmittelbaren Auswirkungen der Änderung zu erkennen. Einige Module verfügen über eine spezielle Jeedom-Dokumentation, die Ihnen bei den verschiedenen Parametern sowie den empfohlenen Werten hilft.

Testen Sie Ihr Modul, bestätigen Sie die Rückmeldung, die Statusrückmeldung und mögliche Maßnahmen bei einem Stellantrieb.

Während des Interviews suchte Ihr neues Modul nach seinen Nachbarn. Die Module in Ihrem Netzwerk kennen Ihr neues Modul jedoch noch nicht.

Bewegen Sie Ihr Modul an seinen endgültigen Standort. Starten Sie das Update seiner Nachbarn und aktivieren Sie es erneut.

![troubleshooting07](../images/troubleshooting07.png)

Wir sehen, dass er eine bestimmte Anzahl von Nachbarn sieht, aber dass die Nachbarn ihn nicht sehen.

Um diese Situation zu beheben, muss die Aktion zur Pflege des Netzwerks gestartet werden, um alle Module aufzufordern, ihre Nachbarn zu finden.

Diese Aktion kann 24 Stunden dauern, bevor sie abgeschlossen ist. Ihre Batteriemodule führen die Aktion erst beim nächsten Aufwachen aus.

![troubleshooting08](../images/troubleshooting08.png)

Die Option, das Netzwerk zweimal pro Woche zu behandeln, ermöglicht es Ihnen, diesen Vorgang ohne Ihr Zutun durchzuführen. Dies ist nützlich, wenn Sie neue Module installieren oder verschieben.

## Keine Rückmeldung zum Batteriezustand

Z-Wave-Module senden sehr selten ihren Batteriestatus an die Steuerung. Einige tun dies beim Einschluss nur dann, wenn es 20% oder einen anderen kritischen Schwellenwert erreicht.

Um den Status Ihrer Batterien besser überwachen zu können, erhalten Sie auf dem Bildschirm Batterien im Menü Analyse einen Überblick über den Status Ihrer Batterien. Ein Benachrichtigungsmechanismus für niedrigen Batteriestand ist ebenfalls verfügbar.

Der vom Bildschirm "Batterien" zurückgegebene Wert ist der letzte im Cache bekannte Wert.

Jede Nacht fordert das Z-Wave-Plugin jedes Modul auf, den Akkuwert zu aktualisieren. Beim nächsten Aufwachen sendet das Modul den Wert an Jeedom, um ihn dem Cache hinzuzufügen. Daher müssen Sie in der Regel mindestens 24 Stunden warten, bevor Sie einen Wert auf dem Bildschirm „Batterien“ erhalten.

> **Tip**
>
> Es ist natürlich möglich, den Batteriewert manuell über die Registerkarte Werte des Moduls zu aktualisieren und dann entweder auf das nächste Aufwecken zu warten oder das Modul sogar manuell aufzuwecken, um einen sofortigen Anstieg zu erzielen. Das Aufweckintervall des Moduls wird auf der Registerkarte System des Moduls definiert. Um die Lebensdauer Ihrer Batterien zu optimieren, wird empfohlen, diese Verzögerung so lange wie möglich zu berücksichtigen.. Wenden Sie für 4 Stunden 14400, 12 Stunden 43200 an. Bestimmte Module müssen regelmäßig Nachrichten von der Steuerung abhören, z. B. Thermostate. In diesem Fall müssen Sie an 15 Minuten denken, d. H. 900. Jedes Modul ist anders, daher gibt es keine genaue Regel, es ist von Fall zu Fall und erfahrungsgemäß.

> **Tip**
>
> Die Entladung einer Batterie ist nicht linear. Einige Module weisen in den ersten Tagen nach der Inbetriebnahme einen großen prozentualen Verlust auf und bewegen sich dann wochenlang nicht, um sich nach 20% schnell zu entleeren..

## Controller wird initialisiert

Wenn Sie beim Starten des Z-Wave-Dämons versuchen, sofort einen Einschluss / Ausschluss zu starten, wird möglicherweise diese Meldung angezeigt: \* "Der Controller wird initialisiert. Bitte versuchen Sie es in einigen Minuten erneut"

> **Tip**
>
> Nach dem Start des Daemons schaltet der Controller alle Module ein, um das Interview zu wiederholen. Dieses Verhalten ist in OpenZWave völlig normal.

Wenn Sie diese Meldung jedoch nach einigen Minuten (mehr als 10 Minuten) immer noch haben, ist sie nicht mehr normal.

Sie müssen die verschiedenen Schritte ausprobieren:

-   Stellen Sie sicher, dass die Anzeigen des Jeedom-Gesundheitsbildschirms grün leuchten.
-   Stellen Sie sicher, dass die Plugin-Konfiguration in Ordnung ist.
-   Stellen Sie sicher, dass Sie den richtigen Port für den ZWave-Schlüssel ausgewählt haben.
-   Stellen Sie sicher, dass Ihre Jeedom Network-Konfiguration korrekt ist. (Achtung, wenn Sie eine DIY-Installation in Richtung des offiziellen Images wiederhergestellt haben, sollte das Suffix / jeedom dort nicht erscheinen.)
-   Überprüfen Sie im Plugin-Protokoll, ob kein Fehler gemeldet wurde.
-   Beobachten Sie die **Console** ZWave-Plugin, um festzustellen, ob kein Fehler gemeldet wurde.
-   Starten Sie den Dämon mit **Debug** schau nochmal auf die **Console** und Plugin-Protokolle.
-   Starten Sie Jeedom vollständig neu.
-   Stellen Sie sicher, dass Sie einen Z-Wave-Controller haben. Die Razberry werden häufig mit dem EnOcean verwechselt (Fehler bei der Bestellung)..

Wir müssen jetzt die Hardwaretests starten:

-   Der Razberry ist gut mit dem GPIO-Port verbunden.
-   USB-Strom ist ausreichend.

Wenn das Problem weiterhin besteht, setzen Sie den Controller zurück:

-   Stoppen Sie Ihr Jeedom vollständig über das Stoppmenü im Benutzerprofil.
-   Trennen Sie die Stromversorgung.
-   Entfernen Sie den USB-Dongle oder Razberry nach Bedarf ca. 5 Minuten.
-   Verbinden Sie alles erneut und versuchen Sie es erneut.

## Der Controller antwortet nicht mehr

Es werden keine Bestellungen mehr an die Module gesendet, aber Statusrückgaben werden an Jeedom zurückgesendet.

Die Controller-Nachrichtenwarteschlange ist möglicherweise voll. Siehe den Bildschirm Z-Wave-Netzwerk, wenn die Anzahl der ausstehenden Nachrichten nur zunimmt.

In diesem Fall müssen Sie den Demon Z-Wave neu starten.

Wenn das Problem weiterhin besteht, müssen Sie den Controller zurücksetzen:

-   Stoppen Sie Ihr Jeedom vollständig über das Stoppmenü im Benutzerprofil.
-   Trennen Sie die Stromversorgung.
-   Entfernen Sie den USB-Dongle oder Razberry nach Bedarf ca. 5 Minuten.
-   Verbinden Sie alles erneut und versuchen Sie es erneut.

## Fehler bei Abhängigkeiten

Beim Aktualisieren von Abhängigkeiten können mehrere Fehler auftreten. Überprüfen Sie das Abhängigkeitsaktualisierungsprotokoll, um festzustellen, was genau der Fehler ist. Im Allgemeinen befindet sich der Fehler in den letzten Zeilen am Ende des Protokolls.

Hier sind die möglichen Probleme und ihre möglichen Lösungen:

-   konnte mercurial - abort nicht installieren

Das mercurial-Paket möchte nicht installiert werden, um den Start in ssh zu korrigieren:

````
    sudo rm /var/lib/dpkg/info/$mercurial* -f
    sudo apt-gund install mercurial
````

-   Abhängigkeiten scheinen bei 75% blockiert zu sein

Mit 75% ist dies der Beginn der Kompilierung der Openzwave-Bibliothek sowie des Openzwave-Python-Wrappers. Dieser Schritt ist sehr lang. Sie können den Fortschritt jedoch über die Ansicht des Aktualisierungsprotokolls anzeigen.. Man muss also nur geduldig sein.

-   Fehler beim Kompilieren der Openzwave-Bibliothek

````
        arm-linux-gnueabihf-gcc: internal compiler error: Killed (program cc1plus)
        Please submit a full bug report,
        with preprocessed source if appropriate.
        See <file:///usr/share/doc/gcc-4.9/README.Bugs> for instructions.
        error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4
        Makefile:266: recipe for targund 'build' failed
        make: *** [build] Fehler 1
````

Dieser Fehler kann aufgrund eines Mangels an RAM-Speicher während der Kompilierung auftreten.

Starten Sie über die Jeedom-Benutzeroberfläche die Kompilierung von Abhängigkeiten.

Stoppen Sie diese Prozesse nach dem Start in ssh (Consumer in Memory). :

````
    sudo systemctl stop cron
    sudo systemctl stop apache2
    sudo systemctl stop mysql.
````

Um den Fortschritt der Kompilierung zu verfolgen, beenden wir die Protokolldatei openzwave\_update.

````
    tail -f /var/www/html/log/openzwave_update
````

Wenn die Kompilierung abgeschlossen und fehlerfrei ist, starten Sie die Dienste neu, die Sie gestoppt haben

````
sudo systemctl start cron sudo systemctl start apache2 sudo systemctl
start mysql
````

## Verwenden der Razberry-Karte auf einem Raspberry Pi 3

Um einen Razberry-Controller auf einem Raspberry Pi 3 zu verwenden, muss der interne Bluetooth-Controller des Raspberry deaktiviert sein.

Fügen Sie diese Zeile hinzu:

````
    dtoverlay=pi3-miniuart-bt
````

Am Ende der Datei:

````
    /boot/config.txt
````

Starten Sie dann Ihre Himbeere neu.

# HTTP-API

Das Z-Wave-Plugin bietet Entwicklern und Benutzern eine vollständige API, um das Z-Wave-Netzwerk per HTTP-Anfrage betreiben zu können.

Sie können alle vom REST-Server des Z-Wave-Dämons bereitgestellten Methoden verwenden.

Die Syntax zum Aufrufen von Routen liegt in dieser Form vor:

URLs = ``http://token:\.#APIKEY\.#@\.#IP\._JEEDOM\.#:\.#PORTDEMON\.#/\.#ROUTE\.#``

-   \.#API\._KEY\.# entspricht Ihrem API-Schlüssel, der für Ihre Installation spezifisch ist. Pour la trouver, il faut aller dans le menu « Allgemein », puis « Administration » und « Konfiguration », en activant le mode Expert, vous verrez alors une ligne Clef API.
-   \.#IP\._JEEDOM\.# entspricht Ihrer Jeedom-Zugriffs-URL.
-   \.#PORTDEMON\.# entspricht standardmäßig der auf der Konfigurationsseite des Z-Wave-Plugins angegebenen Portnummer: 8083.
-   \.#ROUTE\.# entspricht der auszuführenden Route auf dem REST-Server.

Um alle Routen zu kennen, beziehen Sie sich bitte
[Github](https://github.com/jeedom/plugin-openzwave) des Z-Wave Plugins.

Example: So pingen Sie die Knoten-ID 2

URLs = ``http://token:a1b2c3d4e5f6g7h8@192.168.0.1:8083/ZWaveAPI/Run/devices\.[2\.].TestNode()``

# FAQ

> **Ich erhalte die Fehlermeldung "Nicht genügend Speicherplatz im Stream-Puffer"**
>
> Leider handelt es sich bei diesem Fehler um Hardware, es gibt nichts, was wir tun können, und wir suchen derzeit nach Möglichkeiten, um im Falle dieses Fehlers einen Neustart des Dämons zu erzwingen (häufig ist es jedoch auch erforderlich, den Schlüssel 5 Minuten lang abzuziehen, damit er erneut gestartet wird).
