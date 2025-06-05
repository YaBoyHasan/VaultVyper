# main.py

import time
from core.block_watcher import get_new_contracts
from core.source_checker import check_source_code_verified
from core.slither_analyzer import run_slither
from core.slither_parser import parse_slither_report
# from core.fork_test import run_fork_test   # uncomment if you still want to run forks

SLEEP_SECONDS = 1  # how long to wait before re‐scanning

def scan_once():
    print("[⛏] Scanning recent blocks...")
    candidates = get_new_contracts()
    print(f"[🔍] {len(candidates)} candidates found")

    verified = check_source_code_verified(candidates)
    print(f"[📜] {len(verified)} verified contracts")

    for address, _ in verified:
        # run Slither; if it produces any output, parse the report
        if run_slither("mainnet", address):
            if parse_slither_report(address):
                print(f"[‼️] Critical vuln found in {address}")
                return address  # signal “found one”
            else:
                print(f"[✅] No critical vuln in {address}")
        else:
            print(f"[⚠️] Slither skipped or crashed on {address}")

    return None  # no critical vulnerabilities found this round

def main():
    print("▶️ Starting continuous scan. Will re‐run every "
          f"{SLEEP_SECONDS} seconds until a critical vuln is found.\n")

    while True:
        critical = scan_once()
        if critical:
            # found one; exit loop (or you could alert/pause here)
            print(f"\n🏁 Stopping scan. Vulnerable contract: {critical}");
            continue
            #break

        print(f"\n🕒 No critical vulns found—waiting {SLEEP_SECONDS} seconds before next scan...\n")
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
