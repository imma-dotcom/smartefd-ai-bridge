# receipt.py
#-------------------------------------------------------------
#WHAT THIS FILE DOES:
#Defines what a "receipt" looks like in our
#system and give us tools to create them.
#--------------------------------------------------------------

import datetime
import time



#WHY A DICTIONARY
#A dictionary lets us store many differen oueces 
#of inrormation about a)NE receipt,
#all under one variable name.

def create_receipt(business_uin, amount_tzs, item_category, cashier_id="UNKNOWN"):
    """
    Builds a standardized receipt  dictionary.

    Paremeters:
    ----------
    business_uin   : str  - TRA Unique ID for the business (e.g "TRA-001")
    amount_tzs     : float - Transaction amount in Tanzania Shillings
    item_category  : str   - Type of goods (e.g "food", "electronics", "clothing")
    cashier_id     : str   - ID of the cashier who issued the receipt

    Returns:
    --------
    dict - A complete receipt for processing 
    """

    receipt = {
        "receipt_id"    : generate_receipt_id(),
        "business_uin"  : business_uin,
        "amount_tzs"    : amount_tzs,
        "item_category" : item_category,
        "cashier_id"    : cashier_id,
        "timestamp"    : datetime.datetime.now().isoformat(),
        "date"          : datetime.date.today().isoformat(),
        "risk_flag"     : None, #will be filled by risk engine later
        "on_chain"      : False, #True once sent to Avalanche blockchain
    }

    return receipt


def generate_receipt_id():
    """
    Creates a unique receipt ID using the current time in milliseconds.
    WHY milliseconds? Two receipts issued at the same second will still 
    get different IDs because milliseconds are more precise.
    """
    ms = int(time.time() * 1000)
    return f"EFD-TZ-{ms}"


def display_receipt(receipt):
    """
    Prints a receipt in a clean, readagle format.
    WHY a separate function? So we can reuse this
    print logic anywhere in th project.
    """

    print("\n" + "=" * 45)
    print("    SMARTEFD AI BRIDGE - RECEIPT")
    print("=" * 45)
    print(f" Receipt ID     : {receipt['receipt_id']}")
    print(f" Business UIN   : {receipt['business_uin']}")
    print(f" Amount (TZs)   : {receipt['amount_tzs']}")
    print(f" Category       : {receipt['item_category']}")
    print(f" Cashier        : {receipt['cashier_id']}")
    print(f" Date           : {receipt['date']}")
    print(f" Time           : {receipt['timestamp'][11:19]}")
    print(f" On-chain       : {'✅ Yes' if receipt['on_chain'] else '⏳ Pending'}")
    print(f" Risk Flag      : {receipt['risk_flag'] or 'None'}")
    print("=" * 45 + "\n")    

    