import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


CASE = {
    "caseReferenceId": "CASE-000001",
    "createdOn": "March 15, 2026",
    "lastStatus": "New",
    "caseType": "Payment (SWIFT)",
    "systemId": "SYS-DEMO-20260315-001",
    "caseAge": "1d",
    "tat": "1d",
    "caseDescription": "DEMO20260315001 USD 125,000.00 - SAMPLE PAYMENT - Vessel",
    "status": "In Progress",
    "reviewedBy": "Alex Reviewer",
    "owner": "Jordan Analyst",
    "escalateTo": "Find items",
    "escalationReason": "",
    "escalationDate": "",
    "valueDate": "March 15, 2026",
    "remitterName": "Sample Trading Company Ltd.",
    "remitterAccountNumber": "",
    "remittingFi": "Demo Bank A",
    "beneficiary": "Example Logistics Pte Ltd",
    "beneficiaryAccountNumber": "",
    "beneficiaryFi": "Demo Bank B",
    "sanctionsProgram": "Sample Watchlist - vessel",
}


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/cases/<case_reference_id>")
def get_case(case_reference_id):
    if case_reference_id != CASE["caseReferenceId"]:
        return jsonify({"error": "Case not found"}), 404

    return jsonify(CASE)


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
    )
