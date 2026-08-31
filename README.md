# AUTORIA-Baukasten v1.3 — AP1-Prüfungssimulationen

Setzt den Masterprompt **AP1 v4.6** maschinell um. Aus einer Satzspezifikation
entstehen alle Artefakte nach §11.2, die Checkliste nach §14.1 läuft automatisch,
das Ergebnis ist ein ZIP nach §18.7 plus Ampelbericht nach §14.2.

## Schnellstart

```bash
pip install python-docx openpyxl matplotlib pillow --break-system-packages
python3 run.py saetze/nr04.py
```

Ergebnis: `ausgabe/AP1-Nr04-V4-6.zip` und ein Ampelbericht auf der Konsole.

Für jeden Folgesatz gehören zwei Dateien dazu — die Historie des Vorgängers
(§11.7) und der Reihenplan (§10):

```bash
python3 run.py saetze/nr05.py \
    --historie ausgabe/AP1-Nr04-V4-6_Historie.json \
    --reihenplan AP1-Reihenplan_Nr04-Nr29.json
```

Ohne `--reihenplan` läuft der Satz durch, die Pflichtbelegung nach §10.3 wird
aber nicht fortgeschrieben; der Ampelbericht meldet das als Gelb.

## Voraussetzungen

| Was | Wofür | Pflicht |
|---|---|---|
| Python 3.10+ | alles | ja |
| python-docx, openpyxl | Word- und Excel-Dateien | ja |
| Pillow | Schriftbreitenmessung für das Layout | ja |
| matplotlib | Diagramm-Gestaltungsmuster | nur für Musterbilder |
| LibreOffice (`soffice`) | PDF-Export und Rechenprobe | dringend empfohlen |
| Liberation Sans | metrisch identisch mit Arial | für exaktes Layout |

Ohne LibreOffice entfallen PDF-Export und Rechenprobe. Der Ampelbericht meldet
das dann als **Rot** — fehlende Prüfmöglichkeit ist kein Bestehen (§14.2).

## Ordner

```
autoria/        Baukasten (nicht ändern, außer du willst Regeln anpassen)
  layout.py     Schriftbreiten, Spaltenbreiten, Punkte-Umbruch
  docxbau.py    Word-Bausteine, echte Fußnoten, Goldberg-Vorlagen
  xlsxbau.py    Arbeitsmappe mit echten Formeln
  dokumente.py  Aufgabenbogen, Materialheft, Bewertungsbogen, Handreichung
  pruefung.py   Checkliste §14.1 und Ampelbericht §14.2
  lauf.py       Orchestrierung, Historie, ZIP
  muster.py     Diagramm-Gestaltungsmuster
  reihe.py      Sperrlisten §10.1 und §10.2, Pflichtbelegung §10.3
saetze/         eine Datei je Prüfungssatz — hier arbeitest du
vorlagen/       die sieben Goldberg-Wordvorlagen (bereits enthalten)
bilder/         Musterbilder für die Anlagen
arbeit/         Zwischenstände je Satz
ausgabe/        die fertigen ZIPs
```

## Einen neuen Satz anlegen

1. `saetze/nr01.py` kopieren, etwa nach `saetze/nr02.py`.
2. **Kontrollrechnung oben** anpassen: Stammdaten, Angebote, Schwellenwerte. Sie
   rechnet unabhängig von Excel und liefert die Sollwerte für die Rechenprobe.
   Der Block `erwartete_werte` verweist darauf — er ist das Rückgrat von §14.1
   Punkt 3.
3. **Blätter** anpassen: das Blatt mit `"art": "auswertung"` trägt die Spalten mit
   `formel` beziehungsweise `werte`. Platzhalter in Formeln: `{z}` für die
   laufende Zeile, `{erste}` und `{letzte}` für den Bereich.
