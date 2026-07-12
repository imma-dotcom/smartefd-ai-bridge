# risk_engine.py  —  COMPLETE FILE
import datetime

CATEGORY_RISK = {
    "food"        : 5,
    "clothing"    : 8,
    "agriculture" : 8,
    "services"    : 12,
    "electronics" : 18,
    "fuel"        : 20,
    "liquor"      : 20,
}

def score_amount(amount_tzs):
    if amount_tzs < 10_000:
        return 0
    elif amount_tzs < 500_000:
        return 10
    elif amount_tzs < 5_000_000:
        return 25
    else:
        return 40

def score_category(item_category):
    category = item_category.lower()
    return CATEGORY_RISK.get(category, 10)

def score_time(timestamp_str):
    try:
        dt   = datetime.datetime.fromisoformat(timestamp_str)
        hour = dt.hour
    except Exception:
        return 10
    if 6 <= hour < 20:
        return 0
    elif 20 <= hour < 23:
        return 10
    else:
        return 20

def score_missing_fields(receipt):
    points = 0
    if receipt["cashier_id"] == "UNKNOWN":
        points += 10
    amount = receipt["amount_tzs"]
    if amount > 100_000 and amount % 1_000_000 == 0:
        points += 10
    return points

def calculate_risk(receipt):
    amount_pts   = score_amount(receipt["amount_tzs"])
    category_pts = score_category(receipt["item_category"])
    time_pts     = score_time(receipt["timestamp"])
    missing_pts  = score_missing_fields(receipt)

    total_score  = min(amount_pts + category_pts + time_pts + missing_pts, 100)

    if total_score <= 25:
        verdict = "LOW ✅"
    elif total_score <= 50:
        verdict = "MEDIUM ⚠️"
    elif total_score <= 75:
        verdict = "HIGH 🔶"
    else:
        verdict = "CRITICAL 🚨"

    receipt["risk_score"]  = total_score
    receipt["risk_flag"]   = verdict
    receipt["risk_detail"] = {
        "amount_pts"   : amount_pts,
        "category_pts" : category_pts,
        "time_pts"     : time_pts,
        "missing_pts"  : missing_pts,
    }
    return receipt

def display_risk_report(receipt):
    detail = receipt["risk_detail"]
    print("\n" + "=" * 45)
    print("     SMARTEFD — RISK ANALYSIS REPORT")
    print("=" * 45)
    print(f"  Receipt ID   : {receipt['receipt_id']}")
    print(f"  Business UIN : {receipt['business_uin']}")
    print(f"  Amount (TZS) : {receipt['amount_tzs']:,.0f}")
    print("-" * 45)
    print("  SCORE BREAKDOWN:")
    print(f"    Amount risk    : {detail['amount_pts']:>3} pts")
    print(f"    Category risk  : {detail['category_pts']:>3} pts")
    print(f"    Time risk      : {detail['time_pts']:>3} pts")
    print(f"    Missing fields : {detail['missing_pts']:>3} pts")
    print(f"                     {'─' * 7}")
    print(f"    TOTAL SCORE    : {receipt['risk_score']:>3} / 100")
    print("-" * 45)
    print(f"  VERDICT  -->  {receipt['risk_flag']}")
    print("=" * 45 + "\n")