import os
import os.path
import base64
import requests
from google import genai
from apify_client import ApifyClient
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# ==========================================
# 1. YOUR CREDENTIALS (PUT YOUR NEW KEYS HERE!)
# ==========================================
HUNTER_API_KEY = "YOUR_API_KEY_HERE" 
APIFY_API_TOKEN ="YOUR_API_KEY_HERE"
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

# ==========================================
# 2. YOUR "GOD-MODE" PERSONALIZATION ENGINE
# ==========================================
MY_PROFILE = """
Name: Rusheel Vijay Sable
Education: Master of Science in Computer Science, University of Southern California (USC). GPA: 3.65/4.0. Expected Grad: May 2027.
Undergrad: B.Tech in CSE, MIT-World Peace University (CGPA: 9.07/10).
Goal: Seeking a 2026 Internship in Software Engineering (SDE), Machine Learning, Generative AI, or AI Research.

WORK EXPERIENCE:
1. Graduate Research Assistant @ USC (Feb 2026-Present): Architecting a harmonized neuroimaging pipeline for ADNI and HCP-Aging using MONAI. Training a MONAI-based 3D U-Net for optic nerve segmentation and modeling Alzheimer's progression using Gaussian Processes and Cox models.
2. Full Stack / GenAI Intern @ Markytics.AI (Jan 2025-June 2025): Launched DeepSeek & Mistral voice-enabled chatbots handling 500+ monthly interactions (94% intent accuracy). Built an end-to-end GPT document pipeline processing 1000+ POs/month. Led a 3-person team to architect AI backends with Django and LangChain.
3. Data Analyst Intern @ Modi Innovations (June 2024-Aug 2024): Deployed ARIMA, SARIMA, and Prophet time-series models for inventory demand, boosting accuracy by 20% and reducing stockouts by 25%.

ADVANCED PROJECTS:
- AdaptIQ (Distributed Systems/Backend): Autonomous AI tutor built with FastAPI, Mistral LLM, Redis (in-memory caching), and PostgreSQL, reducing data latency by 40%.
- ResolveAI (GenAI/LLMOps): Intelligent debt recovery agent using Parameter-Efficient Fine-Tuning (PEFT) on Mistral/DeepSeek for streaming inference.
- CypherGaze / NeuroHUD (Computer Vision): Real-time AI emotion detector using an OpenCV + MediaPipe pipeline with ONNX inference maintaining 30+ FPS.
- FractureNet & Alzheimer's CNN (Healthcare AI): Xception-based fracture pipeline with Grad-CAM (95% accuracy) and an Alzheimer's CNN trained on 5000+ MRI scans (94% accuracy, published in IJCRT).
"""

COMPANIES_TO_TARGET = [
    {"domain": "nvidia.com", "role": "University Recruiter"},
    {"domain": "medtronic.com", "role": "Early Career Talent"},
    {"domain": "apple.com", "role": "Machine Learning Manager"},
    {"domain": "amazon.com", "role": "Software Engineering Recruiter"}
]

# ==========================================
# 3. THE PIPELINE LOGIC
# ==========================================
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def create_gmail_draft(to_email, subject, body):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to_email
    message['Subject'] = subject
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'message': {'raw': encoded_message}}
    service.users().drafts().create(userId="me", body=create_message).execute()
    print(f"✅ Draft successfully created for {to_email}!")

def run_fully_automatic_pipeline(company_domain, job_title):
    client = ApifyClient(APIFY_API_TOKEN)
    company_name = company_domain.split('.')[0].capitalize()

    # A. SCOUT (Apify)
    print(f"🚀 Finding {job_title} at {company_name}...")
    run_input = { "queries": f"site:linkedin.com/in/ '{job_title}' '{company_name}'", "maxPagesPerQuery": 1 }
    run = client.actor("apify/google-search-scraper").call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    
    if not items or 'organicResults' not in items[0] or not items[0]['organicResults']:
        raise Exception("No LinkedIn profile found.")
        
    full_name = items[0]['organicResults'][0].get('title', '').split("-")[0].strip()

    # B. PHONEBOOK (Hunter.io)
    print(f"📧 Getting email for {full_name} via Hunter.io...")
    first_name = full_name.split()[0]
    last_name = full_name.split()[-1]
    
    hunter_url = f"https://api.hunter.io/v2/email-finder?domain={company_domain}&first_name={first_name}&last_name={last_name}&api_key={HUNTER_API_KEY}"
    hunter_req = requests.get(hunter_url)
    
    if hunter_req.status_code == 200:
        data = hunter_req.json().get('data', {})
        email = data.get('email')
        if not email:
            email = f"university_recruiting@{company_domain}"
    else:
        print(f"⚠️ Hunter Error {hunter_req.status_code}: {hunter_req.text}")
        email = f"university_recruiting@{company_domain}"

    # C. THE BRAIN (Gemini)
    print(f"🧠 Gemini is writing the personalized email...")
    ai_client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are an elite executive recruiter writing a cold outreach email on behalf of Rusheel.
    
    Student Profile: {MY_PROFILE}
    Target Recruiter: {full_name}, {job_title} at {company_name}.
    
    Task: Write a highly personalized, confident, and professional cold email (strictly under 140 words).
    
    CRITICAL ROUTING RULES (Choose ONLY ONE path based on the target job title/company):
    - Path A (If targeting SDE/Backend roles): Focus heavily on Markytics.AI (Django/React architecture) OR AdaptIQ (FastAPI/Redis/PostgreSQL low-latency design). Mention Java/C++/Golang.
    - Path B (If targeting GenAI/LLM roles): Focus entirely on ResolveAI (PEFT fine-tuning on Mistral/DeepSeek) OR the Markytics.AI voice agents (LangChain/RAG).
    - Path C (If targeting ML/Computer Vision/HealthTech): Focus on the USC Research (MONAI/3D U-Net) OR CypherGaze (ONNX/OpenCV) OR FractureNet/Alzheimer's CNN.
    - Path D (If targeting Data Science/Analytics): Focus on Modi Innovations (ARIMA/SARIMA time-series forecasting, PowerBI).
    
    Drafting Rules:
    1. Hook the reader immediately. State Rusheel is a USC MS CS student and mention that you just formally applied for their Summer 2026 Internship online.
    2. Include 1-2 hard numbers/metrics from the chosen path (e.g., "reduced latency by 40%", "94% accuracy").
    3. You are reaching out directly because you believe your specific experience aligns perfectly with their team.
    4. Keep the tone ambitious, concise, and highly technical. No generic fluff. 
    5. Sign off as Rusheel Vijay Sable.
    """
    
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    email_body = response.text
    subject = f"USC MS CS Student / 2026 Internship Inquiry - Rusheel Vijay Sable"

    # D. THE MAILMAN (Gmail)
    create_gmail_draft(email, subject, email_body)

# ==========================================
# 4. EXECUTE THE BULK RUN
# ==========================================
print(f"Starting bulk outreach for {len(COMPANIES_TO_TARGET)} companies...\n")

for target in COMPANIES_TO_TARGET:
    try:
        run_fully_automatic_pipeline(target["domain"], target["role"])
    except Exception as e:
        print(f"⚠️ Skipped {target['domain']} due to error: {e}")
    print("-" * 50)

print("\n🎉 Pipeline complete! Go check your Gmail Drafts.")