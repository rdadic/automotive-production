Automotive Production Data Pipeline 

1. Projektbeschreibung 

Dieses Projekt ist ein Programmier- und Datenanalyseprojekt im Automotive-Bereich. 
Es orientiert sich thematisch an der Unterbodenschutzfertigung (UBS) in der BMW-Lackiererei am Standort München.

Im Mittelpunkt stehen die Entwicklung einer Datenpipeline, die Verarbeitung relationaler Daten 
und die Analyse von Produktionsdaten mit Python, SQL, Pandas, Apache Airflow und Apache Kafka.

Die Simulation berücksichtigt die BMW-Baureihen G20, G21, G26, G80 und G81 mit unterschiedlichen Antriebsarten. Die verwendeten Prozessparameter, darunter Flächen, Schichtdicken und Materialvolumen, sind vereinfachte Schätzwerte und dienen ausschließlich der Simulation. Sie stellen keine technisch validierten Prozessdaten dar.

Alle Produktionsdaten und Messwerte sind synthetisch und wurden für dieses Projekt generiert. Es werden keine realen oder vertraulichen BMW-Produktionsdaten verwendet.

Das Ziel ist es, Programmierkenntnisse, Datenbankentwicklung, ETL-Prozesse, Datenanalyse und Datenvisualisierung anhand eines praxisorientierten Beispiels aus der Automobilindustrie zu demonstrieren.

Verwendete Technologien:
Python - Datengenerierung, Datenverarbeitung und Pipeline-Logik 
MySQL - relationale Datenbank und analytische Abfragen 
Pandas - Transformationen und Aggregation von Daten 
Matplotlib - Visualisierung von Produktios- und Messdaten 
Apache Airflow - Orchestrierung automatisierter Workflows
Git und GitHub - Versionverwaltung und Projektdokumentation 

2. Projektfunktionen 

2.1 Generierung synthetischer Daten 

Produktionsdatensätze und PVC-Messdaten werden mit Python generiert und in einer MySQL-Datenbank
gespeichert. 
Die generierten Daten umfassen eindeutige Fahrzeugkennungen (IGEF), Fahrzeugmodelle, Produktionslinien, Produktionszeitpunkte, Robotermessungen und Abweichungen von vordefinierten
Prozessspezifikationen. 
Die Messdaten simulieren unterschiedliche Prozessbedingungen und ermöglichen die Durchführung analytischer Abfragen. Sie stellen keine validierten industriellen Messwerte dar. 

2.2 Datenbank uns SQL-Analysen 

Die MySQL-Datenbank enthält miteinander verknüpfte Tabellen für Fahrzeugmodelle, Robotertypen, Roboter, Prozessspezifikationen, Produktionsdatensätze und Produktionsmessungen. Zusätzliche wird die Tabelle vehicle_status über einen Trigger aktualisiert.

Die SQL-Skripte demonstrieren unter anderem:
- Erstellung von Tabellen und relationaler Datenmodellierung 
- Tabelleverknüpfungen mit JOIN 
- Aggregationen und Filterbedingungen 
- Common Table Expressions (CTEs)
- Unterabfragen (Subqueries)
- Views 
- Indizes
- Trigger zur automatischen Aktualisierung von Daten
- Prepared Statements
- WITH ROLLUP zur Berechnung von Gruppensummen und Gesamtergebnissen 
- Stored Procedures zur Wiederverwendung analytischer Abfragen 

Die Analysen umfassen Produktionsmengen, PVC-Verbrauch, Messabweichungen und Roboter mit einer übersdurchschnittlichen Anzahl erforderlicher Prüfungen. 

2.3 Datenanalyse und Visualisierung 

Mit Python und Pandas werden Produktionsdatensätze, Messdaten und Prozessspezifikationen miteinander verknüpft und ausgewertet. 

