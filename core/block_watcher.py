from web3 import Web3
import time

WSS_URL = ""  # your WebSocket RPC URL
w3 = Web3(Web3.LegacyWebSocketProvider(WSS_URL))

# keep this at module‐scope so it persists across blocks
seen_contracts = set()

def handle_new_block(block_hash):
    block = w3.eth.get_block(block_hash, full_transactions=False)
    # track addresses seen just in this block to avoid duplicates within the same block
    block_seen = set()

    for tx_hash in block.transactions:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt.contractAddress:
                addr = receipt.contractAddress
            else:
                addr = receipt.to

            if not addr:
                continue

            # skip if we've already printed this contract ever, or already saw it in this block
            if addr in seen_contracts or addr in block_seen:
                continue

            code = w3.eth.get_code(addr)
            if code == b"":
                continue

            balance = w3.eth.get_balance(addr)
            if balance > int(0.1 * 1e18):
                print(f"[+] {addr} | {balance/1e18:.2f} ETH")
                seen_contracts.add(addr)
                block_seen.add(addr)

        except Exception as e:
            print(f"[!] TX {tx_hash.hex()} error: {e}")

# subscribe to new blocks
block_filter = w3.eth.filter("latest")
print("[ℹ️] Listening for new blocks…")

while True:
    for new_hash in block_filter.get_new_entries():
        handle_new_block(new_hash)
    time.sleep(0.5)
