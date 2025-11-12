# 🔧 Fix: "relation compliance_complianceaudit does not exist"

## Problem
The database tables for the compliance app haven't been created yet. This error occurs when the migrations haven't been run.

## Solution: Run Migrations

### Option 1: Using the Script (Windows)

```powershell
cd backend
.\run_migrations.bat
```

### Option 2: Manual Commands

**In the terminal where your virtual environment is activated:**

```bash
# Navigate to backend directory
cd backend

# Run compliance migrations
python manage.py migrate compliance

# Run all migrations (to ensure everything is up to date)
python manage.py migrate
```

### Option 3: Using PowerShell

```powershell
cd backend

# Activate venv (if not already activated)
.\venv\Scripts\Activate.ps1

# Run migrations
python manage.py migrate compliance
python manage.py migrate
```

## Expected Output

When migrations run successfully, you should see:

```
Operations to perform:
  Apply all migrations: compliance
Running migrations:
  Applying compliance.0001_initial... OK

Operations to perform:
  Apply all migrations: admin, auth, accounts, compliance, consents, contenttypes, organization, sessions
Running migrations:
  No migrations to apply.
```

## Verify Tables Are Created

After running migrations, you can verify the tables exist:

### Using Django Shell

```bash
python manage.py shell
```

```python
from django.db import connection

cursor = connection.cursor()

# For PostgreSQL
cursor.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_name LIKE 'compliance_%'
""")

tables = [row[0] for row in cursor.fetchall()]
print("Compliance tables:", tables)

# Should show:
# ['compliance_complianceaudit', 'compliance_violationreport']

exit()
```

### Using psql (PostgreSQL)

```bash
psql -d your_database_name

# Then run:
\dt compliance_*

# Should show:
# compliance_complianceaudit
# compliance_violationreport
```

## After Running Migrations

1. **Restart your backend server** (if it's running):
   ```bash
   # Stop the server (Ctrl+C)
   # Then restart:
   python manage.py runserver
   ```

2. **Refresh your frontend page:**
   - Go to: `http://localhost:3000/admin/organization/compliance`
   - The error should be gone
   - You should see the compliance scanner page

## Troubleshooting

### Issue: "No migrations to apply"
**Solution:** The migrations might already be applied. Check if tables exist using the verification steps above.

### Issue: "Migration file not found"
**Solution:** Make sure the migration file exists:
```bash
ls backend/compliance/migrations/0001_initial.py
```

If it doesn't exist, create it:
```bash
python manage.py makemigrations compliance
python manage.py migrate compliance
```

### Issue: "Permission denied" (PostgreSQL)
**Solution:** Make sure your database user has CREATE TABLE permissions:
```sql
GRANT ALL PRIVILEGES ON DATABASE your_database TO your_user;
```

### Issue: "Database connection error"
**Solution:** Check your database settings in `backend/truconn/settings.py`:
- Verify `DATABASE_URL` environment variable is set
- Check database credentials
- Ensure database exists

## Quick Fix Checklist

- [ ] Activate virtual environment
- [ ] Navigate to `backend` directory
- [ ] Run: `python manage.py migrate compliance`
- [ ] Run: `python manage.py migrate`
- [ ] Verify tables exist (optional)
- [ ] Restart backend server
- [ ] Refresh frontend page
- [ ] Test compliance scanner

---

**After completing these steps, the error should be resolved!** ✅

