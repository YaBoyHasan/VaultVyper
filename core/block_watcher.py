from web3 import Web3
from utils.web3_provider import get_web3

w3 = get_web3()

def get_new_contracts(from_block=None, to_block=None):
    latest = w3.eth.block_number
    from_block = from_block or (latest - 1)
    to_block = to_block or latest

    print(f"[ℹ️] Blocks {from_block} → {to_block}")
    candidates = set()

    for block_number in range(from_block, to_block + 1):
        try:
            block = w3.eth.get_block(block_number, full_transactions=True)
        except Exception as e:
            print(f"[!] Block {block_number} error: {e}")
            continue

        for tx in block.transactions:
            try:
                if tx.to is None:
                    receipt = w3.eth.get_transaction_receipt(tx.hash)
                    addr = receipt.contractAddress
                else:
                    addr = Web3.to_checksum_address(tx.to)

                if addr and addr not in candidates:
                    code = w3.eth.get_code(addr)
                    balance = w3.eth.get_balance(addr)
                    if code != b"" and balance > 0.1 * 1e18:
                        print(f"[+] {addr} | {balance / 1e18:.2f} ETH")
                        candidates.add(addr)
            except Exception as e:
                print(f"[!] TX {tx.hash.hex()} error: {e}")

    return list(candidates)
