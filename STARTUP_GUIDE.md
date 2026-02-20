# Certificate Validation Platform - Startup Guide

## Quick Start

The application is fully synced and ready to run! Follow these steps to get started:

### 1. Verify the installation
```bash
python test_app.py
```
This will run comprehensive tests and confirm everything is working correctly.

### 2. Start the Flask application
```bash
python app.py
```

### 3. Open in your browser
Navigate to: **http://localhost:5000**

---

## Features

### ✅ Issue Certificate
- **Route:** `/` (Home page)
- **Form Fields:**
  - Student Name (required)
  - Father's Name (required)
  - Date of Birth (required)
  - Course (required)
  - Issue Date (required)
- **Output:** Certificate ID that can be used for verification

### ✅ Verify Certificate
- **Route:** `/verify`
- **Input:** Certificate ID
- **Result:** Certificate validity status with full details if valid

---

## Database Schema

The application uses SQLite with the following schema:

```
certificates table:
├── certificate_id (TEXT, PRIMARY KEY)
├── name (TEXT)
├── father_name (TEXT) ← NEW
├── dob (TEXT) ← NEW
├── course (TEXT)
├── issuer (TEXT)
├── issue_date (TEXT)
└── hash (TEXT)
```

---

## File Structure

```
cvp-enigma/
├── app.py                          # Main Flask application
├── test_app.py                     # Test suite
├── database.db                     # SQLite database (auto-created)
├── requirements.txt                # Python dependencies
├── README.md
├── templates/
│   ├── issue.html                  # Certificate issuance form (modern theme)
│   ├── verify.html                 # Certificate verification (modern theme)
│   └── result.html                 # Results display (modern theme)
└── utils/
    ├── __init__.py
    ├── db_utlis.py                 # Database operations
    └── hash_utils.py               # Hash generation & normalization
```

---

## Recent Updates

✅ **Synced with new issue.html:**
- Added `father_name` field
- Added `dob` (Date of Birth) field
- Updated database schema to support new fields
- Updated `app.py` to handle new fields
- Updated `hash_utils.py` to include new fields in hash generation
- Modernized all HTML templates with blue-green gradient theme (#4e73df to #1cc88a)
- Added comprehensive test suite

---

## Styling

All templates use a modern, responsive design with:
- **Color Scheme:** Blue (#4e73df) to Green (#1cc88a) gradient
- **Typography:** Segoe UI, sans-serif
- **Components:** Rounded buttons, smooth transitions, focus states
- **Responsive:** Works on desktop and mobile devices

---

## Testing

Run the test suite to verify all components:

```bash
python test_app.py
```

Tests include:
1. Database module import and initialization
2. Hash utility functions
3. Certificate insertion and retrieval
4. Flask app setup and routes
5. HTML template validation

---

## API Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Display issue certificate form |
| POST | `/issue` | Process certificate issuance |
| GET | `/verify` | Display verification form |
| POST | `/verify/result` | Process certificate verification |

---

## How It Works

1. **Issue Phase:**
   - User fills out certificate details
   - System generates unique certificate ID
   - Data is normalized and hashed using SHA-256
   - Certificate stored in database

2. **Verify Phase:**
   - User enters certificate ID
   - System retrieves certificate from database
   - Data is re-normalized and rehashed
   - Hash is compared to stored hash
   - Result displays status (Valid/Invalid/Tampered)

---

## Requirements

- Python 3.8+
- Flask 3.1.2
- SQLite3 (included with Python)

See `requirements.txt` for complete list.

---

## Troubleshooting

**Port 5000 already in use?**
```bash
python app.py --port 5001
```

**Database corruption?**
Delete `database.db` and restart the app to create a fresh database.

**Import errors?**
Ensure you're in the `cvp-enigma` directory and have the correct Python environment.

---

## License & Credits

Certificate Validation Platform - Built with Flask & SQLite
