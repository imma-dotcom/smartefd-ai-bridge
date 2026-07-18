# test_blockchain.py
from receipt import create_receipt
from risk_engine import calculate_risk
from blockchain import (
    check_connection,
    hash_receipt,
    issue_receipt_onchain,
    verify_receipt_onchain,
    get_business_count
)

print("\n" + "=" * 52)
print("  SMARTEFD - BLOCKCHAIN SESSION TESTS")
print("=" * 52)

# ── Test 1: Connection ──
print("\n[1] Connecting to Avalanche Fuji...")
result = check_connection()
if result["connected"]:
    print(f"    Network  : {result['network']}")
    print(f"    Chain ID : {result['chain_id']}")
    print(f"    Block    : {result['latest_block']}")
    print(f"    Contract : {result['contract']}")
else:
    print(f"    FAILED   : {result['error']}")
    exit()

# ── Test 2: Hash a receipt ──
print("\n[2] Hashing a receipt...")
r = create_receipt("TRA-CHAIN-001", 75000, "electronics", "CASHIER-X")
r = calculate_risk(r)
h = hash_receipt(r)
print(f"    Receipt ID   : {r['receipt_id']}")
print(f"    Hash preview : {h[:20]}...{h[-8:]}")
print(f"    Hash length  : {len(h)} chars (must be 66)")

# ── Test 3: Issue receipt on-chain ──
print("\n[3] Writing receipt to Avalanche Fuji...")
result = issue_receipt_onchain(r)
if result["success"]:
    print(f"    Status     : SUCCESS ✅")
    print(f"    TX Hash    : {result['tx_hash'][:20]}...")
    print(f"    Block      : {result['block_number']}")
    print(f"    SnowTrace  : {result['snowtrace_url']}")
else:
    print(f"    Status     : FAILED ❌")
    print(f"    Error      : {result.get('error')}")
    if result.get("snowtrace_url"):
        print(f"    SnowTrace  : {result['snowtrace_url']}")
        print("    Open that URL in your browser to see the revert reason")

# ── Test 4: Verify from blockchain ──
print("\n[4] Verifying receipt from blockchain...")
verify = verify_receipt_onchain(r["receipt_id"])
print(f"    Verified     : {verify['verified']}")
if verify["verified"]:
    print(f"    Business     : {verify['business_uin']}")
    print(f"    Amount (TZS) : {verify['amount_tzs']:,}")
    print(f"    Message      : {verify['message']}")
else:
    print(f"    Message      : {verify.get('message') or verify.get('error')}")

# ── Test 5: Business receipt count ──
print("\n[5] Checking on-chain receipt count...")
count = get_business_count("TRA-CHAIN-001")
print(f"    Business     : {count.get('business_uin')}")
print(f"    On-chain     : {count.get('onchain_count')} receipt(s)")

print("\n" + "=" * 52)
print("  BLOCKCHAIN TESTS COMPLETE")
print("=" * 52 + "\n")