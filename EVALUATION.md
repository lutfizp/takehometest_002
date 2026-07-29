# Candidate Evaluation Framework & Scoring Rubric

## Scoring Summary

| Category | Weight | Description |
| :--- | :--- | :--- |
| **Warm-up Binary Parsing (Challenge 0)** | 10% | Header unpacking, magic validation, and XOR checksum verification |
| **Mathematical Cryptanalysis (Challenge 1)** | 35% | First-principles implementation of Feistel rounds and LFSR subkeys |
| **Code Architecture & Quality (Challenge 2)** | 25% | Structural cleanliness, modularity, static typing, and runtime speedup |
| **Bug Audit & Vulnerability Analysis** | 15% | Depth of root-cause identification and antipattern analysis |
| **Git Command & Workflow Hygiene** | 15% | Branch management, atomic commit history, clean rebase, and PR structure |

---

## Detailed Evaluation Breakdown

### 0. Warm-up Binary Packet Parsing (10 Points)
- **Header Structure & Magic Validation (5 pts)**: Correct binary unpacking of magic signature `INTK` and length header.
- **XOR Checksum Verification (5 pts)**: Correct 16-bit word-level checksum calculation and payload extraction.

### 1. Mathematical Cryptanalysis (35 Points)
- **State Transformations (15 pts)**: Correct implementation of LFSR polynomial feedback taps and word rotation without bit truncation.
- **Round Function Execution (10 pts)**: Precise implementation of Feistel network rounds and subkey injection.
- **Decryption & Padding (10 pts)**: Flawless PKCS#7 padding validation and reverse stream block processing.

### 2. Code Architecture & Quality (25 Points)
- **Modularity & Scalability (10 pts)**: Decoupled functions, clean abstraction boundaries, and reusable primitive components.
- **Maintainability & Readability (10 pts)**: Clear naming conventions, logical layout, zero magic constants, direct documentation.
- **Compilation & Execution Hygiene (5 pts)**: Zero compiler warnings under strict flags (`-Wall -Wextra -Werror`), type safety, memory leak prevention.

### 3. Code Audit & Antipattern Analysis (15 Points)
- **Root-Cause Identification (8 pts)**: Thorough breakdown of $O(N^2)$ quadratic scanning, list re-allocation overheads, and global mutations in `REFACTORING_ANALYSIS.md`.
- **Refactoring Quality (7 pts)**: Robust, production-grade refactoring achieving significant runtime acceleration (> 100x relative speedup ratio $\frac{T_{\text{legacy}}}{T_{\text{refactored}}}$).

### 4. Git Command & Workflow Hygiene (15 Points)
- **Branch Strategy (5 pts)**: Dedicated feature branch created following the naming convention (`solution/<candidate-name>`).
- **Commit History Hygiene (5 pts)**: Atomic, structured commit messages adhering to Conventional Commits guidelines.
- **Pull Request Presentation (5 pts)**: Comprehensive PR description summarizing changes, verification steps, and execution commands.
