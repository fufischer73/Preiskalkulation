#!/usr/bin/env python3
"""Rechenprobe zu Stufe 2 (zk1, zk2, zk3, fv1, db1): alle Zahlen der Aufgaben, kaufmännisch gerundet (je Zeile auf Cent).
Aufruf: python3 docs/rechenprobe_stufe2.py  – jede Zeile „PRÜFUNG“ muss „ok“ sein.
Die Funktionen werden auch beim Schreiben der Lösungen benutzt (import)."""
from decimal import Decimal as D, ROUND_HALF_UP


def r(x, n=2):
    return D(str(x)).quantize(D(1).scaleb(-n), rounding=ROUND_HALF_UP)


def eur(x, n=2):
    s = f"{r(x, n):,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s.replace("-", "−") + " €"


def zahl(x, n=2):
    return f"{r(x, n):,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")


def pct(x, n=2):
    return zahl(x, n) + " %"


def zuschlag(mek, fek, z, gewinn=None, skonto=None, rabatt=None, sekf=0, sekv=0, menge=1):
    """Zuschlagskalkulation. z = (MGK, FGK, VwGK, VtGK) in %. Je Stück gerundet; Spalte „menge“ = je Stück · Menge.
    Gewinn auf die Selbstkosten, Skonto und Rabatt „im Hundert“."""
    L = {}
    L["MEK"] = r(mek); L["MGK"] = r(L["MEK"] * D(str(z[0])) / 100); L["MK"] = L["MEK"] + L["MGK"]
    L["FEK"] = r(fek); L["FGK"] = r(L["FEK"] * D(str(z[1])) / 100)
    L["SEKF"] = r(sekf); L["FK"] = L["FEK"] + L["FGK"] + L["SEKF"]
    L["HK"] = L["MK"] + L["FK"]
    L["VwGK"] = r(L["HK"] * D(str(z[2])) / 100); L["VtGK"] = r(L["HK"] * D(str(z[3])) / 100); L["SEKV"] = r(sekv)
    L["SK"] = L["HK"] + L["VwGK"] + L["VtGK"] + L["SEKV"]
    if gewinn is not None:
        L["Gewinn"] = r(L["SK"] * D(str(gewinn)) / 100); L["BVP"] = L["SK"] + L["Gewinn"]
    if skonto is not None:
        L["Skonto"] = r(L["BVP"] * D(str(skonto)) / (100 - D(str(skonto)))); L["ZVP"] = L["BVP"] + L["Skonto"]
    if rabatt is not None:
        L["Rabatt"] = r(L["ZVP"] * D(str(rabatt)) / (100 - D(str(rabatt)))); L["LVP"] = L["ZVP"] + L["Rabatt"]
    return L


def mal(L, n):
    return {k: v * n for k, v in L.items()}


ok = True


def pruefe(name, ist, soll):
    global ok
    gut = r(ist) == r(soll)
    ok &= gut
    print(f"PRÜFUNG {name}: {zahl(ist)} {'ok' if gut else '!!! erwartet ' + zahl(soll)}")


