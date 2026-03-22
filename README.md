
# ⚡ AutoReach: Autonomous GenAI Outreach Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-8A2BE2?style=for-the-badge&logo=google)
![Apify](https://img.shields.io/badge/Apify-Scraper-00FF00?style=for-the-badge)
![Hunter.io](https://img.shields.io/badge/Hunter.io-Email_Auth-FF4500?style=for-the-badge)

> **Objective:** Penetrate Applicant Tracking Systems (ATS) through deterministic, LLM-driven direct networking.

AutoReach is a zero-touch, automated outreach pipeline. It dynamically acquires target personnel (Recruiters, ML Engineers), resolves their verified corporate contact data, and deploys a hyper-personalized, context-aware email draft to a local Gmail client. 

## 🧠 The "God-Mode" Routing Engine

Traditional cold email scripts use static templates. AutoReach uses **Dynamic Profile Stitching**.

The onboard LLM (Gemini 2.5 Flash) acts as a contextual routing engine. It ingests a master payload of 5 different resumes (SDE, ML, GenAI, Data, Research) and dynamically alters the outreach narrative based on the target's specific job title and company domain:

* **[PATH A] Software Engineering:** Triggers the Backend architecture payload (FastAPI, Redis, PostgreSQL distributed state management).
* **[PATH B] Generative AI:** Triggers the LLMOps payload (PEFT Fine-Tuning, DeepSeek/Mistral Voice Agents, LangChain).
* **[PATH C] Machine Learning / Healthcare:** Triggers the Computer Vision payload (MONAI, 3D U-Net Alzheimer's pipelines, ONNX Inference).

## ⚙️ Core Architecture (The 4-Phase Pipeline)

1.  **Reconnaissance (Apify API):** Executes programmatic Google Dorks against LinkedIn to identify the exact human target handling university recruitment or engineering management for a specified domain.
2.  **Target Acquisition (Hunter.io API):** Bypasses standard rate limits to cross-reference the target's name and company domain, extracting and verifying their internal corporate email address.
3.  **Neural Drafting (Google GenAI):** Synthesizes the target data with the God-Mode routing engine to generate a sub-140-word, highly technical outreach draft.
4.  **Payload Delivery (Gmail API):** Utilizes cached OAuth 2.0 tokens to silently push the generated draft directly to the user's Gmail Drafts folder. **(Failsafe: AutoReach never transmits emails without manual human review).**

## 🛠️ Initialization Protocol

**1. Clone the Matrix**
```bash
git clone [https://github.com/rusheel080703/AutoReach.git](https://github.com/rusheel080703/AutoReach.git)
cd AutoReach
```

**2. Install Dependencies**
```bash
pip install google-genai apify-client google-auth-oauthlib google-api-python-client requests
```

**3. Configure Environment Variables**
Securely inject your API tokens into the configuration block (or use a `.env` file):
* `APIFY_API_TOKEN`
* `HUNTER_API_KEY`
* `GEMINI_API_KEY`

**4. Authorize Google Cloud**
* Enable the Gmail API via GCP.
* Drop `credentials.json` into the root directory.
* On first execution, authenticate the OAuth client to generate the persistent `token.json` cache.

## 🚀 Execution Telemetry

Inject your target domains into the execution loop:
```python
COMPANIES_TO_TARGET = [
    {"domain": "nvidia.com", "role": "University Recruiter"},
    {"domain": "apple.com", "role": "Machine Learning Manager"}
]
```

Deploy the agent:
```bash
python outreach.py
```

## ⚠️ Ethical Compliance
This architecture is engineered for highly targeted, ethical networking. It is designed strictly for local staging (Drafts) and relies on manual human authorization for transmission. Do not use for mass-spam or API abuse.
