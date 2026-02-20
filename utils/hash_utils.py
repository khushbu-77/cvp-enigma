import hashlib


def normalize_data(certificate_id, name, father_name, dob, course, issue_date, issuer):
    return "|".join([
        certificate_id.strip().lower(),
        name.strip().lower(),
        father_name.strip().lower(),
        dob.strip(),
        course.strip().lower(),
        issuer.strip().lower(),
        issue_date.strip()
    ])


def generate_hash(normalized_string):
    return hashlib.sha256(normalized_string.encode()).hexdigest()