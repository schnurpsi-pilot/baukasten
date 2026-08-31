# -*- coding: utf-8 -*-
"""Wiederkehrende Textbausteine für alle Sätze der Reihe.

Die Allgemeinen Hinweise standen bisher in jeder Satzdatei einzeln und wurden
beim Anlegen eines neuen Satzes vom Vorgänger abgeschrieben. Eine Änderung
musste deshalb an jeder Stelle einzeln nachgezogen werden. Hier stehen sie
einmal; die Satzdateien holen sie sich von hier.

Der Absatz zur Umsatzsteuer ist nach §5.2 wörtlich vorgeschrieben und darf
nicht umformuliert werden.
"""

# Domain des Modellunternehmens. .test ist nach RFC 2606 für Testzwecke
# reserviert und kann niemandem gehören — eine erfundene .com-Adresse
# dagegen schon. Deshalb steht sie hier zentral und wird nicht je Satz
# neu getippt.
DOMAIN = "goldberg.test"


def mail(name):
    """Baut eine E-Mail-Adresse des Modellunternehmens.

    mail("ines.kortmann") ergibt "ines.kortmann@goldberg.test".
    """
    return f"{name}@{DOMAIN}"


# Platzhalter {beispieldatei} wird je Satz gefüllt, weil die Endung von der
# ersten Aufgabe abhängt. Die Zahl der Anlagen wird bewusst nicht genannt:
# sie ändert sich je Satz, ließe sich nicht gegen die Anlagenliste prüfen und
# brächte den Teilnehmenden keinen Nutzen — welche Anlage gebraucht wird,
# steht ohnehin an jeder Aufgabe.
HINWEISE_STANDARD = [
    ("Ablage der Dateien",
     "Wenn Sie nicht schon einen Ordner mit dem Namen AP1 angelegt haben, "
     "machen Sie es bitte jetzt. Kopieren Sie die ZIP-Datei in diesen Ordner "
     "und entpacken Sie sie dort. Bearbeiten Sie die Aufgaben ausschließlich "
     "in den entpackten Dateien und speichern Sie diese im selben Ordner."),
    ("Dateibenennung",
     "Speichern Sie jede bearbeitete Datei unter Ihrer Teilnehmernummer und "
     "der Aufgabennummer. Die Teilnehmernummer besteht aus Ihrem Nachnamen "
     "und dem heutigen Tagesdatum im Format TTMM, also Tag und Monat je "
     "zweistellig. Beispiel: {beispieldatei}."),
    ("Anlagen",
     "Die Anlagen stehen im Materialheft. Jede Aufgabe nennt die Anlagen, die "
     "dafür gebraucht werden. Die Anlagen werden nicht bearbeitet."),
    ("Punkte",
     "Die Punktzahl steht hinter jeder Teilaufgabe. In jeder Aufgabe "
     "entfallen zusätzlich 2 Punkte auf die Einhaltung der Formatvorgaben. "
     "Verwenden Sie kopierfähige Formeln mit Zellbezügen, wo mehrere Zeilen "
     "gleichartig berechnet werden."),
    ("Umsatzsteuer",
     "Alle Beträge in den Anlagen und Dateien sind Nettobeträge; der "
     "Umsatzsteuersatz beträgt 19 Prozent."),
]


def hinweise(beispieldatei="Weber1708_A1.xlsx"):
    """Liefert die Allgemeinen Hinweise mit gefülltem Platzhalter.

    beispieldatei: Beispiel für die Dateibenennung, passend zur ersten
    Aufgabe des Satzes.
    """
    return [(titel, text.format(beispieldatei=beispieldatei))
            for titel, text in HINWEISE_STANDARD]
