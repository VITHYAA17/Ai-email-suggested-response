"""
Mathematical and lexical metrics for email response quality evaluation.
Computes Semantic Embedding Cosine Similarity, Lexical Overlap, and Composite Weighting.
"""

from typing import Dict, Any, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import METRIC_WEIGHTS, QUALITY_THRESHOLDS


def compute_semantic_similarity(candidate_text: str, reference_text: str) -> float:
    """
    Computes semantic similarity between generated reply and ground truth.
    Uses TF-IDF character and word n-grams for fast, robust cosine similarity.
    """
    if not candidate_text.strip() or not reference_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        analyzer="word",
        stop_words="english",
        sublinear_tf=True
    )
    try:
        matrix = vectorizer.fit_transform([candidate_text, reference_text])
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        return max(0.0, min(1.0, score))
    except Exception:
        return 0.5


def compute_lexical_token_overlap(candidate_text: str, reference_text: str) -> float:
    """
    Compute basic Jaccard word token overlap (used to demonstrate why exact overlap is inadequate).
    """
    cand_tokens = set(candidate_text.lower().split())
    ref_tokens = set(reference_text.lower().split())
    if not cand_tokens or not ref_tokens:
        return 0.0
    intersection = cand_tokens.intersection(ref_tokens)
    union = cand_tokens.union(ref_tokens)
    return len(intersection) / len(union)


def calculate_composite_score(
    intent_score: float,          # 1.0 - 5.0
    factual_score: float,         # 1.0 - 5.0
    semantic_score: float,        # 0.0 - 1.0
    tone_score: float,            # 1.0 - 5.0
    completeness_score: float     # 1.0 - 5.0
) -> float:
    """
    Calculate normalized 0-100 composite accuracy score based on weighted rubric.
    """
    # Normalize 1-5 scales to 0.0 - 1.0
    norm_intent = max(0.0, (intent_score - 1.0) / 4.0)
    norm_factual = max(0.0, (factual_score - 1.0) / 4.0)
    norm_semantic = max(0.0, min(1.0, semantic_score))
    norm_tone = max(0.0, (tone_score - 1.0) / 4.0)
    norm_comp = max(0.0, (completeness_score - 1.0) / 4.0)

    composite = (
        norm_intent * METRIC_WEIGHTS["intent_resolution"] +
        norm_factual * METRIC_WEIGHTS["factual_correctness"] +
        norm_semantic * METRIC_WEIGHTS["semantic_similarity"] +
        norm_tone * METRIC_WEIGHTS["tone_empathy"] +
        norm_comp * METRIC_WEIGHTS["completeness_actionability"]
    ) * 100.0

    return round(float(composite), 2)


def get_quality_tier(score: float) -> str:
    """Classify overall accuracy score into human-readable quality bands."""
    if score >= QUALITY_THRESHOLDS["EXCELLENT"]:
        return "EXCELLENT"
    elif score >= QUALITY_THRESHOLDS["GOOD"]:
        return "GOOD"
    elif score >= QUALITY_THRESHOLDS["FAIR"]:
        return "FAIR"
    else:
        return "POOR"
