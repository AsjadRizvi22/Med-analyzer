# 🔴 MUST FEATURES (Core MVP Requirements)

## 1. Report Input System

### System Behavior
The system shall allow users to input medical report data via a text interface.

### User Actions
- User pastes or types medical report data
- User clicks "Analyze Report"

### Expected Output
- Input text is accepted and stored for processing

### Data Processing Steps
1. Capture raw text input
2. Store in memory/session
3. Pass to parsing module

---

## 2. Basic Data Extraction

### System Behavior
The system shall extract structured medical parameters from text.

### User Actions
- No additional action required

### Expected Output
Structured format:
Test Name | Value | Reference Range

### Data Processing Steps
1. Parse text using regex or patterns
2. Extract:
   - Test names
   - Values
   - Reference ranges
3. Store as structured JSON

---

## 3. Abnormal Value Detection

### System Behavior
The system shall classify values as Low, Normal, or High.

### User Actions
- None

### Expected Output
Example:
Hemoglobin → Low

### Data Processing Steps
1. Compare value with reference range
2. Assign:
   - Low
   - Normal
   - High

---

## 4. AI-Based Explanation Generator

### System Behavior
The system shall generate simple explanations.

### User Actions
- Trigger analysis

### Expected Output
Example:
"Your hemoglobin is low, which may indicate anemia."

### Data Processing Steps
1. Send structured data to AI model
2. Generate explanation
3. Return plain-language output

---

## 5. Output Display Interface

### System Behavior
Display structured results clearly.

### User Actions
- View results

### Expected Output
- Test Name
- Value
- Status
- Explanation

### Data Processing Steps
1. Format processed data
2. Render in UI (table/cards)

---

## 6. Medical Disclaimer

### System Behavior
Always display a disclaimer.

### User Actions
- None

### Expected Output
"This is not a medical diagnosis. Please consult a doctor."

### Data Processing Steps
- Append disclaimer to output