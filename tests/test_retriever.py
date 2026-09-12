"""
Unit tests for RAG Semantic Retrieval.
"""

import pytest
from src.generator.retriever import TicketRetriever


def test_retriever_query_matching():
    """Verify semantic retriever returns relevant tickets for domain queries."""
    retriever = TicketRetriever()
    
    # Query for Okta SSO
    matches = retriever.retrieve(
        query_subject="Okta SAML error",
        query_email="AudienceRestriction mismatch error when logging in",
        top_k=2
    )
    assert len(matches) > 0
    top_ticket, score = matches[0]
    assert "okta" in top_ticket.subject.lower() or "sso" in top_ticket.subject.lower() or "saml" in top_ticket.subject.lower()
    assert score > 0.15


def test_retriever_refund_matching():
    """Verify retriever identifies billing refund tickets."""
    retriever = TicketRetriever()
    matches = retriever.retrieve(
        query_subject="Charged twice for annual renewal",
        query_email="I need a refund for the duplicate payment",
        top_k=2
    )
    assert len(matches) > 0
    top_ticket, _ = matches[0]
    assert top_ticket.category == "billing_and_invoicing"


def test_format_retrieved_context():
    """Verify formatting generates structured markdown prompt context."""
    retriever = TicketRetriever()
    matches = retriever.retrieve("email attachment error", "413 Payload Too Large", top_k=2)
    formatted = retriever.format_retrieved_context(matches)
    assert "Historical Ticket 1" in formatted
    assert "Approved Resolution" in formatted
