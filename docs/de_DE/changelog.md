>**Wichtig**
>
>Zur Erinnerung: Wenn keine Informationen zum Update vorhanden sind, bedeutet dies, dass es sich nur um die Aktualisierung von Dokumentation, Übersetzung oder Text handelt

# 10/07/2019

- Ein Fehler beim Stoppen des Daemons wurde behoben
- Fehlerbehebungen
- DIESES UPDATE MUSS DIE ABHÄNGIGKEITEN ERNEUERN (NEUSTART)

# 2019-09-19

- Fehlerkorrektur anzeigen

# 09-10-2019

- Ein Problem mit der Anzeige der Routing-Tabelle wurde behoben

# 09-09-2019
- Anpassen von Abhängigkeiten für Debian10 Buster
- Änderung, die es ermöglicht, die Ausgaben auf dem Smart Implantat zu trennen (diese Funktion erfordert eine Neukompilierung der Abhängigkeiten)

2019-02-04
===
- DIESES UPDATE MUSS DIE ABHÄNGIGKEITEN ERNEUERN (NEUSTART)
- Behebung eines Fehlers bei mehreren Instanzen von Thermostaten
- Das Erstellen einer Warteschlangenebene ist aufgrund von Aktionen für Aktualisierungen veraltet
- Hinzufügen vieler Confs (zur Erinnerung: Die Schaltfläche zum Wiederherstellen von Confs ist nützlich, um auf dem neuesten Stand zu sein, ohne das Plugin zu aktualisieren.)
- Verbesserte Verwaltung gekapselter Mehrkanäle
- Zugabe von CC herstellerspezifisch
- Einfache Installation des CC Soundswitch
- Fix für mehrfache Einbeziehung von Geräten <
- Verbesserte CC-Switch-Binärdatei
- Die Eingabe manueller Parameter ist immer möglich
- Schwanzverbesserung
- Vorbereitung zum Hinzufügen neuer CCs (insbesondere Benachrichtigung)
- Hinzufügen von Codes zum CC-Alarm für die Zipato-Tastatur für den Moment
- Korrektur des Philios im sicheren Modus, der während der Klingeltöne eine Zeitüberschreitung von 10 Sekunden verursachte (es ist sicherlich notwendig, die Erkennung der Sirene neu zu generieren oder sie wieder einzuschließen)
- Korrektur eines Fehlers, wenn die Protokollstufe keine ist
- DIESES UPDATE MUSS DIE ABHÄNGIGKEITEN ERNEUERN

2018-03-17
===

- Zweigwechsel zur Wiederherstellung von Confs während der Synchronisierung (nach einer Änderung in der Organisation der Githubs)

2018-01-17 / 2018-01-19
===

-   Neuankömmlinge

    -   Rückgabe der Möglichkeit, Confs zu synchronisieren, ohne das Plugin zu aktualisieren

    -   Verbesserungen

    -   Hinzufügung der internen Möglichkeit, Aktualisierungen für bestimmte Werte und bestimmte Module auszulösen (verwendet in jeedom confs)

    -   Vollständige Neugestaltung der Funktion, die es ermöglicht, einen Wert für einen anderen Befehl zu simulieren, um zu vermeiden, dass er für eine Reihe von Modulen verwendet wird, jedoch speziell (Jeedom intern)

-   Fehler behoben

    -   Es wurde ein Fehler behoben, der dazu führte, dass automatisch generierte Confs im alten Format vorliegen und daher nicht mehr verwendet werden können

    -   Korrektur des Fehlers beim Verlust des anstehenden Sollwerts an den Thermostatventilen (geht mit Punkt 2 der Verbesserungen einher)

    -   Reduzierung der Größe der Bilder, um die Größe des Plugins so weit wie möglich zu begrenzen (ca. 500 Bilder)

    -   Entfernen von mehr verwendeten Abhängigkeiten wie Mercurial Sphinx usw

    -   Unterdrückung der Bereinigung der Konfigurationen vor der Aktualisierung (vermeidet, dass Zwave-Symbole anstelle der Bilder verwendet werden, wenn die Aktualisierung wegen Zeitüberschreitung oder aus anderen Gründen nicht erfolgreich ist)

2017-08-xx
===


