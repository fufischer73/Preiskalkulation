#!/usr/bin/env python3
"""Erzeugt das Arbeitsmaterial: material/Kalkulationsschemata.xlsx (Tabelle mit einem Blatt je Schema, eine Spalte je Aufgabe)
und material/Kalkulationsschemata.pdf (dieselben Blätter zum Ausdrucken, über LibreOffice).
Aufruf (im Projektordner):  python3 docs/bau_material.py
Die Spalten stehen unter „Aufgaben“ in SPALTEN; neue Aufgabe = neue Spalte eintragen und neu bauen."""
import subprocess
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BLAU, HELL, GRAU, ROT = "2563B0", "E7EEF8", "F3F6FB", "EA2423"
duenn = Side(style="thin", color="8A94A3")
RAND = Border(left=duenn, right=duenn, top=duenn, bottom=duenn)

# (Blattname, Titel, Hinweis, Zeilen, Spalten)  Zeilen: (Beschriftung, Art) – Art: e = Eingabezeile, s = Summenzeile (fett), t = Zwischentitel
Z_ZUSCHLAG = [("Materialeinzelkosten (MEK)", "e"), ("+ Materialgemeinkosten (MGK)", "e"), ("= Materialkosten (MK)", "s"),
              ("Fertigungseinzelkosten (FEK)", "e"), ("+ Fertigungsgemeinkosten (FGK)", "e"), ("+ Sondereinzelkosten der Fertigung (SEKF)", "e"),
              ("= Fertigungskosten (FK)", "s"), ("= Herstellkosten (MK + FK)", "s"), ("+ Verwaltungsgemeinkosten (VwGK)", "e"),
              ("+ Vertriebsgemeinkosten (VtGK)", "e"), ("+ Sondereinzelkosten des Vertriebs (SEKV)", "e"), ("= Selbstkosten (SK)", "s"),
              ("+ Gewinnzuschlag", "e"), ("= Barverkaufspreis (BVP)", "s"), ("+ Skonto („im Hundert“)", "e"), ("= Zielverkaufspreis (ZVP)", "s"),
              ("+ Rabatt („im Hundert“)", "e"), ("= Listenverkaufspreis (LVP)", "s")]
