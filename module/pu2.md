---
titel: "Preisuntergrenzen II: Unausgelastete Kapazitäten – Zusatzauftrag annehmen?"
minuten: 150
review: entwurf
datei: pu2.html
lernziele:
  - Selbstkosten für einen Auftrag mit Sondereinzelkosten kalkulieren,
  - einen Auftrag auf Vollkostenbasis und auf Teilkostenbasis beurteilen,
  - die kurzfristige, die liquiditätsorientierte und die langfristige Preisuntergrenze bestimmen,
  - begründet entscheiden, ob ein Zusatzauftrag unter den Selbstkosten angenommen wird.
quellen: [q-arbeitsbuch, q-modell]
kurzcheck:
  - typ: zahl
    frage: "Ein Auftrag bringt 52,00 € je Stück. Die variablen Selbstkosten betragen 38,40 €, die Selbstkosten 61,20 €. Wie hoch ist der Stückdeckungsbeitrag?"
    loesung: 13.6
    einheit: "€"
    richtig_text: "Richtig: 52,00 € − 38,40 € = 13,60 €. Du rechnest mit den variablen Selbstkosten, nicht mit den Selbstkosten."
    falsch_text: "Der Stückdeckungsbeitrag ist der Preis minus die variablen Kosten (nicht minus die Selbstkosten)."
  - typ: luecken
    frage: Ergänze die Zusammenfassung.
    text: "Die {{a}}rechnung unterscheidet nicht zwischen fixen und variablen Kosten. Sie ist ungeeignet, wenn {{b}} Entscheidungen zur Kapazitätsauslastung getroffen werden müssen."
    luecken:
      a: {akzeptiert: [Vollkosten], hinweis: "Voll- oder Teil…?"}
      b: {akzeptiert: [kurzfristige, kurzfristig], hinweis: "kurz- oder langfristig?"}
  - frage: "Die Fertigung ist nicht ausgelastet. Ein Kunde bietet einen Preis zwischen der kurzfristigen und der langfristigen Preisuntergrenze. Was spricht für die Annahme?"
    antworten:
      - "Der Auftrag liefert einen positiven Deckungsbeitrag, und die Fixkosten fallen ohnehin an."
      - "Der Auftrag liefert einen Gewinn auf Vollkostenbasis."
      - "Der niedrige Preis bleibt dem restlichen Markt verborgen."
    richtig: 1
    richtig_text: "Genau. Gegen die Annahme können trotzdem Nebenwirkungen sprechen, zum Beispiel das Preisimage."
    falsch_text: "Denke an den Deckungsbeitrag: Er verbessert das Betriebsergebnis, solange die Fixkosten ohnehin anfallen."
  - typ: zahl
    frage: "Variable Stückkosten: 30,00 €. Ausgabenwirksame Fixkosten: 4.000,00 € bei 500 Stück. Wie hoch ist die liquiditätsorientierte (mittelfristige) Preisuntergrenze?"
    loesung: 38
    einheit: "€"
    richtig_text: "Richtig: 30,00 € + 4.000 € : 500 Stück = 38,00 €."
    falsch_text: "Variable Stückkosten plus die ausgabenwirksamen fixen Kosten je Stück (Fixkosten : Menge)."
---
## 1. Ausgangssituation

:::situation Ausgangssituation: Unausgelastete Kapazitäten – sollen wir den Zusatzauftrag annehmen?
Auf dem Abteilungsleitermeeting der Montelli GmbH wird diese Anfrage besprochen:

> **Nordlicht Versicherung AG, Kiel**
> An die Montelli GmbH, z. Hd. Merle Dahl
>
> Sehr geehrte Frau Dahl,
> im Rahmen unserer Kampagne „Gesund zur Arbeit“ möchten wir unsere Außendienstmitarbeiter mit einem Rucksack ausstatten. Gern hätten wir Ihren **„Business Deluxe“**, mit unserem Firmenlogo bestickt und in unserer Geschenkverpackung.
> In einem ersten Schritt würden wir bis Ende Februar **300 Rucksäcke** abnehmen. Ein Folgeauftrag über **600 Rucksäcke** bis Mai wäre denkbar.
> Da wir mit anderen Herstellern sprechen, können wir einen Preis von **höchstens 118,00 €** je Rucksack akzeptieren.
> Bitte senden Sie uns ein verbindliches Angebot.

