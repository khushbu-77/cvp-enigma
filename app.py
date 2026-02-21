from flask import Flask, render_template, request
import uuid
import sqlite3

from utils.db_utlis import init_db, insert_certificate, get_certificate_by_id
from utils.hash_utils import normalize_data, generate_hash

app = Flask(__name__)

# Ensure database + table exist at startup
init_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template(
        "home.html",
        breadcrumbs=[{"label": "Home", "url": "/"}]
    )


# ---------------- SELECT ROLE ----------------
@app.route("/selectrole")
def select_role():
    return render_template(
        "selectrole.html",
        breadcrumbs=[
            {"label": "Home", "url": "/"},
            {"label": "Select Role", "url": "/selectrole"}
        ]
    )


# ---------------- USER LOGIN ----------------
@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template(
        "user_login.html",
        breadcrumbs=[
            {"label": "Home", "url": "/"},
            {"label": "User Login", "url": "/user-login"}
        ]
    )


# ---------------- USER DASHBOARD ----------------
@app.route("/user-dashboard", methods=["POST"])
def user_dashboard():
    name = request.form["name"]
    dob = request.form["dob"]

    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()

    # Total certificates issued to this user
    cursor.execute(
        "SELECT COUNT(*) FROM certificates WHERE name=? AND dob=?",
        (name, dob)
    )
    total_certificates = cursor.fetchone()[0]

    # Valid certificates (no revocation/expiry logic yet)
    valid_certificates = total_certificates

    # Placeholder stats (can be extended later)
    total_verifications = 0
    issues = 0

    conn.close()

    return render_template(
        "user_dashboard.html",
        total=total_certificates,
        valid=valid_certificates,
        verifications=total_verifications,
        issues=issues,
        breadcrumbs=[
            {"label": "Home", "url": "/"},
            {"label": "User Dashboard", "url": "#"}
        ]
    )


# ---------------- ISSUE CERTIFICATE ----------------
@app.route("/issue", methods=["GET", "POST"])
def issue_certificate():
    if request.method == "GET":
        return render_template(
            "issue.html",
            breadcrumbs=[
                {"label": "Home", "url": "/"},
                {"label": "Select Role", "url": "/selectrole"},
                {"label": "Issue Certificate", "url": "/issue"}
            ]
        )

    # ⭐ Mandatory fields (used for hashing + verification)
    name = request.form["name"]
    father_name = request.form["father_name"]
    dob = request.form["dob"]
    course = request.form["course"]
    issue_date = request.form["issue_date"]
    issuer = request.form["issuer"]

    # 🔐 Generate unique certificate ID
    certificate_id = f"CERT-{uuid.uuid4().hex[:10].upper()}"

    # 🔐 Normalize ONLY mandatory fields
    normalized_data = normalize_data(
        certificate_id,
        name,
        father_name,
        dob,
        course,
        issue_date,
        issuer
    )

    # 🔐 Generate hash
    cert_hash = generate_hash(normalized_data)

    # 💾 Store in database
    insert_certificate(
        certificate_id,
        name,
        father_name,
        dob,
        course,
        issuer,
        issue_date,
        cert_hash
    )

    # ✅ Issued success page
    return render_template(
        "issued.html",
        certificate_id=certificate_id,
        breadcrumbs=[
            {"label": "Home", "url": "/"},
            {"label": "Select Role", "url": "/selectrole"},
            {"label": "Issued", "url": "#"}
        ]
    )


# ---------------- VERIFY CERTIFICATE ----------------
@app.route("/verify", methods=["GET", "POST"])
def verify_certificate():
    if request.method == "GET":
        return render_template(
            "verify.html",
            breadcrumbs=[
                {"label": "Home", "url": "/"},
                {"label": "Verify Certificate", "url": "/verify"}
            ]
        )

    certificate_id = request.form["certificate_id"]

    # 🔍 Fetch from DB using certificate ID
    record = get_certificate_by_id(certificate_id)

    if not record:
        return render_template(
            "result.html",
            status="invalid",
            breadcrumbs=[
                {"label": "Home", "url": "/"},
                {"label": "Verify Certificate", "url": "/verify"},
                {"label": "Result", "url": "#"}
            ]
        )

    # 🔁 Recalculate hash using SAME mandatory fields
    normalized_data = normalize_data(
        record["certificate_id"],
        record["name"],
        record["father_name"],
        record["dob"],
        record["course"],
        record["issue_date"],
        record["issuer"]
    )

    recalculated_hash = generate_hash(normalized_data)

    status = "valid" if recalculated_hash == record["hash"] else "tampered"

    return render_template(
        "result.html",
        status=status,
        record=record,
        breadcrumbs=[
            {"label": "Home", "url": "/"},
            {"label": "Verify Certificate", "url": "/verify"},
            {"label": "Result", "url": "#"}
        ]
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)