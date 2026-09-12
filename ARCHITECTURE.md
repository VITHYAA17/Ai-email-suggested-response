# System Architecture: AI Email Suggested-Response & Accuracy Platform

## 1. High-Level Architectural Flow

```
+-----------------------------------------------------------------------------------------+
|                                 INCOMING CUSTOMER EMAIL                                 |
|                         (Subject, Body, Category, Sentiment)                            |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                 1. RETRIEVAL ENGINE (RAG)                               |
| • Corpus: 30 Domain-Specific Support Tickets in data/historical_kb.json                 |
| • Algorithm: Hybrid TF-IDF Sublinear Vectorization + N-Gram Matching                    |
| • Output: Top-K Semantically Similar Tickets + Policies + Approved Resolutions          |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                 2. PROMPT GROUNDING & GUARDRAILS                        |
| • Injects Retrieved Historical Tickets & Company Policies                               |
| • Sets Persona: Empathetic, Concise, Resolution-Oriented Support Specialist             |
| • Enforces Guardrails: No false promises, no unauthorized disclosures, 2FA safety rules |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                 3. MULTI-PROVIDER GENERATIVE AI                         |
| • Primary Engine: Groq (openai/gpt-oss-120b / qwen/qwen3.8-27b) ~500 tokens/sec        |
| • Secondary Options: OpenAI (gpt-4o-mini / gpt-4o), Google Gemini                       |
| • Deterministic Fallback: Offline Mock Heuristic Client                                 |
| • Output: Suggested Customer Reply + Generation Telemetry                               |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                         4. MULTI-DIMENSIONAL ACCURACY EVALUATION                        |
|                                (The Core Challenge Engine)                              |
|                                                                                         |
|   ┌─────────────────────────────────┬────────────────────────────────────────────────┐  |
|   │ Metric Dimension                │ Evaluation Method & Objective                  │  |
|   ├─────────────────────────────────┼────────────────────────────────────────────────┤  |
|   │ 1. Intent Resolution (35%)      │ LLM Judge: Did it address customer's core goal?│  |
|   │ 2. Factual Correctness (30%)    │ LLM Judge: Policy adherence & hallucination ban│  |
|   │ 3. Semantic Cosine (15%)        │ N-Gram Embedding Cosine vs Ground Truth        │  |
|   │ 4. Tone & Empathy (10%)         │ LLM Judge: Sentiment de-escalation & brand voice│  |
|   │ 5. Completeness (10%)           │ LLM Judge: Actionable next steps & timelines   │  |
|   └─────────────────────────────────┴────────────────────────────────────────────────┘  |
|                                                                                         |
|   Output: Composite Score (0-100%), Quality Tier, Chain-of-Thought Rationale            |
+-----------------------------------------------------------------------------------------+
                                             |
                      +----------------------+----------------------+
                      |                                             |
                      v                                             v
+-------------------------------------------+ +-------------------------------------------+
|          5. STREAMLIT WEB DASHBOARD       | |               6. RICH CLI TOOL            |
| • Live interactive email testing          | | • python -m src.cli generate              |
| • RAG context explorer                    | | • python -m src.cli evaluate              |
| • Plotly polar radar charts of metrics    | | • python -m src.cli validate              |
| • System-wide benchmark analytics         | | • Automated JSON & MD benchmark reports   |
| • Human correlation scatter plot          | |                                           |
+-------------------------------------------+ +-------------------------------------------+
```

## 2. Directory Structure

```
.
├── data/
│   ├── historical_kb.json               # 30 Curated historical support tickets for RAG
│   ├── eval_benchmark.json              # 20 Diverse test cases (Standard, Edge, Adversarial)
│   └── human_validation_ground_truth.json # Human expert ratings for metric validation
├── src/
│   ├── __init__.py
│   ├── config.py                        # System configurations, thresholds, and weights
│   ├── data/
│   │   ├── __init__.py
│   │   ├── dataset_loader.py            # Pydantic schemas and dataset loaders
│   │   └── generator.py                 # Synthetic dataset generation script
│   ├── generator/
│   │   ├── __init__.py
│   │   ├── llm_client.py                # Multi-provider LLM adapter (Groq, OpenAI, Offline)
│   │   ├── retriever.py                 # Semantic RAG retriever with TF-IDF/Neural support
│   │   ├── prompts.py                   # Structured prompt templates (RAG, Few-Shot, Zero-Shot)
│   │   └── response_generator.py        # Core response generation orchestrator
│   ├── evaluator/
│   │   ├── __init__.py
│   │   ├── metrics.py                   # Semantic similarity, lexical overlap, and composite weights
│   │   ├── llm_judge.py                 # LLM-as-a-Judge with Chain-of-Thought rationale
│   │   ├── validation.py                # Human-metric statistical correlation runner
│   │   └── pipeline.py                  # Benchmark runner for system-wide reporting
│   ├── ui/
│   │   ├── __init__.py
│   │   └── app.py                       # Full-featured Streamlit Web Dashboard
│   └── cli.py                           # Rich CLI tool for generation and evaluation
├── tests/
│   ├── __init__.py
│   ├── run_all_tests.py                 # Direct standalone test runner
│   ├── test_dataset.py                  # Dataset schema & integrity tests
│   ├── test_retriever.py                # Semantic retriever tests
│   ├── test_generator.py                # Response generator unit tests
│   └── test_evaluator.py                # Accuracy metric & composite weighting tests
├── scripts/
│   ├── build_kb.py                      # Historical KB generator script
│   ├── build_eval_benchmark.py          # Benchmark test cases generator script
│   └── build_human_validation.py        # Human validation dataset generator script
├── requirements.txt                     # Pinned project dependencies
├── Dockerfile                           # Production container definition
├── .env.example                         # Environment variable template
├── .gitignore                           # Git ignore rules protecting keys and caches
├── EVALUATION_METHODOLOGY.md            # In-depth mathematical & QA evaluation rationale
└── README.md                            # Comprehensive project overview and documentation
```

## 3. Key Design Decisions

1. **Hybrid Vector Retrieval**: We utilize TF-IDF with sublinear term-frequency scaling and character/word n-gram matching as the primary retriever. This provides instant zero-latency vector search (< 5ms) and avoids multi-gigabyte cold-start model downloads, while preserving domain keyword fidelity (e.g. `AudienceRestriction`, `413 Payload Too Large`, `Okta SAML`).
2. **Provider Agnosticism**: The system abstracts LLM invocation behind a unified interface (`BaseLLMClient`). If an API key is absent, the system defaults to an offline heuristic generator so the codebase is 100% executable by reviewers out-of-the-box.
3. **Structured Judgments**: The LLM-as-a-judge outputs strict JSON adhering to a Pydantic schema, guaranteeing parseability and separating quantitative grades from qualitative Chain-of-Thought explanations.