BLAETTER = [
    ("Zuschlagskalk. pu2+zk1", "Zuschlagskalkulation (Vollkosten): pu2 und zk1", "Eine Spalte je Aufgabe. Zuschlagssätze stehen in der Aufgabe, hier trägst du die Beträge ein. Zeilen, die nicht vorkommen, bleiben leer.",
     Z_ZUSCHLAG,
     ["pu2 · Aufgabe 2\n(je Stück)", "pu2 · Aufgabe 2\n(300 Stück)", "zk1 · Aufgabe 2\n(je Stück)", "zk1 · Aufgabe 2\n(40 Stück)", "zk1 · Übung\nSporttasche „Match“",
      "zk1 · Plus 2\n(Serie, Gesamtwerte)"]),
    ("Zuschlagskalk. zk3", "Zuschlagskalkulation (Vollkosten): zk3 Sondereinzelkosten", "Eine Spalte je Aufgabe. Sondereinzelkosten der Fertigung und des Vertriebs stehen in eigenen Zeilen.",
     Z_ZUSCHLAG,
     ["zk3 · Aufgabe 1\n(je Stück)", "zk3 · Aufgabe 1\n(50 Stück)", "zk3 · Übung\n„Expedition“ (100 St.)", "zk3 · Plus 1", "zk3 · Plus 2 a)"]),
    ("Zwei Fertigungsstufen", "Zuschlagskalkulation mit zwei Fertigungsstufen", "Für zk1 · Plus 1 (Messe-Rucksack). Rechne die Lohnkosten aus Minuten und Stundensatz.",
     [("Fertigungsmaterial (MEK)", "e"), ("+ Materialgemeinkosten (MGK)", "e"), ("= Materialkosten (MK)", "s"), ("Fertigungslohn Stufe I", "e"), ("+ FGK Stufe I", "e"),
      ("Fertigungslohn Stufe II", "e"), ("+ FGK Stufe II", "e"), ("= Fertigungskosten (FK)", "s"), ("= Herstellkosten", "s"), ("+ Verwaltungsgemeinkosten", "e"),
      ("+ Vertriebsgemeinkosten", "e"), ("= Selbstkosten", "s"), ("+ Gewinn", "e"), ("= Barverkaufspreis", "s"), ("+ Skonto („im Hundert“)", "e"),
      ("= Zielverkaufspreis", "s"), ("+ Rabatt („im Hundert“)", "e"), ("= Listenverkaufspreis", "s")], ["zk1 · Plus 1\n(je Rucksack)"]),
    ("Vor- und Nachkalkulation", "Vor- und Nachkalkulation", "Je Aufgabe zwei Spalten: links die Vorkalkulation (Normalkosten), rechts die Nachkalkulation (Ist-Kosten). Der Barverkaufspreis steht fest.",
     [("Materialeinzelkosten", "e"), ("+ Materialgemeinkosten", "e"), ("= Materialkosten", "s"), ("Fertigungseinzelkosten", "e"), ("+ Fertigungsgemeinkosten", "e"),
      ("= Fertigungskosten", "s"), ("= Herstellkosten", "s"), ("+ Verwaltungsgemeinkosten", "e"), ("+ Vertriebsgemeinkosten", "e"), ("= Selbstkosten", "s"),
      ("Gewinn (Barverkaufspreis − Selbstkosten)", "e"), ("= Barverkaufspreis", "s")],
     ["zk2 · Aufgabe 1\nVorkalkulation", "zk2 · Aufgabe 1\nNachkalkulation", "zk2 · Übung\nVorkalkulation", "zk2 · Übung\nNachkalkulation", "zk2 · Plus\nVorkalkulation", "zk2 · Plus\nNachkalkulation"]),
    ("Teilkostenrechnung", "Teilkostenrechnung (variable Kosten)", "Nur die variablen Anteile eintragen. Einzelkosten sind zu 100 % variabel, bei den Gemeinkosten gibt die Aufgabe den variablen Anteil an.",
     [("Materialeinzelkosten (MEK)", "e"), ("+ variable Materialgemeinkosten", "e"), ("= variable Materialkosten", "s"), ("Fertigungseinzelkosten (FEK)", "e"),
      ("+ variable Fertigungsgemeinkosten", "e"), ("+ Sondereinzelkosten der Fertigung", "e"), ("= variable Fertigungskosten", "s"), ("= variable Herstellkosten", "s"),
      ("+ variable Verwaltungsgemeinkosten", "e"), ("+ variable Vertriebsgemeinkosten", "e"), ("+ Sondereinzelkosten des Vertriebs", "e"), ("= variable Selbstkosten", "s"),
      ("Erlös (Preis)", "e"), ("= Deckungsbeitrag", "s")],
     ["pu2 · Aufgabe 5\n(je Stück)", "pu2 · Aufgabe 5\n(300 Stück)", "pu2 · Übung 2\n„Daypack Basic“"]),
    ("Handelskalk. vorwärts", "Handelskalkulation: Vorwärtskalkulation", "Vom Einstandspreis zum Listenverkaufspreis. Darunter: Kalkulationszuschlag, -satz, -faktor, Handelsspanne.",
     [("Bezugs-/Einstandspreis", "e"), ("+ Handlungskosten", "e"), ("= Selbstkostenpreis", "s"), ("+ Gewinn", "e"), ("= Barverkaufspreis", "s"), ("+ Skonto („im Hundert“)", "e"),
      ("= Zielverkaufspreis", "s"), ("+ Rabatt („im Hundert“)", "e"), ("= Listenverkaufspreis", "s"), ("Kalkulationszuschlag (€)", "e"), ("Kalkulationszuschlagssatz (%)", "e"),
      ("Kalkulationsfaktor", "e"), ("Handelsspanne (%)", "e")],
     ["hk1 · Aufgabe 3\nLederPro", "hk1 · Plus b)\nRegenhülle", "hk1 · Plus b)\nGepäckrolle", "hk2 · Aufgabe 1\nStormGuard"]),
    ("Bezugskalkulation", "Bezugskalkulation (Einkauf)", "Vom Listeneinkaufspreis zum Einstandspreis. Das Ergebnis ist der Start der Handelskalkulation.",
     [("Listeneinkaufspreis", "e"), ("− Lieferantenrabatt", "e"), ("= Zieleinkaufspreis", "s"), ("− Lieferantenskonto", "e"), ("= Bareinkaufspreis", "s"),
      ("+ Bezugskosten", "e"), ("= Bezugs-/Einstandspreis", "s")], ["hk2 · Übung 1"]),
    ("Handelskalk. rückwärts", "Handelskalkulation: Rückwärtskalkulation", "Vom Listenverkaufspreis zurück zum höchsten Einstandspreis. Rabatt und Skonto „vom Hundert“, Gewinn und Handlungskosten „auf Hundert“.",
     [("Listenverkaufspreis", "e"), ("− Rabatt („vom Hundert“)", "e"), ("= Zielverkaufspreis", "s"), ("− Skonto („vom Hundert“)", "e"), ("= Barverkaufspreis", "s"),
      ("− Gewinn („auf Hundert“)", "e"), ("= Selbstkosten", "s"), ("− Handlungskosten („auf Hundert“)", "e"), ("= Bezugs-/Einstandspreis (höchstens)", "s"),
      ("− Bezugskosten (falls gegeben)", "e"), ("= Bareinkaufspreis", "s")], ["hk2 · Aufgabe 3", "hk2 · Plus 1"]),
    ("Differenzkalkulation", "Handelskalkulation: Differenzkalkulation", "Einstandspreis und Listenverkaufspreis sind gegeben. Oben vorwärts bis zu den Selbstkosten, in der Mitte rückwärts bis zum Barverkaufspreis, unten der Gewinn.",
     [("Einstandspreis", "e"), ("+ Handlungskosten", "e"), ("= Selbstkosten (vorwärts)", "s"), ("Listenverkaufspreis (gegeben)", "e"), ("− Rabatt", "e"),
      ("= Zielverkaufspreis", "s"), ("− Skonto", "e"), ("= Barverkaufspreis (rückwärts)", "s"), ("Gewinn (Barverkaufspreis − Selbstkosten)", "e"), ("Gewinn in % der Selbstkosten", "e")],
     ["hk2 · Aufgabe 4", "hk2 · Übung 1", "hk2 · Übung 2 a)", "hk2 · Übung 2 b)", "hk2 · Übung 2 c)", "hk2 · Übung 2 d)", "hk2 · Plus 2", "hk2 · Plus 3"]),
]


