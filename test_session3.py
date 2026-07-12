from receipt import create_receipt
from risk_engine import calculate_risk
from history_tracker import record_receipt, display_business_summary

#-----Simulate TRA-DAR-001: normal active food business ------
print("Recording receipt for    TRA-DAR-001....")
for amount in [12000, 18000, 9500, 22000, 15000]:
    r = create_receipt("TRA-DAR-001", amount, "food", "CASHIER-A")
    r = calculate_risk(r)
    count = record_receipt(r)
    print(f"    Saved receipt #{count}  | Score: {r['risk_score']}  |   {r['risk_flag']}")

#-----Simulate TRA-DSM-099:  large suspicious electronics -----
print("\nRecording receipts for TRA-DSM-099...")
for amount in [4500000, 8000000]:
    r = create_receipt("TRA-DSM-099", amount, "electronics", "UNKNOWN")
    r = calculate_risk(r)
    count = record_receipt(r)
    print(f"    Saved receipt #{count}  |   Score: {r['risk_score']}    |   {r['risk_flag']}")

#------Analyze and display full history ----------
print("\n --------BUSINESS ANALYSIS ----------")
display_business_summary("TRA-DAR-001")
display_business_summary("TRA-DSM-099")

#-------Test a business with zero history -----
display_business_summary("TRA-MWZ-GHOST")