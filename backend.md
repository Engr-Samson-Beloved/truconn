# 🇳🇬 TruCon – Nigerian Data Trust & Consent Platform (Backend)

> **Purpose:** TruCon is a national-grade, trust-first data management system designed to empower Nigerian citizens and organizations with transparent data consent, verification, and control mechanisms.

---

## 🧭 Overview

TruCon Backend provides the **secure logic, API endpoints, authentication, and data validation layer** for the full Nigerian Data Trust framework.  
It ensures that every data transaction — whether a consent, revocation, or organization verification — is **cryptographically recorded, auditable, and privacy-respecting**.

The system is built for:
- **Transparency:** Citizens see who accesses their data and when.  
- **Consent Control:** Users can grant or revoke data access in real time.  
- **Trust Assurance:** Organizations are verified before requesting any data.  

---

## ⚙️ System Architecture


IMPLEMENTATION!
        ┌──────────────────────────┐
        │        Frontend UI       │
        │  (v0.dev + Next.js)      │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │        API Gateway        │
        │ (FastAPI / Node.js / Supa)│
        └────────────┬─────────────┘
                     │
                     ▼
     ┌────────────────────────────┐
     │  Core Backend Services     │
     │                            │
     │ • Auth & Identity Mgmt     │
     │ • Consent Controller       │
     │ • Org Verification Engine  │
     │ • Audit & Transparency Log │
     │ • Notification Service     │
     └────────────┬───────────────┘
                     │
                     ▼
       ┌──────────────────────────┐
       │   PostgreSQL / Supabase  │
       │   (Data + Audit Ledger)  │
       └──────────────────────────┘


TASKS AND USE CASES

---

## 🧱 Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| Backend Framework | **FastAPI** (Python) or **Express.js** (Node) | API orchestration and routing |
| Database | **PostgreSQL** (via Supabase) | Relational storage + auth |
| Auth | **JWT** + Supabase Auth | Secure authentication & session |
| Storage | Supabase Storage / AWS S3 | Document and proof uploads |
| Audit Trail | Custom PostgreSQL triggers | Immutable transparency log |
| Cache | Redis (optional) | Speed up frequent verification |
| Deployment | Docker + Railway / Render | Cloud-ready containerization |

---

## 🗄️ Database Schema (Core Tables)

### `users`
| Field | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| full_name | VARCHAR | User’s full name |
| email | VARCHAR | Unique email |
| national_id | VARCHAR | NIN or BVN |
| password_hash | TEXT | Encrypted password |
| user_role | ENUM('citizen', 'org_admin', 'super_admin') | Role-based access |
| created_at | TIMESTAMP | Record creation |
| updated_at | TIMESTAMP | Record update |

---

### `organizations`
| Field | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| org_name | VARCHAR | Registered organization |
| cac_number | VARCHAR | CAC / license identifier |
| verification_status | ENUM('pending', 'verified', 'revoked') | Trust state |
| contact_email | VARCHAR | For data access requests |
| created_at | TIMESTAMP | Timestamp |

---

### `consents`
| Field | Type | Description |
|--------|------|-------------|
| id | UUID | Consent record |
| user_id | UUID | Linked citizen |
| org_id | UUID | Linked organization |
| data_scope | JSONB | Fields user consents to share |
| consent_status | ENUM('granted', 'revoked', 'expired') | Current state |
| timestamp | TIMESTAMP | Event date |

---

### `audit_logs`
| Field | Type | Description |
|--------|------|-------------|
| id | SERIAL | Log ID |
| entity_type | ENUM('user', 'org', 'consent') | Source type |
| entity_id | UUID | Related entity |
| action | VARCHAR | What occurred |
| performed_by | UUID | User or org responsible |
| created_at | TIMESTAMP | Immutable timestamp |
| metadata | JSONB | Request context |

---

## 🔐 Authentication & Authorization

**Supabase Auth** manages the authentication lifecycle:
- Email/Password + Magic Link login.
- JWT token injected into all API requests.
- Role-based route protection:
  - `/citizen/*` → Citizen access only.
  - `/org/*` → Organization admins only.
  - `/admin/*` → Platform supervisors.

All access is checked using middleware that validates:
- Token authenticity.
- Role permission.
- Session expiry.

---

## 🚦 API ENDPOINTS (Core)

| Endpoint | Method | Description | Auth |
|-----------|---------|-------------|------|
| `/auth/signup` | POST | Register new user | ❌ |
| `/auth/login` | POST | Authenticate user | ❌ |
| `/users/me` | GET | Fetch current user info | ✅ |
| `/organizations` | POST | Register an organization | ✅ |
| `/organizations/verify/:id` | PATCH | Verify an organization | 🔒 admin |
| `/consents/request` | POST | Create a new consent request | ✅ |
| `/consents/approve/:id` | PATCH | Grant data access | ✅ |
| `/consents/revoke/:id` | PATCH | Withdraw consent | ✅ |
| `/audit` | GET | Retrieve transparency logs | ✅ |

---

## 📜 Consent Flow Logic

1. **Organization Request:**  
   Org sends consent request (JSON schema: data_scope, reason, expiry).
2. **Citizen Receives Prompt:**  
   Citizen receives in-app + email notification.
3. **Citizen Grants or Revokes:**  
   Consent decision stored in `consents` table.
4. **Audit Entry Logged:**  
   System writes immutable record into `audit_logs`.
5. **Org Data Access Enabled:**  
   If consent is `granted`, system issues signed access token.
6. **Revocation:**  
   If revoked, all tokens invalidated automatically via middleware.

---

## 🧩 Modular Service Design

- **AuthService:** Handles login, token refresh, and roles.
- **OrgService:** Manages organization onboarding and verification.
- **ConsentService:** Controls all user-data sharing logic.
- **AuditService:** Records immutable event history.
- **NotificationService:** Sends alerts (email/SMS/push).

Each service is isolated and can be deployed independently via containerization.

---

## ⚡ Performance & Scalability

- Use **connection pooling (pgBouncer)** for database.
- Implement **rate-limiting middleware** (e.g., `express-rate-limit`).
- Cache verified orgs with **Redis TTL (5 mins)**.
- Queue async notifications using **BullMQ / Celery**.
- Database indexing on: `user_id`, `org_id`, and `created_at`.

---

## 🧪 Testing

- Unit tests: Jest / Pytest
- Integration tests: Supertest (for Express)
- Mocking: `nock` or `pytest-mock`
- CI/CD: GitHub Actions run full pipeline before merge.

---

## 🔒 Security Considerations

- Enforce HTTPS everywhere.  
- Use Argon2 or bcrypt for password hashing.  
- Sign JWTs with short expiry (15m) + refresh tokens.  
- Log every admin action in `audit_logs`.  
- Apply field-level encryption for sensitive PII (AES-256).  
- GDPR/Nigeria Data Protection compliant (NDPA).

---

## 🚀 Deployment Guide

**Using Docker:**
```bash
docker build -t trucon-backend .
docker run -p 8080:8080 trucon-backend
