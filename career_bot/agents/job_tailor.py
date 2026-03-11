"""Job Tailor agent – rewrites an existing resume to match a specific job posting.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from career_bot.config import settings
from career_bot.prompts.job_tailor_prompts import (
    JOB_TAILOR_HUMAN_PROMPT,
    JOB_TAILOR_SYSTEM_PROMPT,
)


class JobTailorAgent:
    """Agent persona that tailors a resume to a specific job posting.

    Usage::

        agent = JobTailorAgent()
        result = agent.tailor(resume_text, job_posting_text)
    """

    def __init__(self, model: str | None = None) -> None:
        self._llm = ChatOpenAI(
            model=model or settings.openai_model,
            temperature=0.3,
            openai_api_key=settings.openai_api_key,
        )

    def tailor(self, resume: str, job_posting: str) -> str:
        """Tailor *resume* to the requirements in *job_posting*.

        Parameters
        ----------
        resume:
            The candidate's current resume (markdown or plain text).
        job_posting:
            The full text of the job posting.

        Returns
        -------
        str
            A tailored resume followed by a "Match Analysis" section, both in
            markdown format.
        """
        system_msg = SystemMessage(content=JOB_TAILOR_SYSTEM_PROMPT)
        human_msg = HumanMessage(
            content=JOB_TAILOR_HUMAN_PROMPT.format(
                resume=resume,
                job_posting=job_posting,
            )
        )

        response = self._llm.invoke([system_msg, human_msg])
        return str(response.content)
