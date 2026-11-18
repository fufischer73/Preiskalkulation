#!/usr/bin/env python3
"""Rechenprobe zu Stufe 3 (hk1, hk2): alle Zahlen der Handelskalkulation, kaufmännisch gerundet (je Zeile auf Cent).
Aufruf: python3 docs/rechenprobe_stufe3.py  – jede Zeile „PRÜFUNG“ muss „ok“ sein."""
from decimal import Decimal as D, ROUND_HALF_UP


def r(x, n=2):
    return D(str(x)).quantize(D(1).scaleb(-n), rounding=ROUND_HALF_UP)


def zahl(x, n=2):
    return f"{r(x, n):,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")


def vor(e, hk, g, s, rab):
    """Vorwärtskalkulation: Einstandspreis → Listenverkaufspreis. Gewinn auf die Selbstkosten, Skonto/Rabatt „im Hundert“."""
    L = {"E": r(e)}
    L["HK"] = r(L["E"] * D(str(hk)) / 100); L["SK"] = L["E"] + L["HK"]
    L["G"] = r(L["SK"] * D(str(g)) / 100); L["BVP"] = L["SK"] + L["G"]
    L["S"] = r(L["BVP"] * D(str(s)) / (100 - D(str(s)))); L["ZVP"] = L["BVP"] + L["S"]
    L["R"] = r(L["ZVP"] * D(str(rab)) / (100 - D(str(rab)))); L["LVP"] = L["ZVP"] + L["R"]
    return L


def rueck(lvp, hk, g, s, rab):
    """Rückwärtskalkulation: Listenverkaufspreis → maximaler Einstandspreis. Rabatt/Skonto vom Hundert, Gewinn/HK „auf Hundert“."""
    L = {"LVP": r(lvp)}
    L["R"] = r(L["LVP"] * D(str(rab)) / 100); L["ZVP"] = L["LVP"] - L["R"]
    L["S"] = r(L["ZVP"] * D(str(s)) / 100); L["BVP"] = L["ZVP"] - L["S"]
    L["SK"] = r(L["BVP"] / (1 + D(str(g)) / 100)); L["G"] = L["BVP"] - L["SK"]
    L["E"] = r(L["SK"] / (1 + D(str(hk)) / 100)); L["HK"] = L["SK"] - L["E"]
    return L


def kz(e, lvp):
    """Kalkulationszuschlagssatz (%), Kalkulationsfaktor, Handelsspanne (%)."""
    return dict(KZS=(D(str(lvp)) - D(str(e))) / D(str(e)) * 100, F=D(str(lvp)) / D(str(e)),
                HS=(D(str(lvp)) - D(str(e))) / D(str(lvp)) * 100)


ok = True


def pruefe(name, ist, soll, n=2):
    global ok
    gut = r(ist, n) == r(soll, n)
    ok &= gut
    print(f"PRÜFUNG {name}: {zahl(ist, n)} {'ok' if gut else '!!! erwartet ' + zahl(soll, n)}")


# ---------------------------------------------------------------- hk1
A1 = vor("3.60", 30, 12, 2, 6)                    # Lederpflege-Spray „LederPro“
A1K = kz(A1["E"], A1["LVP"])
FAKTOR = r(A1K["F"], 4)                           # 4 Nachkommastellen
A1_PRODUKTE = {n: (D(e), r(D(e) * FAKTOR)) for n, e in (("Ledercreme", "5.20"), ("Imprägnierspray", "3.45"), ("Reißverschlusswachs", "2.80"))}
A1_TAB = [("Regenhülle S", "4.80", "9.90"), ("Regenhülle L", "6.20", "12.50"), ("Schlüsselband", "2.40", "2.90"),
          ("Gepäckanhänger", "3.20", "3.40"), ("Trinkflasche", "5.90", "8.90")]
A1_TAB_F = {n: kz(e, l) for n, e, l in A1_TAB}
UE1A = kz("31.20", "52.00")
UE1B = dict(LVP=r(D(275) * D("1.30")), HS=(D(275) * D("1.30") - 275) / (D(275) * D("1.30")) * 100)
# Plus: einheitlicher Faktor vs. warengruppenspezifische Handlungskosten
PL1 = {"Regenhülle (20 % HK)": vor("4.80", 20, 12, 2, 6), "Gepäckrolle (45 % HK)": vor("14.50", 45, 12, 2, 6)}
PL1_EINH = {"Regenhülle (20 % HK)": r(D("4.80") * FAKTOR), "Gepäckrolle (45 % HK)": r(D("14.50") * FAKTOR)}
# Gewinn bei einheitlichem Preis (mit den tatsächlichen Handlungskosten)
def gewinn_bei_preis(e, hk, lvp, s, rab):
    """Aus Listenpreis rückwärts bis zum Barverkaufspreis, dann Gewinn = BVP − Selbstkosten (Handlungskosten „auf Hundert“)."""
    zvp = r(D(str(lvp)) * (100 - D(str(rab))) / 100); bvp = r(zvp * (100 - D(str(s))) / 100)
    sk = r(D(str(e)) * (1 + D(str(hk)) / 100))
    return dict(BVP=bvp, SK=sk, G=bvp - sk, Gp=(bvp - sk) / sk * 100)
PL1_G = {k: gewinn_bei_preis(e, hk, PL1_EINH[k], 2, 6) for k, e, hk in (("Regenhülle (20 % HK)", "4.80", 20), ("Gepäckrolle (45 % HK)", "14.50", 45))}

