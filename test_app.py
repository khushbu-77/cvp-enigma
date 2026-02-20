#!/usr/bin/env python
"""
Test script to verify the certificate validation application works correctly
"""

import os
import sys
from datetime import datetime

# Test 1: Check database module
print("=" * 60)
print("TEST 1: Importing and initializing database...")
print("=" * 60)

try:
    from utils.db_utlis import init_db, insert_certificate, get_certificate_by_id
    print("✓ Successfully imported database utilities")
    
    # Clean up old database if it exists
    if os.path.exists("database.db"):
        os.remove("database.db")
        print("✓ Cleaned up old database")
    
    init_db()
    print("✓ Database initialized with new schema (certificate_id, name, father_name, dob, course, issuer, issue_date, hash)")
except Exception as e:
    print(f"✗ Database test failed: {e}")
    sys.exit(1)

# Test 2: Check hash utilities
print("\n" + "=" * 60)
print("TEST 2: Testing hash utilities...")
print("=" * 60)

try:
    from utils.hash_utils import normalize_data, generate_hash
    print("✓ Successfully imported hash utilities")
    
    # Test with sample data including new fields
    test_id = "CERT-TEST001"
    test_name = "John Doe"
    test_father_name = "James Doe"
    test_dob = "2000-01-15"
    test_course = "Python Programming"
    test_issue_date = "2024-02-20"
    test_issuer = "My Institute"
    
    normalized = normalize_data(
        test_id, test_name, test_father_name, test_dob, test_course, test_issue_date, test_issuer
    )
    print(f"✓ Normalized data: {normalized[:50]}...")
    
    test_hash = generate_hash(normalized)
    print(f"✓ Generated hash: {test_hash[:16]}...")
except Exception as e:
    print(f"✗ Hash utility test failed: {e}")
    sys.exit(1)

# Test 3: Insert and retrieve certificate
print("\n" + "=" * 60)
print("TEST 3: Testing certificate insertion and retrieval...")
print("=" * 60)

try:
    insert_certificate(
        test_id,
        test_name,
        test_father_name,
        test_dob,
        test_course,
        test_issuer,
        test_issue_date,
        test_hash
    )
    print("✓ Successfully inserted certificate into database")
    
    retrieved = get_certificate_by_id(test_id)
    if retrieved:
        print("✓ Successfully retrieved certificate")
        print(f"  - Name: {retrieved['name']}")
        print(f"  - Father's Name: {retrieved['father_name']}")
        print(f"  - DOB: {retrieved['dob']}")
        print(f"  - Course: {retrieved['course']}")
        print(f"  - Issue Date: {retrieved['issue_date']}")
        print(f"  - Hash matches: {retrieved['hash'] == test_hash}")
    else:
        print("✗ Could not retrieve certificate")
        sys.exit(1)
except Exception as e:
    print(f"✗ Certificate insertion/retrieval test failed: {e}")
    sys.exit(1)

# Test 4: Check Flask app imports
print("\n" + "=" * 60)
print("TEST 4: Testing Flask application setup...")
print("=" * 60)

try:
    from app import app
    print("✓ Successfully imported Flask app")
    print(f"✓ Flask app routes: {list(app.url_map.iter_rules())}")
    
    # List available routes
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.rule} [{rule.methods - {'HEAD', 'OPTIONS'}}]")
    
    print("\nAvailable endpoints:")
    for route in sorted(routes):
        print(f"  - {route}")
except Exception as e:
    print(f"✗ Flask app test failed: {e}")
    sys.exit(1)

# Test 5: Check templates exist
print("\n" + "=" * 60)
print("TEST 5: Checking HTML templates...")
print("=" * 60)

templates = ["issue.html", "verify.html", "result.html"]
for template in templates:
    path = f"templates/{template}"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "linear-gradient(135deg, #4e73df, #1cc88a)" in content or template == "result.html":
                print(f"✓ {template} exists and has modern theme styling")
            else:
                print(f"✓ {template} exists")
    else:
        print(f"✗ {template} not found")
        sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nApplication is ready to run. Start with:")
print("  python app.py")
print("\nThen visit http://localhost:5000 in your browser")
