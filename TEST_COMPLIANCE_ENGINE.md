# 🧪 NDPR Compliance Engine - Testing Guide

This guide provides step-by-step instructions to test the NDPR compliance engine implementation.

## Prerequisites

1. **Backend Setup:**
   - Python 3.10+ installed
   - Virtual environment activated
   - Dependencies installed: `pip install -r backend/requirements.txt`

2. **Frontend Setup:**
   - Node.js 18+ installed
   - Dependencies installed: `npm install` or `pnpm install`

---

## 🔧 Backend Testing

### Step 1: Activate Virtual Environment

```bash
# Windows
cd backend
.\venv\Scripts\Activate.ps1

# Linux/Mac
cd backend
source venv/bin/activate
```

### Step 2: Run Migrations

```bash
cd backend
python manage.py migrate compliance
python manage.py migrate  # Run all migrations
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: compliance
Running migrations:
  Applying compliance.0001_initial... OK
```

### Step 3: Verify Models

```bash
python manage.py shell
```

```python
from compliance.models import ComplianceAudit, ViolationReport
from organization.models import Org

# Check models exist
print(ComplianceAudit._meta.db_table)  # Should print: compliance_complianceaudit
print(ViolationReport._meta.db_table)  # Should print: compliance_violationreport
exit()
```

### Step 4: Run Unit Tests

```bash
python manage.py test compliance.test_compliance_setup
```

**Expected Output:**
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 0.123s

OK
Destroying test database for alias 'default'...
```

### Step 5: Start Backend Server

```bash
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 6: Test API Endpoints

#### 6.1 Test Health Check

```bash
curl http://localhost:8000/health/
```

**Expected Response:**
```json
{"status": "ok"}
```

#### 6.2 Test Compliance Endpoints (Requires Authentication)

First, create an organization user and get authentication token:

```bash
# Register organization (if not exists)
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testorg@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "Org",
    "user_role": "ORGANIZATION"
  }'
```

Then login and get session cookie or JWT token:

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "testorg@example.com",
    "password": "testpass123"
  }'
```

#### 6.3 Test Compliance Scan (GET)

```bash
curl -X GET http://localhost:8000/api/compliance/scan/ \
  -b cookies.txt \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "risk_score": 0,
  "total_violations": 0,
  "critical_count": 0,
  "high_count": 0,
  "medium_count": 0,
  "audits": []
}
```

#### 6.4 Test Compliance Scan (POST - Run Scan)

```bash
curl -X POST http://localhost:8000/api/compliance/scan/ \
  -b cookies.txt \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "message": "Compliance scan completed successfully",
  "data": {
    "risk_score": 0,
    "total_violations": 0,
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "violations": [],
    "audit_records": []
  }
}
```

#### 6.5 Test Compliance Reports

```bash
curl -X GET http://localhost:8000/api/compliance/reports/ \
  -b cookies.txt \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "organization": {
    "id": 1,
    "name": "Test Organization"
  },
  "statistics": {
    "total_audits": 0,
    "pending_audits": 0,
    "resolved_audits": 0,
    "unresolved_violations": 0
  },
  "audits": [],
  "violations": []
}
```

---

## 🎨 Frontend Testing

### Step 1: Install Dependencies (if not done)

```bash
npm install
# or
pnpm install
```

### Step 2: Start Frontend Server

```bash
npm run dev
# or
pnpm dev
```

**Expected Output:**
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

### Step 3: Test Compliance Scanner Page

1. **Navigate to:** `http://localhost:3000/admin/organization/compliance`

2. **Login as Organization User:**
   - If not logged in, you'll be redirected to login
   - Login with organization credentials

3. **Verify Page Loads:**
   - ✅ Page title: "Compliance Scanner"
   - ✅ Risk score card displays (initially 0)
   - ✅ "Run Full Compliance Scan" button visible
   - ✅ No errors in browser console

