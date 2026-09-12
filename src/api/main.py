"""
FastAPI REST Service for AI Email Suggested-Response & Accuracy Evaluation.
Provides production-ready REST API endpoints with OpenAPI / Swagger documentation.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from src.generator.response_generator import EmailResponseGenerator
from src.evaluator.llm_judge import LLMJudge
from src.evaluator.pipeline import EvaluationPipeline
from src.evaluator.validation import run_metric_validation
from src.data.dataset_loader import load_historical_kb, load_eval_benchmark

app = FastAPI(
    title="AI Email Suggested-Response & Evaluation API",
    description="Production REST API for generating grounded email suggestions and evaluating quality.",
    version="1.0.0"
)

# Global instances
generator = EmailResponseGenerator()
judge = LLMJudge()
pipeline = EvaluationPipeline(generator=generator, judge=judge)


class SuggestRequest(BaseModel):
    subject: str = Field(..., example="Cannot log in with Okta SSO")
    customer_email: str = Field(..., example="Our team gets AudienceRestriction mismatch")
    category: Optional[str] = Field(default=None, example="account_access")
    mode: str = Field(default="rag_grounded", description="rag_grounded, few_shot_static, or zero_shot")
    top_k: int = Field(default=3, ge=1, le=5)


class EvaluateRequest(BaseModel):
    subject: str = Field(..., example="Charged twice for renewal")
    customer_email: str = Field(..., example="I was charged $150 twice today. Please refund.")
    generated_reply: str = Field(..., example="Hi there, I have refunded the duplicate charge of $150 to your card.")
    reference_reply: Optional[str] = Field(default=None)
    intent: Optional[str] = Field(default="Customer Inquiry")
    sentiment: Optional[str] = Field(default="neutral")
    expected_facts: Optional[List[str]] = Field(default_factory=list)
    prohibited_promises: Optional[List[str]] = Field(default_factory=list)


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint confirming API status and model readiness."""
    return {
        "status": "healthy",
        "service": "AI Email Suggested-Response System",
        "active_model": generator.llm_client.model if hasattr(generator.llm_client, "model") else "standard"
    }


@app.post("/v1/suggest", tags=["Generation"])
def suggest_response(req: SuggestRequest):
    """Generate a suggested customer support reply grounded in historical data."""
    try:
        res = generator.generate_response(
            subject=req.subject,
            customer_email=req.customer_email,
            mode=req.mode,
            category=req.category,
            top_k=req.top_k
        )
        return res.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/evaluate", tags=["Evaluation"])
def evaluate_response(req: EvaluateRequest):
    """Evaluate a generated reply using the multi-dimensional LLM-as-a-judge rubric."""
    try:
        ref = req.reference_reply or req.generated_reply
        res = judge.evaluate(
            subject=req.subject,
            customer_email=req.customer_email,
            generated_reply=req.generated_reply,
            reference_reply=ref,
            intent=req.intent or "Customer Inquiry",
            sentiment=req.sentiment or "neutral",
            expected_facts=req.expected_facts,
            prohibited_promises=req.prohibited_promises
        )
        return res.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/benchmark", tags=["Evaluation"])
def run_benchmark(
    limit: int = Query(default=5, ge=1, le=20),
    mode: str = Query(default="rag_grounded")
):
    """Run benchmark evaluation suite across held-out test cases."""
    try:
        report = pipeline.run_benchmark(limit=limit, mode=mode)
        return report.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/validate", tags=["Validation"])
def validate_metrics(samples: int = Query(default=5, ge=2, le=10)):
    """Run statistical correlation proof comparing automated metrics against human ratings."""
    try:
        report = run_metric_validation(sample_limit=samples)
        return report.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
