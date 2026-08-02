"""
Challenge 2: Benchmark & Verification Script

Skrip ini digunakan untuk mengeksekusi dan membandingkan kode bawaan (legacy) 
dengan kode hasil refactoring saya. 

Saya memastikan pengujian dilakukan secara adil dengan memuat kode legacy secara 
terisolasi (menggunakan importlib) dan mereset status globalnya setiap kali iterasi. 
Skrip ini juga bertugas memvalidasi secara otomatis bahwa output dari kedua versi 
tersebut 100% identik sebelum menampilkan hasil benchmark.
"""
from __future__ import annotations

import argparse
import importlib.util
import platform
import statistics
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import perf_counter
from types import ModuleType
from typing import Callable

# Mengambil fungsi dan object dari hasil refactor saya
from refactored_processor import ProcessingResult, run_pipeline

# Konfigurasi path dan target sesuai instruksi soal
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LEGACY_SOURCE = (
    PROJECT_ROOT / "challenges" / "challenge-2-bugfix" / "legacy_processor.py"
)
DEFAULT_OUTPUT = Path(__file__).resolve().with_name("benchmark_results.txt")
TARGET_SPEEDUP = 100.0


@dataclass(frozen=True, slots=True)
class PipelineSnapshot:
    """Dataclass pembantu untuk menyimpan state output akhir agar mudah dibandingkan."""
    report: str
    total_count: int
    average_val: float


@dataclass(frozen=True, slots=True)
class TimingResult:
    """Penyimpan durasi eksekusi dengan property untuk menghitung nilai median & minimum."""
    durations: tuple[float, ...]

    @property
    def median_seconds(self) -> float:
        return statistics.median(self.durations)

    @property
    def minimum_seconds(self) -> float:
        return min(self.durations)


def load_legacy_module() -> ModuleType:
    """
    Memuat file legacy secara dinamis. 
    Ini lebih aman daripada 'import' biasa karena menghindari konflik modul
    dan memastikan kita mengeksekusi file aslinya secara langsung dari path.
    """
    specification = importlib.util.spec_from_file_location(
        "challenge_2_legacy_processor",
        LEGACY_SOURCE,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Gagal memuat source legacy di: {LEGACY_SOURCE}")

    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def run_legacy_pipeline(module: ModuleType) -> PipelineSnapshot:
    """
    Menjalankan kode lama.
    Perhatikan: Di sini kita wajib mengosongkan ulang semua variabel global secara manual.
    Ini adalah salah satu alasan kuat mengapa saya menghapus global state pada kode refactor!
    """
    module.g_records = []
    module.g_results_str = ""
    module.g_cache = []

    module.load_raw_data()
    module.do_processing()
    summary = module.get_summary_stats()

    return PipelineSnapshot(
        report=module.g_results_str,
        total_count=summary["total_count"],
        average_val=summary["average_val"],
    )


def snapshot_refactored_result(result: ProcessingResult) -> PipelineSnapshot:
    """Mengekstrak hasil dari kode refactor agar bentuknya sama dengan PipelineSnapshot."""
    return PipelineSnapshot(
        report=result.report,
        total_count=result.summary.total_count,
        average_val=result.summary.average_val,
    )


def run_refactored_pipeline() -> PipelineSnapshot:
    """Menjalankan kode baru yang jauh lebih bersih tanpa memikirkan reset global state."""
    return snapshot_refactored_result(run_pipeline())


def verify_equivalence(
    legacy_snapshot: PipelineSnapshot,
    refactored_snapshot: PipelineSnapshot,
) -> None:
    """
    Verifikasi utama. Jika output laporan, total count, atau average beda sedikit saja,
    program akan otomatis berhenti (raise AssertionError).
    """
    if legacy_snapshot != refactored_snapshot:
        raise AssertionError("Output dari legacy pipeline dan refactored pipeline berbeda!")


def measure(
    operation: Callable[[], PipelineSnapshot],
    iterations: int,
) -> tuple[TimingResult, PipelineSnapshot]:
    """Menjalankan operasi berulang kali untuk mendapatkan hasil rata-rata yang valid."""
    if iterations <= 0:
        raise ValueError("Jumlah iterasi benchmark harus lebih dari nol")

    durations: list[float] = []
    latest_snapshot: PipelineSnapshot | None = None

    # Memakai perf_counter() karena sangat presisi untuk perhitungan performa
    for _ in range(iterations):
        start_time = perf_counter()
        latest_snapshot = operation()
        durations.append(perf_counter() - start_time)

    if latest_snapshot is None:
        raise RuntimeError("Benchmark gagal memproduksi hasil (result)")

    return TimingResult(tuple(durations)), latest_snapshot


def format_durations(durations: tuple[float, ...]) -> str:
    return ", ".join(f"{duration:.6f}" for duration in durations)


def build_report(
    legacy_timing: TimingResult,
    refactored_timing: TimingResult,
    snapshot: PipelineSnapshot,
) -> str:
    """
    Merangkai teks laporan akhir. Saya biarkan isi laporannya menggunakan Bahasa Inggris 
    agar format log output terminalnya rapi dan profesional sesuai standar.
    """
    speedup_ratio = (
        legacy_timing.median_seconds / refactored_timing.median_seconds
    )
    target_status = "PASS" if speedup_ratio > TARGET_SPEEDUP else "FAIL"

    lines = [
        "Challenge 2 Benchmark Results",
        "=" * 29,
        f"Timestamp: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Python: {platform.python_version()}",
        f"Platform: {platform.platform()}",
        f"Records: {snapshot.total_count}",
        f"Report characters: {len(snapshot.report)}",
        f"Average value: {snapshot.average_val:.2f}",
        "Output equivalence: PASS",
        "",
        f"Legacy runs (seconds): {format_durations(legacy_timing.durations)}",
        f"Legacy median (seconds): {legacy_timing.median_seconds:.6f}",
        f"Legacy minimum (seconds): {legacy_timing.minimum_seconds:.6f}",
        "",
        "Refactored runs (seconds): "
        f"{format_durations(refactored_timing.durations)}",
        f"Refactored median (seconds): {refactored_timing.median_seconds:.6f}",
        f"Refactored minimum (seconds): {refactored_timing.minimum_seconds:.6f}",
        "",
        f"Speedup ratio: {speedup_ratio:.2f}x",
        f"Target (> {TARGET_SPEEDUP:.0f}x): {target_status}",
    ]
    return "\n".join(lines) + "\n"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Skrip untuk membandingkan performa legacy vs refactored telemetry pipeline."
    )
    # Kode legacy dijalankan lebih sedikit karena O(N^2) memakan waktu yang sangat lama
    parser.add_argument("--legacy-runs", type=int, default=3)
    parser.add_argument("--refactored-runs", type=int, default=20)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    legacy_module = load_legacy_module()

    legacy_timing, legacy_snapshot = measure(
        lambda: run_legacy_pipeline(legacy_module),
        arguments.legacy_runs,
    )
    refactored_timing, refactored_snapshot = measure(
        run_refactored_pipeline,
        arguments.refactored_runs,
    )
    
    # 1. Pastikan logika bisnis tidak rusak
    verify_equivalence(legacy_snapshot, refactored_snapshot)

    # 2. Bangun laporan benchmark
    report = build_report(
        legacy_timing,
        refactored_timing,
        refactored_snapshot,
    )
    
    # 3. Simpan ke file teks dan print ke terminal
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(report, encoding="utf-8")
    sys.stdout.write(report)


if __name__ == "__main__":
    main()