-   Neue Funktionen

    -   Möglichkeit, Bestellungen für Geräte ohne zu aktualisieren
        vorhandene löschen.

    -   Möglichkeit zum Erstellen eines Informationsbefehls zu den Werten von
        Registerkarte System.

-   Verbesserungen / Verbesserungen

    -   Unterstützung für neue Module, ozw Definitionen
        und Bestellungen.

    -   Möglichkeit zur Auswahl der Standardzuordnung
        (ohne Instanz) auf den Modulen, die das unterstützen
        Assoziationen mit mehreren Instanzen.

    -   Überprüfung der Gültigkeit von Assoziationsgruppen am Ende
        des Interviews.

    -   Wiederherstellung des letzten Ladezustands der Batterien beim Start des Dämons.

-   Fehler behoben

    -   Korrektur der Migration der Batterieinfo.

    -   Korrektur der Batterieinfo-Rückmeldung in
        den Bildschirm Ausrüstung.

    -   Wiederherstellung des Batterietyps in Konfigurationen
        von Modulen.

    -   Korrektur von Aktionen für Schaltflächentypwerte in
        Modulbildschirm.

    -   Korrektur des Abrufs von Parameterübersetzungen.

    -   Korrektur des leeren Fehlers bei Änderung der RAW-Typwerte
        (RFid-Code).

    -   Anzeige anstehender Werte korrigiert
        angewendet werden.

    -   Unterdrückung der Benachrichtigung über Wertänderungen vor
        dass es nicht angewendet wird.

    -   Zeigen Sie das Vorhängeschloss nicht mehr auf dem Modulbildschirm an, wenn das Modul
        unterstützt keine Sicherheitsbefehlsklasse.

    -   Anwendung der manuellen Aktualisierung in
        empfohlene Einstellungen.

    -   Ausweisverwaltungsassistent für RFID-Lesegeräte.

    -   Korrektur des Assistenten zur Erkennung unbekannter Module.

    -   Korrektur der Assistenten von "Fortsetzen von .." und "Übernehmen"
        on ... "auf der Registerkarte" Einstellungen ".

2017-06-20
===

-   Neue Funktionen

    -   N / A

-   Verbesserungen / Verbesserungen

    -   Fügen Sie alle Modulkonfigurationen zum hinzu
        neues Format.

-   Fehler behoben

    -   Testen Sie nicht, ob während des Löschvorgangs eine NodeId vorhanden ist
        eines Vereins.

    -   Wiederherstellen der ausstehenden Einzahlungsbenachrichtigung am
        Thermostate.

    -   Senden der ausstehenden Aktivierungsszene 1.

    -   Zeigen Sie das Vorhängeschloss im Gesundheitsbildschirm nicht mehr an
        Module, die die Sicherheitsbefehlsklasse nicht unterstützen.

    -   Wiederholung des Wertes auf den Fernbedienungen vor dem Ende von
        das Interview (Kyefob, Minimote).

    -   Ändern Sie einen Parameter der Typliste nach Wert über a
        Aktionsbefehl.

    -   Ändern Sie einen Parameter in einem Modul ohne definierte Konfiguration.

2017-06-13
===

-   Neue Funktionen

    -   N / A

-   Verbesserungen / Verbesserungen

    -   Hinzufügung der Fibaro US-Modulkonfiguration

-   Fehler behoben

    -   N / A

2017-05-31
===

-   Neue Funktionen

    -   N / A

-   Verbesserungen / Verbesserungen

    -   N / A

-   Fehler behoben

    -   Korrektur der Zuordnung von Werten im RAW-Format von Codes
        für RFid Reader.

23.05.2017
===

-   Neue Funktionen

    -   Entfernen des Master / Slave-Modus. Ersetzt durch Plugin
        Jeedom Link.

    -   Verwendung eines privaten API-Schlüssels für das ZWave-Plugin.

    -   Neues Format der Konfigurationsdateien in der Zuordnung von
        mit jeedom bestellen.

    -   Automatische Umwandlung bestehender Aufträge in neue
        Format bei der Installation des Plugins.

    -   Unterstützung für die Central Scene Command Class hinzugefügt.

    -   Unterstützung für Barrier Operator Command Class hinzugefügt.

