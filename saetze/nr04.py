# -*- coding: utf-8 -*-
"""Satzspezifikation AP1-Nr04-V4-6 — Angebotsvergleich Bürodrehstühle.

Diese Datei ist das Referenzbeispiel: Sie zeigt, wie ein vollständiger Satz
beschrieben wird. Für einen neuen Satz kopieren, umbenennen und die Inhalte
austauschen. Der Rechenteil oben ist die unabhängige Kontrollrechnung — sie
liefert zugleich die Sollwerte für die Rechenprobe nach §14.1 Punkt 3.
"""
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP

from autoria.layout import eur, datum
from autoria.texte import hinweise

SATZNAME = "AP1-Nr04-V4-6"

# ============================================================ Kontrollrechnung
SCHWELLE_PREIS = Decimal("168.00")
SCHWELLE_TAGE = 35

RABATTSTAFFEL = [(Decimal("0.00"), Decimal("0.000")),
                 (Decimal("5000.00"), Decimal("0.020")),
                 (Decimal("10000.00"), Decimal("0.040")),
                 (Decimal("20000.00"), Decimal("0.060")),
                 (Decimal("22000.00"), Decimal("0.080")),
                 (Decimal("25000.00"), Decimal("0.100"))]

LIEFERANTEN = [
    (4101, "Sitzwerk Nord GmbH", "Rostock", 30, Decimal("0.020"), 10),
    (4102, "Ergoline Bürotechnik GmbH", "Kassel", 30, Decimal("0.030"), 8),
    (4103, "Vitagon Objekteinrichtung GmbH", "Ulm", 14, Decimal("0.015"), 14),
    (4104, "Kramm & Söhne Bürobedarf GmbH", "Bielefeld", 60, Decimal("0.025"), 10),
    (4105, "Merzhoff Akustikbau GmbH", "Erfurt", 30, Decimal("0.020"), 14),
    (4106, "Talberg Leuchten GmbH", "Aachen", 21, Decimal("0.010"), 7),
    (4107, "Nordfeld Bodenbeläge GmbH", "Flensburg", 30, Decimal("0.025"), 10),
    (4108, "Pralow Verpackungen GmbH", "Cottbus", 14, Decimal("0.015"), 10),
    (4109, "Sanderhoff Büromaterial GmbH", "Gera", 30, Decimal("0.030"), 8),
    (4110, "Weißenfeld Textil GmbH", "Hof", 45, Decimal("0.020"), 14),
]

ANGEBOTE = [
    (4101, "AN-2026-4417", dt.date(2026, 8, 3), dt.date(2026, 9, 30),
     Decimal("189.00"), 120, Decimal("145.00")),
    (4102, "26-08-0912", dt.date(2026, 8, 5), dt.date(2026, 9, 15),
     Decimal("174.50"), 120, Decimal("260.00")),
    (4103, "VO-8823", dt.date(2026, 8, 4), dt.date(2026, 9, 4),
     Decimal("168.00"), 120, Decimal("390.00")),
    (4104, "K-2026/551", dt.date(2026, 8, 7), dt.date(2026, 11, 7),
     Decimal("182.00"), 120, Decimal("0.00")),
]


def _tage360(d1, d2):
    """US-Methode wie Excel ohne drittes Argument."""
    t1, m1, j1 = d1.day, d1.month, d1.year
    t2, m2, j2 = d2.day, d2.month, d2.year
    if t1 == 31:
        t1 = 30
    if t2 == 31:
        if t1 == 30:
            t2 = 30
        else:
            t2, m2 = 1, m2 + 1
            if m2 == 13:
                m2, j2 = 1, j2 + 1
    return (j2 - j1) * 360 + (m2 - m1) * 30 + (t2 - t1)


def _rechnen():
    namen = {n: name for n, name, *_ in LIEFERANTEN}
    skonto = {n: sk for n, _na, _o, _z, sk, _f in LIEFERANTEN}
    rows = []
    for liefnr, angnr, dat, bis, preis, menge, fracht in ANGEBOTE:
        warenwert = preis * menge
        rsatz = max(s for g, s in RABATTSTAFFEL if warenwert >= g)
        rabatt = warenwert * rsatz
        sk = (warenwert - rabatt) * skonto[liefnr]
        bezug = warenwert - rabatt - sk + fracht
        je_stueck = (bezug / menge).quantize(Decimal("0.01"), ROUND_HALF_UP)
        rows.append(dict(name=namen[liefnr], liefnr=liefnr, angnr=angnr, datum=dat,
                         bis=bis, preis=preis, menge=menge, fracht=fracht,
                         warenwert=warenwert, rsatz=rsatz, rabatt=rabatt, skonto=sk,
                         bezug=bezug, je_stueck=je_stueck,
                         tage=_tage360(dat, bis)))
    sortiert = sorted(r["je_stueck"] for r in rows)
    for r in rows:
        r["rang"] = sortiert.index(r["je_stueck"]) + 1
        r["hinweis"] = ("Rücksprache"
                        if (r["je_stueck"] > SCHWELLE_PREIS
                            or r["tage"] < SCHWELLE_TAGE) else "freigegeben")
    return rows


Z = _rechnen()
MIN_JE_STUECK = min(r["je_stueck"] for r in Z)

# ==================================================================== Textteile
SACHVERHALT = (
    "Die Goldberg Designermöbel GmbH bezieht im Herbst ein zweites "
    "Verwaltungsgebäude in der Lorenzistraße. Für die Erstausstattung der Büros "
    "werden 120 Bürodrehstühle benötigt. Die Abteilung Beschaffung/Einkauf hat vier "
    "Angebote eingeholt. Die Angebote unterscheiden sich im Listenpreis, in der "
    "Frachtpauschale und in den Zahlungskonditionen. Frau Ines Kortmann, Leiterin "
    "der Abteilung Beschaffung/Einkauf, bittet Sie, die Angebote rechnerisch "
    "aufzubereiten, das Ergebnis in einem Kurzbericht festzuhalten und einen Brief "
    "an einen der Anbieter zu erstellen."
)

FORMATVORGABEN = [
    ["Geldbeträge", "zwei Dezimalstellen, Tausenderpunkt, Leerzeichen vor dem "
                    "Eurozeichen"],
    ["Prozentwerte", "eine Dezimalstelle"],
    ["Mengen und Stückzahlen", "ohne Dezimalstellen, ab fünf Stellen mit "
                               "Tausenderpunkt"],
    ["Zeitspannen in Tagen", "ganze Zahl, ohne Tausenderpunkt"],
    ["Rangfolge", "ganze Zahl, ohne Tausenderpunkt"],
    ["Datum", "TT.MM.JJJJ"],
    ["Schrift in allen Dateien", "Arial 11 pt"],
    ["Diagramm", "Titel, Legende und Achsenbeschriftung sichtbar"],
]

BERICHT_ABSAETZE = [
    "Die Goldberg Designermöbel GmbH stattet das neue Verwaltungsgebäude in der "
    "Lorenzistraße mit Bürodrehstühlen aus. Für die Erstausstattung werden 120 "
    "Stühle benötigt. Die Abteilung Beschaffung/Einkauf hat dazu vier Angebote "
    "eingeholt.",
    "Die Angebote unterscheiden sich im Listenpreis, in der Frachtpauschale und in "
    "den Zahlungskonditionen. Ein Vergleich allein über den Listenpreis führt "
    "deshalb zu keiner belastbaren Aussage. Maßgeblich ist der Bezugspreis je Stück.",
    "@@RABATT@@",
    "Alle Angebote sind bis zu einem festen Termin bindend. Läuft die Bindefrist vor "
    "der Entscheidung ab, muss erneut angefragt werden. Die verbleibende Bindefrist "
    "wird deshalb mit ausgewertet.",
]
RABATT_TEIL1 = ("Die Rabattsätze richten sich nach dem Warenwert des Auftrags. Die "
                "Staffel gilt für alle Anbieter gleichermaßen und ist in den "
                "Einkaufsunterlagen hinterlegt.")
