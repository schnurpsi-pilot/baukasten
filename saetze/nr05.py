# -*- coding: utf-8 -*-
"""Satzspezifikation AP1-Nr05-V4-6 — Posteingang nach Bearbeitungsdauer.

Setzt den Planeintrag Nr05 des Reihenplans um: Abteilung Verwaltung/
Büroorganisation, Stoffschwerpunkt Prozentrechnung, Kreisdiagramm über den
Anteil je Postart, Dokumentvorlage Laufzettel mit WordArt-Kopf,
innerbetriebliche Mitteilung.

Der Rechenteil oben ist die unabhängige Kontrollrechnung — sie liefert die
Sollwerte für die Rechenprobe nach §14.1 Punkt 3.
"""
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP
from autoria.texte import hinweise

SATZNAME = "AP1-Nr05-V4-6"

# ============================================================ Kontrollrechnung
# Postarten mit Kürzel, Klartext und der vereinbarten Sollzeit in Minuten.
POSTARTEN = [
    ("RE", "Rechnung", 45),
    ("AN", "Angebot", 60),
    ("BE", "Bestellung", 30),
    ("RK", "Reklamation", 90),
    ("AL", "Allgemeine Korrespondenz", 25),
]

# Posteingang einer Woche. Beim Zahlenentwurf nach §6.1 beachtet:
# - P-2603 trifft die Sollzeit exakt; nur so trennt sich > von >=.
# - Vier Vorgänge laufen über eine volle Stunde hinweg (P-2604, P-2606,
#   P-2609, P-2610). Wer nur MINUTE rechnet, erhält dort sichtbar falsche
#   Werte statt zufällig richtiger.
VORGAENGE = [
    ("P-2601", "RE", dt.time(8, 15), dt.time(9, 5)),
    ("P-2602", "AL", dt.time(8, 40), dt.time(9, 0)),
    ("P-2603", "BE", dt.time(9, 5), dt.time(9, 35)),
    ("P-2604", "RK", dt.time(9, 20), dt.time(11, 5)),
    ("P-2605", "RE", dt.time(9, 50), dt.time(10, 25)),
    ("P-2606", "AN", dt.time(10, 10), dt.time(11, 20)),
    ("P-2607", "RE", dt.time(10, 35), dt.time(11, 15)),
    ("P-2608", "AL", dt.time(11, 0), dt.time(11, 30)),
    ("P-2609", "AN", dt.time(11, 25), dt.time(12, 15)),
    ("P-2610", "RE", dt.time(13, 5), dt.time(14, 0)),
]

ERSTE_ZEILE = 4                      # erste Datenzeile im Blatt Ausw
ANZAHL_VORGAENGE = len(VORGAENGE)
ANTEIL_ERSTE = 21                    # erste Zeile des Anteilsblocks


def _rechnen():
    klartext = {k: n for k, n, _s in POSTARTEN}
    sollzeit = {k: s for k, _n, s in POSTARTEN}
    rows = []
    for nr, kuerzel, ein, erl in VORGAENGE:
        dauer = ((erl.hour - ein.hour) * 60) + (erl.minute - ein.minute)
        rows.append(dict(nr=nr, kuerzel=kuerzel, ein=ein, erl=erl,
                         postart=klartext[kuerzel], dauer=dauer,
                         soll=sollzeit[kuerzel],
                         urteil=("überschritten" if dauer > sollzeit[kuerzel]
                                 else "eingehalten")))
    return rows


Z = _rechnen()
ANZ_VORGAENGE = len(Z)
ANZ_UEBERSCHRITTEN = sum(1 for r in Z if r["urteil"] == "überschritten")
GESAMTDAUER = sum(r["dauer"] for r in Z)

# Anteil je Postart — der Stoffschwerpunkt des Satzes (§7: Prozentrechnung).
ANTEILE = []
for _k, _name, _s in POSTARTEN:
    anzahl = sum(1 for r in Z if r["kuerzel"] == _k)
    ANTEILE.append(dict(kuerzel=_k, postart=_name, anzahl=anzahl,
                        anteil=Decimal(anzahl) / Decimal(ANZ_VORGAENGE)))


def _prozent(wert):
    """0.4 wird zu '40,0 %' — Fließtextschreibweise nach §5.7."""
    z = (Decimal(wert) * 100).quantize(Decimal("0.1"), ROUND_HALF_UP)
    return f"{z}".replace(".", ",") + "\u00a0%"


def _uhr(t):
    return t.strftime("%H:%M")


# ==================================================================== Textteile
SACHVERHALT = (
    "Die Goldberg Designermöbel GmbH bearbeitet den gesamten Posteingang zentral "
    "in der Abteilung Verwaltung/Büroorganisation. Für jede Postart ist eine "
    "Sollzeit vereinbart, innerhalb derer ein Vorgang an die Fachabteilung "
    "weitergegeben sein soll. In der Kalenderwoche 35 sind zehn Vorgänge erfasst "
    "worden. Frau Ute Winkelmann, Leiterin der Abteilung Verwaltung/"
    "Büroorganisation, bittet Sie, die Bearbeitungsdauern auszuwerten, einen "
    "Laufzettel als Dokumentvorlage zu erstellen und die Abteilung über das "
    "Ergebnis zu unterrichten."
)

# Nur die Zeilen, die dieser Satz braucht (§5.7 Teil 2). Geldbeträge kommen
# nicht vor, dafür Uhrzeiten — das Pflichtelement STUNDE/MINUTE verlangt sie.
FORMATVORGABEN = [
    ["Uhrzeit", "SS:MM"],
    ["Zeitspannen in Minuten", "ganze Zahl, ohne Tausenderpunkt"],
    ["Prozentwerte", "eine Dezimalstelle"],
    ["Mengen und Stückzahlen", "ohne Dezimalstellen, ab fünf Stellen mit "
                               "Tausenderpunkt"],
    ["Datum", "TT.MM.JJJJ"],
    ["Schrift in allen Dateien", "Arial 11 pt"],
    ["Diagramm", "Titel und Legende sichtbar"],
]

# --------------------------------------------------------------- Laufzettel A2
LAUFZETTEL_TITEL = "Laufzettel Posteingang"
LAUFZETTEL_VORSPANN = (
    "Der Laufzettel begleitet jeden Posteingang von der Erfassung bis zur "
    "Ablage. Er wird von der Poststelle ausgefüllt und verbleibt beim Vorgang."
)
LAUFZETTEL_KOPF = ["Angabe", "Eintrag"]
LAUFZETTEL_ZEILEN = [
    ["Vorgangsnummer", ""],
    ["Postart", ""],
    ["Eingang am, um", ""],
    ["Zuständige Abteilung", ""],
    ["Weitergegeben am, um", ""],
    ["Bemerkung", ""],
]
LAUFZETTEL_SCHLUSS = (
    "Bei Reklamationen ist die Abteilung Vertrieb zusätzlich zu unterrichten."
)


