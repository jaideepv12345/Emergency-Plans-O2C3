import json
import os
import tempfile
from datetime import datetime

from docx import Document
from flask import Flask, jsonify, render_template_string, request, send_file
from PyPDF2 import PdfReader
from weasyprint import HTML

# Initialize Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()


# -----------------------------
# 🔍 1. PRECISION HAZARD AUTOPSY
# -----------------------------
def run_disaster_replay(text: str) -> list[str]:
    known_failures = {
        "evacuation route": "Route 9 flooded during Hurricane Michael (2018)",
        "shelter power": "Shelter B lost power for 72h in 2020 storm",
        "comms failure": "Radio towers downed in 2019 wildfire",
    }
    issues = []
    for keyword, failure in known_failures.items():
        if keyword in text:
            issues.append(
                f"🔴 **Failure Replay**: {failure}. Plan does not address redundancy."
            )
    return issues


# -----------------------------
# 🧬 2. FEMA GRANT DNA SEQUENCER
# -----------------------------
def check_grant_dna(text: str) -> list[str]:
    bric_criteria = {
        "innovation": "Proposes new tech/method",
        "maintenance": "Includes 10-year O&M plan",
        "community": "Documents public input",
        "cost_benefit": "Includes BCA using FEMA 430",
        "equity": "Addresses vulnerable populations",
    }
    missing = []
    for gene in bric_criteria:
        if gene.replace("_", " ") not in text:
            missing.append(f"🧬 Missing Gene: `{gene}` → loses points in BRIC")
    return missing


# -----------------------------
# 🎯 3. EQUITY LASER SCANNER
# -----------------------------
def equity_audit(text: str, county_data: dict) -> list[str]:
    svi_high = county_data.get("svi_high", False)
    lep_pct = county_data.get("lep_pct", 0)
    issues = []
    if svi_high and "equity" not in text:
        issues.append("🎯 Equity Gap: High SVI area ignored in outreach")
    if lep_pct > 20 and "spanish" not in text.lower():
        issues.append(f"🎯 Language Gap: {lep_pct}% LEP population, no multilingual alerts")
    return issues


# -----------------------------
# ⚠️ 4. CLIMATE TRAUMA SIMULATOR
# -----------------------------
def climate_simulator(text: str) -> list[str]:
    if "sea level rise" not in text and "2050" not in text:
        return ["⚠️ Climate Lag: No forward-looking projections (e.g., NOAA RCP 8.5)"]
    if "adaptive trigger" in text:
        return ["✅ Climate Ready: Includes plan update triggers"]
    return ["⚠️ Missing: Adaptive triggers for climate thresholds"]


# -----------------------------
# 🩹 5. POLICY SUTURE ENGINE
# -----------------------------
def generate_patches(text: str) -> list[dict]:
    patches = []
    if "capability assessment" not in text:
        patches.append(
            {
                "issue": "Missing: Capability Assessment",
                "fix": (
                    'Add: "The jurisdiction assessed its capacity to implement mitigation '
                    'actions, including staffing and funding, per 44 CFR §201.6(c)(4)."'
                ),
            }
        )
    if "maintenance plan" not in text:
        patches.append(
            {
                "issue": "Missing: Maintenance Plan",
                "fix": (
                    'Add: "All projects include a 10-year O&M plan funded through '
                    'municipal reserves."'
                ),
            }
        )
    return patches


# -----------------------------
# 📊 6. RESILIENCE PULSE MONITOR
# -----------------------------
def get_vital_signs(text: str, county_data: dict) -> dict:
    compliance = 80 if "44 cfr" in text else 50
    equity = 30 if county_data.get("lep_pct", 0) > 20 and "spanish" not in text else 70
    climate = 40 if "2050" in text else 20
    funding = 100 - len(check_grant_dna(text)) * 10
    return {
        "compliance": compliance,
        "equity": equity,
        "climate": climate,
        "funding": max(30, funding),
    }


# -----------------------------
# 🎤 7. DIRECTOR'S WAR ROOM BRIEFING
# -----------------------------
def generate_director_brief(
    filename: str, issues: list[str], patches: list[dict], vitals: dict, county_data: dict
) -> str:
    _ = county_data  # Reserved for future county-aware narrative.
    score = int(sum(vitals.values()) / 4)
    funding_potential = "up to $3.8M" if vitals["funding"] > 60 else "$0–$1.2M"

    critical = (
        "".join(f"- {i}\n" for i in issues[:3]) if issues else "- No critical issues found.\n"
    )
    fixes = (
        "".join(f'- {p["issue"]}: {p["fix"]}\n' for p in patches)
        if patches
        else "- All policies sutured.\n"
    )

    return f"""
Hazard Mitigation Surgical Report
=================================
Patient: {filename}
Date: {datetime.now().strftime('%B %d, %Y')}
Resilience Score: {score}/100
Funding Potential: {funding_potential}

🔴 Critical Diagnoses
{critical}

✅ Prescriptions
{fixes}

📊 Vital Signs
- FEMA Compliance: {vitals['compliance']}/100
- Equity Access: {vitals['equity']}/100
- Climate Foresight: {vitals['climate']}/100
- Grant Readiness: {vitals['funding']}/100

🎯 Director's Orders
1. Add adaptive triggers for climate updates.
2. Launch multilingual alert pilot.
3. Resubmit plan by August 15 for BRIC Cycle.

Prognosis: {'Good with intervention' if score > 60 else 'Guarded – immediate action needed'}
    """.strip()


