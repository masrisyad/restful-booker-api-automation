# RESTful Booker API Automation

REST API automation testing framework for the RESTful Booker API using Python, pytest, GitHub Actions, and Jira.

## Project Overview

This project demonstrates a maintainable REST API automation framework with integration between:

- Jira
- GitHub
- pytest
- GitHub Actions
- Automated Test Reporting

API under test:

https://restful-booker.herokuapp.com

API documentation:

https://restful-booker.herokuapp.com/apidoc/

## Technology Stack

- Python 3.12+
- pytest
- requests
- python-dotenv
- jsonschema
- Faker
- pytest-html
- pytest-xdist
- GitHub
- GitHub Actions
- Jira

## Project Structure

```text
restful-booker-api-automation/
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── src/
│   ├── clients/
│   │   ├── __init__.py
│   │   └── base_client.py
│   │
│   ├── schemas/
│   └── utils/
│
├── tests/
│   ├── smoke/
│   ├── regression/
│   ├── negative/
│   ├── e2e/
│   └── conftest.py
│
├── reports/
├── docs/
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md


Test Categories
The framework supports the following pytest markers:
smoke
regression
negative
e2e

Run Smoke Tests:
python -m pytest -m smoke

Run Regression Tests:
python -m pytest -m regression

Run Negative Tests:
python -m pytest -m negative

Run End-to-End Tests:
python -m pytest -m e2e

Local Setup
1. Clone Repository
git clone https://github.com/masrisyad/restful-booker-api-automation.git

2. Open Project Directory
cd restful-booker-api-automation

3. Create Virtual Environment
Windows:
python -m venv .venv

4. Activate Virtual Environment
PowerShell:
.\.venv\Scripts\Activate.ps1

5. Install Dependencies
pip install -r requirements.txt

Environment Configuration
Copy:
.env.example

to:
.env

Example configuration:
BASE_URL=https://restful-booker.herokuapp.com
API_USERNAME=admin
API_PASSWORD=password123
REQUEST_TIMEOUT=30

The .env file must not be committed to Git.
Running Tests
Run all automated tests:
python -m pytest

Run Smoke Tests:
python -m pytest -m smoke

Run Regression Tests:
python -m pytest -m regression

Run Negative Tests:
python -m pytest -m negative

Run End-to-End Tests:
python -m pytest -m e2e

Test Reporting
The framework supports HTML and JUnit XML test reporting.
Generate HTML report:
python -m pytest --html=reports/report.html --self-contained-html

Generate JUnit XML report:
python -m pytest --junitxml=reports/junit.xml

Generate both reports:
python -m pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml

Expected report output:
reports/
├── report.html
└── junit.xml

Jira Traceability
Development work follows Jira work item naming conventions.
Branch Naming
Format:
<JIRA-KEY>-<short-description>

Example:
RBA-2-setup-api-automation-framework

Commit Naming
Format:
<JIRA-KEY> <description>

Example:
RBA-2 setup API automation framework

Pull Request Naming
Format:
<JIRA-KEY> <description>

Example:
RBA-2 Setup API Automation Framework

Planned API Coverage
The automation project will cover:
- Health Check
- Authentication
- Get Booking
- Create Booking
- Full Update Booking
- Partial Update Booking
- Delete Booking
- Booking Filters
- Negative API Scenarios
- JSON Schema Validation
- End-to-End Booking Lifecycle
- Smoke Test Suite
- Regression Test Suite
- Automated Test Reporting
- GitHub Actions CI
- Jira and GitHub Integration
- CI Test Result Integration with Jira
Automation Architecture
Tests
  ↓
API Clients
  ↓
Base Client
  ↓
Requests
  ↓
RESTful Booker API

Development Workflow
Jira Work Item
      ↓
Feature Branch
      ↓
Automation Development
      ↓
Commit
      ↓
Push
      ↓
Pull Request
      ↓
GitHub Actions
      ↓
Smoke / Regression Tests
      ↓
Test Report
      ↓
PASS / FAIL
      ↓
Jira Update

Current Status
Current implementation:
- Project repository initialized
- Python virtual environment configured
- Required dependencies installed
- pytest configured
- Environment configuration prepared
- Reusable Base API Client created
- Test folder structure created
- Smoke, Regression, Negative, and E2E markers configured
Next implementation:
- Health Check API Automation
- Authentication API Automation
- Booking CRUD Automation
- CI/CD Integration