# Missing Frontend-Backend Integrations

This document lists all backend endpoints that are implemented but not yet connected to the frontend.

## Summary

**Total Backend Endpoints:** 9
**Connected:** 2 (Login, Signup)
**Missing:** 7

---

## 🔴 Missing Integrations

### 1. **Profile Management** (Citizens & Organizations)

#### GET `/api/auth/profile/`
- **Status:** ❌ Not Connected
- **Location:** `app/profile/page.tsx`
- **Current State:** Uses mock data from auth context
- **Backend:** ✅ Implemented in `backend/accounts/views.py` (ProfileView.get)
- **Action Required:**
  - Create API function in `lib/auth/api.ts` or new `lib/profile/api.ts`
  - Fetch profile data on page load
  - Display real profile data instead of mock

#### PUT `/api/auth/profile`
- **Status:** ❌ Not Connected
- **Location:** `app/profile/page.tsx` (line 88 has TODO comment)
- **Current State:** `handleSave()` function has TODO comment
- **Backend:** ✅ Implemented in `backend/accounts/views.py` (ProfileView.put)
- **Action Required:**
  - Implement API call to update profile
  - Handle success/error states
  - Update UI after successful save

---

### 2. **Consent Management** (Citizens)

#### GET `/api/consents/`
- **Status:** ❌ Not Connected
- **Location:** `app/dashboard/consent/page.tsx`
- **Current State:** Uses `mockConsents` from `lib/mock-data.ts`
- **Backend:** ✅ Implemented in `backend/consents/views.py` (ConsentApiView)
- **Backend Response:** Returns array of consent objects with `name` field
- **Action Required:**
  - Create API function in `lib/consents/api.ts`
  - Fetch consents on page load
  - Map backend response to frontend format
  - Display real consent categories

#### POST `/api/consents/<consent_id>/toggle/`
- **Status:** ❌ Not Connected
- **Location:** `app/dashboard/consent/page.tsx` (line 13-15)
- **Current State:** `handleToggle()` only updates local state
- **Backend:** ✅ Implemented in `backend/consents/views.py` (UserConsentView)
- **Backend Response:** `{ consent: string, access: boolean }`
- **Action Required:**
  - Implement API call to toggle consent
  - Update UI based on response
  - Handle errors (e.g., if user not authenticated)

---

### 3. **Data Access Requests** (Citizens)

#### GET `/api/organization/requested-consent/`
- **Status:** ❌ Not Connected
- **Location:** `app/dashboard/data-access/page.tsx`
- **Current State:** Uses `mockDataAccess` from `lib/mock-data.ts`
- **Backend:** ✅ Implemented in `backend/organization/views.py` (RequestedConsentView)
- **Backend Response:** 
  ```json
  {
    "message": "Consent requests retrieved successfully.",
    "count": 5,
    "data": [/* AccessRequest objects */]
  }
  ```
- **Action Required:**
  - Create API function in `lib/organization/api.ts`
  - Fetch access requests on page load
  - Map backend `AccessRequest` model to frontend `DataAccess` format
  - Display real data access records

#### POST `/api/organization/consent/<access_id>/toggle-access/`
- **Status:** ❌ Not Connected
- **Location:** `app/dashboard/data-access/page.tsx` (line 35-38)
- **Current State:** `handleRevoke()` only has console.log
- **Backend:** ✅ Implemented in `backend/organization/views.py` (ConsentRevocationView)
- **Backend Response:** `{ message: "Consent Granted!" }` or `{ message: "Consent Revoked!" }`
- **Action Required:**
  - Implement API call to approve/revoke access requests
  - Update UI after successful toggle
  - Handle error states

---

### 4. **Organization Features** (Organizations)

#### POST `/api/organization/consent/<user_id>/<consent_id>/request/`
- **Status:** ❌ Not Connected
- **Location:** No UI exists yet - needs to be created
- **Current State:** No frontend implementation
- **Backend:** ✅ Implemented in `backend/organization/views.py` (ConsentRequestView)
- **Backend Response:** 
  ```json
  {
    "message": "Access approved successfully.",
    "data": {/* AccessRequest object */}
  }
  ```
- **Backend Requirements:**
  - Organization must be authenticated
  - Target user must be a CITIZEN
  - User must have granted the consent (UserConsent.access = True)
  - If user hasn't granted consent, returns 400: `{"error": "User has not granted this consent."}`
- **Action Required:**
  - Create UI for organizations to browse/search citizens
  - Add "Request Access" functionality to citizen profile pages
  - Implement API call to request access
  - Handle success and error states
  - Show which consents the citizen has granted

---

## 📋 Backend Data Models Reference

### AccessRequest Model
```python
- id
- organization (ForeignKey to Org)
- user (ForeignKey to CustomUser)
- consent (ForeignKey to Consent)
- status: 'PENDING' | 'APPROVED' | 'REVOKED'
- requested_at (DateTime)
- purpose (CharField)
```

### Consent Model
```python
- id
- name (CharField) - e.g., "Financial", "Biometric", "Health", "Identity"
- created_at
```

### UserConsent Model
```python
- id
- user (ForeignKey to CustomUser)
- consent (ForeignKey to Consent)
- access (Boolean) - True = granted, False = revoked
```

### Profile Model
```python
- id
- user (OneToOneField to CustomUser)
- title (CharField)
- company (CharField)
- url (URLField)
- phone_no (CharField)
- about (TextField)
- profile_pic (ImageField)
```

---

## 🎯 Priority Order for Implementation

1. **High Priority:**
   - Profile GET/PUT (affects all users)
   - Consents GET/Toggle (core citizen feature)

2. **Medium Priority:**
   - Requested Consent GET (citizen data access view)
   - Toggle Access POST (citizen control)

3. **Low Priority:**
   - Organization Request POST (if UI doesn't exist, create it)

---

## 📝 Implementation Notes

1. **API Base URL:** `https://truconn.onrender.com` (from `lib/auth/api.ts`)
2. **Authentication:** Uses session-based auth (cookies)
3. **Error Handling:** Backend returns proper HTTP status codes and error messages
4. **Data Mapping:** Frontend mock data structures may need adjustment to match backend models

---

## ✅ Already Connected

- ✅ POST `/api/auth/login/` - Connected in `lib/auth/api.ts`
- ✅ POST `/api/auth/signup/` - Connected in `lib/auth/api.ts`

