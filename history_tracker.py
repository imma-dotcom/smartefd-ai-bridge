#saves every receipt to json file so that
#system remembers past behaviour then analyse that history
#to find suspicious pattern across time

import json
import os
import datetime

HISTORY_FILE = "transaction_history.json"

#FUCTION 1 - Load the history file

def load_history():
    """
    Reads the JSON file and return its contents as python dictionary
    
    WHY CHECK os.path.exists FIRST
    If we try to open a file that does not exist, Python crashes.
    we return an empty dict instead so the first run works without errors
    """
    if not os.path.exists(HISTORY_FILE):
        return {}
    
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)  #json.load reads file » python dict
    
# FUNCTION 2 -save the history file

def save_history(history):
    """
    write the full history dictionary back to json file,

    Why indent=2?
    Makes the JSON file human-readable with proper indentation when
    you open it in vs code.
    """

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2) #json.dump  writes dict → filel


# FUNCTION 3 - record one receipt into history

def record_receipt(receipt):
    """adds a processed receipt to the history file.

    """
    history = load_history()

    uin = receipt["business_uin"]

    if uin not in history:
        history[uin] = []

    #compact summary of the receipt
    summary = {
        "receipt_id"    : receipt["receipt_id"],
        "amount_tzs"    : receipt["amount_tzs"],
        "date"          : receipt["date"],
        "timestamp"     : receipt["timestamp"],
        "risk_score"    : receipt.get("risk_score", None),
        "risk_flag"     : receipt.get("risk_flag", None),
    }

    history[uin].append(summary)
    save_history(history)

    return len(history[uin])

#FUNCTION 4 - Detect inactivity gaps

def detect_gaps(sorted_dates):
    """
    Receives a sorted list of date strings 
    find any gap of 7+ days(mosty business operate at least weekly) where no receipt were issued"""

    gaps = []

    for i in range(1, len(sorted_dates)):
        d1 = datetime.date.fromisoformat(sorted_dates[i - 1])
        d2 = datetime.date.fromisoformat(sorted_dates[i])

        gap_days = (d2 - d1).days#days btn these two dates

        if gap_days >= 7:
            gaps.append({
                "from"  : sorted_dates[i - 1], 
                "to"    : sorted_dates[i],
                "days"  : gap_days,
            })

    return gaps

#FUNCTION 5 - Analyze a business's full history

def analyze_business(uin):
    """load all receipt for a business and returns a dictionary of statistics
    and risk indicators"""

    history = load_history()
    receipts = history.get(uin, [])

    if not receipts:
        return {"status": "NO HISTORY", "uin": uin}
    
    #basic statics
    total   = len(receipts)
    amounts = [r["amount_tzs"] for r in receipts]
    avg     = sum(amounts) / total
    maximum = max(amounts)

    #get unique active dates, sorted oldest to newest
    dates = sorted(set(r["date"] for r in receipts))

    #count how many receipt scored above 50 (medium+)
    high_risk = sum(
        1 for r in receipts
        if r.get("risk_score") and r["risk_score"] > 50
    )

    gaps = detect_gaps(dates)

    return{
        "uin"               : uin, 
        "total_receipts"    : total, 
        "avg_amount_tzs"    : round(avg),
        "max_amount_tzs"    : maximum,
        "active_days"       : len(dates),
        "first_seen"        : dates[0],
        "last_seen"         : dates[-1],
        "high_risk_count"   : high_risk,
        "gaps"              : gaps,
    }

#FUNCTION 6 - Display business summary

def display_business_summary(uin):
    """Prints a readable history report for one business."""

    summary = analyze_business(uin)

    if summary.get("status") == "NO HISTORY":
        print(f"\n No history found for {uin}\n")
        return
    
    print("\n" + "=" * 45)
    print("     SMARTEFD - BUSINESS HISTORY SUMMARY")
    print("=" * 45)
    print(f"    Business UIN    : {summary['uin']}")
    print(f"    Total Receipts  : {summary['total_receipts']}")
    print(f"    Avg Amount      : TZS {summary['avg_amount_tzs']}")
    print(f"    Max Amount      : TZS {summary['max_amount_tzs']}")
    print(f"    Active Days     : {summary['active_days']}")
    print(f"    First Seen      : {summary['first_seen']}")
    print(f"    Last Seen       : {summary['last_seen']}")
    print("-" * 45)

    if summary["gaps"]:
        print("     WARNING - INACTIVITY GAPS DETECTED:")
        for g in summary["gaps"]:
            print(f"    {g['from']}     to      {g['to']}   ({g['days']} days silent)")

    else:
        print(" No suspicious inactivity gaps found")

    print("=" * 45 + "\n")