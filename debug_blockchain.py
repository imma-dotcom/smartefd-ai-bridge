# debug_blockchain.py
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

FUJI_RPC     = "https://api.avax-test.network/ext/bc/C/rpc"
CONTRACT     = "0x8F241Ab76e7aAB7B4D10711E9fEB650EC8c41f7F"
PRIVATE_KEY  = os.getenv("WALLET_PRIVATE_KEY")

print("\n" + "=" * 50)
print("  BLOCKCHAIN DEBUG")
print("=" * 50)

# ── Check 1: Is .env loading? ──
print("\n[1] Checking .env file...")
if PRIVATE_KEY is None:
    print("    PROBLEM: WALLET_PRIVATE_KEY is None")
    print("    The .env file is not being found OR")
    print("    the variable name is spelled wrong inside it")
elif PRIVATE_KEY == "0xYourMetaMaskPrivateKeyHere":
    print("    PROBLEM: You forgot to replace the placeholder")
elif len(PRIVATE_KEY) < 60:
    print(f"    PROBLEM: Key too short ({len(PRIVATE_KEY)} chars)")
    print("    A private key should be 64 hex chars after 0x")
else:
    print(f"    OK: Key loaded ({len(PRIVATE_KEY)} chars)")

# ── Check 2: Derive wallet address ──
print("\n[2] Deriving wallet address from key...")
try:
    w3      = Web3(Web3.HTTPProvider(FUJI_RPC))
    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"    Wallet address : {account.address}")
    print(f"    Copy this and compare with your MetaMask account")
except Exception as e:
    print(f"    FAILED: {e}")

# ── Check 3: AVAX balance ──
print("\n[3] Checking AVAX balance...")
try:
    balance_wei  = w3.eth.get_balance(account.address)
    balance_avax = w3.from_wei(balance_wei, "ether")
    print(f"    Balance : {balance_avax:.4f} AVAX")
    if balance_avax < 0.01:
        print("    WARNING: Balance too low — need at least 0.01 AVAX for gas")
        print("    Get free test AVAX at: https://faucet.avax.network")
    else:
        print("    OK: Enough balance for transactions")
except Exception as e:
    print(f"    FAILED: {e}")

# ── Check 4: Is wallet the contract owner? ──
print("\n[4] Checking contract ownership...")
try:
    OWNER_ABI = [{
        "inputs":[], "name":"owner",
        "outputs":[{"internalType":"address","name":"","type":"address"}],
        "stateMutability":"view","type":"function"
    }]
    address  = Web3.to_checksum_address(CONTRACT)
    contract = w3.eth.contract(address=address, abi=OWNER_ABI)
    owner    = contract.functions.owner().call()
    print(f"    Contract owner : {owner}")
    print(f"    Your wallet    : {account.address}")
    if owner.lower() == account.address.lower():
        print("    OK: You are the owner — issueReceipt will work")
    else:
        print("    PROBLEM: Your wallet is NOT the contract owner")
        print("    The contract was deployed from a different account")
        print("    Solution: redeploy from the MetaMask account")
        print("    whose private key is in your .env file")
except Exception as e:
    print(f"    FAILED: {e}")

print("\n" + "=" * 50 + "\n")