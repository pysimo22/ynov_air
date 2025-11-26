#!/usr/bin/env python
"""
Force delete database and reset
"""
import os
import sys
import time
import subprocess
from pathlib import Path

db_dir = Path(r"C:\Users\simo\Desktop\Django\ynovair")
db_file = db_dir / "db.sqlite3"
db_wal = db_dir / "db.sqlite3-wal"
db_shm = db_dir / "db.sqlite3-shm"

print("=" * 60)
print("FORCE DATABASE RESET")
print("=" * 60)

# Try to close file explorer handles
os.system("taskkill /F /IM explorer.exe")
time.sleep(2)

# Try to delete database files
for db_path in [db_file, db_wal, db_shm]:
    if db_path.exists():
        try:
            os.remove(db_path)
            print(f"✓ Deleted {db_path.name}")
        except Exception as e:
            print(f"✗ Failed to delete {db_path.name}: {e}")

# Apply migrations
print("\nApplying migrations...")
result = subprocess.run([sys.executable, "manage.py", "migrate"], cwd=db_dir, capture_output=True, text=True)
if result.returncode == 0:
    print("✓ Migrations applied successfully")
else:
    print(f"✗ Migration failed: {result.stderr}")

# Create sample data
print("\nCreating sample data...")
result = subprocess.run([sys.executable, "create_data.py"], cwd=db_dir, capture_output=True, text=True)
if result.returncode == 0:
    print("✓ Sample data created successfully")
    print(result.stdout)
else:
    print(f"✗ Sample data creation failed: {result.stderr}")

print("\n" + "=" * 60)
print("DATABASE READY!")
print("=" * 60)
