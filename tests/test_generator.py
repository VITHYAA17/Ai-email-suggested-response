"""
Unit tests for Suggested-Response Generator.
"""

import pytest
from src.generator.response_generator import EmailResponseGenerator
from src.generator.llm_client import OfflineMockClient


def test_offline_generator_rag_mode():
    """Verify generator produces valid suggested responses in RAG mode."""
    mock_client = OfflineMockClient()
    generator = EmailResponseGenerator(llm_client=mock_client)
    
    res = generator.generate_response(
        subject="How to set up round robin",
        customer_email="We want to evenly distribute emails across our 4 agents",
        mode="rag_grounded"
    )
    
    assert res.suggested_reply is not None
    assert len(res.suggested_reply) > 20
    assert res.mode == "rag_grounded"
    assert len(res.retrieved_tickets) > 0
    assert res.latency_seconds >= 0.0


def test_generator_zero_shot_mode():
    """Verify generator functions in zero-shot baseline mode."""
    mock_client = OfflineMockClient()
    generator = EmailResponseGenerator(llm_client=mock_client)
    
    res = generator.generate_response(
        subject="Billing issue",
        customer_email="My card was declined",
        mode="zero_shot"
    )
    
    assert res.suggested_reply is not None
    assert res.mode == "zero_shot"
    assert len(res.retrieved_tickets) == 0
