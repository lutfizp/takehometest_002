from __future__ import annotations

import argparse
import struct
from pathlib import Path

# ==========================================
# KONSTANTA & PARAMETER CIPHER
# ==========================================
BLOCK_SIZE_BYTES = 8
ROUNDS_PER_BLOCK = 8
MAX_32_BIT = 0xFFFFFFFF  # Masking untuk memastikan angka tidak melebihi 32-bit

# Parameter bawaan dari soal cryptanalysis
INITIAL_LFSR_SEED = 0x9E3779B9
ROUND_CONSTANT = 0x5A5A5A5A
ROTATION_BITS = 5


def rotate_left_32(value: int, shift: int) -> int:
    """
    Memutar bit ke kiri (Circular Left Shift) untuk angka 32-bit.
    Bit yang terbuang di kiri akan dilempar kembali ke sisi paling kanan.
    """
    clean_value = value & MAX_32_BIT
    actual_shift = shift % 32
    
    shifted_left = clean_value << actual_shift
    wrapped_bits = clean_value >> (32 - actual_shift)
    
    return (shifted_left | wrapped_bits) & MAX_32_BIT


def advance_lfsr(current_state: int) -> int:
    """
    Menggeser LFSR (Linear-Feedback Shift Register) sebanyak 1 langkah.
    Sesuai algoritma cipher, tap diambil dari bit ke 31, 30, 29, dan 9.
    """
    # 1. Ambil nilai dari masing-masing posisi tap (dihitung dari kanan)
    bit_31 = current_state >> 31
    bit_30 = current_state >> 30
    bit_29 = current_state >> 29
    bit_9  = current_state >> 9
    
    # 2. XOR semua tap untuk menghasilkan bit baru (feedback bit)
    new_bit = (bit_31 ^ bit_30 ^ bit_29 ^ bit_9) & 1
    
    # 3. Geser state ke kiri 1 posisi, lalu masukkan bit baru di ujung kanan
    next_state = ((current_state << 1) | new_bit) & MAX_32_BIT
    return next_state


def feistel_round_function(right_half: int, round_key: int) -> int:
    """
    Fungsi F (Round Function) pada jaringan Feistel.
    Menggabungkan bagian kanan data dengan kunci ronde dan konstanta.
    """
    # Algoritma: Rotasi bit Kanan -> XOR dengan Kunci -> XOR dengan Konstanta
    rotated = rotate_left_32(right_half, ROTATION_BITS)
    mixed_with_key = rotated ^ round_key
    scrambled = mixed_with_key ^ ROUND_CONSTANT
    
    return scrambled & MAX_32_BIT


def generate_block_round_keys(current_lfsr_state: int) -> tuple[list[int], int]:
    """
    Menghasilkan 8 kunci (round keys) untuk 1 blok (64-bit).
    Catatan penting: State LFSR akan diteruskan ke blok berikutnya!
    """
    keys_for_this_block = []
    
    for _ in range(ROUNDS_PER_BLOCK):
        # Update LFSR, lalu jadikan state barunya sebagai kunci ronde ini
        current_lfsr_state = advance_lfsr(current_lfsr_state)
        keys_for_this_block.append(current_lfsr_state)

    return keys_for_this_block, current_lfsr_state


def decrypt_block(encrypted_block: bytes, round_keys: list[int]) -> bytes:
    """
    Mendekripsi 1 blok (8 byte) menggunakan kebalikan jaringan Feistel.
    """
    if len(encrypted_block) != BLOCK_SIZE_BYTES:
        raise ValueError("Ukuran blok harus pas 8 byte.")

    # Pecah blok 64-bit menjadi 2 bagian 32-bit (Kiri dan Kanan)
    # '>II' artinya Big-Endian, dua buah Unsigned Integer
    left_half, right_half = struct.unpack(">II", encrypted_block)

    # Trik dekripsi Feistel: Gunakan kunci yang sama, tapi urutannya DIBALIK!
    for key in reversed(round_keys):
        # Memutar balik logika Feistel:
        # Kiri yang asli = Kanan saat ini XOR Fungsi F(Kiri saat ini, Kunci)
        original_left = right_half ^ feistel_round_function(left_half, key)
        original_right = left_half
        
        # Geser posisi untuk putaran mundur berikutnya
        left_half, right_half = original_left, original_right

    # Gabungkan kembali bagian Kiri dan Kanan yang sudah didekripsi
    return struct.pack(">II", left_half, right_half)


