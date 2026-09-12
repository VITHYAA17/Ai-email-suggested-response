"""
Semantic and Hybrid RAG Retriever for historical customer support tickets.
Provides instantaneous, zero-latency vector retrieval using TF-IDF + Cosine Similarity,
with optional neural sentence embeddings.
"""

import os
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data.dataset_loader import EmailTicket, load_historical_kb
from src.config import TOP_K_RETRIEVAL, SIMILARITY_THRESHOLD


class TicketRetriever:
    """Retrieves semantically relevant historical email pairs for in-context grounding."""

    def __init__(self, kb_tickets: Optional[List[EmailTicket]] = None, use_neural: bool = False):
        self.tickets = kb_tickets if kb_tickets is not None else load_historical_kb()
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        
        # Build document corpus from subject + customer email + intent
        self.corpus = [
            f"{t.subject} {t.customer_email} {t.intent} {t.category}"
            for t in self.tickets
        ]
        
        # Fit vectorizer
        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        else:
            self.tfidf_matrix = None
            
        self.st_model = None
        self._embedding_matrix = None
        if use_neural or os.getenv("USE_NEURAL_EMBEDDINGS", "false").lower() == "true":
            self._init_sentence_transformer()

    def _init_sentence_transformer(self):
        """Optionally load sentence transformer for dense neural search."""
        try:
            from sentence_transformers import SentenceTransformer
            self.st_model = SentenceTransformer("all-MiniLM-L6-v2")
            self._embedding_matrix = self.st_model.encode(
                self.corpus, convert_to_numpy=True, normalize_embeddings=True
            )
        except Exception:
            self.st_model = None
            self._embedding_matrix = None

    def retrieve(
        self,
        query_subject: str,
        query_email: str,
        top_k: int = TOP_K_RETRIEVAL,
        category: Optional[str] = None
    ) -> List[Tuple[EmailTicket, float]]:
        """
        Retrieve top-k most similar historical tickets with similarity scores.
        """
        if not self.tickets or self.tfidf_matrix is None:
            return []

        query_text = f"{query_subject} {query_email}"
        
        # If neural embeddings are active, perform dense semantic similarity
        if self.st_model is not None and self._embedding_matrix is not None:
            query_emb = self.st_model.encode([query_text], convert_to_numpy=True, normalize_embeddings=True)
            scores = np.dot(self._embedding_matrix, query_emb.T).flatten()
        else:
            # High-speed TF-IDF cosine similarity
            query_vec = self.vectorizer.transform([query_text])
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        ranked_indices = np.argsort(scores)[::-1]
        
        results = []
        for idx in ranked_indices:
            score = float(scores[idx])
            ticket = self.tickets[idx]
            
            # Boost matching category
            if category and ticket.category == category:
                score = min(1.0, score * 1.15)
                
            results.append((ticket, score))
            if len(results) >= top_k:
                break
                
        return results

    def format_retrieved_context(self, retrieved: List[Tuple[EmailTicket, float]]) -> str:
        """Format retrieved tickets into a clean context block for LLM prompts."""
        if not retrieved:
            return "No historical reference tickets available."

        context_blocks = []
        for i, (ticket, score) in enumerate(retrieved, start=1):
            block = (
                f"### [Historical Ticket {i}] (Similarity: {score:.2f}) [Category: {ticket.category}]\n"
                f"- Subject: {ticket.subject}\n"
                f"- Customer Inquiry: {ticket.customer_email}\n"
                f"- Customer Intent: {ticket.intent}\n"
                f"- Policy Applied: {ticket.policy_applied or 'Standard Support Policy'}\n"
                f"- Required Factual Elements: {', '.join(ticket.key_facts)}\n"
                f"- Prohibited Actions: {', '.join(ticket.prohibited_actions)}\n"
                f"- Approved Resolution:\n{ticket.ground_truth_reply}\n"
            )
            context_blocks.append(block)

        return "\n".join(context_blocks)
