# Preiskalkulation – Lernpfad (BGW24a, Jahrgang 13)

Lernpfad zu **Absatzprozesse › Preispolitik** mit der Modellfirma **Montelli GmbH**. Kern ist die **Bestimmung von
Preisuntergrenzen** (Lernsituation 15). Dazu kommen Wiederholungen (Zuschlagskalkulation, fixe und variable Kosten,
Deckungsbeitrag und Break-even) und als neues Thema die Handelskalkulation. Ziel: Moodle 4.5 (BBZ) und Web-Version.

## Aufbau

| Stufe | Module | Zeit (Basis) | Zugang in Moodle |
| --- | --- | --- | --- |
| 🎯 Kern: Preisuntergrenzen | `pu1`, `pu2`, `pum` ★ | 390 min | nacheinander, Meilenstein am Ende |
| 🔁 Wiederholung | `zk1`, `zk2`, `zk3`, `fv1`, `db1` | 255 min | von Anfang an offen, freie Reihenfolge |
| 🛒 Neu: Handelskalkulation | `hk1`, `hk2` | 130 min | nach dem Meilenstein |

Stand: **Stufe 1 ist geschrieben (alle Module noch `review: entwurf`)**, die Module der Stufen 2 und 3 sind Platzhalter.

## Ordner

- `kurs.yaml` Kursbeschreibung · `module/` Module · `loesungen/` Lösungen (nur als PDF in Moodle, verborgen)
- `quellen.yaml` Quellen · `material/` Logo · `docs/rechenprobe-stufe1.py` Rechenprobe aller Zahlen der Stufe 1
- `ausgabe/` wird erzeugt (nicht im Repo)

## Bauen

Mit dem Skill **lernpfad-baukasten** (Branch `claude/busy-pascal-ez2bhb` im Repo `lernpfad-baukasten`; dort sind PDF-Export,
Erkunden-Grafik, Datei-Aktivität und das Design `bbz-blau` entstanden):

```bash
python3 <skill>/skripte/pruefen.py .
python3 <skill>/skripte/alles.py . --entwuerfe     # Testkurs mit Entwürfen
python3 docs/rechenprobe-stufe1.py                 # alle Zahlen gegenrechnen
```

Nur Module mit `review: freigegeben` kommen in den Moodle-Kurs für die Klasse. Freigeben kann nur die Lehrkraft.

## Urheberrecht

Aufgabentypen, die Reihenfolge der Arbeitsaufträge und die Rechenwege orientieren sich am Arbeitsbuch (© Westermann, Lernsituationen 7, 8,
13–15). Alle Texte, Fälle und Zahlen sind eigene Texte mit dem Modellunternehmen Montelli GmbH. Das Buch wird nicht abgedruckt.
