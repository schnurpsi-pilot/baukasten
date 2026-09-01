# -*- coding: utf-8 -*-
"""Reihenwissen: Sperrlisten (§10.1, §10.2) und Pflichtbelegung (§10.3).

Der Baukasten kennt bis hierher nur den einzelnen Satz. Sperren und
Pflichtbelegung sind aber Eigenschaften der ganzen Reihe: Sie ergeben sich
aus dem Reihenplan und aus allen bisher gelieferten Sätzen der Historie.

Dieses Modul liest den Plan, prüft den neuen Satz gegen die Vorgänger und
liefert die Felder, die nach §11.7 in die Historie gehören.

Ohne Reihenplan bleibt alles arbeitsfähig — die betroffenen Prüfungen
melden sich dann als ungeprüft (§14.2: fehlende Prüfmöglichkeit ist kein
Bestehen).
"""
import json
import os
import re
import unicodedata

# Stufen nach Anhang E.4. Kernfunktionen dürfen in nahezu jedem Satz
# vorkommen, für häufige gilt die Quote als Obergrenze (§10.2).
STUFE_KERN = {"SVERWEIS", "WENN"}
STUFE_HAEUFIG = {"SUMME", "SUMMEWENN", "ZÄHLENWENN"}
# Obergrenze als Anteil der Sätze, oberer Rand der Spanne aus Anhang E.4.
QUOTE_HAEUFIG = 0.72


# --------------------------------------------------------------- Hilfsmittel
UMLAUTE = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}


def _normal(text):
    """Vergleichsform: Kleinschreibung, Umlaute ausgeschrieben, ohne Sonderzeichen.

    Sperren dürfen nicht daran scheitern, dass ein Szenario einmal mit und
    einmal ohne Bindestrich geschrieben wurde. Umlaute werden nach deutscher
    Konvention ersetzt (ü zu ue), nicht auf den Grundbuchstaben verkürzt —
    sonst gälten „Bürodrehstühle" und „Buerodrehstuehle" als verschieden.
    """
    if not text:
        return ""
    text = str(text).lower()
    for um, ersatz in UMLAUTE.items():
        text = text.replace(um, ersatz)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _soll_kommunikationsform(plan, form):
    """Sollzahl einer Kommunikationsform aus dem Reihenplan.

    Der Plan führt sie als Fließtext, etwa „Brief 5×, E-Mail 5×". Fehlt der
    Plan oder die Form, gibt es keine Obergrenze zu prüfen.
    """
    if not plan or not form:
        return None
    text = (plan.get("verteilung_uebrige_achsen") or {}).get("Kommunikationsform")
    if not text:
        return None
    gesucht = _normal(form)
    for teil in str(text).split(","):
        treffer = re.match(r"\s*(.+?)\s*(\d+)\s*[×x]\s*$", teil)
        if treffer and _normal(treffer.group(1)) == gesucht:
            return int(treffer.group(2))
    return None


def _funktionsname(eintrag):
    """"SVERWEIS (WAHR)" wird zu "SVERWEIS" — die Sperre gilt der Funktion."""
    return re.split(r"[ (]", str(eintrag).strip())[0].upper()


def plan_laden(pfad):
    """Reihenplan einlesen. Rückgabe None, wenn keiner übergeben wurde."""
    if not pfad or not os.path.exists(pfad):
        return None
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


def _vorgaenger(historie, eintrag):
    """Alle gelieferten Sätze der Reihe außer dem, der gerade entsteht.

    Ein Satz, der unter altem Namen schon in der Historie steht, ist kein
    Vorgänger seiner selbst — sonst meldete jede Umbenennung eine Kollision
    mit dem eigenen Szenario. Ausgeschlossen wird deshalb sowohl der neue
    Satzname als auch der in `vorgaenger_satzname` genannte alte.
    """
    if not historie:
        return []
    if isinstance(eintrag, str):
        eintrag = {"satzname": eintrag}
    eigen = {eintrag.get("satzname"), eintrag.get("vorgaenger_satzname")}
    for s in historie.get("saetze", []):
        if s.get("satzname") == eintrag.get("satzname"):
            eigen.add(s.get("vorgaenger_satzname"))
    eigen.discard(None)
    return [s for s in historie.get("saetze", [])
            if s.get("satzname") not in eigen
            and s.get("status", "geliefert") == "geliefert"]


# ------------------------------------------------------------- Harte Sperren
def harte_sperren(eintrag, historie):
    """§10.1: Szenario, Diagrammgestaltung und TV-Objekt dürfen sich nicht
    innerhalb der Reihe wiederholen.

    Rückgabe: (verstoesse, geprueft_gegen) — Liste von Klartextmeldungen und
    Zahl der verglichenen Sätze.
    """
    frueher = _vorgaenger(historie, eintrag)
    felder = [("szenario", "Szenario und Rahmenhandlung"),
              ("diagramm", "Diagrammgestaltung"),
              ("tv_objekt", "Kombination aus Textverarbeitungsobjekt und Auftrag")]
    verstoesse = []
    for feld, klartext in felder:
        neu = _normal(eintrag.get(feld))
        if not neu:
            continue
        for alt in frueher:
            if _normal(alt.get(feld)) == neu:
                verstoesse.append(
                    f"{klartext} wiederholt sich: bereits belegt in "
                    f"{alt.get('satzname')} (§10.1). Neu planen.")
                break
    return verstoesse, len(frueher)


