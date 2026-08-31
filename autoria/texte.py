# -*- coding: utf-8 -*-
"""Wiederkehrende Textbausteine für alle Sätze der Reihe.

Die Allgemeinen Hinweise standen bisher in jeder Satzdatei einzeln und wurden
beim Anlegen eines neuen Satzes vom Vorgänger abgeschrieben. Eine Änderung
musste deshalb an jeder Stelle einzeln nachgezogen werden. Hier stehen sie
einmal; die Satzdateien holen sie sich von hier.

Der Absatz zur Umsatzsteuer ist nach §5.2 wörtlich vorgeschrieben und darf
nicht umformuliert werden.
"""

# Platzhalter {beispieldatei} wird je Satz gefüllt, weil die Endung von der
# ersten Aufgabe abhängt.
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
     "Die Anlagen 1 bis {anlagenzahl} stehen im Materialheft. Jede Aufgabe "
     "nennt die Anlagen, die dafür gebraucht werden. Die Anlagen werden nicht "
     "bearbeitet."),
    ("Punkte",
     "Die Punktzahl steht hinter jeder Teilaufgabe. In jeder Aufgabe "
     "entfallen zusätzlich 2 Punkte auf die Einhaltung der Formatvorgaben. "
     "Verwenden Sie kopierfähige Formeln mit Zellbezügen, wo mehrere Zeilen "
     "gleichartig berechnet werden."),
    ("Umsatzsteuer",
     "Alle Beträge in den Anlagen und Dateien sind Nettobeträge; der "
     "Umsatzsteuersatz beträgt 19 Prozent."),
]


def hinweise(beispieldatei="Weber1708_A1.xlsx", anlagenzahl=5):
    """Liefert die Allgemeinen Hinweise mit gefüllten Platzhaltern.

    beispieldatei: Beispiel für die Dateibenennung, passend zur ersten
    Aufgabe des Satzes. anlagenzahl: Zahl der Anlagen im Materialheft.
    """
    return [(titel, text.format(beispieldatei=beispieldatei,
                                anlagenzahl=anlagenzahl))
            for titel, text in HINWEISE_STANDARD]
