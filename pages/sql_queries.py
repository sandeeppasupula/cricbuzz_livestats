"""
pages/sql_queries.py
Cricket Intelligence & SQL Analytics Workbench.
Houses all 25 pre-engineered analytical queries across Beginner (1-8),
Intermediate (9-16), and Advanced (17-25) tiers with syntax inspectors,
logic breakdowns, execution metrics, and instant CSV export capabilities.
"""

import streamlit as st
import pandas as pd
from utils.db_connection import run_query

# 1. Spacing fix to prevent header clipping
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown('<span class="arcade-badge">Analytics Workbench</span>', unsafe_allow_html=True)
st.title("🔍 Cricket Intelligence & SQL Analytics")
st.caption("Execute 25 industrial-grade SQL queries across Beginner, Intermediate, and Advanced analytical models.")

# 2. Master Query Catalog
SQL_CATALOG = {
    "Beginner": [
        {
            "id": 1,
            "title": "Q1: Indian National Team Roster",
            "desc": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
            "sql": """
                SELECT full_name, playing_role, batting_style, bowling_style
                FROM players
                WHERE country = 'India'
                ORDER BY full_name ASC;
            """,
            "explanation": "Uses a basic `SELECT` with a `WHERE country = 'India'` filter to isolate domestic players and sorts alphabetically."
        },
        {
            "id": 2,
            "title": "Q2: Matches Played in the Last 30 Days",
            "desc": "Show all cricket matches played in the last 30 days with descriptions, teams, venue, city, and date.",
            "sql": """
                SELECT m.match_description, m.team1_name, m.team2_name,
                       v.venue_name, v.city, m.match_date
                FROM matches m
                JOIN venues v ON m.venue_id = v.venue_id
                WHERE m.match_date >= date('2026-10-15', '-30 days')
                ORDER BY m.match_date DESC;
            """,
            "explanation": "Performs an `INNER JOIN` between `matches` and `venues` on `venue_id` and filters using SQLite's `date()` relative offset function."
        },
        {
            "id": 3,
            "title": "Q3: Top 10 ODI Run Scorers",
            "desc": "List the top 10 highest run scorers in ODI cricket with runs, batting average, and centuries.",
            "sql": """
                SELECT p.full_name AS player_name, c.runs_scored, c.batting_average, c.centuries
                FROM player_career_stats c
                JOIN players p ON c.player_id = p.player_id
                WHERE c.cricket_format = 'ODI'
                ORDER BY c.runs_scored DESC
                LIMIT 10;
            """,
            "explanation": "Joins career stats with player records, isolates `cricket_format = 'ODI'`, and limits to the top 10 using `ORDER BY runs_scored DESC LIMIT 10`."
        },
        {
            "id": 4,
            "title": "Q4: Global Venues with Capacity > 50,000",
            "desc": "Display all cricket venues with seating capacity exceeding 50,000 spectators ordered by largest first.",
            "sql": """
                SELECT venue_name, city, country, capacity
                FROM venues
                WHERE capacity > 50000
                ORDER BY capacity DESC;
            """,
            "explanation": "Applies a numeric predicate `capacity > 50000` on the `venues` table and sorts in descending order."
        },
        {
            "id": 5,
            "title": "Q5: Match Victories by International Team",
            "desc": "Calculate total match victories achieved by each international team across all formats.",
            "sql": """
                SELECT winning_team AS team_name, COUNT(*) AS total_wins
                FROM matches
                WHERE winning_team IS NOT NULL AND winning_team != ''
                GROUP BY winning_team
                ORDER BY total_wins DESC;
            """,
            "explanation": "Groups records by `winning_team` and applies aggregate `COUNT(*)` to tally total match wins."
        },
        {
            "id": 6,
            "title": "Q6: Player Distribution by Playing Role",
            "desc": "Count how many players belong to each playing role (Batsman, Bowler, All-rounder, Wicket-keeper).",
            "sql": """
                SELECT playing_role, COUNT(*) AS total_players
                FROM players
                GROUP BY playing_role
                ORDER BY total_players DESC;
            """,
            "explanation": "Buckets player profiles using `GROUP BY playing_role` to analyze squad demographic distributions."
        },
        {
            "id": 7,
            "title": "Q7: Highest Individual Score by Cricket Format",
            "desc": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I).",
            "sql": """
                SELECT cricket_format, MAX(highest_score) AS max_individual_score
                FROM player_career_stats
                GROUP BY cricket_format
                ORDER BY max_individual_score DESC;
            """,
            "explanation": "Groups format statistics using `GROUP BY cricket_format` and extracts format ceiling scores using `MAX(highest_score)`."
        },
        {
            "id": 8,
            "title": "Q8: Cricket Series Commencing in 2024",
            "desc": "Show all cricket series that started in the year 2024 including host country, match type, and planned fixtures.",
            "sql": """
                SELECT series_name, host_country, match_type, start_date, total_matches_planned
                FROM series
                WHERE start_date LIKE '2024%'
                ORDER BY start_date ASC;
            """,
            "explanation": "Uses string pattern matching (`LIKE '2024%'`) on ISO date strings to filter tournaments starting in calendar year 2024."
        }
    ],
    "Intermediate": [
        {
            "id": 9,
            "title": "Q9: Premier All-Rounders (>1000 Runs & >50 Wickets)",
            "desc": "Find all-rounders who scored > 1,000 runs and took > 50 wickets in their career by format.",
            "sql": """
                SELECT p.full_name AS player_name, c.cricket_format,
                       c.runs_scored, c.wickets_taken
                FROM player_career_stats c
                JOIN players p ON c.player_id = p.player_id
                WHERE c.runs_scored > 1000 AND c.wickets_taken > 50
                ORDER BY c.runs_scored DESC;
            """,
            "explanation": "Applies composite boolean conditions (`runs_scored > 1000 AND wickets_taken > 50`) across multi-table joins to identify elite two-way performers."
        },
        {
            "id": 10,
            "title": "Q10: Detailed Log of Last 20 Completed Matches",
            "desc": "Retrieve details of the last 20 completed matches with teams, winner, victory margin, and venue.",
            "sql": """
                SELECT m.match_description, m.team1_name, m.team2_name,
                       m.winning_team, m.victory_margin, m.victory_type,
                       v.venue_name, m.match_date
                FROM matches m
                JOIN venues v ON m.venue_id = v.venue_id
                WHERE m.status = 'Completed'
                ORDER BY m.match_date DESC
                LIMIT 20;
            """,
            "explanation": "Combines status filtering (`status = 'Completed'`) with foreign key table resolution and chronological sorting."
        },
        {
            "id": 11,
            "title": "Q11: Cross-Format Run Comparison",
            "desc": "Compare performance for players with >= 2 formats: runs in Test, ODI, and T20I, with overall average.",
            "sql": """
                SELECT p.full_name AS player_name,
                       SUM(CASE WHEN c.cricket_format = 'Test' THEN c.runs_scored ELSE 0 END) AS test_runs,
                       SUM(CASE WHEN c.cricket_format = 'ODI' THEN c.runs_scored ELSE 0 END) AS odi_runs,
                       SUM(CASE WHEN c.cricket_format = 'T20I' THEN c.runs_scored ELSE 0 END) AS t20i_runs,
                       ROUND(AVG(c.batting_average), 2) AS overall_batting_avg
                FROM player_career_stats c
                JOIN players p ON c.player_id = p.player_id
                GROUP BY p.player_id
                HAVING COUNT(DISTINCT c.cricket_format) >= 2
                ORDER BY (test_runs + odi_runs + t20i_runs) DESC;
            """,
            "explanation": "Pivots rows into format columns using conditional `CASE WHEN` aggregation and applies a post-aggregation `HAVING COUNT(DISTINCT format) >= 2` filter."
        },
        {
            "id": 12,
            "title": "Q12: Home vs. Away Victory Breakdown",
            "desc": "Determine wins in home vs. away conditions based on whether the venue country matches team country.",
            "sql": """
                SELECT t.team_name,
                       SUM(CASE WHEN m.winning_team = t.team_name AND v.country = t.country THEN 1 ELSE 0 END) AS home_wins,
                       SUM(CASE WHEN m.winning_team = t.team_name AND v.country != t.country THEN 1 ELSE 0 END) AS away_wins
                FROM teams t
                JOIN matches m ON t.team_name = m.team1_name OR t.team_name = m.team2_name
                JOIN venues v ON m.venue_id = v.venue_id
                GROUP BY t.team_name
                ORDER BY (home_wins + away_wins) DESC;
            """,
            "explanation": "Cross-references venue sovereignty against national affiliations to calculate localized home/away win splits."
        },
        {
            "id": 13,
            "title": "Q13: Century Partnerships (>100 Runs)",
            "desc": "Identify batting partnerships where two consecutive batsmen scored >= 100 runs in the same innings.",
            "sql": """
                SELECT match_id, innings_number,
                       player1_name || ' & ' || player2_name AS partnership_batters,
                       partnership_runs
                FROM partnerships
                WHERE partnership_runs >= 100
                ORDER BY partnership_runs DESC;
            """,
            "explanation": "Filters consecutive partnership records for century stands and concatenates batter pairs using SQLite's `||` operator."
        },
        {
            "id": 14,
            "title": "Q14: Venue-Specific Bowling Economy (>=3 Matches)",
            "desc": "For bowlers with >= 3 matches at a venue and >= 4 overs per match, calculate average economy rate and total wickets.",
            "sql": """
                SELECT p.full_name AS bowler_name, v.venue_name,
                       COUNT(mp.perf_id) AS matches_played,
                       ROUND(AVG(mp.economy_rate), 2) AS avg_economy_rate,
                       SUM(mp.wickets_taken) AS total_wickets
                FROM match_performances mp
                JOIN players p ON mp.player_id = p.player_id
                JOIN venues v ON mp.venue_id = v.venue_id
                WHERE mp.overs_bowled >= 4.0
                GROUP BY mp.player_id, mp.venue_id
                HAVING COUNT(mp.perf_id) >= 3
                ORDER BY avg_economy_rate ASC;
            """,
            "explanation": "Calculates ground-specific bowling control using composite grouping (`GROUP BY player_id, venue_id`) and volume filtering with `HAVING`."
        },
        {
            "id": 15,
            "title": "Q15: Clutch Player Analysis in Close Matches",
            "desc": "Analyze performances in close matches (<50 runs or <5 wickets): average runs, matches played, and team wins.",
            "sql": """
                SELECT p.full_name AS player_name,
                       COUNT(mp.perf_id) AS close_matches_played,
                       ROUND(AVG(mp.runs_scored), 2) AS avg_runs_close_matches,
                       SUM(CASE WHEN m.winning_team = mp.team_name THEN 1 ELSE 0 END) AS close_match_wins
                FROM match_performances mp
                JOIN matches m ON mp.match_id = m.match_id
                JOIN players p ON mp.player_id = p.player_id
                WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
                   OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
                GROUP BY mp.player_id
                HAVING close_matches_played >= 2
                ORDER BY avg_runs_close_matches DESC;
            """,
            "explanation": "Filters matches on high-pressure criteria (`margin < 50 runs OR margin < 5 wickets`) to calculate pressure batting averages."
        },
        {
            "id": 16,
            "title": "Q16: Annual Batting Progression Since 2020",
            "desc": "For matches since 2020, show each player's average runs and strike rate per year (min 5 matches per year).",
            "sql": """
                SELECT p.full_name AS player_name, mp.match_year,
                       COUNT(mp.perf_id) AS matches_played,
                       ROUND(AVG(mp.runs_scored), 2) AS avg_runs_per_match,
                       ROUND(AVG(mp.strike_rate), 2) AS avg_strike_rate
                FROM match_performances mp
                JOIN players p ON mp.player_id = p.player_id
                WHERE mp.match_year >= 2020 AND mp.batted_in_match = 1
                GROUP BY mp.player_id, mp.match_year
                HAVING matches_played >= 5
                ORDER BY mp.player_id, mp.match_year ASC;
            """,
            "explanation": "Tracks longitudinal player output across seasons by grouping on `(player_id, match_year)` with a minimum 5-match threshold."
        }
    ],
    "Advanced": [
        {
            "id": 17,
            "title": "Q17: Toss Decision Win-Advantage Analysis",
            "desc": "Calculate the percentage of matches won by the toss winner, broken down by toss decision (Bat vs. Field).",
            "sql": """
                SELECT toss_decision,
                       COUNT(*) AS total_matches,
                       SUM(CASE WHEN toss_winner = winning_team THEN 1 ELSE 0 END) AS toss_winner_wins,
                       ROUND((SUM(CASE WHEN toss_winner = winning_team THEN 1.0 ELSE 0.0 END) / COUNT(*)) * 100, 2) AS win_percentage
                FROM matches
                GROUP BY toss_decision;
            """,
            "explanation": "Computes strategic probability splits using conditional floating-point ratios (`SUM(CASE WHEN ...) / COUNT(*) * 100`)."
        },
        {
            "id": 18,
            "title": "Q18: Most Economical Limited-Overs Bowlers",
            "desc": "Find economical bowlers in ODI/T20 with >= 10 matches and >= 2 overs per match on average.",
            "sql": """
                SELECT p.full_name AS bowler_name,
                       COUNT(mp.perf_id) AS matches_bowled,
                       ROUND(AVG(mp.overs_bowled), 1) AS avg_overs_per_match,
                       ROUND(SUM(mp.runs_conceded) / SUM(mp.overs_bowled), 2) AS true_economy_rate,
                       SUM(mp.wickets_taken) AS total_wickets
                FROM match_performances mp
                JOIN players p ON mp.player_id = p.player_id
                WHERE mp.cricket_format IN ('ODI', 'T20I')
                GROUP BY mp.player_id
                HAVING matches_bowled >= 10 AND avg_overs_per_match >= 2.0
                ORDER BY true_economy_rate ASC;
            """,
            "explanation": "Computes true bowling economy across limited-overs spells (`SUM(runs_conceded) / SUM(overs_bowled)`) rather than averaging averages."
        },
        {
            "id": 19,
            "title": "Q19: Batting Consistency Index (Standard Deviation)",
            "desc": "Calculate average runs and standard deviation of runs for batsmen facing >= 10 balls since 2022 (Lower STDDEV = more consistent).",
            "sql": """
                SELECT p.full_name AS batsman_name,
                       COUNT(mp.perf_id) AS innings_count,
                       ROUND(AVG(mp.runs_scored), 2) AS avg_runs,
                       ROUND(STDDEV(mp.runs_scored), 2) AS consistency_stddev
                FROM match_performances mp
                JOIN players p ON mp.player_id = p.player_id
                WHERE mp.match_year >= 2022 AND mp.balls_faced >= 10
                GROUP BY mp.player_id
                HAVING innings_count >= 5
                ORDER BY consistency_stddev ASC;
            """,
            "explanation": "Executes our custom SQLite `STDDEV` aggregate function to measure run variance, where a lower spread indicates reliable scoring."
        },
        {
            "id": 20,
            "title": "Q20: Multi-Format Match Counts & Averages (>=20 Matches)",
            "desc": "Analyze matches played and batting averages across Test, ODI, and T20 formats for players with >= 20 total matches.",
            "sql": """
                SELECT p.full_name AS player_name,
                       SUM(CASE WHEN c.cricket_format = 'Test' THEN c.matches_played ELSE 0 END) AS test_matches,
                       SUM(CASE WHEN c.cricket_format = 'Test' THEN c.batting_average ELSE 0.0 END) AS test_avg,
                       SUM(CASE WHEN c.cricket_format = 'ODI' THEN c.matches_played ELSE 0 END) AS odi_matches,
                       SUM(CASE WHEN c.cricket_format = 'ODI' THEN c.batting_average ELSE 0.0 END) AS odi_avg,
                       SUM(CASE WHEN c.cricket_format = 'T20I' THEN c.matches_played ELSE 0 END) AS t20i_matches,
                       SUM(CASE WHEN c.cricket_format = 'T20I' THEN c.batting_average ELSE 0.0 END) AS t20i_avg,
                       SUM(c.matches_played) AS total_matches
                FROM player_career_stats c
                JOIN players p ON c.player_id = p.player_id
                GROUP BY p.player_id
                HAVING total_matches >= 20
                ORDER BY total_matches DESC;
            """,
            "explanation": "Aggregates multi-format career volume using conditional transposition and filters for seasoned players with `>= 20` career appearances."
        },
        {
            "id": 21,
            "title": "Q21: Composite Weighted Player Performance Ranking",
            "desc": "Combines batting, bowling, and fielding into a single weighted score using the exact formula from specifications.",
            "sql": """
                WITH PlayerMetrics AS (
                    SELECT p.full_name, c.cricket_format,
                           (c.runs_scored * 0.01 + c.batting_average * 0.5 + c.strike_rate * 0.3) AS batting_points,
                           (c.wickets_taken * 2.0 + CASE WHEN c.bowling_average > 0 THEN (50 - c.bowling_average) * 0.5 ELSE 0 END + (6.0 - c.economy_rate) * 2.0) AS bowling_points,
                           (c.catches * 3.0 + c.stumpings * 5.0) AS fielding_points
                    FROM player_career_stats c
                    JOIN players p ON c.player_id = p.player_id
                )
                SELECT full_name, cricket_format,
                       ROUND(batting_points, 2) AS bat_pts,
                       ROUND(bowling_points, 2) AS bowl_pts,
                       ROUND(fielding_points, 2) AS field_pts,
                       ROUND(batting_points + bowling_points + fielding_points, 2) AS total_composite_score,
                       RANK() OVER (PARTITION BY cricket_format ORDER BY (batting_points + bowling_points + fielding_points) DESC) AS format_rank
                FROM PlayerMetrics
                ORDER BY cricket_format, format_rank ASC;
            """,
            "explanation": "Utilizes a Common Table Expression (`WITH PlayerMetrics AS (...)`) and a Window Function (`RANK() OVER (PARTITION BY format ...)`) to rank players by weighted index."
        },
        {
            "id": 22,
            "title": "Q22: Head-to-Head Team Dominance & Margin Analysis",
            "desc": "Head-to-head analysis between teams with >= 5 matches in the last 3 years: wins, win %, and victory margins.",
            "sql": """
                SELECT team1_name AS team_a, team2_name AS team_b,
                       COUNT(*) AS total_encounters,
                       SUM(CASE WHEN winning_team = team1_name THEN 1 ELSE 0 END) AS team_a_wins,
                       SUM(CASE WHEN winning_team = team2_name THEN 1 ELSE 0 END) AS team_b_wins,
                       ROUND(AVG(CASE WHEN winning_team = team1_name THEN victory_margin ELSE NULL END), 1) AS avg_team_a_margin,
                       ROUND((SUM(CASE WHEN winning_team = team1_name THEN 1.0 ELSE 0.0 END) / COUNT(*)) * 100, 2) AS team_a_win_pct
                FROM matches
                WHERE match_date >= date('2026-10-15', '-3 years')
                GROUP BY team1_name, team2_name
                HAVING total_encounters >= 5
                ORDER BY total_encounters DESC;
            """,
            "explanation": "Computes bilateral rivalry records over a 3-year rolling window with average victory margins and percentage shares."
        },
        {
            "id": 23,
            "title": "Q23: Form & Momentum Categorization",
            "desc": "Calculates last 5 vs last 10 innings averages, strike rate trends, and categorizes players into Form Tiers.",
            "sql": """
                WITH RankedInnings AS (
                    SELECT mp.player_id, p.full_name, mp.runs_scored, mp.strike_rate,
                           ROW_NUMBER() OVER (PARTITION BY mp.player_id ORDER BY mp.match_date DESC) AS innings_recency
                    FROM match_performances mp
                    JOIN players p ON mp.player_id = p.player_id
                    WHERE mp.batted_in_match = 1
                ),
                FormMetrics AS (
                    SELECT player_id, full_name,
                           AVG(CASE WHEN innings_recency <= 5 THEN runs_scored END) AS last_5_avg,
                           AVG(CASE WHEN innings_recency <= 10 THEN runs_scored END) AS last_10_avg,
                           AVG(CASE WHEN innings_recency <= 5 THEN strike_rate END) AS recent_sr,
                           SUM(CASE WHEN innings_recency <= 10 AND runs_scored >= 50 THEN 1 ELSE 0 END) AS fifty_plus_scores,
                           STDDEV(CASE WHEN innings_recency <= 10 THEN runs_scored END) AS recent_stddev
                    FROM RankedInnings
                    WHERE innings_recency <= 10
                    GROUP BY player_id
                )
                SELECT full_name,
                       ROUND(last_5_avg, 2) AS last_5_avg,
                       ROUND(last_10_avg, 2) AS last_10_avg,
                       ROUND(recent_sr, 2) AS recent_sr,
                       fifty_plus_scores,
                       CASE
                           WHEN last_5_avg >= 55 AND fifty_plus_scores >= 2 THEN '🔥 Excellent Form'
                           WHEN last_5_avg >= 40 THEN '✅ Good Form'
                           WHEN last_5_avg >= 25 THEN '⚡ Average Form'
                           ELSE '⚠️ Poor Form'
                       END AS form_category
                FROM FormMetrics
                ORDER BY last_5_avg DESC;
            """,
            "explanation": "Employs `ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_date DESC)` to segment the last 5 and 10 innings, categorizing momentum via conditional rules."
        },
        {
            "id": 24,
            "title": "Q24: Partnership Synergy & Success Rate (>=5 Stands)",
            "desc": "Ranks consecutive batting pairs (>=5 partnerships) by average runs, 50+ stands, and success rate.",
            "sql": """
                SELECT player1_name || ' & ' || player2_name AS batting_duo,
                       COUNT(*) AS total_partnerships,
                       ROUND(AVG(partnership_runs), 2) AS avg_partnership_runs,
                       SUM(CASE WHEN partnership_runs >= 50 THEN 1 ELSE 0 END) AS stands_above_50,
                       MAX(partnership_runs) AS highest_stand,
                       ROUND((SUM(CASE WHEN partnership_runs >= 50 THEN 1.0 ELSE 0.0 END) / COUNT(*)) * 100, 2) AS success_rate_pct
                FROM partnerships
                GROUP BY player1_name, player2_name
                HAVING total_partnerships >= 5
                ORDER BY avg_partnership_runs DESC;
            """,
            "explanation": "Calculates pair synergy by tracking consecutive batting partnerships, benchmark conversions (50+ runs), and conversion percentages."
        },
        {
            "id": 25,
            "title": "Q25: Longitudinal Career Trajectory Modeling",
            "desc": "Tracks quarterly averages and classifies career phase as Ascending, Declining, or Stable across >= 6 quarters.",
            "sql": """
                WITH QuarterlyStats AS (
                    SELECT p.full_name, mp.match_quarter,
                           COUNT(mp.perf_id) AS quarter_matches,
                           AVG(mp.runs_scored) AS q_avg_runs,
                           AVG(mp.strike_rate) AS q_avg_sr
                    FROM match_performances mp
                    JOIN players p ON mp.player_id = p.player_id
                    WHERE mp.batted_in_match = 1
                    GROUP BY mp.player_id, mp.match_quarter
                    HAVING quarter_matches >= 3
                ),
                QuarterDiffs AS (
                    SELECT full_name, match_quarter, q_avg_runs,
                           LAG(q_avg_runs, 1) OVER (PARTITION BY full_name ORDER BY match_quarter ASC) AS prev_q_avg,
                           COUNT(*) OVER (PARTITION BY full_name) AS total_quarters_active
                    FROM QuarterlyStats
                )
                SELECT full_name,
                       COUNT(*) AS qualifying_quarters,
                       ROUND(AVG(q_avg_runs), 2) AS career_span_avg,
                       ROUND(AVG(q_avg_runs - prev_q_avg), 2) AS avg_quarterly_delta,
                       CASE
                           WHEN AVG(q_avg_runs - prev_q_avg) > 1.5 THEN '🚀 Career Ascending'
                           WHEN AVG(q_avg_runs - prev_q_avg) < -1.5 THEN '📉 Career Declining'
                           ELSE '⚖️ Career Stable'
                       END AS trajectory_status
                FROM QuarterDiffs
                WHERE prev_q_avg IS NOT NULL AND total_quarters_active >= 6
                GROUP BY full_name
                ORDER BY avg_quarterly_delta DESC;
            """,
            "explanation": "Uses the `LAG()` analytical window function across quarterly intervals to calculate momentum derivatives and classify trajectories."
        }
    ]
}

