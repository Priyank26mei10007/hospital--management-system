# Ledger — Hospital Management System

A patient record management web app built with Python and Flask. It lets
a clinic front desk add patients, search existing records, assign a
department and doctor, and track each patient's consultation status —
all through a browser interface backed by a Python server.

## Features

- **Add Patient** — register a new patient with name, age, gender, and
  contact number; each patient gets an auto-generated ID.
- **Search Patient** — filter patients by (partial) name or by ID.
- **Display Patient Details** — every patient's full record is shown in
  the list, including department, doctor, and current status.
- **Doctor / Department Assignment** — assign a patient to a department
  and a specific doctor from that department when adding them.
- **Consultation Status** — update a patient's status between Waiting,
  In Consultation, Completed, and Cancelled directly from the list.
- **Delete Patient** — remove a record no longer needed.

All logic (adding, searching, updating, deleting) runs in Python on the
server (`app.py`); the page itself only displays data and sends
requests to it.

## Requirements

- Python 3.8 or later
- Flask (listed in `requirements.txt`)

## Setup

1. Clone the repository:
  bash
  git clone 
  https://github.com/Priyank26mei10007/hospital--management-system.git
  cd hospital--management-system
  
2. Confirm Python 3 is installed:
   ```bash
   python --version
   ```
   If this isn't recognized, install Python 3 from
   [python.org/downloads](https://www.python.org/downloads/) first.
3. Install the project's dependencies:
   ```bash
   pip install -r requirements.txt
   ```

No further configuration is required.

## Running the project

From the project's root folder (the one containing `app.py`), run:

```bash
python app.py
```

You should see output similar to:

```
 * Running on http://127.0.0.1:5000
```

Open that address in a browser to use the app. Press `Ctrl+C` in the
terminal to stop the server.

## Usage

1. Fill in the **Add patient** form on the left — name, age, gender,
   contact, department, and doctor — and submit it. The new patient
   starts with status "Waiting".
2. Use the **search box** above the patient list to find a patient by
   name or ID.
3. Change a patient's status directly from the dropdown next to their
   row as they move through Waiting → In Consultation → Completed.
4. Click the ✕ button on a row to remove a patient.
5. The stats at the top (total patients, waiting, in consultation,
   completed) update automatically.

## Data storage

Patient records are stored in `patients.json`, a file Flask creates
automatically in the project folder the first time you add a patient.
Data persists between runs — stopping and restarting the server does
not clear it. This file is excluded from version control via
`.gitignore`, since it's generated data rather than source code.

## Project structure

```
.
├── app.py                # Flask app — routes and data logic
├── requirements.txt      # Python dependencies (Flask)
├── templates/
│   └── index.html        # Page UI, talks to app.py via fetch requests
├── patients.json          # Created automatically — patient data (git-ignored)
└── README.md              # This file
```

## Notes

This project was built as part of the Python Essentials course
evaluation. The backend (`app.py`) is written in plain Python using
Flask's routing and JSON file storage — no database or external
services are required to run it.