# ---------------------------------------------------------------- hk2
B_E, B_HK, B_G, B_S, B_R, B_MARKT = D("58.00"), 18, 22, 2, 6, D("79.00")
B1 = vor(B_E, B_HK, B_G, B_S, B_R)
B_HS = (B1["LVP"] - B_E) / B1["LVP"] * 100
B3 = rueck(B_MARKT, B_HK, B_G, B_S, B_R)
B4G = B3["BVP"] - B1["SK"]; B4P = B4G / B1["SK"] * 100        # Differenzkalkulation: Einstand bleibt 38,00 €
B5 = (B_MARKT - B_E) / B_MARKT * 100
# Übung 1: Bezugskalkulation
def bezug(lek, rab, sk, bez):
    r1 = r(D(str(lek)) * D(str(rab)) / 100); zek = D(str(lek)) - r1
    s1 = r(zek * D(str(sk)) / 100); bek = zek - s1
    return dict(LEK=r(lek), R=r1, ZEK=zek, S=s1, BEK=bek, BZK=r(bez), E=bek + r(bez))
UE2_B = bezug(360, 20, 2, "18.50")
UE2 = vor(UE2_B["E"], 20, 0, 2, 10)                            # nur bis Selbstkosten nötig
UE2_LVP = D(430)
def diff(e, hk, s, rab, lvp):
    sk = r(D(str(e)) * (1 + D(str(hk)) / 100)); zvp = r(D(str(lvp)) * (100 - D(str(rab))) / 100); bvp = r(zvp * (100 - D(str(s))) / 100)
    return dict(SK=sk, ZVP=zvp, BVP=bvp, G=bvp - sk, Gp=(bvp - sk) / sk * 100)
UE2_D = diff(UE2_B["E"], 20, 2, 10, UE2_LVP)
UE3 = [("a", "36.00", 25, "2.5", 10, "74.00"), ("b", "92.00", 20, 2, "12.5", "148.00"), ("c", "15.40", 15, "1.5", 8, "31.00"), ("d", "840.00", 30, 1, 5, "1450.00")]
UE3_D = {k: diff(e, hk, s, rab, l) for k, e, hk, s, rab, l in UE3}
# Plus: Konkurrenz rückwärts
P1 = rueck("24.90", "20", "12.5", 2, 10)
P1_BE = P1["E"] - r("1.80"); P1_K = kz(P1["E"], "24.90")
# Plus: Mengenrabatt auf Gesamtmenge
P2 = dict(E=D("19.20"), hk=15, preis_alt=D("29.90"), rabatt=D("12.5"))
P2["HK"] = r(P2["E"] * 15 / 100); P2["SK"] = P2["E"] + P2["HK"]
P2["G_alt"] = P2["preis_alt"] - P2["SK"]; P2["Gp_alt"] = P2["G_alt"] / P2["SK"] * 100
P2["R"] = r(P2["preis_alt"] * D("12.5") / 100); P2["P_neu"] = P2["preis_alt"] - P2["R"]; P2["G_neu"] = P2["P_neu"] - P2["SK"]; P2["Gp_neu"] = P2["G_neu"] / P2["SK"] * 100
P2["Gesamt_alt"] = P2["G_alt"] * 150; P2["Gesamt_neu"] = P2["G_neu"] * 200
# Plus: Einstand 55, BVP 89, HK 18 %
P3 = dict(SK=r(D(55) * D("1.18")), HK=r(D(55) * 18 / 100)); P3["G"] = D(89) - P3["SK"]; P3["Gp"] = P3["G"] / P3["SK"] * 100


def haupt():
    print("=== hk1 · AS I ===")
    for k in ("E", "HK", "SK", "G", "BVP", "S", "ZVP", "R", "LVP"):
        print(f"  {k:4} {zahl(A1[k])}")
    pruefe("LVP LederPro", A1["LVP"], "5.69")
    print("  KZ:", {k: zahl(v, 4) for k, v in A1K.items()}, "· Faktor gerundet", FAKTOR)
    for n, (e, p) in A1_PRODUKTE.items():
        print(f"  {n}: {zahl(e)} → {zahl(p)}")
    for n, v in A1_TAB_F.items():
        print(f"  {n}: Faktor {zahl(v['F'], 4)} · KZS {zahl(v['KZS'])} % · HS {zahl(v['HS'])} %")
    print("  Übung 1a:", {k: zahl(v, 4) for k, v in UE1A.items()}, " 1b:", {k: zahl(v) for k, v in UE1B.items()})
    for n, v in PL1.items():
        print(f"  Plus {n}:", {k: zahl(x) for k, x in v.items()}, "· einheitlich", zahl(PL1_EINH[n]), "· Gewinn bei einheitl. Preis", {k: zahl(x) for k, x in PL1_G[n].items()})
    print("=== hk2 · AS II ===")
    print(" ", {k: zahl(v) for k, v in B1.items()}, "· Handelsspanne", zahl(B_HS))
    print("  rückwärts:", {k: zahl(v) for k, v in B3.items()})
    print("  Differenz: Gewinn", zahl(B4G), "=", zahl(B4P), "% · Handelsspanne bei 79 €:", zahl(B5))
    print("  Übung 1:", {k: zahl(v) for k, v in UE2_B.items()}, "· SK", zahl(UE2["SK"]), {k: zahl(v) for k, v in UE2_D.items()})
    for k, v in UE3_D.items():
        print(f"  Übung 2{k}:", {a: zahl(b) for a, b in v.items()})
    print("  Plus 1:", {k: zahl(v) for k, v in P1.items()}, "· Bareinkauf", zahl(P1_BE), {k: zahl(v, 4) for k, v in P1_K.items()})
    print("  Plus 2:", {k: zahl(v) for k, v in P2.items()})
    print("  Plus 3:", {k: zahl(v) for k, v in P3.items()})
    print("\nGESAMT:", "alles ok" if ok else "FEHLER – bitte oben suchen")


if __name__ == "__main__":
    haupt()
