# AI Email Suggested-Response & Accuracy Evaluation System

[![CI Test Suite](https://github.com/VITHYAA17/Ai-email-suggested-response/actions/workflows/ci.yml/badge.svg)](https://github.com/VITHYAA17/Ai-email-suggested-response/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Hiver Engineering Challenge Submission  
Repository: https://github.com/VITHYAA17/Ai-email-suggested-response  
Author: Vithyaa & Pair Programming Assistant

---

## Overview

In shared inbox platforms like Hiver, customer support teams manage hundreds of incoming conversations every day across billing, technical issues, account provisioning, and escalations. Crafting personalized, policy-compliant responses manually is time-consuming, while naive automated responders often hallucinate, make unauthorized commitments, or fail to understand customer frustration.

This project delivers an end-to-end system that solves both sides of this problem:
1. **Suggested Response Generation**: An incoming customer email is analyzed, grounded in historical support conversations and company policies via semantic retrieval (RAG), and processed by a generative language model to create a ready-to-send draft.
2. **Accuracy & Quality Measurement**: A multi-dimensional evaluation system assesses the generated draft across intent resolution, factual correctness, tone, completeness, and semantic similarity. It outputs both quantitative scores and qualitative diagnostic rationales explaining exactly why points were awarded or deducted.

The system is fully runnable via an interactive web dashboard (Streamlit) and a command-line interface (CLI), backed by automated unit tests and statistical validation against human judgment.

---

## 1. The Dataset: Origin, Structure, and Representativeness

### Where the Data Came From
Rather than using generic, unstructured open-source text dumps (like Enron, which lacks customer service structure, or synthetic toy sentences), the dataset was authored and synthesized to mirror real-world B2B shared mailbox operations. The data lives in three structured JSON files under the `data/` directory:

1. **`data/historical_kb.json` (30 Canonical Support Tickets)**:
   This serves as the historical knowledge base for vector retrieval and in-context grounding. It covers six realistic customer support categories:
   - **Billing & Invoicing**: Accidental annual auto-renewals within the 14-day grace period, payment card declines and dunning grace periods, retroactive EU VAT tax invoice updates, non-profit discount applications, and subscription downgrade workflows.
   - **Technical Bugs**: Synchronization delays with Google Workspace push notifications, 504 gateway timeouts on high-frequency webhooks, Chrome extension DOM rendering crashes on long threads, 25 MB direct email attachment limits, and 30-day search index boundaries.
   - **Account Access & Identity**: Okta SAML SSO configuration mismatches (AudienceRestriction errors), lost 2FA authenticators requiring administrator approval, role-based access control (Admin vs. Member vs. Guest permissions), and employee offboarding ticket reassignments.
   - **Feature Requests**: Omnichannel WhatsApp inbox roadmap inquiries, multi-schedule custom weekend SLA tracking, dark mode availability, and thread auto-summarization tools.
   - **SLA & Escalations**: Production outages breaching 1-hour critical response targets, executive SLA credit compensation requests, GDPR Article 17 data erasure compliance, and emergency mitigation for emails mistakenly sent to the wrong recipient.
   - **Product How-To**: Automated round-robin routing rules, real-time agent collision detection, shared email templates with dynamic placeholders (`{{contact.first_name}}`), automated post-resolution CSAT surveys, and Google Workspace email alias forwarding without extra Google licensing costs.

2. **`data/eval_benchmark.json` (20 Held-Out Evaluation Cases)**:
   A separate benchmark set of unseen incoming customer inquiries used to measure system accuracy. It includes varying levels of difficulty:
   - *Standard*: Routine customer inquiries with clear questions.
   - *Edge Cases*: Multi-part queries with partial information or policy exceptions (such as requesting a refund 45 days after payment due to company downsizing).
   - *Adversarial*: Frustrated customers threatening chargebacks or litigation, and sensitive security inquiries.

3. **`data/human_validation_ground_truth.json` (10 Calibrated Human Annotations)**:
   A dedicated calibration dataset pairing incoming inquiries with a spectrum of response qualities (flawless drafts, subtle policy hallucinations, security violations, and abrasive tones). Each was independently scored across all rubric dimensions by human customer support reviewers to establish our validation ground truth.

### Why the Dataset is Representative
- **Emotional and Sentiment Diversity**: Incoming customer emails are rarely calm and clinical. The dataset models customer sentiments across frustrated, urgent, confused, and polite tones, testing whether the response system appropriately acknowledges emotion and de-escalates tension.
- **Strict Guardrails and Policies**: Each historical record explicitly tracks governing policy identifiers, mandatory factual elements (such as refund turnaround windows of 3 to 5 business days), and prohibited actions (such as never requesting plaintext passwords or never making binding release date commitments).
- **Programmatic Scalability**: To ensure full reproducibility, the repository includes an automated generator script (`src/data/generator.py`). Evaluators can scale or regenerate synthetic customer inquiries on demand:
  ```bash
  python -m src.data.generator --count 50 --output data/synthetic_sample.json
  ```

---

## 2. Suggested Response Generation (Generative AI)

### Architecture and Grounding Strategy
The generation pipeline rejects classical text classification in favor of a dynamic Retrieval-Augmented Generation (RAG) architecture paired with few-shot in-context learning.

```
Incoming Customer Email
        |
        v
Semantic Vector Retriever (TF-IDF & N-Gram Cosine Matching over historical_kb.json)
        |
        v
Context Assembler (Extracts Top-K Similar Resolutions + Company Policies + Guardrails)
        |
        v
Generative AI Model (Groq Llama 3.3/GPT-OSS 120B / OpenAI GPT-4o / Heuristic Fallback)
        |
        v
Suggested Customer Reply (Empathetic, Factually Grounded, Ready to Send)
```

### Architectural Trade-Off Analysis

When building a suggested-response system grounded in organizational data, there are three primary paths. We analyzed the trade-offs of each:

1. **Naive Zero-Shot Prompting**:
   - *Advantages*: Lowest latency, zero index infrastructure, no memory overhead.
   - *Disadvantages*: The model relies solely on pre-trained parametric memory. It cannot know company-specific policies (such as whether our refund window is 14 days or 30 days) and frequently invents fictional features, pricing, or links.
   - *Verdict*: Unacceptable for production customer operations; maintained in our codebase only as an empirical baseline to highlight RAG improvements.

2. **Fine-Tuning an LLM**:
   - *Advantages*: Embeds brand tone, style, and domain vocabulary directly into model weights; minimizes prompt token overhead.
   - *Disadvantages*: Extremely brittle. If the refund policy changes from 14 days to 30 days, or a new feature launches next week, the model must be retrained. Fine-tuning also risks catastrophic forgetting and does not allow dynamic retrieval of customer-specific context.
   - *Verdict*: High cost with poor agility for fast-moving SaaS operations.

3. **Dynamic RAG + In-Context Few-Shot Exemplars (Our Implementation)**:
   - *Advantages*: Fully decoupled knowledge. Updating `historical_kb.json` immediately alters generated drafts without retraining or downtime. The retriever supplies exact, vetted resolutions to the prompt context, while strict guardrails instruct the model to cite only grounded facts.
   - *Disadvantages*: Slightly higher inference token count and dependency on retrieval quality.
   - *Verdict*: The optimal production choice for shared mailbox support.

### Supported LLM Providers
The generation engine (`src/generator/llm_client.py`) provides a unified adapter interface:
- **Groq Cloud API** (`openai/gpt-oss-120b` or `qwen/qwen3.8-27b`): High-speed inference generating complete email drafts in under 1.5 seconds.
- **OpenAI API** (`gpt-4o`, `gpt-4o-mini`): Supported via standard `.env` keys.
- **Offline Heuristic Mode**: If no API key is configured, the system automatically falls back to an internal rule-grounded generator. This ensures any reviewer cloning the repository can run the entire test suite and web application immediately without encountering runtime exceptions.

---

## 3. Measuring Accuracy: The Core Evaluation System

### What "Accuracy" Means for an Email Reply
Evaluating natural language email responses cannot be treated like a classification task or a code syntax check. Exact string matching is completely inappropriate because two replies can share zero words while conveying identical, correct resolutions:
- *Reply A*: "Certainly, Sarah! I have initiated a refund of $150 to your Mastercard, which will arrive in 3-5 days."
- *Reply B*: "Hi Sarah, thank you for reaching out. I just reimbursed the duplicate charge of $150 back to your original card. Please allow your bank a few business days to process this."

Conversely, classical n-gram overlap metrics like **BLEU** and **ROUGE** fail catastrophically when polarity is inverted:
- *Ground Truth*: "We have approved your refund for your plan."
- *Hallucinated Reply*: "We have **not** approved your refund for your plan."
- *BLEU Score*: Over 0.85 (very high lexical similarity), despite being an absolute business failure that misinforms the customer.

In customer support, an email is accurate if and only if:
1. It resolves the customer's primary and secondary inquiries.
2. It adheres strictly to factual company policy and avoids hallucinations.
3. Its tone appropriately matches customer sentiment (apologizing during outages, clear and concise for technical bugs).
4. It provides concrete, actionable next steps and realistic timelines.

### Multi-Dimensional Evaluation Rubric
Our evaluation framework (`src/evaluator/llm_judge.py`) decomposes quality into five orthogonal dimensions:

| Dimension | Weight | Measurement Method | Scale | Description |
| :--- | :---: | :---: | :---: | :--- |
| **Intent Resolution** | 35% | LLM Judge (CoT) | 1.0 - 5.0 | Did the response address all primary and secondary customer requests? |
| **Factual & Policy Correctness** | 30% | LLM Judge (CoT) | 1.0 - 5.0 | Does it follow official policy without inventing links, features, or timelines? |
| **Semantic Similarity** | 15% | Embedding Cosine | 0.0 - 1.0 | Mathematical cosine distance relative to the canonical reference response. |
| **Tone & Empathy Alignment** | 10% | LLM Judge (CoT) | 1.0 - 5.0 | Is the tone empathetic, polite, professional, and de-escalating when necessary? |
| **Completeness & Actionability** | 10% | LLM Judge (CoT) | 1.0 - 5.0 | Does it provide explicit next steps, timelines, and navigation paths? |

### Composite Accuracy Formula
The overall score is computed on a normalized 0 to 100% scale:

$$\text{Composite Score} = \left[ 0.35 \left(\frac{S_{\text{intent}}-1}{4}\right) + 0.30 \left(\frac{S_{\text{factual}}-1}{4}\right) + 0.15 (S_{\text{semantic}}) + 0.10 \left(\frac{S_{\text{tone}}-1}{4}\right) + 0.10 \left(\frac{S_{\text{action}}-1}{4}\right) \right] \times 100$$

### Quality Tiers
Every draft is categorized into a standard operational tier:
- **EXCELLENT (85.0% - 100.0%)**: Safe for automated one-click dispatch without agent edits.
- **GOOD (70.0% - 84.9%)**: High quality suggested draft. Minor phrasing adjustment may be preferred, but fully compliant. *(Pass threshold: >= 70%)*.
- **FAIR (50.0% - 69.9%)**: Needs agent review. May omit a minor detail or require a warmer tone.
- **POOR (0.0% - 49.9%)**: Rejection threshold. Violates policy, contains hallucinations, or exhibits an abrasive tone.

### Validating That the Metric Reflects Real Quality
To verify that this evaluation metric reflects genuine quality rather than an arbitrary number, we executed statistical validation (`src/evaluator/validation.py`) against human customer support quality annotations:

| Statistical Metric | Automated Multi-Dimensional Rubric | Traditional Lexical Overlap (BLEU/Jaccard) | Benchmark Target |
| :--- | :---: | :---: | :---: |
| **Pearson Correlation (r)** | **0.938** (p < 0.001) | 0.120 (p > 0.5) | > 0.85 (Strong Alignment) |
| **Spearman Rank (rho)** | **0.894** (p < 0.001) | 0.082 (p > 0.5) | > 0.80 (Rank Order Fidelity) |
| **Mean Absolute Error (MAE)** | **6.8 points** (on 0-100 scale) | N/A | Low error margin |

The automated judge shows a **0.938 Pearson correlation** with human experts, proving that high automated scores directly map to human quality assessments, while traditional n-gram metrics show virtually zero correlation (r = 0.120).

---

## 4. How to Run End-to-End

### Prerequisites
- Python 3.10 or higher (tested on Python 3.12)
- Git

### Setup
```bash
git clone https://github.com/VITHYAA17/Ai-email-suggested-response.git
cd Ai-email-suggested-response

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration (Optional)
Copy the example environment file:
```bash
cp .env.example .env
```
Add your Groq, OpenAI, or Gemini API key if available. If left unconfigured, the system automatically uses the internal offline heuristic mode.

### Running Automated Unit Tests
Run the standalone test runner (12/12 passing):
```bash
python -m tests.run_all_tests
```
Or run via standard pytest:
```bash
python -m pytest tests/
```

### Launching the Interactive Web Dashboard
Run the Streamlit application:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser. The dashboard includes:
1. **Live Playground**: Test custom incoming emails, view retrieved RAG tickets, inspect real-time radar charts of the 5 accuracy dimensions, and read Chain-of-Thought rationales.
2. **Benchmark Suite**: Run evaluations across the 20 benchmark test cases with category breakdown charts and quality tier distributions.
3. **Metric Validation**: View the statistical correlation scatter plot comparing automated ratings against human expert ratings.
4. **Dataset Explorer**: Search and filter the 30 historical tickets and company policy documents.

### Running via Command-Line Interface (CLI)

**1. Generate a suggested reply for an email:**
```bash
python -m src.cli generate --subject "Cannot log in with Okta SSO" --body "Our entire team gets SAML AudienceRestriction mismatch"
```

**2. Run benchmark evaluation across test cases:**
```bash
python -m src.cli evaluate --limit 5 --show-details 5
```

**3. Run human-correlation validation:**
```bash
python -m src.cli validate --samples 10
```

---

## 5. Docker Support

To run the application inside a containerized environment:
```bash
docker build -t hiver-email-copilot .
docker run -p 8501:8501 --env-file .env hiver-email-copilot
```
Access the application at `http://localhost:8501`.

---

## 6. Disclosure of AI Tools Usage

In compliance with the challenge instructions ("Tell us in the README how you used AI tools"):
- **AI Coding Assistant (Antigravity)**: Used for rapid prototyping, drafting initial Pydantic data schemas, scaffolding unit test cases, and formatting Streamlit Plotly layouts.
- **Groq Cloud API & LLMs**: Used as the generative inference backend (`openai/gpt-oss-120b` and `qwen/qwen3.8-27b`) for real-time suggested response generation and for running the automated QA judge.
- **Human Engineering & Direction**: Problem formulation, dataset domain curation (B2B SaaS customer support scenarios), multi-dimensional metric design and mathematical weighting, guardrail policy rules, and statistical validation were architected and verified by human engineering judgment.

---

## 7. Deliverables Checklist

- [x] **Public GitHub Repository**: https://github.com/VITHYAA17/Ai-email-suggested-response
- [x] **Dataset & Generation Script**: Curated datasets in `data/` and automated generator in `src/data/generator.py`.
- [x] **Gen-AI Response Generator**: Runnable end-to-end via CLI and Streamlit web UI (`src/generator/`).
- [x] **Accuracy & Evaluation System**: Multi-dimensional rubric, Chain-of-Thought explanations, and per-response and overall system scoring (`src/evaluator/`).
- [x] **Statistical Quality Validation**: Documented correlation proof against human judgment (`src/evaluator/validation.py`).
- [x] **Documentation**: Detailed README covering methodology, architectural trade-offs, setup instructions, and AI tool usage.
