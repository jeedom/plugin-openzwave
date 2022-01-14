# OpenZWave Plugin

Dieses Plugin ermöglicht die Nutzung von Z-Wave-Modulen über die OpenZwave-Bibliothek.

# Introduction

Z-Wave kommuniziert mit Low-Power-Funktechnologie im Frequenzband 868,42 MHz. Es wurde speziell für Hausautomationsanwendungen entwickelt. Das Z-Wave-Funkprotokoll ist für den Austausch mit geringer Bandbreite (zwischen 9 und 40 kbit / s) zwischen Geräten mit Batterie oder Netzstrom optimiert.

Z-Wave arbeitet nach Regionen im Sub-Gigahertz-Frequenzbereich (868 MHz in Europa, 908 MHz in den USA und andere Frequenzen nach ISM-Bändern der Regionen)). Die theoretische Reichweite beträgt etwa 30 Meter in Innenräumen und 100 Meter im Freien. Das Z-Wave-Netzwerk verwendet Mesh-Technologie, um die Reichweite und Zuverlässigkeit zu erhöhen. Z-Wave lässt sich problemlos in elektronische Produkte mit geringem Stromverbrauch integrieren, einschließlich batteriebetriebener Geräte wie Fernbedienungen, Rauchmelder und Sicherheitssensoren.

Der Z-Wave + bringt bestimmte Verbesserungen, einschließlich einer besseren Reichweite, und verbessert unter anderem die Lebensdauer der Batterien. Volle Abwärtskompatibilität mit dem Z-Wave.

## Compatibilité

Sie finden [hier](https://compatibility.jeedom.com/index.php?v=d&p=home&plugin=openzwave) die Liste der Module, die mit dem Plugin kompatibel sind

## Mit anderen drahtlosen Signalquellen zu beachtende Entfernungen

Funkempfänger müssen in einem Mindestabstand von 50 cm zu anderen Funkquellen aufgestellt werden.

Beispiele für Radioquellen:

-   Ordinateurs
-   Mikrowellengeräte
-   Elektronische Transformatoren
-   Audio- und Videogeräte
-   Vorkopplungsvorrichtungen für Leuchtstofflampen

> **Spitze**
>
> Wenn Sie einen USB-Controller (Z-Stick) haben, wird empfohlen, ihn mit einem einfachen USB-Verlängerungskabel von beispielsweise 1 m von der Box zu entfernen.

Der Abstand zwischen anderen drahtlosen Sendern wie schnurlosen Telefonen oder Radio-Audioübertragungen sollte mindestens 3 Meter betragen. Die folgenden Funkquellen sollten berücksichtigt werden :

-   Störung durch Schalter von Elektromotoren
-   Störungen durch defekte elektrische Geräte
-   Störungen durch HF-Schweißgeräte
-   medizinische Behandlungsgeräte

## Effektive Wandstärke

Die Positionen der Module müssen so gewählt werden, dass die direkte Verbindungsleitung nur über einen sehr kurzen Abstand durch das Material (eine Wand) funktioniert, um eine Dämpfung so weit wie möglich zu vermeiden.

![introduction01](../images/introduction01.png)

Metallteile des Gebäudes oder der Möbel können elektromagnetische Wellen blockieren.

## Vernetzung und Routing

Netz-Z-Wave-Knoten können Nachrichten senden und wiederholen, die sich nicht in direkter Reichweite des Controllers befinden. Dies ermöglicht eine größere Flexibilität der Kommunikation, selbst wenn keine direkte drahtlose Verbindung besteht oder wenn eine Verbindung aufgrund einer Änderung im Raum oder Gebäude vorübergehend nicht verfügbar ist.

![introduction02](../images/introduction02.png)

Der Controller **Id 1** kann direkt mit den Knoten 2, 3 und 4 kommunizieren. Knoten 6 befindet sich außerhalb seiner Funkreichweite, befindet sich jedoch im Funkabdeckungsbereich von Knoten 2. Daher kann die Steuerung über Knoten 2 mit Knoten 6 kommunizieren. Auf diese Weise wird der Pfad der Steuerung über Knoten 2 zu Knoten 6 als Route bezeichnet. Falls die direkte Kommunikation zwischen Knoten 1 und Knoten 2 blockiert ist, gibt es noch eine weitere Option zur Kommunikation mit Knoten 6, wobei Knoten 3 als weiterer Signalverstärker verwendet wird.

Es wird deutlich, dass je mehr Sektorknoten Sie haben, desto mehr Routing-Optionen und desto mehr Netzwerkstabilität. Das Z-Wave-Protokoll kann Nachrichten über bis zu vier Wiederholungsknoten weiterleiten. Dies ist ein Kompromiss zwischen der Größe des Netzwerks, der Stabilität und der maximalen Dauer einer Nachricht.

> **Spitze**
>
> Es wird dringend empfohlen, zu Beginn der Installation ein Verhältnis zwischen Sektorknoten und Knoten bei Batterien von 2/3 zu verwenden, um ein gutes Netzwerknetz zu erhalten. Bevorzugen Sie Mikromodule gegenüber intelligenten Steckern. Die Mikromodule befinden sich an einem endgültigen Ort und werden nicht getrennt. Sie haben im Allgemeinen auch eine bessere Reichweite. Ein guter Anfang ist die Beleuchtung der öffentlichen Bereiche. Auf diese Weise können Sie die Sektormodule an strategischen Standorten in Ihrem Zuhause ordnungsgemäß verteilen. Dann können Sie beliebig viele Module zum Stapel hinzufügen, wenn Ihre Basisrouten gut sind.

> **Spitze**
>
> Die **Netzwerkdiagramm** sowie die **Routing-Tabelle** Mit dieser Option können Sie die Qualität Ihres Netzwerks anzeigen.

> **Spitze**
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

Nach der Aktivierung sollte der Dämon starten. Das Plugin ist mit Standardwerten vorkonfiguriert. Sie haben normalerweise nichts mehr zu tun. Sie können jedoch die Konfiguration ändern.

## Nebengebäude

In diesem Teil können Sie die Abhängigkeiten überprüfen und installieren, die für das ordnungsgemäße Funktionieren des Zwave-Plugins erforderlich sind (sowohl lokal als auch remote, hier lokal) ![Konfiguration02](../images/configuration02.png)

-   Ein Statut **OK** bestätigt, dass Abhängigkeiten erfüllt sind.
-   Wenn der Status ist **NOK**, Abhängigkeiten müssen über die Schaltfläche neu installiert werden ![Konfiguration03](../images/configuration03.png)

> **Spitze**
>
> Das Aktualisieren von Abhängigkeiten kann je nach Hardware mehr als 20 Minuten dauern. Der Fortschritt wird in Echtzeit und in einem Protokoll angezeigt **Openzwave\_update** ist zugänglich.

> **Wichtig**
>
> Das Aktualisieren von Abhängigkeiten darf normalerweise nur durchgeführt werden, wenn der Status lautet **NOK**, Es ist jedoch möglich, bestimmte Probleme zu lösen und die Installation von Abhängigkeiten zu wiederholen.

> **Spitze**
>
> Wenn Sie sich im Remote-Modus befinden, können die Abhängigkeiten des lokalen Dämons NOK sein. Dies ist völlig normal.

## Dämon

In diesem Teil können Sie den aktuellen Status der Dämonen überprüfen und deren automatische Verwaltung konfigurieren. ![Konfiguration04](../images/configuration04.png) Der lokale Dämon und alle deportierten Dämonen werden mit ihren unterschiedlichen Informationen angezeigt

-   Die **Status** zeigt an, dass der Dämon gerade läuft.
-   Die **Konfiguration** Gibt an, ob die Konfiguration des Dämons gültig ist.
-   Die Schaltfläche **(Neustarten** Ermöglicht das Erzwingen des Neustarts des Plugins im normalen Modus oder das erstmalige Starten.
-   Die Schaltfläche **Verhaftet**, Nur sichtbar, wenn die automatische Verwaltung deaktiviert ist, zwingt den Dämon zum Stoppen.
-   Die **Automatische Verwaltung** ermöglicht Jeedom, den Daemon beim Start von Jeedom automatisch zu starten und ihn im Falle eines Problems neu zu starten.
-   Die **Letzter Start** ist, wie sein Name das Datum des letzten bekannten Starts des Dämons angibt.

## Log

In diesem Teil können Sie die Protokollebene auswählen und deren Inhalt einsehen.

![configuration05](../images/configuration05.png)

Wählen Sie die Ebene aus und speichern Sie sie. Der Dämon wird dann mit den ausgewählten Anweisungen und Traces neu gestartet.

Das Level **Debuggen** oder **Info** kann nützlich sein, um zu verstehen, warum der Dämon einen Wert pflanzt oder nicht.

> **Wichtig**
>
> Im Modus **Debuggen** Der Dämon ist sehr ausführlich. Es wird empfohlen, diesen Modus nur zu verwenden, wenn Sie ein bestimmtes Problem diagnostizieren müssen. Es wird nicht empfohlen, den Dämon laufen zu lassen **Debuggen** dauerhaft, wenn wir eine verwenden **SD-Karte**. Vergessen Sie nach dem Debug nicht, zu einer niedrigeren Ebene wie der Ebene zurückzukehren **Fehler** das geht nur auf mögliche fehler zurück.

## Configuration

In diesem Teil können Sie die allgemeinen Parameter des Plugins konfigurieren ![Konfiguration06](../images/configuration06.png)

-   **Allgemein** :
    -   **Ausgeschlossene Geräte automatisch löschen** :Mit der Option Ja können Sie Geräte löschen, die vom Z-Wave-Netzwerk ausgeschlossen sind. Mit der Option Nein können Sie die Geräte in Jeedom behalten, auch wenn sie aus dem Netzwerk ausgeschlossen wurden. Die Ausrüstung
        muss dann manuell gelöscht oder durch Zuweisen einer neuen Z-Wave-ID wiederverwendet werden, wenn Sie vom Hauptcontroller migrieren.
    -   **Wenden Sie den empfohlenen Konfigurationssatz für die Aufnahme an** : Option zum direkten Anwenden des vom Jeedom-Team empfohlenen Konfigurationssatzes zur Aufnahme (empfohlen))
    -   **Deaktivieren Sie die Hintergrundaktualisierung der Laufwerke** : Bitten Sie nicht um eine Aktualisierung der Laufwerke im Hintergrund.
    -   **Fahrräder)** : ermöglicht es, die Häufigkeit von Aufzügen zur Freiheit zu definieren.
    -   **Z-Wave-Schlüsselanschluss** : Der USB-Anschluss, an den Ihre Z-Wave-Schnittstelle angeschlossen ist. Wenn Sie den Razberry verwenden, haben Sie je nach Ihrer Architektur (RPI oder Jeedomboard) die 2 Möglichkeiten am Ende der Liste.
    -   **Server-Port** (gefährliche Modifikation, muss auf allen Z-Wave Remote Jeedoms den gleichen Wert haben) : Ermöglicht das Ändern des internen Kommunikationsports des Dämons.
    -   **Backups** : Mit dieser Option können Sie Sicherungen der Netzwerktopologiedatei verwalten (siehe unten))
    -   **Netzwerk-Backups** : ermöglicht Ihnen die Verwaltung von Controller-Backups. Sie können ein Backup eines Schlüssels erstellen, ein Backup wiederherstellen, herunterladen oder hochladen. Um einen Bakcup zu erstellen, müssen Sie einen Namen vergeben, den richtigen Port für den Controller auswählen und auf Backup starten klicken. Der Vorgang kann einige Minuten dauern. Um ein Backup wiederherzustellen, wählen Sie einfach den Controller-Port aus, wählen Sie das wiederherzustellende Backup aus dem Dropdown-Menü und klicken Sie auf Backup wiederherstellen.  Mit der Download-Schaltfläche können Sie ein Backup auf Ihren PC herunterladen. Mit der Schaltfläche "Backup hinzufügen" können Sie ein Backup auf Jeedom hochladen. Der Löschknopf wann erlaubt es, wie der Name schon sagt, das Löschen eines Backups.
    -   **Module konfigurieren** : ermöglicht die manuelle Wiederherstellung der OpenZWave-Konfigurationsdateien mit den Parametern der Module sowie der Definition der Befehle der Module für deren Verwendung.

        > **Spitze**
        >
        > Modulkonfigurationen werden jede Nacht automatisch abgerufen.

        > **Spitze**
        >
        > Ein Neustart des Daemons nach dem Aktualisieren der Modulkonfigurationen ist nutzlos.

        > **Wichtig**
        >
        > Wenn Sie ein nicht erkanntes Modul haben und gerade ein Konfigurationsupdate angewendet wurde, können Sie die Wiederherstellung von Modulkonfigurationen manuell starten.

