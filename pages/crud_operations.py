"""
pages/crud_operations.py
Data Management Studio & CRUD Workbench.
Provides form-based interfaces for Create, Read, Update, and Delete operations
on player profiles and statistical career records in cricbuzz.db with live registry KPIs.
"""

import streamlit as st
import pandas as pd
from utils.db_connection import run_query, execute_crud

# 1. Spacing fix to prevent header clipping
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown('<span class="arcade-badge">Registry Management</span>', unsafe_allow_html=True)
st.title("🛠️ Cricket Data Management Studio")
st.caption("Perform transactional Create, Read, Update, and Delete operations directly on cricbuzz.db.")

# 2. Live Registry KPI Strip
total_players = run_query("SELECT COUNT(*) AS c FROM players").iloc[0]["c"]
total_batters = run_query("SELECT COUNT(*) AS c FROM players WHERE playing_role = 'Batsman'").iloc[0]["c"]
total_bowlers = run_query("SELECT COUNT(*) AS c FROM players WHERE playing_role = 'Bowler'").iloc[0]["c"]
total_allrounders = run_query("SELECT COUNT(*) AS c FROM players WHERE playing_role = 'All-rounder'").iloc[0]["c"]

st.markdown(
    f"""<div class="hud-grid" style="margin-bottom: 16px;">
        <div class="hud-card">
            <div class="hud-label">Total Roster</div>
            <div class="hud-value teal">{total_players}</div>
            <div class="hud-delta">Registered Profiles</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Specialist Batters</div>
            <div class="hud-value">{total_batters}</div>
            <div class="hud-delta">Top & Middle Order</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Specialist Bowlers</div>
            <div class="hud-value">{total_bowlers}</div>
            <div class="hud-delta">Pace & Spin Units</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">All-Rounders</div>
            <div class="hud-value gold">{total_allrounders}</div>
            <div class="hud-delta">Dual-Discipline Players</div>
        </div>
    </div>""",
    unsafe_allow_html=True
)

st.divider()

# 3. CRUD Operation Tabs
tab_create, tab_read, tab_update, tab_delete = st.tabs([
    "➕ Register Player (Create)",
    "🔍 Player Registry (Read)",
    "✏️ Edit Career Stats (Update)",
    "🗑️ Retire Player (Delete)"
])

# ==============================================================================
# 1. CREATE: Register New Player
# ==============================================================================
with tab_create:
    st.subheader("Register a New International Player")
    st.markdown("Add a player profile and initialize their career record in the relational database.")

    with st.form("form_create_player", clear_on_submit=True):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            new_name = st.text_input("Full Name *", placeholder="e.g. Yashasvi Jaiswal")
            new_country = st.selectbox("National Team *", [
                "India", "Australia", "England", "South Africa",
                "New Zealand", "Pakistan", "Sri Lanka", "West Indies",
                "Afghanistan", "Bangladesh", "Ireland", "Zimbabwe"
            ])
            new_role = st.selectbox("Playing Role *", [
                "Batsman", "Bowler", "All-rounder", "Wicket-keeper"
            ])
        with col_c2:
            new_bat_style = st.selectbox("Batting Style *", [
                "Right-hand bat", "Left-hand bat"
            ])
            new_bowl_style = st.selectbox("Bowling Style *", [
                "Right-arm fast", "Left-arm fast", "Right-arm fast-medium",
                "Right-arm offbreak", "Right-arm legbreak",
                "Slow left-arm orthodox", "Left-arm wrist-spin", "None"
            ])
            init_format = st.selectbox("Primary Initial Format *", ["ODI", "T20I", "Test"])

        st.markdown("##### Initial Format Career Figures")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            init_matches = st.number_input("Matches Played", min_value=0, value=1, step=1)
            init_runs = st.number_input("Runs Scored", min_value=0, value=0, step=10)
        with col_s2:
            init_hs = st.number_input("Highest Score", min_value=0, value=0, step=1)
            init_avg = st.number_input("Batting Average", min_value=0.0, value=0.0, step=0.5)
        with col_s3:
            init_sr = st.number_input("Strike Rate", min_value=0.0, value=0.0, step=1.0)
            init_100s = st.number_input("Centuries (100s)", min_value=0, value=0, step=1)
        with col_s4:
            init_wkts = st.number_input("Wickets Taken", min_value=0, value=0, step=1)
            init_econ = st.number_input("Economy Rate", min_value=0.0, value=0.0, step=0.1)

        submitted_create = st.form_submit_button("Commit Player to Database", use_container_width=True)

        if submitted_create:
            if not new_name.strip():
                st.error("Player name cannot be empty.")
            else:
                insert_player_sql = """
                    INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style)
                    VALUES (?, ?, ?, ?, ?);
                """
                success_p, msg_p = execute_crud(
                    insert_player_sql,
                    (new_name.strip(), new_country, new_role, new_bat_style, new_bowl_style)
                )

                if success_p:
                    p_id_df = run_query("SELECT last_insert_rowid() AS pid;")
                    generated_id = int(p_id_df.iloc[0]["pid"])

                    insert_stat_sql = """
                        INSERT INTO player_career_stats (
                            player_id, cricket_format, matches_played, innings_batted,
                            runs_scored, highest_score, batting_average, strike_rate,
                            centuries, half_centuries, wickets_taken, bowling_average,
                            economy_rate, catches, stumpings
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, 0.0, ?, 0, 0);
                    """
                    success_s, msg_s = execute_crud(
                        insert_stat_sql,
                        (
                            generated_id, init_format, init_matches, init_matches,
                            init_runs, init_hs, init_avg, init_sr,
                            init_100s, init_wkts, init_econ
                        )
                    )

                    if success_s:
                        st.success(f"Player **{new_name.strip()}** successfully registered with ID #{generated_id}!")
                        st.rerun()
                    else:
                        st.error(f"Failed to initialize stats: {msg_s}")
                else:
                    st.error(f"Failed to create player: {msg_p}")


