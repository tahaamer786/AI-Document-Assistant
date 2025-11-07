from fastapi import FastAPI, UploadFile, File, Form
from dotenv import load_dotenv
import pdfplumber
import requests
import os
import uuid
import json

load_dotenv()

app = FastAPI()  #backend api object ha ye

MAX_RESUME_CHARS = 12000


# PDF KA PATH LENA

def extract_pdf_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text[:MAX_RESUME_CHARS]


def parse_scholarship_json(scholarship_json: str):
    try:
        return json.loads(scholarship_json)
    except:
        return None



# INTELLIGENT, DOMAIN-AWARE PROMPT BUILDER ( MAKE PROMPTS)

#AI KE LIA PROMPT GENERATE KARNA KA MAIN FUNCTION
def build_prompt(doc_type: str, resume_text: str, data: dict | None, raw_json: str):

    # Extract scholarship metadata #Scholarship JSON ko readable format bnata hai
    scholarship_summary = "\n".join(   #Saare formatted lines ko new line se join karta hai
        f"{k.replace('_', ' ').title()}: {v}"
        for k, v in (data or {}).items() #Agar data (scholarship JSON) valid hai → data.items() use ho #Agar data None ho (JSON parsing failed) → an empty {} use ho
        if v and k != "_id"  #k = "title"   → v = "AI Scholarship" #k = "country" → v = "USA"

    )
    if not scholarship_summary.strip():  #Agar JSON empty ho, raw JSON string use karo.
        scholarship_summary = raw_json

    # REAL DOMAIN ANALYSIS LAYER
    # This is the FIX that makes outputs scholarship-specific
    domain_logic = """
YOU MUST FIRST ANALYZE THE SCHOLARSHIP FIELD.

Identify which domain the scholarship belongs to:
- Biomedical / Biosensing / Microfabrication / Biology
- Civil / Environmental / Climate / Infrastructure
- Machine Learning / AI / Data Science
- Economics / Policy / Social Sciences / Inequality
- Robotics / Mechanical / Electrical Engineering
- Chemistry / Materials / Nanotechnology
- Any other detected domain

Then re-map the applicant's REAL experience accordingly:
- If scholarship = BIOMEDICAL → map ML to biosignal analysis, CV to microscopy, data eng to biological datasets.
- If scholarship = MATERIALS → map AI to structural defect analysis, vision for microstructure detection.
- If scholarship = POLICY → map NLP to document analysis, ML to impact modelling.
- If scholarship = CLIMATE → map forecasting to hazard prediction, CV to satellite imagery.
- If scholarship = ENGINEERING → map pipelines to experimentation workflows.
- If scholarship = ECONOMICS → map ML to econometrics-like modelling.

Rules:
✔ NEVER fabricate any new project or degree.
✔ ONLY reinterpret existing resume content.
✔ Tailoring MUST be so strong that the output looks built for THIS scholarship only.
✔ Remove irrelevant details from the resume automatically.
✔ Use professional, academic phrasing.
"""

    # DOCUMENT-TYPE SPECIFIC INSTRUCTIONS

    if doc_type == "Enhanced Resume":
        doc_specific = """
Create a fully scholarship-tailored ATS RESUME.

Structure:
1. SUMMARY → rewrite so skills look relevant to THIS scholarship domain.
2. CORE SKILLS → list only skills relevant to THIS scholarship.
3. EXPERIENCE → rewrite bullet points to highlight transferrable relevance.
4. PROJECTS → keep only projects that can be reinterpreted for this domain.
5. EDUCATION → keep unchanged.
6. Remove ALL irrelevant MLOps/DevOps noise unless academically useful.
"""
    elif doc_type == "Cover Letter":
        doc_specific = """
Write a 3–5 paragraph COVER LETTER.

Must include:
- Why you are applying
- How your background fits the SCHOLARSHIP DOMAIN 
- Clear interdisciplinary mapping
- Strong academic motivation
- Zero fabrication
"""
    elif doc_type == "SOP Document":
        doc_specific = """
Write a 900–1300 word Statement of Purpose with the following structure:
1. Motivation for the domain of the scholarship
2. Applicant's AI/ML background → mapped to the scholarship field
3. Research alignment with the scholarship topic
4. Why THIS institution and THIS project
5. Future research goals
"""
    else:
        doc_specific = """
Write a short 120–180 word PROFESSIONAL EMAIL with a subject line.
Align background with scholarship domain.
"""

    # -------- FINAL PROMPT --------

    final_prompt = f"""
You are an expert scholarship application writer.

APPLICANT RESUME (verbatim):
----------------------------
{resume_text}

SCHOLARSHIP DETAILS:
----------------------------
{scholarship_summary}

TASK:
Generate ONLY this document → {doc_type}

STRICT RULES:
- DO NOT fabricate any degree, project, or experience.
- You MUST reinterpret existing resume details to match the scholarship field.
- Every line must sound tailored specifically to THIS scholarship.
- Output plain text only.
- Domain interpretation is mandatory (see logic below).

DOMAIN ADAPTATION LOGIC:
{domain_logic}             

DOCUMENT REQUIREMENTS:
{doc_specific}

Begin now.
"""

    return final_prompt


# ------------------------------------------------
# GROQ API REQUEST
# ------------------------------------------------

def generate_with_groq(prompt: str):
#Ye prompt ko Groq API par send karta hai.

    api_url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You do not fabricate facts and must obey instructions exactly."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.10,
        "max_tokens": 6000,
    }

    r = requests.post(api_url, headers=headers, json=payload)

    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    return "Groq API Error: " + r.text


# ------------------------------------------------
# COMMON HANDLER
# ------------------------------------------------

async def handle_generation(scholarship_json: str, resume_file: UploadFile, doc_type: str):

    temp_file = f"temp_{uuid.uuid4().hex}.pdf"
    with open(temp_file, "wb") as f:
        f.write(await resume_file.read())

    resume_text = extract_pdf_text(temp_file)
    data = parse_scholarship_json(scholarship_json)

    prompt = build_prompt(doc_type, resume_text, data, scholarship_json)
    output = generate_with_groq(prompt)

    os.remove(temp_file)
    return output


# FASTAPI 4 END-POINTS DEFINED

@app.post("/generate/resume")
async def generate_resume(scholarship_json: str = Form(...), resume_file: UploadFile = File(...)):
    return {"content": await handle_generation(scholarship_json, resume_file, "Enhanced Resume")}


@app.post("/generate/coverletter")
async def generate_coverletter(scholarship_json: str = Form(...), resume_file: UploadFile = File(...)):
    return {"content": await handle_generation(scholarship_json, resume_file, "Cover Letter")}


@app.post("/generate/sop")
async def generate_sop(scholarship_json: str = Form(...), resume_file: UploadFile = File(...)):
    return {"content": await handle_generation(scholarship_json, resume_file, "SOP Document")}


@app.post("/generate/email")
async def generate_email(scholarship_json: str = Form(...), resume_file: UploadFile = File(...)):
    return {"content": await handle_generation(scholarship_json, resume_file, "Scholarship Email")}


