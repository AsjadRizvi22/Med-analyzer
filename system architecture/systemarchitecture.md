# 🏗️ System Architecture Overview
## AI Medical Report Analyzer & Diagnosis Assistant

---

## 🔷 High-Level Architecture

User → React Frontend → FastAPI Backend → Groq AI
                              ↓
                          Supabase
                              ↓
                    External Services (OCR, etc.)

---

## 🎯 Architecture Goals

- Fast AI inference (Groq)
- Scalable backend (FastAPI)
- Real-time database & auth (Supabase)
- Clean modular design
- MVP-ready but extensible

---

## 🧩 Core Components

1. Frontend (React)
2. Backend (FastAPI)
3. API Layer (REST)
4. Database (Supabase)
5. AI Engine (Groq)
6. External Services (OCR, Translation)

---

## 🔄 Data Flow Summary

1. User inputs medical report
2. React sends request to FastAPI
3. FastAPI:
   - Parses data
   - Detects abnormalities
   - Calls Groq AI
4. AI generates explanation
5. Backend sends response
6. React displays results
7. (Optional) Supabase stores report

---

## ⚡ MVP Simplification

- No authentication required initially
- Supabase optional for storage
- OCR skipped in first version
- Focus on text-based input

---
📁 FRONTEND_ARCHITECTURE.md
# 🎨 Frontend Architecture (React)

---

## 📌 Overview

The frontend is built using React and handles:
- User interaction
- Data input
- Displaying analyzed results

---

## 🧱 Component Structure

src/
│
├── components/
│   ├── InputForm.jsx
│   ├── ResultCard.jsx
│   ├── Loader.jsx
│   └── Disclaimer.jsx
│
├── pages/
│   └── Home.jsx
│
├── services/
│   └── api.js
│
└── App.jsx

---

## ⚙️ Key Responsibilities

- Capture report input
- Call backend API
- Display structured results
- Highlight abnormal values
- Show AI explanations

---

## 🔄 User Flow

1. User enters report text
2. Clicks "Analyze"
3. API request sent
4. Loading state shown
5. Results displayed

---

## 🔌 API Integration

POST /analyze

Request:
{
  "report_text": "Hb: 9 g/dL (12-16)"
}

Response:
{
  "results": [...],
  "disclaimer": "Not a diagnosis"
}

---

## 🎯 UI Features

- Clean input box
- Result cards
- Color coding:
  - Red → Abnormal
  - Green → Normal
- Responsive design

---
📁 BACKEND_ARCHITECTURE.md
# ⚡ Backend Architecture (FastAPI)

---

## 📌 Overview

FastAPI handles:
- Business logic
- Data parsing
- AI integration
- API endpoints

---

## 🧱 Project Structure

backend/
│
├── main.py
├── routes/
│   └── analyze.py
│
├── services/
│   ├── parser.py
│   ├── analyzer.py
│   └── ai_service.py
│
├── models/
│   └── schemas.py
│
└── utils/
    └── helpers.py

---

## 🔌 API Endpoints

### POST /analyze

Input:
- report_text

Output:
- structured results
- explanations
- disclaimer

---

## ⚙️ Core Modules

### 1. Parser Service
- Extract test name, values, ranges

### 2. Analyzer Service
- Detect abnormal values

### 3. AI Service
- Communicate with Groq API

---

## 🔄 Processing Flow

1. Receive request
2. Parse text
3. Analyze values
4. Call AI
5. Return response

---

## 🚀 Advantages of FastAPI

- High performance
- Async support
- Easy API development
- Built-in docs (Swagger)

---
📁 DATABASE_ARCHITECTURE.md
# 🗄️ Database Architecture (Supabase)

---

## 📌 Overview

Supabase provides:
- PostgreSQL database
- Authentication (optional)
- Storage (future use)

---

## 🧱 Tables (Initial Design)

### reports
- id (UUID)
- user_id (optional)
- report_text
- created_at

---

### results
- id (UUID)
- report_id (FK)
- test_name
- value
- status
- explanation

---

## 🔐 Authentication (Optional)

- Email/password login
- JWT-based session

---

## ⚙️ Responsibilities

- Store reports
- Store analysis results
- Enable history tracking

---

## 🔄 Data Flow

1. Backend receives report
2. (Optional) Save to Supabase
3. Store results after processing
4. Retrieve for future use

---

## 🚀 Benefits of Supabase

- Instant backend
- Real-time database
- Easy integration with React
- Scalable

---
📁 AI_ARCHITECTURE.md
# 🤖 AI Architecture (Groq Integration)

---

## 📌 Overview

Groq is used for:
- Generating explanations
- Providing medical insights

---

## ⚙️ AI Responsibilities

- Convert structured data → simple explanation
- Provide medical interpretation
- (Future) Suggest possible diagnoses

---

## 🔌 Integration Flow

1. Backend prepares prompt
2. Send to Groq API
3. Receive response
4. Return to frontend

---

## 🧠 Example Prompt

Explain the following lab result in simple terms:

Test: Hemoglobin
Status: Low

---

## 📤 Example Output

"Your hemoglobin level is low, which may indicate anemia."

---

## ⚠️ Safety Layer

- Always include disclaimer
- Avoid definitive diagnosis
- Keep output educational

---

## 🚀 Why Groq?

- Ultra-fast inference
- Low latency
- Ideal for real-time apps

---
📁 API_FLOW.md
# 🔄 API Flow & Component Interaction

---

## 📌 End-to-End Flow

### Step 1: User Input
- User enters report in React UI

---

### Step 2: API Request
- React sends POST request to FastAPI

---

### Step 3: Backend Processing

FastAPI:
1. Parses input
2. Extracts values
3. Detects abnormalities

---

### Step 4: AI Call

- Backend sends structured data to Groq
- Receives explanation

---

### Step 5: Response Assembly

- Combine:
  - Test results
  - AI explanation
  - Disclaimer

---

### Step 6: Response to Frontend

- JSON returned

---

### Step 7: UI Rendering

- Display results
- Highlight abnormalities

---

## 🔁 Optional Flow (With Supabase)

1. Save report
2. Save results
3. Enable history tracking

---

## 🎯 Key Design Principles

- Keep backend stateless
- Use async API calls
- Modular services
- Scalable architecture