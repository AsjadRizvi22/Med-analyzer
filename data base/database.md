# 🗄️ Database Design — AI Medical Report Analyzer & Diagnosis Assistant

---

## 1. Overview

The database stores:
- User accounts (optional for MVP)
- Medical reports
- Analyzed results
- Logs/analytics (usage tracking)

**Database Choice:** Supabase (PostgreSQL)

---

## 2. ER Diagram (Conceptual)


Users ──< Reports ──< Results
│
└─< Logs


- One user can have multiple reports  
- Each report can have multiple test results  
- Logs track user activity/events

---

## 3. Tables and SQL Schema

### 3.1 Users Table

Stores registered users (optional for MVP).

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

Relationships:

users.id → reports.user_id (One-to-Many)

3.2 Reports Table

Stores each uploaded or entered medical report.

CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    report_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

Relationships:

One report can have multiple results

Foreign key to users allows user-specific reports

3.3 Results Table

Stores individual test results extracted from a report.

CREATE TABLE results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID REFERENCES reports(id) ON DELETE CASCADE,
    test_name VARCHAR(255) NOT NULL,
    value NUMERIC NOT NULL,
    reference_range VARCHAR(50),
    status VARCHAR(10) CHECK (status IN ('Low', 'Normal', 'High')),
    explanation TEXT,
    created_at TIMESTAMP DEFAULT now()
);

Relationships:

report_id → links to parent report

Each report can have multiple test results

3.4 Logs Table

Optional: Track system usage for analytics.

CREATE TABLE logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    report_id UUID REFERENCES reports(id),
    event_type VARCHAR(50) NOT NULL,
    event_time TIMESTAMP DEFAULT now(),
    details JSONB
);

Example Events:

"Report Submitted"

"Analysis Viewed"

"AI Explanation Requested"

4. Relationships Summary
Table	Relationship	Notes
Users	1 → Many Reports	A user can have multiple reports
Reports	1 → Many Results	Each report contains multiple tests
Users	1 → Many Logs	Tracks user actions
Reports	1 → Many Logs	Logs can be linked to specific reports
5. Example Query

Get all results for a specific user:

SELECT r.id AS report_id, rs.test_name, rs.value, rs.status, rs.explanation
FROM users u
JOIN reports r ON r.user_id = u.id
JOIN results rs ON rs.report_id = r.id
WHERE u.email = 'patient@example.com';
6. Notes

UUIDs for primary keys ensure unique identification across distributed systems

JSONB in logs allows flexible storage of events and metadata

Status field constrained to Low, Normal, High for consistency

Supabase automatically provides authentication, so users table can integrate with Supabase Auth

✅ Design Benefits

Fully relational for easy joins

Supports multiple reports per user

Allows detailed per-test results

Logs enable analytics and future features (trends, AI usage metrics)