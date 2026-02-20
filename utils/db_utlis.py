import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
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


def insert_certificate(certificate_id, name, father_name, dob, course, issuer, issue_date, hash_value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO certificates VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (certificate_id, name, father_name, dob, course, issuer, issue_date, hash_value))

    conn.commit()
    conn.close()


def get_certificate_by_id(certificate_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM certificates WHERE certificate_id = ?
    """, (certificate_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "certificate_id": row[0],
        "name": row[1],
        "father_name": row[2],
        "dob": row[3],
        "course": row[4],
        "issuer": row[5],
        "issue_date": row[6],
        "hash": row[7]
    }