Sobald die Konfigurationen abgerufen wurden, abhängig von den vorgenommenen Änderungen:

-   Für ein neues Modul ohne Konfiguration oder Steuerung : Schließen Sie das Modul aus und schließen Sie es erneut ein.
-   Für ein Modul, für das nur die Parameter aktualisiert wurden : Starten Sie die Regeneration der Knotenerkennung über die Registerkarte Aktionen des Moduls (das Plugin muss neu gestartet werden).
-   Pour un module dont le « mapping » de commandes a été corrigé : die Lupe an den Bedienelementen siehe unten.

    > **Spitze**
    >
    > Im Zweifelsfall wird empfohlen, das Modul auszuschließen und erneut einzuschließen.

Vergiss es nicht ![Konfiguration08](../images/configuration08.png) wenn Sie eine Änderung vornehmen.

> **Wichtig**
>
> Wenn Sie Ubuntu verwenden : Damit der Daemon funktioniert, muss Ubuntu 15 vorhanden sein.04 (niedrigere Versionen haben einen Fehler und der Daemon kann nicht gestartet werden). Seien Sie vorsichtig, wenn Sie von 14 aktualisieren.04 es dauert einmal in 15.04 Starten Sie die Installation von Abhängigkeiten neu.

> **Wichtig**
>
> Auswahl des Z-Wave-Schlüsselanschlusses im automatischen Erkennungsmodus, **Auto**, funktioniert nur für USB-Dongles.

## Mobiles Panel

![configuration09](../images/configuration09.png)

Ermöglicht das Anzeigen oder Nicht-Anzeigen des mobilen Panels, wenn Sie die Anwendung auf einem Telefon verwenden.

# Gerätekonfiguration

Auf die Konfiguration der Z-Wave-Geräte kann über das Plugin-Menü zugegriffen werden :

![appliance01](../images/appliance01.png)

Unten ein Beispiel für eine Z-Wave-Plugin-Seite (mit einigen Geräten dargestellt) :

![appliance02](../images/appliance02.png)

> **Spitze**
>
> Wie an vielen Stellen in Jeedom wird durch Platzieren der Maus ganz links ein Schnellzugriffsmenü angezeigt (Sie können es in Ihrem Profil immer sichtbar lassen).

> **Spitze**
>
> Die Schaltflächen in der obersten Zeile **Synchronize**, **Zwave Netzwerk** und **Gesundheit**, sind nur sichtbar, wenn Sie sich im Modus befinden **Experte**. ![Gerät03](../images/appliance03.png)

## Allgemein

Hier finden Sie die gesamte Konfiguration Ihrer Geräte :

![appliance04](../images/appliance04.png)

-   **Name der Ausrüstung** : Name Ihres Z-Wave-Moduls.
-   **Übergeordnetes Objekt** : Gibt das übergeordnete Objekt an, zu dem das Gerät gehört.
-   **Kategorie** : Gerätekategorien (es kann zu mehreren Kategorien gehören).
-   **Aktivieren** : macht Ihre Ausrüstung aktiv.
-   **Sichtbar** : macht es auf dem Dashboard sichtbar.
-   **Knoten-ID** : Modul-ID im Z-Wave-Netzwerk. Dies kann nützlich sein, wenn Sie beispielsweise ein fehlerhaftes Modul ersetzen möchten. Fügen Sie einfach das neue Modul hinzu, rufen Sie seine ID ab, setzen Sie es anstelle der ID des alten Moduls ein und löschen Sie schließlich das neue Modul.
-   **Modul** : Dieses Feld wird nur angezeigt, wenn es unterschiedliche Konfigurationstypen für Ihr Modul gibt (z. B. für Module, die Pilotdrähte herstellen können). Hier können Sie die zu verwendende Konfiguration auswählen oder später ändern

