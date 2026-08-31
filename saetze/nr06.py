# -*- coding: utf-8 -*-
"""Satzspezifikation AP1-Nr06-V4-6 — Probezeitgespräche und Fristenkontrolle.

Setzt den Planeintrag Nr06 des Reihenplans um: Abteilung Personal/Ausbildung,
Stoffschwerpunkt Dreisatz, Säulendiagramm über die Gespräche je Monat,
Serienbrief mit Bedingungsfeld nach Standort.

Abweichung vom Planeintrag: Der Plan sieht als Kommunikationsform die
Einladung vor. Damit wären Textverarbeitungsobjekt und Kommunikationsform
dieselbe Textsorte — in der ganzen Reihe der einzige Satz, bei dem die beiden
Varianzachsen des §10 zusammenfallen. Nach Rücksprache steht hier deshalb ein
Aktenvermerk; die Einladung wandert in einen Satz ohne Serienbrief.
"""
import datetime as dt

SATZNAME = "AP1-Nr06-V4-6"

# ============================================================ Kontrollrechnung
# Die Probezeit dauert 180 Kalendertage. Das Gespräch soll spätestens 14 Tage
# vor Ablauf geführt sein, die Frist gilt also ab 167 Tagen als kritisch.
PROBEZEIT_TAGE = 180
VORLAUF_TAGE = 14
GRENZE_TAGE = PROBEZEIT_TAGE - VORLAUF_TAGE          # 166, kritisch ab 167

# Richtwert für den Dreisatz (§7: Wirtschaftsrechnen, Dreisatz).
ERFAHRUNG_GESPRAECHE = 12
ERFAHRUNG_MINUTEN = 540

STANDORTE = ["Berlin", "Leipzig", "Hamburg"]

# Beim Zahlenentwurf nach §6.1 beachtet:
# - Brandt trifft mit 166 Tagen die Grenze exakt; nur so trennt sich > von >=.
# - Die Termine laufen über den Jahreswechsel, deshalb liefert JAHR zwei
#   verschiedene Werte statt einer Konstanten.
# - Fünf Gespräche liegen in der ersten, drei in der zweiten Monatshälfte.
MITARBEITENDE = [
    (70301, "Ahrens, Nele", "Frau", "Nele", "Ahrens", "Berlin",
     dt.date(2026, 4, 1), dt.date(2026, 9, 10), dt.time(9, 0)),
    (70302, "Brandt, Ilja", "Herr", "Ilja", "Brandt", "Leipzig",
     dt.date(2026, 4, 15), dt.date(2026, 9, 28), dt.time(10, 30)),
    (70303, "Cordes, Milan", "Herr", "Milan", "Cordes", "Hamburg",
     dt.date(2026, 5, 4), dt.date(2026, 10, 20), dt.time(9, 30)),
    (70304, "Dressler, Ayse", "Frau", "Ayse", "Dressler", "Berlin",
     dt.date(2026, 5, 18), dt.date(2026, 10, 30), dt.time(14, 0)),
    (70305, "Ewers, Tomke", "Frau", "Tomke", "Ewers", "Leipzig",
     dt.date(2026, 6, 1), dt.date(2026, 11, 24), dt.time(11, 0)),
    (70306, "Fischer, Lars", "Herr", "Lars", "Fischer", "Berlin",
     dt.date(2026, 6, 22), dt.date(2026, 12, 4), dt.time(13, 30)),
    (70307, "Gerlach, Svea", "Frau", "Svea", "Gerlach", "Hamburg",
     dt.date(2026, 7, 6), dt.date(2027, 1, 8), dt.time(10, 0)),
    (70308, "Hoffmann, Nils", "Herr", "Nils", "Hoffmann", "Leipzig",
     dt.date(2026, 8, 3), dt.date(2027, 2, 2), dt.time(15, 0)),
]

ERSTE_ZEILE = 4
ANZAHL_MA = len(MITARBEITENDE)
MONAT_ERSTE = 19                                     # erste Zeile Monatsblock

# Die Termine laufen von September bis Februar, deshalb diese Reihenfolge.
MONATE = [("September 2026", 9), ("Oktober 2026", 10), ("November 2026", 11),
          ("Dezember 2026", 12), ("Januar 2027", 1), ("Februar 2027", 2)]


def _rechnen():
    rows = []
    for (nr, name, anrede, vor, nach, ort, ein, term, uhr) in MITARBEITENDE:
        tage = (term - ein).days
        rows.append(dict(nr=nr, name=name, anrede=anrede,
                         briefanrede=("Sehr geehrte" if anrede == "Frau"
                                      else "Sehr geehrter"),
                         vorname=vor,
                         nachname=nach, ort=ort, eintritt=ein, termin=term,
                         uhrzeit=uhr, jahr=term.year, monat=term.month,
                         tage=tage,
                         haelfte=("erste Hälfte" if term.day <= 15
                                  else "zweite Hälfte"),
                         urteil=("kritisch" if tage > GRENZE_TAGE
                                 else "rechtzeitig")))
    return rows


Z = _rechnen()
ANZ_KRITISCH = sum(1 for r in Z if r["urteil"] == "kritisch")
MONATSZAHLEN = [sum(1 for r in Z if r["monat"] == m) for _n, m in MONATE]
ZEITBEDARF = ERFAHRUNG_MINUTEN / ERFAHRUNG_GESPRAECHE * ANZAHL_MA


def _datum(d):
    return d.strftime("%d.%m.%Y")


def _uhr(t):
    return t.strftime("%H:%M")


# ==================================================================== Textteile
SACHVERHALT = (
    "Die Goldberg Designermöbel GmbH beschäftigt an den Standorten Berlin, "
    "Leipzig und Hamburg acht Mitarbeiterinnen und Mitarbeiter, deren Probezeit "
    "in den kommenden Monaten endet. Die Probezeit dauert 180 Kalendertage; das "
    "Probezeitgespräch soll spätestens 14 Tage vor Ablauf geführt sein. Frau Sina "
    "Reinbold, Leiterin der Abteilung Personal/Ausbildung, bittet Sie, die "
    "Fristen zu prüfen, die Einladungen zum Gespräch als Serienbrief "
    "vorzubereiten und das Ergebnis der Fristenkontrolle in einem Aktenvermerk "
    "festzuhalten."
)

HINWEISE = [
    ("Ablage der Dateien",
     "Legen Sie einen Ordner mit dem Namen AP1 an. Kopieren Sie die ZIP-Datei in "
     "diesen Ordner und entpacken Sie sie dort. Bearbeiten Sie die Aufgaben "
     "ausschließlich in den entpackten Dateien und speichern Sie diese im selben "
     "Ordner."),
    ("Dateibenennung",
     "Speichern Sie jede bearbeitete Datei unter Ihrer Teilnehmernummer und der "
     "Aufgabennummer. Die Teilnehmernummer besteht aus Ihrem Nachnamen und dem "
     "heutigen Tagesdatum im Format TTMM, also Tag und Monat je zweistellig. "
     "Beispiel: Weber1708_A1.xlsx."),
    ("Anlagen",
     "Die Anlagen 1 bis 5 stehen im Materialheft. Jede Aufgabe nennt die Anlagen, "
     "die dafür gebraucht werden. Die Anlagen werden nicht bearbeitet."),
    ("Punkte",
     "Die Punktzahl steht hinter jeder Teilaufgabe. In jeder Aufgabe entfallen "
     "zusätzlich 2 Punkte auf die Einhaltung der Formatvorgaben. Verwenden Sie "
     "überall dort Formeln, die Sie nach unten kopieren können, wo mehrere Zeilen "
     "gleichartig berechnet werden."),
    ("Umsatzsteuer",
     "Alle Beträge in den Anlagen und Dateien sind Nettobeträge; der "
     "Umsatzsteuersatz beträgt 19 Prozent."),
]

