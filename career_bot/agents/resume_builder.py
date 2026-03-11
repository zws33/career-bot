"""Resume Builder agent – creates a professional resume from the candidate's
personal documents stored in the vector store.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from career_bot.config import settings
from career_bot.prompts.resume_prompts import (
    RESUME_HUMAN_PROMPT,
    RESUME_REFINE_PROMPT,
    RESUME_SYSTEM_PROMPT,
)
from career_bot.tools.document_processor import retrieve_context


class ResumeBuilderAgent:
    """Agent persona that generates a professional resume from the candidate's
    stored career documents.

    Usage::

        agent = ResumeBuilderAgent()
        resume = agent.build()
        revised = agent.refine(resume, "Make the summary shorter.")
    """

    def __init__(self, model: str | None = None) -> None:
        self._llm = ChatOpenAI(
            model=model or settings.openai_model,
            temperature=0.3,
            openai_api_key=settings.openai_api_key,
        )

    def build(self, user_instructions: str = "") -> str:
        """Build a full resume from the candidate's personal documents.

        Parameters
        ----------
        user_instructions:
            Optional extra guidance (e.g. "focus on leadership experience" or
            "target a senior Android engineer role at a startup").

        Returns
        -------
        str
            The generated resume in markdown format.
        """
        context = retrieve_context(
            "skills experience accomplishments projects education Android"
        )

        system_msg = SystemMessage(
            content=RESUME_SYSTEM_PROMPT.format(context=context)
        )
        human_msg = HumanMessage(
            content=RESUME_HUMAN_PROMPT.format(
                user_instructions=user_instructions or "No extra instructions."
            )
        )

        response = self._llm.invoke([system_msg, human_msg])
        return str(response.content)

    def refine(self, current_resume: str, feedback: str) -> str:
        """Refine an existing resume draft based on user feedback.

        Parameters
        ----------
        current_resume:
            The resume text to revise.
        feedback:
            The user's revision instructions.

        Returns
        -------
        str
            The revised resume in markdown format.
        """
        context = retrieve_context(
            "skills experience accomplishments projects education Android"
        )

        system_msg = SystemMessage(
            content=RESUME_SYSTEM_PROMPT.format(context=context)
        )
        human_msg = HumanMessage(
            content=RESUME_REFINE_PROMPT.format(
                current_resume=current_resume,
                feedback=feedback,
            )
        )

        response = self._llm.invoke([system_msg, human_msg])
        return str(response.content)
