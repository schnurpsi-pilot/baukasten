#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Startet einen Produktionslauf.

    python3 run.py saetze/nr01.py
    python3 run.py saetze/nr04.py --historie alt/Historie.json \
                   --reihenplan AP1-Reihenplan_Nr04-Nr29.json

Erzeugt alle Artefakte, arbeitet die Checkliste §14.1 ab, schreibt die
Historie fort und packt das ZIP nach ausgabe/.
"""
import argparse
import importlib.util
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)

from autoria import lauf


def spec_laden(pfad):
    name = os.path.splitext(os.path.basename(pfad))[0]
    spec_datei = importlib.util.spec_from_file_location(name, pfad)
    modul = importlib.util.module_from_spec(spec_datei)
    spec_datei.loader.exec_module(modul)
    if not hasattr(modul, "spec"):
        raise AttributeError(f"{pfad} hat keine Funktion spec()")
    return modul.spec()


def main():
    ap = argparse.ArgumentParser(description="AUTORIA — AP1-Satz erzeugen")
    ap.add_argument("satzdatei", help="z. B. saetze/nr01.py")
    ap.add_argument("--historie", default=None,
                    help="bisherige Historie-JSON zum Fortschreiben (§11.7)")
    ap.add_argument("--reihenplan", default=None,
                    help="Reihenplan-JSON für Sperren und Pflichtbelegung (§10)")
    ap.add_argument("--ausgabe", default=os.path.join(HIER, "ausgabe"))
    ap.add_argument("--arbeit", default=os.path.join(HIER, "arbeit"))
    ap.add_argument("--ohne-pdf", action="store_true")
    args = ap.parse_args()

    spec = spec_laden(args.satzdatei)
    name = spec["meta"]["satzname"]
    print(f"Satz {name} — Produktion läuft …")

    zip_pfad, befund = lauf.satz_bauen(
        spec,
        arbeitsordner=os.path.join(args.arbeit, name),
        ausgabeordner=args.ausgabe,
        vorlagen_ordner=os.path.join(HIER, "vorlagen"),
        bilder_ordner=os.path.join(HIER, "bilder"),
        alte_historie=args.historie,
        pdf=not args.ohne_pdf,
        reihenplan=args.reihenplan,
    )
    print()
    print("=" * 72)
    print(f"AMPELBERICHT {name}  (§14.2)")
    print("=" * 72)
    print(befund.bericht())
    print("=" * 72)
    print(f"ZIP: {zip_pfad}")
    if not befund.bestanden:
        print("\nRegelverstöße gefunden — Satz vor dem Einsatz überarbeiten.")
        return 1
    print("\nKeine Regelverstöße. Die roten Einträge sind Grenzen der maschinellen "
          "Prüfung und vor dem Einsatz abzuarbeiten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