Dabei entstehen aggregierte Datensätze für folgende Analysen: 
- Produktions- und Messkennzahlen je Fahrzeugmodell und Produktionslinie
- Vergleich der durchschnittlichen absoluten Messabweichungen zwischen den Produktionslinien
- Stündliche Produktionsmengen 
- Produktionsunterbrechungen anhand der Zeitabstände zwischen aufeinanderfolgenden Fahrzeugen
- Messungen, bei denen eine zusätzliche Prüfung erforderlich ist

Matplotlib wird zur Visualisierung von Produktionsverläufen und Unterbrechungen eingesetzt. Die Diagramme werden als Bild-dateien gespeichert. 

2.4 Workflow-Orchestrierung mit Apache Airflow 

Ein Airflow-DAG mit dem Namen automotive_production_pipeline organisiert die Datenverarbeitung in drei aufeinander aufbauenden Tasks: 
    1. extract - liest Datena aus MySQL aus und speichert sie als CSV-Dateien 
    2. transform - verknüpft die extrahierten Datensätze und berechnet analytische Kennzahlen
    3. visualize - erstellt Diagramme auf Grundlage der verarbeiteten Daten und speicher sie als Bilddateien
Die Tasks werden nacheinander ausgeführt. Der Ablauf kann über die Benutzeroberfläche von Apache Airflow überwacht werden. 

2.5 Event-Streaming mit Apache Kafka 

Ein Kafka-Producer liest Produktionsdaten aus MySQL aus, verknüpft die Produktionsdaten mit den Fahrzeugmodellen, serialisiert jeden Datensatz als JSON und veröffentlicht die Nachrichten im Kafka-Topic productionUBS. 

Jede Nachricht enthält die Fahrzekennung (IGEF), das Modell, die Antriebsart, die Produktionslinie und den Produktionszeitpunkt. Die IGEF-Nummer wird als Kafka-Nachrichtenschlüssel verwendet. 

Ein Kafka-Consumer abonniert das Topic und gibt die empfangenen Produktionsereignisse im Terminal aus. 

Die aktuelle Implementierung überträgt vorhandene Datenbanksätze bei Ausführung der Producers. Sie demonstriert die Erzeugung und Verarbeitung von Events, jedoch keine kontinuierliche Echtzeitverbindung zu einer tatsächlichen Produktionsanlage. 


3. Datengrundlage und Einschränkungen 

Das Projekt verwendet synthetische Daten, um technische Implentierungen und analytische Methoden zu demonstrieren. 
Die PVC-Sollwerte, tatsächlichen Volumen und Abweichungen werden für Entwicklungs- und Testzwecke simuliert. Sie dürfen nicht als validierte physikalische Berechnungen oder reale Qualitätsmessungen interpretiert werden. 

4. Projektstatus 

Das Projetk wird schrittweise entwickelt. Die Dokumentation orientiert sich am aktuellen Funktionsumfang der implementierten Komponenten. Weitere Verbesserungen und Erweiterungen sind möglich. 

5. Projektsturktur 

automotive-production/
|-- data/
|       models.csv
|       robots.csv
|       robot_types.csv
|       process_specifications.xlsx
|-- generators/
|       production.py
|       measurements.py     
|-- sql/
|       create_tables.sql
|       views.sql
|       indexes.sql
|       triggers.sql
|       procedures.sql
|       analytical_queries.sql
|-- src/
|       kafka/
|             consumer.py
|             producer.py
|-- dags/
|       automotive_pipeline.py
|-- pipeline/ 
|-- generate_data.py
|-- requirements.txt
|-- .gitignore
|-- README.md

Der Ordner pipeline/ enthält die im Rahmen der Datenverarbeitung erzeugten Dateien. Dazu gehören extrahierte Datensätze, Analyseergebnisse und gegebenenfalls Diagramme. 

6. Ausführung der Projekts 

Voraussetzungen 

Für die Ausführung des Projekts werden folgende Technologien benötigt:
Python - zur Datengenerierung, Datenverarbeitung und Visualisierung 
MySQL-Server - zur Speicherung und Verwaltung der Produktions- und Messdaten
Apache Airflow - zur Automatiserung und Überwachung der Datenpipeline 
Apache Kafka - zur Übertragung von Produktionsdaten zwischen Producer und Consumer