4. **Aufgaben, Anlagen, Bewertung, Handreichung** austauschen.
5. `historie_eintrag` füllen — er landet in der Historie-JSON.
6. Lauf starten. Der Ampelbericht sagt, was noch offen ist.

## Was der Lauf automatisch sicherstellt

- Punktesumme exakt, je Aufgabe Teilaufgaben plus 2 Formatpunkte (§9.1, §5.2)
- Deckungsabgleich Aufgabenbogen ↔ Bewertungsbogen, je Aufgabe eine Formatzeile
  (§14.1 Punkt 6, §9.3)
- Obergrenzen für Teilaufgaben: 12 / 8 / 5 (§5.4)
- Funktionsrahmen gegen Anhang D.3 — englische Formelnamen werden übersetzt
- Rechenprobe: LibreOffice berechnet die Lösungsdatei neu, Abgleich gegen die
  Kontrollrechnung (§14.1 Punkt 3)
- Teilnehmerdatei: Bearbeitungsbereich leer, Stammdatenblätter gefüllt, kein
  Diagramm (§6.1, §15.3)
- Vollständigkeit aller Artefakte; ohne sie kein ZIP (§18.7)
- Layout: feste Spaltenbreiten ohne Worttrennung mitten im Wort, Punktangaben
  rechtsbündig ohne Kleben oder Verrutschen, Seitenlogik des Aufgabenbogens
  (§18.3, §18.4)
- Kennzeichnung nach §20.3 auf dem Deckblatt, Hilfsmittelangabe wörtlich

## Was der Lauf nicht kann

Der Ampelbericht meldet diese Punkte selbst — sie bleiben deine Aufgabe:

- **Zielsoftware:** Geprüft wird mit LibreOffice. Die Lösungsdateien einmal in
  Word und Excel öffnen, besonders Fußnoten und Diagramme.
- **Sperrlisten §10.1:** Nur prüfbar, wenn du die Historie mitgibst. Ohne sie
  beginnt die Historie neu.
- **Eindeutigkeit §4.3, Eigenständigkeit §20:** inhaltliche Prüfungen.
- **Bearbeitungszeit §5.4:** wird übernommen, nicht nachgerechnet.

## Technische Hinweise

**Fußnoten.** python-docx kann keine. `docxbau.fussnoten_einfuegen` entpackt das
fertige docx, erzeugt `footnotes.xml` und hängt es in Content-Types und
Relationships ein. Der Marker (`@@FN1@@`) muss in einem **eigenen Run** stehen —
in der Spezifikation über die `teile`-Liste eines Absatzes.

**Formeln.** openpyxl schreibt englisch mit Komma: `=IF(OR(N4>168,O4<35),…)`.
Excel zeigt in deutscher Oberfläche `=WENN(ODER(…);…)`. Im Bewertungsbogen
stehen die deutschen Namen, weil ihn die Lehrkraft liest.

**Tabellenbreiten.** Feste Breiten brauchen dreierlei: `tblLayout=fixed`, Breite
an jeder Spalte **und** an jeder Zelle. Fehlt eines, verteilt Word neu und
Spaltenüberschriften brechen mitten im Wort. `layout.auto_breiten` misst vorher
das breiteste unteilbare Wort je Spalte — Kopfzeilen fett, Daten normal.

**Geldbeträge in Tabellen.** `layout.eur()` setzt ein geschütztes Leerzeichen vor
das Eurozeichen, damit der Betrag nicht umbricht.

**Goldberg-Vorlagen.** Werden kopiert und befüllt, nie nachgebaut (§11.6).
Schriftart und -größe werden beim Befüllen nicht gesetzt, sie kommen aus der
Formatvorlage. Fehlt eine Vorlage, bricht der Lauf ab statt ein Ersatzlayout zu
bauen.

**Querformat.** Anlagen mit `"quer": True` bekommen einen eigenen Abschnitt.
Sinnvoll ab etwa sieben Tabellenspalten und für Diagrammmuster.