# ---------------------------------------------------------------- Daten
ZS = (5, 130, 10, 5)                    # Montelli-Normalzuschlagssätze (wie in pu2)
ZK1 = zuschlag(24, 36, ZS, gewinn=20, skonto=2, rabatt=8)
ZK1_UE = zuschlag("18.50", 12, ("6.35", 130, "4.5", "6.2"), gewinn=30, skonto=2, rabatt=5)   # Sporttasche
# Messe-Rucksack mit zwei Fertigungsstufen
def messe():
    mek = D("12.00") + D("4.50") + D("6.50") + D("3.00")
    l1 = r(D(40) * D("36.00") / 60); l2 = r(D(25) * D("30.00") / 60)
    L = {"MEK": r(mek)}; L["MGK"] = r(L["MEK"] * 8 / 100); L["MK"] = L["MEK"] + L["MGK"]
    L["FEK1"] = l1; L["FGK1"] = r(l1 * 90 / 100); L["FEK2"] = l2; L["FGK2"] = r(l2 * 70 / 100)
    L["FK"] = L["FEK1"] + L["FGK1"] + L["FEK2"] + L["FGK2"]; L["HK"] = L["MK"] + L["FK"]
    L["VwGK"] = r(L["HK"] * 7 / 100); L["VtGK"] = r(L["HK"] * 5 / 100); L["SK"] = L["HK"] + L["VwGK"] + L["VtGK"]
    L["Gewinn"] = r(L["SK"] * 12 / 100); L["BVP"] = L["SK"] + L["Gewinn"]
    L["Skonto"] = r(L["BVP"] * 2 / 98); L["ZVP"] = L["BVP"] + L["Skonto"]
    L["Rabatt"] = r(L["ZVP"] * 10 / 90); L["LVP"] = L["ZVP"] + L["Rabatt"]
    return L
ZK1_P1 = messe()
# Serienfertigung: 500 Stück, Gesamtwerte
def serie():
    mek, fek = D(16000), D(12000)
    mgk = r(mek * 8 / 100); fgk = r(fek * 120 / 100); hk = mek + mgk + fek + fgk
    vw = r(hk * 9 / 100); vt = r(hk * 6 / 100); sk = hk + vw + vt
    return dict(MGK=mgk, FGK=fgk, HK=hk, VwGK=vw, VtGK=vt, SK=sk, HKj=r(hk / 500), SKj=r(sk / 500),
                Gewinn_j=D(118) - r(sk / 500), Gewinn_pct=(D(118) - sk / 500) / (sk / 500) * 100)
ZK1_P2 = serie()

# zk2
NACH_IST = dict(mek=D(1010), fek=D(1420), z=("5.6", 128, "10.4", "5.2"))
def nachkalk():
    mek, fek = D(1010), D(1420)
    mgk = r(mek * D("5.6") / 100); mk = mek + mgk; fgk = r(fek * 128 / 100); fk = fek + fgk; hk = mk + fk
    vw = r(hk * D("10.4") / 100); vt = r(hk * D("5.2") / 100); sk = hk + vw + vt
    bvp = ZK1["BVP"] * 40
    return dict(MEK=mek, MGK=mgk, MK=mk, FEK=fek, FGK=fgk, FK=fk, HK=hk, VwGK=vw, VtGK=vt, SK=sk, BVP=bvp,
                Gewinn=bvp - sk, Gewinn_pct=(bvp - sk) / sk * 100)
ZK2 = nachkalk()
def zk2_uebung():
    """30 Messerucksäcke: Vorkalkulation (Normal) und Nachkalkulation (Ist)."""
    mek, fek = D(3000), D(1500)
    v = zuschlag(mek, fek, ZS, gewinn=12, skonto=2, rabatt=5)
    mek2, fek2 = D(3060), D(1470)
    mgk = r(mek2 * 6 / 100); mk = mek2 + mgk; fgk = r(fek2 * 125 / 100); fk = fek2 + fgk; hk = mk + fk
    vw = r(hk * 11 / 100); vt = r(hk * 4 / 100); sk = hk + vw + vt
    return v, dict(MEK=mek2, MGK=mgk, MK=mk, FEK=fek2, FGK=fgk, FK=fk, HK=hk, VwGK=vw, VtGK=vt, SK=sk, BVP=v["BVP"],
                   Gewinn=v["BVP"] - sk, Gewinn_pct=(v["BVP"] - sk) / sk * 100)
