# app.py  —  COMPLETE FILE WITH ALL ROUTES
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from receipt import create_receipt
from risk_engine import calculate_risk
from history_tracker import record_receipt, analyze_business, load_history
from blockchain import issue_receipt_onchain, verify_receipt_onchain

app = Flask(__name__)
CORS(app)

# In-memory receipt store for blockchain lookups
receipt_store = {}

# ── Serve HTML files ──────────────────────────────────
@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/verify.html")
def serve_verify():
    return send_from_directory(".", "verify.html")

# ── Health check ──────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status"  : "running",
        "system"  : "SmartEFD AI Bridge",
        "version" : "1.0.0"
    }), 200

# ── Submit receipt ────────────────────────────────────
@app.route("/receipt", methods=["POST"])
def submit_receipt():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No JSON body received"}), 400
    required = ["business_uin", "amount_tzs", "item_category", "cashier_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    r = create_receipt(
        business_uin  = data["business_uin"],
        amount_tzs    = data["amount_tzs"],
        item_category = data["item_category"],
        cashier_id    = data["cashier_id"]
    )
    r = calculate_risk(r)
    count = record_receipt(r)
    receipt_store[r["receipt_id"]] = r
    return jsonify({
        "status"        : "success",
        "receipt_id"    : r["receipt_id"],
        "business_uin"  : r["business_uin"],
        "amount_tzs"    : r["amount_tzs"],
        "risk_score"    : r["risk_score"],
        "risk_flag"     : r["risk_flag"],
        "receipt_count" : count,
        "risk_detail"   : r["risk_detail"]
    }), 201

# ── Send receipt to blockchain ────────────────────────
@app.route("/receipt/onchain", methods=["POST"])
def send_receipt_onchain():
    data       = request.get_json()
    receipt_id = data.get("receipt_id")
    if not receipt_id or receipt_id not in receipt_store:
        return jsonify({"error": "Receipt not found. Submit it first."}), 404
    receipt = receipt_store[receipt_id]
    result  = issue_receipt_onchain(receipt)
    return jsonify(result), 200

# ── Get risk profile for one business ─────────────────
@app.route("/risk/<uin>", methods=["GET"])
def get_risk_profile(uin):
    summary = analyze_business(uin)
    if summary.get("status") == "NO HISTORY":
        return jsonify({"error": f"No history found for {uin}"}), 404
    return jsonify(summary), 200

# ── Get all businesses summary ─────────────────────────
@app.route("/summary", methods=["GET"])
def get_summary():
    history   = load_history()
    summaries = []
    for uin in history.keys():
        s = analyze_business(uin)
        if s.get("status") != "NO HISTORY":
            summaries.append(s)
    summaries.sort(key=lambda x: x.get("high_risk_count", 0), reverse=True)
    return jsonify(summaries), 200

# ── Verify receipt on blockchain ───────────────────────
@app.route("/verify/<receipt_id>", methods=["GET"])
def verify_receipt(receipt_id):
    result = verify_receipt_onchain(receipt_id)
    return jsonify(result), 200

# ── Start server ───────────────────────────────────────
if __name__ == "__main__":
    print("\n  SmartEFD AI Bridge — API Server Starting...")
    print("  Local  : http://localhost:5000")
    print("  Network: run 'ipconfig' and use your IPv4 address\n")
    app.run(debug=True, port=5000, host="0.0.0.0")