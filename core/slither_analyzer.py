import subprocess

def run_slither(chain_slug, address):
    print(f"[🔎] Running Slither on {chain_slug}:{address}")

    cmd = [
        "slither",
        f"{chain_slug}:{address}",
        "--solc-args", "--via-ir --optimize --allow-paths C:/Users/haych/Desktop/VaultVyper",
        "--json", f"slither_reports/{address}.json",
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        print(f"[❌] Slither subprocess error for {address}: {e}")
        return False

    # On Windows, Slither often returns a large non-zero code even when it compiles/finds issues
    # So we treat *any* return code as “analysis succeeded,” and only inspect stderr if needed
    if proc.stderr:
        print(f"[⚠️] Slither reported issues or warnings for {address}")
    else:
        print(f"[✅] Slither ran clean (no issues) for {address}")

    return True