ZK2_UE_V, ZK2_UE_N = zk2_uebung()
def zk2_plus():
    """Nachkalkulation zur Sporttasche (je Stück)."""
    mek, fek = D("19.30"), D("11.60")
    mgk = r(mek * D("6.9") / 100); mk = mek + mgk; fgk = r(fek * 134 / 100); fk = fek + fgk; hk = mk + fk
    vw = r(hk * D("4.8") / 100); vt = r(hk * 6 / 100); sk = hk + vw + vt
    bvp = ZK1_UE["BVP"]
    return dict(MEK=mek, MGK=mgk, MK=mk, FEK=fek, FGK=fgk, FK=fk, HK=hk, VwGK=vw, VtGK=vt, SK=sk, BVP=bvp,
                Gewinn=bvp - sk, Gewinn_pct=(bvp - sk) / sk * 100)
ZK2_PLUS = zk2_plus()

# zk3
ZK3 = zuschlag(24, 36, ZS, gewinn=20, skonto=2, rabatt=8, sekf="6.50", sekv="2.20")
ZK3_UE = zuschlag(2400, 1850, ("5.5", 128, "9.5", "5.5"), gewinn=18, skonto=2, rabatt=6, sekf=480, sekv=220)
ZK3_P1 = zuschlag(14000, 9000, (10, 140, 12, 8), gewinn=6, skonto=2, sekf=1300, sekv=1420)
ZK3_P2A = zuschlag(12000, 4000, (10, 250, 9, 6), gewinn=5, sekf=1500, sekv=1500)
def zk3_p2b():
    mek, sekv = D(11000), D(1250)
    mk = mek * D("1.10"); sk = D(31500) / D("1.05"); hk = (sk - sekv) / D("1.15")
    return dict(MK=mk, SK=sk, HK=hk, FK=hk - mk)
ZK3_P2B = zk3_p2b()

# fv1 (Fjord 500)
FV_KV = D("38.00") + D("21.00") + D("4.00")
FV_FIX = D(3000) + D(1000) + D(1400) + D(600)
FV_MENGEN = [100, 200, 300, 400, 500]
def fv_tabelle():
    return [dict(x=x, kfix=FV_FIX, kvar=FV_KV * x, kg=FV_FIX + FV_KV * x, kfs=FV_FIX / x, kvs=FV_KV, ks=FV_FIX / x + FV_KV) for x in FV_MENGEN]
FV_TAB = fv_tabelle()
def fv_ue1():
    fix = D(4250) + D(2400) + D(1100) + D(600); kv = D("31.00") + D("14.00") + D("2.50")
    return dict(fix=fix, var=kv * 500, gesamt=fix + kv * 500, kfs=fix / 500, kvs=kv, ks=fix / 500 + kv,
                ks700=fix / 700 + kv, ks300=fix / 300 + kv)
FV_UE1 = fv_ue1()
FV_UE2 = dict(var=D(3360) - D(2340), kvs=(D(3360) - D(2340)) / 120, ks=D(3360) / 120,
              k100=D(2340) + D("8.50") * 100, k150=D(2340) + D("8.50") * 150)
FV_P1 = [dict(kv=(D(118000) - D(154000)) / (D(8000) - D(12000))), ]
FV_P1 = dict(kv=(D(154000) - D(118000)) / D(4000), kf=D(118000) - D(9) * D(8000))
FV_P1b = dict(kv=(D(71000) - D(62000)) / D(1000), kf=D(71000) - D(9) * D(5000))
def fv_p2():
    benzin = D(7) * D("1.60") / 100 * 100     # € je 100 km
    oel = D("6.00") / 1000 * 100              # 1 l je 1.000 km zu 6,00 € → € je 100 km
    var100 = benzin + oel
    fix = D(240) + D(780) + D(40) * 12 + D(1300) + D(3900)
    return dict(benzin=benzin, oel=oel, var100=var100, fixj=fix, fixm=fix / 12, ges=fix + var100 * 400, jekm=(fix + var100 * 400) / 40000,
                pausch=(fix + var100 * D(520)) / 52000)
FV_P2 = fv_p2()

# db1 (Fjord 500: kv 63, Kf 6.000, Preis 99)
DB_E, DB_KV, DB_KF = D(99), FV_KV, FV_FIX
DB_DB = DB_E - DB_KV
DB_BEP = DB_KF / DB_DB
def db_gewinn(x):
    return DB_DB * x - DB_KF
