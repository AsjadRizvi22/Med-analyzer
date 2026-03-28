# 🤖 AI Treatment Planning & Lifestyle Recommendation Module

---

## 📌 Overview

This module extends the AI Medical Report Analyzer by providing:

- Personalized lifestyle recommendations
- General treatment guidance
- Medication class suggestions (non-prescriptive)
- Doctor referral suggestions

⚠️ IMPORTANT:
This system provides **educational guidance only** and must NOT replace professional medical advice.

---

## 🎯 Goals

- Help users understand **next steps after report analysis**
- Provide **actionable health advice**
- Bridge gap between diagnosis and management
- Improve patient awareness and decision-making

---

## ⚠️ Safety & Compliance Layer (CRITICAL)

The system MUST:

- ❌ NOT provide exact prescriptions (final drug orders)
- ❌ NOT replace a doctor
- ✅ Provide **general medication classes**, not strict prescriptions
- ✅ Include strong disclaimer:
  
"This is not a prescription. Consult a licensed doctor before taking any medication."

---

## 🧠 Functional Requirements

---

### 1. AI-Based Management Recommendation

#### System Behavior
Generate management plan based on analyzed report.

#### User Actions
- User submits report
- Views "Management Plan" section

#### Expected Output
Example:

- Increase iron-rich foods (spinach, red meat)
- Improve hydration
- Monitor symptoms

#### Data Processing Steps
1. Take analyzed results
2. Send structured data to AI
3. Generate lifestyle + management advice

---

### 2. Lifestyle Modification Suggestions

#### System Behavior
Provide personalized daily life recommendations.

#### Expected Output
- Diet suggestions
- Exercise recommendations
- Sleep improvements

#### Example
- “Increase intake of iron-rich foods”
- “Avoid excessive sugar intake”
- “Engage in moderate physical activity”

---

### 3. Medication Guidance (Safe Mode)

#### System Behavior
Suggest **general medication categories**, NOT strict prescriptions.

#### Expected Output
Example:
- Iron supplements (e.g., ferrous sulfate)
- Vitamin B12 supplements

⚠️ RULE:
- Avoid exact dosage unless labeled as “typical range”
- Always include disclaimer

---

### 4. Treatment Plan Structure

#### System Behavior
Organize output into a structured plan.

#### Expected Output Format

1. Condition Overview
2. Lifestyle Changes
3. Possible Treatments
4. Monitoring Advice

---

### 5. Doctor Recommendation

#### System Behavior
Suggest appropriate specialist.

#### Expected Output
Example:
- General Physician
- Hematologist
- Endocrinologist

---

### 6. Risk Stratification (Optional Advanced)

#### System Behavior
Classify severity level.

#### Output
- Mild / Moderate / Severe

---

## 🔌 AI Prompt Design (Groq)

### Example Prompt

---

## 📤 Example Output

### 🧾 Management Plan

**Lifestyle Changes:**
- Increase iron-rich diet
- Maintain hydration

**Treatment Options:**
- Iron supplementation (general recommendation)

**Doctor to Consult:**
- General Physician or Hematologist

**Disclaimer:**
This is not a medical prescription. Consult a doctor.

---

## 🧩 Integration with Existing System

### Updated Flow

1. User submits report
2. Backend analyzes report
3. AI generates:
   - Explanation
   - Management plan
4. Response returned to frontend
5. Display:
   - Results
   - Explanation
   - Management Plan (NEW)

---

## 🗄️ Database Changes

### Add to `results` or separate table

Option 1: Add column

Option 2 (Better): New table

```sql
CREATE TABLE treatment_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID REFERENCES reports(id) ON DELETE CASCADE,
    lifestyle TEXT,
    treatment TEXT,
    medications TEXT,
    doctor_recommendation TEXT,
    created_at TIMESTAMP DEFAULT now()
);