# 3. Mount Difficulty Tabs
tab_beg, tab_mid, tab_adv = st.tabs([
    "🌱 Beginner Queries (Q1–Q8)",
    "⚡ Intermediate Queries (Q9–Q16)",
    "🚀 Advanced Analytics (Q17–Q25)"
])

def render_query_section(tier_name: str):
    queries = SQL_CATALOG[tier_name]
    titles = [f"{q['title']}" for q in queries]
    
    selected_idx = st.selectbox(
        f"Select {tier_name} Query Model",
        range(len(titles)),
        format_func=lambda x: titles[x],
        key=f"select_{tier_name.lower()}"
    )
    
    item = queries[selected_idx]
    
    # Prompt & Analytical Objective
    st.markdown(
        f"""<div class="arcade-card" style="margin: 12px 0;">
            <div style="font-size: 11px; font-weight: 700; color: #14B8A6; text-transform: uppercase;">
                Analytical Objective
            </div>
            <div style="font-size: 15px; font-weight: 600; color: #E5E7EB; margin-top: 4px;">
                {item['desc']}
            </div>
        </div>""",
        unsafe_allow_html=True
    )
    
    # Logic Explanation
    st.info(f"💡 **Under the Hood:** {item['explanation']}")
    
    # Collapsible SQL Syntax Inspector
    with st.expander("🛠️ Inspect Raw SQL Query Syntax", expanded=False):
        st.code(item['sql'].strip(), language="sql")
    
    # Execute query
    df_result = run_query(item['sql'])
    
    # Action Header with Results Count & CSV Download
    col_records, col_export = st.columns([3, 1])
    with col_records:
        st.markdown(f"**Query Results:** `{len(df_result)} record(s) returned`")
    with col_export:
        if not df_result.empty:
            csv_data = df_result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export CSV",
                data=csv_data,
                file_name=f"cricbuzz_query_{item['id']}_export.csv",
                mime="text/csv",
                key=f"dl_{item['id']}"
            )
    
    if not df_result.empty:
        st.dataframe(df_result, use_container_width=True, hide_index=True)
    else:
        st.warning("Query executed successfully, but returned 0 rows for current filter parameters.")

with tab_beg:
    render_query_section("Beginner")

with tab_mid:
    render_query_section("Intermediate")

with tab_adv:
    render_query_section("Advanced")