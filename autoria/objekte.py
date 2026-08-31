# -*- coding: utf-8 -*-
"""Textverarbeitungsobjekte jenseits des Fließtexts (Anhang D.2).

Hier liegen die Bausteine, die python-docx nicht von sich aus kann:

* Dokumentvorlage `.dotx` — eine Vorlage unterscheidet sich von einem
  Dokument nur im Content-Type und in der Endung, nicht im Inhalt. Word
  legt beim Öffnen einer Vorlage eine Kopie an, statt die Vorlage selbst
  zu ändern; genau das ist die Prüfungsleistung beim Laufzettel.
* WordArt — ein Schrifteffekt, den python-docx nicht kennt. Er wird als
  VML-Textpfad in den Absatz gehängt, weil Word und LibreOffice diese
  ältere Form beide lesen; die moderne DrawingML-Variante rendert
  LibreOffice unzuverlässig.

Beides ist bewusst schlicht gehalten: Der Prüfungssatz stellt die Objekte
bereit, gestaltet werden sie von den Teilnehmenden.
"""
import os
import shutil
import zipfile

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Content-Types: Dokument gegen Vorlage. Der einzige technische Unterschied.
CT_DOKUMENT = ("application/vnd.openxmlformats-officedocument."
               "wordprocessingml.document.main+xml")
CT_VORLAGE = ("application/vnd.openxmlformats-officedocument."
              "wordprocessingml.template.main+xml")


# ------------------------------------------------------- Dokumentvorlage
def als_dotx(docx_pfad, dotx_pfad):
    """Schreibt ein fertiges .docx als Dokumentvorlage .dotx.

    Der Inhalt bleibt unverändert; getauscht wird allein der Content-Type
    des Hauptdokuments. Ohne diesen Tausch behandelt Word die Datei trotz
    der Endung als gewöhnliches Dokument und legt beim Öffnen keine Kopie
    an — die Vorlageneigenschaft wäre dann nur behauptet, nicht vorhanden.
    """
    tmp = dotx_pfad + ".auspack"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    with zipfile.ZipFile(docx_pfad) as z:
        z.extractall(tmp)

    ct_pfad = os.path.join(tmp, "[Content_Types].xml")
    with open(ct_pfad, encoding="utf-8") as f:
        ct = f.read()
    if CT_DOKUMENT not in ct:
        raise ValueError("Kein Word-Hauptdokument gefunden — "
                         f"{os.path.basename(docx_pfad)} ist keine .docx.")
    with open(ct_pfad, "w", encoding="utf-8") as f:
        f.write(ct.replace(CT_DOKUMENT, CT_VORLAGE))

    if os.path.exists(dotx_pfad):
        os.remove(dotx_pfad)
    with zipfile.ZipFile(dotx_pfad, "w", zipfile.ZIP_DEFLATED) as z:
        for wurzel, _d, dateien in os.walk(tmp):
            for name in dateien:
                voll = os.path.join(wurzel, name)
                z.write(voll, os.path.relpath(voll, tmp))
    shutil.rmtree(tmp, ignore_errors=True)
    return dotx_pfad


def ist_vorlage(pfad):
    """Prüft, ob eine Datei tatsächlich als Dokumentvorlage angelegt ist."""
    with zipfile.ZipFile(pfad) as z:
        return CT_VORLAGE in z.read("[Content_Types].xml").decode("utf-8")