DB_UE1 = dict(db=D(215) - D(96), erg=(D(215) - D(96)) * 400 - D(38000), bep=D(38000) / (D(215) - D(96)),
              db2=D(215) * D("0.8") - D(96), erg2=(D(215) * D("0.8") - D(96)) * 400 - D(38000), bep2=D(38000) / (D(215) * D("0.8") - D(96)))
DB_UE2 = dict(e=D(52), kv=D(25), kf=D(3100))
DB_UE2.update(db=DB_UE2["e"] - DB_UE2["kv"], bep=DB_UE2["kf"] / (DB_UE2["e"] - DB_UE2["kv"]))
DB_UE2.update(DB=DB_UE2["db"] * 250, gew=DB_UE2["db"] * 250 - DB_UE2["kf"], kv2=DB_UE2["kv"] * D("0.9"), kf2=DB_UE2["kf"] * D("0.85"))
DB_UE2["db2"] = DB_UE2["e"] - DB_UE2["kv2"]; DB_UE2["bep2"] = DB_UE2["kf2"] / DB_UE2["db2"]
DB_UE2["DB2"] = DB_UE2["db2"] * 250; DB_UE2["gew2"] = DB_UE2["DB2"] - DB_UE2["kf2"]
DB_P1 = dict(kv=(D("39900") - D("36120")) / 210, )
DB_P1["kf"] = D(39900) - DB_P1["kv"] * 1050
DB_P1["e"] = D(37800) / 1050; DB_P1["db"] = DB_P1["e"] - DB_P1["kv"]; DB_P1["bep"] = DB_P1["kf"] / DB_P1["db"]
DB_P1["max"] = DB_P1["db"] * 1400 - DB_P1["kf"]
DB_P2 = dict(bep=D(22032) / D("1.35"), ausl=D(22032) / D("1.35") / 20400 * 100, erg70=D("1.35") * (D(20400) * D("0.7")) - D(22032))
DB_P2["zus_db"] = (D("3.20") - D("2.80")) * 6000; DB_P2["zus_erg"] = DB_P2["zus_db"] - D(1400)
DB_P2["neu"] = DB_P2["erg70"] + DB_P2["zus_erg"]; DB_P2["ausl2"] = (D(20400) * D("0.7") + 6000) / 20400 * 100
DB_P3 = {}
for nm, e, kv, x in (("A", 32, 26, 1200), ("B", 58, 49, 1100), ("C", 118, 82, 2500)):
    DB_P3[nm] = dict(e=D(e), kv=D(kv), x=x, db=D(e) - D(kv), DB=(D(e) - D(kv)) * x)
DB_P3["erg"] = sum(v["DB"] for v in DB_P3.values() if isinstance(v, dict)) - D(90000)

# mehrstufige DB-Rechnung (Montelli): Produkte A1, A2 (Rucksäcke) | B1, B2 (Taschen) | C1 (Zubehör)
MS = {"A1": dict(e=D(220000), kv=D(98540), ef=D(51500)), "A2": dict(e=D(154800), kv=D(93500), ef=D(44000)),
      "B1": dict(e=D(216500), kv=D(87450), ef=D(79000)), "B2": dict(e=D(124500), kv=D(65200), ef=D(65000)),
      "C1": dict(e=D(255500), kv=D(95000), ef=D(71000))}
MS_GR = {"Rucksäcke": (["A1", "A2"], D(52500)), "Taschen": (["B1", "B2"], D(45000)), "Zubehör": (["C1"], D(21000))}
MS_UF = D(52000)
def ms():
    out = {k: dict(db1=v["e"] - v["kv"], db2=v["e"] - v["kv"] - v["ef"]) for k, v in MS.items()}
    gr = {}
    for g, (ps, gf) in MS_GR.items():
        gr[g] = dict(db2=sum(out[p]["db2"] for p in ps), db3=sum(out[p]["db2"] for p in ps) - gf)
    gesamt3 = sum(v["db3"] for v in gr.values())
    return out, gr, gesamt3, gesamt3 - MS_UF