-   Verbesserungen / Verbesserungen

    -   Vollständige Überholung des REST-Servers mit TORNADO.

        -   Änderung aller vorhandenen Straßen,
            Skripte müssen angepasst werden, wenn die ZWave-API verwendet wird.

        -   Verstärkung der Sicherheit, nur Anrufe werden abgehört
            der REST-Server.

        -   Verwenden des erforderlichen ZWave-API-Schlüssels zum Starten
            REST-Anfragen.

    -   Deaktivieren (vorübergehender) Gesundheitstests.

    -   (Temporäre) Deaktivierung der Update Engine
        Modulkonfigurationen.

    -   Deaktivierung der Heal Network-Funktion automatisch
        zweimal pro Woche (Rückgang des Austauschs mit
        der Controller).

    -   Optimierungen des Openzwave-Bibliothekscodes.

        -   Fibaro FGK101 muss das Interview nicht mehr abschließen, um es anzukündigen
            eine Zustandsänderung.

        -   Der Auslöseknopfbefehl (Stopp eines Verschlusses) wird nicht mehr erzwungen
            Aktualisieren aller Modulwerte
            (Verringerung der Nachrichtenwarteschlange).

        -   Möglichkeit, Werte in der Klasse von zu benachrichtigen
            Alarmbefehl (Klingeltonauswahl bei Sirenen)

    -   Mehr tägliche Nachfrage nach Batteriestand (weniger als
        Nachrichten, spart Batterien).

    -   Der Akkuladestand wird direkt an den Akkubildschirm gesendet
        Level-Bericht empfangen.

-   Fehler behoben

    -   Aktualisierung aller Instanzen nach a
        CC Switch ALL Broadcast.

2016-08-26
===

-   Neue Funktionen

    -   Aucune

-   Verbesserungen / Verbesserungen

    -   RPI3-Erkennung beim Abhängigkeitsupdate.

    -   Aktivieren Sie den standardmäßigen nicht sicheren Einschlussmodus.

-   Fehler behoben

    -   Testen Sie die Herstellerinformationen auf dem Gesundheitsbildschirm
        nicht mehr NOK.

    -   Verlust von Kontrollkästchen auf der Registerkarte Befehle der
        Ausrüstungsseite.

2016-08-17
===

-   Neue Funktionen

    -   Neustart des Dämons, wenn der Controller während des Timeouts erkannt wird
        Controller-Initialisierung.

-   Verbesserungen / Verbesserungen

    -   OpenZWave-Bibliotheksupdate 1.4.2088.

    -   Rechtschreibkorrektur.

    -   Neugestaltung des Gerätebildschirms mit Registerkarten.

-   Fehler behoben

    -   Problem beim Anzeigen bestimmter Module in der Routing-Tabelle
        und Netzwerkgraph.

    -   Vision Secure-Module, die nicht in den Standby-Modus zurückkehren
        während des Interviews.

    -   Installation von Abhängigkeiten in der Schleife (Github-Problem).

2016-07-11
===

-   Neue Funktionen

    -   Unterstützung für die Wiederherstellung des letzten bekannten Levels am
        verdunkeln sie.

    -   Unterscheidung von FLiRS-Modulen im Integritätsbildschirm.

    -   Anforderung zum Aktualisieren der Rückrouten hinzugefügt
        an die Steuerung.

    -   Assistent zum Anwenden der Konfigurationsparameter von a
        Modul zu mehreren anderen Modulen.

    -   Identifizierung der Zwave + unterstützenden Module
        BEFEHL\_KLASSE\_ZWAVE\_PLUS\_INFO.

    -   Anzeige des Sicherheitsstatus der unterstützten Module
        BEFEHL\_KLASSE\_SICHERHEIT.

    -   Hinzufügung der Möglichkeit, Instanz 0 der auszuwählen
        Controller für Multi-Instance-Assoziationen.

    -   Sichern aller Anrufe an den REST-Server.

    -   Automatische Dongle-Erkennung auf der Konfigurationsseite
        Plugin.

    -   Einschlussdialog mit Auswahl des Einschlussmodus für
        Vereinfachen Sie die sichere Aufnahme.

    -   Unter Berücksichtigung deaktivierter Geräte innerhalb der
        Z-Wave Motor.

        -   Graue Anzeige im Gesundheitsbildschirm ohne Analyse an
            der Knoten.

        -   Versteckt in der Netzwerktabelle und im Netzwerkdiagramm.

        -   Deaktivierte Knoten schließen Gesundheitstests aus.