def remove_pkcs7_padding(padded_data: bytes) -> bytes:
    """
    Membersihkan byte ekstra (padding) PKCS#7 yang ditambahkan saat enkripsi.
    Misal: Jika ada 4 byte kosong, paddingnya akan berisi [0x04, 0x04, 0x04, 0x04].
    """
    if not padded_data:
        return padded_data

    # Ambil byte terakhir untuk mengetahui jumlah padding
    padding_length = padded_data[-1]
    
    # Validasi dasar padding
    if padding_length < 1 or padding_length > BLOCK_SIZE_BYTES:
        raise ValueError(f"Panjang padding tidak valid: {padding_length}")

    # Cek apakah semua byte padding isinya sesuai dengan aturan PKCS#7
    expected_padding = bytes([padding_length]) * padding_length
    if padded_data[-padding_length:] != expected_padding:
        raise ValueError("Padding rusak atau ini bukan ciphertext yang valid!")

    # Potong data dan buang padding-nya
    return padded_data[:-padding_length]


def decrypt_ciphertext(ciphertext: bytes) -> bytes:
    """Fungsi utama untuk mendekripsi seluruh file ciphertext."""
    decrypted_data = bytearray()
    
    # Inisialisasi LFSR dengan seed awal
    lfsr_state = INITIAL_LFSR_SEED

    # Proses per 8 Byte (1 Blok)
    for offset in range(0, len(ciphertext), BLOCK_SIZE_BYTES):
        block = ciphertext[offset : offset + BLOCK_SIZE_BYTES]
        
        # Generate kunci dan update state LFSR untuk blok berikutnya
        keys, lfsr_state = generate_block_round_keys(lfsr_state)
        
        # Dekripsi blok dan simpan hasilnya
        decrypted_block = decrypt_block(block, keys)
        decrypted_data.extend(decrypted_block)

    # Buang padding PKCS#7 sebelum dikembalikan sebagai plaintext utuh
    return remove_pkcs7_padding(bytes(decrypted_data))


def main() -> None:
    # Set default path untuk mempermudah testing lokal
    project_root = Path(__file__).resolve().parents[2]
    default_input = project_root / "challenges" / "challenge-1-cryptanalysis" / "cipher.enc"
    default_output = Path(__file__).resolve().with_name("FLAG.txt")

    parser = argparse.ArgumentParser(description="Cryptanalysis Tool: Custom Feistel/LFSR Decryptor")
    parser.add_argument("ciphertext", nargs="?", type=Path, default=default_input, help="Path ke file cipher.enc")
    parser.add_argument("--output", type=Path, default=default_output, help="Path untuk menyimpan hasil plaintext")
    
    args = parser.parse_args()

    print("[*] Memulai proses dekripsi...")
    print(f"[*] Target file   : {args.ciphertext}")
    
    try:
        # Baca file yang dienkripsi
        encrypted_bytes = args.ciphertext.read_bytes()
        print(f"[*] Ukuran data   : {len(encrypted_bytes)} bytes")
        
        # Eksekusi dekripsi
        plaintext_bytes = decrypt_ciphertext(encrypted_bytes)
        plaintext = plaintext_bytes.decode("ascii")
        
        # Simpan ke file output
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{plaintext}\n", encoding="ascii")
        
        print("[+] Dekripsi Berhasil!")
        print(f"[+] Disimpan di   : {args.output}")
        print("\n--- ISI PLAINTEXT (FLAG) ---")
        print(plaintext)
        print("----------------------------\n")
        
    except FileNotFoundError:
        print(f"[!] Error: File {args.ciphertext} tidak ditemukan!")
    except Exception as error:
        print(f"[!] Dekripsi gagal. Kemungkinan ciphertext rusak atau algoritma tidak cocok.")
        print(f"[!] Detail error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()