# core/fork_tester.py (simplified excerpt)

import os, subprocess, json, time

def run_fork_test(entry_point_address, block_number):
    # 1) Start Hardhat‐fork
    node_proc = subprocess.Popen(
        ["npx.cmd", "hardhat", "node",
         "--fork", f"https://eth-mainnet.public.blastapi.io@{block_number}",
         "--port", "8545"],
        cwd=".", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(5)  # give Hardhat 5s to boot

    # 2) Run the “simple_poc.js” script with TARGET & AMOUNT set:
    env = os.environ.copy()
    env["TARGET"] = entry_point_address
    env["AMOUNT"] = str(10**16)  # 0.01 ETH in wei

    try:
        raw_out = subprocess.check_output(
            ["npx.cmd", "hardhat", "run", "--network", "localhost", "scripts/simple_poc.js"],
            cwd=".", stderr=subprocess.STDOUT, env=env, text=True
        )
        # The script just prints “final balance” and “profit” lines.
        # We can grep “profit” out of raw_out:
        for line in raw_out.splitlines():
            if line.strip().startswith("profit"):
                profit_str = line.split(":")[1].strip()
                profit_wei = float(profit_str)
                if profit_wei > 0:
                    print("[🚀] Fork test success! profit:", profit_str, "ETH")
                    node_proc.kill()
                    return True
        print("[✖️] Fork test saw no profit.")
    except subprocess.CalledProcessError as e:
        print("[⚠️] PoC script reverted or errored:", e.output)

    node_proc.kill()
    return False
