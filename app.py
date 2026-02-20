from flask import Flask, render_template, request
import uuid

from utils.db_utlis import init_db, insert_certificate, get_certificate_by_id
from utils.hash_utils import normalize_data, generate_hash

app = Flask(__name__)

# Ensure database + table exist at startup
init_db()


@app.route("/")
def home():
    return render_template("issue.html")


@app.route("/issue", methods=["POST"])
def issue_certificate():
    name = request.form["name"]
    father_name = request.form["father_name"]
    dob = request.form["dob"]
    course = request.form["course"]
    issue_date = request.form["issue_date"]

    certificate_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"

    normalized = normalize_data(
        certificate_id, name, father_name, dob, course, issue_date, "My Institute"
    )
    cert_hash = generate_hash(normalized)

    insert_certificate(
        certificate_id,
        name,
        father_name,
        dob,
        course,
        "My Institute",
        issue_date,
        cert_hash
    )

    return render_template(
        "result.html",
        status="issued",
        certificate_id=certificate_id
    )


@app.route("/verify")
def verify_page():
    return render_template("verify.html")


@app.route("/verify/result", methods=["POST"])
def verify_result():
    certificate_id = request.form["certificate_id"]

    record = get_certificate_by_id(certificate_id)

    if not record:
        return render_template("result.html", status="invalid")

    normalized = normalize_data(
        record["certificate_id"],
        record["name"],
        record["father_name"],
        record["dob"],
        record["course"],
        record["issue_date"],
        record["issuer"]
    )
    recalculated_hash = generate_hash(normalized)

    if recalculated_hash == record["hash"]:
        return render_template("result.html", status="valid", record=record)
    else:
        return render_template("result.html", status="tampered")


if __name__ == "__main__":
    app.run(debug=True)