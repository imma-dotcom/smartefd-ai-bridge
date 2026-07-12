# test_session1.py
# Run this to verify Session 1 works correctly.

from receipt import create_receipt, display_receipt

#---Test 1: A normal food sale -----
receipt1 = create_receipt(
    business_uin = "TRA- DAR-001",
    amount_tzs = 15000,
    item_category = "food",
    cashier_id = "CASHIER-A"
)

display_receipt(receipt1)

#---- Test 2: A large electronics sale -----
receipt2 = create_receipt(
    business_uin  = "TRA-DSM-099",
    amount_tzs    = 4500000,
    item_category = "electronics",
    cashier_id = "CASHIER-B"
)

display_receipt(receipt2)

# -----Test 3: Check that each receipt ID is unique ---------
print("Are the IDs different?", receipt1["receipt_id"] != receipt2["receipt_id"])

#-----Test 4: Access a single field -----
print("Business that issued receipt  2:", receipt2["business_uin"])