# Hackathon Winner Repository Benchmark

Reviewed on 27 September 2026. These are examples of **submission practice**, not evidence that copying their layout guarantees a prize.

| Reference | Verified practice | Applied here |
|---|---|---|
| [Official Call for Code project sample](https://github.com/Call-for-Code/Project-Sample) | Problem, technology, architecture, demo, roadmap, run instructions, and license are easy to locate. | README quick links and a working local runbook. |
| [Pyrrha / Prometeo, Call for Code 2019 global winner](https://github.com/Pyrrha-Platform/Pyrrha) | A concrete user story, component roles, and a quick start connect the idea to implementation. | One `WO-1028` story and a clear implemented/planned split. |
| [Lunar Trek, NASA Space Apps 2023 global winner](https://github.com/MohammadHelaly/lunar-trek) | Runnable source, setup, deployment notes, and a preserved submission snapshot. | Dependency-free app, repeatable tests, and snapshot guidance. |
| [Project AEDES, NASA Space Apps 2019 Best Use of Data](https://github.com/Cirrolytix/aedes_dpg) | Problem rationale, sources, implementation directions, and documentation. | Source-linked problem validation and explicit evidence limitations. |

The [IBM SkillsBuild National Hackathon 2026 program page](https://hacktiv8.com/projects/ibm/hackathon) specifically asks participants to prepare an MVP/prototype, business model, demo video, documentation, and a technical diagram. Its public page does not establish that these example repositories define the contest rubric.

## Patterns adopted

### IBM Call for Code official template

The official project sample recommends a README that covers the issue, solution, IBM technology use, architecture, demo video, roadmap, how to run, and live demo. PROOF2PAY mirrors those judge-navigation needs through `README.md`, `SUBMISSION.md`, architecture docs, and implementation evidence.

### Prometeo / Pyrrha — Call for Code 2019 Global Winner

The winner repository makes the problem story immediately understandable, separates setup/roadmap, names the technologies used, and provides a clear component model. PROOF2PAY adopts the same principle: problem first, component roles second, setup/evidence paths explicit.

### Lunar Trek — NASA Space Apps 2023 Global Winner

The repository has a concise overview, explicit tech stack, project structure, runbook, deployment instructions, and preserves the original submission in an archive branch. PROOF2PAY therefore adds `SUBMISSION_SNAPSHOT.md` and an implementation-status source of truth.

### AEDES — NASA Space Apps 2019 Global Winner

AEDES documents challenge, problem, solution, data sources, related literature, objectives, and pilot-area rationale. PROOF2PAY follows this evidence-first pattern with `research/`, validation limitations, and a narrow initial vertical.

## Principle

The goal is not to copy another project's visual style. The goal is to copy **submission discipline**:

**problem clarity + runnable prototype + transparent architecture + evidence + reproducibility + demo-first navigation + honest limitations.**