MS_ERG = ms()
# E2: DB I gegeben
E2 = dict(db1={"P1": D(84000), "P2": D(160000), "P3": D(62500), "P4": D(38000), "P5": D(71000)},
          ef={"P1": D(8000), "P2": D(24000), "P3": D(9000), "P4": D(3000), "P5": D(12000)})
E2["db2"] = {k: E2["db1"][k] - E2["ef"][k] for k in E2["db1"]}
E2["g1"] = E2["db2"]["P1"] + E2["db2"]["P2"] - D(16000); E2["g2"] = E2["db2"]["P3"] + E2["db2"]["P4"] - D(10000); E2["g3"] = E2["db2"]["P5"]
E2["bA"] = E2["g1"] + E2["g2"] - D(30000); E2["bB"] = E2["g3"] - D(18000)
E2["erfolg"] = E2["bA"] + E2["bB"] - D(25000)


def haupt():
    print("=== zk1 · AS I Angebot (40 Stück) ===")
    for k in ("MGK", "MK", "FGK", "FK", "HK", "VwGK", "VtGK", "SK", "Gewinn", "BVP", "Skonto", "ZVP", "Rabatt", "LVP"):
        print(f"  {k:7} {eur(ZK1[k]):>12}   ×40 = {eur(ZK1[k] * 40):>14}")
    pruefe("zk1 SK", ZK1["SK"], "124.20"); pruefe("zk1 BVP", ZK1["BVP"], "149.04"); pruefe("zk1 LVP", ZK1["LVP"], "165.30")
    print("=== zk1 · Übung Sporttasche ===")
    for k in ("MGK", "MK", "FGK", "FK", "HK", "VwGK", "VtGK", "SK", "Gewinn", "BVP", "Skonto", "ZVP", "Rabatt", "LVP"):
        print(f"  {k:7} {eur(ZK1_UE[k]):>12}")
    pruefe("Sporttasche LVP", ZK1_UE["LVP"], "73.07")
    print("=== zk1 · Plus Messe-Rucksack (zwei Fertigungsstufen) ===")
    for k, v in ZK1_P1.items():
        print(f"  {k:7} {eur(v):>12}")
    pruefe("Messe LVP", ZK1_P1["LVP"], "135.02")
    print("=== zk1 · Plus Serie (500 Stück) ===")
    for k, v in ZK1_P2.items():
        print(f"  {k:10} {zahl(v)}")
    print("=== zk2 · Nachkalkulation (40 Stück) ===")
    for k, v in ZK2.items():
        print(f"  {k:10} {zahl(v)}")
    pruefe("zk2 SK Ist", ZK2["SK"], "4975.61"); pruefe("zk2 Gewinn Ist", ZK2["Gewinn"], "985.99")
    print("  Vorkalkulation SK ×40:", eur(ZK1["SK"] * 40), "· Gewinn:", eur(ZK1["Gewinn"] * 40), "· Abweichung:", eur(ZK2["Gewinn"] - ZK1["Gewinn"] * 40))
    print("=== zk2 · Übung (30 Messerucksäcke) ===")
    print("  Vor: " + ", ".join(f"{k} {zahl(v * 30)}" for k, v in ZK2_UE_V.items()))
    print("  Nach:", ", ".join(f"{k} {zahl(v)}" for k, v in ZK2_UE_N.items()))
    print("=== zk2 · Plus (Sporttasche Ist) ===")
    print("  ", ", ".join(f"{k} {zahl(v)}" for k, v in ZK2_PLUS.items()))
    print("=== zk3 · AS III Sondereinzelkosten ===")
    for k in ("MGK", "MK", "FGK", "SEKF", "FK", "HK", "VwGK", "VtGK", "SEKV", "SK", "Gewinn", "BVP", "Skonto", "ZVP", "Rabatt", "LVP"):
        print(f"  {k:7} {eur(ZK3[k]):>12}   ×50 = {eur(ZK3[k] * 50):>14}")
    pruefe("zk3 SK", ZK3["SK"], "133.88"); pruefe("zk3 LVP", ZK3["LVP"], "178.20")
    print("  Mehrpreis gegenüber ohne SEK:", eur(ZK3["LVP"] - ZK1["LVP"]), "· Stückgewinn mit SEK:", eur(ZK3["Gewinn"]), "vs", eur(ZK1["Gewinn"]))
    print("=== zk3 · Übung Sonderserie (100 Stück gesamt) ===")
    for k in ("MGK", "MK", "FGK", "FK", "HK", "VwGK", "VtGK", "SK", "Gewinn", "BVP", "Skonto", "ZVP", "Rabatt", "LVP"):
        print(f"  {k:7} {eur(ZK3_UE[k]):>12}")
    print("=== zk3 · Plus 1 (Angebotspreis = ZVP) ===")
    print("  ", ", ".join(f"{k} {zahl(v)}" for k, v in ZK3_P1.items()))
    print("=== zk3 · Plus 2 ===")
    print("  a)", ", ".join(f"{k} {zahl(v)}" for k, v in ZK3_P2A.items()))
    print("  b)", ", ".join(f"{k} {zahl(v)}" for k, v in ZK3_P2B.items()))
    print("=== fv1 ===")
    pruefe("kv", FV_KV, 63); pruefe("Kf", FV_FIX, 6000)
    for t in FV_TAB:
        print(f"  {t['x']:>4} St.: Kf {zahl(t['kfix'])} · Kv {zahl(t['kvar'])} · K {zahl(t['kg'])} · kf {zahl(t['kfs'])} · kv {zahl(t['kvs'])} · k {zahl(t['ks'])}")
    print("  Ü1:", ", ".join(f"{k} {zahl(v)}" for k, v in FV_UE1.items()))
    print("  Ü2:", ", ".join(f"{k} {zahl(v)}" for k, v in FV_UE2.items()))
    print("  P1a:", {k: zahl(v) for k, v in FV_P1.items()}, " P1b:", {k: zahl(v) for k, v in FV_P1b.items()})
    print("  P2:", {k: zahl(v, 4) for k, v in FV_P2.items()})
    print("=== db1 ===")
    pruefe("db", DB_DB, 36); pruefe("BEP", DB_BEP, "166.67")
    for x in (150, 200, 250):
        print(f"  {x} St.: DB {zahl(DB_DB * x)} · Ergebnis {zahl(db_gewinn(x))}")
    print("  Ü1:", {k: zahl(v) for k, v in DB_UE1.items()})
    print("  Ü2:", {k: zahl(v) for k, v in DB_UE2.items()})
    print("  P1:", {k: zahl(v) for k, v in DB_P1.items()})
    print("  P2:", {k: zahl(v) for k, v in DB_P2.items()})
    print("  P3:", {k: (v if not isinstance(v, dict) else {a: zahl(b) for a, b in v.items()}) for k, v in DB_P3.items()})
    print("  mehrstufig:", {k: {a: zahl(b) for a, b in v.items()} for k, v in MS_ERG[0].items()})
    print("   Gruppen:", {k: {a: zahl(b) for a, b in v.items()} for k, v in MS_ERG[1].items()}, "· DB IV gesamt", zahl(MS_ERG[2]), "· Erfolg", zahl(MS_ERG[3]))
    print("  E2:", {k: (zahl(v) if not isinstance(v, dict) else {a: zahl(b) for a, b in v.items()}) for k, v in E2.items()})
    pruefe("E1 Erfolg", MS_ERG[3], 50610); pruefe("E2 Erfolg", E2["erfolg"], 260500)
    print("\nGESAMT:", "alles ok" if ok else "FEHLER – bitte oben suchen")


if __name__ == "__main__":
    haupt()