FORMATVORGABEN = [
    ["Datum", "TT.MM.JJJJ"],
    ["Uhrzeit", "SS:MM"],
    ["Personalnummern", "ganze Zahl, ohne Tausenderpunkt"],
    ["Zeitspannen in Tagen", "ganze Zahl, ohne Tausenderpunkt"],
    ["Zeitspannen in Minuten", "ganze Zahl, ohne Tausenderpunkt"],
    ["Mengen und Stückzahlen", "ohne Dezimalstellen, ab fünf Stellen mit "
                               "Tausenderpunkt"],
    ["Schrift in allen Dateien", "Arial 11 pt"],
    ["Diagramm", "Titel, Legende und Achsenbeschriftung sichtbar"],
]

# ------------------------------------------------------------ Serienbrief A2
SB_UEBERSCHRIFT = "Einladung zum Probezeitgespräch"
# Der erste Absatz trägt die Seriendruckfelder und das Bedingungsfeld. Er
# beginnt klein, weil er die Anrede fortsetzt (§6.3).
SB_ABSATZ1 = ("am {termin} um {uhrzeit} Uhr möchten wir mit Ihnen das "
              "Probezeitgespräch führen. Das Gespräch findet {ort} statt und "
              "dauert etwa 45 Minuten.")
SB_LUECKE = "\u2026\u2026\u2026\u2026\u2026"
SB_ABSAETZE = [
    "Es geht um Ihre bisherige Einarbeitung, um Ihre Aufgaben im kommenden Jahr "
    "und um den weiteren Verlauf des Arbeitsverhältnisses. Bitte bringen Sie "
    "Ihre Einarbeitungsunterlagen mit.",
    "Sollte Ihnen der Termin nicht möglich sein, melden Sie sich bitte bis eine "
    "Woche vorher in der Personalabteilung.",
]
SB_GRUSS = "Mit freundlichen Grüßen"
SB_UNTERSCHRIFT = ["Goldberg Designermöbel GmbH", "Sina Reinbold",
                   "Leiterin Personal/Ausbildung"]
# Das Bedingungsfeld unterscheidet nach Standort (Planeintrag Nr06).
SB_ORT_BERLIN = "in der Zentrale, Raum 2.14"
SB_ORT_UEBRIGE = "in Ihrem Standortbüro"


