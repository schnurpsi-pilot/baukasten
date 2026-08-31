# -*- coding: utf-8 -*-
"""Layoutrechnung: Schriftbreiten, Spaltenbreiten, Umbruch der Punktangabe.

Grundlage ist Liberation Sans, das metrisch mit Arial übereinstimmt. Damit
lässt sich vor dem Schreiben ausrechnen, ob ein Wort in eine Spalte passt
und ob die Punktangabe noch in die letzte Textzeile passt (§18.3, §18.4).
"""
from PIL import ImageFont

_PFAD_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
_PFAD_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_EM = 220.0

try:
    _FONT = ImageFont.truetype(_PFAD_REG, int(_EM))
    _FONT_B = ImageFont.truetype(_PFAD_BOLD, int(_EM))
    METRIK_VERFUEGBAR = True
except OSError:                                     # pragma: no cover
    _FONT = _FONT_B = None
    METRIK_VERFUEGBAR = False


def breite_cm(text, pt=11, fett=False):
    """Breite eines Textes in cm bei Arial/Liberation Sans in Größe pt."""
    if not METRIK_VERFUEGBAR:
        return len(text) * pt * 0.0175          # grobe Näherung ohne Font
    px = (_FONT_B if fett else _FONT).getlength(text)
    return px / _EM * pt / 72 * 2.54


def auto_breiten(kopf, zeilen, gesamt_cm=16.0, pt=9, rand_cm=0.55, min_cm=1.2):
    """Spaltenbreiten, bei denen kein Wort mitten getrennt wird (§18.3).

    Misst je Spalte das breiteste unteilbare Wort — Kopfzeilen fett, Daten
    normal — und verteilt den Rest nach dem Platzbedarf der Spalten. Passt
    die Summe nicht in gesamt_cm, wird proportional verkleinert und die
    Schriftgröße mit reduziert.

    Rückgabe: (liste_breiten_cm, schriftgroesse_pt)
    """
    n = len(kopf)
    mind = []
    for i in range(n):
        kandidaten = [breite_cm(w, pt, fett=True)
                      for w in str(kopf[i]).replace("-", "- ").split()]
        for z in zeilen:
            kandidaten += [breite_cm(w, pt) for w in str(z[i]).split()]
        mind.append(max(min_cm, max(kandidaten, default=0) * 1.06 + rand_cm))

    summe = sum(mind)
    if summe > gesamt_cm:
        faktor = gesamt_cm / summe
        return [b * faktor for b in mind], max(7, int(pt * faktor))

    rest = gesamt_cm - summe
    ideal = []
    for i in range(n):
        texte = [str(kopf[i])] + [str(z[i]) for z in zeilen]
        ideal.append(max(breite_cm(t, pt) for t in texte))
    gewicht = sum(ideal) or 1
    return [mind[i] + rest * ideal[i] / gewicht for i in range(n)], pt


def punkte_umbrechen(text, punktetext, textbreite_cm=15.2, tabbreite_cm=15.0,
                     abstand_cm=0.4, pt=11):
    """True, wenn die Punktangabe nicht mehr in die letzte Textzeile passt.

    Verhindert, dass die Punktzahl am Text klebt oder in die Folgezeile
    rutscht (§18.3). Der Aufrufer setzt dann vor dem Tabulator einen
    Zeilenumbruch innerhalb desselben Absatzes — Auftragstext und
    Punktangabe bleiben damit zusammen (§18.4).
    """
    zeile = ""
    for wort in text.replace("@@", "").split(" "):
        probe = (zeile + " " + wort).strip()
        if breite_cm(probe, pt) * 1.03 > textbreite_cm and zeile:
            zeile = wort
        else:
            zeile = probe
    letzte = breite_cm(zeile, pt) * 1.03
    return letzte + breite_cm(punktetext, pt) + abstand_cm > tabbreite_cm


def eur(x, nbsp=True):
    """Geldbetrag nach §5.7: zwei Dezimalstellen, Tausenderpunkt, Leerzeichen
    vor dem Eurozeichen. Das Leerzeichen ist geschützt, damit der Betrag in
    Tabellenzellen nicht umbricht."""
    s = f"{float(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s + ("\u00a0€" if nbsp else " €")


def datum(d):
    """Datum nach §5.7 als TT.MM.JJJJ."""
    return d.strftime("%d.%m.%Y")

# Weicher Trennstrich: Überschriften wie "Personal~nummer" erscheinen in
# breiten Spalten als ein Wort und brechen in schmalen mit Trennstrich um.
# Ein gewöhnlicher Bindestrich wäre dauerhaft sichtbar und damit in
# "Personal-nummer" schlicht falsch geschrieben.
WEICH = "\u00ad"


def trennbar(text):
    """Wandelt ~ in einen bedingten Trennstrich."""
    return str(text).replace("~", WEICH) if text is not None else text
