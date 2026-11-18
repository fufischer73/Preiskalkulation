#!/usr/bin/env python3
"""Rechenprobe zu Stufe 1 (pu1, pu2, pum): alle Zahlen der Aufgaben und Lösungen, kaufmännisch gerundet.
Aufruf: python3 docs/rechenprobe-stufe1.py  – jede Zeile „PRÜFUNG“ muss „ok“ sein."""
from decimal import Decimal as D, ROUND_HALF_UP

def r(x, n=2):
    return D(str(x)).quantize(D(1).scaleb(-n), rounding=ROUND_HALF_UP)
def eur(x): return f"{r(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"
ok = True
def pruefe(name, ist, soll):
    global ok
    gut = r(ist) == r(soll)
    ok &= gut
    print(f"PRÜFUNG {name}: {eur(ist)} {'ok' if gut else '!!! erwartet ' + eur(soll)}")

print("=== pu1 · AS I: Daypack „City Light“ ===")
kap, preis_alt, markt = 4000, D(89), D(64)
kv = D("24.00") + D("13.50") + D("2.00")
Kf = D(58000) + D(16000) + D(38000) + D(8000)
kf = Kf / kap; k = kv + kf
pruefe("variable Stückkosten", kv, "39.50"); pruefe("fixe Stückkosten", kf, "30.00"); pruefe("Stückkosten", k, "69.50")
db = markt - kv; pruefe("Stückdeckungsbeitrag bei 64", db, "24.50")
DB = db * kap; pruefe("Gesamtdeckungsbeitrag", DB, 98000)
pruefe("Ergebnis bei 64 €", DB - Kf, -22000); pruefe("Verlust ohne Produktion", -Kf, -120000)
pruefe("Verlust je Stück bei 64", markt - k, "-5.50")

print("=== pu1 · Übung: Rucksack „Trail Pro“ ===")
kv2, Kf2, kap2, m2 = D(52), D(96000), 1600, D(98)
pruefe("kf", Kf2 / kap2, 60); pruefe("k", kv2 + Kf2 / kap2, 112); pruefe("db bei 98", m2 - kv2, 46)
pruefe("Ergebnis bei 98 (1.600 St.)", (m2 - kv2) * kap2 - Kf2, -22400)
pruefe("lang. PUG bei 1.200 St.", kv2 + Kf2 / 1200, 132); pruefe("Ergebnis bei 98 (1.200 St.)", (m2 - kv2) * 1200 - Kf2, -40800)

print("=== pu1 · Plus: City Light zu 58 €, nur 2.500 Stück ===")
pruefe("db bei 58", D(58) - kv, "18.50"); pruefe("Ergebnis", (D(58) - kv) * 2500 - Kf, -73750)
pruefe("lang. PUG bei 2.500 St.", kv + Kf / 2500, "87.50")

print("=== pu2 · AS II: Sonderedition Business Deluxe, 300 Stück zu 118 € ===")
def schema(menge, mek, fek, sekf, sekv, z, anteil):
    """z: MGK, FGK, VwGK, VtGK in %; anteil: variabler Anteil der Gemeinkosten. Rundung je Zeile auf Cent (je Stück)."""
    L = {}
    L["MEK"] = r(mek); L["MGK"] = r(L["MEK"] * z[0] / 100); L["MK"] = L["MEK"] + L["MGK"]
    L["FEK"] = r(fek); L["FGK"] = r(L["FEK"] * z[1] / 100); L["SEKF"] = r(sekf); L["FK"] = L["FEK"] + L["FGK"] + L["SEKF"]
    L["HK"] = L["MK"] + L["FK"]
    L["VwGK"] = r(L["HK"] * z[2] / 100); L["VtGK"] = r(L["HK"] * z[3] / 100); L["SEKV"] = r(sekv)
    L["SK"] = L["HK"] + L["VwGK"] + L["VtGK"] + L["SEKV"]
    T = {}
    T["MEK"] = L["MEK"]; T["vMGK"] = r(L["MGK"] * anteil[0] / 100); T["vMK"] = T["MEK"] + T["vMGK"]
    T["FEK"] = L["FEK"]; T["vFGK"] = r(L["FGK"] * anteil[1] / 100); T["SEKF"] = L["SEKF"]; T["vFK"] = T["FEK"] + T["vFGK"] + T["SEKF"]
    T["vHK"] = T["vMK"] + T["vFK"]
    T["vVwGK"] = r(L["VwGK"] * anteil[2] / 100); T["vVtGK"] = r(L["VtGK"] * anteil[3] / 100); T["SEKV"] = L["SEKV"]
    T["vSK"] = T["vHK"] + T["vVwGK"] + T["vVtGK"] + T["SEKV"]
    return L, T
L, T = schema(300, 24, 36, "4.50", "1.80", (5, 130, 10, 5), (50, 25, 20, 10))
for kz in ("MEK", "MGK", "MK", "FEK", "FGK", "SEKF", "FK", "HK", "VwGK", "VtGK", "SEKV", "SK"):
    print(f"  {kz:5} {eur(L[kz]):>12}  ×300 = {eur(L[kz] * 300):>14}")
