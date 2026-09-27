"""
Deal Intelligence Agent - Streamlit App
HackWithHyderabad 3.0 (Hindsight track)

Run with:  streamlit run app.py
"""

import streamlit as st
from hindsight_client import get_client
from agent import summarize_call_notes, generate_briefing, suggest_tactics_across_deals

st.set_page_config(page_title="Deal Intelligence Agent", page_icon="🧠", layout="wide")

st.title("🧠 Deal Intelligence Agent")
st.caption("Remembers every call across a deal cycle — objections, competitors, pricing — and gets sharper with every interaction.")

with st.sidebar:
    st.header("Select / Create Deal")
    deal_name = st.text_input("Deal name (e.g. acme-corp)", value="acme-corp").strip().lower().replace(" ", "-")
    st.markdown("---")
    st.markdown(
        "**How this works**\n\n"
        "1. Log notes after each sales call\n"
        "2. Agent stores a structured memory via Hindsight\n"
        "3. Before your next call, get an instant briefing built from full deal history\n"
        "4. Cross-deal view surfaces which tactics actually work"
    )

if not deal_name:
    st.warning("Enter a deal name in the sidebar to get started.")
    st.stop()

client = get_client(deal_name)

tab1, tab2, tab3 = st.tabs(["📝 Log a Call", "📋 Pre-Call Briefing", "📊 Cross-Deal Patterns"])

# ---------------- Tab 1: Log a call ----------------
with tab1:
    st.subheader(f"Log a call for: {deal_name}")
    raw_notes = st.text_area(
        "Paste raw call notes",
        height=200,
        placeholder="e.g. Talked to Priya (VP Eng). She's worried about integration time. "
                    "Mentioned they're also evaluating CompetitorX. Budget is ~$40k/yr. "
                    "Next step: send technical deep-dive doc by Friday.",
    )
    if st.button("Summarize & Store Memory", type="primary"):
        if not raw_notes.strip():
            st.error("Paste some call notes first.")
        else:
            with st.spinner("Summarizing and storing in Hindsight memory..."):
                summary = summarize_call_notes(deal_name, raw_notes)
                client.add_memory(summary, metadata={"deal": deal_name})
            st.success("Memory stored.")
            st.markdown("**Structured summary saved:**")
            st.info(summary)

    st.markdown("---")
    st.subheader("Full memory history for this deal")
    memories = client.get_all_memories()
    if not memories:
        st.caption("No memories yet — log your first call above.")
    else:
        for m in reversed(memories):
            with st.expander(f"{m.get('timestamp', 'unknown date')}"):
                st.write(m["content"])

# ---------------- Tab 2: Pre-call briefing ----------------
with tab2:
    st.subheader(f"Pre-call briefing: {deal_name}")
    st.caption("This is where memory becomes visible — generic without it, sharp with it.")
    if st.button("Generate Briefing", type="primary"):
        with st.spinner("Recalling deal history and generating briefing..."):
            memories = client.get_all_memories()
            briefing = generate_briefing(deal_name, memories)
        st.markdown(briefing)

# ---------------- Tab 3: Cross-deal pattern learning ----------------
with tab3:
    st.subheader("What's working across all deals?")
    st.caption("This is the 'agent gets smarter over time' story — patterns learned across every deal, not just one.")
    deal_names_input = st.text_input(
        "Enter deal names to compare (comma-separated)",
        value=deal_name,
    )
    if st.button("Analyze Patterns", type="primary"):
        names = [d.strip().lower().replace(" ", "-") for d in deal_names_input.split(",") if d.strip()]
        combined = []
        for name in names:
            c = get_client(name)
            mems = c.get_all_memories()
            if mems:
                combined.append(f"=== Deal: {name} ===\n" + "\n".join(m["content"] for m in mems))
        if not combined:
            st.warning("No memory found for those deals yet. Log some calls first.")
        else:
            with st.spinner("Finding patterns across deals..."):
                tactics = suggest_tactics_across_deals("\n\n".join(combined))
            st.markdown(tactics)