-   **Machen Sie** : Hersteller Ihres Z-Wave-Moduls.
-   **Konfiguration** : Konfigurationsfenster für Moduleinstellungen
-   **Assistent** : Es ist nur für bestimmte Module verfügbar und hilft Ihnen bei der Konfiguration des Moduls (z. B. bei der Zipato-Tastatur))
-   **Dokumentation** : Mit dieser Schaltfläche können Sie die Jeedom-Dokumentation zu diesem Modul direkt öffnen.
-   **Löschen** : Ermöglicht das Löschen eines Geräts und aller dieser angehängten Befehle, ohne es aus dem Z-Wave-Netzwerk auszuschließen.

> **Wichtig**
>
> Das Löschen von Geräten führt nicht zum Ausschluss des Moduls von der Steuerung. ![Gerät11](../images/appliance11.png) Gelöschte Geräte, die noch an den Controller angeschlossen sind, werden nach der Synchronisierung automatisch neu erstellt.

## Commandes

Nachfolgend finden Sie die Liste der Bestellungen :

![appliance05](../images/appliance05.png)

> **Spitze**
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
-   die Klasse der Z-Wave-Steuerung (für Experten reserviert).
-   der Wertindex (für Experten reserviert).
-   die Bestellung selbst (für Experten reserviert).
-   "Statusrückmeldungswert "und" Dauer vor Statusrückmeldung" : ermöglicht es Jeedom anzuzeigen, dass nach einer Änderung der Informationen der Wert auf Y, X min nach der Änderung zurückkehren muss. Beispiel : Bei einem Anwesenheitsdetektor, der nur während einer Anwesenheitserkennung emittiert, ist es sinnvoll, beispielsweise 0 in Wert und 4 in Dauer einzustellen, so dass 4 min nach einer Bewegungserkennung (und wenn dann) , es gab keine neuen) Jeedom setzt den Wert der Informationen auf 0 zurück (keine Bewegung mehr erkannt).
-   Chronik : ermöglicht das Historisieren der Daten.
-   Anzeige : ermöglicht die Anzeige der Daten im Dashboard.
-   Umgekehrt : Ermöglicht das Invertieren des Status für Binärtypen.
-   Unit : Dateneinheit (kann leer sein).
-   Min / max : Datengrenzen (können leer sein).
-   Erweiterte Konfiguration (kleine gekerbte Räder) : Zeigt die erweiterte Konfiguration des Befehls an (Protokollierungsmethode, Widget usw.)).

-   Test : Wird zum Testen des Befehls verwendet.
-   Löschen (unterschreiben -) : ermöglicht das Löschen des Befehls.

> **Wichtig**
>
> Die Schaltfläche **Test** Im Fall eines Befehls vom Typ Info wird das Modul nicht direkt abgefragt, sondern der im Jeedom-Cache verfügbare Wert. Der Test gibt nur dann den korrekten Wert zurück, wenn das betreffende Modul einen neuen Wert gesendet hat, der der Definition des Befehls entspricht. Es ist daher völlig normal, nach der Erstellung eines neuen Info-Befehls kein Ergebnis zu erhalten, insbesondere bei einem batteriebetriebenen Modul, das Jeedom selten benachrichtigt.

Die **Lupe**, Auf der Registerkarte "Allgemein" können Sie alle Befehle für das aktuelle Modul neu erstellen. ![Gerät13](../images/appliance13.png) Wenn kein Befehl vorhanden ist oder wenn die Befehle falsch sind, sollte die Lupe Abhilfe schaffen.

> **Wichtig**
>
> Die **Lupe** löscht bestehende Bestellungen. Wenn die Befehle in Szenarien verwendet wurden, müssen Sie Ihre Szenarien an den anderen Stellen korrigieren, an denen die Befehle verwendet wurden.

## Befehlsspiele

Einige Module verfügen über mehrere vorkonfigurierte Befehlssätze

![appliance06](../images/appliance06.png)

Sie können sie über die möglichen Auswahlmöglichkeiten auswählen, sofern das Modul dies zulässt.

> **Wichtig**
>
> Sie müssen vergrößern, um die neuen Befehlssätze anzuwenden.

## Dokumentation und Assistent

Für eine bestimmte Anzahl von Modulen stehen eine spezifische Hilfe für die Installation sowie Empfehlungen zu Parametern zur Verfügung.

![appliance07](../images/appliance07.png)

Die Schaltfläche **Dokumentation** bietet Zugriff auf spezifische Moduldokumentationen für Jeedom.

Bestimmte Module haben auch einen speziellen Assistenten, um die Anwendung bestimmter Parameter oder Operationen zu erleichtern.

Die Schaltfläche **Assistent** Ermöglicht den Zugriff auf den spezifischen Assistentenbildschirm des Moduls.

## Empfohlene Konfiguration

![appliance08](../images/appliance08.png)

Wenden Sie einen vom Jeedom-Team empfohlenen Konfigurationssatz an.

> **Spitze**
>
> Wenn enthalten, haben die Module die Standardparameter des Herstellers und bestimmte Funktionen sind standardmäßig nicht aktiviert.

Die folgenden Elemente werden gegebenenfalls angewendet, um die Verwendung des Moduls zu vereinfachen.

-   **Einstellungen** Ermöglicht eine schnelle Inbetriebnahme aller Modulfunktionen.
-   **Vereinsgruppen** für den ordnungsgemäßen Betrieb erforderlich.
-   **Weckintervall**, für Module auf Batterie.
-   Aktivierung von **manuelle Aktualisierung** Bei Modulen, die nicht von selbst hochgehen, ändert sich ihr Status.

Klicken Sie auf die Schaltfläche, um den empfohlenen Konfigurationssatz anzuwenden : **Empfohlene Konfiguration**, Bestätigen Sie dann die Anwendung der empfohlenen Konfigurationen.

![appliance09](../images/appliance09.png)

Der Assistent aktiviert die verschiedenen Konfigurationselemente.

Eine Bestätigung des guten Fortschritts wird in Form eines Banners angezeigt

![appliance10](../images/appliance10.png)

> **Wichtig**
>
> Batteriemodule müssen aktiviert werden, um den Konfigurationssatz anzuwenden.

Auf der Ausrüstungsseite werden Sie informiert, wenn auf dem Modul noch keine Elemente aktiviert wurden. Informationen zum manuellen Aufwecken oder Warten auf den nächsten Aufweckzyklus finden Sie in der Moduldokumentation.

![Gerät11](../images/appliance11.png)

> **Spitze**
>
> Es ist möglich, die Anwendung des empfohlenen Konfigurationssatzes automatisch zu aktivieren, wenn ein neues Modul hinzugefügt wird. Weitere Informationen finden Sie im Abschnitt Plugin-Konfiguration.

# Konfiguration von Modulen

Hier finden Sie alle Informationen zu Ihrem Modul

![node01](../images/node01.png)

Das Fenster hat mehrere Registerkarten :

## Zusammenfassung

Bietet eine vollständige Zusammenfassung Ihres Knotens mit verschiedenen Informationen, z. B. dem Status von Anforderungen, mit denen Sie wissen, ob der Knoten auf Informationen wartet, oder der Liste benachbarter Knoten.

> **Spitze**
>
> Auf dieser Registerkarte können Warnungen angezeigt werden, falls ein Konfigurationsproblem erkannt wird. Jeedom teilt Ihnen die Vorgehensweise zur Behebung mit. Verwechseln Sie eine Warnung nicht mit einem Fehler. Die Warnung ist in den meisten Fällen eine einfache Empfehlung.

## Valeurs

![node02](../images/node02.png)

Hier finden Sie alle möglichen Befehle und Zustände Ihres Moduls. Sie sind nach Instanz und Befehlsklasse geordnet und dann indexiert. Die « mapping » des commandes est entièrement basé sur ces informations.

> **Spitze**
>
> Aktualisierung eines Werts erzwingen. Die Module im Akkubetrieb aktualisieren einen Wert erst beim nächsten Aufweckzyklus. Es ist jedoch möglich, ein Modul manuell zu aktivieren, siehe die Moduldokumentation.

> **Spitze**
>
> Es ist möglich, hier mehr Bestellungen zu haben als auf Jeedom, das ist völlig normal. In Jeedom wurden die Befehle für Sie vorausgewählt.

