AI Document Assistant – LLM-Powered Resume, SOP & Cover Letter Generator

This project is an AI-powered document generation system built with FastAPI and integrated with Groq’s Llama 3.3 70B LLM.
It automatically creates scholarship-ready documents by analyzing the user’s resume and the provided scholarship details.

✅ Key Features

Enhanced Resume Generator
Automatically tailors the user’s resume to match a specific scholarship domain (AI, Biomedical, Climate, Materials, Policy, etc.).
Removes irrelevant details and rewrites bullet points professionally.

Cover Letter Generator
Produces a strong, personalized, domain-aligned cover letter in 3–5 paragraphs.

Statement of Purpose (SOP) Generator
Creates a detailed 900–1300 word SOP with motivation, background mapping, research alignment, and future goals.

Professional Email Writer
Generates concise, formal scholarship inquiry or application emails.

✅ How It Works

Upload Resume (PDF)
The system extracts text using pdfplumber.

Provide Scholarship JSON
The JSON is parsed and converted into a readable form for the AI.

Intelligent Prompt Builder
A domain-aware prompt engine analyzes the scholarship field and
reinterprets the applicant’s existing experience to fit the domain—
without fabricating any details.

LLM Generation (Groq API)
A structured prompt is sent to Groq’s Llama model, which returns the tailored document.

FastAPI Endpoints

/generate/resume

/generate/coverletter

/generate/sop

/generate/email

✅ Tech Stack

FastAPI – Backend service

Groq Llama-3.3-70B – LLM for document generation

Python – Core logic

pdfplumber – Resume text extraction

dotenv – Environment variables management

Requests – API communication

✅ Purpose

This project automates scholarship document writing and ensures that every generated output is:
✅ Domain-specific
✅ Professional
✅ Tailored
✅ ATS-friendly
✅ Based strictly on the user’s real resume

It acts as a full AI Document Assistant for students applying to scholarships, research programs, and academic opportunities.

LLM-Powered Resume, SOP, Cover Letter & Email Generator

The AI Document Assistant is a FastAPI-based backend service that uses advanced Large Language Models (LLMs) to automatically generate high-quality, scholarship-ready documents.
It intelligently analyzes the user’s resume and scholarship details to produce:

✅ Tailored Resume
✅ Cover Letter
✅ Statement of Purpose (SOP)
✅ Professional Email

This system ensures domain-adapted, highly relevant academic documents without fabricating any information.

🚀 Features
✅ 1. Enhanced ATS-Friendly Resume Generator

Converts your existing resume into a scholarship-specific version

Removes irrelevant details automatically

Rewrites experience and skills based on the scholarship domain

Ensures academic phrasing and clarity

✅ 2. Cover Letter Generator

Generates a clean, professional 3–5 paragraph letter

Directly aligned with scholarship goals and requirements

Highlights your motivation and competence

✅ 3. SOP (Statement of Purpose) Writer

Produces a 900–1300 word SOP

Includes motivation, background, research alignment & future goals

Reinterprets your experience to match the scholarship field

✅ 4. Professional Email Writer

Creates well-structured scholarship inquiry or application emails

Focuses on clarity, brevity, and domain relevance

🧠 Intelligent Prompt Engine

The system includes an advanced domain-aware prompt builder that:

Detects scholarship domain (AI, Biomedical, Robotics, Climate, Policy, Materials, etc.)

Maps the applicant’s real experience into the domain (without fabrication)

Removes irrelevant information

Enforces academic writing quality

Keeps all generated documents consistent and scholarship-specific

This ensures highly accurate and personalized outputs every time.

API Endpoints
POST /generate/resume

Generates a fully tailored resume.

POST /generate/coverletter

Creates a scholarship-specific cover letter.

POST /generate/sop

Produces a detailed Statement of Purpose.

POST /generate/email

Generates a short, professional scholarship email.

How It Works

✅ User uploads resume (PDF)

✅ Scholarship JSON is provided

✅ System extracts text using pdfplumber

✅ Scholarship metadata is parsed

✅ Prompt builder constructs a domain-adapted prompt

✅ Groq Llama-3.3-70B generates the document

✅ Output is returned as JSON

✅ Why This Project?

This system is ideal for:

Students applying for international scholarships

Research applicants

Fellowship candidates

Universities offering automated document assistance

Platforms providing AI-powered academic tools

It removes writing stress and ensures your documents appear highly professional and tailored.


Conclusion:

The AI Document Assistant is a powerful LLM-integrated backend that transforms ordinary resumes and info into scholarship-ready documents through domain intelligence and precise prompt engineering.
