import os
import time
import threading
import requests
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_URL = "http://127.0.0.1:8000/api/v1"
CSV_FILE = "scanned.csv"

# --- API Test Functions ---
def test_get_engines():
    resp = requests.get(f"{BASE_URL}/engines")
    data = resp.json()
    engines = data.get("engines", [])
    return {"endpoint": "/engines", "result": f"{len(engines)} engines"}

def test_get_engine_status():
    resp = requests.get(f"{BASE_URL}/engines/status")
    return {"endpoint": "/engines/status", "result": resp.json()}

def test_system_metrics():
    resp = requests.get(f"{BASE_URL}/system/metrics")
    return {"endpoint": "/system/metrics", "result": resp.json()}

def test_scan_history():
    resp = requests.get(f"{BASE_URL}/scan/history")
    return {"endpoint": "/scan/history", "result": resp.json()}

def test_scan_file(filepath):
    try:
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f)}
            resp = requests.post(f"{BASE_URL}/scan/file", files=files)
            return resp.json()
    except Exception as e:
        return {"error": str(e), "file": filepath}

def test_scan_batch(filepaths):
    files = [("files", (os.path.basename(fp), open(fp, "rb"))) for fp in filepaths]
    try:
        resp = requests.post(f"{BASE_URL}/scan/batch", files=files)
        return resp.json()
    finally:
        for _, (_, f) in files:
            f.close()

def test_scan_status(scan_id):
    resp = requests.get(f"{BASE_URL}/scan/{scan_id}/status")
    return resp.json()

# --- Directory Watcher ---
class ScanHandler(FileSystemEventHandler):
    def __init__(self, scan_callback):
        super().__init__()
        self.scan_callback = scan_callback
    def on_created(self, event):
        if not event.is_directory:
            self.scan_callback(event.src_path)

# --- CSV Logging ---
def append_to_csv(data, columns):
    df = pd.DataFrame([data], columns=columns)
    if not os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, index=False)
    else:
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)

# --- Main Test Runner ---
def run_api_tests():
    results = []
    results.append(test_get_engines())
    results.append(test_get_engine_status())
    results.append(test_system_metrics())
    results.append(test_scan_history())
    # Scan all files in current dir as a batch test
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f != os.path.basename(__file__) and not f.endswith('.csv')]
    if files:
        batch_result = test_scan_batch(files)
        results.append({"endpoint": "/scan/batch", "result": batch_result})
    # Log summary to CSV
    for r in results:
        append_to_csv({"API Endpoint": r["endpoint"], "Result": str(r["result"])}, ["API Endpoint", "Result"])
    print("API tests complete. Results logged to scanned.csv.")

# --- Watch and Scan New Files ---
def scan_and_log(filepath):
    print(f"Scanning new file: {filepath}")
    result = test_scan_file(filepath)
    # Flatten result for CSV
    row = {
        "File": os.path.basename(filepath),
        "Detected Type": result.get("result", {}).get("detected_type") if isinstance(result.get("result"), dict) else None,
        "Confidence": result.get("result", {}).get("confidence") if isinstance(result.get("result"), dict) else None,
        "Extension": result.get("result", {}).get("extension") if isinstance(result.get("result"), dict) else None,
        "Scan Time": result.get("result", {}).get("scan_time") if isinstance(result.get("result"), dict) else None,
        "Threat Level": result.get("result", {}).get("security", {}).get("threat_level") if isinstance(result.get("result", {}).get("security"), dict) else None,
        "Error": result.get("error")
    }
    append_to_csv(row, ["File", "Detected Type", "Confidence", "Extension", "Scan Time", "Threat Level", "Error"])
    print(f"Scan result for {filepath} logged.")

def start_watcher():
    event_handler = ScanHandler(scan_and_log)
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()
    print("Watching current directory for new files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Run all API tests and log
    run_api_tests()
    # Start directory watcher in main thread
    start_watcher()