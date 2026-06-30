---
tags:
  - vault-health
  - decision-matrix
  - meta
type: decision-matrix
created: 2026-06-30
# --- Gewichtungen (Summe sollte 1.0 ergeben) ---
weight_nutzen: 0.30
weight_aufwand: 0.20
weight_risiko: 0.20
weight_privacy: 0.15
weight_wartung: 0.15
---

# Vault Health & Routinen-Priorisierung (Weighted Scoring Model)

> [!info] Live-Anpassung
> Ändere die `weight_*`-Werte im Frontmatter oben — die Tabelle unten rechnet automatisch neu.
> Rohdaten (Scores 1-10 je Kriterium) stehen direkt im DataviewJS-Block und können dort angepasst werden.

## Kriterien-Übersicht

| Kriterium | Gewicht | Bedeutung (10 = optimal) |
|---|---|---|
| Nutzen | `= this.weight_nutzen` | Täglicher/wöchentlicher Mehrwert |
| Aufwand | `= this.weight_aufwand` | 10 = sehr einfach umsetzbar |
| Risiko | `= this.weight_risiko` | 10 = ungefährlich bei Fehlern |
| Privacy | `= this.weight_privacy` | 10 = unkritischer Datenzugriff |
| Wartung | `= this.weight_wartung` | 10 = wartungsfrei |

```dataviewjs
const p = dv.current();
const W = {
    nutzen:  p.weight_nutzen,
    aufwand: p.weight_aufwand,
    risiko:  p.weight_risiko,
    privacy: p.weight_privacy,
    wartung: p.weight_wartung
};

const sumW = Object.values(W).reduce((a,b) => a+b, 0);
if (Math.abs(sumW - 1.0) > 0.01) {
    dv.paragraph(`> ⚠️ **Achtung:** Gewichte summieren sich auf ${sumW.toFixed(2)} statt 1.0 — Scores sind nicht direkt vergleichbar.`);
}

// --- Rohdaten: hier anpassen ---
const items = [
    { name: "B – Morning Synthesis",        kategorie: "Routine",  nutzen: 9, aufwand: 8, risiko: 8, privacy: 7, wartung: 8 },
    { name: "D – Weekly Review",             kategorie: "Routine",  nutzen: 7, aufwand: 8, risiko: 9, privacy: 6, wartung: 9 },
    { name: "C – Meeting/Content Processor", kategorie: "Routine",  nutzen: 8, aufwand: 7, risiko: 7, privacy: 6, wartung: 7 },
    { name: "F – Vault Health Check",        kategorie: "Routine",  nutzen: 5, aufwand: 6, risiko: 8, privacy: 7, wartung: 8 },
    { name: "A – Nächtliche Bereinigung",    kategorie: "Routine",  nutzen: 8, aufwand: 4, risiko: 3, privacy: 4, wartung: 4 },
    { name: "E – Cross-Pollinator/Kickoff",  kategorie: "Routine",  nutzen: 4, aufwand: 3, risiko: 6, privacy: 5, wartung: 5 },
    { name: "Single-Vault (Tags/Ordner)",    kategorie: "Architektur", nutzen: 6, aufwand: 8, risiko: 8, privacy: 5, wartung: 8 },
    { name: "Multi-Vault (Personal/Work/Learning)", kategorie: "Architektur", nutzen: 8, aufwand: 3, risiko: 5, privacy: 9, wartung: 3 },
];

const rows = items.map(it => {
    const score = it.nutzen*W.nutzen + it.aufwand*W.aufwand + it.risiko*W.risiko
                + it.privacy*W.privacy + it.wartung*W.wartung;
    return { ...it, score: Math.round(score * 100) / 100 };
}).sort((a,b) => b.score - a.score);

dv.header(3, "Ergebnis (live berechnet)");
dv.table(
    ["Rang", "Item", "Kategorie", "Nutzen", "Aufwand", "Risiko", "Privacy", "Wartung", "Score"],
    rows.map((r, i) => [
        i + 1,
        r.name,
        r.kategorie,
        r.nutzen, r.aufwand, r.risiko, r.privacy, r.wartung,
        r.score.toFixed(2)
    ])
);
```

## Interpretationshilfe

| Score-Bereich | Bedeutung | Aktion |
|---|---|---|
| ≥ 7,5 | Hochpriorisiert | Sofort implementieren |
| 6,0 – 7,4 | Solide | In nächste Phase aufnehmen |
| 4,5 – 5,9 | Mit Vorbehalt | Nur mit Risiko-Mitigation umsetzen |
| < 4,5 | Zurückstellen | Aufwand/Nutzen-Verhältnis schlecht |

## Changelog

- 2026-06-30: Initiale Matrix erstellt, basierend auf Vergleich des "AI-Powered Second Brain"-Workflows.

---
*Hinweis: Diese Datei ist als portables Artefakt gedacht. Um sie aktiv mit Dataview zu nutzen, kopiere sie in deinen Obsidian Vault, z. B. nach `00 - Meta/` oder `03 - Resources/Frameworks/`. Benötigt das Dataview-Plugin (mit aktiviertem JavaScript-Query-Support unter Einstellungen → Dataview → Enable JavaScript Queries).*
