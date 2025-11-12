# 🔧 Fix: "column organization_org.trust_score does not exist"

## Problem
The database columns for trust score fields haven't been created yet. The migrations exist but haven't been run.

## Solution: Run Migrations

### For Local Development:

```bash
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate     # Linux/Mac

# Set environment variables (if needed)
$env:SECRET_KEY = "your-secret-key"
$env:DEBUG = "True"

# Run migrations
python manage.py migrate organization
```

### For Production (Render.com):

1. **Via Render Dashboard:**
   - Go to your Render dashboard
   - Navigate to your Django service
   - Open the Shell/Console
   - Run: `python manage.py migrate organization`

2. **Via Render CLI:**
   ```bash
   render run python manage.py migrate organization
   ```

3. **Via SSH (if available):**
   ```bash
   ssh into your server
   cd /opt/render/project/src
   python manage.py migrate organization
   ```

### Expected Output:

```
Operations to perform:
  Apply all migrations: organization
Running migrations:
  Applying organization.0005_org_trust_score... OK
  Applying organization.0006_integrityrecord... OK
```

## Verify Migrations Applied

After running migrations, verify the columns exist:

```python
python manage.py shell
```

```python
from django.db import connection

cursor = connection.cursor()

# For PostgreSQL
cursor.execute("""
    SELECT column_name FROM information_schema.columns 
    WHERE table_name = 'organization_org' 
    AND column_name LIKE 'trust_%'
""")

columns = [row[0] for row in cursor.fetchall()]
print("Trust score columns:", columns)

# Should show:
# ['trust_score', 'trust_level', 'trust_score_last_calculated', 
#  'trust_certificate_issued', 'trust_certificate_issued_at']

exit()
```

## After Running Migrations

1. **Restart your backend server** (if it's running)
2. **Refresh your frontend page** - the error should be gone
3. **Test the trust score system:**
   - Organization dashboard: `http://localhost:3000/admin/organization`
   - Trust registry: `http://localhost:3000/trust-registry`

## Troubleshooting

### Issue: "Migration already applied"
**Solution:** Check migration status:
```bash
python manage.py showmigrations organization
```

### Issue: "No such migration"
**Solution:** Make sure migration files exist:
```bash
ls backend/organization/migrations/0005_org_trust_score.py
ls backend/organization/migrations/0006_integrityrecord.py
```

### Issue: "Permission denied" (Production)
**Solution:** Make sure you have database write permissions on your production database.

---

**After completing these steps, the error should be resolved!** ✅

