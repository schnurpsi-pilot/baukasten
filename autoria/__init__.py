# -*- coding: utf-8 -*-
"""AUTORIA-Baukasten für AP1-Prüfungssimulationen (Kaufleute für Büromanagement).

Setzt den Masterprompt AP1 v4.6 maschinell um: aus einer Satzspezifikation
entstehen alle Artefakte nach §11.2, die Checkliste nach §14.1 läuft
automatisch, das Ergebnis ist ein ZIP nach §18.7.
"""
from . import layout, docxbau, xlsxbau, dokumente, pruefung, lauf, muster

__all__ = ["layout", "docxbau", "xlsxbau", "dokumente", "pruefung", "lauf", "muster"]
__version__ = "1.0"
