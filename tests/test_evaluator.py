"""
Unit tests for accuracy metrics, composite scoring, and quality tier classification.
"""

import pytest
from src.evaluator.metrics import (
    compute_semantic_similarity,
    compute_lexical_token_overlap,
    calculate_composite_score,
    get_quality_tier
)


def test_semantic_similarity_identical():
    """Identical text should yield maximum semantic similarity."""
    text = "We have processed a full refund of $150 back to your credit card."
    score = compute_semantic_similarity(text, text)
    assert score >= 0.95


def test_semantic_similarity_orthogonal():
    """Completely unrelated text should yield low similarity."""
    text1 = "How do I configure SAML Okta SSO login?"
    text2 = "Apples and oranges are grown on agricultural farms."
    score = compute_semantic_similarity(text1, text2)
    assert score < 0.2


def test_calculate_composite_score():
    """Verify composite weighting formula."""
    # Flawless response (all 5.0)
    top_score = calculate_composite_score(
        intent_score=5.0,
        factual_score=5.0,
        semantic_score=1.0,
        tone_score=5.0,
        completeness_score=5.0
    )
    assert top_score == 100.0

    # Minimum response (all 1.0)
    low_score = calculate_composite_score(
        intent_score=1.0,
        factual_score=1.0,
        semantic_score=0.0,
        tone_score=1.0,
        completeness_score=1.0
    )
    assert low_score == 0.0


def test_quality_tiers():
    """Verify threshold band classifications."""
    assert get_quality_tier(90.0) == "EXCELLENT"
    assert get_quality_tier(75.0) == "GOOD"
    assert get_quality_tier(55.0) == "FAIR"
    assert get_quality_tier(30.0) == "POOR"
