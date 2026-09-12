"""
Unit tests for dataset loading, integrity, and schema adherence.
"""

import pytest
from src.data.dataset_loader import load_historical_kb, load_eval_benchmark, load_human_validation_data
from src.config import SUPPORT_CATEGORIES


def test_historical_kb_integrity():
    """Verify historical KB loads with valid schemas and category representation."""
    tickets = load_historical_kb()
    assert len(tickets) >= 20, f"Expected at least 20 historical tickets, found {len(tickets)}"
    
    categories_found = set()
    for t in tickets:
        assert t.id.startswith("KB-"), f"Invalid ID format: {t.id}"
        assert len(t.subject.strip()) > 5, "Subject too short"
        assert len(t.customer_email.strip()) > 10, "Email body too short"
        assert len(t.ground_truth_reply.strip()) > 20, "Reply too short"
        assert len(t.intent.strip()) > 5, "Intent too short"
        assert len(t.key_facts) >= 1, "Must contain at least one key fact"
        categories_found.add(t.category)
        
    for cat in SUPPORT_CATEGORIES:
        assert cat in categories_found, f"Category '{cat}' missing from historical KB"


def test_eval_benchmark_integrity():
    """Verify evaluation benchmark dataset has valid schemas and difficulty spread."""
    cases = load_eval_benchmark()
    assert len(cases) >= 15, f"Expected at least 15 evaluation cases, found {len(cases)}"
    
    difficulties = set()
    for c in cases:
        assert c.id.startswith("EVAL-"), f"Invalid eval ID format: {c.id}"
        assert len(c.reference_reply.strip()) > 20, "Reference reply missing or too short"
        assert len(c.expected_facts) >= 1, "Must define expected facts"
        difficulties.add(c.difficulty)
        
    assert "standard" in difficulties
    assert "edge_case" in difficulties or "adversarial" in difficulties


def test_human_validation_data_integrity():
    """Verify human validation dataset is populated with calibrated ratings."""
    annotations = load_human_validation_data()
    assert len(annotations) >= 5, "Expected at least 5 human validation annotations"
    for a in annotations:
        assert 1.0 <= a.human_intent_score <= 5.0
        assert 1.0 <= a.human_factual_score <= 5.0
        assert 0.0 <= a.human_overall_score <= 100.0