> **Wichtig**
>
> Einige Module senden ihre Status nicht automatisch. In diesem Fall muss die manuelle Aktualisierung nach 5 Minuten für die gewünschten Werte aktiviert werden. Es wird empfohlen, die Aktualisierung automatisch zu verlassen. Der Missbrauch der manuellen Aktualisierung kann die Leistung des Z-Wave-Netzwerks stark beeinträchtigen. Verwenden Sie diese Option nur für die in der spezifischen Jeedom-Dokumentation empfohlenen Werte. ![Knoten16](../images/node16.png) Der Wertesatz (Index) der Instanz eines Klassenbefehls wird neu zusammengesetzt, wodurch die manuelle Aktualisierung des kleinsten Index der Instanz des Klassenbefehls aktiviert wird. Wiederholen Sie dies bei Bedarf für jede Instanz.

## Einstellungen

![node03](../images/node03.png)

Hier finden Sie alle Möglichkeiten zum Konfigurieren der Parameter Ihres Moduls sowie die Möglichkeit, die Konfiguration von einem bereits vorhandenen Knoten zu kopieren.

Wenn ein Parameter geändert wird, wird die entsprechende Zeile gelb, ![node04](../images/node04.png) Die Einstellung wartet darauf, angewendet zu werden.

Wenn das Modul den Parameter akzeptiert, wird die Linie transparent.

Wenn das Modul den Wert jedoch ablehnt, wird die Zeile mit dem vom Modul zurückgegebenen angewendeten Wert rot. ![node05](../images/node05.png)

Bei der Aufnahme wird ein neues Modul mit den Standardeinstellungen des Herstellers erkannt. Bei einigen Modulen sind Funktionen nicht aktiv, ohne einen oder mehrere Parameter zu ändern. Informationen zur ordnungsgemäßen Konfiguration Ihrer neuen Module finden Sie in der Dokumentation des Herstellers und in unseren Empfehlungen.

> **Spitze**
>
> Batteriemodule übernehmen Parameteränderungen nur für den nächsten Weckzyklus. Es ist jedoch möglich, ein Modul manuell zu aktivieren, siehe die Moduldokumentation.

> **Spitze**
>
> Die Bestellung **Lebenslauf von** Mit dieser Option können Sie die Konfiguration eines anderen identischen Moduls auf dem aktuellen Modul fortsetzen.

![node06](../images/node06.png)

> **Spitze**
>
> Die Bestellung **Bewerben auf** Mit dieser Option können Sie die aktuelle Modulkonfiguration auf ein oder mehrere identische Module anwenden.

![node18](../images/node18.png)

> **Spitze**
>
> Die Bestellung **Einstellungen aktualisieren** zwingt das Modul, die im Modul gespeicherten Parameter zu aktualisieren.

Wenn für das Modul keine Konfigurationsdatei definiert ist, können Sie mit einem manuellen Assistenten Parameter auf das Modul anwenden. ![Knoten17](../images/node17.png) Die Definition von Index, Wert und Größe finden Sie in der Dokumentation des Herstellers.

##Associations

Hier finden Sie die Verwaltung der Zuordnungsgruppen Ihres Moduls.

![node07](../images/node07.png)

Z-Wave-Module können andere Z-Wave-Module steuern, ohne den Controller oder Jeedom zu durchlaufen. Die Beziehung zwischen einem Steuermodul und einem anderen Modul wird als Zuordnung bezeichnet.

Um ein anderes Modul zu steuern, muss das Befehlsmodul eine Liste der Geräte führen, die die Befehlssteuerung erhalten. Diese Listen werden als Zuordnungsgruppen bezeichnet und sind immer mit bestimmten Ereignissen verknüpft (z. B. Drücken der Taste, Sensorauslöser usw.) ).

Im Falle eines Ereignisses erhalten alle in der betreffenden Zuordnungsgruppe registrierten Geräte einen Basisbefehl.

> **Spitze**
>
> In der Dokumentation des Moduls finden Sie Informationen zu den verschiedenen Gruppen möglicher Assoziationen und deren Verhalten.

> **Spitze**
>
> Die meisten Module haben eine Zuordnungsgruppe, die für die Hauptsteuerung reserviert ist. Sie wird zum Senden von Informationen an die Steuerung verwendet. Es wird allgemein genannt : **Bericht** oder **Lebenslinie**.

> **Spitze**
>
> Ihr Modul hat möglicherweise keine Gruppen.

> **Spitze**
>
> Die Änderung der Zuordnungsgruppen eines Batteriemoduls wird auf den nächsten Weckzyklus angewendet. Es ist jedoch möglich, ein Modul manuell zu aktivieren, siehe die Moduldokumentation.

Um zu wissen, welchen anderen Modulen das aktuelle Modul zugeordnet ist, klicken Sie einfach auf das Menü **Verbunden mit welchen Modulen**

![node08](../images/node08.png)

Alle Module, die das aktuelle Modul verwenden, sowie der Name der Zuordnungsgruppen werden angezeigt.

**Assoziationen mit mehreren Instanzen**

Einige Module unterstützen einen Klassenbefehl für Assoziationen mit mehreren Instanzen. Wenn ein Modul diesen CC unterstützt, kann angegeben werden, mit welcher Instanz die Zuordnung erstellt werden soll

![node09](../images/node09.png)

> **Wichtig**
>
> Einige Module müssen der Instanz 0 des Hauptcontrollers zugeordnet sein, damit sie ordnungsgemäß funktionieren. Aus diesem Grund ist der Controller mit und ohne Instanz 0 vorhanden.

## Systeme

Registerkarte, die die Systemparameter des Moduls gruppiert.

![node10](../images/node10.png)

> **Spitze**
>
> Batteriemodule werden in regelmäßigen Abständen aktiviert, die als Aufweckintervall bezeichnet werden). Das Aufweckintervall ist ein Kompromiss zwischen maximaler Akkulaufzeit und gewünschten Geräteantworten. Um die Lebensdauer Ihrer Module zu maximieren, passen Sie den Wert für das Aufweckintervall beispielsweise auf 14.400 Sekunden (4 Stunden) an. Je nach Modul und Verwendung wird sogar ein höherer Wert angezeigt. ![Knoten11](../images/node11.png)

> **Spitze**
>
> Die Module **Wechseln** und **Dimmer** kann eine spezielle Befehlsklasse mit dem Namen implementieren **SwitchAll** 0x27. Hier können Sie das Verhalten ändern. Je nach Modul stehen verschiedene Optionen zur Verfügung. Die Bestellung **Alle ein- / ausschalten** kann über Ihr Hauptsteuerungsmodul gestartet werden.

## Actions

Ermöglicht das Ausführen bestimmter Aktionen für das Modul.

![node12](../images/node12.png)

Bestimmte Aktionen sind je nach Modultyp und seinen Möglichkeiten oder nach dem aktuellen Status des Moduls aktiv, z. B. wenn es von der Steuerung als tot angenommen wird.

> **Wichtig**
>
> Verwenden Sie keine Aktionen für ein Modul, wenn Sie nicht wissen, was Sie tun. Einige Aktionen sind irreversibel. Aktionen können helfen, Probleme mit einem oder mehreren Z-Wave-Modulen zu lösen.

> **Spitze**
>
> Die **Regeneration der Knotenerkennung** Ermöglicht die Erkennung des Moduls, um die letzten Parametersätze zu akzeptieren. Diese Aktion ist erforderlich, wenn Sie darüber informiert werden, dass eine Aktualisierung der Parameter und / oder des Verhaltens des Moduls für eine ordnungsgemäße Funktion erforderlich ist. Die Regeneration der Erkennung des Knotens impliziert einen Neustart des Netzwerks, der Assistent führt ihn automatisch aus.

> **Spitze**
>
> Wenn Sie mehrere identische Module haben, die zum Ausführen des **Regeneration der Knotenerkennung**, Es ist möglich, es für alle identischen Module einmal zu starten.

![node13](../images/node13.png)

> **Spitze**
>
> Wenn ein Modul auf einem Stapel nicht mehr erreichbar ist und Sie es ausschließen möchten und der Ausschluss nicht erfolgt, können Sie es starten **Geisterknoten entfernen** Ein Assistent führt verschiedene Aktionen aus, um das sogenannte Ghost-Modul zu entfernen. Diese Aktion umfasst einen Neustart des Netzwerks und kann einige Minuten dauern.

![node14](../images/node14.png)

Nach dem Start wird empfohlen, den Modulkonfigurationsbildschirm zu schließen und das Löschen des Moduls über den Z-Wave-Integritätsbildschirm zu überwachen.

> **Wichtig**
>
> Über diesen Assistenten können nur Module mit Batterie gelöscht werden.

