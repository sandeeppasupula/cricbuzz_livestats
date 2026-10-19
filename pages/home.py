"""
Cricbuzz LiveStats - Match Center & Intelligence Portal.
Professional landing page displaying live system KPIs, real-time recent international fixtures
fetched from Cricbuzz API with team crests, format filters, and spotlight performers.
"""

import streamlit as st
from utils.db_connection import run_query
from utils.api_handler import fetch_recent_matches

# 1. Official National Team Flags Map
TEAM_FLAGS = {
    "India": "https://flagcdn.com/w40/in.png",
    "IND": "https://flagcdn.com/w40/in.png",
    "Australia": "https://flagcdn.com/w40/au.png",
    "AUS": "https://flagcdn.com/w40/au.png",
    "England": "https://flagcdn.com/w40/gb-eng.png",
    "ENG": "https://flagcdn.com/w40/gb-eng.png",
    "South Africa": "https://flagcdn.com/w40/za.png",
    "SA": "https://flagcdn.com/w40/za.png",
    "New Zealand": "https://flagcdn.com/w40/nz.png",
    "NZ": "https://flagcdn.com/w40/nz.png",
    "Pakistan": "https://flagcdn.com/w40/pk.png",
    "PAK": "https://flagcdn.com/w40/pk.png",
    "Sri Lanka": "https://flagcdn.com/w40/lk.png",
    "SL": "https://flagcdn.com/w40/lk.png",
    "West Indies": "https://flagcdn.com/w40/jm.png",
    "WI": "https://flagcdn.com/w40/jm.png",
    "Bangladesh": "https://flagcdn.com/w40/bd.png",
    "BAN": "https://flagcdn.com/w40/bd.png",
    "Afghanistan": "https://flagcdn.com/w40/af.png",
    "AFG": "https://flagcdn.com/w40/af.png",
    "Nepal": "https://flagcdn.com/w40/np.png",
    "Oman": "https://flagcdn.com/w40/om.png",
    "Zimbabwe": "https://flagcdn.com/w40/zw.png",
}

# 2. Top Header Banner
col_head, col_status = st.columns([4, 1])
with col_head:
    st.title("🏏 Match Center & Analytics Hub")
    st.caption("Real-Time Tracking • Historical Performance Modeling • Statistical Intelligence")
with col_status:
    st.markdown(
        """<div style="text-align: right; margin-top: 15px;">
            <span style="background: rgba(63, 185, 80, 0.15); color: #3FB950; padding: 6px 12px; border-radius: 99px; font-weight: 700; font-size: 12px; border: 1px solid rgba(63, 185, 80, 0.4);">
                ● LIVE SYNC
            </span>
        </div>""",
        unsafe_allow_html=True,
    )

# 3. Dynamic Metric HUD Strip
team_count = run_query("SELECT COUNT(*) AS c FROM teams").iloc[0]["c"]
match_count = run_query("SELECT COUNT(*) AS c FROM matches").iloc[0]["c"]
player_count = run_query("SELECT COUNT(*) AS c FROM players").iloc[0]["c"]
venue_count = run_query("SELECT COUNT(*) AS c FROM venues").iloc[0]["c"]

st.markdown(
    f"""<div class="hud-grid">
        <div class="hud-card">
            <div class="hud-label">International Teams</div>
            <div class="hud-value teal">{team_count}</div>
            <div class="hud-delta">Active ICC Roster</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Tracked Fixtures</div>
            <div class="hud-value">{match_count}</div>
            <div class="hud-delta">Test • ODI • T20I</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Global Players</div>
            <div class="hud-value">{player_count}</div>
            <div class="hud-delta">Multi-Format Profiles</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">World Venues</div>
            <div class="hud-value">{venue_count}</div>
            <div class="hud-delta">Capacity & Pitch Profiles</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Analytics Engine</div>
            <div class="hud-value gold">25 Models</div>
            <div class="hud-delta">Form • H2H • Projections</div>
        </div>
    </div>""",
    unsafe_allow_html=True,
)

st.divider()

# 4. Main Dashboard: Real-Time Recent Fixtures from Cricbuzz API
left_col, right_col = st.columns([5, 3])

