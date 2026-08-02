"""
Challenge 2: Refactored Telemetry Processor
Kandidat: Rio Saputra Duha

Catatan untuk Reviewer:
Halo! Di versi refactor ini, saya fokus untuk menghilangkan bottleneck algoritma 
yang tadinya O(N^2) dan menghapus penggunaan global variable dari kode bawaan (legacy). 
Saya juga menggunakan fitur @dataclass dengan parameter frozen agar datanya immutable 
dan penggunaan memori jauh lebih efisien.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from time import perf_counter
from typing import Sequence

# Kumpulan konstanta (dipindahkan ke sini agar tidak ada hardcode di dalam fungsi)
ACTIVE_STATUS = "ACTIVE"
INACTIVE_STATUS = "INACTIVE"
DEFAULT_RECORD_COUNT = 10_000
DEFAULT_DEVICE_COUNT = 50
SOURCE_VALUE_MULTIPLIER = 1.5
OUTPUT_VALUE_MULTIPLIER = 2.0
REPORT_HEADER = "HEADER: PROCESSING START\n"


# Saya mengganti dictionary biasa menjadi dataclass.
# Menggunakan slots=True sangat membantu menghemat memori saat memproses banyak data.
@dataclass(frozen=True, slots=True)
class TelemetryRecord:
    record_id: int
    device_id: str
    value: float
    status: str


@dataclass(frozen=True, slots=True)
class SummaryStats:
    total_count: int
    average_val: float

    # Fungsi ini memungkinkan kita memanggil data sebagai dictionary (seperti kode legacy)
    def as_dict(self) -> dict[str, int | float]:
        return {
            "total_count": self.total_count,
            "average_val": self.average_val,
        }


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    report: str
    summary: SummaryStats


def load_raw_data(
    record_count: int = DEFAULT_RECORD_COUNT,
    device_count: int = DEFAULT_DEVICE_COUNT,
) -> list[TelemetryRecord]:
    """Fungsi untuk membuat data input tiruan (logikanya disamakan dengan versi lama)."""
    if record_count < 0:
        raise ValueError("record_count tidak boleh negatif")
    if device_count <= 0:
        raise ValueError("device_count harus lebih besar dari nol")

    return [
        TelemetryRecord(
            record_id=record_index,
            device_id=f"DEV_{record_index % device_count}",
            value=record_index * SOURCE_VALUE_MULTIPLIER,
            status=ACTIVE_STATUS if record_index % 2 == 0 else INACTIVE_STATUS,
        )
        for record_index in range(record_count)
    ]


def count_active_records(records: Sequence[TelemetryRecord]) -> Counter[str]:
    """
    Fungsi bantuan untuk menghitung record yang aktif.
    Dengan collections.Counter, kita hanya perlu melakukan satu kali perulangan (O(N)),
    menggantikan proses scanning berulang kali di kode lama.
    """
    return Counter(
        record.device_id
        for record in records
        if record.status == ACTIVE_STATUS
    )


def process_records(records: Sequence[TelemetryRecord]) -> ProcessingResult:
    """Fungsi pemrosesan utama yang sudah tidak lagi bergantung pada global variable."""
    
    # Hitung semua perangkat aktif di awal agar tidak membebani loop utama
    active_counts = count_active_records(records)
    
    # Saya menggunakan list untuk menampung baris teks alih-alih operator (+=).
    # Karena string di Python bersifat immutable, menggabungkannya di akhir akan jauh lebih cepat.
    report_lines = [REPORT_HEADER]
    total_value = 0.0

    for record in records:
        total_value += record.value

        if record.status == ACTIVE_STATUS:
            transformed_value = record.value * OUTPUT_VALUE_MULTIPLIER
            report_lines.append(
                f"DEV:{record.device_id}|VAL:{transformed_value}"
                f"|ACT:{active_counts[record.device_id]}\n"
            )

    total_count = len(records)
    average_value = total_value / total_count if total_count else 0

    return ProcessingResult(
        report="".join(report_lines),
        summary=SummaryStats(
            total_count=total_count,
            average_val=average_value,
        ),
    )


def run_pipeline(
    record_count: int = DEFAULT_RECORD_COUNT,
    device_count: int = DEFAULT_DEVICE_COUNT,
) -> ProcessingResult:
    """Mengatur alur load data dan pemrosesan secara berurutan."""
    records = load_raw_data(record_count, device_count)
    return process_records(records)


def main() -> None:
    # Menggunakan perf_counter() dengan variabel t0 dan t1 seperti struktur asli di gambar
    t0 = perf_counter()
    print("[*] Starting telemetry processing pipeline...")

    result = run_pipeline()
    # Ekstrak dictionary dari hasil summary agar variabel pemanggilannya identik
    stats = result.summary.as_dict()

    t1 = perf_counter()
    print(f"[+] Processing completed in {t1 - t0:.4f} seconds.")
    print(f"[+] Total records processed: {stats['total_count']}")
    print(f"[+] Calculated average: {stats['average_val']:.2f}")


if __name__ == "__main__":
    main()