def tabelle_blatt(ws, titel, hinweis, zeilen, spalten):
    ws["A1"] = titel
    ws["A1"].font = Font(bold=True, size=14, color=BLAU)
    ws["A2"] = hinweis
    ws["A2"].font = Font(italic=True, size=10, color="595959")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max(2, min(len(spalten) + 1, 8)))
    ws.row_dimensions[2].height = 32
    kopf = 4
    ws.cell(row=kopf, column=1, value="Position").font = Font(bold=True, color="FFFFFF")
    ws.cell(row=kopf, column=1).fill = PatternFill("solid", fgColor=BLAU)
    ws.cell(row=kopf, column=1).border = RAND
    for j, s in enumerate(spalten, 2):
        c = ws.cell(row=kopf, column=j, value=s)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=BLAU)
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        c.border = RAND
        ws.column_dimensions[get_column_letter(j)].width = 16
    ws.row_dimensions[kopf].height = 44
    ws.column_dimensions["A"].width = 44
    for i, (text, art) in enumerate(zeilen, kopf + 1):
        c = ws.cell(row=i, column=1, value=text)
        c.data_type = "s"   # Beschriftungen wie „= Materialkosten“ sind Text, keine Formel
        c.border = RAND
        c.font = Font(bold=(art == "s"))
        c.fill = PatternFill("solid", fgColor=HELL if art == "s" else GRAU)
        for j in range(2, len(spalten) + 2):
            e = ws.cell(row=i, column=j)
            e.border = RAND
            e.number_format = "#,##0.00"
            if art == "s":
                e.fill = PatternFill("solid", fgColor=HELL)
        ws.row_dimensions[i].height = 20
    ws.freeze_panes = ws.cell(row=kopf + 1, column=2)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = f"{kopf}:{kopf}"
    ws.oddFooter.center.text = "&A · Seite &P von &N"
    ws.oddHeader.left.text = "Absatzprozesse · Preispolitik"
    ws.oddHeader.right.text = "BGW24a · BRC"