for kz in ("vMGK", "vMK", "vFGK", "vFK", "vHK", "vVwGK", "vVtGK", "vSK"):
    print(f"  {kz:6} {eur(T[kz]):>11}  ×300 = {eur(T[kz] * 300):>14}")
pruefe("Selbstkosten", L["SK"], "131.18"); pruefe("variable Selbstkosten", T["vSK"], "81.41")
pruefe("Ergebnis je Stück Vollkosten", 118 - L["SK"], "-13.18"); pruefe("Ergebnis gesamt Vollkosten", (118 - L["SK"]) * 300, -3954)
pruefe("Stückdeckungsbeitrag", 118 - T["vSK"], "36.59"); pruefe("Deckungsbeitrag gesamt", (118 - T["vSK"]) * 300, 10977)
# Standardrucksack ohne Sondereinzelkosten (Bezug zu Montelli: variable Stückkosten 75,00 €)
L0, T0 = schema(1, 24, 36, 0, 0, (5, 130, 10, 5), (50, 25, 20, 10))
pruefe("Standard: variable Stückkosten (Montelli-Eckdatum 75 €)", T0["vSK"], 75); print("  Standard: Selbstkosten", eur(L0["SK"]))

print("=== pu2 · Übung 1: Messe-Tasche „Express“ (monatlich) ===")
kv3 = D("14.60") + D("6.40"); kap3 = 600
fix3 = {"Abschreibungen": D(1800), "Zinsen": D(900), "Versicherung": D(120), "Gehalt Aufsicht": D(2400)}
pruefe("kurzfristige PUG", kv3, 21)
aus = fix3["Versicherung"] + fix3["Gehalt Aufsicht"]
pruefe("liquiditätsorientierte PUG", kv3 + aus / kap3, "25.20"); pruefe("langfristige PUG", kv3 + sum(fix3.values()) / kap3, "29.70")

print("=== pu2 · Übung 2: Daypack-Teilkostenschema ===")
L2, T2 = schema(1, "11.00", "11.00", 0, 0, (5, 130, 8, 4), (60, 50, 25, 15))
L2, T2 = schema(1, 14, 11, 0, 0, (5, 130, 8, 4), (60, 50, 25, 15))
for kz in ("MEK", "MGK", "MK", "FEK", "FGK", "FK", "HK", "VwGK", "VtGK", "SK"):
    print(f"  {kz:5} {eur(L2[kz]):>10}")
for kz in ("vMGK", "vMK", "vFGK", "vFK", "vHK", "vVwGK", "vVtGK", "vSK"):
    print(f"  {kz:6} {eur(T2[kz]):>9}")

print("=== pu2 · Plus: Rucksack „Office Slim“, Discounter ===")
kv4 = D(36000) / 800; pruefe("var. Stückkosten", kv4, 45)
erl = D(95) * D("0.8"); pruefe("Discounter-Preis", erl, 76); pruefe("db", erl - kv4, 31); pruefe("Verbesserung", (erl - kv4) * 100, 3100)
pruefe("mittelfr. PUG bei 1.000", kv4 + D(22000) * D("0.12") / 1000, "47.64"); pruefe("langfr. PUG bei 1.000", kv4 + D(22000) / 1000, 67)

print("=== pum · Meilenstein: Fallakte Eigenmarken-Anfrage ===")
kap5, absatz, p_liste, kv5, Kf5, ausg5 = 10000, 6600, D(165), D(75), D(350000), D(105000)
menge, p_ang, sekv5, auftragsfix = 2800, D(99), D("3.50"), D(9000)
pruefe("Ergebnis heute", (p_liste - kv5) * absatz - Kf5, 244000)
pruefe("Stückdeckungsbeitrag Auftrag", p_ang - kv5 - sekv5, "20.50"); pruefe("DB gesamt Auftrag", (p_ang - kv5 - sekv5) * menge, 57400)
pruefe("Beitrag nach auftragsfixen Kosten", (p_ang - kv5 - sekv5) * menge - auftragsfix, 48400)
pruefe("Ergebnis mit Auftrag", (p_liste - kv5) * absatz - Kf5 + 48400, 292400)
pruefe("Auslastung nach Auftrag %", D(absatz + menge) * 100 / kap5, 94)
pruefe("kurzfr. PUG des Auftrags (incl. auftragsfixe Kosten)", kv5 + sekv5 + auftragsfix / menge, "81.71")
pruefe("liquiditätsorient. PUG (bei 9.400 St.)", kv5 + sekv5 + ausg5 / (absatz + menge), "89.67")
pruefe("langfr. PUG bei 6.600 St.", kv5 + Kf5 / absatz, "128.03"); pruefe("langfr. PUG bei 9.400 St.", kv5 + Kf5 / (absatz + menge), "112.23")
pruefe("Forderungen: Erlös Auftrag", p_ang * menge, 277200)
pruefe("Break-even-Preis des Auftrags (DB deckt auftragsfixe Kosten)", kv5 + sekv5 + auftragsfix / menge, "81.71")
print("\nGESAMT:", "alles ok" if ok else "FEHLER – bitte oben suchen")