**Merle Dahl** (Verkauf): „Eine interessante Anfrage. Aber unser Listenpreis liegt bei **165,00 €**. Der Kunde will deutlich weniger zahlen.“

**Tobias Brandt** (Controlling): „Ich glaube, schon unsere Selbstkosten liegen bei diesem Auftrag über 118,00 €. Wir würden bei der Annahme Verlust machen.“

**Jonas Albers** (Fertigung): „Im Januar und Februar ist unsere Fertigung nicht ausgelastet. Den Auftrag könnte ich gut gebrauchen, um die Fixkosten zu decken.“
:::

## 2. Aufgaben: Auf Vollkostenbasis entscheiden

:::aufgabe basis 10 Aufgabe 1 · Die Anfrage zusammenfassen
Fasse die wichtigsten Informationen aus der Ausgangssituation in eigenen Worten zusammen.

:::hilfe 💡 Tipp
Beantworte: Wer will was, in welcher Menge, bis wann und zu welchem Preis? Was spricht dafür, was dagegen?
:::
:::

:::aufgabe basis 25 Aufgabe 2 · Die Selbstkosten kalkulieren
Kalkuliere mit den Zahlen des Controllings die **Selbstkosten** für diesen Auftrag, je Stück und für 300 Stück. Runde die einzelnen Zeilen je Stück auf Cent. Die Zahlen für 300 Stück erhältst du, indem du die Werte je Stück mit 300 multiplizierst.

| Angabe | Wert |
| --- | --- |
| Materialeinzelkosten (MEK) | 24,00 € |
| Fertigungseinzelkosten (FEK) | 36,00 € |
| Sondereinzelkosten der Fertigung (Logostickerei) | 4,50 € |
| Sondereinzelkosten des Vertriebs (Geschenkverpackung) | 1,80 € |
| Materialgemeinkostenzuschlag (MGKZS) | 5,0 % |
| Fertigungsgemeinkostenzuschlag (FGKZS) | 130,0 % |
| Verwaltungsgemeinkostenzuschlag (VwGKZS) | 10,0 % |
| Vertriebsgemeinkostenzuschlag (VtGKZS) | 5,0 % |

:::rechenraum 12
Kalkulationsschema (je Stück und 300 Stück)
:::

:::hilfe 💡 Tipp
Das Schema kennst du aus der Zuschlagskalkulation: MEK + MGK = Materialkosten, FEK + FGK + Sondereinzelkosten der Fertigung = Fertigungskosten. Verwaltungs- und Vertriebsgemeinkosten rechnest du auf die **Herstellkosten**. Die Sondereinzelkosten des Vertriebs addierst du am Schluss. Hilfe findest du in [Zuschlagskalkulation: Angebot kalkulieren](modul:zk1) und [Sondereinzelkosten](modul:zk3).
:::

:::hilfe 🧮 Zwischenergebnisse zum Prüfen
Materialkosten 25,20 €, Fertigungskosten 87,30 €, Herstellkosten 112,50 €.
:::
:::

:::aufgabe basis 10 Aufgabe 3 · Gewinn oder Verlust?
Berechne den **Gewinn bzw. Verlust**, wenn der Auftrag zu **118,00 € je Stück** angenommen wird, je Stück und insgesamt für 300 Stück.

:::rechenraum 5
Rechenraum zu Aufgabe 3
:::
:::

:::aufgabe basis 10 Aufgabe 4 · Entscheidung auf Vollkostenbasis
Triff aufgrund deiner Rechnung auf **Vollkostenbasis** eine Entscheidung: Sollte die Montelli GmbH den Auftrag annehmen?

:::rechenraum 4
Deine Entscheidung
:::
:::

## 3. Info: Zuschlagskalkulation mit variablen Kosten