## Statistiques

Diese Registerkarte enthält einige Kommunikationsstatistiken mit dem Knoten.

![node15](../images/node15.png)

Kann bei Modulen interessant sein, die vom Controller als tot angenommen werden "Dead".

# Einschluss / Ausschluss

Wenn ein Modul das Werk verlässt, gehört es keinem Z-Wave-Netzwerk an.

## Einschlussmodus

Das Modul muss einem vorhandenen Z-Wave-Netzwerk beitreten, um mit den anderen Modulen dieses Netzwerks zu kommunizieren. Dieser Vorgang wird aufgerufen **Aufnahme**. Geräte können auch ein Netzwerk verlassen. Dieser Vorgang wird aufgerufen **Ausschluss**. Beide Prozesse werden vom Hauptcontroller des Z-Wave-Netzwerks initiiert.

![addremove01](../images/addremove01.png)

Mit dieser Schaltfläche können Sie in den Einschlussmodus wechseln, um Ihrem Z-Wave-Netzwerk ein Modul hinzuzufügen.

Sie können den Einschlussmodus auswählen, nachdem Sie auf die Schaltfläche geklickt haben
**Aufnahme**.

![addremove02](../images/addremove02.png)

Seit dem Erscheinen des Z-Wave + ist es möglich, den Austausch zwischen dem Controller und den Knoten zu sichern. Es wird daher empfohlen, die Einschlüsse im Modus vorzunehmen **Sicher**.

Wenn ein Modul jedoch nicht im sicheren Modus enthalten sein kann, fügen Sie es bitte im sicheren Modus hinzu **Nicht sicher**.

Einmal im Einschlussmodus : Jeedom sagt es dir.

>**Spitze**
>
>Ein "ungesichertes" Modul kann "unsichere" Module bestellen'. Ein "nicht sicheres" Modul kann kein "sicheres" Modul bestellen'. Ein "sicheres" Modul kann "nicht sichere" Module bestellen, sofern der Sender dies unterstützt.

![addremove03](../images/addremove03.png)

Nach dem Start des Assistenten müssen Sie dasselbe für Ihr Modul tun (Informationen zum Umschalten in den Einschlussmodus finden Sie in der Dokumentation).

> **Spitze**
>
> Solange Sie das Banner nicht haben, befinden Sie sich nicht im Einschlussmodus.

Wenn Sie erneut auf die Schaltfläche klicken, verlassen Sie den Einschlussmodus.

> **Spitze**
>
> Es wird empfohlen, vor der Aufnahme eines neuen Moduls, das "neu" auf dem Markt wäre, die Bestellung zu starten **Module konfigurieren** über den Plugin-Konfigurationsbildschirm. Diese Aktion stellt alle neuesten Versionen der openzwave-Konfigurationsdateien sowie die Jeedom-Befehlszuordnung wieder her.

> **Wichtig**
>
> Während einer Aufnahme wird empfohlen, dass sich das Modul in der Nähe des Hauptcontrollers oder weniger als einen Meter von Ihrem Jeedom entfernt befindet.

> **Spitze**
>
> Einige Module erfordern eine Aufnahme in den Modus **Sicher**, zum Beispiel für Türschlösser.

> **Spitze**
>
> Beachten Sie, dass Sie über die mobile Oberfläche auch Zugriff auf die Aufnahme haben. Das mobile Panel muss aktiviert sein.

> **Spitze**
>
> Wenn das Modul bereits zu einem Netzwerk gehört, befolgen Sie den Ausschlussprozess, bevor Sie es in Ihr Netzwerk aufnehmen. Andernfalls schlägt die Aufnahme dieses Moduls fehl. Es wird auch empfohlen, vor dem Einschluss einen Ausschluss auszuführen, auch wenn das Produkt neu ist.

> **Spitze**
>
> Sobald sich das Modul an seinem endgültigen Standort befindet, muss die Aktion zur Pflege des Netzwerks gestartet werden, um alle Module aufzufordern, alle Nachbarn zu aktualisieren.

## Ausschlussmodus

![addremove04](../images/addremove04.png)

Mit dieser Schaltfläche können Sie in den Ausschlussmodus wechseln. Um ein Modul aus Ihrem Z-Wave-Netzwerk zu entfernen, müssen Sie dasselbe mit Ihrem Modul tun (Informationen zum Umschalten in den Ausschlussmodus finden Sie in der Dokumentation).

![addremove05](../images/addremove05.png)

> **Spitze**
>
> Solange Sie das Banner nicht haben, befinden Sie sich nicht im Ausschlussmodus.

Wenn Sie erneut auf die Schaltfläche klicken, wird der Ausschlussmodus beendet.

> **Spitze**
>
> Beachten Sie, dass Sie über die mobile Oberfläche auch auf den Ausschluss zugreifen können.

> **Spitze**
>
> Ein Modul muss nicht von demselben Controller ausgeschlossen werden, auf dem es zuvor enthalten war. Daher wird empfohlen, vor jedem Einschluss einen Ausschluss auszuführen.

## Synchroniser

![addremove06](../images/addremove06.png)

Taste zur Synchronisation der Z-Wave-Netzwerkmodule mit Jeedom-Geräten. Die Module sind der Hauptsteuerung zugeordnet, die Geräte in Jeedom werden automatisch erstellt, wenn sie enthalten sind. Sie werden auch automatisch gelöscht, wenn sie ausgeschlossen werden **Ausgeschlossene Geräte automatisch löschen** ist aktiviert.

Wenn Sie Module ohne Jeedom eingebaut haben (erfordert einen Batteriedongle wie den Aeon-labs Z-Stick GEN5), ist nach dem Einstecken des Schlüssels eine Synchronisierung erforderlich, sobald der Daemon gestartet und betriebsbereit ist.

> **Spitze**
>
> Wenn Sie das Bild nicht haben oder Jeedom Ihr Modul nicht erkannt hat, kann diese Schaltfläche zur Korrektur verwendet werden (vorausgesetzt, das Modulinterview ist abgeschlossen).

> **Spitze**
>
> Wenn sich in Ihrer Routing-Tabelle und / oder auf dem Z-Wave-Integritätsbildschirm ein oder mehrere Module mit deren Namen befinden **Gattungsname**, Durch die Synchronisierung wird diese Situation behoben.

Die Schaltfläche Synchronisieren ist nur im Expertenmodus sichtbar :
![addremove07](../images/addremove07.png)

# Z-Wave-Netzwerke

![network01](../images/network01.png)

Hier finden Sie allgemeine Informationen zu Ihrem Z-Wave-Netzwerk.

![network02](../images/network02.png)

## Zusammenfassung

Auf der ersten Registerkarte finden Sie eine grundlegende Zusammenfassung Ihres Z-Wave-Netzwerks. Sie finden insbesondere den Status des Z-Wave-Netzwerks sowie die Anzahl der Elemente in der Warteschlange.

**Information**

-   Gibt allgemeine Informationen über das Netzwerk, das Startdatum und die Zeit, die erforderlich ist, um das Netzwerk in einen sogenannten Funktionszustand zu versetzen.
-   Die Gesamtzahl der Knoten im Netzwerk sowie die Anzahl der Knoten, die gerade schlafen.
-   Das Anforderungsintervall ist mit der manuellen Aktualisierung verbunden. Es ist im Z-Wave-Motor nach 5 Minuten voreingestellt.
-   Die Nachbarn des Controllers.

**Zustand**

![network03](../images/network03.png)

Eine Reihe von Informationen über den aktuellen Status des Netzwerks, nämlich :

-   Aktueller Zustand vielleicht **Treiber initialisiert**, **Topologie geladen** oder **Fertig**.
-   Ausgehende Warteschlange gibt die Anzahl der Nachrichten an, die in der Steuerung in der Warteschlange stehen und auf den Versand warten. Dieser Wert ist im Allgemeinen während des Netzwerkstarts hoch, wenn der Status noch aktiv ist **Treiber initialisiert**.

Sobald das Netzwerk mindestens erreicht hat **Topologie geladen**, Interne Mechanismen des Z-Wave-Servers erzwingen Aktualisierungen von Werten. Daher ist es völlig normal, dass die Anzahl der Nachrichten steigt. Dies wird schnell auf 0 zurückkehren.

