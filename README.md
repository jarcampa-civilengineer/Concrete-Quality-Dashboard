# Concrete Quality Dashboard

A small Python command-line application that records concrete quality-control
observations and generates a standalone HTML dashboard.

## Features
- Record concrete placement and test information: project, location, pour date,
  mix ID, supplier, delivery ticket, and volume.
- Capture slump, concrete temperature, air content, and 7-/28-day compressive strength.
- Enter project-specific screening limits for slump, temperature, and air content.
- Flag records for review when entered measurements fall outside those entered limits.
- Display record count, flagged count, total recorded volume, average slump, and
  average entered 28-day strength.
- Generate an HTML dashboard and export a CSV test register.
- Store records locally in JSON.

## Project files
- `main.py` — command-line menu and data entry.
- `models.py` — concrete test record data model.
- `validators.py` — required field, date, and numeric validation.
- `quality_manager.py` — record creation and range screening.
- `storage.py` — JSON persistence.
- `dashboard.py` — dashboard metrics, register display, and HTML generation.

## Requirements
Python 3.9 or newer. Uses only the Python standard library.

## Run
```bash
python main.py
```

Choose **Generate HTML dashboard** to create `reports/concrete_quality_dashboard.html`.
Open that file in a web browser. Choose **Export test register to CSV** to create
`reports/concrete_quality_register.csv`.

## Important engineering note
This application is a recordkeeping and preliminary screening aid. The range checks
use limits manually entered for each record; they do not establish compliance or
acceptance. Confirm requirements against approved mix designs, project specifications,
applicable ASTM/AASHTO procedures, testing agency documentation, and the responsible
engineer's quality-control plan. Compressive-strength results should be interpreted
using the applicable acceptance criteria and required test ages.