-   Verbesserungen / Verbesserungen

    -   Optimierung der Hygienekontrollen.

    -   Optimierung von Netzwerkgraphen.

    -   Verbesserte Erkennung des Hauptcontrollers für
        Gruppentest.

    -   Update auf die OpenZWave-Bibliothek 1.4.296.

    -   Optimierung der Hintergrundkühlung der Laufwerke.

    -   Optimierte Hintergrundaktualisierung für
        die Motoren.

    -   Anpassung für Jeedom-Kern 2.3

    -   Integritätsbildschirm, Änderung des Spaltennamens und Warnung
        im Falle der Nichtkommunikation mit einem Modul.

    -   Optimierung des REST-Servers.

    -   Korrektur der Schreibweise der Bildschirme, danke @ Juan-Pedro
        aka: Kiko.

    -   Aktualisieren der Plugin-Dokumentation.

-   Fehler behoben

    -   Korrektur möglicher Probleme beim Update
        Modulkonfigurationen.

    -   Netzwerkgraph, Berechnung der Sprünge auf der Controller-ID
        Auftraggeber und nicht ID 1 annehmen.

    -   Verwaltung der Schaltfläche Hinzufügen einer Gruppenzuordnung.

    -   Anzeige falscher Werte auf der Registerkarte Konfiguration.

    -   Nehmen Sie nicht mehr das aktuelle Datum für den Zustand der Batterien an, wenn Sie nicht empfangen werden
        Gerätebericht.

2016-05-30
===

-   Neue Funktionen

    -   Option zum Aktivieren / Deaktivieren von Steuerelementen hinzugefügt
        Sanitär auf allen Modulen.

    -   Hinzufügen einer Registerkarte "Benachrichtigungen", um die letzten 25 anzuzeigen
        Controller-Benachrichtigungen.

    -   Hinzufügen einer Route zur Wiederherstellung des Zustands eines Knotens.
        ip\_jeedom:8083 / ZWaveAPI / Run / Geräte \ [Knoten\_id \]. GetHealth ()

    -   Hinzufügen einer Route zum Abrufen der letzten Benachrichtigung
        eines Knotens.
        ip\_jeedom:8083 / ZWaveAPI / Run / Geräte \ [Knoten\_id \]. GetLastNotification ()

-   Verbesserungen / Verbesserungen

    -   Ermöglichen Sie die Auswahl von FLiRS-Modulen während
        direkte Assoziationen.

    -   Ermöglichen Sie die Auswahl aller Instanzen von Modulen während
        direkte Assoziationen.

    -   OpenZWave Python Wrapper Update auf Version 0.3.0.

    -   Aktualisierung der OpenZWave 1.4.248-Bibliothek.

    -   Zeigen Sie keine abgelaufene Weckwarnung für an
        batteriebetriebene Module.

    -   Überprüfung, ob ein Modul auf der ID-Ebene für identisch ist
        Kopieren von Parametern ermöglichen.

    -   Vereinfachung des Assistenten zum Kopieren von Parametern.

    -   Nicht vorkommende Systemregisterkartenwerte ausblenden
        angezeigt werden.

    -   Anzeige der Beschreibung der Controller-Funktionen.

    -   Aktualisierung der Dokumentation.

    -   Korrektur der Schreibweise der Dokumentation, danke
        @Juan-Pedro aka: Kiko.

-   Fehler behoben

    -   Rechtschreibkorrektur.

    -   Die Aufnahme in den sicheren Modus wurde korrigiert.

    -   Korrektur des asynchronen Aufrufs. (error: \ [Errno 32 \]
        Rohrbruch)

2016-05-04
===