RABATT_TEIL2 = (" Die Skontosätze sind dagegen anbieterbezogen vereinbart und stehen "
                "im Lieferantenstamm.")
PRUEFSCHRITTE = [
    "Übernahme der Angebotsdaten in die Auswertungstabelle",
    "Ermittlung von Warenwert, Rabattbetrag und Skontobetrag",
    "Ermittlung des Bezugspreises je Stück und der Rangfolge",
    "Kennzeichnung der Angebote, die eine Rücksprache erfordern",
]
BERICHT_SCHLUSS = ("Der Bericht geht nach Abschluss der Prüfung an die "
                   "Geschäftsführung. Über die Vergabe wird in der Sitzung am "
                   "10.09.2026 entschieden.")
UEBERSICHT_TEXT = "Die folgende Übersicht nennt die vier eingegangenen Angebote."
TAB_BERICHT_KOPF = ["Anbieter", "Angebotsnummer", "Angebotsdatum", "Angebot gültig bis"]
TAB_BERICHT = [[r["name"], r["angnr"], datum(r["datum"]), datum(r["bis"])] for r in Z]

FUSSNOTEN = {
    "@@FN1@@": "Einkaufsunterlagen der Goldberg Designermöbel GmbH, Rabattstaffel, "
               "Stand 01.07.2026.",
    "@@FN2@@": "Lieferantenstamm der Goldberg Designermöbel GmbH, Auszug vom "
               "10.08.2026.",
}