# ================================================================ Spezifikation
def spec():
    dateien = {"a1": f"{SATZNAME}_A1_Teilnehmer.xlsx",
               "a2": f"{SATZNAME}_A2_Teilnehmer.docx",
               "a3": f"{SATZNAME}_A3_Teilnehmer.docx"}
    m_erste = MONAT_ERSTE
    m_letzte = MONAT_ERSTE + len(MONATE) - 1              # 24

    return {
        "meta": {
            "satzname": SATZNAME,
            "reihe": "AP1 Prüfungssimulationen Goldberg Designermöbel GmbH",
            "hinweis": ("Der Satz setzt den Planeintrag Nr06 um. Abweichend vom "
                        "Plan steht als Kommunikationsform ein Aktenvermerk "
                        "statt einer Einladung, weil sonst Serienbrief und "
                        "Kommunikationsaufgabe dieselbe Textsorte wären und die "
                        "Varianz nach §10 an dieser Stelle verloren ginge. Die "
                        "Einladung ist damit noch offen und gehört in einen "
                        "Satz ohne Serienbrief."),
            "bezeichnung": ["Abschlussprüfung Teil 1",
                            "Kaufleute für Büromanagement",
                            "Informationstechnisches Büromanagement"],
            "bearbeitungszeit": 120,
            "gesamtpunkte": 100,
        },
        "fettbegriffe": list(dateien.values()) + ["Frist", "Teiln"],
        "sachverhalt": SACHVERHALT,
        "hinweise": HINWEISE,
        "formatvorgaben": FORMATVORGABEN,

        # ---------------------------------------------------------- Arbeitsmappe
        "aktives_blatt": "Sem",
        "blaetter": [
            {"name": "Sem", "titel": "Seminarplanung laufendes Jahr",
             "kopf": ["Seminar", "Referent/-in", "Termin", "Plätze",
                      "Angemeldet"],
             "formate": [None, None, "datum", "ganz", "ganz"],
             "zeilen": [["Arbeitsrecht kompakt", "Dr. Weinhold, Anke",
                         dt.date(2026, 9, 15), 16, 14],
                        ["Gesprächsführung", "Petersen, Rolf",
                         dt.date(2026, 10, 6), 12, 12],
                        ["Zeitmanagement", "Kabelac, Mira",
                         dt.date(2026, 11, 10), 20, 9],
                        ["Warenkunde Massivholz", "Thelen, Kaan",
                         dt.date(2027, 1, 19), 14, 11]]},

            {"name": "Frist", "art": "auswertung",
             "titel": "Fristenkontrolle Probezeitgespräche",
             "anzahl_zeilen": ANZAHL_MA,
             "spalten": [
                 {"kopf": "Personal-nummer", "breite": 24, "format": "ganz",
                  "ausrichtung": "center", "werte": [r["nr"] for r in Z]},
                 {"kopf": "Name", "art": "text", "breite": 20,
                  "werte": [r["name"] for r in Z]},
                 {"kopf": "Standort", "art": "text", "breite": 13,
                  "werte": [r["ort"] for r in Z]},
                 {"kopf": "Eintritt", "breite": 13, "format": "datum",
                  "werte": [r["eintritt"] for r in Z]},
                 {"kopf": "Gesprächs-termin", "breite": 14, "format": "datum",
                  "formel": "=VLOOKUP(A{z},Teiln!$A$4:$H$11,7,FALSE)"},
                 {"kopf": "Jahr des Gesprächs", "breite": 12, "format": "ganz",
                  "formel": "=YEAR(E{z})"},
                 {"kopf": "Monat des Gesprächs", "breite": 12, "format": "ganz",
                  "formel": "=MONTH(E{z})"},
                 {"kopf": "Tage von Eintritt bis Gespräch", "breite": 14,
                  "format": "ganz", "formel": "=E{z}-D{z}"},
                 {"kopf": "Zeitpunkt im Monat", "breite": 16,
                  "ausrichtung": "center",
                  "formel": '=IF(DAY(E{z})<=15,"erste Hälfte","zweite Hälfte")'},
                 {"kopf": "Beurteilung", "breite": 14, "ausrichtung": "center",
                  "formel": '=IF(H{z}>%d,"kritisch","rechtzeitig")'
                            % GRENZE_TAGE},
             ],
             "festzellen": [
                 {"zelle": "A13", "text": "Kennzahlen", "fett": True},
                 {"zelle": "A17", "text": "Gespräche je Monat", "fett": True},
                 {"zelle": "A18", "text": "Monat", "fett": True, "rahmen": True},
                 {"zelle": "B18", "text": "Monatszahl", "fett": True,
                  "rahmen": True, "ausrichtung": "center"},
                 {"zelle": "C18", "text": "Gespräche", "fett": True,
                  "rahmen": True, "ausrichtung": "center"},
                 {"zelle": "A26", "text": "Zeitplanung", "fett": True},
             ] + [{"zelle": f"A{m_erste + i}", "text": n, "rahmen": True}
                  for i, (n, _z) in enumerate(MONATE)]
               + [{"zelle": f"B{m_erste + i}", "text": z, "rahmen": True}
                  for i, (_n, z) in enumerate(MONATE)],
             "einzelzellen": [
                 {"label": "Stand der Auswertung", "label_zelle": "A14",
                  "zelle": "B14", "format": "datum", "formel": "=TODAY()"},
                 {"label": "Kritische Fristen", "label_zelle": "A15",
                  "zelle": "B15", "format": "ganz",
                  "formel": '=COUNTIF(J{erste}:J{letzte},"kritisch")'},
                 {"label": "Gespräche im Richtwert", "label_zelle": "A27",
                  "zelle": "B27", "format": "ganz",
                  "formel": "=%d" % ERFAHRUNG_GESPRAECHE},
                 {"label": "Minuten im Richtwert", "label_zelle": "A28",
                  "zelle": "B28", "format": "ganz",
                  "formel": "=%d" % ERFAHRUNG_MINUTEN},
                 {"label": "Zeitbedarf in Minuten",
                  "label_zelle": "A29", "zelle": "B29", "format": "ganz",
                  "formel": "=B28/B27*SUM(C%d:C%d)" % (m_erste, m_letzte)},
             ] + [{"zelle": f"C{m_erste + i}", "format": "ganz",
                   "formel": "=COUNTIF($G${erste}:$G${letzte},B%d)"
                             % (m_erste + i)}
                  for i in range(len(MONATE))],
             "diagramm": {"typ": "saeule", "wertespalte": 3, "rubrikspalte": 1,
                          "werte_zeilen": (18, m_letzte),
                          "rubrik_zeilen": (m_erste, m_letzte),
                          "titel": "Probezeitgespräche je Monat",
                          "wertachse": "Anzahl der Gespräche",
                          "rubrikachse": "Monat", "position": "A32",
                          "legende": "unten",
                          "breite": 15.5, "hoehe": 8.0}},

            {"name": "Teiln", "titel": "Mitarbeitende in der Probezeit",
             "stammdaten": True,
             "kopf": ["Personal-nummer", "Anrede", "Briefanrede", "Vorname",
                      "Nachname", "Standort", "Gesprächstermin", "Uhrzeit"],
             "breiten": [13, 10, 16, 14, 16, 13, 15, 11],
             "formate": ["ganz", None, None, None, None, None, "datum",
                         "zeit"],
             "zeilen": [[r["nr"], r["anrede"], r["briefanrede"], r["vorname"],
                         r["nachname"], r["ort"], r["termin"], r["uhrzeit"]]
                        for r in Z]},

            {"name": "Fehlz", "titel": "Fehlzeiten laufendes Jahr",
             "kopf": ["Personal-nummer", "Grund", "Von", "Bis", "Arbeitstage"],
             "formate": ["ganz", None, "datum", "datum", "ganz"],
             "zeilen": [[70214, "Krankheit", dt.date(2026, 3, 9),
                         dt.date(2026, 3, 13), 5],
                        [70231, "Fortbildung", dt.date(2026, 4, 20),
                         dt.date(2026, 4, 24), 5],
                        [70238, "Krankheit", dt.date(2026, 5, 26),
                         dt.date(2026, 5, 29), 4],
                        [70251, "Sonderurlaub", dt.date(2026, 6, 15),
                         dt.date(2026, 6, 16), 2],
                        [70259, "Fortbildung", dt.date(2026, 7, 13),
                         dt.date(2026, 7, 17), 5]]},

            {"name": "Stand", "titel": "Standorte und Anschriften",
             "kopf": ["Standort", "Straße", "PLZ", "Ort", "Beschäftigte"],
             "formate": [None, None, None, None, "ganz"],
             "zeilen": [["Berlin", "Lorenzistraße 14", "10437", "Berlin", 96],
                        ["Leipzig", "Kärrnerweg 8", "04229", "Leipzig", 41],
                        ["Hamburg", "Buchsbaumallee 3", "22297", "Hamburg", 27]]},

            {"name": "Ausb", "titel": "Auszubildende im laufenden Jahrgang",
             "kopf": ["Name", "Beruf", "Lehrjahr", "Berufsschultag"],
             "formate": [None, None, "ganz", None],
             "zeilen": [["Barisch, Levin", "Kaufmann für Büromanagement", 1,
                         "Dienstag"],
                        ["Deppe, Marlene", "Kauffrau für Büromanagement", 2,
                         "Donnerstag"],
                        ["Kilic, Emre", "Holzmechaniker", 2, "Mittwoch"],
                        ["Sanwald, Frieda", "Kauffrau für Büromanagement", 3,
                         "Dienstag"]]},

            {"name": "Tel", "titel": "Telefonverzeichnis",
             "kopf": ["Durchwahl", "Name", "Abteilung", "Funktion"],
             "zeilen": [["357-150", "Reinbold, Sina", "Personal/Ausbildung",
                         "Abteilungsleitung"],
                        ["357-152", "Marquardt, Ove", "Personal/Ausbildung",
                         "Sachbearbeitung"],
                        ["357-120", "Winkelmann, Ute",
                         "Verwaltung/Büroorganisation", "Abteilungsleitung"],
                        ["357-110", "Kortmann, Ines", "Beschaffung/Einkauf",
                         "Abteilungsleitung"],
                        ["357-140", "Osterkamp, Jan", "Lager/Logistik",
                         "Abteilungsleitung"],
                        ["357-160", "Thelen, Kaan", "Vertrieb",
                         "Sachbearbeitung"]]},
        ],

        # Sollwerte für die Rechenprobe (§14.1 Punkt 3).
        "erwartete_werte": {
            **{f"Frist!E{ERSTE_ZEILE + i}": dt.datetime.combine(
                Z[i]["termin"], dt.time()) for i in range(ANZAHL_MA)},
            **{f"Frist!F{ERSTE_ZEILE + i}": Z[i]["jahr"]
               for i in range(ANZAHL_MA)},
            **{f"Frist!G{ERSTE_ZEILE + i}": Z[i]["monat"]
               for i in range(ANZAHL_MA)},
            **{f"Frist!H{ERSTE_ZEILE + i}": Z[i]["tage"]
               for i in range(ANZAHL_MA)},
            **{f"Frist!I{ERSTE_ZEILE + i}": Z[i]["haelfte"]
               for i in range(ANZAHL_MA)},
            **{f"Frist!J{ERSTE_ZEILE + i}": Z[i]["urteil"]
               for i in range(ANZAHL_MA)},
            "Frist!B14": dt.datetime.combine(dt.date.today(), dt.time()),
            "Frist!B15": ANZ_KRITISCH,
            **{f"Frist!C{m_erste + i}": MONATSZAHLEN[i]
               for i in range(len(MONATE))},
            "Frist!B29": ZEITBEDARF,
        },

        # ------------------------------------------------------------- Aufgaben
        "aufgaben": [
            {"nr": 1, "typ": "tabellenkalkulation", "titel": "Tabellenkalkulation",
             "punkte": 46,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a1']}. Sie arbeiten "
                            "im Blatt Frist. Die Angaben zu den Mitarbeitenden "
                            "stehen im Blatt Teiln."),
             "teilaufgaben": [
                 ("a", "Übertragen Sie die acht Mitarbeitenden aus Anlage 2 in "
                       "den Bereich A4 bis D11 des Blattes Frist. Halten Sie "
                       "die Reihenfolge der Anlage ein.", 5),
                 ("b", "Ermitteln Sie in Spalte E den Gesprächstermin. Die "
                       "Termine stehen im Blatt Teiln.", 4),
                 ("c", "Ermitteln Sie in Spalte F das Jahr des Gesprächs.", 3),
                 ("d", "Ermitteln Sie in Spalte G den Monat des Gesprächs.", 3),
                 ("e", "Ermitteln Sie in Spalte H die Zahl der Tage zwischen "
                       "dem Eintritt und dem Gesprächstermin.", 4),
                 ("f", "Geben Sie in Spalte I aus, ob das Gespräch in der "
                       "ersten oder in der zweiten Monatshälfte liegt. Zur "
                       "ersten Hälfte zählen die Tage 1 bis 15.", 4),
                 ("g", "Geben Sie in Spalte J eine Beurteilung aus. Es soll "
                       "@@kritisch@@ erscheinen, wenn zwischen Eintritt und "
                       "Gespräch mehr als 166 Tage liegen. In allen anderen "
                       "Fällen soll @@rechtzeitig@@ erscheinen.", 4),
                 ("h", "Ermitteln Sie in Zelle B14 das Tagesdatum. Der Wert "
                       "soll sich beim Öffnen der Datei aktualisieren.", 2),
                 ("i", "Ermitteln Sie in Zelle B15 die Anzahl der kritischen "
                       "Fristen.", 3),
                 ("j", "Ermitteln Sie im Bereich C19 bis C24 die Anzahl der "
                       "Gespräche je Monat.", 4),
                 ("k", "Ermitteln Sie in Zelle B29 den Zeitbedarf für alle "
                       "Gespräche in Minuten. Rechnen Sie mit dem "
                       "Richtwert aus den Zellen B27 und B28.", 4),
                 ("l", "Erstellen Sie im Blatt Frist ab Zelle A32 ein "
                       "Säulendiagramm zu den Gesprächen je Monat. Gestalten "
                       "Sie es nach dem Muster in Anlage 5.", 4),
             ]},
            {"nr": 2, "typ": "textverarbeitung", "titel": "Textverarbeitung",
             "punkte": 32,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a2']}. Sie "
                            "enthält das Hauptdokument der Einladung. Der "
                            "Feldplan steht in Anlage 3."),
             "teilaufgaben": [
                 ("a", "Richten Sie die Datei als Serienbrief ein und "
                       "verbinden Sie als Datenquelle das Blatt Teiln der "
                       f"Datei {dateien['a1']}.", 5),
                 ("b", "Fügen Sie im Anschriftfeld die Seriendruckfelder für "
                       "Anrede, Vorname und Nachname ein.", 6),
                 ("c", "Fügen Sie in der Anredezeile die Seriendruckfelder für "
                       "Anrede und Nachname ein. Die Zeile soll lauten: Sehr "
                       "geehrte Frau Ahrens, beziehungsweise Sehr geehrter "
                       "Herr Brandt,", 6),
                 ("d", "Fügen Sie im ersten Absatz die Seriendruckfelder für "
                       "den Gesprächstermin und die Uhrzeit ein und ergänzen "
                       "Sie ein Bedingungsfeld für den Ort: Am Standort Berlin "
                       "soll @@in der Zentrale, Raum 2.14@@ erscheinen, an "
                       "allen anderen Standorten @@in Ihrem Standortbüro@@.", 9),
                 ("e", "Führen Sie den Seriendruck zusammen und speichern Sie "
                       "das Ergebnis mit den acht fertigen Einladungen.", 4),
             ]},
            {"nr": 3, "typ": "kommunikation",
             "titel": "Geschäftliche Kommunikation", "punkte": 22,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a3']}. Das Datum "
                            "ist bereits eingetragen. Die Angaben für den "
                            "Aktenvermerk stehen in Anlage 4. Beachten Sie "
                            "DIN 5008:2020."),
             "teilaufgaben": [
                 ("a", "Vervollständigen Sie die Felder Betreff und "
                       "Sachbearbeiter/-in.", 4),
                 ("b", "Halten Sie einleitend fest, was geprüft wurde und "
                       "welchen Zeitraum die Fristenkontrolle umfasst.", 5),
                 ("c", "Halten Sie das Ergebnis fest: die Anzahl der "
                       "kritischen Fristen und den Zeitbedarf für alle "
                       "Gespräche.", 7),
                 ("d", "Halten Sie fest, was veranlasst wurde, und nennen Sie "
                       "einen Termin zur Wiedervorlage.", 4),
             ]},
        ],

        # -------------------------------------------------------------- Anlagen
        "anlagen": [
            {"nr": 1, "titel": "E-Mail der Personalleitung",
             "gehoert_zu": "Aufgaben 1 bis 3",
             "bloecke": [
                 {"typ": "felder", "paare": [
                     ("Von", "sina.reinbold@goldberg.test"),
                     ("An", "personal@goldberg.test"),
                     ("Datum", "26.08.2026"),
                     ("Betreff", "Probezeitgespräche – Fristenkontrolle, "
                                 "Einladungen und Aktenvermerk")]},
                 {"typ": "absaetze", "zeilen": [
                     "Guten Morgen,", "",
                     "bei acht Mitarbeiterinnen und Mitarbeitern endet die "
                     "Probezeit in den kommenden Monaten. Die Übersicht finden "
                     "Sie in Anlage 2, die persönlichen Angaben stehen im Blatt "
                     "Teiln der Arbeitsmappe.", "",
                     "Bitte prüfen Sie zuerst die Fristen. Die Probezeit dauert "
                     "180 Kalendertage, und das Gespräch soll spätestens 14 Tage "
                     "vor Ablauf geführt sein. Ich möchte wissen, bei wem es eng "
                     "wird und wie sich die Gespräche über die Monate verteilen.",
                     "",
                     "Anschließend bereiten Sie bitte die Einladungen als "
                     "Serienbrief vor. Der Feldplan steht in Anlage 3. Achten "
                     "Sie darauf, dass der Ort des Gesprächs vom Standort "
                     "abhängt.", "",
                     "Das Ergebnis der Fristenkontrolle halten Sie bitte in "
                     "einem Aktenvermerk fest; die Angaben dazu stehen in "
                     "Anlage 4.", "",
                     "Vielen Dank und freundliche Grüße", "Sina Reinbold",
                     "Leiterin Personal/Ausbildung"]},
             ]},
            {"nr": 2, "titel": "Übersicht der Probezeiten",
             "gehoert_zu": "Aufgabe 1",
             "bloecke": [
                 {"typ": "text", "text": "Übertragen Sie die folgenden Angaben "
                                         "positionsgerecht in die "
                                         "Auswertungstabelle."},
                 {"typ": "tabelle",
                  "kopf": ["Personal-nummer", "Name", "Standort", "Eintritt"],
                  "zeilen": [[str(r["nr"]), r["name"], r["ort"],
                              _datum(r["eintritt"])] for r in Z],
                  "zahlenspalten": [0, 3]},
                 {"typ": "ueberschrift", "text": "Regeln der Fristenkontrolle"},
                 {"typ": "liste", "zeilen": [
                     "Die Probezeit dauert 180 Kalendertage, gerechnet ab dem "
                     "Tag des Eintritts.",
                     "Das Probezeitgespräch soll spätestens 14 Tage vor Ablauf "
                     "der Probezeit geführt sein. Liegen zwischen Eintritt und "
                     "Gespräch mehr als 166 Tage, ist die Frist kritisch.",
                     "Die Gesprächstermine sind bereits vereinbart und stehen "
                     "im Blatt Teiln der Arbeitsmappe.",
                     "Für die Zeitplanung gilt der Richtwert der "
                     "Abteilung: 12 Gespräche binden 540 Minuten."]},
             ]},
            {"nr": 3, "titel": "Feldplan für den Serienbrief",
             "gehoert_zu": "Aufgabe 2",
             "bloecke": [
                 {"typ": "text", "text":
                     "Der Text der Einladung steht bereits in der Datei. An den "
                     "unten genannten Stellen werden die Seriendruckfelder "
                     "eingefügt. Die Datenquelle ist das Blatt Teiln der "
                     "Arbeitsmappe zu Aufgabe 1."},
                 {"typ": "ueberschrift", "text": "Felder und ihre Stellen"},
                 {"typ": "tabelle", "kopf": ["Stelle im Dokument", "Feld"],
                  "zeilen": [["Anschriftfeld, erste Zeile", "Anrede"],
                             ["Anschriftfeld, zweite Zeile",
                              "Vorname und Nachname"],
                             ["Anredezeile", "Anrede und Nachname"],
                             ["Erster Absatz, Termin",
                              "Gesprächstermin und Uhrzeit"],
                             ["Erster Absatz, Ort", "Bedingungsfeld, "
                                                    "siehe unten"]]},
                 {"typ": "ueberschrift", "text": "Bedingung für den Ort"},
                 {"typ": "liste", "zeilen": [
                     "Ist der Standort Berlin, erscheint: in der Zentrale, "
                     "Raum 2.14",
                     "In allen anderen Fällen erscheint: in Ihrem "
                     "Standortbüro",
                     "Die Bedingung wird über ein Bedingungsfeld gelöst, nicht "
                     "über acht einzeln bearbeitete Briefe."]},
             ]},
            {"nr": 4, "titel": "Notiz für den Aktenvermerk",
             "gehoert_zu": "Aufgabe 3",
             "bloecke": [
                 {"typ": "felder", "paare": [
                     ("Datum", "27.08.2026"),
                     ("Sachbearbeiter/-in", "Ove Marquardt, Sachbearbeitung "
                                            "Personal/Ausbildung"),
                     ("Auftrag von", "Sina Reinbold, Leiterin "
                                     "Personal/Ausbildung")]},
                 {"typ": "text", "text":
                     "Geprüft wurden die Probezeiten der acht Mitarbeitenden, "
                     "deren Probezeit zwischen September 2026 und Februar 2027 "
                     "endet. Als Betreff ist die Fristenkontrolle der "
                     "Probezeitgespräche anzugeben."},
                 {"typ": "text", "text":
                     "Die Anzahl der kritischen Fristen und den Zeitbedarf für "
                     "alle Gespräche entnehmen Sie Ihrer eigenen Auswertung aus "
                     "Aufgabe 1. Beide Werte gehören in den Aktenvermerk."},
                 {"typ": "text", "text":
                     "Veranlasst wurde die Einladung aller acht Mitarbeitenden "
                     "als Serienbrief. Die Einladungen gehen am 31.08.2026 in "
                     "den Versand. Zur Wiedervorlage ist der 15.09.2026 "
                     "vorzumerken; bis dahin sollen die Rückmeldungen zu den "
                     "Terminen vorliegen."},
                 {"typ": "text", "text":
                     "Der Aktenvermerk beginnt ohne Anrede unmittelbar mit dem "
                     "Inhalt. Er wird auf den 27.08.2026 datiert; das Datum ist "
                     "in der Datei bereits eingetragen."},
             ]},
            {"nr": 5, "titel": "Gestaltungsmuster für das Diagramm",
             "gehoert_zu": "Aufgabe 1", "quer": True,
             "bloecke": [
                 {"typ": "text", "text":
                     "Das Muster zeigt ausschließlich Aufbau und Gestaltung. "
                     "Die abgebildeten Werte und Bezeichnungen gehören nicht "
                     "zur Aufgabe.", "nach": 10},
                 {"typ": "bild", "pfad": "muster_saeule.png", "breite": 22.0},
             ]},
        ],

        # --------------------------------------------------------- Aufgabendateien
        "dateien": [
            {"art": "xlsx", "praefix": "A1"},
            {"art": "dokument", "praefix": "A2", "fusszeile": True,
             # Teilnehmerdatei: Hauptdokument ohne Datenquellenanbindung und
             # ohne Felder — beides ist Prüfungsleistung (§6.2). Die Lücken
             # markieren die Stellen, die der Feldplan in Anlage 3 benennt.
             "teilnehmer": (
                 [{"typ": "absatz", "text": SB_LUECKE, "nach": 0},
                  {"typ": "absatz", "text": SB_LUECKE, "nach": 0},
                  {"typ": "leer", "nach": 12},
                  {"typ": "ueberschrift", "text": SB_UEBERSCHRIFT,
                   "groesse": 12, "vor": 0, "nach": 12},
                  {"typ": "absatz", "text": f"{SB_LUECKE},", "nach": 12},
                  {"typ": "absatz",
                   "text": SB_ABSATZ1.format(termin=SB_LUECKE,
                                             uhrzeit=SB_LUECKE,
                                             ort=SB_LUECKE),
                   "blocksatz": True}]
                 + [{"typ": "absatz", "text": t, "blocksatz": True}
                    for t in SB_ABSAETZE]
                 + [{"typ": "absatz", "text": SB_GRUSS, "vor": 12, "nach": 24}]
                 + [{"typ": "absatz", "text": t, "nach": 0}
                    for t in SB_UNTERSCHRIFT]),
             # Lösungsdatei: das zusammengeführte Ergebnis, also die acht
             # fertigen Einladungen, nicht ein Hauptdokument mit toter
             # Verknüpfung (§6.2).
             "loesung": [b for i, r in enumerate(Z) for b in (
                 ([{"typ": "seitenumbruch"}] if i else [])
                 + [{"typ": "absatz", "text": r["anrede"], "nach": 0},
                    {"typ": "absatz",
                     "text": f"{r['vorname']} {r['nachname']}", "nach": 0},
                    {"typ": "leer", "nach": 12},
                    {"typ": "ueberschrift", "text": SB_UEBERSCHRIFT,
                     "groesse": 12, "vor": 0, "nach": 12},
                    {"typ": "absatz",
                     "text": f"{r['briefanrede']} {r['anrede']} "
                             f"{r['nachname']},", "nach": 12},
                    {"typ": "absatz", "blocksatz": True,
                     "text": SB_ABSATZ1.format(
                         termin=_datum(r["termin"]),
                         uhrzeit=_uhr(r["uhrzeit"]),
                         ort=(SB_ORT_BERLIN if r["ort"] == "Berlin"
                              else SB_ORT_UEBRIGE))}]
                 + [{"typ": "absatz", "text": t, "blocksatz": True}
                    for t in SB_ABSAETZE]
                 + [{"typ": "absatz", "text": SB_GRUSS, "vor": 12, "nach": 24}]
                 + [{"typ": "absatz", "text": t, "nach": 0}
                    for t in SB_UNTERSCHRIFT])]},
            {"art": "vorlage", "praefix": "A3", "form": "aktenvermerk",
             "teilnehmer": {"felder": {"Datum": "27.08.2026"}},
             "loesung": {
                 "felder": {
                     "Datum": "27.08.2026",
                     "Betreff": "Fristenkontrolle der Probezeitgespräche",
                     "Sachbearbeiter/-in": "Ove Marquardt, Sachbearbeitung "
                                           "Personal/Ausbildung"},
                 # Der Aktenvermerk kennt keine Anrede und beginnt deshalb
                 # groß unmittelbar mit dem Inhalt (§6.3).
                 "koerper": [
                     "Im Auftrag von Frau Sina Reinbold wurden die Probezeiten "
                     "der acht Mitarbeitenden geprüft, deren Probezeit zwischen "
                     "September 2026 und Februar 2027 endet. Grundlage sind die "
                     "vereinbarten Gesprächstermine und die Regel, dass das "
                     "Probezeitgespräch spätestens 14 Tage vor Ablauf der "
                     "Probezeit geführt sein soll.", "",
                     "Bei vier der acht Mitarbeitenden liegt die Frist im "
                     "kritischen Bereich; zwischen Eintritt und Gespräch liegen "
                     "dort mehr als 166 Tage. Für alle acht Gespräche ist nach "
                     "dem Richtwert der Abteilung ein Zeitbedarf von "
                     "360 Minuten anzusetzen.", "",
                     "Veranlasst wurde die Einladung aller acht Mitarbeitenden "
                     "als Serienbrief. Die Einladungen gehen am 31.08.2026 in "
                     "den Versand.", "",
                     "Wiedervorlage: 15.09.2026. Bis dahin sollen die "
                     "Rückmeldungen zu den Terminen vorliegen.", "",
                     "Ove Marquardt"]}},
        ],

        # ---------------------------------------------------------- Bewertung
        "bewertung": _bewertung(),

        # -------------------------------------------------------- Handreichung
        "handreichung": _handreichung(),

        # ----------------------------------------------------- Historieneintrag
        "historie_eintrag": {
            "satzname": SATZNAME, "nummer": "06",
            "satzart": "vollpruefung", "bearbeitungszeit_min": 120,
            "gesamtpunkte": 100, "abteilung": "Personal/Ausbildung",
            "szenario": "Probezeitgespräche und Fristenkontrolle mit "
                        "Zeitbedarf nach Dreisatz",
            "stoffschwerpunkt": ["wirtschaftsrechnen", "dreisatz"],
            "aufgabenzuschnitt": {"A1": 46, "A2": 32, "A3": 22},
            "diagramm": "Säulendiagramm: Probezeitgespräche je Monat",
            "tv_objekt": "Serienbrief Gesprächseinladung mit Bedingungsfeld "
                         "nach Standort",
            "kommunikationsform": "Aktenvermerk",
            "eingesetzte_funktionen": ["SVERWEIS (FALSCH)", "JAHR", "MONAT",
                                       "TAG", "HEUTE", "WENN", "ZÄHLENWENN",
                                       "SUMME"],
            "pflichtelemente_belegt": ["Serienbrief-Bedingungsfeld",
                                       "JAHR/MONAT/TAG", "HEUTE"],
            "status": "geliefert",
        },
    }