-   Neue Funktionen

    -   Option zum Deaktivieren der Hintergrundaktualisierung hinzugefügt
        Dimmer.

    -   Anzeige von Assoziationen, denen ein Modul zugeordnet ist
        (Verwendung finden).

    -   Unterstützung für CC MULTI\_INSTANCE\_ASSOCIATION hinzugefügt.

    -   Hinzufügen einer Info-Benachrichtigung bei der Bewerbung
        Setzen Sie\_Point, um den unter angeforderten Sollwert zu verwenden
        cmd info form.

    -   Hinzufügen eines empfohlenen Konfigurationsassistenten.

    -   Option zum Aktivieren / Deaktivieren des Assistenten hinzufügen
        empfohlene Konfiguration beim Einschließen
        neue Module.

    -   Option zum Aktivieren / Deaktivieren des Updates von hinzufügen
        Modulkonfigurationen jede Nacht.

    -   Hinzufügen einer Route zum Verwalten mehrerer Zuordnungsinstanzen.

    -   Fehlende Abfragephase hinzufügen.

    -   Validierung der Auswahl des USB-Dongles zum hinzugefügt
        den Dämon starten.

    -   Hinzufügung der Validierung und Test des Rückrufs beim Start
        des Dämons.

    -   Option zum Deaktivieren der automatischen Aktualisierung hinzugefügt
        Modulkonfiguration.

    -   Hinzufügen einer Route zum Ändern der Protokollablaufverfolgungen zur Laufzeit
        der REST-Server. Note: Keine Auswirkung auf die OpenZWave-Ebene.
        <http://ip_jeedom:8083/ZWaveAPI/Run/ChangeLogLevel(level>) level
        ⇒ 40:Fehler, 20: Debug 10 Info

-   Verbesserungen / Verbesserungen

    -   Update des OpenZWave Python Wrappers auf Version 0.3.0b9.

    -   Hervorheben von Gruppen ausstehender Assoziationen
        angewendet werden.

    -   Update auf die OpenZWave-Bibliothek 1.4.167.

    -   Änderung des direkten Assoziationssystems.

    -   Aktualisierung der Dokumentation

    -   Möglichkeit, die Regeneration der Knotenerkennung zu starten
        für alle identischen Module (Marke und Modell).

    -   Wird im Integritätsbildschirm angezeigt, wenn Konfigurationselemente vorhanden sind
        werden nicht angewendet.

    -   Zeigen Sie im Gerätebildschirm an, ob Elemente von
        Konfiguration werden nicht angewendet.

    -   Wird im Integritätsbildschirm angezeigt, wenn ein Batteriemodul dies nicht getan hat
        bin nie aufgewacht.

    -   Anzeige im Integritätsbildschirm, wenn ein Batteriemodul überschritten wurde
        die erwartete Weckzeit.

    -   Hinzufügen von Traces bei Benachrichtigungsfehler.

    -   Bessere Wiederherstellung des Batteriestatus.

    -   Zusammenfassung / Gesundheitskonformität für Batteriethermostate.

    -   Bessere Erkennung von Modulen auf Batterien.

    -   Optimierung des Debug-Modus für den REST-Server.

    -   Erzwingen Sie eine Aktualisierung und ein Dimer des Schaltzustands
        nach dem Senden eines Befehls switch all.

-   Fehler behoben

    -   Entdeckung von Assoziationsgruppen behoben.

    -   Korrektur des Fehlers "Exception KeyError: (91,) in
        'libopenzwave.notif\_callback 'wird ignoriert".

    -   Korrektur der Auswahl der Moduldokumentation für
        Module mit mehreren Profilen.

    -   Verwaltung der Aktionstasten des Moduls.

    -   Korrektur der Beschreibung des generischen Klassennamens.

    -   Korrektur der Sicherung der zwcfg-Datei.

2016-03-01
===

-   Neue Funktionen

    -   Hinzufügen der Schaltfläche Konfiguration über den Verwaltungsbildschirm
        Ausrüstung.

    -   Hinzufügung neuer Modulinterviewzustände.

    -   Bearbeiten von Beschriftungen in Benutzeroberflächen.

-   Verbesserungen / Verbesserungen

    -   Bessere Verwaltung der Schaltflächen für Modulaktionen.

    -   Dokumentation Hinzufügen von Abschnitten.

    -   Optimierung des Daemon-Statuserkennungsmechanismus.

    -   Protestmechanismus während der Wiederherstellung der
        Beschreibung der Parameter, wenn sie Zeichen enthalten
        nicht gültig.

    -   Kehren Sie niemals zu den Batteriestatusinformationen auf a zurück
        Modul an das Stromnetz angeschlossen.

    -   Aktualisierung der Dokumentation.