# --------------------------------------------------------------- WordArt
# Die Form wird als VML gebaut. Word 2010 und neuer liest sie, LibreOffice
# ebenfalls; die DrawingML-Variante rendert LibreOffice dagegen teils ohne
# Text, was in einer Prüfung nicht auffallen darf.
_VML = (
    '<w:pict xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:v="urn:schemas-microsoft-com:vml" '
    'xmlns:o="urn:schemas-microsoft-com:office:office">'
    '<v:shapetype id="_x0000_t136" coordsize="21600,21600" o:spt="136" '
    'adj="10800" path="m@7,l@8,m@5,21600l@6,21600e">'
    '<v:formulas><v:f eqn="sum #0 0 10800"/><v:f eqn="prod #0 2 1"/>'
    '<v:f eqn="sum 21600 0 @1"/><v:f eqn="sum 0 0 @2"/>'
    '<v:f eqn="sum 21600 0 @3"/><v:f eqn="if @0 @3 0"/>'
    '<v:f eqn="if @0 21600 @1"/><v:f eqn="if @0 0 @2"/>'
    '<v:f eqn="if @0 @4 21600"/></v:formulas>'
    '<v:path textpathok="t" o:connecttype="custom"/>'
    '<v:textpath on="t" fitshape="t"/></v:shapetype>'
    '<v:shape id="{kennung}" type="#_x0000_t136" '
    'style="{lage}width:{breite}pt;height:{hoehe}pt" '
    'fillcolor="{fuellung}" stroked="f">'
    '<v:textpath style="font-family:&quot;{schrift}&quot;;font-size:{groesse}pt;'
    'font-weight:bold" string="{text}"/></v:shape></w:pict>'
)


def wordart(absatz, text, breite_pt=340, hoehe_pt=42, schrift="Arial",
            groesse_pt=36, fuellung="#404040", kennung="WordArt1",
            fliessend=True):
    """Hängt einen WordArt-Schriftzug in einen vorhandenen Absatz (D.2).

    Standardmäßig steht der Schriftzug fließend in der Zeile; mit
    `fliessend=False` wird er absolut positioniert und überlagert den
    folgenden Text.

    Der Effekt ist bewusst schlicht: eine Graustufenfüllung ohne Kontur,
    passend zum Schwarz-Weiß-Druck der Prüfungsunterlagen (§8). Sollen die
    Teilnehmenden den Effekt selbst setzen, wird hier nichts eingefügt —
    dann ist WordArt Prüfungsleistung und gehört nicht in die Vorlage.
    """
    sicher = (str(text).replace("&", "&amp;").replace("<", "&lt;")
              .replace(">", "&gt;").replace('"', "&quot;"))
    # Fließend heißt: der Schriftzug steht in der Zeile und schiebt den
    # folgenden Text nach unten. Absolut positioniert läge er darüber und
    # verdeckte ihn — in einem Laufzettelkopf ein sichtbarer Fehler.
    lage = "" if fliessend else ("position:absolute;margin-left:0;"
                                 "margin-top:0;z-index:1;")
    xml = _VML.format(kennung=kennung, breite=breite_pt, hoehe=hoehe_pt,
                      schrift=schrift, groesse=groesse_pt,
                      fuellung=fuellung, text=sicher, lage=lage)
    lauf = absatz.add_run()
    lauf._r.append(OxmlElement("w:rPr"))
    from docx.oxml import parse_xml
    lauf._r.append(parse_xml(xml))
    return absatz


def hat_wordart(dokument):
    """True, wenn im Dokument mindestens ein WordArt-Textpfad steckt."""
    xml = dokument.element.xml
    return "v:textpath" in xml and 'string="' in xml


