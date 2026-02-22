# 🛡️ Lumen Proxy: Agentic AI Security Gateway & Web-SOC

**Lumen Proxy** is a production-grade, multi-layered security middleware designed to protect Large Language Model (LLM) applications from prompt injection, social engineering, and adversarial attacks. It bridges the gap between **deterministic heuristics** and **agentic AI reflection**, providing a robust defense-in-depth architecture.

---

## 🏗️ Architecture & Components

The system operates on a **Tiered Escalation** philosophy: Filter the "noise" locally, and escalate "intent" to the Cloud.

1. **`guadrail.py` (The Interceptor):** A high-speed heuristic engine using **frequency-weighted scoring** and **diminishing multipliers** to identify known red flags with sub-millisecond latency.
2. **`judge.py` (The AI Brain):** The "Agentic Pivot." Ambiguous inputs (Yellow Zone) are escalated to a **Google Gemini 1.5** model. The Judge performs deep semantic analysis to detect obfuscated malicious intent.
3. **`database.py` (The Memory):** Handles persistent logging of all interactions, scores, and decisions into a local **SQLite** database (`lumen_proxy.db`).
4. **`audit_logs.py` (The Analyst Tool):** A CLI utility that extracts raw logs from the database and presents them in a clean, professional table format for Security Analysts.
5. **`dashboard_summary.py` (The Analytics Engine):** Processes telemetry to generate high-level metrics and identifies the top **Adversarial Vectors**, filtering out common English noise.
6. **`app.py` (The Webscale SOC Dashboard):** A dynamic, "Cyber-Dark" themed web interface built with **Streamlit** and **ECharts**. Features live threat visualizations and interactive monitoring.

---

## 🛡️ Security Philosophy & DevSecOps

* **Cost-to-Value Optimization:** Local heuristics handle 90% of traffic, significantly reducing API token costs.
* **Hybrid Intelligence:** Combines the speed of Python regex with the "reasoning" of Generative AI.
* **Sanitized Telemetry:** The analytics engine utilizes a custom **Stop-Word Filter** to isolate actual adversarial keywords.
* **Secret Management:** Strict protocol using `.env` files to protect sensitive API credentials.

---

## 🚀 Setup & Installation

### Prerequisites
* Python 3.11+
* Google Gemini API Key

### Installation

1. **Clone and Navigate:**
   ```bash
   cd Lumen_Proxy
2. **Install Dependencies:**
   ```bash
   pip install google-genai python-dotenv streamlit streamlit-echarts pandas colorama
   ```
3. **Configure Environment Variables:**
   - Create a `.env` file in the root directory:

   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```  
### Usage Pipeline:
1. **Run the Core Proxy:**
```bash
python guadrail.py
```
2. **Test Inputs:**
* Try typing: "Just a normal question about the weather." (GREEN)
* Try typing: "system" (YELLOW -> Escalates to AI Judge)
* Try typing: "I want to bypass the admin rules." (RED)
3. **Audit Logs (Security Analyst View):**
```bash
python audit_logs.py
```
4. **Generate Threat Intelligence (Executive View):**
```bash
python dashboard_summary.py
```
5. **Launch the Webscale SOC Dashboard:**
```bash
python -m streamlit run app.py
```
The dashboard will compile the telemetry and open in your default browser at `http://localhost:8501`.

### Dashboard Preview:
![alt text][def]

[def]: image.png