def freie_tabelle(ws, titel, hinweis, kopf, zeilen_beschriftung, spalten_breite=15):
    """Kopfzeile + beschriftete Zeilen (z. B. Mengen), alles andere zum Ausfüllen."""
    ws["A1"] = titel
    ws["A1"].font = Font(bold=True, size=14, color=BLAU)
    ws["A2"] = hinweis
    ws["A2"].font = Font(italic=True, size=10, color="595959")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(kopf))
    for j, k in enumerate(kopf, 1):
        c = ws.cell(row=4, column=j, value=k)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=BLAU)
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        c.border = RAND
        ws.column_dimensions[get_column_letter(j)].width = 22 if j == 1 else spalten_breite
    ws.row_dimensions[4].height = 36
    for i, text in enumerate(zeilen_beschriftung, 5):
        c = ws.cell(row=i, column=1, value=text)
        c.border = RAND
        c.fill = PatternFill("solid", fgColor=GRAU)
        for j in range(2, len(kopf) + 1):
            e = ws.cell(row=i, column=j)
            e.border = RAND
            e.number_format = "#,##0.00"
        ws.row_dimensions[i].height = 20
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "&A · Seite &P von &N"
    ws.oddHeader.left.text = "Absatzprozesse · Preispolitik"
    ws.oddHeader.right.text = "BGW24a · BRC"


def baue(ordner):
    wb = Workbook()
    wb.remove(wb.active)
    for name, titel, hinweis, zeilen, spalten in BLAETTER:
        tabelle_blatt(wb.create_sheet(name[:31]), titel, hinweis, zeilen, spalten)
    ws = wb.create_sheet("Kosten und Menge")
    freie_tabelle(ws, "Fixe und variable Kosten: Tabelle nach Mengen", "Für fv1 · Aufgabe 2 (Fjord 500: 100 bis 500 Stück). Die Zeilen darunter sind für weitere Mengen frei (z. B. Übungen).",
                  ["Menge", "fixe Kosten", "variable Kosten", "Gesamtkosten", "fixe Stückkosten", "variable Stückkosten", "Stückkosten"],
                  ["100 Stück", "200 Stück", "300 Stück", "400 Stück", "500 Stück", "", "", ""])
    ws = wb.create_sheet("Deckungsbeitrag")
    freie_tabelle(ws, "Deckungsbeitrag und Ergebnis nach Mengen", "Für db1 · Aufgabe 2 (150, 200, 250 Stück). Freie Zeilen für weitere Mengen.",
                  ["Menge", "Erlös", "variable Kosten", "Gesamtdeckungsbeitrag", "fixe Kosten", "Gewinn / Verlust"], ["150 Stück", "200 Stück", "250 Stück", "", "", ""])
    zeilen_ms = [("Nettoerlöse", "e"), ("− variable Kosten", "e"), ("= Deckungsbeitrag I", "s"), ("− Erzeugnisfixkosten", "e"), ("= Deckungsbeitrag II", "s"),
                 ("− Erzeugnisgruppenfixkosten", "e"), ("= Deckungsbeitrag III", "s"), ("− Bereichsfixkosten", "e"), ("= Deckungsbeitrag IV", "s"),
                 ("− Unternehmensfixkosten", "e"), ("= Erfolg", "s")]
    hinweis_ms = "Je Spalte ein Erzeugnis. Gruppen-, Bereichs- und Unternehmensfixkosten trägst du in der Spalte des ersten Erzeugnisses der Gruppe bzw. des Bereichs ein."
    tabelle_blatt(wb.create_sheet("Mehrstufige DB Plus 4"), "Mehrstufige Deckungsbeitragsrechnung: db1 Plus 4", hinweis_ms, zeilen_ms,
                  ["A1", "A2", "B1", "B2", "C1"])
    tabelle_blatt(wb.create_sheet("Mehrstufige DB Plus 5"), "Mehrstufige Deckungsbeitragsrechnung: db1 Plus 5", hinweis_ms, zeilen_ms,
                  ["P1", "P2", "P3", "P4", "P5"])
    ziel = ordner / "material"
    ziel.mkdir(exist_ok=True)
    x = ziel / "Kalkulationsschemata.xlsx"
    wb.save(x)
    # PDF über LibreOffice (jedes Blatt eine oder mehrere Seiten, quer)
    r = subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(ziel), str(x)], capture_output=True, text=True, timeout=180)
    if r.returncode != 0 or not (ziel / "Kalkulationsschemata.pdf").exists():
        sys.exit("PDF-Erzeugung mit LibreOffice fehlgeschlagen:\n" + r.stderr)
    return x, ziel / "Kalkulationsschemata.pdf"


if __name__ == "__main__":
    x, p = baue(Path(__file__).resolve().parents[1])
    print("✓", x, "·", p)