# ================================================================ Spezifikation
def spec():
    dateien = {"a1": f"{SATZNAME}_A1_Teilnehmer.xlsx",
               "a2": f"{SATZNAME}_A2_Teilnehmer.docx",
               "a3": f"{SATZNAME}_A3_Teilnehmer.docx"}
    letzte = ERSTE_ZEILE + ANZAHL_VORGAENGE - 1          # Zeile 13
    a_erste = ANTEIL_ERSTE                                # Zeile 21
    a_letzte = ANTEIL_ERSTE + len(POSTARTEN) - 1          # Zeile 25

    return {
        "meta": {
            "satzname": SATZNAME,
            "reihe": "AP1 Prüfungssimulationen Goldberg Designermöbel GmbH",
            "hinweis": ("Der Satz setzt den Planeintrag Nr05 des Reihenplans "
                        "AP1-Reihenplan_Nr04-Nr29.json um und trägt dessen "
                        "laufende Nummer (§11.2). Der Reihenplan selbst wird "
                        "nicht mit ausgeliefert."),
            "bezeichnung": ["Abschlussprüfung Teil 1",
                            "Kaufleute für Büromanagement",
                            "Informationstechnisches Büromanagement"],
            "bearbeitungszeit": 120,
            "gesamtpunkte": 100,
        },
        "fettbegriffe": list(dateien.values()) + ["Ausw", "Post"],
        "sachverhalt": SACHVERHALT,
        "hinweise": hinweise(beispieldatei="Weber1708_A1.xlsx"),
        "formatvorgaben": FORMATVORGABEN,

        # ---------------------------------------------------------- Arbeitsmappe
        "aktives_blatt": "Tel",
        "blaetter": [
            {"name": "Tel", "titel": "Telefonverzeichnis",
             "kopf": ["Durchwahl", "Name", "Abteilung", "Funktion"],
             "zeilen": [["357-120", "Winkelmann, Ute",
                         "Verwaltung/Büroorganisation", "Abteilungsleitung"],
                        ["357-122", "Berger, Timo",
                         "Verwaltung/Büroorganisation", "Sachbearbeitung"],
                        ["357-124", "Halm, Petra",
                         "Verwaltung/Büroorganisation", "Poststelle"],
                        ["357-110", "Kortmann, Ines", "Beschaffung/Einkauf",
                         "Abteilungsleitung"],
                        ["357-131", "Lehnhoff, Marie",
                         "Rechnungswesen/Controlling", "Sachbearbeitung"],
                        ["357-140", "Osterkamp, Jan", "Lager/Logistik",
                         "Abteilungsleitung"],
                        ["357-150", "Reinbold, Sina", "Personal/Ausbildung",
                         "Abteilungsleitung"],
                        ["357-160", "Thelen, Kaan", "Vertrieb",
                         "Sachbearbeitung"]]},

            {"name": "Ausw", "art": "auswertung",
             "titel": "Auswertung Posteingang Kalenderwoche 35",
             "anzahl_zeilen": ANZAHL_VORGAENGE,
             "spalten": [
                 {"kopf": "Vorgangs-Nr.", "art": "text", "breite": 27,
                  "werte": [r["nr"] for r in Z]},
                 {"kopf": "Postart-Kürzel", "art": "text", "breite": 18,
                  "werte": [r["kuerzel"] for r in Z]},
                 {"kopf": "Eingang", "breite": 18, "format": "zeit",
                  "werte": [r["ein"] for r in Z]},
                 {"kopf": "Erledigt", "breite": 12, "format": "zeit",
                  "werte": [r["erl"] for r in Z]},
                 {"kopf": "Postart", "art": "text", "breite": 26,
                  "formel": "=VLOOKUP(B{z},Post!$A$4:$C$8,2,FALSE)"},
                 {"kopf": "Bearbeitungs~dauer in Minuten", "breite": 15,
                  "format": "ganz",
                  "formel": "=HOUR(D{z}-C{z})*60+MINUTE(D{z}-C{z})"},
                 {"kopf": "Sollzeit in Minuten", "breite": 13, "format": "ganz",
                  "formel": "=VLOOKUP(B{z},Post!$A$4:$C$8,3,FALSE)"},
                 {"kopf": "Beurteilung", "breite": 16, "ausrichtung": "left",
                  "formel": '=IF(F{z}>G{z},"überschritten","eingehalten")'},
             ],
             "festzellen": [
                 {"zelle": "A15", "text": "Kennzahlen der Woche", "fett": True},
                 {"zelle": "A20", "text": "Postart", "fett": True,
                  "rahmen": True},
                 {"zelle": "B20", "text": "Anzahl Vorgänge", "fett": True,
                  "rahmen": True, "ausrichtung": "center"},
                 {"zelle": "C20", "text": "Anteil in Prozent", "fett": True,
                  "rahmen": True, "ausrichtung": "center"},
             ] + [{"zelle": f"A{a_erste + i}", "text": a["postart"],
                   "rahmen": True}
                  for i, a in enumerate(ANTEILE)],
             "einzelzellen": [
                 {"label": "Erfasste Vorgänge", "label_zelle": "A16",
                  "zelle": "B16", "format": "ganz",
                  "formel": "=COUNTA(A{erste}:A{letzte})"},
                 {"label": "Vorgänge über Sollzeit", "label_zelle": "A17",
                  "zelle": "B17", "format": "ganz",
                  "formel": '=COUNTIF(H{erste}:H{letzte},"überschritten")'},
                 {"label": "Dauer gesamt in Minuten",
                  "label_zelle": "A18", "zelle": "B18", "format": "ganz",
                  "formel": "=SUM(F{erste}:F{letzte})"},
             ] + [{"zelle": f"B{a_erste + i}", "format": "ganz",
                   "formel": ("=COUNTIF($E${erste}:$E${letzte},A%d)"
                              % (a_erste + i))}
                  for i in range(len(ANTEILE))] +
                 [{"zelle": f"C{a_erste + i}", "format": "prozent",
                   "formel": "=B%d/$B$16" % (a_erste + i)}
                  for i in range(len(ANTEILE))],
             "diagramm": {"typ": "kreis", "wertespalte": 3, "rubrikspalte": 1,
                          "werte_zeilen": (20, a_letzte),
                          "rubrik_zeilen": (a_erste, a_letzte),
                          "titel": "Anteil je Postart am Posteingang",
                          "beschriftung": "prozent", "position": "A28",
                          "breite": 15.5, "hoehe": 9.5}},

            {"name": "Rekl", "titel": "Reklamationen laufendes Jahr",
             "kopf": ["Vorgangs~nummer", "Möbelserie", "Grund", "Eingang",
                      "Erledigt"],
             "zeilen": [["R-2604", "Novara", "Transportschaden",
                         dt.date(2026, 1, 22), "ja"],
                        ["R-2611", "Belvento", "Fehlteil",
                         dt.date(2026, 2, 17), "ja"],
                        ["R-2618", "Cortina", "Oberflächenfehler",
                         dt.date(2026, 4, 3), "ja"],
                        ["R-2625", "Marano", "Falschlieferung",
                         dt.date(2026, 5, 11), "nein"],
                        ["R-2634", "Novara", "Fehlteil", dt.date(2026, 6, 26),
                         "nein"],
                        ["R-2642", "Belvento", "Transportschaden",
                         dt.date(2026, 7, 30), "nein"]]},

            {"name": "Post", "titel": "Postarten und vereinbarte Sollzeiten",
             "stammdaten": True,
             "kopf": ["Kürzel", "Postart", "Sollzeit in Minuten"],
             "breiten": [12, 28, 14],
             "formate": [None, None, "ganz"],
             "zeilen": [[k, n, s] for k, n, s in POSTARTEN]},

            {"name": "Messe", "titel": "Messeplanung laufendes Jahr",
             "kopf": ["Messe", "Ort", "Beginn", "Ende", "Standfläche in qm"],
             "formate": [None, None, "datum", "datum", "ganz"],
             "zeilen": [["Wohnen und Interieur", "Hamburg",
                         dt.date(2026, 9, 17), dt.date(2026, 9, 20), 48],
                        ["Objekt und Kontrakt", "Köln", dt.date(2026, 10, 8),
                         dt.date(2026, 10, 11), 72],
                        ["Nordische Möbeltage", "Bremen",
                         dt.date(2026, 11, 5), dt.date(2026, 11, 7), 36],
                        ["Designforum Süd", "München", dt.date(2027, 2, 11),
                         dt.date(2027, 2, 14), 60]]},

            {"name": "Pers", "titel": "Personalstamm Verwaltung",
             "kopf": ["Personal~nummer", "Name", "Abteilung", "Eintritt",
                      "Wochen-stunden"],
             "zeilen": [[70211, "Adam, Ruth", "Beschaffung/Einkauf",
                         dt.date(2018, 4, 1), 40],
                        [70214, "Berger, Timo", "Verwaltung/Büroorganisation",
                         dt.date(2019, 9, 16), 30],
                        [70218, "Halm, Petra", "Verwaltung/Büroorganisation",
                         dt.date(2014, 8, 1), 35],
                        [70231, "Lehnhoff, Marie",
                         "Rechnungswesen/Controlling", dt.date(2021, 7, 1), 35],
                        [70238, "Osterkamp, Jan", "Lager/Logistik",
                         dt.date(2020, 3, 2), 40],
                        [70244, "Reinbold, Sina", "Personal/Ausbildung",
                         dt.date(2017, 11, 2), 32],
                        [70251, "Thelen, Kaan", "Vertrieb",
                         dt.date(2022, 1, 10), 40],
                        [70259, "Winkelmann, Ute",
                         "Verwaltung/Büroorganisation", dt.date(2016, 6, 1),
                         40]]},

            {"name": "Lagor", "titel": "Lagerorte Zentrallager",
             "kopf": ["Lagerort", "Halle", "Regalreihe", "Stellplätze",
                      "Belegt"],
             "zeilen": [["ZL-A-01", "A", 1, 48, 44], ["ZL-A-02", "A", 2, 48, 31],
                        ["ZL-B-01", "B", 1, 60, 52], ["ZL-B-02", "B", 2, 60, 18],
                        ["ZL-C-01", "C", 1, 36, 29], ["ZL-C-02", "C", 2, 36, 15]]},
        ],

        # Sollwerte für die Rechenprobe (§14.1 Punkt 3).
        "erwartete_werte": {
            **{f"Ausw!E{ERSTE_ZEILE + i}": Z[i]["postart"]
               for i in range(ANZAHL_VORGAENGE)},
            **{f"Ausw!F{ERSTE_ZEILE + i}": Z[i]["dauer"]
               for i in range(ANZAHL_VORGAENGE)},
            **{f"Ausw!G{ERSTE_ZEILE + i}": Z[i]["soll"]
               for i in range(ANZAHL_VORGAENGE)},
            **{f"Ausw!H{ERSTE_ZEILE + i}": Z[i]["urteil"]
               for i in range(ANZAHL_VORGAENGE)},
            "Ausw!B16": ANZ_VORGAENGE,
            "Ausw!B17": ANZ_UEBERSCHRITTEN,
            "Ausw!B18": GESAMTDAUER,
            **{f"Ausw!B{a_erste + i}": ANTEILE[i]["anzahl"]
               for i in range(len(ANTEILE))},
            **{f"Ausw!C{a_erste + i}": float(ANTEILE[i]["anteil"])
               for i in range(len(ANTEILE))},
        },

        # ------------------------------------------------------------- Aufgaben
        "aufgaben": [
            {"nr": 1, "typ": "tabellenkalkulation", "titel": "Tabellenkalkulation",
             "punkte": 48,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a1']}. Sie arbeiten "
                            "im Blatt Ausw. Die Postarten und die vereinbarten "
                            "Sollzeiten stehen im Blatt Post."),
             "teilaufgaben": [
                 ("a", "Übertragen Sie die zehn Vorgänge aus Anlage 2 in den "
                       "Bereich A4 bis D13 des Blattes Ausw. Halten Sie die "
                       "Reihenfolge der Anlage ein.", 5),
                 ("b", "Ermitteln Sie in Spalte E die ausgeschriebene Postart. "
                       "Die Zuordnung steht im Blatt Post.", 5),
                 ("c", "Ermitteln Sie in Spalte F die Bearbeitungsdauer je "
                       "Vorgang in Minuten aus der Eingangs- und der "
                       "Erledigungsuhrzeit.", 7),
                 ("d", "Ermitteln Sie in Spalte G die vereinbarte Sollzeit je "
                       "Vorgang. Die Sollzeiten stehen im Blatt Post.", 4),
                 ("e", "Geben Sie in Spalte H eine Beurteilung aus. Es soll "
                       "@@überschritten@@ erscheinen, wenn die "
                       "Bearbeitungsdauer über der Sollzeit liegt. In allen "
                       "anderen Fällen soll @@eingehalten@@ erscheinen.", 4),
                 ("f", "Ermitteln Sie in Zelle B16 die Anzahl der erfassten "
                       "Vorgänge.", 3),
                 ("g", "Ermitteln Sie in Zelle B17 die Anzahl der Vorgänge "
                       "über der Sollzeit.", 3),
                 ("h", "Ermitteln Sie in Zelle B18 die gesamte "
                       "Bearbeitungsdauer aller Vorgänge in Minuten.", 2),
                 ("i", "Ermitteln Sie im Bereich B21 bis B25 die Anzahl der "
                       "Vorgänge je Postart.", 4),
                 ("j", "Ermitteln Sie im Bereich C21 bis C25 den Anteil jeder "
                       "Postart am gesamten Posteingang.", 5),
                 ("k", "Erstellen Sie im Blatt Ausw ab Zelle A28 ein "
                       "Kreisdiagramm zum Anteil der Postarten am "
                       "Posteingang. Gestalten Sie es nach dem Muster in "
                       "Anlage 5.", 4),
             ]},
            {"nr": 2, "typ": "textverarbeitung", "titel": "Textverarbeitung",
             "punkte": 30,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a2']}. Der Entwurf "
                            "des Laufzettels steht in Anlage 3."),
             "teilaufgaben": [
                 ("a", "Fügen Sie oberhalb der Überschrift einen Schriftzug "
                       "mit dem Text @@Goldberg Designermöbel GmbH@@ als "
                       "Schrifteffekt ein. Der Schriftzug ist zentriert und "
                       "etwa 12 cm breit.", 6),
                 ("b", "Formatieren Sie die Überschrift Laufzettel Posteingang: "
                       "Arial 14 pt, fett, zentriert, Abstand nach 12 pt.", 4),
                 ("c", "Erstellen Sie unterhalb des einleitenden Absatzes eine "
                       "Tabelle mit den sechs Angaben aus Anlage 3. Die linke "
                       "Spalte ist 5 cm breit, die rechte 10 cm.", 7),
                 ("d", "Fügen Sie in die Fußzeile den Dateinamen, das "
                       "Tagesdatum und die Seitenanzahl als Felder ein. Die "
                       "Fußzeile ist zentriert und in Arial 9 pt gesetzt.", 6),
                 ("e", "Speichern Sie die Datei zusätzlich als Dokumentvorlage "
                       "unter Ihrer Teilnehmernummer und der Aufgabennummer, "
                       "also zum Beispiel Weber1708_A2.dotx.", 5),
             ]},
            {"nr": 3, "typ": "kommunikation",
             "titel": "Geschäftliche Kommunikation", "punkte": 22,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a3']}. Das Datum "
                            "ist bereits eingetragen. Die Angaben für die "
                            "Mitteilung stehen in Anlage 4. Beachten Sie "
                            "DIN 5008:2020."),
             "teilaufgaben": [
                 ("a", "Vervollständigen Sie die Felder An, Von und Thema.", 5),
                 ("b", "Beschreiben Sie einleitend, welche Auswertung "
                       "vorgenommen wurde und welchen Zeitraum sie umfasst.", 5),
                 ("c", "Teilen Sie mit, wie viele Vorgänge die Sollzeit "
                       "überschritten haben, und schlagen Sie den Laufzettel "
                       "als Maßnahme vor.", 6),
                 ("d", "Weisen Sie auf die beigefügte Auswertung hin und "
                       "schließen Sie die Mitteilung ab.", 4),
             ]},
        ],

        # -------------------------------------------------------------- Anlagen
        "anlagen": [
            {"nr": 1, "titel": "E-Mail der Abteilungsleitung",
             "gehoert_zu": "Aufgaben 1 bis 3",
             "bloecke": [
                 {"typ": "felder", "paare": [
                     ("Von", "ute.winkelmann@goldberg.test"),
                     ("An", "verwaltung@goldberg.test"),
                     ("Datum", "26.08.2026"),
                     ("Betreff", "Posteingang KW 35 – Auswertung, Laufzettel "
                                 "und Mitteilung")]},
                 {"typ": "absaetze", "zeilen": [
                     "Guten Morgen,", "",
                     "für die Kalenderwoche 35 liegen mir zehn erfasste "
                     "Posteingänge vor. Die Aufstellung finden Sie in Anlage 2, "
                     "die vereinbarten Sollzeiten stehen im Blatt Post der "
                     "Arbeitsmappe.", "",
                     "Bitte werten Sie die Vorgänge aus und ermitteln Sie die "
                     "Bearbeitungsdauer je Vorgang sowie den Anteil der "
                     "einzelnen Postarten am gesamten Posteingang.", "",
                     "Damit die Laufwege künftig nachvollziehbar sind, soll "
                     "jeder Posteingang einen Laufzettel erhalten. Den Entwurf "
                     "dazu habe ich Ihnen in Anlage 3 notiert; er wird als "
                     "Dokumentvorlage abgelegt.", "",
                     "Über das Ergebnis unterrichten Sie bitte anschließend die "
                     "Abteilung. Die Angaben dazu stehen in Anlage 4.", "",
                     "Vielen Dank und freundliche Grüße", "Ute Winkelmann",
                     "Leiterin Verwaltung/Büroorganisation"]},
             ]},
            {"nr": 2, "titel": "Posteingang Kalenderwoche 35",
             "gehoert_zu": "Aufgabe 1",
             "bloecke": [
                 {"typ": "text", "text": "Übertragen Sie die folgenden Angaben "
                                         "positionsgerecht in die "
                                         "Auswertungstabelle."},
                 {"typ": "tabelle",
                  "kopf": ["Vorgangs-Nr.", "Postart-Kürzel", "Eingang",
                           "Erledigt"],
                  "zeilen": [[r["nr"], r["kuerzel"], _uhr(r["ein"]),
                              _uhr(r["erl"])] for r in Z],
                  "zahlenspalten": [2, 3]},
                 {"typ": "ueberschrift", "text": "Hinweise zur Erfassung"},
                 {"typ": "liste", "zeilen": [
                     "Das Postart-Kürzel verweist auf das Blatt Post der "
                     "Arbeitsmappe. Dort stehen die ausgeschriebene Postart und "
                     "die vereinbarte Sollzeit.",
                     "Eingang und Erledigung sind Uhrzeiten desselben Tages; "
                     "kein Vorgang läuft über Nacht.",
                     "Die Sollzeit gilt als eingehalten, solange die "
                     "Bearbeitungsdauer sie nicht überschreitet.",
                     "Der Anteil einer Postart bezieht sich auf die Anzahl der "
                     "Vorgänge, nicht auf die Bearbeitungsdauer."]},
             ]},
            {"nr": 3, "titel": "Entwurf des Laufzettels",
             "gehoert_zu": "Aufgabe 2",
             "bloecke": [
                 {"typ": "text", "text":
                     "Der Laufzettel trägt oben einen Schriftzug mit der "
                     "Firmierung, darunter die Überschrift und den "
                     "einleitenden Absatz. Beide stehen bereits in der Datei."},
                 {"typ": "ueberschrift", "text": "Angaben der Tabelle"},
                 {"typ": "tabelle", "kopf": ["Angabe", "Art des Eintrags"],
                  "zeilen": [["Vorgangsnummer", "freie Eingabe"],
                             ["Postart", "freie Eingabe"],
                             ["Eingang am, um", "Datum im Format TT.MM.JJJJ "
                                                "und Uhrzeit im Format SS:MM"],
                             ["Zuständige Abteilung", "freie Eingabe"],
                             ["Weitergegeben am, um", "Datum im Format "
                                                      "TT.MM.JJJJ und Uhrzeit "
                                                      "im Format SS:MM"],
                             ["Bemerkung", "freie Eingabe"]]},
                 {"typ": "ueberschrift", "text": "Angaben der Fußzeile"},
                 {"typ": "liste", "zeilen": [
                     "Dateiname der Vorlage",
                     "Tagesdatum, das sich beim Öffnen aktualisiert",
                     "Seitenanzahl"]},
             ]},
            {"nr": 4, "titel": "Notiz für die Mitteilung",
             "gehoert_zu": "Aufgabe 3",
             "bloecke": [
                 {"typ": "felder", "paare": [
                     ("Datum", "26.08.2026"),
                     ("Verfasserin", "Ute Winkelmann, Leiterin Verwaltung/"
                                     "Büroorganisation"),
                     ("Betrifft", "Unterrichtung der Abteilung über die "
                                  "Auswertung KW 35")]},
                 {"typ": "text", "text":
                     "Empfänger sind alle Mitarbeiterinnen und Mitarbeiter der "
                     "Abteilung Verwaltung/Büroorganisation. Absenderin ist "
                     "Frau Ute Winkelmann, Leiterin der Abteilung."},
                 {"typ": "text", "text":
                     "Ausgewertet wurde der Posteingang der Kalenderwoche 35 "
                     "vom 24. bis zum 28.08.2026, verglichen mit den "
                     "vereinbarten Sollzeiten je Postart."},
                 {"typ": "text", "text":
                     "Als Maßnahme ist der Laufzettel aus Aufgabe 2 "
                     "eingeführt. Er begleitet ab dem 01.09.2026 jeden "
                     "Posteingang und wird in der Poststelle ausgefüllt."},
                 {"typ": "text", "text":
                     "Die Auswertung liegt der Mitteilung als Anlage bei. "
                     "Rückfragen beantwortet Frau Petra Halm unter der "
                     "Durchwahl 357-124."},
             ]},
            {"nr": 5, "titel": "Gestaltungsmuster für das Diagramm",
             "gehoert_zu": "Aufgabe 1", "quer": True,
             "bloecke": [
                 {"typ": "text", "text":
                     "Das Muster zeigt ausschließlich Aufbau und Gestaltung. "
                     "Die abgebildeten Werte und Bezeichnungen gehören nicht "
                     "zur Aufgabe.", "nach": 10},
                 {"typ": "bild", "pfad": "muster_kreis.png", "breite": 20.0},
             ]},
        ],

        # --------------------------------------------------------- Aufgabendateien
        "dateien": [
            {"art": "xlsx", "praefix": "A1"},
            {"art": "dotx", "praefix": "A2", "wordart_erwartet": True,
             "autotext": ("dateiname", "datum", "seiten"),
             "teilnehmer": (
                 [{"typ": "absatz", "text": LAUFZETTEL_TITEL},
                  {"typ": "absatz", "text": LAUFZETTEL_VORSPANN},
                  {"typ": "absatz", "text": LAUFZETTEL_SCHLUSS}]),
             "loesung": (
                 [{"typ": "wordart", "text": "Goldberg Designermöbel GmbH",
                   "breite_pt": 340, "hoehe_pt": 40, "groesse_pt": 30,
                   "nach": 12},
                  {"typ": "ueberschrift", "text": LAUFZETTEL_TITEL,
                   "groesse": 14, "vor": 0, "nach": 12, "zentriert": True},
                  {"typ": "absatz", "text": LAUFZETTEL_VORSPANN,
                   "blocksatz": True, "nach": 12},
                  {"typ": "tabelle", "kopf": LAUFZETTEL_KOPF,
                   "zeilen": LAUFZETTEL_ZEILEN, "breiten": [5.0, 10.0]},
                  {"typ": "leer", "nach": 0},
                  {"typ": "absatz", "text": LAUFZETTEL_SCHLUSS, "vor": 12,
                   "blocksatz": True}])},
            {"art": "vorlage", "praefix": "A3", "form": "mitteilung",
             "teilnehmer": {"felder": {"Datum": "27.08.2026"}},
             "loesung": {
                 "felder": {
                     "An": "Alle Mitarbeiterinnen und Mitarbeiter der "
                           "Abteilung Verwaltung/Büroorganisation",
                     "Von": "Ute Winkelmann, Leiterin Verwaltung/"
                            "Büroorganisation",
                     "Datum": "27.08.2026",
                     "Thema": "Auswertung des Posteingangs der "
                              "Kalenderwoche 35"},
                 "koerper": [
                     "Liebe Kolleginnen und Kollegen,", "",
                     "für die Kalenderwoche 35 vom 24. bis zum 28.08.2026 haben "
                     "wir die zehn erfassten Posteingänge ausgewertet. "
                     "Verglichen wurde die Bearbeitungsdauer je Vorgang mit der "
                     "Sollzeit, die für die jeweilige Postart vereinbart ist.",
                     "",
                     "Bei fünf der zehn Vorgänge lag die Bearbeitungsdauer über "
                     "der vereinbarten Sollzeit. Damit die Laufwege künftig "
                     "nachvollziehbar sind, führen wir zum 01.09.2026 einen "
                     "Laufzettel ein. Er begleitet jeden Posteingang von der "
                     "Erfassung bis zur Ablage und wird in der Poststelle "
                     "ausgefüllt.", "",
                     "Die vollständige Auswertung ist dieser Mitteilung als "
                     "Anlage beigefügt. Rückfragen nimmt Frau Petra Halm unter "
                     "der Durchwahl 357-124 entgegen.", "",
                     "Mit freundlichen Grüßen", "", "Ute Winkelmann"]}},
        ],

        # ---------------------------------------------------------- Bewertung
        "bewertung": _bewertung(),

        # -------------------------------------------------------- Handreichung
        "handreichung": _handreichung(),

        # ----------------------------------------------------- Historieneintrag
        "historie_eintrag": {
            "satzname": SATZNAME, "nummer": "05",
            "satzart": "vollpruefung", "bearbeitungszeit_min": 120,
            "gesamtpunkte": 100, "abteilung": "Verwaltung/Büroorganisation",
            "szenario": "Auswertung des Posteingangs nach Bearbeitungsdauer "
                        "mit Anteilsrechnung je Postart",
            "stoffschwerpunkt": ["wirtschaftsrechnen", "prozentrechnung"],
            "aufgabenzuschnitt": {"A1": 48, "A2": 30, "A3": 22},
            "diagramm": "Kreisdiagramm: Anteil je Postart am Posteingang",
            "tv_objekt": "Dokumentvorlage Laufzettel als .dotx mit "
                         "WordArt-Kopf und Autotext-Fußzeile",
            "kommunikationsform": "innerbetriebliche Mitteilung",
            "eingesetzte_funktionen": ["SVERWEIS (FALSCH)", "STUNDE", "MINUTE",
                                       "WENN", "ANZAHL2", "ZÄHLENWENN",
                                       "SUMME"],
            "pflichtelemente_belegt": ["STUNDE/MINUTE", "ANZAHL/ANZAHL2",
                                       "Autotext", "WordArt"],
            "status": "geliefert",
        },
    }