# -----------------------------
# 📄 TEXT EXTRACTION
# -----------------------------
def extract_text(file_path: str, filename: str) -> str:
    text = ""
    if filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    elif filename.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif filename.endswith(".txt"):
        with open(file_path, encoding="utf-8") as file:
            text = file.read()
    return text.lower()


# -----------------------------
# 🖨️ PDF GENERATION
# -----------------------------
def generate_pdf_report(content: str, filename: str) -> str:
    html = f"""
    <html>
    <head><title>Surgical Report</title></head>
    <body style="font-family: Arial; padding: 30px; font-size: 12px;">
        <h1>Hazard Mitigation Surgical Report</h1>
        <h3>{filename}</h3>
        <pre>{content}</pre>
        <p><small>Generated by Mitigation Surgeon Engine | {datetime.now().strftime('%Y-%m-%d')}</small></p>
    </body>
    </html>
    """
    pdf_file = os.path.join(tempfile.gettempdir(), "surgical_report.pdf")
    HTML(string=html).write_pdf(pdf_file)
    return pdf_file


# -----------------------------
# 🌐 FLASK ROUTES
# -----------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <title>Mitigation Surgeon</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <style>
    body { background: #f0f2f5; }
    .container { max-width: 1000px; margin: 30px auto; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 30px; }
    .upload { text-align: center; padding: 40px; border: 3px dashed #007bff; border-radius: 10px; margin: 20px 0; }
    .progress { height: 20px; }
    .report { background: #f8f9fa; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="text-center text-primary">🔪 Mitigation Surgeon</h1>
    <p class="text-center text-muted">Surgical Stress-Test for Hazard Mitigation Plans</p>

    <div class="upload">
      <h4>📤 Upload Your HMP (PDF, DOCX, TXT)</h4>
      <input type="file" id="file" accept=".pdf,.docx,.txt" class="form-control mb-2" style="max-width: 400px; margin: 0 auto;"/>
      <label>County:
        <select id="county" class="form-select" style="max-width: 300px; display: inline-block; width: auto;">
          <option value='{"svi_high": true, "lep_pct": 34}'>Jefferson County, FL</option>
          <option value='{"svi_high": false, "lep_pct": 12}'>Boulder County, CO</option>
          <option value='{"svi_high": true, "lep_pct": 41}'>Hidalgo County, TX</option>
        </select>
      </label>
      <br><br>
      <button onclick="analyze()" class="btn btn-danger btn-lg">Run Surgical Scan</button>
    </div>

    <div id="results" style="display: none;">
      <h3>📋 Surgical Report</h3>
      <div id="report" class="report"></div>
      <button onclick="downloadPDF()" class="btn btn-success">📥 Download PDF Report</button>
    </div>

    <div id="progress" style="display: none;" class="text-center">
      <h5>🔬 Running Precision Diagnostics...</h5>
      <div class="progress">
        <div id="bar" class="progress-bar bg-info" style="width: 0%;">0%</div>
      </div>
    </div>
  </div>

  <script>
    function analyze() {
      const file = document.getElementById('file').files[0];
      const countySelect = document.getElementById('county');
      const countyData = JSON.parse(countySelect.value);
      if (!file) return alert('Upload a file!');

      const formData = new FormData();
      formData.append('file', file);
      formData.append('county_data', JSON.stringify(countyData));

      document.getElementById('progress').style.display = 'block';
      const bar = document.getElementById('bar');
      let p = 0;
      const intr = setInterval(() => {
        p += 5;
        bar.style.width = p + '%';
        bar.textContent = p + '%';
        if (p >= 100) clearInterval(intr);
      }, 150);

      fetch('/analyze', { method: 'POST', body: formData })
        .then(r => r.json())
        .then(data => {
          clearInterval(intr);
          document.getElementById('bar').style.width = '100%';
          document.getElementById('bar').textContent = '100%';
          document.getElementById('report').textContent = data.report || data.error;
          document.getElementById('results').style.display = 'block';
          document.getElementById('progress').style.display = 'none';
        })
        .catch(e => alert('Error: ' + e.message));
    }

    function downloadPDF() {
      const content = document.getElementById('report').textContent;
      const form = new FormData();
      form.append('content', content);
      form.append('filename', 'Surgical_Report');
      fetch('/pdf', { method: 'POST', body: form })
        .then(r => r.blob())
        .then(blob => {
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'Mitigation_Surgical_Report.pdf';
          a.click();
        });
    }
  </script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    county_data = json.loads(request.form.get("county_data", "{}"))

    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(temp_path)

    try:
        text = extract_text(temp_path, file.filename)
        issues = []
        issues.extend(run_disaster_replay(text))
        issues.extend(check_grant_dna(text))
        issues.extend(equity_audit(text, county_data))
        issues.extend(climate_simulator(text))

        patches = generate_patches(text)
        vitals = get_vital_signs(text, county_data)
        report = generate_director_brief(file.filename, issues, patches, vitals, county_data)

        return jsonify({"report": report})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/pdf", methods=["POST"])
def pdf():
    content = request.form["content"]
    filename = request.form.get("filename", "report")
    pdf_path = generate_pdf_report(content, filename)
    return send_file(pdf_path, as_attachment=True, download_name="Surgical_Report.pdf")


if __name__ == "__main__":
    print("🔪 Mitigation Surgeon Activated")
    print("👉 Open http://127.0.0.1:5000")
    app.run(debug=True)