4. **Test Compliance Scan:**
   - Click "Run Full Compliance Scan" button
   - Wait for scan to complete (should be < 5 seconds)
   - Verify:
     - ✅ Risk score updates
     - ✅ Statistics cards update
     - ✅ Audit records display (if any violations found)
     - ✅ No errors in console

5. **Test Audit Status Update:**
   - If audits are displayed, click "Mark as Resolved" on any audit
   - Verify:
     - ✅ Status badge changes to "RESOLVED"
     - ✅ Button disappears
     - ✅ Data refreshes automatically

### Step 4: Verify API Connection

Open browser DevTools (F12) → Network tab:

1. **Check API Calls:**
   - When page loads: `GET /api/compliance/scan/` should return 200
   - When clicking scan: `POST /api/compliance/scan/` should return 200
   - When updating status: `PATCH /api/compliance/audit/<id>/` should return 200

2. **Check for Errors:**
   - No 401 (Unauthorized) errors
   - No 500 (Server Error) errors
   - No CORS errors

---

## 🧪 Integration Testing

### Test Scenario 1: Full Compliance Flow

1. **Backend:** Create test data (organization, users, access requests)
2. **Backend:** Run compliance scan via API
3. **Frontend:** Navigate to compliance page
4. **Frontend:** Verify scan results display
5. **Frontend:** Mark an audit as resolved
6. **Backend:** Verify audit status updated in database

### Test Scenario 2: Violation Detection

1. **Backend:** Create access request with revoked consent
2. **Backend:** Run compliance scan
3. **Verify:** CRITICAL violation detected for REVOCATION_HANDLING
4. **Verify:** Risk score > 0
5. **Verify:** Violation report created

### Test Scenario 3: Real-time Updates

1. **Frontend:** Open compliance page
2. **Backend:** Create violation via API
3. **Frontend:** Click "Run Full Compliance Scan"
4. **Verify:** New violations appear immediately

---

## ✅ Verification Checklist

### Backend
- [ ] Migrations run successfully
- [ ] Models can be created
- [ ] Rules engine runs without errors
- [ ] API endpoints return 200 status
- [ ] Serializers work correctly
- [ ] Permissions work (only organizations can access)

### Frontend
- [ ] Page loads without errors
- [ ] API calls succeed
- [ ] Risk score displays correctly
- [ ] Scan button works
- [ ] Results display properly
- [ ] Status update works
- [ ] No console errors

### Integration
- [ ] Frontend can connect to backend
- [ ] Authentication works
- [ ] Data flows correctly
- [ ] Updates reflect in real-time

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** Activate virtual environment:
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
pip install -r requirements.txt
```

### Issue: "Migration not found"
**Solution:** Create migrations:
```bash
python manage.py makemigrations compliance
python manage.py migrate compliance
```

### Issue: "401 Unauthorized" in frontend
**Solution:** 
- Check if user is logged in
- Verify user role is "ORGANIZATION"
- Check session cookie is set

### Issue: "CORS error"
**Solution:** 
- Verify backend CORS settings in `settings.py`
- Check `CORS_ALLOWED_ORIGINS` includes frontend URL
- Restart backend server

### Issue: "500 Internal Server Error"
**Solution:**
- Check backend logs
- Verify database migrations applied
- Check if organization exists for user

---

## 📊 Expected Test Results

### With No Violations:
- Risk Score: 0
- Total Violations: 0
- Audit Records: Empty array

### With Violations:
- Risk Score: 5-100 (depending on severity)
- Total Violations: > 0
- Audit Records: Array with violation details
- Violation Reports: Created for CRITICAL/HIGH issues

---

## 🎯 Success Criteria

✅ **Backend is working if:**
- All API endpoints return 200 status
- Compliance scan completes successfully
- Audit records are created in database

✅ **Frontend is working if:**
- Page loads without errors
- Scan button triggers API call
- Results display correctly
- Status updates work

✅ **Integration is working if:**
- Frontend can fetch data from backend
- Updates reflect immediately
- No authentication errors
- No CORS errors

---

*Last Updated: 2025-12-11*

