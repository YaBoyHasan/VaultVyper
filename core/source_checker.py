import requests
import os
import time

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "4Q3GTX7MJTE4KT8E444M8I6FA6J9GN1NPZ")
ETHERSCAN_URL = "https://api.etherscan.io/v2/api"

def check_source_code_verified(addresses, chain_id=8453):
    verified = []

    for addr in addresses:
        try:
            res = requests.get(ETHERSCAN_URL, params={
                "chainid": chain_id,
                "module": "contract",
                "action": "getsourcecode",
                "address": addr,
                "apikey": ETHERSCAN_API_KEY
            })

            result = res.json().get("result", [{}])[0]
            source = result.get("SourceCode", "")
            abi = result.get("ABI", "")

            if source.strip() and "not verified" not in abi.lower():
                print(f"[✅] Verified: {addr}")
                verified.append((addr, source))
            else:
                print(f"[❌] Not verified: {addr}")

            time.sleep(0.2)  # avoid Etherscan rate limits

        except Exception as e:
            print(f"[!] Etherscan error on {addr}: {e}")

    return verified