> **Spitze**
>
> Das Netzwerk soll funktionsfähig sein, wenn es den Status erreicht **Topologie geladen**, Das heißt, dass alle Sektorknoten ihre Interviews abgeschlossen haben. Abhängig von der Anzahl der Module, der Batterie- / Sektorverteilung, der Auswahl des USB-Dongles und dem PC, auf dem das Z-Wave-Plugin ausgeführt wird, erreicht das Netzwerk diesen Zustand zwischen einer und fünf Minuten.

Ein Netzwerk **Fertig**, bedeutet, dass alle Sektor- und Batterieknoten ihr Interview abgeschlossen haben.

> **Spitze**
>
> Abhängig von Ihren Modulen erreicht das Netzwerk möglicherweise nie den Status von selbst **Fertig**. Fernbedienungen zum Beispiel wachen nicht von alleine auf und werden ihr Interview niemals beenden. In diesem Fall ist das Netzwerk voll funktionsfähig, und selbst wenn die Fernbedienungen das Interview noch nicht abgeschlossen haben, stellen sie ihre Funktionalität innerhalb des Netzwerks sicher.

**Kapazitäten**

Wird verwendet, um herauszufinden, ob der Controller ein primärer oder ein sekundärer Controller ist.

**Systeme**

Zeigt verschiedene Systeminformationen an.

-   Informationen zum verwendeten USB-Anschluss.
-   OpenZwave-Bibliotheksversion
-   Version der Python-OpenZwave-Bibliothek

## Actions

![network05](../images/network05.png)

Hier finden Sie alle möglichen Aktionen für Ihr gesamtes Z-Wave-Netzwerk. Jede Aktion wird von einer kurzen Beschreibung begleitet.

> **Wichtig**
>
> Bestimmte Handlungen sind wirklich riskant oder sogar irreversibel. Das Jeedom-Team kann bei unsachgemäßer Handhabung nicht zur Verantwortung gezogen werden.

> **Wichtig**
>
> Einige Module müssen in den sicheren Modus integriert werden, z. B. für Türschlösser. Die sichere Aufnahme muss über die Aktion auf diesem Bildschirm gestartet werden.

> **Spitze**
>
> Wenn eine Aktion nicht gestartet werden kann, wird sie deaktiviert, bis sie erneut ausgeführt werden kann.

## Statistiques

![network06](../images/network06.png)

Hier finden Sie allgemeine Statistiken für Ihr gesamtes Z-Wave-Netzwerk.

## Netzwerkdiagramm

![network07](../images/network07.png)

Auf dieser Registerkarte erhalten Sie eine grafische Darstellung der verschiedenen Verknüpfungen zwischen den Knoten.

Erklärung der Farblegende :

-   **Schwarz** : Der Hauptcontroller, allgemein als Jeedom dargestellt.
-   **Grün** : Direkte Kommunikation mit dem Controller, ideal.
-   **Blau** : Bei Steuerungen wie Fernbedienungen sind sie der primären Steuerung zugeordnet, haben jedoch keinen Nachbarn.
-   **Gelb** : Alle Straßen haben mehr als einen Sprung, bevor sie am Controller ankommen.
-   **Grau** : Das Interview ist noch nicht abgeschlossen, die Links werden nach Abschluss des Interviews wirklich bekannt sein.
-   **Rot** : vermutlich tot oder ohne Nachbarn, nimmt nicht / nicht mehr an der Vernetzung des Netzwerks teil.

> **Spitze**
>
> Im Netzwerkdiagramm werden nur aktive Geräte angezeigt.

Das Z-Wave-Netzwerk besteht aus drei verschiedenen Knotentypen mit drei Hauptfunktionen.

Der Hauptunterschied zwischen den drei Knotentypen besteht in ihrer Kenntnis der Netzwerkrouting-Tabelle und anschließend in ihrer Fähigkeit, Nachrichten an das Netzwerk zu senden.

## Routing-Tabelle

Jeder Knoten kann bestimmen, welche anderen Knoten in direkter Kommunikation stehen. Diese Knoten werden Nachbarn genannt. Während der Aufnahme und / oder später auf Anfrage kann der Knoten den Controller über die Liste der Nachbarn informieren. Dank dieser Informationen kann der Controller eine Tabelle erstellen, die alle Informationen zu den möglichen Kommunikationsrouten in einem Netzwerk enthält.

![network08](../images/network08.png)

Die Zeilen der Tabelle enthalten die Quellknoten und die Spalten enthalten die Zielknoten. Beziehen Sie sich auf die Legende, um die Zellenfarben zu verstehen, die die Verbindungen zwischen zwei Knoten anzeigen.

Erklärung der Farblegende :

-   **Grün** : Direkte Kommunikation mit dem Controller, ideal.
-   **Blau** : Mindestens 2 Routen mit einem Sprung.
-   **Gelb** : Weniger als 2 Routen mit einem Sprung.
-   **Grau** : Das Interview ist noch nicht abgeschlossen, wird tatsächlich aktualisiert, sobald das Interview abgeschlossen ist.
-   **Orange** : Alle Straßen haben mehr als einen Sprung. Kann Latenzen verursachen.

> **Spitze**
>
> Im Netzwerkdiagramm werden nur aktive Geräte angezeigt.

> **Wichtig**
>
> Ein Modul, von dem angenommen wird, dass es tot ist, nimmt nicht mehr an der Vernetzung des Netzwerks teil. Es wird hier mit einem roten Ausrufezeichen in einem Dreieck markiert.

> **Spitze**
>
> Sie können die Nachbaraktualisierung manuell, nach Modul oder für das gesamte Netzwerk über die in der Routing-Tabelle verfügbaren Schaltflächen starten.

# Santé

![health01](../images/health01.png)

Dieses Fenster fasst den Status Ihres Z-Wave-Netzwerks zusammen :

![health02](../images/health02.png)

Du hast hier :

-   **Modul** : Klicken Sie auf den Namen Ihres Moduls, um direkt darauf zuzugreifen.
-   **Identifikation** : ID Ihres Moduls im Z-Wave-Netzwerk.
-   **Benachrichtigung** : letzte Art des Austauschs zwischen dem Modul und der Steuerung
-   **Gruppe** : Gibt an, ob die Gruppenkonfiguration in Ordnung ist (Controller zumindest in einer Gruppe). Wenn Sie nichts haben, ist es normal, dass das Modul den Begriff der Gruppe nicht unterstützt
-   **Hersteller** : Gibt an, ob die Wiederherstellung der Modulidentifikationsinformationen in Ordnung ist
-   **Nachbar** : Gibt an, ob die Liste der Nachbarn abgerufen wurde
-   **Status** : Zeigt den Status des Modulinterviews an (Abfragephase)
-   **Batterie** : Batteriestand des Moduls (ein Netzstecker zeigt an, dass das Modul über das Stromnetz mit Strom versorgt wird).
-   **Weckzeit** : Bei Modulen mit Batterie wird die Frequenz in Sekunden angegeben, zu der das Modul automatisch aufwacht.
-   **Gesamtpaket** : Zeigt die Gesamtzahl der erfolgreich empfangenen oder an das Modul gesendeten Pakete an.
-   **% Ok** : Zeigt den Prozentsatz der erfolgreich gesendeten / empfangenen Pakete an.
-   **Zeitverzögerung** : Zeigt die durchschnittliche Paketversandverzögerung in ms an.
-   **Letzte Benachrichtigung** : Datum der letzten vom Modul empfangenen Benachrichtigung und Zeitpunkt des nächsten geplanten Aufweckens für Module, die sich im Ruhezustand befinden.
    -   Außerdem können Sie informieren, ob der Knoten seit dem Start des Dämons nicht einmal aufgeweckt wurde.
    -   Und zeigt an, ob ein Knoten nicht wie erwartet aufgewacht ist.
-   **Klingeln** : Ermöglicht das Senden einer Reihe von Nachrichten an das Modul, um dessen ordnungsgemäße Funktion zu testen.

> **Wichtig**
>
> Deaktivierte Geräte werden angezeigt, es sind jedoch keine Diagnoseinformationen vorhanden.

Dem Namen des Moduls können ein oder zwei Bilder folgen:

![health04](../images/health04.png) Modules supportant la COMMAND\._CLASS\._ZWAVE\._PLUS\._INFO

![health05](../images/health05.png) Modules supportant la COMMAND\._CLASS\._SECURITY und securisé.

![health06](../images/health06.png) Modules supportant la COMMAND\._CLASS\._SECURITY und non Sicher.

