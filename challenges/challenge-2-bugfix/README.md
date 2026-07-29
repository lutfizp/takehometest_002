# Challenge 2: Telemetry Pipeline Refactoring & Code Audit

## Overview
The file `legacy_processor.py` implements an end-to-end data processing pipeline for device telemetry logs. The script ingests raw telemetry records, processes device activity statuses, applies value transformations, and calculates aggregated summary statistics.

While the script runs and produces correct outputs, the code quality, software architecture, and execution performance fall below production engineering standards.

Your objective is to conduct a code audit, identify all architectural and performance flaws, document your findings, and provide a refactored implementation.

---

## Data Pipeline Workflow
`legacy_processor.py` performs three core operations:

1. **Data Ingestion (`load_raw_data`)**:
   Simulates raw device telemetry payload ingestion containing device identifiers, numeric readings, and activity status flags (`ACTIVE` / `INACTIVE`).

2. **Telemetry Processing (`do_processing`)**:
   Iterates through telemetry records, counts active record occurrences per device identifier, applies numeric scalar transformations, and builds a formatted execution log.

3. **Statistical Aggregation (`get_summary_stats`)**:
   Computes global record counts and calculates average value metrics across processed telemetry entries.

---

## Benchmarking & Online Testing Platform
To ensure hardware-independent evaluation, performance is measured using the **Execution Speedup Ratio**:

$$\text{Speedup Ratio} = \frac{\text{Execution Time of Legacy Code}}{\text{Execution Time of Refactored Code}}$$

- **Target**: Achieve a **> 100x Speedup Ratio** on the same machine or platform.
- **Online Compiler Option (No Account Required)**:
  If testing on lower-end local hardware, run both scripts on a free online Python runner:
  - [Online Python](https://www.online-python.com)
  - [Programiz Python Compiler](https://www.programiz.com/python-programming/online-compiler)
  - [OneCompiler Python](https://onecompiler.com/python)

Attach a screenshot of your execution comparison as `benchmark_proof.png` inside `submission/challenge-2/`.

---

## Task Requirements

1. **Audit & Analysis (`submission/challenge-2/REFACTORING_ANALYSIS.md`)**:
   - Perform a thorough code review of `legacy_processor.py`.
   - Identify every software antipattern, performance bottleneck, memory inefficiency, and design flaw.
   - Explain why each identified issue impairs execution scalability, maintainability, or code safety.
   - Detail your refactoring strategy and document the calculated speedup ratio ($\frac{T_{\text{legacy}}}{T_{\text{refactored}}}$).

2. **Refactored Implementation (`submission/challenge-2/refactored_processor.py`)**:
   - Deliver a production-grade, modular refactored script (in Python, C, C++, or Rust).
   - Preserve exact functional output correctness while optimizing execution speed and memory efficiency.
   - Include runtime benchmark output comparing original vs refactored execution times.

---

## Deliverables Checklist
Place all completed files inside `submission/challenge-2/`:
- `REFACTORING_ANALYSIS.md` (Code audit report & antipattern analysis)
- `refactored_processor.py` (Production-ready refactored codebase)
- `benchmark_proof.png` (Screenshot showing benchmark execution results)
