"""
Core Suggested-Response Generator integrating RAG Retrieval and Multi-Provider LLMs.
"""

import time
from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field

from src.generator.retriever import TicketRetriever
from src.generator.llm_client import get_llm_client, BaseLLMClient
from src.generator.prompts import (
    SYSTEM_PROMPT_SUPPORT_AGENT,
    RAG_PROMPT_TEMPLATE,
    STATIC_FEW_SHOT_TEMPLATE,
    ZERO_SHOT_TEMPLATE
)
from src.data.dataset_loader import EmailTicket


class GeneratedResponse(BaseModel):
    """Container for suggested reply and generation telemetry."""
    suggested_reply: str
    mode: str = Field(..., description="rag_grounded, few_shot_static, or zero_shot")
    model_name: str
    provider: str
    latency_seconds: float
    retrieved_tickets: List[Dict[str, Any]] = Field(default_factory=list)
    retrieved_context_str: Optional[str] = None


class EmailResponseGenerator:
    """Generates suggested email replies grounded in historical support data."""

    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        retriever: Optional[TicketRetriever] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.llm_client = llm_client or get_llm_client(provider=provider, model=model)
        self.retriever = retriever or TicketRetriever()

    def generate_response(
        self,
        subject: str,
        customer_email: str,
        mode: str = "rag_grounded",
        category: Optional[str] = None,
        top_k: int = 3,
        temperature: float = 0.2
    ) -> GeneratedResponse:
        """
        Generate a suggested reply for an incoming email.
        
        Args:
            subject: The incoming email subject
            customer_email: The incoming email body
            mode: 'rag_grounded', 'few_shot_static', or 'zero_shot'
            category: Optional category hint for retrieval prioritization
            top_k: Number of historical tickets to retrieve for RAG
            temperature: LLM sampling temperature
        """
        start_time = time.time()
        retrieved_tickets_data = []
        retrieved_context_str = ""

        if mode == "rag_grounded":
            # 1. Semantic Retrieval over Historical Knowledge Base
            retrieved = self.retriever.retrieve(
                query_subject=subject,
                query_email=customer_email,
                top_k=top_k,
                category=category
            )
            retrieved_context_str = self.retriever.format_retrieved_context(retrieved)
            for t, score in retrieved:
                retrieved_tickets_data.append({
                    "id": t.id,
                    "subject": t.subject,
                    "category": t.category,
                    "similarity_score": round(score, 3),
                    "policy_applied": t.policy_applied
                })

            optional_meta = f"Category Hint: {category}" if category else ""
            user_prompt = RAG_PROMPT_TEMPLATE.format(
                retrieved_context=retrieved_context_str,
                subject=subject,
                customer_email=customer_email,
                optional_metadata=optional_meta
            )

        elif mode == "few_shot_static":
            user_prompt = STATIC_FEW_SHOT_TEMPLATE.format(
                subject=subject,
                customer_email=customer_email
            )

        elif mode == "zero_shot":
            user_prompt = ZERO_SHOT_TEMPLATE.format(
                subject=subject,
                customer_email=customer_email
            )

        else:
            raise ValueError(f"Unknown generation mode: {mode}. Must be 'rag_grounded', 'few_shot_static', or 'zero_shot'.")

        # 2. Invoke LLM
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_SUPPORT_AGENT},
            {"role": "user", "content": user_prompt}
        ]

        llm_res = self.llm_client.generate(messages=messages, temperature=temperature)
        total_latency = time.time() - start_time

        return GeneratedResponse(
            suggested_reply=llm_res.content,
            mode=mode,
            model_name=llm_res.model,
            provider=llm_res.provider,
            latency_seconds=round(total_latency, 3),
            retrieved_tickets=retrieved_tickets_data,
            retrieved_context_str=retrieved_context_str if mode == "rag_grounded" else None
        )