def _bewertung():
    tage = "; ".join(str(r["tage"]) for r in Z)
    urteil = "; ".join(r["urteil"] for r in Z)
    monate = "; ".join(f"{n} {MONATSZAHLEN[i]}"
                       for i, (n, _z) in enumerate(MONATE))
    return [
        {"nr": "1a", "punkte": 5,
         "leistung": "Die acht Mitarbeitenden stehen zeilengerecht in A4:D11 "
                     "des Blattes Frist, in der Reihenfolge der Anlage 2.",
         "hinweis": "Je Zeile 0,5 Punkte für die vollständige und richtige "
                    "Übernahme aller vier Angaben; 1 Punkt für die "
                    "eingehaltene Reihenfolge. Personalnummer und "
                    "Eintrittsdatum sind als Zahl beziehungsweise Datum "
                    "erfasst, nicht als Text.",
         "toleranz": "Datum als Text: 0,5 Punkte Abzug je betroffener Zeile, "
                     "weil die Differenz in Spalte H daran scheitert."},
        {"nr": "1b", "punkte": 4,
         "leistung": "Spalte E enthält je Zeile eine kopierfähige Formel, die "
                     "den Gesprächstermin aus dem Blatt Teiln holt.",
         "hinweis": "E4: =SVERWEIS(A4;Teiln!$A$4:$H$11;7;FALSCH), nach unten "
                    "kopiert. Exakte Suche über die Personalnummer.",
         "toleranz": "Fehlender absoluter Bezug bei richtigem Ergebnis: "
                     "2 Punkte Abzug. Abgetippte Termine statt Formel: "
                     "0 Punkte."},
        {"nr": "1c", "punkte": 3,
         "leistung": "Spalte F enthält je Zeile eine kopierfähige Formel für "
                     "das Jahr des Gesprächs.",
         "hinweis": "F4: =JAHR(E4), nach unten kopiert. Ergebnisse: sechsmal "
                    "2026, zweimal 2027.",
         "toleranz": "Zellformat mit Jahresanzeige statt Funktion: 3 Punkte "
                     "Abzug, weil kein Wert entsteht, mit dem sich rechnen "
                     "lässt."},
        {"nr": "1d", "punkte": 3,
         "leistung": "Spalte G enthält je Zeile eine kopierfähige Formel für "
                     "den Monat des Gesprächs.",
         "hinweis": "G4: =MONAT(E4), nach unten kopiert. Ergebnisse: "
                    + "; ".join(str(r["monat"]) for r in Z) + ".",
         "toleranz": "Ausgabe als Monatsname über ein Zellformat: kein Abzug, "
                     "solange die Zelle die Monatszahl enthält."},
        {"nr": "1e", "punkte": 4,
         "leistung": "Spalte H enthält je Zeile eine kopierfähige Formel für "
                     "die Zahl der Tage zwischen Eintritt und Gespräch.",
         "hinweis": f"H4: =E4-D4, nach unten kopiert, Zelle als Zahl "
                    f"formatiert. Ergebnisse: {tage}.",
         "toleranz": "TAGE360 statt der Kalenderdifferenz: 2 Punkte Abzug, "
                     "weil die Regel Kalendertage nennt. Zelle im Datumsformat "
                     "belassen: 1 Punkt Abzug."},
        {"nr": "1f", "punkte": 4,
         "leistung": "Spalte I enthält je Zeile eine kopierfähige Formel, die "
                     "die erste von der zweiten Monatshälfte trennt.",
         "hinweis": 'I4: =WENN(TAG(E4)<=15;"erste Hälfte";"zweite Hälfte"), '
                    "nach unten kopiert. Fünfmal erste Hälfte, dreimal zweite "
                    "Hälfte.",
         "toleranz": "Vergleich mit <16 statt <=15 zählt voll. Schreibweise "
                     "der Ausgabetexte muss übereinstimmen."},
        {"nr": "1g", "punkte": 4,
         "leistung": "Spalte J enthält je Zeile eine kopierfähige Formel, die "
                     "bei mehr als 166 Tagen kritisch ausgibt.",
         "hinweis": 'J4: =WENN(H4>166;"kritisch";"rechtzeitig"), nach unten '
                    f"kopiert. Ergebnisse: {urteil}.",
         "toleranz": "Vergleich mit >= statt >: 2 Punkte Abzug; erkennbar an "
                     "Brandt, der mit 166 Tagen die Grenze exakt trifft und "
                     "rechtzeitig lauten muss."},
        {"nr": "1h", "punkte": 2,
         "leistung": "Zelle B14 enthält eine Formel, die das Tagesdatum "
                     "liefert und sich beim Öffnen aktualisiert.",
         "hinweis": "B14: =HEUTE(). Der angezeigte Wert hängt vom Prüfungstag "
                    "ab und wird nicht bewertet; bewertet wird die Formel.",
         "toleranz": "Eingetipptes Datum: 0 Punkte, es aktualisiert sich "
                     "nicht. JETZT statt HEUTE: 1 Punkt Abzug, die Funktion "
                     "steht nicht in der Befehlsübersicht."},
        {"nr": "1i", "punkte": 3,
         "leistung": "Zelle B15 enthält eine Formel für die Anzahl der "
                     "kritischen Fristen.",
         "hinweis": f'B15: =ZÄHLENWENN(J4:J11;"kritisch"). Ergebnis: '
                    f"{ANZ_KRITISCH}.",
         "toleranz": "Zählung über einen Vergleich der Spalte H mit richtigem "
                     "Ergebnis zählt voll."},
        {"nr": "1j", "punkte": 4,
         "leistung": "Der Bereich C19 bis C24 enthält je Zeile eine "
                     "kopierfähige Formel für die Anzahl der Gespräche je "
                     "Monat.",
         "hinweis": f"C19: =ZÄHLENWENN($G$4:$G$11;B19), nach unten kopiert. "
                    f"Ergebnisse: {monate}. Die Summe ergibt {ANZAHL_MA}.",
         "toleranz": "Fehlender absoluter Bezug bei richtigem Ergebnis: "
                     "2 Punkte Abzug. Bezug auf die Monatsnamen in Spalte A "
                     "statt auf die Monatszahlen in Spalte B: kein Abzug, "
                     "solange das Ergebnis stimmt."},
        {"nr": "1k", "punkte": 4,
         "leistung": "Zelle B29 enthält eine Formel, die den Zeitbedarf für "
                     "alle Gespräche aus dem Richtwert ableitet.",
         "hinweis": f"B29: =B28/B27*SUMME(C19:C24). Erst der Wert je Gespräch "
                    f"(540 durch 12 ergibt 45 Minuten), dann mal der Anzahl. "
                    f"Ergebnis: {int(ZEITBEDARF)}.",
         "toleranz": "Rechenweg über eine Hilfszelle mit dem Wert je Gespräch "
                     "zählt voll. Feste Zahl 8 statt der Summe aus dem "
                     "Monatsblock: 1 Punkt Abzug, die Formel rechnet dann bei "
                     "geänderter Datenlage falsch."},
        {"nr": "1l", "punkte": 4,
         "leistung": "Im Blatt Frist steht ab A32 ein Säulendiagramm zu den "
                     "Gesprächen je Monat, gestaltet nach Anlage 5.",
         "hinweis": "Datenbereich: Rubriken A19:A24, Werte C19:C24. "
                    "Diagrammtitel, Legende und beide Achsenbeschriftungen "
                    "sind gesetzt. 1 Punkt Datenbereich, 1 Punkt Diagrammtyp, "
                    "2 Punkte Beschriftungen.",
         "toleranz": "Balkendiagramm statt Säulendiagramm: 1 Punkt Abzug. "
                     "Datenbereich über Spalte B statt Spalte C: 1 Punkt "
                     "Abzug, das Diagramm zeigt dann die Monatszahlen."},
        {"nr": "1 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind im Blatt "
                     "Frist eingehalten.",
         "hinweis": "Geprüft werden: Datumsangaben als TT.MM.JJJJ (Spalten D "
                    "und E, Zelle B14); Jahr, Monat, Tage und Minuten ohne "
                    "Dezimalstellen; Personalnummer ohne Tausenderpunkt; "
                    "Arial 11 pt. Abzüge im Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 0,5 Punkte Abzug, insgesamt "
                     "höchstens 2 Punkte."},

        {"nr": "2a", "punkte": 5,
         "leistung": "Die Datei ist als Serienbrief eingerichtet und mit dem "
                     "Blatt Teiln der Arbeitsmappe zu Aufgabe 1 als "
                     "Datenquelle verbunden.",
         "hinweis": "3 Punkte für die eingerichtete Serienbrieffunktion, "
                    "2 Punkte für die richtige Datenquelle. Geprüft wird an "
                    "der Datei der Teilnehmenden, nicht am "
                    "Verbindungsstring — der Pfad ist auf jedem Rechner ein "
                    "anderer.",
         "toleranz": "Verbindung auf eine Kopie des Blattes zählt voll, "
                     "solange die acht Datensätze vollständig erscheinen."},
        {"nr": "2b", "punkte": 6,
         "leistung": "Im Anschriftfeld stehen die Seriendruckfelder für "
                     "Anrede sowie Vorname und Nachname.",
         "hinweis": "2 Punkte Anrede in der ersten Zeile, je 2 Punkte Vorname "
                    "und Nachname in der zweiten Zeile. Geprüft wird über den "
                    "Feldbefehl, sichtbar mit Alt+F9.",
         "toleranz": "Vorname und Nachname in einer Zeile mit Leerzeichen "
                     "dazwischen ist richtig. Abgetippter Name statt Feld: je "
                     "Feld 2 Punkte Abzug."},
        {"nr": "2c", "punkte": 6,
         "leistung": "Die Anredezeile setzt sich aus den Feldern Briefanrede, "
                     "Anrede und Nachname zusammen und endet mit einem Komma.",
         "hinweis": "Je Feld 1,5 Punkte, 1,5 Punkte für Komma und "
                    "Leerzeichen. Ergebnis der ersten Einladung: Sehr geehrte "
                    "Frau Ahrens, — der zweiten: Sehr geehrter Herr Brandt,",
         "toleranz": "Abgetipptes Sehr geehrte ohne das Feld Briefanrede: "
                     "1,5 Punkte Abzug, weil die männliche Form dann falsch "
                     "erscheint."},
        {"nr": "2d", "punkte": 9,
         "leistung": "Der erste Absatz enthält die Seriendruckfelder für "
                     "Gesprächstermin und Uhrzeit sowie ein Bedingungsfeld für "
                     "den Ort.",
         "hinweis": "Je 2 Punkte für Termin und Uhrzeit, 5 Punkte für das "
                    "Bedingungsfeld: 2 Punkte für die richtige Bedingung auf "
                    "das Feld Standort, je 1,5 Punkte für die beiden "
                    "Ausgabetexte in der Zentrale, Raum 2.14 und in Ihrem "
                    "Standortbüro.",
         "toleranz": "Bedingung auf Berlin oder auf die abweichenden Standorte "
                     "formuliert — beide Richtungen zählen voll, solange das "
                     "Ergebnis stimmt. Acht einzeln bearbeitete Briefe statt "
                     "eines Bedingungsfeldes: 5 Punkte Abzug."},
        {"nr": "2e", "punkte": 4,
         "leistung": "Der Seriendruck ist zusammengeführt; das Ergebnis "
                     "enthält acht Einladungen.",
         "hinweis": "2 Punkte für die Zusammenführung, 2 Punkte für die "
                    "Vollständigkeit der acht Datensätze. Jede Einladung steht "
                    "auf einer eigenen Seite.",
         "toleranz": "Gespeichertes Hauptdokument ohne zusammengeführtes "
                     "Ergebnis: 4 Punkte Abzug. Zusätzlich gespeichertes "
                     "Hauptdokument: kein Abzug."},
        {"nr": "2 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind in der "
                     "Einladung eingehalten.",
         "hinweis": "Geprüft werden: Arial 11 pt, Datumsangaben als "
                    "TT.MM.JJJJ, Uhrzeiten als SS:MM. Die Formate der "
                    "Seriendruckfelder werden über den Feldbefehl gesteuert. "
                    "Abzüge im Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 1 Punkt Abzug, insgesamt "
                     "höchstens 2 Punkte."},

        {"nr": "3a", "punkte": 4,
         "leistung": "Die Felder Betreff und Sachbearbeiter/-in sind "
                     "sachgerecht ausgefüllt; das vorbereitete Datum bleibt "
                     "unverändert.",
         "hinweis": "2 Punkte Betreff mit Bezug auf die Fristenkontrolle der "
                    "Probezeitgespräche, 2 Punkte Sachbearbeiter/-in mit Name "
                    "und Funktion.",
         "toleranz": "Andere sinngemäße Formulierung des Betreffs zählt voll. "
                     "Verändertes Datum: 1 Punkt Abzug."},
        {"nr": "3b", "punkte": 5,
         "leistung": "Der Aktenvermerk hält einleitend fest, was geprüft wurde "
                     "und welchen Zeitraum die Fristenkontrolle umfasst.",
         "hinweis": "2 Punkte Gegenstand der Prüfung, 2 Punkte Zeitraum "
                    "September 2026 bis Februar 2027, 1 Punkt Großschreibung "
                    "des ersten Wortes. Der Aktenvermerk kennt keine Anrede "
                    "und beginnt deshalb groß (§6.3).",
         "toleranz": "Eingefügte Anrede: 1 Punkt Abzug, sie gehört nicht in "
                     "einen Aktenvermerk."},
        {"nr": "3c", "punkte": 7,
         "leistung": "Der Aktenvermerk nennt die Anzahl der kritischen Fristen "
                     "und den Zeitbedarf für alle Gespräche.",
         "hinweis": "4 Punkte für die Anzahl der kritischen Fristen (richtig "
                    f"sind {ANZ_KRITISCH} von {ANZAHL_MA}), 3 Punkte für den "
                    f"Zeitbedarf von {int(ZEITBEDARF)} Minuten. Beide Werte "
                    "müssen zur eigenen Auswertung aus Aufgabe 1 passen.",
         "toleranz": "Werte, die zur eigenen fehlerhaften Auswertung passen, "
                     "gelten als Folgefehler und kosten hier keine Punkte. "
                     "Zeitbedarf in Stunden statt Minuten: kein Abzug, solange "
                     "die Umrechnung stimmt."},
        {"nr": "3d", "punkte": 4,
         "leistung": "Der Aktenvermerk hält fest, was veranlasst wurde, und "
                     "nennt einen Termin zur Wiedervorlage.",
         "hinweis": "2 Punkte Veranlassung (Serienbrief, Versand am "
                    "31.08.2026), 2 Punkte Wiedervorlage am 15.09.2026.",
         "toleranz": "Fehlendes Versanddatum bei genannter Veranlassung: "
                     "1 Punkt Abzug."},
        {"nr": "3 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind im "
                     "Aktenvermerk eingehalten.",
         "hinweis": "Geprüft werden: Arial 11 pt aus der Vorlage unverändert, "
                    "Datumsangaben als TT.MM.JJJJ, Gliederungsleerzeilen nach "
                    "DIN 5008:2020. Abzüge im Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 1 Punkt Abzug, insgesamt "
                     "höchstens 2 Punkte."},
    ]


