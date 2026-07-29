# Cryptography & Software Engineering Take-Home Assessment

Welcome to the technical take-home assessment repository. This test evaluates your low-level software engineering skills, mathematical implementation accuracy, binary data parsing, performance optimization, and Git command proficiency.

---

## Getting Started & Repository Setup

1. **Clone the Repository**:
   Clone this repository to your local development environment:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Install optional setup requirements (Python 3.10+ required):
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Your Solution Branch**:
   Do not commit directly to `main`. Create a dedicated feature branch using your name:
   ```bash
   git checkout -b solution/<your-name>
   ```

4. **Read Guidelines**:
   Review [RULES.md](RULES.md) for library restrictions and AI usage policies, and consult [EVALUATION.md](EVALUATION.md) for scoring breakdowns.

---

## Repository Structure

```
.
├── README.md               # Main instructions & setup guide
├── RULES.md                # Submission rules, library restrictions, AI policies
├── EVALUATION.md           # Evaluation breakdown and scoring rubric
├── requirements.txt        # Environment requirements
├── challenges/
│   ├── challenge-0-warmup/
│   │   ├── frame.bin        # Binary telemetry packet file
│   │   └── README.md        # Warm-up binary parsing prompt
│   ├── challenge-1-cryptanalysis/
│   │   ├── cipher.enc       # Encrypted binary payload
│   │   └── README.md        # Cryptanalysis task prompt
│   └── challenge-2-bugfix/
│       ├── legacy_processor.py # Legacy telemetry processor source file
│       └── README.md        # Code audit & refactoring prompt
└── submission/              # Destination folder for candidate code solutions
```

---

## Tasks Overview

### Task 0: Binary Packet Parser & Frame Validation (Warm-up)
Parse the binary telemetry packet `challenges/challenge-0-warmup/frame.bin`. Validate header magic signatures, verify the 16-bit XOR checksum, and extract the decoded ASCII payload string into `submission/challenge-0/`.

### Task 1: Cryptanalysis & Decryption
Reverse engineer the custom 64-bit Feistel cipher and LFSR key schedule described in `challenges/challenge-1-cryptanalysis/README.md`. Write a decryption program to decrypt `cipher.enc` and extract the secret flag string into `submission/challenge-1/`.

### Task 2: Code Audit & Architecture Refactoring
Analyze `challenges/challenge-2-bugfix/legacy_processor.py`. Conduct an independent code audit, identify all performance bottlenecks and software antipatterns, document findings in `submission/challenge-2/REFACTORING_ANALYSIS.md`, and provide a production-ready refactored implementation.

### Task 3: Git Workflow & Repository Hygiene
Demonstrate your Git command proficiency through structured repository management:
1. Clone the repository as specified in the **Getting Started** section.
2. Maintain clean, atomic commit history adhering to Conventional Commits (`feat:`, `fix:`, `docs:`).
3. Perform interactive rebasing (`git rebase -i main`) if necessary to clean up draft commits before submission.
4. Push your branch to the remote repository and open a Pull Request targeting `main`.

---

## Submission Guidelines

1. Place all your code and writeups strictly inside the `submission/` directory:
   - `submission/challenge-0/` -> Binary parser code, `OUTPUT.txt`.
   - `submission/challenge-1/` -> Decryption script, `FLAG.txt`, build/execution instructions.
   - `submission/challenge-2/` -> `REFACTORING_ANALYSIS.md`, patched source code file, benchmark screenshot (`benchmark_proof.png`).
2. Ensure code compiles cleanly without warnings.
3. Submit your work via a Pull Request as instructed in [RULES.md](RULES.md).
4. Consult [EVALUATION.md](EVALUATION.md) to understand the scoring rubric.
