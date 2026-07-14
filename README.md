# 🛡️ Lumen Proxy: Agentic AI Security Gateway & Web-SOC

**Lumen Proxy** is a working prototype of a multi-layered security middleware for Large Language Model (LLM) applications, combining a lightweight local heuristic filter with an LLM-based semantic judge (Google Gemini) for ambiguous cases. It's designed around a **Tiered Escalation** philosophy: resolve obvious cases locally and fast, escalate only genuine ambiguity to the cloud. Validated against a real test batch of adversarial and benign prompts — see [Validation Results](#validation-results) below.

---

## 🏗️ Architecture & Components

The system operates on a **Tiered Escalation** philosophy: filter the "noise" locally, and escalate "intent" to the cloud.

1. **`guardrail.py` (The Interceptor):** A local heuristic engine using **frequency-weighted scoring** and **diminishing multipliers** to identify known red-flag keywords with sub-millisecond latency.
2. **`judge.py` (The AI Brain):** The "Agentic Pivot." Ambiguous inputs (Yellow Zone) are escalated to **Google Gemini (gemini-2.5-flash)**. The Judge performs semantic analysis to catch intent that a keyword filter alone would miss — and to clear false positives the heuristic flags incorrectly.
3. **`database.py` (The Memory):** Handles persistent logging of all interactions, scores, and decisions into a local **SQLite** database (`lumen_proxy.db`).
4. **`audit_logs.py` (The Analyst Tool):** A CLI utility that extracts raw logs from the database and presents them in a clean, readable table format.
5. **`dashboard_summary.py` (The Analytics Engine):** Processes telemetry to generate aggregate metrics and surfaces the top recurring terms in flagged prompts, filtering out common English noise.
6. **`app.py` (The Web-SOC Dashboard):** A "Cyber-Dark" themed web interface built with **Streamlit** and **ECharts**, with live threat visualizations and interactive monitoring.

---

## 🛡️ Security Philosophy & DevSecOps

- **Cost-to-Value Optimization:** In a 10-prompt validation batch, 60% of traffic was resolved locally via heuristic scoring alone, with the remaining 40% escalated to the Gemini-based semantic judge — avoiding a Gemini call on every single request.
- **Verified Semantic Judgment:** The Judge correctly flagged 3 of 4 escalated prompts as malicious, and correctly reclassified 1 heuristic false positive ("tell me about your system") back to safe — demonstrating real semantic reasoning beyond keyword matching, not just a rubber stamp on the heuristic's decision.
- **Data-Driven Keyword Discovery:** The analytics engine performs independent keyword-frequency analysis on flagged prompts, surfacing candidate terms not yet in the heuristic dictionary — a feedback loop for iteratively expanding keyword coverage over time.
- **Fail-Closed Design:** If the Judge is unreachable (API error, network issue), the system defaults to blocking rather than allowing the request through — a deliberate fail-safe choice over fail-open.
- **Secret Management:** API credentials are kept in a local `.env` file, excluded from version control; `.env.example` documents the required variable without exposing a real key.

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.11+
- Google Gemini API Key

### Installation

1. **Clone and Navigate:**

```
git clone https://github.com/GopiKrishnaPittu/Lumen_Proxy.git
cd Lumen_Proxy
```

2. **Install Dependencies:**

```
pip install google-genai python-dotenv streamlit streamlit-echarts pandas
```

3. **Configure Environment Variables:**

Copy the template and add your real key:

```
copy .env.example .env
```

Then open `.env` and replace the placeholder:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### Usage Pipeline

1. **Run the Core Proxy:**

```
python guardrail.py
```

2. **Test Inputs:**

- Try typing: "Just a normal question about the weather." (GREEN)
- Try typing: "system" (YELLOW → escalates to AI Judge)
- Try typing: "I want to bypass the admin rules." (RED)

3. **Audit Logs (raw view):**

```
python audit_logs.py
```

4. **Generate Threat Intelligence Summary:**

```
python dashboard_summary.py
```

5. **Launch the Web-SOC Dashboard:**

```
python -m streamlit run app.py
```

The dashboard compiles the telemetry and opens in your default browser at `http://localhost:8501`.

---

## 📊 Validation Results

Tested against a 10-prompt batch of benign and adversarial inputs:

```
Total Requests Processed: 10
Critical Threats Blocked: 5

GREEN: 4  |  GREEN (JUDGE): 1  |  RED: 2  |  RED (JUDGE): 3
```

Notably, the semantic judge reclassified **"tell me about your system"** from a heuristic YELLOW flag back to safe, while independently catching **"what admin tools do you have access to"** as malicious despite no exact keyword match against the local heuristic dictionary — direct evidence that the Gemini-based judge adds real semantic value on top of the local filter, not just a second opinion that always agrees.

This was a small proof-of-concept validation batch, not a large-scale benchmark — numbers above reflect that sample size.

### Dashboard Preview

[![alt text](https://github.com/GopiKrishnaPittu/Lumen_Proxy/raw/main/image.png)](/GopiKrishnaPittu/Lumen_Proxy/blob/main/image.png)

---

## Testing

Unit tests cover the core scoring and decision logic in `guardrail.py`:

```
pip install pytest
python -m pytest
```

---

## License

MIT — see [LICENSE](./LICENSE).