def _handreichung():
    return {
        "uebersicht": [
            ("Satz", SATZNAME),
            ("Zuschnitt", "Vollprüfung, 3 Aufgaben, 120 Minuten, 100 Punkte"),
            ("Punkteverteilung", "Aufgabe 1: 46 · Aufgabe 2: 32 · Aufgabe 3: 22 "
                                 "(je Aufgabe 2 Punkte für die Formatvorgaben)"),
            ("Stoffschwerpunkt", "Wirtschaftsrechnen, Dreisatz"),
            ("Abteilung", "Personal/Ausbildung"),
            ("Eingesetzte Funktionen", "SVERWEIS (exakte Suche), JAHR, MONAT, "
                                       "TAG, HEUTE, WENN, ZÄHLENWENN, SUMME"),
            ("Pflichtelemente", "Serienbrief-Bedingungsfeld · JAHR/MONAT/TAG · "
                                "HEUTE"),
            ("Kommunikationsform", "Aktenvermerk nach DIN 5008:2020"),
            ("Diagramm", "Säulendiagramm, Probezeitgespräche je Monat"),
        ],
        "zeitraster": [
            ("Einstieg und Rückmeldung der Gruppe", 5),
            ("Aufgabe 1, Teilaufgaben a bis g (Übernahme, Datum, Frist)", 17),
            ("Aufgabe 1, Teilaufgaben h bis l (Kennzahlen, Monate, Diagramm)",
             13),
            ("Aufgabe 2 (Serienbrief, Felder, Bedingungsfeld, Zusammenführen)",
             15),
            ("Aufgabe 3 (Aktenvermerk nach DIN 5008:2020)", 8),
            ("Puffer und offene Fragen", 2),
        ],
        "stolperstellen": [
            ("1b", "Der Suchbereich im Blatt Teiln wird nicht absolut gesetzt; "
                   "beim Kopieren nach unten wandert er mit. Zweite "
                   "Stolperstelle: Spaltenindex 6 statt 7, weil die Spalte "
                   "Briefanrede beim Zählen übersehen wird."),
            ("1e", "Die Differenz wird mit TAGE360 gerechnet. Die Regel nennt "
                   "aber Kalendertage, deshalb ist die einfache Subtraktion "
                   "richtig. Zweite Stolperstelle: die Ergebniszelle bleibt im "
                   "Datumsformat und zeigt ein Datum statt einer Zahl."),
            ("1g", "Der Vergleich wird mit größer oder gleich gesetzt. "
                   "Sichtbar wird das nur bei Brandt, der mit 166 Tagen die "
                   "Grenze exakt trifft."),
            ("1h", "Das Tagesdatum wird eingetippt. Beim nächsten Öffnen steht "
                   "dann ein veraltetes Datum in der Zelle."),
            ("1k", "Statt des Dreisatzes wird der Richtwert von "
                   "540 Minuten direkt übernommen. Richtig ist erst der Wert "
                   "je Gespräch, dann die Multiplikation mit der Anzahl."),
            ("2a", "Die Datenquelle wird als Datei verbunden, ohne das Blatt "
                   "Teiln auszuwählen. Word nimmt dann das erste Blatt der "
                   "Mappe, und die Felder bleiben leer."),
            ("2c", "Die Anrede wird als Sehr geehrte abgetippt. Bei den vier "
                   "männlichen Datensätzen steht dann die falsche Form."),
            ("2d", "Statt eines Bedingungsfeldes werden acht Briefe einzeln "
                   "bearbeitet. Das Ergebnis sieht richtig aus, die geprüfte "
                   "Leistung fehlt aber vollständig."),
            ("2e", "Gespeichert wird das Hauptdokument statt des "
                   "zusammengeführten Ergebnisses. Beim Öffnen auf einem "
                   "anderen Rechner sucht Word die Datenquelle vergeblich."),
            ("3b", "In den Aktenvermerk wird eine Anrede eingefügt. Ein "
                   "Aktenvermerk beginnt unmittelbar mit dem Inhalt."),
        ],
        "falschloesungen": [
            ["TAGE360 statt Kalenderdifferenz", "1e", "2 Punkte Abzug."],
            ["Vergleich mit größer oder gleich", "1g",
             "2 Punkte Abzug; erkennbar an Brandt."],
            ["Eingetipptes Tagesdatum", "1h", "2 Punkte Abzug, keine Formel."],
            ["Richtwert ohne Dreisatz übernommen", "1k",
             "3 Punkte Abzug, das Ergebnis lautet dann 540 statt 360."],
            ["Fehlender absoluter Bezug", "1b, 1j",
             "je 2 Punkte Abzug, weil die Formel nicht kopierfähig ist."],
            ["Abgetippte Anrede statt Feld Briefanrede", "2c",
             "1,5 Punkte Abzug, die männliche Form wird falsch."],
            ["Acht Briefe einzeln bearbeitet", "2d",
             "5 Punkte Abzug, das Bedingungsfeld fehlt."],
            ["Anrede im Aktenvermerk", "3b", "1 Punkt Abzug."],
        ],
        "fachklaerung": [
            ("Probezeit und Frist", "Die Probezeit dauert hier 180 "
                                    "Kalendertage. Das Gespräch soll "
                                    "spätestens 14 Tage vor Ablauf geführt "
                                    "sein; ab 167 Tagen zwischen Eintritt und "
                                    "Gespräch bleibt dafür kein Vorlauf mehr, "
                                    "die Frist gilt als kritisch."),
            ("Kalendertage gegen Zinstage", "TAGE360 rechnet mit 30 Tagen je "
                                            "Monat und wird im kaufmännischen "
                                            "Zinsrechnen gebraucht. Fristen "
                                            "des Arbeitsrechts laufen nach "
                                            "Kalendertagen, deshalb ist hier "
                                            "die einfache Differenz zweier "
                                            "Datumswerte richtig."),
            ("Dreisatz", "Aus 12 Gesprächen zu 540 Minuten folgt der Wert je "
                         "Gespräch: 540 geteilt durch 12 ergibt 45 Minuten. "
                         "Multipliziert mit der Zahl der Gespräche ergibt das "
                         "den Gesamtbedarf. Der Zwischenschritt über die "
                         "Einheit ist der Kern des Dreisatzes."),
            ("Selbstaktualisierende Werte", "HEUTE liefert das Datum des Tages, "
                                            "an dem die Datei geöffnet wird. "
                                            "Der angezeigte Wert ändert sich "
                                            "deshalb ständig und taugt nicht "
                                            "als Bewertungsgrundlage; bewertet "
                                            "wird die Formel."),
            ("Bedingungsfeld", "Ein Bedingungsfeld prüft während des "
                               "Seriendrucks den Inhalt eines Datenfeldes und "
                               "gibt je nach Ergebnis den einen oder den "
                               "anderen Text aus. Es steht im Hauptdokument, "
                               "nicht in der Datenquelle, und ersetzt die "
                               "Handarbeit an den einzelnen Briefen."),
        ],
        "anschlussuebungen": [
            ("Fristen prüfen", "Fünf Eintrittsdaten vorgeben, davon eines "
                               "genau auf der Grenze, und die Beurteilung "
                               "rechnen lassen."),
            ("Dreisatz gegen Direktübernahme", "Denselben Richtwert "
                                               "einmal über den Zwischenschritt "
                                               "je Einheit und einmal direkt "
                                               "anwenden lassen, danach die "
                                               "Ergebnisse vergleichen."),
            ("Bedingungsfeld üben", "Eine kurze Datenquelle mit drei "
                                    "Kategorien vorgeben und zwei "
                                    "verschiedene Schlusssätze über ein "
                                    "Bedingungsfeld ausgeben lassen."),
        ],
        "dateihinweise": [
            "Die Lösungsdatei zu Aufgabe 1 enthält echte Formeln. Öffnen Sie "
            "sie einmal in Excel, damit alle Werte neu berechnet werden. Die "
            "Zelle B14 enthält HEUTE und zeigt deshalb das Datum des Tages, an "
            "dem Sie die Datei öffnen — das ist richtig so. Die Datei enthält "
            "neben dem Auswertungsblatt und dem Blatt Teiln weitere Blätter mit "
            "Daten aus dem Modellunternehmen; sie werden nicht gebraucht, sind "
            "aber Teil der Arbeitsumgebung und bleiben erhalten.",
            "Die Lösungsdatei zu Aufgabe 2 ist das zusammengeführte Ergebnis "
            "mit acht Einladungen auf acht Seiten, kein Hauptdokument. Das ist "
            "Absicht: ein Hauptdokument würde beim Öffnen nach einer "
            "Datenquelle suchen, die auf keinem anderen Rechner am selben Ort "
            "liegt. Prüfen Sie die Arbeit der Teilnehmenden am Feldbefehl in "
            "deren Hauptdokument, sichtbar mit Alt+F9.",
            "Die Teilnehmerdatei zu Aufgabe 2 enthält den Text der Einladung "
            "mit Auslassungspunkten an den Stellen, an denen die "
            "Seriendruckfelder eingefügt werden. Welche Felder wohin gehören, "
            "steht im Feldplan in Anlage 3.",
            "Die Lösungsdatei zu Aufgabe 3 ist die ausgefüllte "
            "Goldberg-Vorlage für den Aktenvermerk. Das Datum ist in beiden "
            "Fassungen vorbereitet und wird nicht bewertet.",
        ],
    }
