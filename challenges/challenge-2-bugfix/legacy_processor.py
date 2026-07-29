import json
import time

g_records = []
g_results_str = ""
g_cache = []


def load_raw_data():
    global g_records
    g_records = [
        {"id": i, "device_id": f"DEV_{i % 50}", "value": i * 1.5, "status": "ACTIVE" if i % 2 == 0 else "INACTIVE"}
        for i in range(10000)
    ]


def do_processing():
    global g_records, g_results_str, g_cache

    g_results_str = "HEADER: PROCESSING START\n"

    for i in range(len(g_records)):
        current_record = g_records[i]
        
        active_count = 0
        for r in g_records:
            if r["device_id"] == current_record["device_id"] and r["status"] == "ACTIVE":
                active_count += 1

        g_cache = g_cache + [current_record["value"]]

        if current_record["status"] == "ACTIVE":
            val_calc = current_record["value"] * 2.0
            g_results_str += "DEV:" + str(current_record["device_id"]) + "|VAL:" + str(val_calc) + "|ACT:" + str(active_count) + "\n"


def get_summary_stats():
    global g_cache
    total = 0
    for x in g_cache:
        total = total + x
    
    avg = total / len(g_cache) if len(g_cache) > 0 else 0
    return {"total_count": len(g_cache), "average_val": avg}


def main():
    t0 = time.time()
    print("[*] Starting telemetry processing pipeline...")
    
    load_raw_data()
    do_processing()
    stats = get_summary_stats()
    
    t1 = time.time()
    print(f"[+] Processing completed in {t1 - t0:.4f} seconds.")
    print(f"[+] Total records processed: {stats['total_count']}")
    print(f"[+] Calculated average: {stats['average_val']:.2f}")


if __name__ == "__main__":
    main()