-   Fehler behoben

    -   Dokumentation Rechtschreibung und grammatikalische Korrekturen.

    -   Überprüfung des Inhalts der zwcfg-Datei vor dem Anwenden.

    -   Installationskorrektur.

2016-02-12
===

-   Verbesserungen / Verbesserungen

    -   Keine Warnung vor toten Knoten, wenn diese deaktiviert ist.

-   Fehler behoben

    -   Korrektur der Statusrückgabe des Fibaro-Pilotdrahtes.

    -   Korrektur eines Fehlers, der die Befehle während der Einstellung neu erstellt
        auf dem neuesten Stand.

2016.02.09
===

-   Neue Funktionen

    -   Das Hinzufügen einer Push-Benachrichtigung im Fall des Knotens\_event ermöglicht
        Implementierung einer cmd-Information in CC 0x20 zur Wiederherstellung
        Ereignis auf Knoten.

    -   ForceRefresh-Route hinzugefügt
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ForceRefresh()
        kann in Bestellungen verwendet werden.

    -   Hinzufügen der SwitchAll-Route
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[1\].commandClasses\[0xF0\].SwitchAll(&lt;int:state&gt;)
        über die Hauptsteuerung verfügbar.

    -   Hinzufügen der ToggleSwitch-Route
        http://ip\_jeedom:8083/ZWaveAPI/Run/devices&lt;int:node\_id&gt;.instances\[&lt;int:instance\_id&gt;\].commandClasses\[&lt;cc\_id&gt;\].data\[&lt;int:index&gt;\].ToggleSwitch()
        kann in Bestellungen verwendet werden.

    -   Hinzufügen einer Push-Benachrichtigung im Falle eines vermuteten toten Knotens.

    -   Ajout de la commande “refresh all parameters” dans
        die Registerkarte Einstellungen.

    -   Hinzufügen der Parameterinformationen, die darauf warten, angewendet zu werden.

    -   Netzwerkbenachrichtigung hinzufügen.

    -   Hinzufügen einer Legende im Netzwerkdiagramm.

    -   Hinzufügen der Netzwerkpflegefunktion über die Routing-Tabelle.

    -   Automatische Entfernung von Geisterknoten mit nur einem Klick.

    -   Verwaltung von Aktionen auf dem Knoten gemäß dem Status des Knotens und dem Typ.

    -   Verwaltung von Netzwerkaktionen nach Netzwerkstatus.

    -   Aktualisierung der automatischen Modulkonfiguration alle
        die Nächte.

-   Verbesserungen / Verbesserungen

    -   Komplettes Refactoring des REST-Servercodes, Optimierung von
        Startgeschwindigkeit, Lesbarkeit, Einhaltung der Konvention
        Benennung.

    -   Quadratische Protokolle.

    -   Vereinfachung der manuellen 5min Refresh Management mit
        Möglichkeit, auf Knoten auf Batterien anzuwenden.

    -   Update der OpenZWave-Bibliothek in 1.4

    -   Änderung des Gesundheitstests zur Wiederbelebung der vermuteten Knoten
        leichter ohne Benutzeraktionen tot.

    -   Verwendung von hellen Farben in der Routing-Tabelle und
        Netzwerkgraph.

    -   Standardisierung der Farben der Routing-Tabelle und der
        Netzwerkgraph.

    -   Optimierung der Informationen auf der Z-Wave-Gesundheitsseite gemäß
        den Stand des Interviews.

    -   Bessere Verwaltung von schreibgeschützten oder Schreibparametern
        nur auf der Registerkarte Einstellungen.

    -   Verbesserte Warnung bei Batteriethermostaten.

-   Fehler behoben

    -   Die in Celsius umgerechnete Temperatur gibt stattdessen Einheit C zurück
        von F.

    -   Korrektur der Aktualisierung von Werten beim Start.

    -   Korrektur der Aktualisierung nach Wert auf der Registerkarte Werte.

    -   Korrektur generischer Modulnamen.

    -   Korrektur des Pings auf den Knoten in Timeout während des
        Gesundheitstest.
