"""Career Bot – CLI entry point.

Usage
-----
    # 1. Ingest your personal documents into the vector store
    python main.py ingest

    # 2. Build a resume
    python main.py build-resume

    # 3. Tailor a resume to a job posting
    python main.py tailor --resume output/resume.md --job-file job.txt

    # 4. Start an interactive interview coaching session
    python main.py interview
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

app = typer.Typer(
    name="career-bot",
    help="AI-powered career coaching agent for Android engineers.",
    add_completion=False,
)
console = Console()


# ── Helpers ───────────────────────────────────────────────────────────────────


def _check_config() -> None:
    """Validate settings before making any API calls."""
    from career_bot.config import settings

    try:
        settings.validate()
    except ValueError as exc:
        console.print(f"[bold red]Configuration error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc


def _save_output(content: str, filename: str) -> Path:
    """Write *content* to ``output/<filename>`` and return the path."""
    from career_bot.config import settings

    settings.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = settings.output_dir / filename
    out_path.write_text(content, encoding="utf-8")
    return out_path


# ── Commands ──────────────────────────────────────────────────────────────────


@app.command()
def ingest(
    docs_dir: Path = typer.Option(
        None,
        "--docs-dir",
        "-d",
        help="Directory containing your personal career documents.",
    ),
) -> None:
    """Load personal career documents into the vector store.

    Supported formats: PDF, DOCX, TXT, MD.
    Place your files in the ``docs/`` directory (or specify a custom path).
    Only new or changed files are embedded; existing unchanged files are skipped.
    """
    _check_config()
    from career_bot.tools.document_processor import build_vector_store, load_documents
    from career_bot.config import settings

    target = docs_dir or settings.docs_dir

    console.print(f"[bold]Scanning documents in:[/bold] {target.resolve()}")

    raw_docs = load_documents(target)
    if not raw_docs:
        console.print(
            "[yellow]No supported documents found. "
            "Add .pdf, .docx, or .txt files to the docs/ directory.[/yellow]"
        )
        raise typer.Exit()

    console.print(f"Found [bold]{len(raw_docs)}[/bold] document pages. Ingesting…")

    with console.status("Building vector store…"):
        build_vector_store(docs_dir=target)

    console.print("[bold green]✓ Documents ingested successfully.[/bold green]")


@app.command(name="build-resume")
def build_resume(
    instructions: str = typer.Option(
        "",
        "--instructions",
        "-i",
        help="Extra guidance for the resume writer (e.g. 'target a senior role').",
    ),
    output: str = typer.Option(
        "resume.md",
        "--output",
        "-o",
        help="Output filename inside the output/ directory.",
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--no-interactive",
        help="Enter a refinement loop after the initial draft is generated.",
    ),
) -> None:
    """Build a professional resume from your ingested career documents.

    The agent reads your skills, accomplishments, and experience from the vector
    store and produces an ATS-friendly markdown resume.
    """
    _check_config()
    from career_bot.agents.resume_builder import ResumeBuilderAgent

    agent = ResumeBuilderAgent()

    console.print(Panel("[bold]Resume Builder[/bold] 📄", expand=False))

    with console.status("Generating resume…"):
        resume = agent.build(user_instructions=instructions)

    console.print(Markdown(resume))
    out_path = _save_output(resume, output)
    console.print(f"\n[bold green]✓ Saved to:[/bold green] {out_path}")

    if not interactive:
        return

    # Refinement loop
    while True:
        feedback = Prompt.ask(
            "\n[bold cyan]Enter feedback to refine (or press Enter to finish)[/bold cyan]",
            default="",
        )
        if not feedback.strip():
            break

        with console.status("Refining resume…"):
            resume = agent.refine(resume, feedback)

        console.print(Markdown(resume))
        out_path = _save_output(resume, output)
        console.print(f"[bold green]✓ Updated:[/bold green] {out_path}")


@app.command()
def tailor(
    resume: Path = typer.Option(
        ...,
        "--resume",
        "-r",
        help="Path to the resume file to tailor (markdown or plain text).",
    ),
    job_file: Path = typer.Option(
        None,
        "--job-file",
        "-f",
        help="Path to a file containing the job posting text.",
    ),
    job_text: str = typer.Option(
        "",
        "--job-text",
        "-j",
        help="Job posting text passed directly on the command line.",
    ),
    output: str = typer.Option(
        "tailored_resume.md",
        "--output",
        "-o",
        help="Output filename inside the output/ directory.",
    ),
) -> None:
    """Tailor an existing resume to a specific job posting.

    Provide the job posting either as a file (``--job-file``) or as inline text
    (``--job-text``).  The agent rewrites your resume to highlight the most
    relevant experience and keywords for the target role and produces a "Match
    Analysis" section.
    """
    _check_config()
    from career_bot.agents.job_tailor import JobTailorAgent

    if not resume.exists():
        console.print(f"[bold red]Resume file not found:[/bold red] {resume}")
        raise typer.Exit(code=1)

    resume_text = resume.read_text(encoding="utf-8")

    if job_file:
        if not job_file.exists():
            console.print(f"[bold red]Job file not found:[/bold red] {job_file}")
            raise typer.Exit(code=1)
        posting = job_file.read_text(encoding="utf-8")
    elif job_text:
        posting = job_text
    else:
        # Fall back to interactive multi-line input
        console.print(
            "[bold cyan]Paste the job posting below. "
            "Enter a blank line followed by EOF (Ctrl-D / Ctrl-Z) when done.[/bold cyan]"
        )
        lines: list[str] = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            pass
        posting = "\n".join(lines)

    if not posting.strip():
        console.print("[bold red]No job posting provided.[/bold red]")
        raise typer.Exit(code=1)

    agent = JobTailorAgent()

    console.print(Panel("[bold]Job Tailor[/bold] 🎯", expand=False))

    with console.status("Tailoring resume…"):
        result = agent.tailor(resume_text, posting)

    console.print(Markdown(result))
    out_path = _save_output(result, output)
    console.print(f"\n[bold green]✓ Saved to:[/bold green] {out_path}")


@app.command()
def interview() -> None:
    """Start an interactive interview coaching session.

    The coach draws on your career documents to ask relevant practice questions,
    give feedback on your answers, and run mock interviews.  Type ``quit`` or
    press Ctrl-C to exit.
    """
    _check_config()
    from career_bot.agents.interview_coach import InterviewCoachAgent

    coach = InterviewCoachAgent()

    console.print(Panel("[bold]Interview Coach[/bold] 🎓", expand=False))

    with console.status("Loading your career documents…"):
        welcome = coach.start_session()

    console.print(Markdown(welcome))

    try:
        while True:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            if user_input.strip().lower() in {"quit", "exit", "q"}:
                console.print("[bold]Goodbye! Good luck with your interviews! 🚀[/bold]")
                break

            with console.status("Coach is thinking…"):
                reply = coach.chat(user_input)

            console.print(f"\n[bold green]Coach:[/bold green]")
            console.print(Markdown(reply))

    except KeyboardInterrupt:
        console.print("\n[bold]Session ended.[/bold]")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()
