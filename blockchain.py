# blockchain.py

import hashlib
import os
from web3 import Web3
from dotenv import load_dotenv

# WHY load_dotenv()?
# This reads our .env file and makes WALLET_PRIVATE_KEY
# available via os.getenv() — so the key never appears
# directly in our code.
load_dotenv()

# ── CONFIGURATION ────────────────────────────────────
FUJI_RPC_URL      = "https://api.avax-test.network/ext/bc/C/rpc"
CONTRACT_ADDRESS  = "0x8F241Ab76e7aAB7B4D10711E9fEB650EC8c41f7F"
PRIVATE_KEY       = os.getenv("WALLET_PRIVATE_KEY")

# ── CONTRACT ABI ─────────────────────────────────────

CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string",  "name": "receiptId",   "type": "string"},
            {"internalType": "string",  "name": "businessUin", "type": "string"},
            {"internalType": "bytes32", "name": "receiptHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "amountTzs",   "type": "uint256"}
        ],
        "name": "issueReceipt",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "receiptId", "type": "string"}
        ],
        "name": "verifyReceipt",
        "outputs": [
            {"internalType": "bool",    "name": "isValid",     "type": "bool"},
            {"internalType": "string",  "name": "businessUin", "type": "string"},
            {"internalType": "bytes32", "name": "receiptHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "amountTzs",   "type": "uint256"},
            {"internalType": "uint256", "name": "timestamp",   "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "businessUin", "type": "string"}
        ],
        "name": "getReceiptCount",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


# ─────────────────────────────────────────────────────
# INTERNAL HELPERS — used by the functions below
# ─────────────────────────────────────────────────────

def get_connection():
    """
    Opens a connection to Avalanche Fuji Testnet.
    WHY SEPARATE FUNCTION?
    Every public function needs a connection. Putting
    this in one place means if the RPC URL ever changes,
    we fix it in exactly one spot.
    """
    w3 = Web3(Web3.HTTPProvider(FUJI_RPC_URL))
    if not w3.is_connected():
        raise ConnectionError(
            "Cannot connect to Avalanche Fuji. Check your internet."
        )
    return w3


def get_contract(w3):
    """
    Returns a Python object that represents our
    SmartEFD.sol contract. We use this object to
    call functions on the contract.

    WHY to_checksum_address()?
    Avalanche addresses are case-sensitive for security
    (EIP-55 checksum). This converts our address to the
    correct mixed-case format that web3.py requires.
    """
    address = Web3.to_checksum_address(CONTRACT_ADDRESS)
    return w3.eth.contract(address=address, abi=CONTRACT_ABI)


# ─────────────────────────────────────────────────────
# FUNCTION 1 — Check blockchain connection health
# ─────────────────────────────────────────────────────

def check_connection():
    """
    Quick health check. Returns connection status,
    chain ID, and latest block number.
    """
    try:
        w3    = get_connection()
        block = w3.eth.block_number
        return {
            "connected"    : True,
            "network"      : "Avalanche Fuji Testnet",
            "chain_id"     : w3.eth.chain_id,
            "latest_block" : block,
            "contract"     : CONTRACT_ADDRESS
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}


# ─────────────────────────────────────────────────────
# FUNCTION 2 — Generate SHA-256 hash of a receipt
# ─────────────────────────────────────────────────────

def hash_receipt(receipt):
    
    data_string = (
        f"{receipt['receipt_id']}"
        f"{receipt['business_uin']}"
        f"{receipt['amount_tzs']}"
        f"{receipt['date']}"
        f"{receipt['item_category']}"
    )

    # hashlib.sha256 → .digest() gives raw bytes
    hash_bytes = hashlib.sha256(
        data_string.encode("utf-8")
    ).digest()

    # Convert bytes to hex string with 0x prefix
    return "0x" + hash_bytes.hex()


# ─────────────────────────────────────────────────────
# FUNCTION 3 — Write receipt hash to blockchain
# ─────────────────────────────────────────────────────

def issue_receipt_onchain(receipt):
    if not PRIVATE_KEY:
        return {"success": False, "error": "WALLET_PRIVATE_KEY missing"}

    try:
        w3       = get_connection()
        contract = get_contract(w3)
        account  = w3.eth.account.from_key(PRIVATE_KEY)

        hash_hex   = hash_receipt(receipt)
        hash_bytes = bytes.fromhex(hash_hex[2:])
        nonce      = w3.eth.get_transaction_count(account.address)

        # ── EIP-1559 transaction format ──────────────────
        # WHY EIP-1559?
        # Avalanche uses this modern format instead of legacy
        # gasPrice. It sets a maxFeePerGas (ceiling) and a
        # maxPriorityFeePerGas (tip to validators).
        latest        = w3.eth.get_block("latest")
        base_fee      = latest["baseFeePerGas"]
        priority_fee  = w3.to_wei("2", "gwei")
        max_fee       = (base_fee * 2) + priority_fee

        tx = contract.functions.issueReceipt(
            receipt["receipt_id"],
            receipt["business_uin"],
            hash_bytes,
            int(receipt["amount_tzs"])
        ).build_transaction({
            "chainId"              : 43113,
            "gas"                  : 300000,
            "maxFeePerGas"         : max_fee,
            "maxPriorityFeePerGas" : priority_fee,
            "nonce"                : nonce,
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

        # Handle web3.py v5 vs v6 attribute name difference
        try:
            raw = signed_tx.raw_transaction
        except AttributeError:
            raw = signed_tx.rawTransaction

        tx_hash     = w3.eth.send_raw_transaction(raw)
        tx_hash_hex = tx_hash.hex()
        if not tx_hash_hex.startswith("0x"):
            tx_hash_hex = "0x" + tx_hash_hex

        snowtrace = f"https://testnet.snowtrace.io/tx/{tx_hash_hex}"

        print(f"    TX sent → {snowtrace}")
        print("    Waiting for confirmation...")

        on_chain = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
        success  = on_chain.status == 1

        if not success:
            return {
                "success" : False,
                "error"   : "Transaction reverted — check SnowTrace",
                "tx_hash" : tx_hash_hex,
                "snowtrace_url" : snowtrace
            }

        # ← ADD THIS LINE HERE — defines block before using it
        block = w3.eth.get_block(on_chain.blockNumber)

        return {
            "success"         : True,
            "tx_hash"         : tx_hash_hex,
            "receipt_hash"    : hash_hex,
            "block_number"    : on_chain.blockNumber,
            "block_timestamp" : block.timestamp,      # ← now block exists
            "snowtrace_url"   : snowtrace
        }

    except Exception as e:
        import traceback
        err = str(e) if str(e) else traceback.format_exc()
        return {"success": False, "error": err}
# ─────────────────────────────────────────────────────
# FUNCTION 4 — Read receipt from blockchain (free)
# ─────────────────────────────────────────────────────

def verify_receipt_onchain(receipt_id):
    
    try:
        w3       = get_connection()
        contract = get_contract(w3)

        # .call() executes a view function — read only
        result = contract.functions.verifyReceipt(receipt_id).call()

        is_valid, business_uin, receipt_hash, amount_tzs, timestamp = result

        if not is_valid:
            return {
                "verified"   : False,
                "receipt_id" : receipt_id,
                "message"    : "Receipt not found on blockchain"
            }

        return {
            "verified"     : True,
            "receipt_id"   : receipt_id,
            "business_uin" : business_uin,
            "amount_tzs"   : amount_tzs,
            "receipt_hash" : "0x" + receipt_hash.hex(),
            "timestamp"    : timestamp,
            "message"      : "Receipt is authentic and blockchain-verified"
        }

    except Exception as e:
        return {"verified": False, "error": str(e)}


# ─────────────────────────────────────────────────────
# FUNCTION 5 — Count on-chain receipts for a business
# ─────────────────────────────────────────────────────

def get_business_count(business_uin):
    """
    Returns the number of receipts a business has stored
    on the blockchain. Free read operation.
    """
    try:
        w3       = get_connection()
        contract = get_contract(w3)
        count    = contract.functions.getReceiptCount(
            business_uin
        ).call()
        return {
            "business_uin"  : business_uin,
            "onchain_count" : count
        }
    except Exception as e:
        return {"error": str(e)}