:::info Info 3 · Zuschlagskalkulation mit variablen Kosten
Die Zuschlagskalkulation berücksichtigt **alle** Kosten. Sie rechnet auch die **fixen Gemeinkosten** mit Zuschlagssätzen auf die Produkte.

Wenn die Fertigung nicht ausgelastet ist, brauchst du zusätzlich eine Rechnung, die nur die **variablen Kosten** enthält. Dafür gilt:

- **Einzelkosten** sind immer zu **100 % variabel**: Sie entstehen nur, wenn produziert wird.
- Bei den **Gemeinkosten** gibt dir das Controlling an, wie viel Prozent **variabel** sind.

So rechnest du die variablen Gemeinkosten: Nimm die Gemeinkosten aus der Vollkostenrechnung und berechne davon den variablen Anteil.

Beispiel: Materialeinzelkosten 50,00 €, MGKZS 6 % → MGK 3,00 €. Sind 40 % der MGK variabel, ergeben sich variable MGK von 1,20 €. Variable Materialkosten: 50,00 € + 1,20 € = 51,20 €.

So geht es weiter durch das ganze Schema: Am Ende stehen die **variablen Selbstkosten**. Sie sind die Grundlage der **kurzfristigen Preisuntergrenze**.
:::

## 4. Aufgaben: Mit der Teilkostenrechnung überprüfen

:::aufgabe basis 25 Aufgabe 5 · Die Entscheidung überprüfen
Überprüfe deine Entscheidung mit der **Teilkostenrechnung**. Das Controlling teilt dir mit: Die Material- und die Fertigungsgemeinkosten sind zu **50 % bzw. 25 %** variabel, die Verwaltungs- und Vertriebsgemeinkosten zu **20 % bzw. 10 %**. Sämtliche Einzelkosten sind zu **100 %** variabel.

Berechne die **variablen Selbstkosten** je Stück und für 300 Stück sowie den **Deckungsbeitrag** bei einem Preis von 118,00 €.

:::rechenraum 12
Teilkostenrechnung (je Stück und 300 Stück)
:::

:::hilfe 💡 Tipp
Gehe das Schema von oben durch. Die variablen Gemeinkosten sind jeweils der angegebene Prozentsatz der Gemeinkosten aus Aufgabe 2. Hilfe zum Deckungsbeitrag: [Deckungsbeitrag und Break-even](modul:db1).
:::

:::hilfe 🧮 Zwischenergebnisse zum Prüfen
Variable Materialkosten 24,60 €, variable Fertigungskosten 52,20 €, variable Herstellkosten 76,80 €.
:::
:::

:::aufgabe basis 10 Aufgabe 6 · Preisuntergrenzen
Bestimme die **kurzfristige** und die **langfristige Preisuntergrenze** für diesen Auftrag.

:::rechenraum 4
Preisuntergrenzen
:::
:::

:::aufgabe basis 20 Aufgabe 7 · Soll die Montelli GmbH den Auftrag annehmen?
Diskutiere, ob die Montelli GmbH die Anfrage der Nordlicht Versicherung AG positiv beantworten und die Rucksäcke produzieren sollte. Nenne mindestens **zwei Gründe dafür** und **zwei Gründe dagegen** und komme zu einer begründeten Entscheidung.

:::rechenraum 8
Pro und Contra
:::

:::hilfe 💡 Tipp
Denke an: Deckungsbeitrag, freie Kapazität im Winter, Folgeauftrag, aber auch an die Händler, die 165,00 € zahlen, und an ein neues Kundensegment.
:::
:::

## 5. Info: Preisuntergrenzen im Überblick

:::kasten Zusammenfassung
| Preisuntergrenze | Formel |
| --- | --- |
| Kurzfristig | variable Stückkosten |
| Liquiditätsorientiert (mittelfristig) | variable Stückkosten + ausgabenwirksame fixe Stückkosten |
| Langfristig | gesamte Stückkosten (variable + fixe) |

Die Vollkostenrechnung ist ungeeignet, wenn **kurzfristig** über die Auslastung oder das Betriebsergebnis entschieden wird. Dann rechnest du mit der **Teilkostenrechnung**.
:::

## 6. Übung: Die Rechnung selbst anwenden

