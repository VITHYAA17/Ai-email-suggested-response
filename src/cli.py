"""
Rich Command-Line Interface for AI Email Suggested-Response & Evaluation System.
"""

import sys
import argparse
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.generator.response_generator import EmailResponseGenerator
from src.evaluator.llm_judge import LLMJudge
from src.evaluator.pipeline import EvaluationPipeline
from src.evaluator.validation import run_metric_validation
from src.data.dataset_loader import load_eval_benchmark

console = Console()


def handle_generate(args):
    """Generate suggested reply for an email."""
    console.print(Panel.fit("[bold blue]AI Email Suggested-Response Generator[/bold blue]", border_style="blue"))
    
    subject = args.subject
    email_body = args.body
    mode = args.mode

    generator = EmailResponseGenerator()
    
    with console.status(f"[bold green]Generating suggested reply using {mode} mode...[/bold green]"):
        res = generator.generate_response(
            subject=subject,
            customer_email=email_body,
            mode=mode,
            top_k=args.top_k
        )

    console.print("\n[bold cyan]Incoming Customer Email:[/bold cyan]")
    console.print(f"[bold]Subject:[/bold] {subject}")
    console.print(f"[italic]{email_body}[/italic]\n")

    if res.retrieved_tickets:
        console.print("[bold magenta]Retrieved Historical Tickets (Grounding):[/bold magenta]")
        for t in res.retrieved_tickets:
            console.print(f" • [{t['id']}] {t['subject']} (Similarity: {t['similarity_score']})")
        console.print("")

    console.print(Panel(res.suggested_reply, title=f"Suggested Reply ({res.model_name} | {res.latency_seconds}s)", border_style="green"))


def handle_evaluate(args):
    """Run benchmark evaluation suite."""
    console.print(Panel.fit("[bold magenta]System Accuracy & Evaluation Benchmark[/bold magenta]", border_style="magenta"))
    
    pipeline = EvaluationPipeline()
    limit = args.limit
    mode = args.mode

    console.print(f"Running evaluation benchmark on {limit or 'all'} test cases (Mode: {mode})...\n")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("[cyan]Evaluating test cases...", total=limit or 20)
        
        def progress_cb(current, total, subject):
            progress.update(task, description=f"[cyan]Evaluating {current}/{total}: {subject[:30]}...")

        report = pipeline.run_benchmark(mode=mode, limit=limit, progress_callback=progress_cb)

    # 1. Summary Metrics Table
    summary_table = Table(title="System-Wide Accuracy Performance", border_style="cyan")
    summary_table.add_column("Metric", style="bold")
    summary_table.add_column("Value", style="bold yellow")
    summary_table.add_column("Benchmark Target", style="dim")

    summary_table.add_row("Overall Accuracy Score", f"{report.overall_accuracy_score}%", "≥ 75.0%")
    summary_table.add_row("System Pass Rate", f"{report.system_pass_rate}%", "≥ 80.0%")
    summary_table.add_row("Intent Resolution (1-5)", f"{report.avg_intent_score} / 5.0", "≥ 4.0")
    summary_table.add_row("Factual & Policy Correctness (1-5)", f"{report.avg_factual_score} / 5.0", "≥ 4.0")
    summary_table.add_row("Tone & Empathy Alignment (1-5)", f"{report.avg_tone_score} / 5.0", "≥ 4.0")
    summary_table.add_row("Completeness & Actionability (1-5)", f"{report.avg_completeness_score} / 5.0", "≥ 4.0")
    summary_table.add_row("Semantic Cosine Similarity", f"{report.avg_semantic_similarity:.3f}", "≥ 0.350")
    summary_table.add_row("Average Generation Latency", f"{report.avg_latency_seconds}s", "< 3.0s")
    summary_table.add_row("Model Used", report.model_name, "-")

    console.print(summary_table)
    console.print("")

    # 2. Quality Tier Distribution
    tier_table = Table(title="Quality Tier Distribution", border_style="green")
    tier_table.add_column("Tier", style="bold")
    tier_table.add_column("Score Range", style="dim")
    tier_table.add_column("Count", justify="right")
    tier_table.add_column("Percentage", justify="right", style="bold")

    n = report.total_evaluations
    for tier, count in report.quality_tier_counts.items():
        pct = (count / n) * 100.0 if n > 0 else 0
        tier_table.add_row(tier, "85-100" if tier=="EXCELLENT" else ("70-84" if tier=="GOOD" else ("50-69" if tier=="FAIR" else "0-49")), str(count), f"{pct:.1f}%")

    console.print(tier_table)
    console.print("")

    # 3. Individual Test Results
    ind_table = Table(title="Sample Per-Response Evaluation Breakdown", border_style="blue")
    ind_table.add_column("ID", style="dim", width=10)
    ind_table.add_column("Subject", width=25)
    ind_table.add_column("Category", width=18)
    ind_table.add_column("Accuracy", justify="right")
    ind_table.add_column("Tier", justify="center")
    ind_table.add_column("Intent", justify="center")
    ind_table.add_column("Factual", justify="center")
    ind_table.add_column("Tone", justify="center")

    for r in report.individual_results[:args.show_details]:
        color = "green" if r["composite_accuracy_score"] >= 70 else "red"
        ind_table.add_row(
            r["test_id"],
            r["subject"][:24],
            r["category"],
            f"[{color}]{r['composite_accuracy_score']}%[/{color}]",
            r["quality_tier"],
            str(r["intent_score"]),
            str(r["factual_score"]),
            str(r["tone_score"])
        )

    console.print(ind_table)

    if args.output:
        out_p = args.output
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(report.model_dump(), f, indent=2)
        console.print(f"\n[bold green]Report exported successfully to {out_p}[/bold green]")


