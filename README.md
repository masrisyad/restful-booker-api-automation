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
API_USERNAME=<your-api-username>
API_PASSWORD=<your-api-password>
REQUEST_TIMEOUT=30

Authentication credentials must be stored in the local `.env` file and must never be committed to Git.

For CI/CD execution, credentials will be provided using GitHub Actions Secrets.

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

## Test Reporting

Setiap CI run menghasilkan tiga file:

```text
reports/
├── stakeholder-report.html  # Ringkasan Bahasa Indonesia untuk stakeholder
├── report.html              # Detail teknis pytest-html
└── junit.xml                # Hasil machine-readable
```

Generate report teknis dan JUnit secara lokal:

```powershell
python -m pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml
```

Render stakeholder report tanpa mengunggah ke layanan eksternal:

```powershell
python scripts/publish_test_results.py --render-only
```

Report stakeholder menampilkan status akhir, jumlah test lulus/gagal/error/dilewati, durasi, kesimpulan sederhana, dan detail teknis kegagalan. Nilai sensitif seperti password, token, authorization header, dan cookie tidak boleh ditambahkan ke test output.

## Cloudflare R2 Report Storage

Publication memakai Cloudflare R2 S3-compatible API. Tambahkan konfigurasi berikut ke `.env` lokal atau GitHub Actions Secrets:

```env
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
R2_PUBLIC_BASE_URL=https://reports.example.com
```

Prasyarat R2:

1. Buat bucket khusus report.
2. Buat API token dengan akses object read/write hanya untuk bucket tersebut.
3. Aktifkan public access atau custom domain untuk report yang boleh dibuka stakeholder.
4. Isi `R2_PUBLIC_BASE_URL` dengan origin publik tersebut.

Object disimpan dengan path immutable:

```text
<repository>/<jira-key>/<github-run-id>-<attempt>/<report-file>
```

Kode tidak mengubah bucket menjadi publik. Kebijakan public access dan lifecycle/retention diatur di Cloudflare.

## Jira Test Result Integration

Setelah report berhasil diunggah ke R2, GitHub Actions menambahkan komentar langsung melalui Jira Cloud REST API v3. Jira Automation rule atau incoming webhook tidak diperlukan.

Tambahkan konfigurasi berikut ke `.env` lokal atau GitHub Actions Secrets:

```env
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=
JIRA_API_TOKEN=
```

Setup Jira:

1. Gunakan akun Jira yang boleh melihat issue target dan menambahkan komentar.
2. Buat Jira API token untuk akun tersebut.
3. Simpan email dan token hanya di `.env` lokal atau GitHub Actions Secrets.
4. Jangan menaruh token pada source code, report, log, komentar, atau Pull Request.

CI mengirim komentar Atlassian Document Format ke endpoint berikut dengan HTTP Basic Auth:

```text
POST {JIRA_BASE_URL}/rest/api/3/issue/{issueKey}/comment
```

Komentar berisi status akhir, total/lulus/gagal/error/dilewati, durasi, kesimpulan, repository/branch/commit, link report R2, dan link GitHub Actions bila tersedia.

Jira key dideteksi berurutan dari input manual, nama branch PR, judul PR, atau commit message. Jika seluruh konfigurasi R2 atau Jira kosong, proses lokal atau PR dari fork tetap membuat report dan melewati integrasi terkait. Konfigurasi parsial dianggap error agar salah setup terlihat jelas. Komentar Jira memerlukan URL stakeholder report yang berhasil diunggah ke R2.

## GitHub Actions Reporting Flow

1. Jalankan smoke test pada Pull Request, atau suite pilihan pada manual run.
2. Hasilkan `pytest-html` dan JUnit XML.
3. Render stakeholder report walau test gagal.
4. Upload folder `reports/` sebagai GitHub Actions artifact selama 30 hari.
5. Upload report ke R2 dan kirim ringkasan ke Jira jika secret tersedia.
6. Pertahankan exit code pytest sehingga test gagal tetap membuat workflow gagal.

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

## Development Workflow

This project follows a Jira-based Git workflow.

For complete Git usage, branch naming, commit conventions, Pull Request flow, and daily development steps, see:

[GIT-WORKFLOW.md](GIT-WORKFLOW.md)