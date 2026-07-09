# LinkedIn Post 9 — Wie ich einen Workshop rette

---

10:47 Uhr. Der Workshop kippt.

Sechs Leute im Raum. Ein Tier-1-Zulieferer, zwei Qualitätsverantwortliche,
ein Safety Manager – und die Stimmung in etwa so warm wie ein Kühlschrank.

Thema: Dürfen wir pytest, coverage.py und pylint in einem ASPICE-Projekt
einsetzen? Oder nicht?

Der Quality-Lead lehnt sich zurück, verschränkt die Arme und sagt den
einen Satz, der jeden Open-Source-Vorstoß im Automotive killt:

„Schön. Aber wo ist das Nachweisdokument? Was zeigen wir dem Assessor?"

Stille.

Der Entwickler neben mir kennt seine Tools in- und auswendig.
Testabdeckung? 94 %. Unit Tests? Grün. Alles sauber.
Nur: Er hat kein einziges Blatt Papier, das ein ASPICE-Assessor
anfassen würde. Kein SWE.4 Work Product. Keine Traceability.
Keine Argumentationskette.

Und genau da kippt jeder dieser Workshops. Nicht an der Technik.
An der Compliance-Lücke.

---

Was ich in dem Moment gemacht habe:

Ich habe nicht über Tools diskutiert. Ich habe das Problem umgedreht.

„Vergesst kurz, welches Tool das erzeugt hat. Was genau will der
Assessor sehen?"

Wir haben es an die Wand geschrieben:
→ Welche Base Practice? (SWE.4 BP1, BP3, BP4)
→ Welches Evidence-Artefakt?
→ Welche Traceability zur Anforderung?

Dann haben wir genau EINEN pytest-Report genommen und ihn live
in ein ASPICE-konformes SWQ-Nachweisdokument übersetzt.
Base Practice für Base Practice. Vor ihren Augen.

Nach 20 Minuten lag ein Dokument auf dem Tisch, das der Safety Manager
tatsächlich angefasst hat. Der Quality-Lead – immer noch skeptisch –
sagte: „Okay. DAS kann ich einem Assessor vorlegen."

Workshop gerettet. Nicht durch ein besseres Tool.
Durch die fehlende Schicht dazwischen.

---

Die Lektion, die ich aus jedem dieser Termine mitnehme:

Open-Source-Tools scheitern im regulierten Automotive fast nie an der
technischen Qualität. Sie scheitern daran, dass sie keine prüffähigen
Nachweise erzeugen. Kein ASPICE-Mapping. Keine Safety-Argumentation.

Die Qualitäts- und Legal-Teams blockieren – zu Recht.
Und das Projekt fällt zurück auf teure proprietäre Toolchains.

Diese eine fehlende Schicht ist der ganze Unterschied zwischen
„interessantes Tool" und „im Serienprojekt freigegeben".

Genau die baue ich – als offene Compliance-Brücke:
pytest, coverage.py, pylint → ASPICE Work Products (SWA, SWQ, SWV),
inklusive Traceability und Assessor-fähigem Evidence.

Wenn dein Team gerade versucht, Open Source an einem Safety-Audit
vorbeizubekommen: Das ist exakt das Problem, an dem ich arbeite.

Wie oft ist bei euch ein Tool nicht an der Technik gescheitert,
sondern am fehlenden Nachweis? 👇

---

#ASPICE #ISO26262 #AutomotiveSoftware #FunctionalSafety #OpenSource
#SoftwareQuality #Compliance #Tooling
