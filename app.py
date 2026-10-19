"""
Cricbuzz LiveStats - Professional Sports Analytics Platform.
Main application runner with executive dark aesthetic and reactive navigation.
"""

import os
import streamlit as st
from utils.db_connection import DB_PATH
from utils.seed_database import initialize_database

# 1. Wide-screen configuration
st.set_page_config(
    page_title="Cricbuzz LiveStats | Cricket Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Auto-initialize database silently in background if first run
if not os.path.exists(DB_PATH):
    initialize_database()

# 3. High-End SaaS Dark Theme (Deep Navy, Neon Teal, Burnished Gold)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0B1220;
        --card: #131C2E;
        --card-hover: #18243B;
        --line: #1F2C42;
        --accent: #14B8A6;
        --accent-glow: rgba(20, 184, 166, 0.2);
        --gold: #E8A33D;
        --ink: #E5E7EB;
        --ink-sub: #8A97AB;
        --green: #3FB950;
    }

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--ink);
    }

    /* Top Live HUD Grid */
    .hud-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 14px;
        margin-bottom: 24px;
    }
    .hud-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 16px 18px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .hud-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent);
    }
    .hud-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--ink-sub);
        margin-bottom: 6px;
    }
    .hud-value {
        font-size: 26px;
        font-weight: 800;
        color: var(--ink);
        line-height: 1.1;
    }
    .hud-value.teal { color: var(--accent); }
    .hud-value.gold { color: var(--gold); }
    .hud-delta {
        font-size: 12px;
        font-weight: 600;
        color: var(--green);
        margin-top: 5px;
    }

    /* Match Showcase Cards */
    .match-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 14px;
        transition: all 0.2s ease;
    }
    .match-card:hover {
        border-color: #2A3A55;
        background: var(--card-hover);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--line);
        padding-bottom: 10px;
        margin-bottom: 12px;
    }
    .match-format {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(20, 184, 166, 0.15);
        color: var(--accent);
    }
    .match-venue {
        font-size: 12px;
        color: var(--ink-sub);
    }
    .team-row {
        display: flex;
        justify-content: space-between;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .match-result {
        font-size: 12px;
        font-weight: 600;
        color: var(--gold);
        margin-top: 10px;
        padding-top: 8px;
        border-top: 1px dashed var(--line);
    }

    /* Navigation Action Cards */
    .nav-card {
        background: linear-gradient(135deg, #131C2E, #0E1626);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 22px;
        height: 100%;
        transition: all 0.25s ease;
    }
    .nav-card:hover {
        border-color: var(--accent);
        box-shadow: 0 6px 20px var(--accent-glow);
    }
    .nav-title {
        font-size: 17px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 8px;
    }
    .nav-desc {
        font-size: 13px;
        color: var(--ink-sub);
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 4. Multi-Page Structure
pages = {
    "Analytics Hub": [
        st.Page("pages/home.py", title="Match Center & Portal", icon="🏏", default=True),
        st.Page("pages/live_matches.py", title="Live Match Tracker", icon="⚡"),
        st.Page("pages/top_stats.py", title="Player Leaderboards", icon="📊"),
        st.Page("pages/sql_queries.py", title="Cricket Intelligence Engine", icon="🔍"),
        st.Page("pages/crud_operations.py", title="Data Management Studio", icon="🛠️"),
    ]
}

pg = st.navigation(pages)

with st.sidebar:
    st.markdown("### 🏏 Cricbuzz LiveStats")
    st.caption("International Cricket Analytics & Intelligence Platform")
    st.divider()

pg.run()