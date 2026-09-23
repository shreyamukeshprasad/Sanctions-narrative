import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
FE_DIR = BASE_DIR / "FE"


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


CASES = {
    "CASE-000001": {
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
    },
    "CASE-000002": {
        "caseReferenceId": "CASE-000002",
        "createdOn": "March 16, 2026",
        "lastStatus": "Escalated",
        "caseType": "Trade Finance",
        "systemId": "SYS-DEMO-20260316-002",
        "caseAge": "2d",
        "tat": "1d",
        "caseDescription": "DEMO20260316002 EUR 82,450.25 - SAMPLE GOODS - Port match",
        "status": "Escalated",
        "reviewedBy": "Morgan Reviewer",
        "owner": "Taylor Analyst",
        "escalateTo": "Compliance Review Team",
        "escalationReason": "Potential vessel name match",
        "escalationDate": "March 17, 2026",
        "valueDate": "March 16, 2026",
        "remitterName": "Northbridge Imports LLC",
        "remitterAccountNumber": "",
        "remittingFi": "Demo Bank C",
        "beneficiary": "Harborline Supplies Ltd.",
        "beneficiaryAccountNumber": "",
        "beneficiaryFi": "Demo Bank D",
        "sanctionsProgram": "Sample Watchlist - port",
    },
    "CASE-000003": {
        "caseReferenceId": "CASE-000003",
        "createdOn": "March 18, 2026",
        "lastStatus": "Pending Review",
        "caseType": "Payment (ACH)",
        "systemId": "SYS-DEMO-20260318-003",
        "caseAge": "4h",
        "tat": "1d",
        "caseDescription": "DEMO20260318003 USD 9,875.00 - SAMPLE SERVICES - Name match",
        "status": "Pending Review",
        "reviewedBy": "Riley Reviewer",
        "owner": "Casey Analyst",
        "escalateTo": "Find items",
        "escalationReason": "",
        "escalationDate": "",
        "valueDate": "March 18, 2026",
        "remitterName": "Blue Ridge Advisory Inc.",
        "remitterAccountNumber": "",
        "remittingFi": "Demo Bank E",
        "beneficiary": "Greenfield Consulting Co.",
        "beneficiaryAccountNumber": "",
        "beneficiaryFi": "Demo Bank F",
        "sanctionsProgram": "Sample Watchlist - individual",
    },
    "CASE-000004": {
        "caseReferenceId": "CASE-000004",
        "createdOn": "March 19, 2026",
        "lastStatus": "Closed",
        "caseType": "Payment (SWIFT)",
        "systemId": "SYS-DEMO-20260319-004",
        "caseAge": "3d",
        "tat": "2d",
        "caseDescription": "DEMO20260319004 GBP 44,200.10 - SAMPLE INVOICE - False positive",
        "status": "Closed",
        "reviewedBy": "Jamie Reviewer",
        "owner": "Avery Analyst",
        "escalateTo": "Find items",
        "escalationReason": "",
        "escalationDate": "",
        "valueDate": "March 19, 2026",
        "remitterName": "Oak Street Manufacturing Ltd.",
        "remitterAccountNumber": "",
        "remittingFi": "Demo Bank G",
        "beneficiary": "Summit Parts Distribution",
        "beneficiaryAccountNumber": "",
        "beneficiaryFi": "Demo Bank H",
        "sanctionsProgram": "Sample Watchlist - entity",
    },
    "CASE-000005": {
        "caseReferenceId": "CASE-000005",
        "createdOn": "March 20, 2026",
        "lastStatus": "New",
        "caseType": "Document Screening",
        "systemId": "SYS-DEMO-20260320-005",
        "caseAge": "30m",
        "tat": "1d",
        "caseDescription": "DEMO20260320005 JPY 12,500,000 - SAMPLE DOCUMENT - Country match",
        "status": "New",
        "reviewedBy": "Sam Reviewer",
        "owner": "Drew Analyst",
        "escalateTo": "Find items",
        "escalationReason": "",
        "escalationDate": "",
        "valueDate": "March 20, 2026",
        "remitterName": "Pacific Sample Exporters",
        "remitterAccountNumber": "",
        "remittingFi": "Demo Bank I",
        "beneficiary": "Metro Equipment Services",
        "beneficiaryAccountNumber": "",
        "beneficiaryFi": "Demo Bank J",
        "sanctionsProgram": "Sample Watchlist - country",
    },
}


@app.get("/")
def index():
    return send_from_directory(FE_DIR, "case-summary.html")


@app.get("/version")
@app.get("/api/version")
def version():
    return jsonify({
        "app": "sanctions-narrative",
        "version": "test-app-001",
        "source": "BE/app.py",
    })


@app.get("/health")
@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/cases/<case_reference_id>")
@app.get("/api/cases/<case_reference_id>")
def get_case(case_reference_id):
    case = CASES.get(case_reference_id.upper())

    if not case:
        return jsonify({"error": "Case not found"}), 404

    return jsonify(case)


@app.post("/llm")
@app.post("/api/llm")
def call_llm():
    data = request.get_json(silent=True) or request.form or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Request body must include a non-empty 'prompt'."}), 400

    try:
        from llm_call import ask_llm

        return jsonify({"response": ask_llm(prompt)})
    except Exception as exc:
        return jsonify({"error": "LLM call failed", "details": str(exc)}), 500


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host="0.0.0.0",
        port=int(os.getenv("DATABRICKS_APP_PORT", os.getenv("PORT", "5000"))),
    )
