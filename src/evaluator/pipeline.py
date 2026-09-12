"""
Comprehensive Evaluation Pipeline for System-Level Benchmarking.
Evaluates response generator across the benchmark suite and produces aggregate reporting.
"""

import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from src.data.dataset_loader import load_eval_benchmark, EvaluationTestCase
from src.generator.response_generator import EmailResponseGenerator, GeneratedResponse
from src.evaluator.llm_judge import LLMJudge, EvaluationResult
from src.config import SUPPORT_CATEGORIES, QUALITY_THRESHOLDS


class SystemBenchmarkReport(BaseModel):
    """Overall system-wide benchmark metrics and evaluation summary."""
    total_evaluations: int
    overall_accuracy_score: float
    system_pass_rate: float
    avg_intent_score: float
    avg_factual_score: float
    avg_tone_score: float
    avg_completeness_score: float
    avg_semantic_similarity: float
    avg_latency_seconds: float
    generation_mode: str
    model_name: str
    quality_tier_counts: Dict[str, int]
    category_performance: Dict[str, Dict[str, Any]]
    individual_results: List[Dict[str, Any]]


class EvaluationPipeline:
    """Orchestrates end-to-end evaluation across the benchmark dataset."""

    def __init__(
        self,
        generator: Optional[EmailResponseGenerator] = None,
        judge: Optional[LLMJudge] = None
    ):
        self.generator = generator or EmailResponseGenerator()
        self.judge = judge or LLMJudge()

    def run_benchmark(
        self,
        test_cases: Optional[List[EvaluationTestCase]] = None,
        mode: str = "rag_grounded",
        limit: Optional[int] = None,
        category: Optional[str] = None,
        progress_callback: Optional[Any] = None
    ) -> SystemBenchmarkReport:
        """
        Run the complete evaluation suite and return aggregate reporting.
        """
        all_cases = test_cases or load_eval_benchmark()
        if category:
            all_cases = [c for c in all_cases if c.category == category]
        if limit:
            all_cases = all_cases[:limit]

        results = []
        tier_counts = {"EXCELLENT": 0, "GOOD": 0, "FAIR": 0, "POOR": 0}
        category_scores: Dict[str, List[float]] = {}
        total_latency = 0.0

        for i, test in enumerate(all_cases):
            if progress_callback:
                progress_callback(i + 1, len(all_cases), test.subject)

            # 1. Generate suggested response
            gen_res = self.generator.generate_response(
                subject=test.subject,
                customer_email=test.customer_email,
                mode=mode,
                category=test.category
            )
            total_latency += gen_res.latency_seconds

            # 2. Evaluate generated response
            eval_res = self.judge.evaluate(
                subject=test.subject,
                customer_email=test.customer_email,
                generated_reply=gen_res.suggested_reply,
                reference_reply=test.reference_reply,
                intent=test.intent,
                sentiment=test.customer_sentiment,
                expected_facts=test.expected_facts,
                prohibited_promises=test.prohibited_promises,
                test_id=test.id
            )

            # Accumulate metrics
            tier_counts[eval_res.quality_tier] = tier_counts.get(eval_res.quality_tier, 0) + 1
            if test.category not in category_scores:
                category_scores[test.category] = []
            category_scores[test.category].append(eval_res.composite_accuracy_score)

            results.append({
                "test_id": test.id,
                "category": test.category,
                "difficulty": test.difficulty,
                "subject": test.subject,
                "customer_sentiment": test.customer_sentiment,
                "customer_email": test.customer_email,
                "reference_reply": test.reference_reply,
                "generated_reply": gen_res.suggested_reply,
                "composite_accuracy_score": eval_res.composite_accuracy_score,
                "quality_tier": eval_res.quality_tier,
                "is_passed": eval_res.is_passed,
                "intent_score": eval_res.intent_score,
                "factual_score": eval_res.factual_score,
                "tone_score": eval_res.tone_score,
                "completeness_score": eval_res.completeness_score,
                "semantic_similarity": eval_res.semantic_similarity,
                "intent_rationale": eval_res.intent_rationale,
                "factual_rationale": eval_res.factual_rationale,
                "tone_rationale": eval_res.tone_rationale,
                "completeness_rationale": eval_res.completeness_rationale,
                "overall_summary": eval_res.overall_summary,
                "strengths": eval_res.identified_strengths,
                "defects": eval_res.identified_defects,
                "latency_seconds": gen_res.latency_seconds,
                "retrieved_tickets": gen_res.retrieved_tickets
            })

        n = len(results)
        if n == 0:
            raise ValueError("No test cases evaluated.")

        overall_score = round(sum(r["composite_accuracy_score"] for r in results) / n, 2)
        passed_count = sum(1 for r in results if r["is_passed"])
        pass_rate = round((passed_count / n) * 100.0, 1)

        avg_intent = round(sum(r["intent_score"] for r in results) / n, 2)
        avg_factual = round(sum(r["factual_score"] for r in results) / n, 2)
        avg_tone = round(sum(r["tone_score"] for r in results) / n, 2)
        avg_comp = round(sum(r["completeness_score"] for r in results) / n, 2)
        avg_sem = round(sum(r["semantic_similarity"] for r in results) / n, 3)
        avg_latency = round(total_latency / n, 2)

        # Compute Category performance
        cat_performance = {}
        for cat, scores in category_scores.items():
            cat_performance[cat] = {
                "count": len(scores),
                "avg_score": round(sum(scores) / len(scores), 2),
                "pass_rate": round((sum(1 for s in scores if s >= 70.0) / len(scores)) * 100.0, 1)
            }

        return SystemBenchmarkReport(
            total_evaluations=n,
            overall_accuracy_score=overall_score,
            system_pass_rate=pass_rate,
            avg_intent_score=avg_intent,
            avg_factual_score=avg_factual,
            avg_tone_score=avg_tone,
            avg_completeness_score=avg_comp,
            avg_semantic_similarity=avg_sem,
            avg_latency_seconds=avg_latency,
            generation_mode=mode,
            model_name=self.generator.llm_client.model if hasattr(self.generator.llm_client, "model") else "standard",
            quality_tier_counts=tier_counts,
            category_performance=cat_performance,
            individual_results=results
        )
