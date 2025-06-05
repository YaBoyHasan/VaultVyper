from web3 import Web3

def get_web3():
    RPC_URL = "https://eth-mainnet.public.blastapi.io"
    return Web3(Web3.HTTPProvider(RPC_URL))