# Prompt Engineering Methodology — Mastery Level

*Applies to: every prompt template in `prompts/` and the `reqa-hwe` analysis skill.*
*Scope: ASPICE v4.0 · ISO 26262:2018 · supplier governance · audit-evidence output.*
*Status: normative for this repository — a prompt change that violates these
principles should be rejected in review.*

---

## Why standard prompting advice fails here

| Generic advice | Beginner assumption | Reality in a compliance context |
|---|---|---|
| "Be specific" | More detail = better answer | Detail without structure = noise; the auditor cannot parse it |
| "Give context" | Paste a context block | The *wrong* context (a generic ASPICE definition) pollutes the result |
| "Use few-shot examples" | Show 2–3 examples | Without a **falsification criterion** the output is a roulette |
| "Iterate" | Feedback loop | Unstructured feedback makes the model circle; the feedback must itself be structured |

The prompt is the **spec**; the model is the **executor**. You are not writing for
the model — you are writing for your future peer review and for an ISO assessor who
will read the output cold.

---

## The 7 principles

### 1. Constitutional Framing
Declare role, experience, and zero-tolerance boundaries **before** the task. The
analyzer prompts open with a fixed auditor identity (15+ yr OEM supplier governance,
PWR architecture, FMEDA sign-off) and an explicit error-cost signal (EUR 50k–500k
rework). Effect: the model calibrates on *precision > volume* and produces
audit-evidence, not advisory prose.

### 2. Context Completeness Check (the safety gate)
Before sending, answer 5 questions internally. Any NO → fix before proceeding:

1. Is the specific role clear?
2. Is the acceptable output format known (can I parse / review / import it)?
3. Are falsification criteria stated (how do I tell WRONG from RIGHT)?
4. Is the task context under ~800 tokens (TSR-compressed)?
5. Is there at least one negative example / declared constraint?

### 3. TSR — Task-Specific Relevance
Only context that **changes this specific task** is valid input. The specific
SYS-REQ, the specific failure mode, the specific HARD constraint — yes. A
Wikipedia-paste of ISO 26262 — no. Generic context moves the model into
information-mode; TSR-compressed context keeps it in problem-solving-mode.

### 4. Falsification-First (inverted logic)
Do not ask "how should this be written?" Ask "under what conditions is this artifact
WRONG or INSUFFICIENT?" The output is a **list of gaps**, each with a failure
scenario and a standard link — not a polished rewrite. This is what catches the
defect an auditor would catch.

```
[Gap N: Title]
- Observation: [what is insufficient or absent]
- Failure scenario: [under what condition this gap causes a problem]
- Standard link: [ISO 26262 / ASPICE clause or BP]
- Evidence in current artifact: [exact text or "not mentioned"]
- Minimal fix: [2-5 words — not "improve the description"]
- Better language: [concrete replacement text]
```

### 5. Evidence-Artifact Orientation
Write the prompt as if the answer is read tomorrow by an ISO assessor. Output uses a
fixed audit structure: **Findings** (severity + evidence + standard link +
remediation), **Traceability status**, **Open items** (supplier-owned vs OEM-owned),
and a **Self-assessment** (confidence + assumptions + conditions under which the
analysis is wrong).

### 6. Constraint-Stacking ("NO" before "YES")
State what is **not** possible before asking what is optimal. Classify every
constraint as **HARD** (physically/contractually non-negotiable) or **SOFT**
(overridable with documented justification). "Multiple approaches are possible" is a
symptom of undeclared HARD constraints — diagnose it, do not output it.

### 7. Iterative Falsification Loop
A prompt is a series of hypothesis tests, not a single shot:

```
ITER 0  model presents solution / gap list
ITER 1  "Under which audit scenario does this FAIL?"        → gaps A, B, C
ITER 2  "Gap A is impossible because [HARD constraint]"     → re-focus on real B, C
ITER 3  "For Gap B: which ISO clause?"                       → cite, or "interpretive → supplier input"
ITER 4  close (revise artifact) or escalate (supplier ticket)
```
"Das stimmt nicht" is not evidence. "Das stimmt nicht, weil Constraint XYZ gilt" is
evidence — only the latter triggers a revision.

---

## The Prompt Regression Test (run before shipping any prompt)

Score 1 point per passed check. Ship at ≥ 5/6; rebuild fundamentals at < 3/6.

| # | Test | Pass condition |
|---|------|----------------|
| Role | Can the role be stated in one sentence? | Output reflects auditor precision, not hedging |
| Context | Only TSR-relevant facts used (≤ 5)? | No generic standard definitions in the chain |
| Falsification | ≥ 2 conditions under which the answer is WRONG? | Assumptions / confidence section present |
| Format | Insertable directly into a governance doc / ALM / audit report? | Matches Evidence-Artifact structure |
| Confidence | Top-3 assumptions named? | Explicit High / Moderate / Low / Unknown + reason |
| Audit | Would an auditor find gaps? | Open Items / Risks section with named unknowns |

---

## Debug Playbook (when a prompt does not converge)

| Symptom | Diagnosis | Fix |
|---|---|---|
| "Multiple approaches are possible" | HARD constraints not declared | Apply Constraint-Stacking; demand HARD/SOFT split |
| Generic best-practice, not task-specific | Constitutional Framing or TSR broken | Re-frame role; strip generic context |
| Output format unusable for the target doc | No explicit format template | Show the target medium; use Evidence-Artifact format |
| Hedges with "it depends" | Falsification criteria missing | Provide rejection conditions; demand a binary answer given the constraints |
| Fabricated ISO clause citations | Asked for a citation, not a concept | Ask "which ISO 26262 *concept* applies?", not "which clause number?" |

---

## Scope

This methodology is applied to the **HWE.1–HWE.4** analyzer prompts by design. HWE
is the downstream stage: the relevant requirements, assessments, and ASIL
classifications are delivered by the **system (SYS)** and inherited downward — the
HWE prompts *consume* those upstream outputs, they do not produce them. The SWE
prompts (`aspice_swq`, `aspice_swa`) are deliberately **out of scope** for the
Mastery Prompt Discipline block; that is a scope boundary, not a pending action.

## Provenance

This methodology was applied to the `reqa-hwe` skill (v1.0.0 → v1.1.0, 2026-06-09)
and propagated into the `prompts/aspice_hwe*_analyzer.md` set. Findings from the
work are recorded in `docs/lessons_learned.md` (LL-2026-0014 …).
