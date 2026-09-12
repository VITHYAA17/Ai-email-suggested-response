"""
System Configuration and Constants for AI Email Suggested-Response & Evaluation System.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HISTORICAL_KB_PATH = DATA_DIR / "historical_kb.json"
EVAL_BENCHMARK_PATH = DATA_DIR / "eval_benchmark.json"
HUMAN_VALIDATION_PATH = DATA_DIR / "human_validation_ground_truth.json"

# LLM Providers Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

DEFAULT_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "groq").lower()

# Vector Retrieval & Embedding Configuration
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "3"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))

# Multi-Dimensional Evaluation Weights
METRIC_WEIGHTS = {
    "intent_resolution": 0.35,
    "factual_correctness": 0.30,
    "semantic_similarity": 0.15,
    "tone_empathy": 0.10,
    "completeness_actionability": 0.10,
}

# Quality Rating Bands
QUALITY_THRESHOLDS = {
    "EXCELLENT": 85.0,
    "GOOD": 70.0,
    "FAIR": 50.0,
    "POOR": 0.0,
}

# Domain Categories
SUPPORT_CATEGORIES = [
    "billing_and_invoicing",
    "technical_bugs",
    "account_access",
    "feature_requests",
    "sla_escalations",
    "product_how_to",
]
