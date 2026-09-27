"""
Deal Intelligence Agent - core logic.

Uses Groq (fast, free-tier LLM) to:
1. Summarize raw call notes into structured memory entries
2. Generate a pre-call briefing by recalling past memories for a deal
3. Suggest objection-handling tactics based on patterns across memories

Set GROQ_API_KEY in your environment.
"""

import os
from groq import Groq

GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))


def _chat(system: str, user: str) -> str:
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    return completion.choices[0].message.content.strip()


def summarize_call_notes(deal_name: str, raw_notes: str) -> str:
    """Turn messy call notes into a clean structured memory entry."""
    system = (
        "You are a sales-ops assistant. Turn raw sales call notes into a concise, "
        "structured summary capturing: objections raised, competitors mentioned, "
        "stakeholders involved, pricing discussion, and next steps. "
        "Keep it factual and terse - this will be stored as long-term memory."
    )
    user = f"Deal: {deal_name}\n\nRaw notes:\n{raw_notes}"
    return _chat(system, user)


def generate_briefing(deal_name: str, memories: list[dict]) -> str:
    """Generate a pre-call briefing from all past memories for this deal."""
    if not memories:
        return (
            f"No prior history found for **{deal_name}**. This looks like a first "
            "interaction - go in with discovery questions rather than assumptions."
        )

    history_text = "\n\n".join(
        f"[{m.get('timestamp', 'unknown date')}] {m['content']}" for m in memories
    )
    system = (
        "You are a sales rep's AI assistant. You are given the full call history "
        "for one deal. Produce a tight pre-call briefing: "
        "1) Summary of where the deal stands, "
        "2) Objections raised so far and how to preempt them, "
        "3) Competitors mentioned and how to differentiate, "
        "4) Recommended tactics for the NEXT call based on what has worked/failed. "
        "Be specific and actionable, not generic."
    )
    user = f"Deal: {deal_name}\n\nFull call history:\n{history_text}"
    return _chat(system, user)


def suggest_tactics_across_deals(all_deal_summaries: str) -> str:
    """
    Cross-deal pattern learning: given summaries across MULTIPLE deals,
    surface which objection-handling approaches tend to work.
    This is what makes memory 'the star' - showing learning across
    interactions, not just recall within one deal.
    """
    system = (
        "You are a sales enablement AI. Given summaries of objections and outcomes "
        "across multiple deals, identify patterns: which objection-handling "
        "approaches correlate with deals progressing, and which stall deals. "
        "Give 3-5 concrete, reusable tactics a rep should apply going forward."
    )
    return _chat(system, all_deal_summaries)
