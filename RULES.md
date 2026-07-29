# Candidate Submission Rules & Engineering Standards

## 1. Acceptable Languages & Tooling
Candidates may complete the challenges using any of the following languages:
- **Low-Level Languages**: C (C11 or later), C++ (C++17 or later), Rust (2021 edition), Assembly (x86_64 / ARM64).
- **High-Level Languages**: Python 3.10+ (using standard library modules only).

---

## 2. Library & Dependency Restrictions
- **Zero Third-Party Cryptography Libraries**: Usage of external cryptography packages (e.g. OpenSSL, `pycryptodome`, `libsodium`, Rust `crypto` crates) is strictly prohibited.
- **First-Principles Implementation**: All bitwise operations, state transitions, LFSR updates, and modular integer arithmetic must be implemented manually using core language syntax.
- Standard I/O and system libraries (`stdio.h`, `stdint.h`, `sys`, `struct`, `std::collections`) are permitted.

---

## 3. Artificial Intelligence (AI) Policy
We evaluate your genuine software design skills, mathematical understanding, and code craftsmanship.
- **Permitted**: Using AI tools (ChatGPT, Claude, Copilot) as a search engine for syntax reference or standard library documentation.
- **Prohibited**: Utilizing AI tools to generate algorithm logic, cryptographic math transformations, bug identification, or complete code solutions.
- Submissions showing signs of synthetic, unverified AI output lacking manual design considerations will receive zero points.

---

## 4. Professional Code Quality Requirements

### A. Cleanliness & Readability
- Follow standard code formatting guidelines (e.g. PEP 8 for Python, `clang-format` for C/C++, `rustfmt` for Rust).
- Use self-documenting variable and function names. Avoid single-letter identifiers except for standard loop indices.

### B. Mathematical & Type Correctness
- Use explicit fixed-width integer types (`uint32_t`, `uint64_t`, `u32`, `u64`) for bitwise logic.
- Avoid implicit type conversions, float conversions, or unsafe pointer aliasing.

### C. Scalability & Maintainability
- Structure logic into decoupled, modular functions (e.g. key expansion, round function, block processing, padding handling).
- Include minimal, direct comments explaining non-trivial mathematical equations.

---

## 5. Git & Submission Workflow Rules
- Do not commit directly to `main`.
- Create feature branch: `solution/<candidate-name>`.
- Use clear, atomic Git commit messages following Conventional Commits (`feat:`, `fix:`, `docs:`).
- Keep `submission/` directory organized per challenge requirements.
- Submit final work via a clean Pull Request targeting `main`.
