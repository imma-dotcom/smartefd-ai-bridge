# test_session2.py

from receipt import create_receipt
from risk_engine import calculate_risk, display_risk_report

#-----Test 1: Small normal food sale - should be low -
r1 = create_receipt("TRA-DAR-001", 8000, "food", "CASHIER-A")
r1 = calculate_risk(r1)
display_risk_report(r1)

#-----Test 2: Large electronics sale - should be HIGH ---
r2 = create_receipt("TRA-DSM-099", 4500000, "electronics", "CASHIER-B")
r2 = calculate_risk(r2)
display_risk_report(r2)

#----Test 3: Suspicious - no cashier, fuel, huge round amount----
r3 = create_receipt("TRA-MWZ-007", 5000000, "fuel", "UNKNOWN")
r3 = calculate_risk(r3)
display_risk_report(r3)

#-----Test 4: Check the score is acrually a number yu can use--
print(f"Report 3 score as a number: {r3['risk_score']}")
print(f"Is it above 75? {r3['risk_score'] > 75}")