:::aufgabe basis 20 Übung 1 · Drei Preisuntergrenzen
Die Montelli GmbH stellt auf einer Anlage die **Messe-Tasche „Express“** her. Monatliche Daten:

| Angabe | Wert |
| --- | --- |
| Kalkulatorische Abschreibungen | 1.800,00 € |
| Kalkulatorische Zinsen | 900,00 € |
| Versicherungskosten | 120,00 € |
| Gehaltskosten für die Überwachung der Anlage | 2.400,00 € |
| Materialverbrauch | 14,60 € je Stück |
| Lohnkosten | 6,40 € je Stück |

Die maximale Kapazität beträgt **600 Stück** monatlich. Der Listenverkaufspreis liegt bei **34,90 €**. Berechne

a) die kurzfristige Preisuntergrenze,

b) die liquiditätsorientierte (mittelfristige) Preisuntergrenze,

c) die langfristige Preisuntergrenze.

:::rechenraum 8
Rechenraum zu Übung 1
:::

:::hilfe 💡 Tipp
Welche der vier Fixkosten sind ausgabenwirksam? Kalkulatorische Abschreibungen und Zinsen sind keine Ausgaben.
:::
:::

:::aufgabe basis 25 Übung 2 · Teilkostenschema
Die Montelli GmbH kalkuliert den Rucksack **„Daypack Basic“** auf Vollkosten- und Teilkostenbasis. Die Material- und die Fertigungsgemeinkosten sind zu **60 % bzw. 50 %**, die Verwaltungs- und Vertriebsgemeinkosten zu **25 % bzw. 15 %** variabel. Die Einzelkosten sind zu 100 % variabel.

| Angabe | Wert |
| --- | --- |
| Materialeinzelkosten | 14,00 € |
| Fertigungseinzelkosten | 11,00 € |
| MGKZS / FGKZS | 5,0 % / 130,0 % |
| VwGKZS / VtGKZS | 8,0 % / 4,0 % |

a) Vervollständige das Kalkulationsschema auf Vollkosten- und Teilkostenbasis (Selbstkosten und variable Selbstkosten).

b) Bestimme die langfristige Preisuntergrenze.

c) Bestimme die kurzfristige Preisuntergrenze.

:::rechenraum 12
Schema: Vollkosten und Teilkosten
:::
:::

:::aufgabe plus 25 Plus · Rabattwunsch eines Discounters
Die Montelli GmbH fertigt monatlich **800 Rucksäcke „Office Slim“** (Kapazitätsauslastung 80 %). Dabei entstehen variable Kosten von **36.000,00 €**. Die fixen Kosten betragen **22.000,00 €**, davon sind **12 %** ausgabenwirksam. Der Listenverkaufspreis beträgt **95,00 €** netto.

Zur Verbesserung der Auslastung könnte Montelli einen Auftrag eines Discounters über **100 Rucksäcke** monatlich annehmen. Der Discounter verlangt **20 % Rabatt** auf den Listenpreis.

a) Triff eine begründete Entscheidung, ob Montelli den Auftrag annehmen soll.

b) Berechne die mittelfristige und die langfristige Preisuntergrenze bei **voller Kapazitätsauslastung** (1.000 Stück).

:::rechenraum 10
Rechenraum zur Plus-Aufgabe
:::
:::

## 7. Zum Schluss

:::achtung Typische Fehler
- **Mit den Selbstkosten statt mit den variablen Selbstkosten rechnen**, wenn der Deckungsbeitrag gefragt ist.
- **Den Zuschlag auf die falsche Basis rechnen:** Verwaltungs- und Vertriebsgemeinkosten beziehen sich auf die **Herstellkosten**.
- **Die langfristige Untergrenze zu hoch ansetzen:** Sie besteht aus den variablen Stückkosten **plus allen fixen Kosten je Stück**. Die ausgabenwirksamen Fixkosten sind darin schon enthalten.
- **Nur auf die Zahlen schauen:** Ein Zusatzauftrag unter Vollkosten kann Nebenwirkungen haben (Preisimage, Händler, Folgeaufträge).
:::

:::kurzcheck
:::
