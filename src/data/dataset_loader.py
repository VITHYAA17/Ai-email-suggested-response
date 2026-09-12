"""
Dataset schemas and loaders for email tickets, knowledge base, and evaluation benchmark.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from src.config import HISTORICAL_KB_PATH, EVAL_BENCHMARK_PATH, HUMAN_VALIDATION_PATH


class EmailTicket(BaseModel):
    """Schema representing an email conversation pair with metadata."""
    id: str = Field(..., description="Unique ticket identifier")
    category: str = Field(..., description="Support category")
    subject: str = Field(..., description="Email subject line")
    customer_email: str = Field(..., description="Incoming customer email body")
    customer_sentiment: str = Field(default="neutral", description="Customer emotional state")
    intent: str = Field(..., description="Primary customer intent or request")
    ground_truth_reply: str = Field(..., description="Canonical agent response")
    key_facts: List[str] = Field(default_factory=list, description="Factual requirements")
    prohibited_actions: List[str] = Field(default_factory=list, description="Forbidden commitments")
    policy_applied: Optional[str] = Field(default=None, description="Governing policy reference")


class EvaluationTestCase(BaseModel):
    """Schema for test benchmark items used during accuracy evaluation."""
    id: str
    category: str
    subject: str
    customer_email: str
    customer_sentiment: str
    intent: str
    reference_reply: str = Field(..., alias="reference_reply")
    expected_facts: List[str]
    prohibited_promises: List[str] = Field(default_factory=list)
    difficulty: str = Field(default="standard", description="standard, edge_case, adversarial")

    def __init__(self, **data):
        # Support ground_truth_reply as alias for reference_reply
        if "reference_reply" not in data and "ground_truth_reply" in data:
            data["reference_reply"] = data["ground_truth_reply"]
        super().__init__(**data)


class HumanAnnotation(BaseModel):
    """Human-scored response for validating the automated accuracy metric."""
    test_id: str
    system_response: str
    human_intent_score: float
    human_factual_score: float
    human_tone_score: float
    human_completeness_score: float
    human_overall_score: float
    annotator_notes: str


def load_historical_kb(path: Optional[Path] = None) -> List[EmailTicket]:
    """Load the historical knowledge base for RAG vector retrieval."""
    file_path = path or HISTORICAL_KB_PATH
    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge base file not found at: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [EmailTicket(**item) for item in data]


def load_eval_benchmark(path: Optional[Path] = None) -> List[EvaluationTestCase]:
    """Load the evaluation benchmark dataset."""
    file_path = path or EVAL_BENCHMARK_PATH
    if not file_path.exists():
        raise FileNotFoundError(f"Evaluation benchmark file not found at: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [EvaluationTestCase(**item) for item in data]


def load_human_validation_data(path: Optional[Path] = None) -> List[HumanAnnotation]:
    """Load human-annotated ratings for metric correlation analysis."""
    file_path = path or HUMAN_VALIDATION_PATH
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [HumanAnnotation(**item) for item in data]