# ================================================================ Spezifikation
def spec():
    dateien = {"a1": f"{SATZNAME}_A1_Teilnehmer.xlsx",
               "a2": f"{SATZNAME}_A2_Teilnehmer.docx",
               "a3": f"{SATZNAME}_A3_Teilnehmer.docx"}

    return {
        "meta": {
            "satzname": SATZNAME,
            "reihe": "AP1 Prüfungssimulationen Goldberg Designermöbel GmbH",
            "hinweis": ("Der Satz setzt den Planeintrag Nr04 um und trägt "
                        "dessen laufende Nummer. Er entstand zunächst unter "
                        "v4.5 als AP1-V4-5-Nr01 und wurde mit v4.6 auf das "
                        "Namensschema AP1-Nr[NN]-V[Version] umgestellt (§11.2); "
                        "der frühere Name steht im Feld vorgaenger_satzname."),
            "bezeichnung": ["Abschlussprüfung Teil 1",
                            "Kaufleute für Büromanagement",
                            "Informationstechnisches Büromanagement"],
            "bearbeitungszeit": 120,
            "gesamtpunkte": 100,
        },
        "fettbegriffe": list(dateien.values()) + ["Ausw", "Kond", "Lief"],
        "sachverhalt": SACHVERHALT,
        "hinweise": hinweise(beispieldatei="Weber1708_A1.xlsx"),
        "formatvorgaben": FORMATVORGABEN,

        # ---------------------------------------------------------- Arbeitsmappe
        "aktives_blatt": "Pers",
        "blaetter": [
            {"name": "Pers", "titel": "Personalstamm Verwaltung",
             "kopf": ["Personal-nummer", "Name", "Abteilung", "Eintritt",
                      "Wochen-stunden"],
             "zeilen": [[70211, "Adam, Ruth", "Beschaffung/Einkauf",
                         dt.date(2018, 4, 1), 40],
                        [70214, "Berger, Timo", "Verwaltung/Büroorganisation",
                         dt.date(2019, 9, 16), 30],
                        [70220, "Kortmann, Ines", "Beschaffung/Einkauf",
                         dt.date(2015, 2, 2), 40],
                        [70231, "Lehnhoff, Marie", "Rechnungswesen/Controlling",
                         dt.date(2021, 7, 1), 35],
                        [70238, "Osterkamp, Jan", "Lager/Logistik",
                         dt.date(2020, 3, 2), 40],
                        [70244, "Reinbold, Sina", "Personal/Ausbildung",
                         dt.date(2017, 11, 2), 32],
                        [70251, "Thelen, Kaan", "Vertrieb", dt.date(2022, 1, 10), 40],
                        [70259, "Winkelmann, Ute", "Verwaltung/Büroorganisation",
                         dt.date(2016, 6, 1), 40]]},
            {"name": "Kond", "titel": "Rabattstaffel nach Warenwert",
             "stammdaten": True,
             "kopf": ["Warenwert ab in Euro", "Rabattsatz"],
             "breiten": [20, 14],
             "formate": ["eur", "prozent"],
             "zeilen": [[float(g), float(s)] for g, s in RABATTSTAFFEL]},
            {"name": "Fuhr", "titel": "Fuhrpark",
             "kopf": ["Kennzeichen", "Fahrzeugtyp", "Baujahr", "Kilometerstand",
                      "Nächste Prüfung"],
             "formate": [None, None, "ganz", "menge", "datum"],
             "zeilen": [["B-GD 1201", "Kastenwagen", 2021, 84200,
                         dt.date(2026, 11, 4)],
                        ["B-GD 1202", "Kastenwagen", 2019, 141750,
                         dt.date(2026, 9, 22)],
                        ["B-GD 1210", "Pritschenwagen", 2022, 46980,
                         dt.date(2027, 3, 18)],
                        ["B-GD 1215", "Kleintransporter", 2023, 29340,
                         dt.date(2027, 6, 9)],
                        ["B-GD 1220", "Pkw Kombi", 2020, 98110,
                         dt.date(2026, 10, 30)],
                        ["B-GD 1224", "Pkw Limousine", 2024, 15600,
                         dt.date(2028, 2, 14)]]},
            {"name": "Ausw", "art": "auswertung",
             "titel": "Angebotsvergleich Bürodrehstühle",
             "anzahl_zeilen": 4,
             "spalten": [
                 {"kopf": "Anbieter", "art": "text", "breite": 30,
                  "werte": [r["name"] for r in Z]},
                 {"kopf": "Lief.-Nr.", "breite": 13, "format": "menge",
                  "werte": [r["liefnr"] for r in Z]},
                 {"kopf": "Angebots-Nr.", "breite": 15, "ausrichtung": "center",
                  "werte": [r["angnr"] for r in Z]},
                 {"kopf": "Angebots-datum", "breite": 13, "format": "datum",
                  "werte": [r["datum"] for r in Z]},
                 {"kopf": "gültig bis", "breite": 13, "format": "datum",
                  "werte": [r["bis"] for r in Z]},
                 {"kopf": "Listenpreis in Euro", "breite": 14, "format": "eur",
                  "werte": [float(r["preis"]) for r in Z]},
                 {"kopf": "Menge in Stück", "breite": 11, "format": "menge",
                  "werte": [r["menge"] for r in Z]},
                 {"kopf": "Fracht in Euro", "breite": 15, "format": "eur",
                  "werte": [float(r["fracht"]) for r in Z]},
                 {"kopf": "Warenwert in Euro", "breite": 14, "format": "eur",
                  "formel": "=F{z}*G{z}"},
                 {"kopf": "Rabattsatz", "breite": 11, "format": "prozent",
                  "formel": "=VLOOKUP(I{z},Kond!$A$4:$B$9,2,TRUE)"},
                 {"kopf": "Rabattbetrag in Euro", "breite": 14, "format": "eur",
                  "formel": "=I{z}*J{z}"},
                 {"kopf": "Skontobetrag in Euro", "breite": 14, "format": "eur",
                  "formel": "=(I{z}-K{z})*VLOOKUP(B{z},Lief!$A$4:$F$13,5,FALSE)"},
                 {"kopf": "Bezugspreis in Euro", "breite": 14, "format": "eur",
                  "formel": "=I{z}-K{z}-L{z}+H{z}"},
                 {"kopf": "Bezugspreis je Stück in Euro", "breite": 15,
                  "format": "eur", "formel": "=ROUND(M{z}/G{z},2)"},
                 {"kopf": "Bindefrist in Tagen", "breite": 12, "format": "ganz",
                  "formel": "=DAYS360(D{z},E{z})"},
                 {"kopf": "Rangfolge", "breite": 11, "format": "ganz",
                  "formel": "=RANK(N{z},$N${erste}:$N${letzte},1)"},
                 {"kopf": "Hinweis", "breite": 14, "ausrichtung": "center",
                  "formel": '=IF(OR(N{z}>168,O{z}<35),"Rücksprache","freigegeben")'},
             ],
             "einzelzellen": [
                 {"label": "Niedrigster Bezugspreis je Stück in Euro",
                  "label_zelle": "A9", "zelle": "B9", "format": "eur",
                  "formel": "=MIN(N{erste}:N{letzte})"}],
             "diagramm": {"typ": "balken", "wertespalte": 14, "rubrikspalte": 1,
                          "titel": "Bezugspreis je Stück nach Anbieter",
                          "wertachse": "Bezugspreis je Stück in Euro",
                          "rubrikachse": "Anbieter", "position": "A12"}},
            {"name": "Tel", "titel": "Telefonverzeichnis",
             "kopf": ["Durchwahl", "Name", "Abteilung", "Funktion"],
             "zeilen": [["357-110", "Kortmann, Ines", "Beschaffung/Einkauf",
                         "Abteilungsleitung"],
                        ["357-112", "Adam, Ruth", "Beschaffung/Einkauf",
                         "Sachbearbeitung"],
                        ["357-120", "Winkelmann, Ute", "Verwaltung/Büroorganisation",
                         "Abteilungsleitung"],
                        ["357-131", "Lehnhoff, Marie", "Rechnungswesen/Controlling",
                         "Sachbearbeitung"],
                        ["357-140", "Osterkamp, Jan", "Lager/Logistik",
                         "Abteilungsleitung"],
                        ["357-150", "Reinbold, Sina", "Personal/Ausbildung",
                         "Abteilungsleitung"],
                        ["357-160", "Thelen, Kaan", "Vertrieb", "Sachbearbeitung"]]},
            {"name": "Lief", "titel": "Lieferantenstammdaten", "stammdaten": True,
             "kopf": ["Lieferanten-nummer", "Name", "Ort", "Zahlungsziel in Tagen",
                      "Skontosatz", "Skontofrist in Tagen"],
             "breiten": [13, 32, 16, 13, 11, 13],
             "formate": ["menge", None, None, "ganz", "prozent", "ganz"],
             "zeilen": [[nr, name, ort, zz, float(sk), sf]
                        for nr, name, ort, zz, sk, sf in LIEFERANTEN]},
            {"name": "Rekl", "titel": "Reklamationen laufendes Jahr",
             "kopf": ["Vorgangs-nummer", "Möbelserie", "Grund", "Eingang", "Erledigt"],
             "zeilen": [["R-2601", "Novara", "Transportschaden",
                         dt.date(2026, 1, 14), "ja"],
                        ["R-2607", "Belvento", "Fehlteil", dt.date(2026, 2, 3), "ja"],
                        ["R-2612", "Novara", "Oberflächenfehler",
                         dt.date(2026, 3, 21), "ja"],
                        ["R-2619", "Cortina", "Falschlieferung",
                         dt.date(2026, 4, 8), "nein"],
                        ["R-2626", "Belvento", "Transportschaden",
                         dt.date(2026, 5, 19), "ja"],
                        ["R-2633", "Marano", "Fehlteil", dt.date(2026, 6, 30),
                         "nein"],
                        ["R-2641", "Cortina", "Oberflächenfehler",
                         dt.date(2026, 7, 24), "nein"]]},
            {"name": "Urlaub", "titel": "Urlaubsplan Verwaltung",
             "kopf": ["Name", "Beginn", "Ende", "Arbeitstage", "Genehmigt"],
             "zeilen": [["Adam, Ruth", dt.date(2026, 9, 7), dt.date(2026, 9, 18),
                         10, "ja"],
                        ["Berger, Timo", dt.date(2026, 10, 5), dt.date(2026, 10, 9),
                         5, "ja"],
                        ["Lehnhoff, Marie", dt.date(2026, 9, 21),
                         dt.date(2026, 10, 2), 10, "nein"],
                        ["Osterkamp, Jan", dt.date(2026, 11, 2),
                         dt.date(2026, 11, 13), 10, "ja"],
                        ["Reinbold, Sina", dt.date(2026, 12, 21),
                         dt.date(2026, 12, 31), 7, "ja"],
                        ["Winkelmann, Ute", dt.date(2026, 8, 31),
                         dt.date(2026, 9, 4), 5, "ja"]]},
            {"name": "Lagor", "titel": "Lagerorte Zentrallager",
             "kopf": ["Lagerort", "Halle", "Regalreihe", "Stellplätze", "Belegt"],
             "zeilen": [["ZL-A-01", "A", 1, 48, 41], ["ZL-A-02", "A", 2, 48, 36],
                        ["ZL-B-01", "B", 1, 60, 57], ["ZL-B-02", "B", 2, 60, 22],
                        ["ZL-C-01", "C", 1, 36, 30], ["ZL-C-02", "C", 2, 36, 12]]},
        ],

        # Sollwerte für die Rechenprobe (§14.1 Punkt 3).
        "erwartete_werte": {
            **{f"Ausw!{sp}{4 + i}": float(Z[i][key])
               for sp, key in [("I", "warenwert"), ("K", "rabatt"), ("L", "skonto"),
                               ("M", "bezug"), ("N", "je_stueck")]
               for i in range(4)},
            **{f"Ausw!O{4 + i}": Z[i]["tage"] for i in range(4)},
            **{f"Ausw!P{4 + i}": Z[i]["rang"] for i in range(4)},
            **{f"Ausw!Q{4 + i}": Z[i]["hinweis"] for i in range(4)},
            "Ausw!B9": float(MIN_JE_STUECK),
        },

        # ------------------------------------------------------------- Aufgaben
        "aufgaben": [
            {"nr": 1, "typ": "tabellenkalkulation", "titel": "Tabellenkalkulation",
             "punkte": 48,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a1']}. Sie arbeiten im "
                            "Blatt Ausw. Die Stammdaten stehen in den Blättern Lief "
                            "und Kond."),
             "teilaufgaben": [
                 ("a", "Übertragen Sie die Angaben der vier Angebote aus Anlage 2 in "
                       "den Bereich A4 bis H7 des Blattes Ausw. Halten Sie die "
                       "Reihenfolge der Anlage ein.", 5),
                 ("b", "Ermitteln Sie in Spalte I den Warenwert je Angebot.", 2),
                 ("c", "Ermitteln Sie in Spalte J den Rabattsatz je Angebot. Die "
                       "Staffel steht im Blatt Kond und richtet sich nach dem "
                       "Warenwert.", 5),
                 ("d", "Ermitteln Sie in Spalte K den Rabattbetrag je Angebot.", 2),
                 ("e", "Ermitteln Sie in Spalte L den Skontobetrag je Angebot. Die "
                       "Skontosätze stehen im Blatt Lief.", 5),
                 ("f", "Ermitteln Sie in Spalte M den Bezugspreis je Angebot.", 3),
                 ("g", "Ermitteln Sie in Spalte N den Bezugspreis je Stück. Runden "
                       "Sie das Ergebnis kaufmännisch auf zwei Dezimalstellen.", 4),
                 ("h", "Ermitteln Sie in Spalte O die Bindefrist in Tagen zwischen "
                       "dem Angebotsdatum und dem letzten Tag der Bindung. Rechnen "
                       "Sie mit 30 Tagen je Monat.", 4),
                 ("i", "Ermitteln Sie in Spalte P die Rangfolge der Angebote nach dem "
                       "Bezugspreis je Stück. Der niedrigste Bezugspreis je Stück "
                       "erhält den Rang 1.", 3),
                 ("j", "Geben Sie in Spalte Q einen Hinweis aus. Es soll "
                       "@@Rücksprache@@ erscheinen, wenn der Bezugspreis je Stück "
                       "über 168,00 Euro liegt oder die Bindefrist unter 35 Tagen "
                       "liegt. In allen anderen Fällen soll @@freigegeben@@ "
                       "erscheinen.", 5),
                 ("k", "Ermitteln Sie in Zelle B9 den niedrigsten Bezugspreis je "
                       "Stück.", 2),
                 ("l", "Erstellen Sie im Blatt Ausw ab Zelle A12 ein Balkendiagramm "
                       "zum Bezugspreis je Stück der vier Anbieter. Gestalten Sie es "
                       "nach dem Muster in Anlage 5.", 6),
             ]},
            {"nr": 2, "typ": "textverarbeitung", "titel": "Textverarbeitung",
             "punkte": 30,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a2']}. Die Unterlagen "
                            "dazu stehen in Anlage 3."),
             "teilaufgaben": [
                 ("a", "Formatieren Sie die Überschrift in der ersten Zeile: Arial "
                       "14 pt, fett, zentriert, Abstand nach 12 pt.", 3),
                 ("b", "Formatieren Sie die drei Zwischenüberschriften Ausgangslage, "
                       "Angebotsübersicht und Prüfschritte: Arial 12 pt, fett, "
                       "Abstand vor 12 pt.", 4),
                 ("c", "Formatieren Sie die vier Absätze des Abschnitts Ausgangslage "
                       "im Blocksatz.", 3),
                 ("d", "Formatieren Sie die vier Zeilen des Abschnitts Prüfschritte "
                       "als Aufzählung mit hängendem Einzug von 0,5 cm.", 4),
                 ("e", "Fügen Sie die beiden Quellenangaben aus Anlage 3 als Fußnoten "
                       "an den Stellen ein, die im Text mit (1) und (2) "
                       "gekennzeichnet sind. Entfernen Sie dabei die "
                       "Kennzeichnungen.", 7),
                 ("f", "Erstellen Sie unterhalb des Absatzes im Abschnitt "
                       "Angebotsübersicht eine Tabelle mit den Angaben aus "
                       "Anlage 3.", 7),
             ]},
            {"nr": 3, "typ": "kommunikation", "titel": "Geschäftliche Kommunikation",
             "punkte": 22,
             "einleitung": (f"Öffnen Sie die Datei {dateien['a3']}. Das Datum ist "
                            "bereits eingetragen. Die Angaben für den Brief stehen in "
                            "Anlage 4. Beachten Sie DIN 5008:2020."),
             "teilaufgaben": [
                 ("a", "Vervollständigen Sie das Anschriftfeld und den "
                       "Informationsblock.", 4),
                 ("b", "Formulieren Sie die Betreffzeile.", 2),
                 ("c", "Nehmen Sie einleitend Bezug auf das Angebot vom "
                       "04.08.2026.", 4),
                 ("d", "Teilen Sie mit, bis zu welchem Termin die Bindefrist "
                       "verlängert werden soll, und begründen Sie die Bitte.", 5),
                 ("e", "Bitten Sie um eine schriftliche Rückmeldung und schließen Sie "
                       "den Brief ab.", 5),
             ]},
        ],

        # -------------------------------------------------------------- Anlagen
        "anlagen": [
            {"nr": 1, "titel": "E-Mail der Abteilungsleitung",
             "gehoert_zu": "Aufgaben 1 bis 3",
             "bloecke": [
                 {"typ": "felder", "paare": [
                     ("Von", "ines.kortmann@goldberg.test"),
                     ("An", "einkauf@goldberg.test"),
                     ("Datum", "26.08.2026"),
                     ("Betreff", "Angebotsprüfung Bürodrehstühle – Auswertung und "
                                 "Schriftverkehr")]},
                 {"typ": "absaetze", "zeilen": [
                     "Guten Morgen,", "",
                     "für die Erstausstattung des zweiten Verwaltungsgebäudes liegen "
                     "mir vier Angebote über je 120 Bürodrehstühle vor. Die Angebote "
                     "sind in Anlage 2 zusammengestellt.", "",
                     "Bitte werten Sie die Angebote in der Arbeitsmappe aus und "
                     "ermitteln Sie den Bezugspreis je Stück sowie die Rangfolge der "
                     "Anbieter. Halten Sie das Ergebnis anschließend im Kurzbericht "
                     "fest; die Unterlagen dazu finden Sie in Anlage 3.", "",
                     "Die Geschäftsführung entscheidet erst in der Sitzung am "
                     "10.09.2026 über die Vergabe. Ein Angebot läuft vorher ab. Die "
                     "Angaben für den erforderlichen Brief habe ich Ihnen in Anlage 4 "
                     "notiert.", "",
                     "Vielen Dank und freundliche Grüße", "Ines Kortmann",
                     "Leiterin Beschaffung/Einkauf"]},
             ]},
            {"nr": 2, "titel": "Angebotsübersicht und Konditionen",
             "gehoert_zu": "Aufgabe 1", "quer": True,
             "bloecke": [
                 {"typ": "text", "text": "Übertragen Sie die folgenden Angaben "
                                         "positionsgerecht in die "
                                         "Auswertungstabelle."},
                 {"typ": "tabelle",
                  "kopf": ["Anbieter", "Lief.-Nr.", "Angebots-Nr.", "Angebots-datum",
                           "gültig bis", "Listenpreis in Euro", "Menge in Stück",
                           "Fracht in Euro"],
                  "zeilen": [[r["name"], str(r["liefnr"]), r["angnr"],
                              datum(r["datum"]), datum(r["bis"]), eur(r["preis"]),
                              str(r["menge"]), eur(r["fracht"])] for r in Z],
                  "zahlenspalten": [1, 5, 6, 7]},
                 {"typ": "ueberschrift", "text": "Konditionen"},
                 {"typ": "liste", "zeilen": [
                     "Der Rabatt ist am Warenwert bemessen. Die Rabattstaffel gilt "
                     "für alle Anbieter gleichermaßen und steht im Blatt Kond der "
                     "Arbeitsmappe.",
                     "Das Skonto ist am Warenwert abzüglich Rabatt bemessen. Die "
                     "Skontosätze sind anbieterbezogen vereinbart und stehen im "
                     "Blatt Lief der Arbeitsmappe.",
                     "Die Frachtpauschale ist weder rabatt- noch skontofähig.",
                     "Alle Angebote umfassen je 120 Bürodrehstühle des gleichen "
                     "Ausstattungsstandards."]},
             ]},
            {"nr": 3, "titel": "Unterlagen für den Kurzbericht",
             "gehoert_zu": "Aufgabe 2",
             "bloecke": [
                 {"typ": "ueberschrift", "text": "Quellenangaben für die Fußnoten",
                  "vor": 0},
                 {"typ": "quellen", "eintraege": [
                     ("(1)", FUSSNOTEN["@@FN1@@"]), ("(2)", FUSSNOTEN["@@FN2@@"])]},
                 {"typ": "ueberschrift", "text": "Angaben für die Tabelle"},
                 {"typ": "tabelle", "kopf": TAB_BERICHT_KOPF, "zeilen": TAB_BERICHT},
             ]},
            {"nr": 4, "titel": "Aktennotiz zur Bindefrist", "gehoert_zu": "Aufgabe 3",
             "bloecke": [
                 {"typ": "felder", "paare": [
                     ("Datum", "26.08.2026"),
                     ("Verfasserin", "Ines Kortmann, Leiterin Beschaffung/Einkauf"),
                     ("Betrifft", "Bindefrist des Angebots VO-8823")]},
                 {"typ": "text", "text":
                     "Das Angebot der Vitagon Objekteinrichtung GmbH trägt die Nummer "
                     "VO-8823 und datiert vom 04.08.2026. Es ist bis zum 04.09.2026 "
                     "bindend."},
                 {"typ": "text", "text":
                     "Über die Vergabe entscheidet die Geschäftsführung in der "
                     "Sitzung am 10.09.2026. Die Bindefrist soll deshalb bis zum "
                     "20.09.2026 verlängert werden. Die Rückmeldung des Anbieters "
                     "wird bis zum 03.09.2026 benötigt."},
                 {"typ": "text", "text":
                     "Ansprechpartnerin beim Anbieter ist Frau Britta Sanwald, "
                     "Vitagon Objekteinrichtung GmbH, Neutorstraße 42, 89073 Ulm."},
                 {"typ": "text", "text":
                     "Den Brief zeichnet Frau Ruth Adam, Sachbearbeiterin "
                     "Beschaffung/Einkauf, Telefon 030 123456-112, Telefax "
                     "030 123456-100, E-Mail ruth.adam@goldberg.test — Unser Zeichen: "
                     "kor-ad. Der Brief wird auf den 27.08.2026 datiert; das Datum "
                     "ist in der Datei bereits eingetragen."},
             ]},
            {"nr": 5, "titel": "Gestaltungsmuster für das Diagramm",
             "gehoert_zu": "Aufgabe 1", "quer": True,
             "bloecke": [
                 {"typ": "text", "text":
                     "Das Muster zeigt ausschließlich Aufbau und Gestaltung. Die "
                     "abgebildeten Werte und Bezeichnungen gehören nicht zur "
                     "Aufgabe.", "nach": 10},
                 {"typ": "bild", "pfad": "muster_balken.png", "breite": 22.0},
             ]},
        ],

        # --------------------------------------------------------- Aufgabendateien
        "dateien": [
            {"art": "xlsx", "praefix": "A1"},
            {"art": "dokument", "praefix": "A2",
             "fussnoten": FUSSNOTEN,
             "teilnehmer": (
                 [{"typ": "absatz", "text": "Bericht zur Angebotsprüfung "
                                            "Bürodrehstühle"},
                  {"typ": "absatz", "text": "Ausgangslage"}]
                 + [{"typ": "absatz",
                     "text": (t.replace("@@RABATT@@",
                                        RABATT_TEIL1 + " (1)" + RABATT_TEIL2 + " (2)")
                              if "@@RABATT@@" in t else t)}
                    for t in BERICHT_ABSAETZE]
                 + [{"typ": "absatz", "text": "Angebotsübersicht"},
                    {"typ": "absatz", "text": UEBERSICHT_TEXT},
                    {"typ": "absatz", "text": "Prüfschritte"}]
                 + [{"typ": "absatz", "text": t} for t in PRUEFSCHRITTE]
                 + [{"typ": "absatz", "text": BERICHT_SCHLUSS}]),
             "loesung": (
                 [{"typ": "ueberschrift", "text": "Bericht zur Angebotsprüfung "
                                                  "Bürodrehstühle",
                   "groesse": 14, "vor": 0, "nach": 12, "zentriert": True},
                  {"typ": "ueberschrift", "text": "Ausgangslage"}]
                 + [({"typ": "absatz", "blocksatz": True, "teile": [
                         (RABATT_TEIL1, {}), ("@@FN1@@", {}),
                         (RABATT_TEIL2, {}), ("@@FN2@@", {})]}
                     if "@@RABATT@@" in t
                     else {"typ": "absatz", "text": t, "blocksatz": True})
                    for t in BERICHT_ABSAETZE]
                 + [{"typ": "ueberschrift", "text": "Angebotsübersicht"},
                    {"typ": "absatz", "text": UEBERSICHT_TEXT, "blocksatz": True},
                    {"typ": "tabelle", "kopf": TAB_BERICHT_KOPF,
                     "zeilen": TAB_BERICHT},
                    {"typ": "leer", "nach": 0},
                    {"typ": "ueberschrift", "text": "Prüfschritte"},
                    {"typ": "aufzaehlung", "zeilen": PRUEFSCHRITTE},
                    {"typ": "absatz", "text": BERICHT_SCHLUSS, "vor": 12,
                     "blocksatz": True}])},
            {"art": "vorlage", "praefix": "A3", "form": "brief",
             "teilnehmer": {"infoblock": {"datum": "27.08.2026"}},
             "loesung": {
                 "empfaenger": ["Vitagon Objekteinrichtung GmbH",
                                "Frau Britta Sanwald", "Neutorstraße 42",
                                "89073 Ulm"],
                 "infoblock": {"ihr_zeichen": "VO-8823",
                               "ihre_nachricht_vom": "04.08.2026",
                               "unser_zeichen": "kor-ad", "name": "Ruth Adam",
                               "telefon": "030 123456-112", "telefax": "030 123456-100",
                               "email": "ruth.adam@goldberg.test",
                               "datum": "27.08.2026"},
                 "betreff": "Angebot VO-8823 vom 04.08.2026 – Bitte um Verlängerung "
                            "der Bindefrist",
                 "absaetze": [
                     "Sehr geehrte Frau Sanwald,", "",
                     "vielen Dank für Ihr Angebot vom 04.08.2026 über 120 "
                     "Bürodrehstühle. Wir haben Ihre Unterlagen geprüft und in "
                     "unseren Angebotsvergleich aufgenommen.", "",
                     "Ihr Angebot ist bis zum 04.09.2026 bindend. Über die Vergabe "
                     "entscheidet unsere Geschäftsführung jedoch erst in der Sitzung "
                     "am 10.09.2026. Wir bitten Sie deshalb, die Bindefrist bis zum "
                     "20.09.2026 zu verlängern.", "",
                     "Bitte bestätigen Sie uns die Verlängerung schriftlich bis zum "
                     "03.09.2026. Für Rückfragen erreichen Sie mich unter der oben "
                     "genannten Durchwahl.", "",
                     "Mit freundlichen Grüßen", ""],
                 "schluss": ["Goldberg Designermöbel GmbH", "Ruth Adam"]}},
        ],

        # ---------------------------------------------------------- Bewertung
        "bewertung": _bewertung(),

        # -------------------------------------------------------- Handreichung
        "handreichung": _handreichung(),

        # ----------------------------------------------------- Historieneintrag
        "historie_eintrag": {
            "satzname": SATZNAME, "nummer": "04",
            "vorgaenger_satzname": "AP1-V4-5-Nr01",
            "satzart": "vollpruefung", "bearbeitungszeit_min": 120,
            "gesamtpunkte": 100, "abteilung": "Beschaffung/Einkauf",
            "szenario": "Angebotsvergleich Bürodrehstühle mit Rabatt- und "
                        "Skontostaffel",
            "stoffschwerpunkt": ["angebotsvergleich", "bezugspreisermittlung"],
            "aufgabenzuschnitt": {"A1": 48, "A2": 30, "A3": 22},
            "diagramm": "Balkendiagramm: Bezugspreis je Stück nach Anbieter",
            "tv_objekt": "Kurzbericht mit Quellenfußnoten und eingefügter "
                         "Angebotstabelle",
            "kommunikationsform": "Brief",
            "eingesetzte_funktionen": ["SVERWEIS (WAHR)", "SVERWEIS (FALSCH)",
                                       "RUNDEN", "TAGE360", "RANG", "WENN", "ODER",
                                       "MIN"],
            "pflichtelemente_belegt": ["RANG", "TAGE360", "ODER", "Fußnote"],
            "status": "geliefert",
        },
    }


