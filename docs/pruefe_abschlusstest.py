#!/usr/bin/env python3
"""Prüft die Formeln des Abschlusstests (fragen/abschlusstest.yaml) gegen eine zweite, unabhängige Rechnung (Decimal, kaufmännisch gerundet).
Aufruf (im Projektordner):  python3 docs/pruefe_abschlusstest.py <pfad-zum-baukasten>/skripte"""
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / ".claude/skills/lernpfad-baukasten/skripte"))
import moodle_xml as mx
import yaml

def r(x, n=2):
    return D(str(x)).quantize(D(1).scaleb(-n), rounding=ROUND_HALF_UP)

def pr(x, p):          # x * p / 100, gerundet
    return r(D(str(x)) * D(str(p)) / 100)

def ref(aid, w):
    w = {k: D(str(v)) for k, v in w.items()}
    if aid == "at-01":
        return dict(kurz=w["var"], mittel=w["var"] + w["fix"] * w["ausp"] / 100 / w["kap"], lang=w["var"] + w["fix"] / w["kap"], erg=(w["preis"] - w["var"]) * w["kap"] - w["fix"])
    if aid == "at-02":
        mek, fek, sekf, sekv = w["mek"], w["fek"], w["sekf"], w["sekv"]
        mgk, fgk = pr(mek, 5), pr(fek, 130); hk = mek + mgk + fek + fgk + sekf
        vw, vt = pr(hk, 10), pr(hk, 5); sk = hk + vw + vt + sekv
        vsk = mek + pr(mgk, 50) + fek + pr(fgk, 25) + sekf + pr(vw, 20) + pr(vt, 10) + sekv
        return dict(hk=hk, sk=sk, vsk=vsk, voll=(w["preis"] - sk) * w["menge"], db=(w["preis"] - vsk) * w["menge"])
    if aid in ("at-03", "at-08"):
        if aid == "at-03":
            mek, fek = w["mek"], w["fek"]
            hk = mek + pr(mek, 5) + fek + pr(fek, 130); sk = hk + pr(hk, 10) + pr(hk, 5); gew = w["gew"]
            out = dict(hk=hk)
        else:
            e = w["e"]; sk = e + pr(e, w["hk"]); gew = w["gew"]; out = {}
        bvp = sk + pr(sk, gew)
        zvp = bvp + r(bvp * w["skonto"] / (100 - w["skonto"])); lvp = zvp + r(zvp * w["rabatt"] / (100 - w["rabatt"]))
        out.update(sk=sk, bvp=bvp, lvp=lvp)
        if aid == "at-08":
            out["faktor"] = lvp / w["e"]
        return out
    if aid == "at-04":
        mek, fek = w["mek"], w["fek"]
        hk = mek + pr(mek, w["mgk"]) + fek + pr(fek, w["fgk"]); sk = hk + pr(hk, w["vw"]) + pr(hk, w["vt"])
        return dict(hk=hk, sk=sk, gewinn=w["bvp"] - sk, gp=(w["bvp"] - sk) / sk * 100)
    if aid == "at-05":
        k = lambda x: w["fix"] + w["var"] * x
        return dict(k1=k(w["x1"]), s1=k(w["x1"]) / w["x1"], f2=w["fix"] / w["x2"], s2=k(w["x2"]) / w["x2"])
    if aid == "at-06":
        kv = w["dk"] / w["dm"]
        return dict(kv=kv, kf=w["k1"] - kv * w["m1"])
    if aid == "at-07":
        db = w["preis"] - w["var"]; bep = (w["fix"] / db).to_integral_value(rounding="ROUND_CEILING")
        return dict(db=db, bep=bep, ausl=bep / w["kap"] * 100, gew=db * w["kap"] - w["fix"])
    if aid == "at-09":
        zvp = w["lvp"] - pr(w["lvp"], w["rabatt"]); bvp = zvp - pr(zvp, w["skonto"])
        sk = bvp * 100 / (100 + w["gew"]); emax = sk / (1 + w["hk"] / 100)
        sk_ist = w["e"] + pr(w["e"], w["hk"])
        return dict(bvp=bvp, sk=sk, emax=emax, g=bvp - sk_ist, gp=(bvp - sk_ist) / sk_ist * 100)

fragen = yaml.safe_load(open("fragen/abschlusstest.yaml", encoding="utf-8"))
fehler = n = 0
for a in fragen:
    for w in mx.zahl_varianten(a, 12):
        ergebnis = dict(w)
        soll = ref(a["id"], w)
        for ant in a["antworten"]:
            x = mx.runde(mx.berechne(ant["formel"], ergebnis), ant.get("runden", 0))
            ergebnis[ant["id"]] = x
            tol = ant.get("toleranz", 0)
            erwartet = float(r(soll[ant["id"]], ant.get("runden", 0)))
            n += 1
            if abs(x - erwartet) > tol + 1e-9:
                fehler += 1
                print(f"✗ {a['id']} {ant['id']}: Formel {x} ≠ Referenz {erwartet} (Parameter {w})")
print(f"{n} Antworten über {len(fragen)} Aufgaben je 12 Varianten geprüft –", "alles ok" if not fehler else f"{fehler} Abweichungen")
# Referenzfälle aus den Rechenproben (pu2, zk1)
w = dict(mek=24, fek=36, sekf=4.5, sekv=1.8, menge=300, preis=118)
e = dict(w)
for ant in fragen[1]["antworten"]:
    e[ant["id"]] = mx.runde(mx.berechne(ant["formel"], e), ant.get("runden", 0))
assert (e["sk"], e["vsk"], e["voll"], e["db"]) == (131.18, 81.41, -3954.0, 10977.0), e
w = dict(mek=24, fek=36, gew=20, skonto=2, rabatt=8)
e = dict(w)
for ant in fragen[2]["antworten"]:
    e[ant["id"]] = mx.runde(mx.berechne(ant["formel"], e), ant.get("runden", 0))
assert (e["sk"], e["bvp"], e["lvp"]) == (124.2, 149.04, 165.3), e
print("Referenzfälle pu2 (131,18 / 81,41 / −3.954 / 10.977) und zk1 (124,20 / 149,04 / 165,30) stimmen.")
