"""
Ledger — Hospital Management System (Flask version)
-----------------------------------------------------
A small Flask web app that serves the patient-record UI and handles all
the logic (add, search, assign, update status, delete) in Python on the
server. Patient data is stored in a JSON file (patients.json) so it
survives restarts.

Run with:
    python app.py
Then open http://127.0.0.1:5000 in a browser.
"""

from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "patients.json"

# Departments and the doctors available in each one.
DEPARTMENTS = {
    "General Medicine": ["Dr. Sharma", "Dr. Verma"],
    "Cardiology": ["Dr. Mehta", "Dr. Rao"],
    "Orthopedics": ["Dr. Singh", "Dr. Iyer"],
    "Pediatrics": ["Dr. Kapoor", "Dr. Nair"],
    "ENT": ["Dr. Joshi"],
}

STATUSES = ["Waiting", "In Consultation", "Completed", "Cancelled"]


# ---------------------------------------------------------
# Simple JSON-file storage helpers
# ---------------------------------------------------------
def load_patients():
    """Read all patients from the JSON file. Returns an empty list if the
    file doesn't exist yet or is empty/corrupted."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_patients(patients):
    """Write the full patient list back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(patients, f, indent=2)


def next_id(patients):
    """Work out the next patient ID (one higher than the current max)."""
    if not patients:
        return 1
    return max(p["id"] for p in patients) + 1


# ---------------------------------------------------------
# Page route — serves the HTML page
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", departments=DEPARTMENTS, statuses=STATUSES)


# ---------------------------------------------------------
# API routes — the page's JavaScript calls these
# ---------------------------------------------------------
@app.route("/api/patients", methods=["GET"])
def get_patients():
    """Return all patients, optionally filtered by a search query (?q=...)
    matching name or ID — this is the Search Patient feature."""
    patients = load_patients()
    query = request.args.get("q", "").strip().lower()
    if query:
        patients = [
            p for p in patients
            if query in p["name"].lower() or query == str(p["id"])
        ]
    return jsonify(patients)


@app.route("/api/patients", methods=["POST"])
def add_patient():
    """Add a new patient. This is the Add Patient feature."""
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    age = data.get("age")
    gender = data.get("gender", "")
    contact = (data.get("contact") or "").strip()
    department = data.get("department", "")
    doctor = data.get("doctor", "")

    if not name or not isinstance(age, int) or age < 0:
        return jsonify({"error": "A name and a valid age are required."}), 400

    patients = load_patients()
    patient = {
        "id": next_id(patients),
        "name": name,
        "age": age,
        "gender": gender,
        "contact": contact,
        "department": department,
        "doctor": doctor,
        "status": "Waiting",  # every new patient starts in the queue
    }
    patients.append(patient)
    save_patients(patients)
    return jsonify(patient), 201


@app.route("/api/patients/<int:patient_id>", methods=["PATCH"])
def update_patient(patient_id):
    """Update a patient's consultation status. This is the Update
    Consultation Status feature (department/doctor reassignment uses the
    same route with different fields, if you extend it later)."""
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")

    if new_status not in STATUSES:
        return jsonify({"error": "Invalid status."}), 400

    patients = load_patients()
    for p in patients:
        if p["id"] == patient_id:
            p["status"] = new_status
            save_patients(patients)
            return jsonify(p)

    return jsonify({"error": "Patient not found."}), 404


@app.route("/api/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    """Remove a patient from the records."""
    patients = load_patients()
    remaining = [p for p in patients if p["id"] != patient_id]

    if len(remaining) == len(patients):
        return jsonify({"error": "Patient not found."}), 404

    save_patients(remaining)
    return jsonify({"deleted": patient_id})


if __name__ == "__main__":
    app.run(debug=True)