Python-Bibliotheken: 
    Pandas - zur Datenverarbeitung und Analyse
    Matplotlib - zur Erstellung von Diagrammen 
    MySQL Connector - zur Verbindung mit der MySQL-Datenbank 
    Python-dotenv - zum Laden der Datenbankkonfiguration 
    Openpyxl - zum Einlesen von Excel-Dateien

Zusätzlich werden die entsprechenden Konfigurationen für die Datenbank, Airflow und Kafka benötigt. 

Die Datenbankzugangsdaten werden über Umgebungsvariablen bereitgestellt und nicht direkt im Quellcode gespeichert. 

6.1 Datenbank vorbereiten 

Zuerst werden die benötigten Tabellen und Datenbankobjekte in MySQ eingerichtet. 
sql/create_tables.sql - erstellt die Tabellen und definiert ihre Beziehungen. 
sql/triggers.sql - erstellt den Trigger, der beim Einfüger neuer Datensätze in production automatisch ausgeführt wird und die Tabelle vehicle_status aktualisiert. 

Das Skript generate_data.py übernimmt die Datengenerierung und den Import. Die Datenbankverbindung muss zuvor korrekt konfiguriert sein. 

6.2 SQL-Abfragen ausführen 
Die SQL-Dateien im Verzeichnis sql/ enthalten die Tabellenstrukturen, Views, Indizes, Trigger, analytischen Abfragen und gespeicherten Prozeduren. 
Mit diesen Abfragen können die Produktionsdaten nach verschiedenen Kriterien ausgewertet werden, beispielsweise nach Fahrzeugmodell, Produktionslinie und Schicht. 

6.3 Datenpipeline ausführen 
Apache Airflow steuert die Verarbeitung der Daten über den DAG automotive_production_pipeline. 
Die Pipeline führt drei Aufgaben nacheinander aus: extract -> transform -> visualize. 
Der Status der einzelnen Aufgaben kann im Airflow-Interface überprüft werden. 

6.4 Kafka Producer und Consumer starten 
Der Kafka-Producer liest ausgewählte Produktionsdaten aus MySQL und sendet sie als JSON-Nachrichten an das Topic productionUBS. 
Der Kafka-Consumer empfängt die Nachrichten aus diesem Topci und gibt sie in der Konsole aus. 

Für die Ausführung müssen der Kafka-Broker und die Datenbank erreichbar sein.


7. Ergebnisse 

Im Verlauf der Datenbankverarbeitung werden verschieden Analyseergebnisse erzeugt.
model_analysis.csv - Produktionsanalyse nach Fahrzeugmodell 
model_line_pivot.csv - Vergleich der Produktionslinien 
hurly_production.csv - Produktionsmenge nach Stunde
interruptions.csv - Erkannte Produktionsunterbrechungen 

Zusätzlich werden Diagramme mit Matplotlib erstellt. Sie ermöglichen eine grafische Auswertung der Produktionsdaten. 


8. Sicherheit 

Datenbankzugangsdaten und andere vertrauliche Konfigurationswerte werden nicht im öffentliche Repository gespeichert. Die entsprechenden Dateien werden über .gitignore vom Git-Tracking ausgeschlossen. 

9. Fazit 

Das Projekt verbindet relationale Datenbanke, SQL-Analysen, Python-basierte Datenverarbeitung, Datenvisualisierung, Workflow-Orchestrierung und Event-Streaming. 

Es zeigt den Aufbau einer Pipeline von der synthetischen Datengenerierung über die Speicherung und Analyse bis zur automatisierten Verarbeitung und Übertragung von Produktionsereginissen. 

Das Projekt dient als praktisches Portfolio-Beispiel für Kenntnisse in SQL, Python und Data Engineering im automobilen Produktonsumfeld. 