def _bewertung():
    e = lambda k: "; ".join(eur(r[k], nbsp=False) for r in Z)
    return [
        {"nr": "1a", "punkte": 5,
         "leistung": "Die Angaben der vier Angebote stehen zeilengerecht in A4:H7 des "
                     "Blattes Ausw, in der Reihenfolge der Anlage 2.",
         "hinweis": "Je Zeile 1 Punkt für die vollständige und richtige Übernahme "
                    "aller acht Angaben; 1 Punkt für die eingehaltene Reihenfolge. "
                    "Datums- und Geldangaben als Zahl, nicht als Text.",
         "toleranz": "Zahlendreher in einer einzelnen Angabe: 0,5 Punkte Abzug in der "
                     "betroffenen Zeile."},
        {"nr": "1b", "punkte": 2,
         "leistung": "Spalte I enthält je Zeile eine kopierfähige Formel für den "
                     "Warenwert.",
         "hinweis": f"I4: =F4*G4, nach unten kopiert. Ergebnisse: {e('warenwert')}.",
         "toleranz": "Jede Formel, die zum richtigen Ergebnis führt. Eingetippte Zahl "
                     "statt Formel: 0 Punkte."},
        {"nr": "1c", "punkte": 5,
         "leistung": "Spalte J enthält je Zeile eine kopierfähige Formel, die den "
                     "Rabattsatz aus dem Blatt Kond anhand des Warenwerts holt.",
         "hinweis": "J4: =SVERWEIS(I4;Kond!$A$4:$B$9;2;WAHR), nach unten kopiert. "
                    "Bereichssuche, weil die Staffel nach Wertgrenzen aufgebaut ist. "
                    "Ergebnisse: 8,0 %; 6,0 %; 6,0 %; 6,0 %.",
         "toleranz": "Absolut gesetzte Matrix mit gleichem Ergebnis in anderer "
                     "Schreibweise zählt voll. Fehlender absoluter Bezug bei "
                     "richtigem Ergebnis: 2 Punkte Abzug (nicht kopierfähig). "
                     "Verschachtelte WENN-Kette mit richtigem Ergebnis: volle "
                     "Punktzahl."},
        {"nr": "1d", "punkte": 2,
         "leistung": "Spalte K enthält je Zeile eine kopierfähige Formel für den "
                     "Rabattbetrag.",
         "hinweis": f"K4: =I4*J4, nach unten kopiert. Ergebnisse: {e('rabatt')}.",
         "toleranz": "Jede Formel mit richtigem Ergebnis."},
        {"nr": "1e", "punkte": 5,
         "leistung": "Spalte L enthält je Zeile eine kopierfähige Formel, die den "
                     "Skontosatz aus dem Blatt Lief holt und auf den Warenwert "
                     "abzüglich Rabatt anwendet.",
         "hinweis": "L4: =(I4-K4)*SVERWEIS(B4;Lief!$A$4:$F$13;5;FALSCH), nach unten "
                    f"kopiert. Exakte Suche über die Lieferantennummer. Ergebnisse: "
                    f"{e('skonto')}.",
         "toleranz": "Hilfsspalte mit dem Skontosatz und anschließender "
                     "Multiplikation zählt voll. Fehlender absoluter Bezug bei "
                     "richtigem Ergebnis: 2 Punkte Abzug. Skonto auf den Warenwert "
                     "ohne Rabattabzug: 3 Punkte Abzug."},
        {"nr": "1f", "punkte": 3,
         "leistung": "Spalte M enthält je Zeile eine kopierfähige Formel für den "
                     "Bezugspreis.",
         "hinweis": "M4: =I4-K4-L4+H4, nach unten kopiert. Die Frachtpauschale kommt "
                    f"ungekürzt hinzu. Ergebnisse: {e('bezug')}.",
         "toleranz": "Rechenweg über Zwischenspalten zählt voll. Fracht in die "
                     "Rabatt- oder Skontobasis einbezogen: 2 Punkte Abzug."},
        {"nr": "1g", "punkte": 4,
         "leistung": "Spalte N enthält je Zeile eine kopierfähige Formel für den "
                     "kaufmännisch auf zwei Dezimalstellen gerundeten Bezugspreis je "
                     "Stück.",
         "hinweis": f"N4: =RUNDEN(M4/G4;2), nach unten kopiert. Ergebnisse: "
                    f"{e('je_stueck')}. Ohne Rundungsfunktion weicht Zeile 5 "
                    "(161,2757…) sichtbar ab.",
         "toleranz": "Nur Zellformatierung statt Rundungsfunktion: 2 Punkte Abzug, "
                     "weil der Wert nicht gerundet ist. Auf- oder Abrunden statt "
                     "kaufmännisch runden: 2 Punkte Abzug."},
        {"nr": "1h", "punkte": 4,
         "leistung": "Spalte O enthält je Zeile eine kopierfähige Formel für die "
                     "Bindefrist in Tagen auf Basis von 30 Tagen je Monat.",
         "hinweis": "O4: =TAGE360(D4;E4), nach unten kopiert. Ergebnisse: "
                    + "; ".join(str(r["tage"]) for r in Z) + ".",
         "toleranz": "Europäische Methode als drittes Argument liefert hier dieselben "
                     "Werte und zählt voll. Einfache Datumsdifferenz (58; 41; 31; "
                     "92): 3 Punkte Abzug."},
        {"nr": "1i", "punkte": 3,
         "leistung": "Spalte P enthält je Zeile eine kopierfähige Formel für die "
                     "aufsteigende Rangfolge nach dem Bezugspreis je Stück.",
         "hinweis": "P4: =RANG(N4;$N$4:$N$7;1), nach unten kopiert. Ergebnisse: "
                    + "; ".join(str(r["rang"]) for r in Z) + ".",
         "toleranz": "Fehlender absoluter Bezug bei richtigem Ergebnis: 2 Punkte "
                     "Abzug. Absteigende Rangfolge (1; 3; 4; 2): 2 Punkte Abzug."},
        {"nr": "1j", "punkte": 5,
         "leistung": "Spalte Q enthält je Zeile eine kopierfähige Formel, die bei "
                     "Überschreiten des Preisschwellenwerts oder Unterschreiten der "
                     "Fristgrenze Rücksprache ausgibt.",
         "hinweis": 'Q4: =WENN(ODER(N4>168;O4<35);"Rücksprache";"freigegeben"), nach '
                    "unten kopiert. Ergebnisse: "
                    + "; ".join(r["hinweis"] for r in Z) + ".",
         "toleranz": "Schreibweise der Ausgabetexte muss übereinstimmen; Groß- und "
                     "Kleinschreibung zählt. Verknüpfung mit UND (viermal "
                     "freigegeben): 3 Punkte Abzug."},
        {"nr": "1k", "punkte": 2,
         "leistung": "Zelle B9 enthält eine Formel für den niedrigsten Bezugspreis je "
                     "Stück.",
         "hinweis": f"B9: =MIN(N4:N7). Ergebnis: {eur(MIN_JE_STUECK, nbsp=False)}.",
         "toleranz": "Eingetippter Wert statt Formel: 0 Punkte."},
        {"nr": "1l", "punkte": 6,
         "leistung": "Im Blatt Ausw steht ab A12 ein Balkendiagramm mit dem "
                     "Bezugspreis je Stück der vier Anbieter, gestaltet nach "
                     "Anlage 5.",
         "hinweis": "Datenbereich: Rubriken A4:A7, Werte N4:N7. Balkendiagramm "
                    "(liegende Balken). Diagrammtitel, Legende und beide "
                    "Achsenbeschriftungen sind gesetzt. 2 Punkte Datenbereich, "
                    "2 Punkte Diagrammtyp, 2 Punkte Beschriftungen.",
         "toleranz": "Säulendiagramm statt Balkendiagramm: 2 Punkte Abzug. Fehlende "
                     "einzelne Beschriftung: je 0,5 Punkte Abzug innerhalb der "
                     "2 Beschriftungspunkte."},
        {"nr": "1 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind im Blatt Ausw "
                     "eingehalten.",
         "hinweis": "Geprüft werden: Geldbeträge mit zwei Dezimalstellen, "
                    "Tausenderpunkt und Leerzeichen vor dem Eurozeichen (Spalten F, "
                    "H, I, K, L, M, N, B9); Rabattsatz mit einer Dezimalstelle als "
                    "Prozentwert; Menge, Bindefrist und Rangfolge ohne "
                    "Dezimalstellen; Datum als TT.MM.JJJJ; Arial 11 pt. Abzüge im "
                    "Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 0,5 Punkte Abzug, insgesamt höchstens "
                     "2 Punkte."},

        {"nr": "2a", "punkte": 3,
         "leistung": "Die Überschrift der ersten Zeile ist in Arial 14 pt, fett und "
                     "zentriert formatiert; der Abstand nach dem Absatz beträgt "
                     "12 pt.",
         "hinweis": "1 Punkt Schriftgrad und Fettung, 1 Punkt Zentrierung, 1 Punkt "
                    "Absatzabstand. Der Abstand wird über die Absatzformatierung "
                    "gesetzt, nicht über eine Leerzeile.",
         "toleranz": "Leerzeile statt Absatzabstand: 1 Punkt Abzug."},
        {"nr": "2b", "punkte": 4,
         "leistung": "Die drei Zwischenüberschriften sind in Arial 12 pt und fett "
                     "formatiert; der Abstand vor dem Absatz beträgt 12 pt.",
         "hinweis": "Je Zwischenüberschrift 1 Punkt, 1 Punkt für den einheitlich "
                    "gesetzten Abstand vor dem Absatz. Zwischenüberschriften: "
                    "Ausgangslage, Angebotsübersicht, Prüfschritte.",
         "toleranz": "Umsetzung über eine selbst angelegte Formatvorlage zählt voll."},
        {"nr": "2c", "punkte": 3,
         "leistung": "Die vier Absätze des Abschnitts Ausgangslage sind im Blocksatz "
                     "ausgerichtet.",
         "hinweis": "Je Absatz 0,75 Punkte. Nur die vier Absätze der Ausgangslage, "
                    "nicht das ganze Dokument.",
         "toleranz": "Blocksatz zusätzlich in weiteren Absätzen: kein Abzug, solange "
                     "die vier Absätze richtig sind."},
        {"nr": "2d", "punkte": 4,
         "leistung": "Die vier Zeilen des Abschnitts Prüfschritte sind als Aufzählung "
                     "mit hängendem Einzug von 0,5 cm formatiert.",
         "hinweis": "2 Punkte Aufzählungszeichen für alle vier Zeilen, 2 Punkte "
                    "hängender Einzug von 0,5 cm.",
         "toleranz": "Aufzählungszeichen frei wählbar. Manuell getippte Striche statt "
                     "Aufzählung: 2 Punkte Abzug."},
        {"nr": "2e", "punkte": 7,
         "leistung": "An den beiden gekennzeichneten Stellen stehen echte Fußnoten "
                     "mit den Quellenangaben aus Anlage 3; die Kennzeichnungen (1) "
                     "und (2) sind entfernt.",
         "hinweis": "Je Fußnote 3 Punkte: 1 Punkt richtige Textstelle, 1 Punkt echte "
                    "Fußnote statt Klammertext, 1 Punkt vollständiger Quellentext. "
                    "1 Punkt für das Entfernen beider Kennzeichnungen.",
         "toleranz": "Endnote statt Fußnote: 2 Punkte Abzug. Abweichende "
                     "Zeichensetzung im Quellentext: kein Abzug."},
        {"nr": "2f", "punkte": 7,
         "leistung": "Unterhalb des Absatzes im Abschnitt Angebotsübersicht steht "
                     "eine Tabelle mit vier Spalten und fünf Zeilen mit den Angaben "
                     "aus Anlage 3.",
         "hinweis": "2 Punkte Tabellenaufbau (4 Spalten, Kopfzeile plus vier "
                    "Datenzeilen), 4 Punkte richtige Inhalte (je Datenzeile 1 Punkt), "
                    "1 Punkt Position unterhalb des Absatzes.",
         "toleranz": "Abweichende Spaltenbreiten: kein Abzug. Vertauschte "
                     "Zeilenreihenfolge: 1 Punkt Abzug."},
        {"nr": "2 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind im Dokument "
                     "eingehalten.",
         "hinweis": "Geprüft werden: Arial 11 pt im Fließtext, Datumsangaben als "
                    "TT.MM.JJJJ in der Tabelle. Abzüge im Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 1 Punkt Abzug, insgesamt höchstens "
                     "2 Punkte."},

        {"nr": "3a", "punkte": 4,
         "leistung": "Anschriftfeld und Informationsblock des Briefes sind nach "
                     "DIN 5008:2020 vollständig ausgefüllt.",
         "hinweis": "2 Punkte Anschriftfeld: Vitagon Objekteinrichtung GmbH / Frau "
                    "Britta Sanwald / Neutorstraße 42 / 89073 Ulm, ohne Leerzeile vor "
                    "der Postleitzahl. 2 Punkte Informationsblock: Ihr Zeichen "
                    "VO-8823, Ihre Nachricht vom 04.08.2026, Unser Zeichen kor-ad, "
                    "Name Ruth Adam, Telefon 030 123456-112, Telefax 030 123456-100, "
                    "E-Mail ruth.adam@goldberg.test — das Datum war vorgegeben.",
         "toleranz": "Reihenfolge Firma vor Person und Person vor Firma zählen beide. "
                     "Nicht ausgefüllte Felder ohne Angabe in Anlage 4 (Unsere "
                     "Nachricht vom): kein Abzug."},
        {"nr": "3b", "punkte": 2,
         "leistung": "Die Betreffzeile nennt Angebotsnummer, Angebotsdatum und das "
                     "Anliegen.",
         "hinweis": "Beispiel: Angebot VO-8823 vom 04.08.2026 – Bitte um Verlängerung "
                    "der Bindefrist. 1 Punkt Angebotsbezug, 1 Punkt Anliegen. Ohne "
                    "das Wort Betreff, ohne Punkt am Ende.",
         "toleranz": "Jede Formulierung, die beide Bestandteile enthält."},
        {"nr": "3c", "punkte": 4,
         "leistung": "Der Einstieg nimmt Bezug auf das Angebot vom 04.08.2026 und den "
                     "Gegenstand.",
         "hinweis": "2 Punkte Bezug auf Angebot und Datum, 1 Punkt Nennung der 120 "
                    "Bürodrehstühle, 1 Punkt Anrede mit Komma und anschließend "
                    "kleingeschriebener Fortsetzung.",
         "toleranz": "Großschreibung nach der Anrede: 1 Punkt Abzug. Anrede an eine "
                     "andere Person aus Anlage 4: 2 Punkte Abzug."},
        {"nr": "3d", "punkte": 5,
         "leistung": "Der Brief nennt den 20.09.2026 als gewünschtes Ende der "
                     "Bindefrist und begründet die Bitte mit der Sitzung am "
                     "10.09.2026.",
         "hinweis": "2 Punkte Termin 20.09.2026, 2 Punkte Begründung über den "
                    "Sitzungstermin 10.09.2026, 1 Punkt Hinweis auf das Ende der "
                    "jetzigen Bindefrist am 04.09.2026.",
         "toleranz": "Begründung mit gleichem Sachgehalt in anderer Formulierung "
                     "zählt voll."},
        {"nr": "3e", "punkte": 5,
         "leistung": "Der Brief bittet um schriftliche Rückmeldung bis zum 03.09.2026 "
                     "und schließt nach DIN 5008:2020 ab.",
         "hinweis": "2 Punkte Bitte um schriftliche Rückmeldung mit Termin "
                    "03.09.2026, 1 Punkt Grußformel, 1 Punkt Firmenbezeichnung "
                    "Goldberg Designermöbel GmbH, 1 Punkt Unterschriftsraum und Name "
                    "Ruth Adam.",
         "toleranz": "Andere übliche Grußformel zählt voll. Fehlender "
                     "Unterschriftsraum bei vorhandenem Namen: 0,5 Punkte Abzug."},
        {"nr": "3 Format", "punkte": 2,
         "leistung": "Die Formatvorgaben des Aufgabenbogens sind im Brief "
                     "eingehalten.",
         "hinweis": "Geprüft werden: Arial 11 pt aus der Vorlage unverändert, "
                    "Datumsangaben als TT.MM.JJJJ, Gliederungsleerzeilen nach "
                    "DIN 5008:2020. Abzüge im Lösungshinweis begründen.",
         "toleranz": "Je Formatart höchstens 1 Punkt Abzug, insgesamt höchstens "
                     "2 Punkte."},
    ]


