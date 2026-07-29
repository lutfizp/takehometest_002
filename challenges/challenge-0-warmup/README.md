# Challenge 0: Binary Packet Parser & Frame Validation (Warm-up)

## Overview
A binary file `frame.bin` is provided in this directory. The file contains a structured binary telemetry frame consisting of a fixed header, a length descriptor, a 16-bit XOR checksum, and an ASCII string payload.

Your task is to write a binary frame parser that validates the packet header and extracts the decoded payload string.

---

## Packet Frame Specifications

### Header Format (8 Bytes Total, Big-Endian)
- **Bytes 0–3**: Magic Signature (`4s`) -> Must match ASCII bytes `INTK` (`0x494E544B`).
- **Bytes 4–5**: Payload Length (`uint16_t` / `>H`) -> Unsigned 16-bit integer representing payload byte length.
- **Bytes 6–7**: Checksum (`uint16_t` / `>H`) -> Unsigned 16-bit XOR checksum calculated over the payload bytes.

### Checksum Algorithm
The 16-bit XOR checksum is calculated across 2-byte words of the payload:
1. Initialize `checksum = 0xFFFF`.
2. Iterate through payload bytes in 16-bit steps (`word = (byte[i] << 8) | byte[i+1]`).
3. Compute `checksum ^= word`.
4. Apply bitwise mask `checksum & 0xFFFF`.

---

## Deliverables
Place all completed files inside `submission/challenge-0/`:

1. **Parser Source Code** (`parse_frame.py`, `parse_frame.c`, or `parse_frame.rs`):
   - Opens `frame.bin` and reads binary header fields.
   - Asserts magic signature validity (`INTK`).
   - Computes and verifies 16-bit XOR checksum.
   - Extracts and prints the decoded ASCII payload string.
2. **`OUTPUT.txt`**:
   - Text file containing the extracted payload string.

---

## Evaluation Focus
- Binary structure unpacking (`struct` / bit shifts).
- Header validation and error handling.
- Basic bitwise checksum verification.
