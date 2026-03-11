"""Interview Coach agent – interactive, persona-driven interview preparation
coach specialising in Android engineering roles.
"""

from __future__ import annotations

from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from career_bot.config import settings
from career_bot.prompts.interview_prompts import (
    INTERVIEW_COACH_FIRST_MESSAGE,
    INTERVIEW_COACH_SYSTEM_PROMPT,
)
from career_bot.tools.document_processor import retrieve_context


class InterviewCoachAgent:
    """Agent persona that coaches the candidate for Android engineering
    interviews through an interactive conversation.

    The agent maintains a rolling message history so context is preserved
    across multiple turns in a single session.

    Usage::

        coach = InterviewCoachAgent()
        print(coach.start_session())      # welcome message
        reply = coach.chat("Give me a hard Kotlin coroutines question.")
        print(reply)
        reply = coach.chat("Here's my answer: ...")
        print(reply)
    """

    def __init__(self, model: str | None = None) -> None:
        self._llm = ChatOpenAI(
            model=model or settings.openai_model,
            temperature=0.7,  # slightly higher creativity for coaching
            openai_api_key=settings.openai_api_key,
        )
        self._history: List[HumanMessage | AIMessage] = []
        self._system_msg: SystemMessage | None = None

    # ──────────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────────

    def start_session(self) -> str:
        """Initialise a coaching session and return the welcome message.

        This method loads the candidate's career context from the vector store
        and prepares the system prompt.  Call it once before :meth:`chat`.
        """
        context = retrieve_context(
            "skills experience accomplishments projects Android"
        )

        self._system_msg = SystemMessage(
            content=INTERVIEW_COACH_SYSTEM_PROMPT.format(context=context)
        )
        self._history = []

        return INTERVIEW_COACH_FIRST_MESSAGE

    def chat(self, user_message: str) -> str:
        """Send *user_message* to the coach and return the coach's reply.

        Maintains full conversation history so the coach can reference earlier
        turns (e.g. "As I mentioned in your last answer…").

        Parameters
        ----------
        user_message:
            A message from the candidate.

        Returns
        -------
        str
            The coach's response.
        """
        if self._system_msg is None:
            import warnings
            warnings.warn(
                "start_session() has not been called. Starting a new session automatically.",
                stacklevel=2,
            )
            self.start_session()

        self._history.append(HumanMessage(content=user_message))

        messages = [self._system_msg, *self._history]
        response = self._llm.invoke(messages)

        ai_message = AIMessage(content=str(response.content))
        self._history.append(ai_message)

        return str(response.content)

    def reset(self) -> None:
        """Clear conversation history and start a fresh session."""
        self._history = []
        self._system_msg = None