# ==============================================================================
# 2. READ: Browse & Search Player Directory
# ==============================================================================
with tab_read:
    st.subheader("Player Directory Explorer")

    col_filter_team, col_filter_role = st.columns(2)
    with col_filter_team:
        team_options = ["All Teams"] + list(run_query("SELECT DISTINCT country FROM players ORDER BY country;")["country"])
        sel_team = st.selectbox("Filter by Country", team_options)
    with col_filter_role:
        role_options = ["All Roles"] + list(run_query("SELECT DISTINCT playing_role FROM players ORDER BY playing_role;")["playing_role"])
        sel_role = st.selectbox("Filter by Role", role_options)

    base_read_sql = """
        SELECT p.player_id AS ID, p.full_name AS Name, p.country AS Country,
               p.playing_role AS Role, p.batting_style AS Batting, p.bowling_style AS Bowling,
               COALESCE(SUM(c.runs_scored), 0) AS Total_Runs,
               COALESCE(SUM(c.wickets_taken), 0) AS Total_Wickets
        FROM players p
        LEFT JOIN player_career_stats c ON p.player_id = c.player_id
        WHERE 1=1
    """
    params = []
    if sel_team != "All Teams":
        base_read_sql += " AND p.country = ?"
        params.append(sel_team)
    if sel_role != "All Roles":
        base_read_sql += " AND p.playing_role = ?"
        params.append(sel_role)

    base_read_sql += " GROUP BY p.player_id ORDER BY p.player_id DESC;"

    df_players = run_query(base_read_sql, params=tuple(params))
    st.markdown(f"**Found {len(df_players)} registered players**")
    st.dataframe(df_players, use_container_width=True, hide_index=True)


