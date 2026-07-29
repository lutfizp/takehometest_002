# Challenge 1: Custom Cipher Cryptanalysis & Decryption

## Overview
An encrypted binary file `cipher.enc` is provided in this directory. The payload was encrypted using a custom 64-bit Feistel block cipher paired with a Linear Feedback Shift Register (LFSR) key expansion mechanism.

Your objective is to reverse engineer the cipher specification, write a decryption tool, and recover the original plaintext string.

---

## Specifications

### 1. Block Cipher Properties
- **Block Size**: 64 bits (split into two 32-bit halves: `Left` and `Right`).
- **Structure**: 8-round symmetric Feistel network.
- **Padding**: PKCS#7 block padding (8-byte block size).
- **Endianness**: Big-endian word packing (`>II`).

### 2. Round Function F(R, K_i)
For a 32-bit right half `R` and a 32-bit subkey `K_i`:

```
F(R, K_i) = rotate_left32(R, 5) ^ K_i ^ 0x5A5A5A5A
```

Where `rotate_left32(R, 5)` performs a bitwise circular left shift by 5 bits on an unsigned 32-bit integer.

### 3. Key Schedule & LFSR
- **Initial Seed**: `0x9E3779B9`
- **State Size**: 32-bit unsigned integer.
- **LFSR Tap Feedback**: Polynomial taps at bit positions 32, 31, 30, and 10.
  ```
  tap = ((state >> 31) ^ (state >> 30) ^ (state >> 29) ^ (state >> 9)) & 1
  ```
- **State Transition**:
  ```
  state_next = ((state << 1) | tap) & 0xFFFFFFFF
  ```
- The updated state directly serves as the 32-bit subkey `K_i` for round $i$. The state carries over continuously across consecutive block operations.

---

## Deliverables
Save your solution inside `submission/challenge-1/`:
1. Source code file (`decrypt.py`, `decrypt.c`, or `decrypt.rs`) implementing the decryption algorithm without third-party cryptography libraries.
2. A plain text file named `FLAG.txt` containing the recovered plaintext.
3. Execution instructions in `README.md` within your submission subfolder.

---

## Evaluation Focus
- First-principles bitwise and modular arithmetic correctness.
- Proper handling of stream state propagation and PKCS#7 unpadding.
- Code readability, static typing (or strict memory management if C/Rust), and structural cleanliness.