with left_col:
    st.subheader("⚡ Recent International Fixtures")

    fmt_filter = st.segmented_control(
        "Filter by Format",
        options=["All", "ODI", "T20", "TEST"],
        default="All",
        label_visibility="collapsed",
    )

    active_filter = fmt_filter if fmt_filter else "All"

    recent_matches_raw, is_api_live = fetch_recent_matches()

    # Format Filter Normalization (Matches ODI, T20/T20I, TEST)
    if active_filter == "All":
        display_matches = recent_matches_raw[:6]
    elif active_filter == "T20":
        display_matches = [m for m in recent_matches_raw if "T20" in m.get("format", "").upper()][:6]
    elif active_filter == "TEST":
        display_matches = [m for m in recent_matches_raw if "TEST" in m.get("format", "").upper()][:6]
    else:
        display_matches = [m for m in recent_matches_raw if active_filter.upper() == m.get("format", "").upper()][:6]

    if not display_matches:
        display_matches = recent_matches_raw[:4]

    for row in display_matches:
        t1 = row.get("team1_name", "Team 1")
        t2 = row.get("team2_name", "Team 2")
        winner = row.get("winning_team", "")
        result = row.get("result_text", "Match Concluded")
        fmt = row.get("format", "Cricket")
        venue = row.get("venue_name", "Stadium")
        city = row.get("city", "")

        t1_flag = TEAM_FLAGS.get(t1, "https://flagcdn.com/w40/un.png")
        t2_flag = TEAM_FLAGS.get(t2, "https://flagcdn.com/w40/un.png")

        t1_won = winner and (t1.lower() in winner.lower())
        t2_won = winner and (t2.lower() in winner.lower())

        t1_badge = '<span style="color:#14B8A6; font-weight:700;">🏆 Winner</span>' if t1_won else ''
        t2_badge = '<span style="color:#14B8A6; font-weight:700;">🏆 Winner</span>' if t2_won else ''

        card_html = (
            f'<div class="match-card">'
            f'<div class="match-header">'
            f'<span class="match-format">{fmt}</span>'
            f'<span class="match-venue">📍 {venue}, {city}</span>'
            f'</div>'
            f'<div class="team-row" style="align-items:center;">'
            f'<span style="display:inline-flex; align-items:center; gap:10px;">'
            f'<img src="{t1_flag}" width="24" height="16" style="border-radius:2px; vertical-align:middle;"/> '
            f'<b>{t1}</b>'
            f'</span>'
            f'{t1_badge}'
            f'</div>'
            f'<div class="team-row" style="align-items:center;">'
            f'<span style="display:inline-flex; align-items:center; gap:10px;">'
            f'<img src="{t2_flag}" width="24" height="16" style="border-radius:2px; vertical-align:middle;"/> '
            f'<b>{t2}</b>'
            f'</span>'
            f'{t2_badge}'
            f'</div>'
            f'<div class="match-result">'
            f'{result}'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

with right_col:
    st.subheader("🔥 Top Spotlight Performers")

    top_bat = run_query(
        """
        SELECT p.full_name, p.country, c.runs_scored, c.batting_average, c.cricket_format
        FROM player_career_stats c
        JOIN players p ON c.player_id = p.player_id
        ORDER BY c.runs_scored DESC
        LIMIT 3;
        """
    )

    for _, batter in top_bat.iterrows():
        p_flag = TEAM_FLAGS.get(batter['country'], "https://flagcdn.com/w40/un.png")
        st.markdown(
            f"""<div class="hud-card" style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <span style="display:inline-flex; align-items:center; gap:8px;">
                        <img src="{p_flag}" width="20" height="14" style="border-radius:2px;"/>
                        <b style="font-size: 15px;">{batter['full_name']}</b>
                    </span>
                    <span style="font-size: 11px; color: #14B8A6; font-weight: 700;">{batter['cricket_format']}</span>
                </div>
                <div style="color: #8A97AB; font-size: 12px; margin: 4px 0 8px 28px;">{batter['country']}</div>
                <div style="display: flex; justify-content: space-between;">
                    <div><span style="color: #8A97AB; font-size: 11px;">RUNS:</span> <b style="color: #E8A33D;">{batter['runs_scored']:,}</b></div>
                    <div><span style="color: #8A97AB; font-size: 11px;">AVG:</span> <b>{batter['batting_average']}</b></div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.subheader("🏟️ Premier Venues")
    top_venues = run_query("SELECT venue_name, city, country, capacity FROM venues ORDER BY capacity DESC LIMIT 2;")
    for _, venue in top_venues.iterrows():
        v_flag = TEAM_FLAGS.get(venue['country'], "https://flagcdn.com/w40/un.png")
        st.markdown(
            f"""<div style="background: #131C2E; border: 1px solid #1F2C42; border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size: 13px;">{venue['venue_name']}</b>
                    <img src="{v_flag}" width="20" height="14" style="border-radius:2px;"/>
                </div>
                <div style="font-size: 12px; color: #8A97AB; margin-top:4px;">
                    {venue['city']}, {venue['country']} &bull; Capacity: <b style="color: #14B8A6;">{venue['capacity']:,}</b>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

st.divider()

# 5. Portal Action Launchers
st.subheader("🚀 Platform Modules")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    st.markdown(
        """<div class="nav-card">
            <div class="nav-title">⚡ Live Match Tracker</div>
            <div class="nav-desc">Real-time ball-by-ball scorecards, run rate comparisons, and live in-game stats.</div>
        </div>""",
        unsafe_allow_html=True,
    )
with nav_col2:
    st.markdown(
        """<div class="nav-card">
            <div class="nav-title">📊 Player Leaderboards</div>
            <div class="nav-desc">Interactive multi-format rankings for run scorers, wicket-takers, and bowling economy rates.</div>
        </div>""",
        unsafe_allow_html=True,
    )
with nav_col3:
    st.markdown(
        """<div class="nav-card">
            <div class="nav-title">🔍 Cricket Intelligence</div>
            <div class="nav-desc">25 deep statistical SQL algorithms covering form momentum, toss advantage, and partnerships.</div>
        </div>""",
        unsafe_allow_html=True,
    )
with nav_col4:
    st.markdown(
        """<div class="nav-card">
            <div class="nav-title">🛠️ Data Management</div>
            <div class="nav-desc">Studio interface for maintaining player registries, match records, and career database entries.</div>
        </div>""",
        unsafe_allow_html=True,
    )