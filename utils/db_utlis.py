import sqlite3

DB_NAME = "certificates.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        certificate_id TEXT PRIMARY KEY,
        name TEXT,
        father_name TEXT,
        dob TEXT,
        course TEXT,
        issuer TEXT,
        issue_date TEXT,
        hash TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_certificate(
    certificate_id,
    name,
    father_name,
    dob,
    course,
    issuer,
    issue_date,
    cert_hash
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO certificates (
        certificate_id,
        name,
        father_name,
        dob,
        course,
        issuer,
        issue_date,
        hash
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        certificate_id,
        name,
        father_name,
        dob,
        course,
        issuer,
        issue_date,
        cert_hash
    ))

    conn.commit()
    conn.close()


def get_certificate_by_id(certificate_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM certificates WHERE certificate_id = ?",
        (certificate_id,)
    )

    row = cursor.fetchone()
    conn.close()
    return row