# --------------------------------------------------- Inhaltssteuerelemente
# Word nennt sie Inhaltssteuerelemente, im XML heißen sie "structured
# document tag" (sdt). python-docx kennt sie nicht, deshalb werden sie hier
# von Hand gesetzt. Aufbau: sdt > sdtPr (was für ein Feld) + sdtContent
# (was angezeigt wird, solange nichts eingetragen ist).
#
# Anhang D.2 kennt vier Arten. Ihre Namen gehören in den Aufgabenbogen,
# nicht in die Anlage (§11.4) — die Anlage nennt nur die Art der Eingabe.
def _sdt(art, platzhalter, eigenschaften=None, tag=None):
    sdt = OxmlElement("w:sdt")
    pr = OxmlElement("w:sdtPr")

    if tag:
        t = OxmlElement("w:tag")
        t.set(qn("w:val"), tag)
        pr.append(t)
    alias = OxmlElement("w:alias")
    alias.set(qn("w:val"), tag or art)
    pr.append(alias)

    # Der Platzhaltertext verschwindet, sobald die Zelle beschrieben wird.
    ph = OxmlElement("w:showingPlcHdr")
    pr.append(ph)

    pr.append(eigenschaften if eigenschaften is not None
              else OxmlElement(f"w:{art}"))
    sdt.append(pr)

    inhalt = OxmlElement("w:sdtContent")
    lauf = OxmlElement("w:r")
    text = OxmlElement("w:t")
    text.text = platzhalter
    lauf.append(text)
    inhalt.append(lauf)
    sdt.append(inhalt)
    return sdt


def textfeld(absatz, platzhalter="Klicken Sie hier, um Text einzugeben.",
             tag=None, mehrzeilig=False):
    """Freies Texteingabefeld (Anhang D.2)."""
    eig = OxmlElement("w:text")
    if mehrzeilig:
        eig.set(qn("w:multiLine"), "1")
    absatz._p.append(_sdt("text", platzhalter, eig, tag))
    return absatz


def datumsfeld(absatz, platzhalter="TT.MM.JJJJ", tag=None,
               format_="dd.MM.yyyy"):
    """Datumsauswahl mit festem Anzeigeformat (Anhang D.2)."""
    eig = OxmlElement("w:date")
    fmt = OxmlElement("w:dateFormat")
    fmt.set(qn("w:val"), format_)
    eig.append(fmt)
    kal = OxmlElement("w:calendar")
    kal.set(qn("w:val"), "gregorian")
    eig.append(kal)
    absatz._p.append(_sdt("date", platzhalter, eig, tag))
    return absatz


def auswahlfeld(absatz, eintraege, platzhalter="Bitte auswählen", tag=None,
                frei=False):
    """Auswahlliste. frei=True lässt zusätzlich eigene Eingaben zu (D.2)."""
    eig = OxmlElement("w:comboBox" if frei else "w:dropDownList")
    for e in eintraege:
        item = OxmlElement("w:listItem")
        item.set(qn("w:displayText"), str(e))
        item.set(qn("w:value"), str(e))
        eig.append(item)
    absatz._p.append(_sdt("dropDownList", platzhalter, eig, tag))
    return absatz


def kontrollkaestchen(absatz, tag=None):
    """Ankreuzfeld (Anhang D.2)."""
    eig = OxmlElement("w14:checkbox")
    for name, wert in (("w14:checked", "0"),
                       ("w14:checkedState", "2612"),
                       ("w14:uncheckedState", "2610")):
        kind = OxmlElement(name)
        if name == "w14:checked":
            kind.set(qn("w14:val"), wert)
        else:
            kind.set(qn("w14:val"), wert)
            kind.set(qn("w14:font"), "MS Gothic")
        eig.append(kind)
    absatz._p.append(_sdt("checkbox", "\u2610", eig, tag))
    return absatz


def formularfelder_zaehlen(dokument):
    """Zählt die Inhaltssteuerelemente je Art.

    Wird von der Checkliste gebraucht: ein Pflichtelement gilt nur als
    belegt, wenn es im Artefakt auch wirklich steckt (§10.3).
    """
    ARTEN = {"text": "Textfeld", "date": "Datumsfeld",
             "dropDownList": "Auswahlfeld", "comboBox": "Auswahlfeld",
             "checkbox": "Kontrollkästchen"}
    gefunden = {}
    for sdtPr in dokument.element.body.iter(qn("w:sdtPr")):
        for kind in sdtPr:
            name = kind.tag.split("}")[-1]
            if name in ARTEN:
                gefunden[ARTEN[name]] = gefunden.get(ARTEN[name], 0) + 1
    return gefunden
