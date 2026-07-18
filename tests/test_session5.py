# test_session5.py
# ─────────────────────────────────────────────────────
# FINAL INTEGRATION TEST
# Simulates a real day of EFD activity across
# 10 different Tanzanian businesses and prints
# a full system summary report.
# ─────────────────────────────────────────────────────

import requests
import json

BASE = "http://localhost:5000"

# ── Simulated businesses with realistic TZ data ──
BUSINESSES = [
    {
        "uin": "TRA-DSM-FOOD-001",
        "name": "Mama Lishe Kariakoo",
        "receipts": [
            {"amount": 8000,  "cat": "food",    "cashier": "CASHIER-A"},
            {"amount": 12000, "cat": "food",    "cashier": "CASHIER-A"},
            {"amount": 9500,  "cat": "food",    "cashier": "CASHIER-A"},
        ]
    },
    {
        "uin": "TRA-DSM-ELEC-002",
        "name": "Dar Tech Electronics",
        "receipts": [
            {"amount": 4500000, "cat": "electronics", "cashier": "CASHIER-B"},
            {"amount": 8000000, "cat": "electronics", "cashier": "UNKNOWN"},
        ]
    },
    {
        "uin": "TRA-MWZ-FUEL-003",
        "name": "Mwanza Fuel Station",
        "receipts": [
            {"amount": 5000000, "cat": "fuel", "cashier": "UNKNOWN"},
            {"amount": 3000000, "cat": "fuel", "cashier": "UNKNOWN"},
        ]
    },
    {
        "uin": "TRA-ARU-CLOTH-004",
        "name": "Arusha Fashion House",
        "receipts": [
            {"amount": 150000, "cat": "clothing", "cashier": "CASHIER-C"},
            {"amount": 280000, "cat": "clothing", "cashier": "CASHIER-C"},
            {"amount": 95000,  "cat": "clothing", "cashier": "CASHIER-C"},
        ]
    },
    {
        "uin": "TRA-DSM-LIQ-005",
        "name": "Msumbiji Bar & Grill",
        "receipts": [
            {"amount": 1000000, "cat": "liquor", "cashier": "UNKNOWN"},
            {"amount": 2000000, "cat": "liquor", "cashier": "UNKNOWN"},
        ]
    },
]

# ─────────────────────────────────────────────────────
# STEP 1: Submit all receipts through the API
# ─────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("   SMARTEFD AI BRIDGE — FULL INTEGRATION TEST")
print("=" * 55)
print("\n📡 STEP 1: Submitting receipts through Flask API...\n")

all_results = []

for biz in BUSINESSES:
    print(f"  Business: {biz['name']} ({biz['uin']})")

    for r in biz["receipts"]:
        payload = {
            "business_uin"  : biz["uin"],
            "amount_tzs"    : r["amount"],
            "item_category" : r["cat"],
            "cashier_id"    : r["cashier"]
        }
        response = requests.post(BASE + "/receipt", json=payload)

        if response.status_code == 201:
            data = response.json()
            result = {
                "uin"     : biz["uin"],
                "name"    : biz["name"],
                "amount"  : r["amount"],
                "score"   : data["risk_score"],
                "verdict" : data["risk_flag"]
            }
            all_results.append(result)
            print(f"    TZS {r['amount']:>12,.0f}  →  Score: {data['risk_score']:>3}  {data['risk_flag']}")
        else:
            print(f"    ERROR: {response.json()}")

    print()

# ─────────────────────────────────────────────────────
# STEP 2: Fetch risk profile for each business
# ─────────────────────────────────────────────────────

print("\n📊 STEP 2: Fetching risk profiles...\n")

risk_profiles = []

for biz in BUSINESSES:
    response = requests.get(BASE + "/risk/" + biz["uin"])

    if response.status_code == 200:
        profile = response.json()
        risk_profiles.append({
            "name"    : biz["name"],
            "profile" : profile
        })

# ─────────────────────────────────────────────────────
# STEP 3: Print the TRA Summary Dashboard
# ─────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("   TRA SMARTEFD — DAILY COMPLIANCE DASHBOARD")
print("=" * 55)

total_amount   = sum(r["amount"]  for r in all_results)
total_receipts = len(all_results)
critical_count = sum(1 for r in all_results if "CRITICAL" in r["verdict"])
high_count     = sum(1 for r in all_results if "HIGH"     in r["verdict"])
low_count      = sum(1 for r in all_results if "LOW"      in r["verdict"])
avg_score      = sum(r["score"] for r in all_results) // total_receipts

print(f"\n  Total Receipts Processed : {total_receipts}")
print(f"  Total Value (TZS)        : {total_amount:,.0f}")
print(f"  Average Risk Score       : {avg_score} / 100")
print(f"  LOW ✅ receipts          : {low_count}")
print(f"  HIGH 🔶 receipts         : {high_count}")
print(f"  CRITICAL 🚨 receipts     : {critical_count}")

print("\n" + "-" * 55)
print("  BUSINESS RISK LEAGUE TABLE")
print("-" * 55)

# Sort businesses by their max receipt score — highest risk first
sorted_results = sorted(
    risk_profiles,
    key=lambda x: x["profile"]["high_risk_count"],
    reverse=True
)

for i, item in enumerate(sorted_results, 1):
    p = item["profile"]
    print(f"\n  #{i}  {item['name']}")
    print(f"       Receipts   : {p['total_receipts']}")
    print(f"       Avg Amount : TZS {p['avg_amount_tzs']:,}")
    print(f"       High-Risk  : {p['high_risk_count']} transactions")
    flag = "🚨 REFER FOR AUDIT" if p["high_risk_count"] >= 2 else "✅ MONITOR"
    print(f"       Status     : {flag}")

print("\n" + "=" * 55)
print("   PYTHON BACKEND — ALL SESSIONS COMPLETE ✅")
print("=" * 55)
print("""
  Sessions completed:
  ✅ Session 1 — Receipt Data Model       (receipt.py)
  ✅ Session 2 — Risk Scoring Engine      (risk_engine.py)
  ✅ Session 3 — Transaction History      (history_tracker.py)
  ✅ Session 4 — Flask REST API           (app.py)
  ✅ Session 5 — Full Integration Test    (test_session5.py)

  Next phase → Blockchain (SmartEFD.sol on Avalanche Fuji)
""")