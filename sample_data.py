"""
Seeds realistic synthetic deal data for demo purposes.
Run: python sample_data.py
This pre-populates memory for 2 fake deals so the "Pre-Call Briefing" and
"Cross-Deal Patterns" tabs have something to show immediately.
"""

from hindsight_client import get_client
from agent import summarize_call_notes

DEALS = {
    "acme-manufacturing": [
        "Call 1 with Rakesh Mehta (VP Operations) at Acme Manufacturing. He's concerned "
        "about integration time with their legacy ERP. Mentioned they're also looking at "
        "CompetitorX. Budget range discussed: $35-45k/yr. Next step: send integration "
        "timeline doc.",
        "Call 2 with Rakesh and Priya Nair (IT Lead). Addressed integration concerns with "
        "the timeline doc - they were satisfied. New objection: security/compliance "
        "questions since they're in a regulated industry. Competitor mention: they ruled "
        "out CompetitorX due to poor support reviews. Next step: security whitepaper + "
        "compliance call with our security team.",
        "Call 3 - security call went well. Rakesh is ready to move to pricing negotiation. "
        "He pushed back on the $45k figure, wants $38k. Mentioned budget approval needs "
        "CFO sign-off by end of quarter. Next step: revised proposal at $40k with annual "
        "commit discount.",
    ],
    "brightpath-retail": [
        "Call 1 with Sara Iyer (Head of Analytics) at BrightPath Retail. Interested but "
        "skeptical about ROI - wants case studies from similar retail companies. No "
        "competitor mentioned yet. Next step: send 2 retail case studies.",
        "Call 2 - case studies landed well. New objection: implementation would need to "
        "happen during their busy holiday season, worried about disruption. Also "
        "mentioned they got a cold outreach from CompetitorY with a lower price point. "
        "Next step: propose phased rollout starting after holiday season.",
    ],
}


def main():
    for deal_name, calls in DEALS.items():
        client = get_client(deal_name)
        print(f"Seeding {deal_name}...")
        for notes in calls:
            summary = summarize_call_notes(deal_name, notes)
            client.add_memory(summary, metadata={"deal": deal_name})
            print(f"  stored memory ({len(summary)} chars)")
    print("Done. Run `streamlit run app.py` and try deal names: "
          "'acme-manufacturing' or 'brightpath-retail'")


if __name__ == "__main__":
    main()