![health07](../images/health07.png) Modul FLiRS, routeurs esclaves (modules à piles) à écoute fréquente.

> **Spitze**
>
> Der Ping-Befehl kann verwendet werden, wenn das Modul als tot "DEATH" angenommen wird, um zu bestätigen, ob dies wirklich der Fall ist.

> **Spitze**
>
> Schlafende Module reagieren erst beim nächsten Aufwachen auf Ping.

> **Spitze**
>
> Timeout-Benachrichtigung bedeutet nicht unbedingt ein Problem mit dem Modul. Starten Sie einen Ping und in den meisten Fällen antwortet das Modul mit einer Benachrichtigung **NoOperation** was eine fruchtbare Rückkehr von Ping bestätigt.

> **Spitze**
>
> Die Verzögerung und% OK auf Knoten mit Batterien vor Abschluss des Interviews ist nicht signifikant. In der Tat reagiert der Knoten nicht auf die Abfragen des Controllers, ob er sich im Tiefschlaf befindet.

> **Spitze**
>
> Der Z-Wave-Server sorgt automatisch dafür, dass nach 15 Minuten Tests für die Module in Timeout gestartet werden

> **Spitze**
>
> Der Z-Wave-Server versucht automatisch, die Module, die als tot gelten, wieder zusammenzusetzen.

> **Spitze**
>
> Eine Warnung wird an Jeedom gesendet, wenn das Modul als tot angenommen wird. Sie können eine Benachrichtigung aktivieren, um so schnell wie möglich informiert zu werden. Siehe die Nachrichtenkonfiguration im Bildschirm Jeedom-Konfiguration.

![health03](../images/health03.png)

> **Spitze**
>
> Wenn sich in Ihrer Routing-Tabelle und / oder auf dem Z-Wave-Integritätsbildschirm ein oder mehrere Module mit deren Namen befinden **Gattungsname**, Durch die Synchronisierung wird diese Situation behoben.

> **Spitze**
>
> Wenn Sie in Ihrer Routing-Tabelle und / oder auf dem Z-Wave-Integritätsbildschirm ein oder mehrere Module benannt haben **Unbekannt**, Dies bedeutet, dass das Modulinterview nicht erfolgreich abgeschlossen wurde. Sie haben wahrscheinlich eine **NOK** in der Konstruktorspalte. Öffnen Sie die Details der Module, um die vorgeschlagenen Lösungen auszuprobieren (siehe Abschnitt Fehlerbehebung und Diagnose unten)).

## Interviewstatus

Schritt des Interviewens eines Moduls nach dem Starten des Daemons.

-   **Keine** Initialisierung des Knotensuchprozesses.
-   **ProtocolInfo** Rufen Sie Protokollinformationen ab, wenn dieser Knoten empfangsbereit ist (Listener), seine maximale Geschwindigkeit und seine Geräteklassen.
-   **Sonde** Pingen Sie das Modul an, um festzustellen, ob es wach ist.
-   **Aufwachen** Starten Sie den Aufweckvorgang, wenn es sich um einen schlafenden Knoten handelt.
-   **Herstellerspezifisch1** Rufen Sie den Namen des Herstellers und die Produkt-IDs ab, wenn ProtocolInfo dies zulässt.
-   **NodeInfo** Informationen zur Unterstützung unterstützter Befehlsklassen abrufen.
-   **NodePlusInfo** Rufen Sie ZWave + -Informationen zur Unterstützung unterstützter Befehlsklassen ab.
-   **Sicherheitsbericht** Rufen Sie die Liste der Auftragsklassen ab, für die Sicherheit erforderlich ist.
-   **Herstellerspezifisch2** Rufen Sie den Namen des Herstellers und die Produktkennungen ab.
-   **Versionen** Versionsinformationen abrufen.
-   **Instanzen** Informationen zur Befehlsklasse für mehrere Instanzen abrufen.
-   **Statisch** Statische Informationen abrufen (ändert sich nicht).
-   **CacheLoad** Pingen Sie das Modul während des Neustarts mit dem Konfigurationscache des Geräts.
-   **Verbände** Informationen zu Assoziationen abrufen.
-   **Nachbarn** Rufen Sie die Liste der benachbarten Knoten ab.
-   **Sitzung** Sitzungsinformationen abrufen (Änderungen selten).
-   **Dynamisch** Dynamische Informationen abrufen (Änderungen häufig).
-   **Konfiguration** Informationen zu Konfigurationsparametern abrufen (nur auf Anfrage).
-   **Vollständig** Der Interviewprozess für diesen Knoten ist abgeschlossen.

## Notification

Details zu Benachrichtigungen, die von Modulen gesendet werden

-   **Abgeschlossen** Aktion erfolgreich abgeschlossen.
-   **Zeitüberschreitung** Verzögerungsbericht beim Senden einer Nachricht gemeldet.
-   **NoOperation** Berichten Sie bei einem Test des Knotens (Ping), dass die Nachricht erfolgreich gesendet wurde.
-   **Wach auf** Melden Sie, wenn ein Knoten gerade aufgewacht ist
-   **Schlaf** Melden Sie, wenn ein Knoten eingeschlafen ist.
-   **Tot** Melden Sie, wenn ein Knoten als tot angenommen wird.
-   **Lebendig** Bericht, wenn ein Knoten neu gestartet wird.

# Backups

Mit dem Sicherungsteil können Sie die Sicherungen Ihrer Netzwerktopologie verwalten. Dies ist Ihre zwcfgxxx-Datei.xml, es stellt den letzten bekannten Status Ihres Netzwerks dar, es ist eine Form des Cache Ihres Netzwerks. Von diesem Bildschirm aus können Sie :

-   Starten Sie eine Sicherung (eine Sicherung wird bei jedem Neustart des Netzwerks und während kritischer Vorgänge erstellt). Die letzten 12 Backups werden aufbewahrt
-   Stellen Sie ein Backup wieder her (indem Sie es aus der obigen Liste auswählen)
-   Löschen Sie eine Sicherung

![backup01](../images/backup01.png)

# Aktualisieren Sie OpenZWave

Nach einem Update des Z-Wave-Plugins werden Sie möglicherweise von Jeedom aufgefordert, die Z-Wave-Abhängigkeiten zu aktualisieren. Eine Abhängigkeit NOK wird angezeigt:

![update01](../images/update01.png)

> **Spitze**
>
> Eine Aktualisierung der Abhängigkeiten darf nicht bei jeder Aktualisierung des Plugins durchgeführt werden.

Jeedom sollte das Abhängigkeitsupdate selbst starten, wenn das Plugin dies für richtig hält **NOK**. Diese Validierung erfolgt nach 5 Minuten.

Die Dauer dieses Vorgangs kann je nach System variieren (bis zu mehr als 1 Stunde bei Himbeer-Pi)

Sobald die Aktualisierung der Abhängigkeiten abgeschlossen ist, wird der Dämon nach der Validierung von Jeedom automatisch neu gestartet. Diese Validierung erfolgt nach 5 Minuten.

> **Spitze**
>
> Für den Fall, dass die Aktualisierung der Abhängigkeiten nicht abgeschlossen ist, konsultieren Sie bitte das Protokoll **Openzwave\_update** Wer sollte Sie über das Problem informieren.

# Liste kompatibler Module