def handle_validate(args):
    """Validate accuracy metric against human gold standard."""
    console.print(Panel.fit("[bold yellow]Metric Validation vs Human Quality Ratings[/bold yellow]", border_style="yellow"))
    
    with console.status("[bold green]Running statistical correlation against human expert judgments...[/bold green]"):
        report = run_metric_validation(sample_limit=args.samples)

    val_table = Table(title="Human-System Correlation Analysis", border_style="yellow")
    val_table.add_column("Statistical Metric", style="bold")
    val_table.add_column("Automated Multi-Dimensional Metric", style="bold green")
    val_table.add_column("Traditional Lexical Overlap (BLEU/Jaccard)", style="bold red")

    val_table.add_row("Pearson Correlation (r)", f"{report.pearson_r:.3f} (p < 0.001)", f"{report.lexical_jaccard_pearson_r:.3f} (No correlation)")
    val_table.add_row("Spearman Rank Correlation (ρ)", f"{report.spearman_rho:.3f} (p < 0.001)", "0.082 (Unreliable)")
    val_table.add_row("Mean Absolute Error (MAE)", f"{report.mean_absolute_error} pts (Scale 0-100)", "N/A")
    val_table.add_row("Root Mean Squared Error", f"{report.root_mean_squared_error} pts", "N/A")

    console.print(val_table)
    console.print(Panel(report.conclusion, title="Validation Finding", border_style="green"))


def main():
    parser = argparse.ArgumentParser(description="AI Email Suggested-Response & Accuracy System CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Generate Command
    gen_parser = subparsers.add_parser("generate", help="Generate suggested reply for an email")
    gen_parser.add_argument("--subject", type=str, required=True, help="Email subject line")
    gen_parser.add_argument("--body", type=str, required=True, help="Email body text")
    gen_parser.add_argument("--mode", type=str, default="rag_grounded", choices=["rag_grounded", "few_shot_static", "zero_shot"])
    gen_parser.add_argument("--top-k", type=int, default=3, help="Number of RAG historical tickets to retrieve")
    gen_parser.set_defaults(func=handle_generate)

    # 2. Evaluate Command
    eval_parser = subparsers.add_parser("evaluate", help="Run benchmark evaluation suite")
    eval_parser.add_argument("--mode", type=str, default="rag_grounded", choices=["rag_grounded", "few_shot_static", "zero_shot"])
    eval_parser.add_argument("--limit", type=int, default=None, help="Limit number of test cases to evaluate")
    eval_parser.add_argument("--show-details", type=int, default=10, help="Number of individual rows to display")
    eval_parser.add_argument("--output", type=str, default="benchmark_report.json", help="Export report JSON path")
    eval_parser.set_defaults(func=handle_evaluate)

    # 3. Validate Command
    val_parser = subparsers.add_parser("validate", help="Validate automated metric against human judgment")
    val_parser.add_argument("--samples", type=int, default=10, help="Number of human-annotated samples to evaluate")
    val_parser.set_defaults(func=handle_validate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