# ==============================================================================
# 3. UPDATE: Edit Player Career Statistics
# ==============================================================================
with tab_update:
    st.subheader("Modify Existing Player Career Figures")

    all_players_df = run_query("SELECT player_id, full_name, country FROM players ORDER BY full_name ASC;")
    
    if all_players_df.empty:
        st.info("No players available to update.")
    else:
        player_choices = {f"{r['full_name']} ({r['country']}) - #{r['player_id']}": r['player_id'] for _, r in all_players_df.iterrows()}
        selected_player_label = st.selectbox("Select Player to Edit", list(player_choices.keys()))
        target_player_id = player_choices[selected_player_label]

        player_formats_df = run_query(
            "SELECT cricket_format FROM player_career_stats WHERE player_id = ?;",
            params=(target_player_id,)
        )
        
        available_formats = list(player_formats_df["cricket_format"]) if not player_formats_df.empty else ["ODI"]
        selected_format = st.selectbox("Format Record to Update", available_formats)

        curr_stats = run_query(
            """
            SELECT runs_scored, wickets_taken, batting_average, strike_rate, economy_rate, centuries
            FROM player_career_stats
            WHERE player_id = ? AND cricket_format = ?;
            """,
            params=(target_player_id, selected_format)
        )

        curr_runs = int(curr_stats.iloc[0]["runs_scored"]) if not curr_stats.empty else 0
        curr_wkts = int(curr_stats.iloc[0]["wickets_taken"]) if not curr_stats.empty else 0
        curr_avg = float(curr_stats.iloc[0]["batting_average"]) if not curr_stats.empty else 0.0
        curr_sr = float(curr_stats.iloc[0]["strike_rate"]) if not curr_stats.empty else 0.0
        curr_econ = float(curr_stats.iloc[0]["economy_rate"]) if not curr_stats.empty else 0.0
        curr_100s = int(curr_stats.iloc[0]["centuries"]) if not curr_stats.empty else 0

        with st.form("form_update_stats"):
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                up_runs = st.number_input("Total Runs", min_value=0, value=curr_runs, step=25)
                up_avg = st.number_input("Batting Average", min_value=0.0, value=curr_avg, step=0.25)
            with col_u2:
                up_wkts = st.number_input("Total Wickets", min_value=0, value=curr_wkts, step=1)
                up_econ = st.number_input("Economy Rate", min_value=0.0, value=curr_econ, step=0.1)
            with col_u3:
                up_sr = st.number_input("Strike Rate", min_value=0.0, value=curr_sr, step=0.5)
                up_100s = st.number_input("Centuries", min_value=0, value=curr_100s, step=1)

            submitted_update = st.form_submit_button("Commit Updates to Database", use_container_width=True)

            if submitted_update:
                update_sql = """
                    UPDATE player_career_stats
                    SET runs_scored = ?, wickets_taken = ?, batting_average = ?,
                        strike_rate = ?, economy_rate = ?, centuries = ?
                    WHERE player_id = ? AND cricket_format = ?;
                """
                success_u, msg_u = execute_crud(
                    update_sql,
                    (up_runs, up_wkts, up_avg, up_sr, up_econ, up_100s, target_player_id, selected_format)
                )
                if success_u:
                    st.success(f"Updated {selected_format} record for player #{target_player_id} successfully!")
                    st.rerun()
                else:
                    st.error(f"Update failed: {msg_u}")


# ==============================================================================
# 4. DELETE: Retire / Remove Player Record
# ==============================================================================
with tab_delete:
    st.subheader("Retire or Remove a Player Profile")
    st.warning("⚠️ Deleting a player automatically purges all linked format stats and match performances (Cascading Delete).")

    all_players_del = run_query("SELECT player_id, full_name, country FROM players ORDER BY player_id DESC;")

    if all_players_del.empty:
        st.info("No players found in registry.")
    else:
        del_choices = {f"{r['full_name']} ({r['country']}) - ID #{r['player_id']}": r['player_id'] for _, r in all_players_del.iterrows()}
        selected_del_label = st.selectbox("Select Player Profile to Permanently Delete", list(del_choices.keys()))
        target_del_id = del_choices[selected_del_label]

        confirm_checkbox = st.checkbox(f"Confirm permanent deletion of player record #{target_del_id}")

        if st.button("Permanently Delete Record", type="primary"):
            if not confirm_checkbox:
                st.error("Check the confirmation box above before proceeding.")
            else:
                del_sql = "DELETE FROM players WHERE player_id = ?;"
                success_d, msg_d = execute_crud(del_sql, (target_del_id,))
                if success_d:
                    st.success(f"Player #{target_del_id} successfully deleted from the registry!")
                    st.rerun()
                else:
                    st.error(f"Delete failed: {msg_d}")