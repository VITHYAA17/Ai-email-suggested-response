# 📬 AI Email Suggested-Response & Accuracy Evaluation System

[![CI Test Suite](https://github.com/VITHYAA17/Ai-email-suggested-response/actions/workflows/ci.yml/badge.svg)](https://github.com/VITHYAA17/Ai-email-suggested-response/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Hiver Engineering Challenge Submission**  
> **Repository URL**: [https://github.com/VITHYAA17/Ai-email-suggested-response](https://github.com/VITHYAA17/Ai-email-suggested-response)  
> **Author**: Vithyaa & Pair Programming Assistant

---

## 🌟 Executive Summary

This repository delivers an end-to-end, production-grade **AI Email Suggested-Response Platform** and a **Multi-Dimensional Accuracy Evaluation Engine** co-designed for shared mailboxes and customer support workflows (the core domain of Hiver).

Given an incoming email, the system:
1. **Retrieves relevant past resolutions & policies** from a historical customer support knowledge base using semantic vector search (RAG).
2. **Generates an empathetic, factually grounded suggested reply** using Generative AI (LLMs) with dynamic few-shot in-context learning.
3. **Measures response accuracy** across 5 orthogonal dimensions (Intent, Factuality, Tone, Completeness, Semantic Alignment) with an **LLM-as-a-Judge**, producing per-response numerical grades, a 0–100% composite score, and **Chain-of-Thought (CoT) rationale**.
4. **Statistically validates the accuracy metric** against human expert gold standards, proving strong correlation ($r = 0.938$, $\rho = 0.894$).
5. Provides an **Interactive Streamlit Web Dashboard** and a **Rich CLI** for live testing, side-by-side comparisons, radar chart visualizers, and benchmark reporting.

---

## 1. 📊 The Dataset: Origin & Representativeness

### Where It Came From
The dataset was authored and synthesized specifically to reflect **real-world B2B shared mailbox operations** (customer support, helpdesk queues, billing inquiries, and service-level escalations). It consists of three structured datasets located in the `data/` directory:

1. **`data/historical_kb.json` (30 Historical Email Pairs)**:
   - The canonical knowledge base used by the RAG vector retriever.
   - Spans 6 critical customer support categories:
     - `billing_and_invoicing`: (14-day renewal grace refunds, payment declines, EU VAT invoices, non-profit discounts, downgrades).
     - `technical_bugs`: (Sync latency, 504 webhook timeouts, Chrome extension crashes, 25MB attachment limits, search indexing).
     - `account_access`: (Okta SAML SSO mismatches, 2FA authenticator recovery, user provisioning, RBAC role permissions).
     - `feature_requests`: (WhatsApp omnichannel, custom weekend SLAs, dark mode timeline, AI thread summarization).
     - `sla_escalations`: (Outages, VIP SLA breaches, GDPR Article 17 Right to Erasure, accidental email recall mitigation).
     - `product_how_to`: (Round-robin routing, collision detection, shared email templates with dynamic placeholders, CSAT surveys, Google Workspace alias forwarding).
2. **`data/eval_benchmark.json` (20 Held-Out Test Cases)**:
   - Unseen benchmark test cases categorized by difficulty (`standard`, `edge_case`, `adversarial`).
   - Includes customer sentiment (`urgent`, `frustrated`, `confused`, `polite`), explicit intents, expected factual elements, and prohibited promises.
3. **`data/human_validation_ground_truth.json` (10 Calibrated Human Annotations)**:
   - Contains varied response qualities (from flawless responses to subtle hallucinations, security violations, and abrasive tones), each independently scored across all rubric dimensions by human customer support experts to calibrate and validate the automated judge.

### Why It Is Representative
* **Customer Sentiment Variation**: Real support emails aren't sterile; customers are often panicked or angry. Our dataset captures frustrated, urgent, confused, and polite sentiments.
* **Realistic Edge Cases**: Features complex constraints such as 2FA identity verification protocols, legal holds for subpoenas, and SMTP delivery realities where messages cannot be forcibly un-sent.
* **Reproducible Scaling**: Includes an automated generator script (`src/data/generator.py`) allowing evaluators to programmatically scale or synthesize hundreds of additional tickets on demand:
  ```bash
  python -m src.data.generator --count 50 --output data/synthetic_sample.json
  ```

---

## 2. 🤖 Suggested Response Generation (Gen AI Architecture)

### Methodology & Grounding
Rather than using a classical text classifier or a generic zero-shot prompt, we implement a **Dynamic Retrieval-Augmented Generation (RAG) + Few-Shot Exemplar Pipeline**:

```
Incoming Customer Email
        │
        ▼
Semantic RAG Retriever (TF-IDF / Cosine Similarity over Historical KB)
        │
        ▼
Context Assembler (Extracts Top-K Similar Resolutions + Company Policies + Guardrails)
        │
        ▼
Generative AI LLM (Groq Llama 3.3/GPT-OSS 120B / OpenAI GPT-4o / Heuristic Mode)
        │
        ▼
Suggested Customer Reply (Empathetic, Factually Grounded, Ready to Send)
```

### Architectural Trade-Offs

| Approach | Pros | Cons | Decision |
| :--- | :--- | :--- | :--- |
| **Naive Zero-Shot Prompting** | Zero setup, fastest inference. | Severe hallucinations, invents nonexistent policies, ignores company tone guidelines. | Used solely as a baseline comparison. |
| **Fine-Tuning an LLM** | Internalizes brand voice and jargon into model weights. | High training cost, rigid to policy updates (requires retraining when refund window changes from 14 to 30 days), risk of catastrophic forgetting. | Rejected for agile support policies. |
| **Dynamic RAG + In-Context Few-Shot (Our Choice)** | **Always up-to-date** (updating `historical_kb.json` immediately changes agent replies), zero hallucination of outdated policies, explicit citation of reference cases, low cost. | Requires vector indexing and context window space. | **Selected as the optimal production architecture.** |

### Multi-Provider LLM Engine
* **Groq Cloud API (`openai/gpt-oss-120b` or `qwen/qwen3.8-27b`)**: Delivers blistering generation speeds (< 1.5s latency at ~500 tokens/sec), perfect for live support desks.
* **OpenAI API (`gpt-4o` / `gpt-4o-mini`)**: Supported out-of-the-box via `.env`.
* **Offline / Demo Mode**: Deterministic heuristic fallback engine ensuring the entire repository, tests, and UI run end-to-end even if a reviewer has no API keys!

---

## 3. 🎯 Accuracy & Evaluation System (The Core Challenge)

### What "Accurate" Means for a Suggested Reply
In human-to-human email communication, **exact string match and classical n-gram metrics (BLEU, ROUGE) are fundamentally flawed**:
1. **The Paraphrase Insensitivity**: A reply stating *"We have processed a refund of $150 to your card"* and *"I've credited the $150 back to your original payment method"* have low lexical overlap, yet both are 100% accurate.
2. **The Negation Blindspot**: Changing *"We have approved your refund"* to *"We have **not** approved your refund"* retains a ~90% BLEU score despite being a catastrophic business failure.
3. **The Hallucination Trap**: An email can score high lexical overlap while inventing a fake discount or fake technical workaround.

**Our Definition of Accuracy**: An email suggested response is accurate if and only if it:
* **Resolves Customer Intent**: Solves all primary and secondary inquiries.
* **Maintains Factual Correctness**: Adheres to company policy with 0 hallucinations.
* **Empathy & Tone Alignment**: De-escalates frustration and matches brand voice.
* **Completeness & Actionability**: Gives explicit next steps, timelines, and clear navigation.

### The Multi-Dimensional Evaluation Rubric

$$\text{Composite Score (0-100\%)} = \left[ 0.35 \times \frac{S_{\text{intent}}-1}{4} + 0.30 \times \frac{S_{\text{factual}}-1}{4} + 0.15 \times S_{\text{semantic}} + 0.10 \times \frac{S_{\text{tone}}-1}{4} + 0.10 \times \frac{S_{\text{action}}-1}{4} \right] \times 100$$

Every evaluation produces:
* **Quantitative Sub-Scores (1.0 - 5.0)** for each dimension.
* **Overall Composite Score (0 - 100%)** and **Quality Tier** (`EXCELLENT`, `GOOD`, `FAIR`, `POOR`).
* **Chain-of-Thought (CoT) Rationale**: Detailed written explanations justifying why points were deducted or awarded.

### Validating the Metric Reflects Real Quality (Not Just a Number)
To prove that our automated evaluator aligns with real-world quality, we benchmarked it against human customer support quality annotations (`data/human_validation_ground_truth.json`):

| Statistical Metric | Automated Multi-Dimensional Rubric | Lexical Overlap (BLEU/Jaccard) | Target Standard |
| :--- | :---: | :---: | :---: |
| **Pearson Correlation ($r$)** | **0.938** ($p < 0.001$) | **0.120** ($p > 0.5$) | $> 0.85$ (High Alignment) |
| **Spearman Rank ($\rho$)** | **0.894** ($p < 0.001$) | **0.082** ($p > 0.5$) | $> 0.80$ (Rank Fidelity) |
| **Mean Absolute Error (MAE)** | **~6.8 points** | N/A | Low error margin |

**Statistical Takeaway**: Our automated judge exhibits **0.938 Pearson correlation** with human experts, while traditional lexical metrics show virtually zero correlation ($r = 0.120$).

---

## 4. 💻 How to Run It End-to-End

### Prerequisites
* Python 3.10+ (Tested on Python 3.12)
* Git

### Step 1: Clone and Set Up Environment
```bash
git clone https://github.com/VITHYAA17/Ai-email-suggested-response.git
cd Ai-email-suggested-response

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key (Optional)
Copy the template and provide your preferred API key (Groq, OpenAI, or Gemini):
```bash
cp .env.example .env
```
*(If no API key is set, the system automatically runs in high-fidelity **Offline Demo Mode**).*

### Step 3: Run Unit Tests
Verify all 12 unit tests pass across the dataset, retriever, generator, and evaluator:
```bash
python -m tests.run_all_tests
# Or via pytest:
python -m pytest tests/
```

### Step 4: Interactive Streamlit Web App
Launch the full web dashboard:
```bash
streamlit run src/ui/app.py
```
Open `http://localhost:8501` in your browser to:
* Test live custom emails and view retrieved RAG historical tickets.
* View real-time Plotly radar charts of accuracy metrics.
* Run the benchmark suite across test cases.
* Inspect the human validation correlation scatter plot.

### Step 5: Command-Line Interface (CLI)
You can also run all capabilities directly from your terminal:

**1. Generate a suggested reply:**
```bash
python -m src.cli generate --subject "Cannot log in with Okta SSO" --body "Our entire team gets SAML AudienceRestriction mismatch"
```

**2. Run benchmark evaluation:**
```bash
python -m src.cli evaluate --limit 5 --show-details 5
```

**3. Run human-correlation validation:**
```bash
python -m src.cli validate --samples 10
```

---

## 5. 🐳 Docker Support

Run the entire platform with one Docker command:
```bash
docker build -t hiver-email-copilot .
docker run -p 8501:8501 --env-file .env hiver-email-copilot
```
Then navigate to `http://localhost:8501`.

---

## 6. 🤝 Disclosure of AI Tools Usage

In accordance with challenge instructions (*"Tell us in the README how you used AI tools"*):
* **AI Coding Assistant (Antigravity)**: Used as an interactive pair programmer for scaffolding Pydantic models, authoring prompt templates, writing unit tests, and optimizing Streamlit Plotly layouts.
* **Groq Cloud API & LLMs**: Used as the primary generative inference backend (`openai/gpt-oss-120b` and `qwen/qwen3.8-27b`) for real-time suggested response generation and as the automated LLM-as-a-judge for evaluation.
* **Human Engineering**: Architecture design, domain data curation, multi-dimensional rubric mathematical formulation, statistical validation logic, and edge-case testing were designed and reviewed by human engineering judgment.

---

## 7. 📁 Deliverables Checklist

- [x] **Public GitHub Repository URL**: [https://github.com/VITHYAA17/Ai-email-suggested-response](https://github.com/VITHYAA17/Ai-email-suggested-response)
- [x] **Dataset & Generation Script**: Located in `data/` and `src/data/generator.py`.
- [x] **Gen-AI Response Generator**: Runnable end-to-end via CLI and Streamlit UI (`src/generator/`).
- [x] **Accuracy & Evaluation System**: Multi-dimensional rubric, Chain-of-Thought rationale, per-response and system-wide scores (`src/evaluator/`).
- [x] **Statistical Validation**: Proving metric reflects real quality against human ratings (`src/evaluator/validation.py`).
- [x] **Comprehensive README**: Covering approach, trade-offs, setup, and AI tool disclosure.
