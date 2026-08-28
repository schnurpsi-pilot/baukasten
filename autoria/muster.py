# -*- coding: utf-8 -*-
"""Erzeugt Gestaltungsmuster für Diagramme (Anlage nach §11.4).

Das Muster zeigt ausschließlich Aufbau und Formatierung. Die Werte sind
bedeutungslos und dürfen nicht zu den Aufgabendaten passen, damit sich
daraus keine Ergebnisse ableiten lassen. Alles schwarz-weiß (§8).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BEISPIEL_KATEGORIEN = ["Muster A", "Muster B", "Muster C", "Muster D"]
BEISPIEL_WERTE = [42, 61, 35, 55]


def diagrammmuster(pfad, typ="balken", kategorien=None, werte=None,
                   titel="Diagrammüberschrift",
                   wertachse="Beschriftung der Wertachse",
                   rubrikachse="Beschriftung der Rubrikenachse",
                   reihenname="Beispielreihe", trendlinie=False):
    """Schreibt ein Musterbild. typ: balken | saeule | linie | kreis."""
    kategorien = kategorien or BEISPIEL_KATEGORIEN
    werte = werte or BEISPIEL_WERTE
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(7.4, 3.5), dpi=200)

    if typ == "balken":
        ax.barh(kategorien[::-1], werte[::-1], color="0.55", edgecolor="0.2",
                height=0.6, label=reihenname)
        ax.set_xlabel(wertachse, fontsize=9)
        ax.set_ylabel(rubrikachse, fontsize=9)
        ax.xaxis.grid(True, color="0.85", linewidth=0.6)
    elif typ == "saeule":
        ax.bar(kategorien, werte, color="0.55", edgecolor="0.2", width=0.6,
               label=reihenname)
        ax.set_ylabel(wertachse, fontsize=9)
        ax.set_xlabel(rubrikachse, fontsize=9)
        ax.yaxis.grid(True, color="0.85", linewidth=0.6)
    elif typ == "linie":
        ax.plot(kategorien, werte, color="0.3", marker="o", label=reihenname)
        ax.set_ylabel(wertachse, fontsize=9)
        ax.set_xlabel(rubrikachse, fontsize=9)
        ax.yaxis.grid(True, color="0.85", linewidth=0.6)
        if trendlinie:
            import numpy as np
            x = np.arange(len(werte))
            k, d = np.polyfit(x, werte, 1)
            ax.plot(kategorien, k * x + d, color="0.2", linestyle="--",
                    label="Trendlinie")
    elif typ == "kreis":
        ax.pie(werte, labels=kategorien, autopct="%1.1f%%",
               colors=["0.4", "0.55", "0.7", "0.85"],
               wedgeprops={"edgecolor": "0.2"}, textprops={"fontsize": 9})
        ax.set_ylabel("")
    else:
        raise KeyError(f"Unbekannter Diagrammtyp: {typ}")

    ax.set_title(titel, fontsize=11, fontweight="bold")
    if typ != "kreis":
        ax.tick_params(labelsize=9)
        ax.legend(loc="lower right", fontsize=8, frameon=True)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    else:
        ax.legend(loc="lower right", fontsize=8, frameon=True)
    fig.tight_layout()
    fig.savefig(pfad, facecolor="white")
    plt.close(fig)
    return pfad