# ------------------------------------------------------------ Weiche Sperren
def weiche_sperren(eintrag, historie, plan=None):
    """§10.2: Häufigkeitsobergrenzen statt Verbot.

    Geprüft werden die Kommunikationsform und die häufigen Funktionen nach
    Anhang E.4. Kernfunktionen bleiben frei; alles mit einem Sollwert in
    §10.3 richtet sich allein nach diesem Sollwert (§10.2 letzter Punkt).
    """
    frueher = _vorgaenger(historie, eintrag)
    gesamt = len(frueher) + 1
    hinweise = []

    kf = _normal(eintrag.get("kommunikationsform"))
    if kf:
        zahl = sum(1 for s in frueher
                   if _normal(s.get("kommunikationsform")) == kf) + 1
        soll = _soll_kommunikationsform(plan, eintrag.get("kommunikationsform"))
        if soll and zahl > soll:
            hinweise.append(
                f"Kommunikationsform {eintrag.get('kommunikationsform')} zum "
                f"{zahl}. Mal, der Plan sieht {soll} Sätze vor (§10.2).")

    pflicht = {_funktionsname(p) for p in eintrag.get("pflichtelemente_belegt", [])}
    for fn in sorted({_funktionsname(f)
                      for f in eintrag.get("eingesetzte_funktionen", [])}):
        if fn in STUFE_KERN or fn in pflicht or fn not in STUFE_HAEUFIG:
            continue
        zahl = sum(1 for s in frueher
                   if fn in {_funktionsname(f)
                             for f in s.get("eingesetzte_funktionen", [])}) + 1
        if zahl / gesamt > QUOTE_HAEUFIG:
            hinweise.append(
                f"{fn} in {zahl} von {gesamt} Sätzen — über der Obergrenze von "
                f"{int(QUOTE_HAEUFIG * 100)} % nach Anhang E.4 (§10.2).")
    return hinweise


# --------------------------------------------------------- Pflichtbelegung
def pflichtbelegung(plan, historie, eintrag):
    """§10.3: welche Pflichtelemente nach diesem Satz noch offen sind.

    Sollwerte kommen aus dem Reihenplan. Belegt ist, was in der Historie
    bepunktet abgefragt wurde — der aktuelle Satz zählt mit.
    """
    if not plan:
        return None
    bilanz = plan.get("pflichtelement_bilanz") or plan.get("pflichtbelegung_bilanz")
    if not bilanz:
        return None

    belegt = {}
    for satz in _vorgaenger(historie, eintrag) + [eintrag]:
        for pe in satz.get("pflichtelemente_belegt", []):
            belegt[_normal(pe)] = belegt.get(_normal(pe), 0) + 1

    offen = []
    for zeile in bilanz:
        name = zeile.get("pflichtelement")
        # Der Feldname trägt die Bezugsgröße der Reihe und hat sich schon
        # zweimal geändert (32, 26, 29 Vollprüfungen). Deshalb wird jedes
        # Feld "soll_bei_*" akzeptiert statt einer festen Liste — sonst
        # rutscht der Sollwert bei der nächsten Umbenennung stillschweigend
        # auf null, und alle Pflichtelemente gelten fälschlich als erfüllt.
        soll = zeile.get("soll", 0)
        for feld, wert in zeile.items():
            if feld.startswith("soll_bei_"):
                soll = wert
                break
        ist = belegt.get(_normal(name), 0)
        if ist < soll:
            offen.append(name)
    return sorted(offen)


# ------------------------------------------------- Fassung für die Historie
def sperrlisten_check(eintrag, historie, plan=None):
    """Baut das Feld sperrlisten_check für die Historie (§11.7)."""
    verstoesse, geprueft = harte_sperren(eintrag, historie)
    weich = weiche_sperren(eintrag, historie, plan)
    if verstoesse:
        hart = "verletzt: " + " ".join(verstoesse)
    elif geprueft:
        wort = "Vorgängersatz" if geprueft == 1 else "Vorgängersätze"
        hart = (f"bestanden (Szenario, Diagrammgestaltung und "
                f"TV-Objektkombination gegen {geprueft} {wort} geprüft)")
    else:
        hart = "bestanden (erster Satz der Reihe, keine Vorgänger zu prüfen)"
    return {"hart": hart,
            "weich": " ".join(weich) if weich
                     else "keine Obergrenze nach §10.2 überschritten"}
