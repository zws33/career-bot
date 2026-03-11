"""Tests for the career-bot agents using mocked LLM calls."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


# ── ResumeBuilderAgent ────────────────────────────────────────────────────────


class TestResumeBuilderAgent:
    """Tests for ResumeBuilderAgent."""

    @patch("career_bot.agents.resume_builder.retrieve_context", return_value="mock context")
    @patch("career_bot.agents.resume_builder.ChatOpenAI")
    def test_build_returns_string(self, mock_chat_cls, mock_retrieve):
        """build() should return the LLM response as a string."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="# John Doe\nAndroid Engineer")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.resume_builder import ResumeBuilderAgent

        agent = ResumeBuilderAgent()
        result = agent.build()

        assert isinstance(result, str)
        assert "John Doe" in result
        mock_llm.invoke.assert_called_once()

    @patch("career_bot.agents.resume_builder.retrieve_context", return_value="mock context")
    @patch("career_bot.agents.resume_builder.ChatOpenAI")
    def test_build_passes_instructions(self, mock_chat_cls, mock_retrieve):
        """build() should include user_instructions in the human message."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="resume")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.resume_builder import ResumeBuilderAgent

        agent = ResumeBuilderAgent()
        agent.build(user_instructions="target senior role")

        call_args = mock_llm.invoke.call_args[0][0]
        human_msg = call_args[-1]
        assert "target senior role" in human_msg.content

    @patch("career_bot.agents.resume_builder.retrieve_context", return_value="mock context")
    @patch("career_bot.agents.resume_builder.ChatOpenAI")
    def test_refine_includes_feedback(self, mock_chat_cls, mock_retrieve):
        """refine() should include both the current resume and the feedback."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="revised resume")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.resume_builder import ResumeBuilderAgent

        agent = ResumeBuilderAgent()
        result = agent.refine("original resume text", "make summary shorter")

        assert isinstance(result, str)
        call_args = mock_llm.invoke.call_args[0][0]
        human_msg = call_args[-1]
        assert "original resume text" in human_msg.content
        assert "make summary shorter" in human_msg.content


# ── JobTailorAgent ────────────────────────────────────────────────────────────


class TestJobTailorAgent:
    """Tests for JobTailorAgent."""

    @patch("career_bot.agents.job_tailor.ChatOpenAI")
    def test_tailor_returns_string(self, mock_chat_cls):
        """tailor() should return the LLM response as a string."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="tailored resume")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.job_tailor import JobTailorAgent

        agent = JobTailorAgent()
        result = agent.tailor("my resume", "senior android engineer job posting")

        assert isinstance(result, str)
        assert result == "tailored resume"

    @patch("career_bot.agents.job_tailor.ChatOpenAI")
    def test_tailor_passes_resume_and_posting(self, mock_chat_cls):
        """tailor() should include both resume and job_posting in the prompt."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="output")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.job_tailor import JobTailorAgent

        agent = JobTailorAgent()
        agent.tailor("MY_RESUME_CONTENT", "JOB_POSTING_CONTENT")

        call_args = mock_llm.invoke.call_args[0][0]
        human_msg = call_args[-1]
        assert "MY_RESUME_CONTENT" in human_msg.content
        assert "JOB_POSTING_CONTENT" in human_msg.content


# ── InterviewCoachAgent ───────────────────────────────────────────────────────


class TestInterviewCoachAgent:
    """Tests for InterviewCoachAgent."""

    @patch(
        "career_bot.agents.interview_coach.retrieve_context",
        return_value="mock context",
    )
    @patch("career_bot.agents.interview_coach.ChatOpenAI")
    def test_start_session_returns_welcome(self, mock_chat_cls, mock_retrieve):
        """start_session() should return the welcome message string."""
        from career_bot.agents.interview_coach import (
            InterviewCoachAgent,
            INTERVIEW_COACH_FIRST_MESSAGE,
        )

        mock_chat_cls.return_value = MagicMock()
        agent = InterviewCoachAgent()
        welcome = agent.start_session()

        assert welcome == INTERVIEW_COACH_FIRST_MESSAGE

    @patch(
        "career_bot.agents.interview_coach.retrieve_context",
        return_value="mock context",
    )
    @patch("career_bot.agents.interview_coach.ChatOpenAI")
    def test_chat_returns_string(self, mock_chat_cls, mock_retrieve):
        """chat() should return the LLM reply as a string."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="Here is a question...")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.interview_coach import InterviewCoachAgent

        agent = InterviewCoachAgent()
        agent.start_session()
        reply = agent.chat("Give me a coroutines question.")

        assert isinstance(reply, str)
        assert reply == "Here is a question..."

    @patch(
        "career_bot.agents.interview_coach.retrieve_context",
        return_value="mock context",
    )
    @patch("career_bot.agents.interview_coach.ChatOpenAI")
    def test_chat_accumulates_history(self, mock_chat_cls, mock_retrieve):
        """chat() should grow the conversation history on each turn."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="response")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.interview_coach import InterviewCoachAgent

        agent = InterviewCoachAgent()
        agent.start_session()

        agent.chat("first message")
        agent.chat("second message")

        # History should have 4 entries: 2 human + 2 AI
        assert len(agent._history) == 4

    @patch(
        "career_bot.agents.interview_coach.retrieve_context",
        return_value="mock context",
    )
    @patch("career_bot.agents.interview_coach.ChatOpenAI")
    def test_reset_clears_history(self, mock_chat_cls, mock_retrieve):
        """reset() should clear the conversation history and system message."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="response")
        mock_chat_cls.return_value = mock_llm

        from career_bot.agents.interview_coach import InterviewCoachAgent

        agent = InterviewCoachAgent()
        agent.start_session()
        agent.chat("hello")

        agent.reset()

        assert agent._history == []
        assert agent._system_msg is None