def _bewertung():
    d = "; ".join(str(r["dauer"]) for r in Z)
    u = "; ".join(r["urteil"] for r in Z)
    anteile = "; ".join(f"{a['postart']} {_prozent(a['anteil'])}"
                        for a in ANTEILE).replace("\u00a0", " ")
    return [
        {"nr": "1a", "punkte": 5,
         "leistung": "Die zehn Vorgänge stehen zeilengerecht in A4:D13 des "
                     "Blattes Ausw, in der Reihenfolge der Anlage 2.",
         "hinweis": "Je Zeile 0,4 Punkte für die vollständige und richtige "
                    "Übernahme aller vier Angaben; 1 Punkt für die "
                    "eingehaltene Reihenfolge. Die Uhrzeiten sind als Zeit "
                    "erfasst, nicht als Text.",
         "toleranz": "Uhrzeit als Text (linksbündig, führendes Apostroph): "
                     "0,5 Punkte Abzug je betroffener Zeile, weil die "
                     "Folgerechnung in Spalte F daran scheitert."},
        {"nr": "1b", "punkte": 5,
         "leistung": "Spalte E enthält je Zeile eine kopierfähige Formel, die "
                     "die ausgeschriebene Postart aus dem Blatt Post holt.",
         "hinweis": "E4: =SVERWEIS(B4;Post!$A$4:$C$8;2;FALSCH), nach unten "
                    "kopiert. Exakte Suche über das Kürzel. Ergebnisse: "
                    + "; ".join(r["postart"] for r in Z) + ".",
         "toleranz": "Fehlender absoluter Bezug bei richtigem Ergebnis: "
                     "2 Punkte Abzug, weil die Formel nicht kopierfähig ist. "
                     "Bereichssuche mit richtigem Ergebnis: 1 Punkt Abzug, "
                     "weil die Kürzelliste unsortiert wäre."},
        {"nr": "1c", "punkte": 7,
         "leistung": "Spalte F enthält je Zeile eine kopierfähige Formel, die "
                     "die Bearbeitungsdauer in Minuten aus den beiden "
                     "Uhrzeiten ermittelt.",
         "hinweis": "F4: =STUNDE(D4-C4)*60+MINUTE(D4-C4), nach unten kopiert. "
                    f"Ergebnisse: {d}. 3 Punkte für die Stundenkomponente, "
                    "2 Punkte für die Minutenkomponente, 2 Punkte für die "
                    "Kopierfähigkeit.",
         "toleranz": "Rechenweg über (D4-C4)*1440 mit richtigem Ergebnis: "
                     "volle Punktzahl, sofern die Zelle als Zahl formatiert "
                     "ist. Nur MINUTE(D4-C4): 4 Punkte Abzug; die vier "
                     "stundenübergreifenden Vorgänge P-2604, P-2606, P-2609 "
                     "und P-2610 sind dann sichtbar falsch."},
        {"nr": "1d", "punkte": 4,
         "leistung": "Spalte G enthält je Zeile eine kopierfähige Formel, die "
                     "die vereinbarte Sollzeit aus dem Blatt Post holt.",
         "hinweis": "G4: =SVERWEIS(B4;Post!$A$4:$C$8;3;FALSCH), nach unten "
                    "kopiert. Ergebnisse: "
                    + "; ".join(str(r["soll"]) for r in Z) + ".",
         "toleranz": "Fehlender absoluter Bezug bei richtigem Ergebnis: "
                     "2 Punkte Abzug. Eingetippte Sollzeiten statt Formel: "
                     "0 Punkte."},
        {"nr": "1e", "punkte": 4,
         "leistung": "Spalte H enthält je Zeile eine kopierfähige Formel, die "
                     "bei Überschreiten der Sollzeit überschritten ausgibt.",
         "hinweis": 'H4: =WENN(F4>G4;"überschritten";"eingehalten"), nach '
                    f"unten kopiert. Ergebnisse: {u}.",
         "toleranz": "Schreibweise der Ausgabetexte muss übereinstimmen; Groß- "
                     "und Kleinschreibung zählt. Vergleich mit >= statt >: "
                     "2 Punkte Abzug; erkennbar an P-2603, der die Sollzeit "
                     "exakt trifft und eingehalten lauten muss."},
        {"nr": "1f", "punkte": 3,
         "leistung": "Zelle B16 enthält eine Formel für die Anzahl der "
                     "erfassten Vorgänge.",
         "hinweis": f"B16: =ANZAHL2(A4:A13). Ergebnis: {ANZ_VORGAENGE}. "
                    "ANZAHL scheidet aus, weil die Vorgangsnummern Text sind.",
         "toleranz": "ANZAHL2 über eine andere vollständig gefüllte Spalte mit "
                     "richtigem Ergebnis zählt voll. Eingetippte Zahl statt "
                     "Formel: 0 Punkte."},
        {"nr": "1g", "punkte": 3,
         "leistung": "Zelle B17 enthält eine Formel für die Anzahl der "
                     "Vorgänge über der Sollzeit.",
         "hinweis": 'B17: =ZÄHLENWENN(H4:H13;"überschritten"). Ergebnis: '
                    f"{ANZ_UEBERSCHRITTEN}.",
         "toleranz": "Zählung über einen Vergleich der Spalten F und G mit "
                     "richtigem Ergebnis zählt voll."},
        {"nr": "1h", "punkte": 2,
         "leistung": "Zelle B18 enthält eine Formel für die gesamte "
                     "Bearbeitungsdauer in Minuten.",
         "hinweis": f"B18: =SUMME(F4:F13). Ergebnis: {GESAMTDAUER}.",
         "toleranz": "Eingetippte Zahl statt Formel: 0 Punkte."},
        {"nr": "1i", "punkte": 4,
         "leistung": "Der Bereich B21 bis B25 enthält je Zeile eine "
                     "kopierfähige Formel für die Anzahl der Vorgänge je "
                     "Postart.",
         "hinweis": "B21: =ZÄHLENWENN($E$4:$E$13;A21), nach unten kopiert. "
                    "Ergebnisse: "
                    + "; ".join(f"{a['postart']} {a['anzahl']}"
                                for a in ANTEILE)
                    + ". Die Summe der fünf Werte ergibt 10.",
         "toleranz": "Zählung über die Kürzel in Spalte B mit richtigem "
                     "Ergebnis zählt voll. Fehlender absoluter Bezug bei "
                     "richtigem Ergebnis: 2 Punkte Abzug."},
        {"nr": "1j", "punkte": 5,
         "leistung": "Der Bereich C21 bis C25 enthält je Zeile eine "
                     "kopierfähige Formel für den Anteil der Postart am "
                     "gesamten Posteingang.",
         "hinweis": f"C21: =B21/$B$16, nach unten kopiert, Zelle im "
                    f"Prozentformat mit einer Dezimalstelle. Ergebnisse: "
                    f"{anteile}. Die Anteile summieren sich auf 100,0 %.",
         "toleranz": "Bezug auf die feste Zahl 10 statt auf B16 mit richtigem "
                     "Ergebnis: 1 Punkt Abzug. Multiplikation mit 100 bei "
                     "gleichzeitigem Prozentformat: 3 Punkte Abzug, weil das "
                     "Ergebnis dann 4000,0 % lautet."},
        {"nr": "1k", "punkte": 4,
         "leistung": "Im Blatt Ausw steht ab A28 ein Kreisdiagramm zum Anteil "
                     "der Postarten, gestaltet nach Anlage 5.",
         "hinweis": "Datenbereich: Rubriken A21:A25, Werte C21:C25. "
                    "Diagrammtitel und Legende sind gesetzt. 2 Punkte "
                    "Datenbereich, 1 Punkt Diagrammtyp, 1 Punkt "
                    "Beschriftungen. Achsenbeschriftungen entfallen, weil das "
                    "Kreisdiagramm keine Achsen hat.",
         "toleranz": "Diagramm über die Anzahl in Spalte B statt über den "
                     "Anteil in Spalte C: kein Abzug, das Kreisbild ist "
                     "identisch. Säulen- oder Balkendiagramm: 1 Punkt Abzug."},
        {"nr": "1 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind im Blatt Ausw "
                     "eingehalten.",
         "hinweis": "Geprüft werden: Uhrzeiten als SS:MM (Spalten C und D); "
                    "Bearbeitungsdauer, Sollzeit und Anzahlen ohne "
                    "Dezimalstellen; Anteile als Prozentwert mit einer "
                    "Dezimalstelle (Spalte C des Anteilsblocks); Arial 11 pt. "
                    "Abzüge im Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 0,5 Punkte Abzug, insgesamt "
                     "höchstens 2 Punkte."},

        {"nr": "2a", "punkte": 6,
         "leistung": "Oberhalb der Überschrift steht ein Schriftzug mit dem "
                     "Text Goldberg Designermöbel GmbH als Schrifteffekt, "
                     "zentriert und rund 12 cm breit.",
         "hinweis": "2 Punkte für einen echten Schrifteffekt (WordArt "
                    "beziehungsweise Fontwork), 2 Punkte für den richtigen "
                    "Wortlaut, 1 Punkt für die Zentrierung, 1 Punkt für die "
                    "Breite von rund 12 cm.",
         "toleranz": "Breite zwischen 11 und 13 cm zählt voll. Als "
                     "gewöhnlicher fetter Text gesetzt: 4 Punkte Abzug, weil "
                     "kein Schrifteffekt vorliegt."},
        {"nr": "2b", "punkte": 4,
         "leistung": "Die Überschrift Laufzettel Posteingang ist in Arial "
                     "14 pt, fett und zentriert formatiert; der Abstand nach "
                     "dem Absatz beträgt 12 pt.",
         "hinweis": "1 Punkt Schriftgrad, 1 Punkt Fettung, 1 Punkt "
                    "Zentrierung, 1 Punkt Absatzabstand. Der Abstand wird "
                    "über die Absatzformatierung gesetzt, nicht über eine "
                    "Leerzeile.",
         "toleranz": "Leerzeile statt Absatzabstand: 1 Punkt Abzug. Umsetzung "
                     "über eine selbst angelegte Formatvorlage zählt voll."},
        {"nr": "2c", "punkte": 7,
         "leistung": "Unterhalb des einleitenden Absatzes steht eine Tabelle "
                     "mit sechs Zeilen und zwei Spalten; die linke Spalte ist "
                     "5 cm, die rechte 10 cm breit.",
         "hinweis": "3 Punkte für die sechs Angaben in der richtigen "
                    "Reihenfolge, 2 Punkte für die beiden Spaltenbreiten, "
                    "2 Punkte für die Kopfzeile Angabe und Eintrag. Die "
                    "rechte Spalte bleibt leer, sie wird später ausgefüllt.",
         "toleranz": "Abweichung der Spaltenbreite bis 0,2 cm zählt voll. "
                     "Tabelle mit Tabulatoren nachgebaut: 5 Punkte Abzug."},
        {"nr": "2d", "punkte": 6,
         "leistung": "Die Fußzeile enthält Dateiname, Tagesdatum und "
                     "Seitenanzahl als Felder, zentriert in Arial 9 pt.",
         "hinweis": "Je Feld 1,5 Punkte, 1,5 Punkte für Zentrierung und "
                    "Schriftgrad. Geprüft wird über die Feldfunktion (Alt+F9), "
                    "nicht über den angezeigten Wert.",
         "toleranz": "Getippter Dateiname oder getipptes Datum statt Feld: je "
                     "1,5 Punkte Abzug, weil sich der Eintrag nicht "
                     "aktualisiert. Reihenfolge der drei Angaben frei."},
        {"nr": "2e", "punkte": 5,
         "leistung": "Die Datei liegt zusätzlich als Dokumentvorlage mit der "
                     "Endung .dotx unter der Teilnehmernummer und der "
                     "Aufgabennummer vor.",
         "hinweis": "3 Punkte für den Dateityp Word-Vorlage, 2 Punkte für den "
                    "Dateinamen nach dem Schema Nachname + TTMM + _A2. Prüfen "
                    "über den Dateityp im Explorer, nicht über die Endung "
                    "allein.",
         "toleranz": "Eine in .dotx umbenannte .docx-Datei: 3 Punkte Abzug, "
                     "sie öffnet sich nicht als Vorlage. Zusätzlich "
                     "gespeicherte .docx-Fassung: kein Abzug."},
        {"nr": "2 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind im Laufzettel "
                     "eingehalten.",
         "hinweis": "Geprüft werden: Arial 11 pt im Fließtext, Datumsangaben "
                    "als TT.MM.JJJJ, Uhrzeiten als SS:MM in den "
                    "Tabellenzeilen. Abzüge im Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 1 Punkt Abzug, insgesamt "
                     "höchstens 2 Punkte."},

        {"nr": "3a", "punkte": 5,
         "leistung": "Die Felder An, Von und Thema sind sachgerecht "
                     "ausgefüllt; das vorbereitete Datum bleibt unverändert.",
         "hinweis": "2 Punkte An (Abteilung Verwaltung/Büroorganisation), "
                    "1 Punkt Von (Ute Winkelmann mit Funktion), 2 Punkte "
                    "Thema mit Bezug auf die Auswertung der Kalenderwoche 35.",
         "toleranz": "Andere sinngemäße Formulierung des Themas zählt voll. "
                     "Verändertes Datum: 1 Punkt Abzug."},
        {"nr": "3b", "punkte": 5,
         "leistung": "Der einleitende Absatz nennt die vorgenommene Auswertung "
                     "und den Zeitraum der Kalenderwoche 35.",
         "hinweis": "2 Punkte Gegenstand der Auswertung, 2 Punkte Zeitraum "
                    "(24. bis 28.08.2026 oder Kalenderwoche 35), 1 Punkt "
                    "Kleinschreibung des ersten Wortes nach der Anrede.",
         "toleranz": "Großschreibung nach der Anrede: 1 Punkt Abzug. Anrede "
                     "an eine Gruppe, etwa Liebe Kolleginnen und Kollegen, "
                     "ist richtig; eine Einzelanrede: 1 Punkt Abzug."},
        {"nr": "3c", "punkte": 6,
         "leistung": "Die Mitteilung nennt die Zahl der Vorgänge über der "
                     "Sollzeit und schlägt den Laufzettel als Maßnahme vor.",
         "hinweis": "3 Punkte für die Zahl, die zur eigenen Auswertung aus "
                    "Aufgabe 1 passt (richtig sind fünf von zehn Vorgängen), "
                    "3 Punkte für den Vorschlag des Laufzettels mit dem Termin "
                    "01.09.2026.",
         "toleranz": "Eine Zahl, die zur eigenen fehlerhaften Auswertung "
                     "passt, gilt als Folgefehler und kostet hier keine "
                     "Punkte. Fehlender Termin: 1 Punkt Abzug."},
        {"nr": "3d", "punkte": 4,
         "leistung": "Die Mitteilung weist auf die beigefügte Auswertung hin "
                     "und schließt mit Grußformel und Namen ab.",
         "hinweis": "2 Punkte Hinweis auf die Anlage, 1 Punkt Grußformel, "
                    "1 Punkt Name der Absenderin. Die Angabe der Durchwahl "
                    "357-124 für Rückfragen zählt zum Hinweis.",
         "toleranz": "Andere übliche Grußformel zählt voll."},
        {"nr": "3 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind in der "
                     "Mitteilung eingehalten.",
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
            ("Punkteverteilung", "Aufgabe 1: 48 · Aufgabe 2: 30 · Aufgabe 3: 22 "
                                 "(je Aufgabe 2 Punkte für die Formatvorgaben)"),
            ("Stoffschwerpunkt", "Wirtschaftsrechnen, Prozentrechnung"),
            ("Abteilung", "Verwaltung/Büroorganisation"),
            ("Eingesetzte Funktionen", "SVERWEIS (exakte Suche), STUNDE, "
                                       "MINUTE, WENN, ANZAHL2, ZÄHLENWENN, "
                                       "SUMME"),
            ("Pflichtelemente", "STUNDE/MINUTE · ANZAHL/ANZAHL2 · Autotext · "
                                "WordArt"),
            ("Kommunikationsform", "Innerbetriebliche Mitteilung nach "
                                   "DIN 5008:2020"),
            ("Diagramm", "Kreisdiagramm, Anteil je Postart am Posteingang"),
        ],
        "zeitraster": [
            ("Einstieg und Rückmeldung der Gruppe", 5),
            ("Aufgabe 1, Teilaufgaben a bis e (Übernahme, Dauer, Beurteilung)",
             18),
            ("Aufgabe 1, Teilaufgaben f bis k (Kennzahlen, Anteile, Diagramm)",
             15),
            ("Aufgabe 2 (Laufzettel, Schrifteffekt, Fußzeile, Vorlage)", 12),
            ("Aufgabe 3 (Mitteilung nach DIN 5008:2020)", 8),
            ("Puffer und offene Fragen", 2),
        ],
        "stolperstellen": [
            ("1a", "Die Uhrzeiten werden als Text eingetippt, etwa mit "
                   "führendem Apostroph oder mit Punkt statt Doppelpunkt. Die "
                   "Berechnung in Spalte F liefert dann einen Fehlerwert."),
            ("1b", "Der Suchbereich im Blatt Post wird nicht absolut gesetzt; "
                   "beim Kopieren nach unten wandert er mit. Zweite "
                   "Stolperstelle: Bereichssuche statt exakter Suche, obwohl "
                   "die Kürzel nicht sortiert sind."),
            ("1c", "Es wird nur MINUTE gerechnet. Bei den vier Vorgängen, die "
                   "über eine volle Stunde laufen, fehlt dann eine Stunde: "
                   "P-2604 ergäbe 45 statt 105 Minuten."),
            ("1e", "Der Vergleich wird mit größer oder gleich statt mit größer "
                   "gesetzt. Sichtbar wird das nur bei P-2603, der die "
                   "Sollzeit exakt trifft."),
            ("1f", "Es wird ANZAHL statt ANZAHL2 verwendet. Weil die "
                   "Vorgangsnummern Text sind, lautet das Ergebnis dann 0."),
            ("1j", "Der Anteil wird mit 100 multipliziert und zusätzlich als "
                   "Prozentwert formatiert. Das Ergebnis lautet dann "
                   "4000,0 % statt 40,0 %."),
            ("1k", "Der Datenbereich wird über die ganze Auswertungstabelle "
                   "gezogen statt über den Anteilsblock in A21:C25."),
            ("2a", "Der Schriftzug wird als fetter Text gesetzt statt als "
                   "Schrifteffekt. In Word liegt WordArt im Register "
                   "Einfügen, in LibreOffice heißt es Fontwork."),
            ("2d", "Dateiname und Datum werden abgetippt statt als Feld "
                   "eingefügt. Mit Alt+F9 lässt sich das in der Besprechung "
                   "sofort zeigen."),
            ("2e", "Die Datei wird in .dotx umbenannt statt über Speichern "
                   "unter als Word-Vorlage gespeichert. Sie öffnet sich dann "
                   "nicht als Kopie."),
            ("3b", "Nach der Anrede wird großgeschrieben weitergeschrieben. "
                   "Richtig ist: Liebe Kolleginnen und Kollegen, / für die "
                   "Kalenderwoche 35 …"),
        ],
        "falschloesungen": [
            ["Nur MINUTE statt STUNDE und MINUTE", "1c",
             "4 Punkte Abzug; erkennbar an P-2604, P-2606, P-2609 und P-2610."],
            ["Vergleich mit größer oder gleich", "1e",
             "2 Punkte Abzug; erkennbar an P-2603."],
            ["ANZAHL statt ANZAHL2", "1f", "3 Punkte Abzug, Ergebnis 0."],
            ["Prozentwert zusätzlich mit 100 multipliziert", "1j",
             "3 Punkte Abzug, Ergebnis 4000,0 %."],
            ["Fehlender absoluter Bezug", "1b, 1d, 1i",
             "je 2 Punkte Abzug, weil die Formel nicht kopierfähig ist."],
            ["Schriftzug als fetter Text", "2a",
             "4 Punkte Abzug, kein Schrifteffekt vorhanden."],
            ["Dateiendung umbenannt statt Vorlage gespeichert", "2e",
             "3 Punkte Abzug."],
            ["Großschreibung nach der Anrede", "3b", "1 Punkt Abzug."],
        ],
        "fachklaerung": [
            ("Bearbeitungsdauer aus Uhrzeiten", "Excel führt Uhrzeiten als "
                                                "Bruchteil eines Tages. Die "
                                                "Differenz zweier Uhrzeiten "
                                                "ist deshalb wieder eine Zeit, "
                                                "keine Minutenzahl. STUNDE und "
                                                "MINUTE zerlegen sie; die "
                                                "Stunden werden mit 60 "
                                                "multipliziert und die Minuten "
                                                "addiert."),
            ("Sollzeit", "Vereinbarte Zeitspanne, innerhalb derer ein Vorgang "
                         "weitergegeben sein soll. Sie hängt an der Postart, "
                         "nicht am einzelnen Vorgang, und wird deshalb aus dem "
                         "Stammdatenblatt geholt statt eingetippt."),
            ("Anteilsrechnung", "Der Anteil ist der Quotient aus der Anzahl "
                                "einer Postart und der Gesamtzahl der "
                                "Vorgänge. Das Prozentformat multipliziert "
                                "bereits mit 100 — eine zusätzliche "
                                "Multiplikation im Rechenweg ist deshalb "
                                "falsch."),
            ("ANZAHL gegen ANZAHL2", "ANZAHL zählt nur Zahlen, ANZAHL2 zählt "
                                     "alle nicht leeren Zellen. Weil die "
                                     "Vorgangsnummern mit einem Buchstaben "
                                     "beginnen, ist hier ANZAHL2 die richtige "
                                     "Wahl."),
            ("Dokumentvorlage", "Eine Vorlage unterscheidet sich von einem "
                                "Dokument im Dateityp. Beim Öffnen legt Word "
                                "eine Kopie an, statt die Vorlage selbst zu "
                                "ändern. Genau das ist der Zweck des "
                                "Laufzettels: Er wird vielfach ausgefüllt, "
                                "die Vorlage bleibt unverändert."),
        ],
        "anschlussuebungen": [
            ("Zeitdifferenzen üben", "Fünf Uhrzeitpaare vorgeben, davon zwei "
                                     "über eine volle Stunde hinweg, und die "
                                     "Dauer in Minuten rechnen lassen."),
            ("Anteil gegen Prozentformat", "Dieselbe Spalte einmal mit und "
                                           "einmal ohne Multiplikation mit 100 "
                                           "rechnen lassen und beide Ergebnisse "
                                           "im Prozentformat vergleichen."),
            ("Vorlage gegen Dokument", "Eine .dotx und eine .docx nebeneinander "
                                       "öffnen lassen und beobachten, welche "
                                       "Datei sich beim Speichern selbst "
                                       "überschreibt."),
        ],
        "dateihinweise": [
            "Die Lösungsdatei zu Aufgabe 1 enthält echte Formeln. Öffnen Sie "
            "sie einmal in Excel, damit alle Werte neu berechnet werden. Die "
            "Datei enthält neben dem Auswertungsblatt und dem Blatt Post "
            "weitere Blätter mit Daten aus dem Modellunternehmen; sie werden "
            "nicht gebraucht, sind aber Teil der Arbeitsumgebung und bleiben "
            "erhalten.",
            "Die Lösungsdatei zu Aufgabe 2 ist eine echte Dokumentvorlage mit "
            "der Endung .dotx. Beim Doppelklick öffnet Word eine unbenannte "
            "Kopie — das ist richtig so und kein Fehler. Die Felder der "
            "Fußzeile zeigen beim Öffnen zunächst einen Platzhalter; "
            "aktualisieren Sie sie mit Strg+A und F9, bevor Sie korrigieren.",
            "Die Lösungsdatei zu Aufgabe 3 ist die ausgefüllte Goldberg-Vorlage "
            "für die innerbetriebliche Mitteilung. Das Datum ist in beiden "
            "Fassungen vorbereitet und wird nicht bewertet.",
        ],
    }