def _handreichung():
    return {
        "uebersicht": [
            ("Satz", SATZNAME),
            ("Zuschnitt", "Vollprüfung, 3 Aufgaben, 120 Minuten, 100 Punkte"),
            ("Punkteverteilung", "Aufgabe 1: 48 · Aufgabe 2: 30 · Aufgabe 3: 22 "
                                 "(je Aufgabe 2 Punkte für die Formatvorgaben)"),
            ("Stoffschwerpunkt", "Angebotsvergleich, Bezugspreisermittlung"),
            ("Abteilung", "Beschaffung/Einkauf"),
            ("Eingesetzte Funktionen", "SVERWEIS (Bereichssuche und exakte Suche), "
                                       "RUNDEN, TAGE360, RANG, WENN mit ODER, MIN"),
            ("Pflichtelemente", "RANG · TAGE360 · ODER · Fußnote"),
            ("Kommunikationsform", "Brief nach DIN 5008:2020"),
            ("Diagramm", "Balkendiagramm, Bezugspreis je Stück nach Anbieter"),
        ],
        "zeitraster": [
            ("Einstieg und Rückmeldung der Gruppe", 5),
            ("Aufgabe 1, Teilaufgaben a bis f (Übernahme, Rabatt, Skonto)", 18),
            ("Aufgabe 1, Teilaufgaben g bis l (Bezugspreis, Frist, Rang, Diagramm)",
             17),
            ("Aufgabe 2 (Bericht, Fußnoten, Tabelle)", 10),
            ("Aufgabe 3 (Brief nach DIN 5008:2020)", 8),
            ("Puffer und offene Fragen", 2),
        ],
        "stolperstellen": [
            ("1a", "Datum und Geldbeträge werden als Text eingetippt (führendes "
                   "Apostroph, Punkt statt Komma). Die Folgerechnungen liefern dann "
                   "Fehlerwerte."),
            ("1c", "Die Matrix im Blatt Kond wird nicht absolut gesetzt; beim "
                   "Kopieren nach unten wandert der Bereich mit. Zweite "
                   "Stolperstelle: exakte Suche statt Bereichssuche, weil die Staffel "
                   "nach Wertgrenzen aufgebaut ist."),
            ("1e", "Das Skonto wird auf den vollen Warenwert bezogen statt auf den "
                   "Warenwert nach Rabattabzug. Oder die Frachtpauschale wird in die "
                   "Skontobasis genommen."),
            ("1g", "Es wird nur das Zellformat auf zwei Dezimalstellen gestellt, "
                   "statt zu runden. Sichtbar wird das in Zeile 5: der ungerundete "
                   "Wert lautet 161,2757…"),
            ("1h", "Die Bindefrist wird als einfache Datumsdifferenz gerechnet. "
                   "Ergebnisse weichen dann um ein bis zwei Tage ab."),
            ("1i", "Der Bezugsbereich der Rangfolge ist nicht absolut gesetzt, oder "
                   "es wird absteigend statt aufsteigend gerangt."),
            ("1j", "Die beiden Bedingungen werden mit UND verknüpft. Dann steht "
                   "viermal freigegeben in der Spalte – ein gut sichtbarer "
                   "Prüfpunkt."),
            ("1l", "Der Datenbereich wird über die ganze Tabelle gezogen statt über "
                   "die Rubriken A4:A7 und die Werte N4:N7. Oder es entsteht ein "
                   "Säulen- statt Balkendiagramm."),
            ("2a", "Der Abstand nach dem Absatz wird über eine Leerzeile erzeugt "
                   "statt über die Absatzformatierung."),
            ("2d", "Die Aufzählung wird mit getippten Strichen nachgebaut; der "
                   "hängende Einzug fehlt oder wird über Tabulatoren erzeugt."),
            ("2e", "Statt einer echten Fußnote wird der Quellentext in Klammern in "
                   "den Fließtext geschrieben, oder es wird eine Endnote gesetzt."),
            ("3a", "Im Anschriftfeld bleibt die alte Leerzeile vor der Postleitzahl "
                   "stehen – nach DIN 5008:2020 entfällt sie."),
            ("3c", "Nach der Anrede wird großgeschrieben weitergeschrieben. Richtig "
                   "ist: Sehr geehrte Frau Sanwald, / vielen Dank …"),
        ],
        "falschloesungen": [
            ["Skonto auf den vollen Warenwert", "1e",
             "3 Punkte Abzug, Folgewerte in M und N gelten als Folgefehler."],
            ["Nur Zellformat statt Rundungsfunktion", "1g",
             "2 Punkte Abzug; das Ergebnis in Zeile 5 weicht sichtbar ab."],
            ["Einfache Datumsdifferenz", "1h", "3 Punkte Abzug."],
            ["UND statt ODER", "1j",
             "3 Punkte Abzug; erkennbar an viermal freigegeben."],
            ["Fehlender absoluter Bezug", "1c, 1e, 1i",
             "je 2 Punkte Abzug, weil die Formel nicht kopierfähig ist."],
            ["Quellentext in Klammern statt Fußnote", "2e",
             "je Stelle 1 Punkt Abzug für die fehlende Fußnote."],
            ["Großschreibung nach der Anrede", "3c", "1 Punkt Abzug."],
        ],
        "fachklaerung": [
            ("Bezugspreis", "Warenwert abzüglich Rabatt und Skonto, zuzüglich der "
                            "Bezugskosten. Die Frachtpauschale ist hier weder rabatt- "
                            "noch skontofähig und kommt deshalb ungekürzt hinzu."),
            ("Rabattstaffel", "Der Rabattsatz hängt am Warenwert des Auftrags, nicht "
                              "an der Menge. Weil die Staffel Wertgrenzen nennt, ist "
                              "die Bereichssuche der richtige Weg: gesucht wird der "
                              "größte Staffelwert, der den Warenwert nicht "
                              "übersteigt."),
            ("Skonto", "Skonto ist ein Abzug für schnelle Zahlung. Bemessen wird es "
                       "hier am Warenwert nach Rabattabzug; die anbieterbezogenen "
                       "Sätze stehen im Lieferantenstamm."),
            ("Bindefrist", "Zeitraum, in dem der Anbieter an sein Angebot gebunden "
                           "ist. Gerechnet wird mit 30 Tagen je Monat. Bei den Daten "
                           "dieses Satzes liefern beide Zählmethoden dasselbe "
                           "Ergebnis."),
            ("Rangfolge", "Aufsteigende Rangfolge: der niedrigste Bezugspreis je "
                          "Stück erhält den Rang 1. Der Bezugsbereich muss absolut "
                          "gesetzt sein, sonst verschiebt er sich beim Kopieren."),
        ],
        "anschlussuebungen": [
            ("Bereichssuche üben", "Eine zweite Staffel mit fünf Wertgrenzen vorgeben "
                                   "und drei Beträge zuordnen lassen – einer davon "
                                   "genau auf einer Grenze."),
            ("Runden gegen Formatieren", "Dieselbe Spalte einmal nur formatiert und "
                                         "einmal gerundet berechnen lassen, danach "
                                         "beide Summen vergleichen."),
            ("UND gegen ODER", "Eine kurze Tabelle mit vier Datensätzen vorgeben, in "
                               "der genau ein Datensatz beide Bedingungen erfüllt. "
                               "Beide Verknüpfungen rechnen lassen."),
        ],
        "dateihinweise": [
            "Die Lösungsdatei zu Aufgabe 1 enthält echte Formeln. Öffnen Sie sie "
            "einmal in Excel, damit alle Werte neu berechnet werden. Die Datei "
            "enthält neben dem Auswertungsblatt und den Stammdatenblättern weitere "
            "Blätter mit Daten aus dem Modellunternehmen; sie werden nicht gebraucht, "
            "sind aber Teil der Arbeitsumgebung und bleiben erhalten.",
            "Die Lösungsdatei zu Aufgabe 2 enthält zwei echte Fußnoten. Der "
            "Kurzbericht in der Teilnehmerdatei ist bewusst unformatiert; die "
            "Formatierung ist die Prüfungsleistung.",
            "Die Lösungsdatei zu Aufgabe 3 ist die ausgefüllte Goldberg-Briefvorlage. "
            "Das Datum ist in beiden Fassungen vorbereitet und wird nicht bewertet.",
        ],
    }
