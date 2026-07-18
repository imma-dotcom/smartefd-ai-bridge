# test_session4.py  —  DEBUG VERSION
import requests

BASE = "http://localhost:5000"

print("\n" + "=" * 50)
print("  SMARTEFD API TESTS")
print("=" * 50)

# ── Test 1: Health check ──
print("\n[1] Health Check...")
response = requests.get(BASE + "/health")
print(f"    Status Code : {response.status_code}")
print(f"    Response    : {response.json()}")

# ── Test 2: Submit a low-risk receipt ──
print("\n[2] Submitting LOW risk receipt...")
payload = {
    "business_uin"  : "TRA-API-001",
    "amount_tzs"    : 12000,
    "item_category" : "food",
    "cashier_id"    : "CASHIER-A"
}
response = requests.post(BASE + "/receipt", json=payload)
print(f"    Status Code  : {response.status_code}")
print(f"    Raw response : {response.text}")   # print raw first

# Only parse JSON if server returned 201
if response.status_code == 201:
    data = response.json()
    print(f"    Receipt ID   : {data['receipt_id']}")
    print(f"    Risk Score   : {data['risk_score']}")
    print(f"    Verdict      : {data['risk_flag']}")
else:
    print("    POST failed — check Terminal 1 for the server error")

# ── Test 3: Submit a critical receipt ──
print("\n[3] Submitting CRITICAL risk receipt...")
payload = {
    "business_uin"  : "TRA-API-002",
    "amount_tzs"    : 9000000,
    "item_category" : "fuel",
    "cashier_id"    : "UNKNOWN"
}
response = requests.post(BASE + "/receipt", json=payload)
print(f"    Status Code  : {response.status_code}")
print(f"    Raw response : {response.text}")

if response.status_code == 201:
    data = response.json()
    print(f"    Risk Score   : {data['risk_score']}")
    print(f"    Verdict      : {data['risk_flag']}")

# ── Test 4: Get risk profile ──
print("\n[4] Fetching risk profile...")
response = requests.get(BASE + "/risk/TRA-API-002")
print(f"    Status Code  : {response.status_code}")
print(f"    Raw response : {response.text}")

if response.status_code == 200:
    data = response.json()
    print(f"    Total Receipts : {data['total_receipts']}")
    print(f"    Max Amount     : TZS {data['max_amount_tzs']:,}")

# ── Test 5: Validation test ──
print("\n[5] Testing validation...")
payload = {
    "business_uin" : "TRA-INCOMPLETE",
    "amount_tzs"   : 5000
}
response = requests.post(BASE + "/receipt", json=payload)
print(f"    Status Code  : {response.status_code}  (should be 400)")
print(f"    Raw response : {response.text}")

print("\n" + "=" * 50)
print("  TESTS COMPLETE")
print("=" * 50 + "\n")