Sie finden die Liste der kompatiblen Module
[hier](https://compatibility.jeedom.com/index.php?v=d&p=home&search=&plugin=openzwave)

# Fehlerbehebung und Diagnose

## Mein Modul wird nicht erkannt oder enthält keine Produkt- und Typkennungen

![troubleshooting01](../images/troubleshooting01.png)

Starten Sie die Regeneration der Knotenerkennung auf der Registerkarte Aktionen des Moduls.

Wenn Sie in diesem Szenario mehrere Module haben, starten Sie **Regenerieren Sie die Erkennung unbekannter Knoten** vom Bildschirm **Zwave Netzwerk** Tab **Lager**.

## Mein Modul wird vom Dead-Controller als tot angenommen

![troubleshooting02](../images/troubleshooting02.png)

Wenn das Modul noch angeschlossen und erreichbar ist, befolgen Sie die im Modulbildschirm vorgeschlagenen Lösungen.

Wenn das Modul abgebrochen wurde oder wirklich defekt ist, können Sie es mit aus dem Netzwerk ausschließen **Löschen Sie den fehlerhaften Knoten** via tab **Lager**.

Wenn das Modul repariert und ein neues Ersatzmodul geliefert wurde, können Sie es starten **Ersetzen Sie den ausgefallenen Knoten** via tab **Lager**, Wenn der Controller die Aufnahme auslöst, müssen Sie mit der Aufnahme auf dem Modul fortfahren. Die ID des alten Moduls sowie seine Befehle werden beibehalten.

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

Der Szenenmodus muss in den Moduleinstellungen aktiviert sein. Weitere Informationen finden Sie in der Dokumentation zu Ihrem Modul.

## Aktualisierungswerte erzwingen

Es ist möglich, die Anforderung zu zwingen, die Werte einer Instanz für einen bestimmten Klassenbefehl zu aktualisieren.

Es ist möglich, dies über eine http-Anfrage zu tun oder eine Bestellung im Gerätezuordnungsbildschirm zu erstellen.

![troubleshooting06](../images/troubleshooting06.png)

Dies ist eine Bestellung **Aktion** Wählen Sie die **CC** gewünscht für a **Instanz** mit dem Befehl gegeben **data \ [0 \]. ForceRefresh()**

Alle Instanzindizes für diesen Klassenbefehl werden aktualisiert. Die Knoten der Batterien warten auf ihr nächstes Erwachen, bevor sie die Aktualisierung ihres Werts durchführen.

Sie können die Verwendung auch per Skript verwenden, indem Sie eine http-Anforderung an den Z-Wave-REST-Server senden.
Ersetzen Sie ip\_jeedom, node\_id, instance\_id, cc\_id und index

``http://token:\.#APIKEY\.#@ip\._jeedom:8083/ZWaveAPI/Run/devicesnode\._id.instances\.[instance\._id\.].commandClasses\.[cc\._id\.].data\.[index\.].ForceRefresh()``

## Übertragen Sie die Module auf eine neue Steuerung

Aus verschiedenen Gründen müssen Sie möglicherweise alle Ihre Module auf einen neuen Hauptcontroller übertragen.

Sie entscheiden sich zu gehen **raZberry** zu einem **Z-Stick Gen5** oder weil Sie eine durchführen müssen **Zurücksetzen** komplett von Hauptsteuerung.

Hier sind verschiedene Schritte, um dorthin zu gelangen, ohne Ihre wertvollen Szenarien, Widgets und den Verlauf zu verlieren:

-   1 \) Erstellen Sie ein Jeedom-Backup.
-   2 \) Denken Sie daran, Ihre Parameterwerte für jedes Modul aufzuschreiben (Screenshot). Sie gehen nach dem Ausschluss verloren.
-   3 \) Deaktivieren Sie in der Z-Wave-Konfiguration die Option "Ausgeschlossene Geräte automatisch löschen" und speichern Sie sie. Neustart des Netzwerks.
-   4a) Im Fall von a **Zurücksetzen**, Setzen Sie den Hauptcontroller zurück und starten Sie das Plugin neu.
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
-   Warten Sie, bis der Startzyklus abgeschlossen ist (Topologie geladen).
-   Das Modul wird normalerweise als tot markiert (tot)).
-   In der nächsten Minute sollte der Knoten vom Integritätsbildschirm verschwinden.
-   Wenn Sie in der Z-Wave-Konfiguration die Option "Ausgeschlossene Geräte automatisch löschen" deaktiviert haben, müssen Sie die entsprechenden Geräte manuell löschen.

Dieser Assistent ist nur für Batteriemodule verfügbar.

## Aktionen nach der Aufnahme

Es wird empfohlen, den Einschluss mindestens 1 m vom Hauptcontroller entfernt durchzuführen, da dies sonst nicht die endgültige Position Ihres neuen Moduls ist. Nach der Aufnahme eines neuen Moduls in Ihr Netzwerk sollten Sie einige bewährte Methoden befolgen.

Sobald die Aufnahme abgeschlossen ist, müssen wir eine bestimmte Anzahl von Parametern auf unser neues Modul anwenden, um das Beste daraus zu machen. Zur Erinnerung: Die Module haben nach der Aufnahme die Standardeinstellungen des Herstellers. Nutzen Sie die Möglichkeit, sich neben dem Jeedom-Controller und der Schnittstelle zu befinden, um Ihr neues Modul ordnungsgemäß zu konfigurieren. Es ist auch einfacher, das Modul zu aktivieren, um die unmittelbaren Auswirkungen der Änderung zu erkennen. Einige Module verfügen über eine spezielle Jeedom-Dokumentation, die Ihnen bei den verschiedenen Parametern sowie den empfohlenen Werten hilft.

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

> **Spitze**
>
> Es ist natürlich möglich, den Batteriewert manuell über die Registerkarte Werte des Moduls zu aktualisieren und dann entweder auf das nächste Aufwecken zu warten oder das Modul sogar manuell aufzuwecken, um einen sofortigen Anstieg zu erzielen. Das Aufweckintervall des Moduls wird auf der Registerkarte System des Moduls definiert. Um die Lebensdauer Ihrer Batterien zu optimieren, wird empfohlen, diese Verzögerung so lange wie möglich zu berücksichtigen. Wenden Sie für 4 Stunden 14400, 12 Stunden 43200 an. Bestimmte Module müssen regelmäßig Nachrichten von der Steuerung abhören, z. B. Thermostate. In diesem Fall müssen Sie an 15 Minuten denken, d. H. 900. Jedes Modul ist anders, daher gibt es keine genaue Regel, es ist von Fall zu Fall und erfahrungsgemäß.

> **Spitze**
>
> Die Entladung einer Batterie ist nicht linear. Einige Module weisen in den ersten Tagen nach der Inbetriebnahme einen großen prozentualen Verlust auf und bewegen sich dann wochenlang nicht, um sich nach 20% schnell zu entleeren.

## Controller wird initialisiert

Wenn Sie beim Starten des Z-Wave-Dämons versuchen, sofort einen Einschluss / Ausschluss zu starten, wird möglicherweise diese Meldung angezeigt: \* "Der Controller wird initialisiert. Bitte versuchen Sie es in einigen Minuten erneut"

> **Spitze**
>
> Nach dem Start des Daemons schaltet der Controller alle Module ein, um das Interview zu wiederholen. Dieses Verhalten ist in OpenZWave völlig normal.

Wenn Sie diese Meldung jedoch nach einigen Minuten (mehr als 10 Minuten) immer noch haben, ist sie nicht mehr normal.

Sie müssen die verschiedenen Schritte ausprobieren:

-   Stellen Sie sicher, dass die Anzeigen des Jeedom-Gesundheitsbildschirms grün leuchten.
-   Stellen Sie sicher, dass die Plugin-Konfiguration in Ordnung ist.
-   Stellen Sie sicher, dass Sie den richtigen Port für den ZWave-Schlüssel ausgewählt haben.
-   Stellen Sie sicher, dass Ihre Jeedom Network-Konfiguration korrekt ist. (Achtung, wenn Sie eine DIY-Installation in Richtung des offiziellen Images wiederhergestellt haben, sollte das Suffix / jeedom dort nicht erscheinen)
-   Überprüfen Sie im Plugin-Protokoll, ob kein Fehler gemeldet wurde.
-   Beobachten Sie die **Konsole** ZWave-Plugin, um festzustellen, ob kein Fehler gemeldet wurde.
-   Starten Sie den Dämon mit **Debuggen** schau nochmal auf die **Konsole** und Plugin-Protokolle.
-   Starten Sie Jeedom vollständig neu.
-   Stellen Sie sicher, dass Sie einen Z-Wave-Controller haben. Die Razberry werden häufig mit dem EnOcean verwechselt (Fehler bei der Bestellung).

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

Mit 75% ist dies der Beginn der Kompilierung der Openzwave-Bibliothek sowie des Openzwave-Python-Wrappers. Dieser Schritt ist sehr lang. Sie können den Fortschritt jedoch über die Ansicht des Aktualisierungsprotokolls anzeigen. Man muss also nur geduldig sein.

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

Stoppen Sie nach dem Start in ssh diese Prozesse (Verbraucher im Speicher)) :

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
> Leider handelt es sich bei diesem Fehler um Hardware. Wir können nichts dagegen tun und suchen derzeit nach Möglichkeiten, um im Falle dieses Fehlers einen Neustart des Daemons zu erzwingen (häufig ist es jedoch auch erforderlich, den Schlüssel 5 Minuten lang abzuziehen, damit er erneut gestartet wird)
