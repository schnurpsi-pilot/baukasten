# -*- coding: utf-8 -*-
"""Blanko-Spezifikation — kopieren, umbenennen, ausfüllen.

Reihenfolge beim Bauen (§10.3): erst das Szenario, dann die Pflichtelemente,
die dazu natürlich passen. Niemals ein Szenario um eine Funktion herum
konstruieren.

Vollständiges Beispiel: saetze/nr01.py
"""
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP

from autoria.layout import eur, datum
from autoria.texte import hinweise

SATZNAME = "AP1-NrXX-V4-6"

# ============================================================ Kontrollrechnung
# Rechnet unabhängig von Excel. Liefert die Sollwerte für die Rechenprobe.
# Beim Zahlenentwurf §6.1 beachten: Bei ODER muss mindestens ein Datensatz nur
# eine Bedingung erfüllen, bei Rundung braucht es je einen Wert über und unter
# der 5 an der ersten wegfallenden Stelle.


def _rechnen():
    return []


Z = _rechnen()


# ================================================================ Spezifikation
def spec():
    dateien = {"a1": f"{SATZNAME}_A1_Teilnehmer.xlsx",
               "a2": f"{SATZNAME}_A2_Teilnehmer.docx",
               "a3": f"{SATZNAME}_A3_Teilnehmer.docx"}
    return {
        "meta": {
            "satzname": SATZNAME,
            "reihe": "AP1 Prüfungssimulationen Goldberg Designermöbel GmbH",
            "stand": "JJJJ-MM-TT",
            "bezeichnung": ["Abschlussprüfung Teil 1",
                            "Kaufleute für Büromanagement",
                            "Informationstechnisches Büromanagement"],
            "bearbeitungszeit": 120,     # §5.4, Obergrenze 120
            "gesamtpunkte": 100,
        },
        # Datei- und Blattnamen, die im Fließtext fett erscheinen (§18.3)
        "fettbegriffe": list(dateien.values()) + ["Ausw", "Kond", "Lief"],

        "sachverhalt": "5 bis 8 Zeilen Rahmenhandlung im Modellunternehmen (§5.2).",

        # Die fünf Pflichtpunkte nach §5.2 — Wortlaut zentral in
        # autoria/texte.py, hier nur die satzabhängigen Platzhalter füllen.
        # Nicht abschreiben und nicht umformulieren: der Absatz zur
        # Umsatzsteuer ist wörtlich vorgeschrieben.
        "hinweise": hinweise(beispieldatei="Weber1708_A1.xlsx"),

        # Nur die Zeilen, die der Satz braucht (§5.7 Teil 2)
        "formatvorgaben": [],

        # ---------------------------------------------------------- Arbeitsmappe
        # Ein Blatt mit "art": "auswertung", die Stammdatenblätter mit
        # "stammdaten": True, dazu mindestens fünf Zusatzblätter (§6.1).
        # Reihenfolge bewusst gemischt.
        "aktives_blatt": "",
        "blaetter": [],

        # Sollwerte für die Rechenprobe: {"Blatt!Zelle": wert}
        "erwartete_werte": {},

        # ------------------------------------------------------------- Aufgaben
        # typ steuert die Obergrenze der Teilaufgaben: tabellenkalkulation 12,
        # textverarbeitung 8, kommunikation 5 (§5.4).
        # punkte je Aufgabe = Summe der Teilaufgaben + 2 Formatpunkte (§5.2).
        "aufgaben": [],

        # -------------------------------------------------------------- Anlagen
        # Blocktypen: text, ueberschrift, felder, absaetze, tabelle, liste,
        # quellen, bild. "quer": True für breite Tabellen und Diagrammmuster.
        "anlagen": [],

        # --------------------------------------------------------- Aufgabendateien
        # art: "xlsx" | "dokument" | "vorlage"
        "dateien": [
            {"art": "xlsx", "praefix": "A1"},
        ],

        # ---------------------------------------------------------- Bewertung
        # Je Teilaufgabe eine Zeile plus je Aufgabe eine Zeile "N Format" (§9.3).
        "bewertung": [],

        # -------------------------------------------------------- Handreichung
        "handreichung": {
            "uebersicht": [], "zeitraster": [], "stolperstellen": [],
            "falschloesungen": [], "fachklaerung": [], "anschlussuebungen": [],
            "dateihinweise": [],
        },

        # ----------------------------------------------------- Historieneintrag
        "historie_eintrag": {
            "satzname": SATZNAME, "satzart": "vollpruefung",
            "szenario": "", "abteilung": "", "stoffschwerpunkt": [],
            "diagramm": "", "tv_objekt": "", "kommunikationsform": "",
            "eingesetzte_funktionen": [], "pflichtelemente_belegt": [],
            "status": "geliefert",
        },
    }
