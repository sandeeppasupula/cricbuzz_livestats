"""
Database Schema Architect & Smart Seeder (Phase 2).
Creates 8 normalized relational tables with proper Primary/Foreign keys and Indexes,
then populates realistic international cricket data for all 25 SQL Analytics queries.
"""

import os
import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cricbuzz.db")


def create_schema(cursor: sqlite3.Cursor):
    cursor.execute("PRAGMA foreign_keys = OFF;")
    tables = [
        "partnerships",
        "match_performances",
        "matches",
        "player_career_stats",
        "players",
        "series",
        "venues",
        "teams",
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL UNIQUE,
            country TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE venues (
            venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            venue_name TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            capacity INTEGER NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE series (
            series_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name TEXT NOT NULL,
            host_country TEXT NOT NULL,
            match_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            total_matches_planned INTEGER NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            country TEXT NOT NULL,
            playing_role TEXT NOT NULL,
            batting_style TEXT NOT NULL,
            bowling_style TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE player_career_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            cricket_format TEXT NOT NULL,
            matches_played INTEGER DEFAULT 0,
            innings_batted INTEGER DEFAULT 0,
            runs_scored INTEGER DEFAULT 0,
            highest_score INTEGER DEFAULT 0,
            batting_average REAL DEFAULT 0.0,
            strike_rate REAL DEFAULT 0.0,
            centuries INTEGER DEFAULT 0,
            half_centuries INTEGER DEFAULT 0,
            wickets_taken INTEGER DEFAULT 0,
            bowling_average REAL DEFAULT 0.0,
            economy_rate REAL DEFAULT 0.0,
            catches INTEGER DEFAULT 0,
            stumpings INTEGER DEFAULT 0,
            FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
            UNIQUE(player_id, cricket_format)
        );
    """)

    cursor.execute("""
        CREATE TABLE matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER,
            match_description TEXT NOT NULL,
            cricket_format TEXT NOT NULL,
            team1_name TEXT NOT NULL,
            team2_name TEXT NOT NULL,
            venue_id INTEGER NOT NULL,
            match_date TEXT NOT NULL,
            toss_winner TEXT NOT NULL,
            toss_decision TEXT NOT NULL,
            winning_team TEXT NOT NULL,
            victory_margin INTEGER NOT NULL,
            victory_type TEXT NOT NULL,
            status TEXT DEFAULT 'Completed',
            FOREIGN KEY (series_id) REFERENCES series(series_id) ON DELETE SET NULL,
            FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE match_performances (
            perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            team_name TEXT NOT NULL,
            venue_id INTEGER NOT NULL,
            cricket_format TEXT NOT NULL,
            match_date TEXT NOT NULL,
            match_year INTEGER NOT NULL,
            match_quarter TEXT NOT NULL,
            runs_scored INTEGER DEFAULT 0,
            balls_faced INTEGER DEFAULT 0,
            strike_rate REAL DEFAULT 0.0,
            overs_bowled REAL DEFAULT 0.0,
            runs_conceded INTEGER DEFAULT 0,
            wickets_taken INTEGER DEFAULT 0,
            economy_rate REAL DEFAULT 0.0,
            batted_in_match INTEGER DEFAULT 1,
            FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
            FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
            FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE partnerships (
            partnership_id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            innings_number INTEGER NOT NULL,
            player1_id INTEGER NOT NULL,
            player1_name TEXT NOT NULL,
            player1_batting_pos INTEGER NOT NULL,
            player2_id INTEGER NOT NULL,
            player2_name TEXT NOT NULL,
            player2_batting_pos INTEGER NOT NULL,
            partnership_runs INTEGER NOT NULL,
            FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
            FOREIGN KEY (player1_id) REFERENCES players(player_id) ON DELETE CASCADE,
            FOREIGN KEY (player2_id) REFERENCES players(player_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("CREATE INDEX idx_players_country ON players(country);")
    cursor.execute("CREATE INDEX idx_players_role ON players(playing_role);")
    cursor.execute("CREATE INDEX idx_career_format ON player_career_stats(cricket_format);")
    cursor.execute("CREATE INDEX idx_matches_date ON matches(match_date);")
    cursor.execute("CREATE INDEX idx_perf_player_date ON match_performances(player_id, match_date);")
    cursor.execute("CREATE INDEX idx_perf_venue ON match_performances(venue_id);")


def seed_data(cursor: sqlite3.Cursor):
    teams_data = [
        ("India", "India"),
        ("Australia", "Australia"),
        ("England", "England"),
        ("South Africa", "South Africa"),
        ("New Zealand", "New Zealand"),
        ("Pakistan", "Pakistan"),
        ("Sri Lanka", "Sri Lanka"),
        ("West Indies", "West Indies"),
    ]
    cursor.executemany("INSERT INTO teams (team_name, country) VALUES (?, ?);", teams_data)

    venues_data = [
        ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
        ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
        ("Eden Gardens", "Kolkata", "India", 68000),
        ("Optus Stadium", "Perth", "Australia", 60000),
        ("Adelaide Oval", "Adelaide", "Australia", 53583),
        ("Rajiv Gandhi International Stadium", "Hyderabad", "India", 55000),
        ("Wankhede Stadium", "Mumbai", "India", 33108),
        ("Lord's Cricket Ground", "London", "England", 31100),
        ("Wanderers Stadium", "Johannesburg", "South Africa", 34000),
        ("Eden Park", "Auckland", "New Zealand", 50000),
    ]
    cursor.executemany(
        "INSERT INTO venues (venue_name, city, country, capacity) VALUES (?, ?, ?, ?);",
        venues_data,
    )

    series_data = [
        ("England Tour of India 2024", "India", "Test", "2024-01-25", 5),
        ("ICC Men's T20 World Cup 2024", "West Indies", "T20I", "2024-06-01", 55),
        ("India Tour of Sri Lanka 2024", "Sri Lanka", "ODI", "2024-08-02", 3),
        ("Border-Gavaskar Trophy 2024-25", "Australia", "Test", "2024-11-22", 5),
        ("Australia Tour of England 2024", "England", "ODI", "2024-09-19", 5),
        ("ICC Champions Trophy 2025", "Pakistan", "ODI", "2025-02-19", 15),
        ("Anderson-Tendulkar Trophy 2025", "England", "Test", "2025-06-20", 5),
        ("ICC Men's T20 World Cup 2026", "India", "T20I", "2026-02-07", 55),
        ("Australia Tour of India Oct 2026", "India", "ODI", "2026-09-20", 5),
    ]
    cursor.executemany(
        """INSERT INTO series
        (series_name, host_country, match_type, start_date, total_matches_planned)
        VALUES (?, ?, ?, ?, ?);""",
        series_data,
    )

    players_data = [
        ("Virat Kohli", "India", "Batsman", "Right-hand bat", "Right-arm medium"),
        ("Rohit Sharma", "India", "Batsman", "Right-hand bat", "Right-arm offbreak"),
        ("Shubman Gill", "India", "Batsman", "Right-hand bat", "Right-arm offbreak"),
        ("KL Rahul", "India", "Wicket-keeper", "Right-hand bat", "None"),
        ("Rishabh Pant", "India", "Wicket-keeper", "Left-hand bat", "None"),
        ("Hardik Pandya", "India", "All-rounder", "Right-hand bat", "Right-arm fast-medium"),
        ("Ravindra Jadeja", "India", "All-rounder", "Left-hand bat", "Slow left-arm orthodox"),
        ("Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Mohammed Siraj", "India", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Kuldeep Yadav", "India", "Bowler", "Left-hand bat", "Left-arm wrist-spin"),
        ("Travis Head", "Australia", "Batsman", "Left-hand bat", "Right-arm offbreak"),
        ("Steve Smith", "Australia", "Batsman", "Right-hand bat", "Right-arm legbreak"),
        ("Glenn Maxwell", "Australia", "All-rounder", "Right-hand bat", "Right-arm offbreak"),
        ("Pat Cummins", "Australia", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Mitchell Starc", "Australia", "Bowler", "Left-hand bat", "Left-arm fast"),
        ("Joe Root", "England", "Batsman", "Right-hand bat", "Right-arm offbreak"),
        ("Jos Buttler", "England", "Wicket-keeper", "Right-hand bat", "None"),
        ("Ben Stokes", "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium"),
        ("Kane Williamson", "New Zealand", "Batsman", "Right-hand bat", "Right-arm offbreak"),
        ("Rachin Ravindra", "New Zealand", "All-rounder", "Left-hand bat", "Slow left-arm orthodox"),
        ("Quinton de Kock", "South Africa", "Wicket-keeper", "Left-hand bat", "None"),
        ("Kagiso Rabada", "South Africa", "Bowler", "Left-hand bat", "Right-arm fast"),
        ("Babar Azam", "Pakistan", "Batsman", "Right-hand bat", "Right-arm offbreak"),
        ("Shaheen Afridi", "Pakistan", "Bowler", "Left-hand bat", "Left-arm fast"),
    ]
    cursor.executemany(
        """INSERT INTO players
        (full_name, country, playing_role, batting_style, bowling_style)
        VALUES (?, ?, ?, ?, ?);""",
        players_data,
    )

    career_stats_data = [
        (1, "ODI", 295, 283, 13906, 183, 58.18, 93.54, 50, 72, 5, 136.0, 6.16, 152, 0),
        (1, "Test", 118, 201, 9040, 254, 47.83, 55.80, 29, 31, 0, 0.0, 0.0, 115, 0),
        (1, "T20I", 125, 117, 4188, 122, 48.69, 137.04, 1, 38, 4, 51.0, 8.05, 54, 0),
        (2, "ODI", 265, 257, 10866, 264, 49.16, 92.43, 31, 57, 9, 64.4, 5.21, 96, 0),
        (2, "Test", 64, 111, 4270, 212, 42.27, 57.05, 12, 18, 2, 112.0, 3.48, 63, 0),
        (2, "T20I", 159, 151, 4231, 121, 32.05, 140.89, 5, 32, 1, 113.0, 9.97, 65, 0),
        (3, "ODI", 50, 50, 2450, 208, 57.00, 101.80, 7, 14, 0, 0.0, 0.0, 28, 0),
        (3, "Test", 30, 54, 1850, 128, 37.75, 59.80, 5, 7, 0, 0.0, 0.0, 26, 0),
        (3, "T20I", 24, 24, 650, 126, 30.95, 145.40, 1, 3, 0, 0.0, 0.0, 12, 0),
        (4, "ODI", 78, 73, 2890, 112, 49.82, 87.60, 7, 18, 0, 0.0, 0.0, 62, 7),
        (4, "Test", 53, 91, 2980, 199, 34.25, 53.10, 8, 15, 0, 0.0, 0.0, 61, 0),
        (4, "T20I", 72, 68, 2265, 110, 37.75, 139.12, 2, 22, 0, 0.0, 0.0, 25, 2),
        (5, "ODI", 31, 27, 871, 125, 33.50, 106.21, 1, 5, 0, 0.0, 0.0, 27, 9),
        (5, "Test", 38, 66, 2690, 159, 44.83, 74.10, 6, 13, 0, 0.0, 0.0, 132, 14),
        (5, "T20I", 76, 66, 1209, 65, 23.25, 127.26, 0, 3, 0, 0.0, 0.0, 44, 11),
        (6, "ODI", 88, 62, 1810, 92, 34.15, 110.36, 0, 11, 86, 35.20, 5.55, 34, 0),
        (6, "T20I", 108, 84, 1680, 71, 28.00, 141.50, 0, 5, 89, 26.40, 8.15, 52, 0),
        (6, "Test", 11, 18, 532, 108, 31.29, 73.88, 1, 4, 17, 31.05, 3.38, 7, 0),
        (7, "ODI", 197, 132, 2756, 87, 32.42, 85.06, 0, 13, 220, 36.07, 4.88, 75, 0),
        (7, "Test", 76, 111, 3230, 175, 36.70, 55.40, 4, 21, 312, 24.05, 2.46, 44, 0),
        (7, "T20I", 74, 41, 515, 46, 21.45, 127.16, 0, 0, 54, 29.85, 7.13, 28, 0),
        (8, "ODI", 89, 25, 91, 16, 7.58, 55.82, 0, 0, 149, 23.55, 4.59, 19, 0),
        (8, "Test", 40, 62, 290, 34, 7.25, 58.00, 0, 0, 181, 20.18, 2.74, 14, 0),
        (8, "T20I", 70, 10, 18, 7, 4.50, 64.28, 0, 0, 89, 17.74, 6.27, 9, 0),
        (9, "ODI", 44, 15, 55, 14, 6.87, 50.00, 0, 0, 71, 24.04, 5.18, 12, 0),
        (9, "Test", 31, 43, 125, 16, 5.20, 42.00, 0, 0, 80, 29.65, 3.35, 10, 0),
        (9, "T20I", 16, 4, 12, 7, 6.00, 80.00, 0, 0, 14, 32.28, 7.79, 4, 0),
        (10, "ODI", 106, 41, 205, 19, 9.76, 61.56, 0, 0, 172, 26.01, 4.99, 16, 0),
        (10, "T20I", 40, 8, 46, 23, 11.50, 79.31, 0, 0, 69, 14.07, 6.77, 11, 0),
        (11, "ODI", 69, 66, 2645, 154, 44.08, 104.96, 6, 16, 21, 41.20, 5.65, 29, 0),
        (11, "Test", 51, 84, 3410, 175, 42.62, 65.80, 7, 17, 12, 54.0, 3.50, 41, 0),
        (11, "T20I", 38, 37, 1093, 91, 33.12, 160.49, 0, 5, 2, 35.0, 8.75, 14, 0),
        (12, "ODI", 163, 147, 5606, 164, 43.45, 87.13, 12, 34, 28, 34.67, 5.42, 88, 0),
        (12, "Test", 111, 198, 9750, 239, 56.68, 53.50, 32, 41, 19, 53.47, 3.82, 183, 0),
        (12, "T20I", 67, 55, 1094, 90, 24.86, 125.45, 0, 5, 17, 22.17, 7.77, 41, 0),
        (13, "ODI", 142, 130, 3950, 201, 34.64, 126.40, 4, 23, 73, 47.10, 5.48, 86, 0),
        (13, "T20I", 113, 103, 2600, 120, 29.88, 154.12, 5, 11, 43, 28.90, 7.65, 51, 0),
        (14, "ODI", 90, 59, 537, 37, 14.13, 79.55, 0, 0, 143, 28.78, 5.29, 25, 0),
        (14, "Test", 64, 95, 1310, 64, 16.58, 45.20, 0, 3, 275, 22.53, 2.86, 26, 0),
        (14, "T20I", 57, 30, 158, 28, 10.53, 118.79, 0, 0, 66, 23.57, 7.42, 16, 0),
        (15, "ODI", 125, 69, 572, 52, 12.17, 81.94, 0, 1, 241, 22.96, 5.25, 26, 0),
        (15, "Test", 91, 132, 2150, 99, 20.67, 56.40, 0, 10, 362, 27.60, 3.41, 31, 0),
        (15, "T20I", 65, 20, 98, 16, 9.80, 91.58, 0, 0, 79, 23.81, 7.74, 17, 0),
        (16, "ODI", 171, 160, 6522, 133, 47.60, 86.77, 16, 39, 27, 58.40, 5.65, 84, 0),
        (16, "Test", 149, 272, 12754, 262, 51.22, 56.90, 35, 64, 69, 45.80, 3.30, 204, 0),
        (16, "T20I", 32, 30, 893, 90, 35.72, 126.30, 0, 5, 6, 23.00, 7.66, 18, 0),
        (17, "ODI", 181, 154, 5022, 162, 39.54, 117.11, 11, 26, 0, 0.0, 0.0, 226, 37),
        (17, "T20I", 126, 115, 3389, 101, 35.67, 146.50, 1, 25, 0, 0.0, 0.0, 74, 14),
        (17, "Test", 57, 100, 2907, 152, 31.94, 54.05, 2, 18, 0, 0.0, 0.0, 161, 1),
        (18, "ODI", 114, 99, 3463, 182, 41.22, 95.68, 5, 24, 74, 42.39, 6.05, 53, 0),
        (18, "Test", 108, 195, 6580, 258, 35.56, 58.80, 13, 34, 206, 32.02, 3.31, 111, 0),
        (18, "T20I", 43, 37, 585, 52, 21.66, 128.00, 0, 1, 26, 32.65, 8.39, 23, 0),
        (19, "ODI", 165, 157, 6810, 148, 48.64, 81.14, 13, 45, 37, 35.40, 5.35, 68, 0),
        (19, "Test", 102, 180, 8881, 251, 54.48, 51.60, 32, 35, 30, 40.20, 3.20, 96, 0),
        (19, "T20I", 93, 90, 2575, 95, 33.44, 123.08, 0, 18, 6, 27.33, 8.20, 46, 0),
        (21, "ODI", 155, 155, 6770, 178, 45.74, 96.64, 21, 30, 0, 0.0, 0.0, 209, 17),
        (21, "T20I", 92, 91, 2584, 100, 31.51, 138.32, 1, 16, 0, 0.0, 0.0, 84, 18),
        (21, "Test", 54, 91, 3300, 141, 38.82, 70.93, 6, 22, 0, 0.0, 0.0, 221, 11),
        (23, "ODI", 120, 117, 5850, 158, 56.25, 88.90, 19, 32, 0, 0.0, 0.0, 54, 0),
        (23, "T20I", 123, 116, 4145, 122, 41.03, 129.08, 3, 36, 0, 0.0, 0.0, 48, 0),
        (23, "Test", 55, 100, 3997, 196, 44.41, 54.60, 9, 26, 2, 20.0, 3.00, 39, 0),
    ]
    cursor.executemany(
        """INSERT INTO player_career_stats
        (player_id, cricket_format, matches_played, innings_batted, runs_scored, highest_score,
         batting_average, strike_rate, centuries, half_centuries, wickets_taken,
         bowling_average, economy_rate, catches, stumpings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
        career_stats_data,
    )

    today = datetime(2026, 10, 15)
    matches_data = []

    recent_specs = [
        (9, "1st ODI - IND vs AUS 2026", "ODI", "India", "Australia", 1, 26, "India", "Bat", "India", 28, "runs"),
        (9, "2nd ODI - IND vs AUS 2026", "ODI", "India", "Australia", 6, 22, "Australia", "Field", "Australia", 4, "wickets"),
        (9, "3rd ODI - IND vs AUS 2026", "ODI", "India", "Australia", 3, 18, "India", "Field", "India", 6, "wickets"),
        (9, "4th ODI - IND vs AUS 2026", "ODI", "India", "Australia", 7, 12, "Australia", "Bat", "India", 3, "wickets"),
        (9, "5th ODI - IND vs AUS 2026", "ODI", "India", "Australia", 1, 7, "India", "Bat", "India", 42, "runs"),
        (8, "1st T20I - ENG vs SA 2026", "T20I", "England", "South Africa", 8, 15, "England", "Field", "England", 18, "runs"),
        (8, "2nd T20I - ENG vs SA 2026", "T20I", "England", "South Africa", 8, 10, "South Africa", "Bat", "South Africa", 12, "runs"),
        (8, "3rd T20I - NZ vs PAK 2026", "T20I", "New Zealand", "Pakistan", 10, 4, "New Zealand", "Bat", "New Zealand", 5, "wickets"),
    ]
    for s_id, desc, fmt, t1, t2, v_id, days_ago, tw, td, wt, vm, vt in recent_specs:
        m_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        matches_data.append((s_id, desc, fmt, t1, t2, v_id, m_date, tw, td, wt, vm, vt, "Completed"))

    historical_specs = [
        (6, "Champions Trophy Semi-Final", "ODI", "India", "Australia", 2, "2025-03-04", "Australia", "Bat", "India", 5, "wickets"),
        (8, "T20 WC Super 8 - IND vs AUS", "T20I", "India", "Australia", 1, "2026-02-24", "India", "Bat", "India", 24, "runs"),
        (4, "1st Test - BGT Perth", "Test", "Australia", "India", 4, "2024-11-22", "India", "Bat", "India", 295, "runs"),
        (4, "2nd Test - BGT Adelaide", "Test", "Australia", "India", 5, "2024-12-06", "Australia", "Bat", "Australia", 10, "wickets"),
        (4, "4th Test - BGT Melbourne", "Test", "Australia", "India", 2, "2024-12-26", "Australia", "Bat", "Australia", 184, "runs"),
        (1, "1st Test - IND vs ENG Hyderabad", "Test", "India", "England", 6, "2024-01-25", "England", "Bat", "England", 28, "runs"),
        (1, "2nd Test - IND vs ENG", "Test", "India", "England", 3, "2024-02-02", "India", "Bat", "India", 106, "runs"),
        (1, "3rd Test - IND vs ENG", "Test", "India", "England", 1, "2024-02-15", "India", "Bat", "India", 434, "runs"),
        (2, "T20 WC Semi-Final 2024", "T20I", "India", "England", 7, "2024-06-27", "England", "Field", "India", 68, "runs"),
        (7, "1st Test - ENG vs IND Lord's", "Test", "England", "India", 8, "2025-06-20", "England", "Field", "India", 45, "runs"),
        (7, "2nd Test - ENG vs IND", "Test", "England", "India", 8, "2025-07-02", "India", "Bat", "England", 4, "wickets"),
        (5, "1st ODI - ENG vs AUS", "ODI", "England", "Australia", 8, "2024-09-19", "England", "Bat", "Australia", 7, "wickets"),
        (5, "2nd ODI - ENG vs AUS", "ODI", "England", "Australia", 8, "2024-09-21", "England", "Field", "Australia", 68, "runs"),
        (5, "3rd ODI - ENG vs AUS", "ODI", "England", "Australia", 8, "2024-09-24", "England", "Field", "England", 46, "runs"),
        (5, "4th ODI - ENG vs AUS", "ODI", "England", "Australia", 8, "2024-09-27", "Australia", "Field", "England", 186, "runs"),
        (5, "5th ODI - ENG vs AUS", "ODI", "England", "Australia", 8, "2024-09-29", "Australia", "Field", "Australia", 49, "runs"),
        (2, "T20 WC Final 2024 - IND vs SA", "T20I", "India", "South Africa", 7, "2024-06-29", "India", "Bat", "India", 7, "runs"),
        (3, "1st ODI - SL vs IND", "ODI", "Sri Lanka", "India", 6, "2024-08-02", "Sri Lanka", "Bat", "Sri Lanka", 32, "runs"),
        (6, "Champions Trophy Group - PAK vs NZ", "ODI", "Pakistan", "New Zealand", 10, "2025-02-19", "Pakistan", "Field", "New Zealand", 60, "runs"),
        (6, "Champions Trophy Group - IND vs PAK", "ODI", "India", "Pakistan", 1, "2025-02-23", "Pakistan", "Bat", "India", 6, "wickets"),
    ]
    for s_id, desc, fmt, t1, t2, v_id, m_date, tw, td, wt, vm, vt in historical_specs:
        matches_data.append((s_id, desc, fmt, t1, t2, v_id, m_date, tw, td, wt, vm, vt, "Completed"))

    cursor.executemany(
        """INSERT INTO matches
        (series_id, match_description, cricket_format, team1_name, team2_name, venue_id,
         match_date, toss_winner, toss_decision, winning_team, victory_margin, victory_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
        matches_data,
    )

    random.seed(42)
    perf_rows = []
    quarters_timeline = [
        (2021, "2021-Q2", ["2021-04-10", "2021-05-12", "2021-05-20", "2021-06-05", "2021-06-18"]),
        (2022, "2022-Q3", ["2022-07-05", "2022-07-19", "2022-08-08", "2022-08-22", "2022-09-11"]),
        (2023, "2023-Q4", ["2023-10-08", "2023-10-14", "2023-10-22", "2023-11-05", "2023-11-19"]),
        (2024, "2024-Q1", ["2024-01-15", "2024-02-04", "2024-03-10"]),
        (2024, "2024-Q2", ["2024-04-12", "2024-05-18", "2024-06-20"]),
        (2024, "2024-Q3", ["2024-07-14", "2024-08-09", "2024-09-21"]),
        (2024, "2024-Q4", ["2024-10-11", "2024-11-15", "2024-12-19"]),
        (2025, "2025-Q1", ["2025-01-19", "2025-02-23", "2025-03-09"]),
        (2025, "2025-Q2", ["2025-04-15", "2025-05-21", "2025-06-25"]),
        (2025, "2025-Q3", ["2025-07-12", "2025-08-17", "2025-09-24"]),
        (2026, "2026-Q1", ["2026-01-18", "2026-02-14", "2026-03-12"]),
    ]

    tracked_batters = [
        (1, "India", 62),
        (2, "India", 54),
        (3, "India", 58),
        (4, "India", 46),
        (6, "India", 38),
        (11, "Australia", 52),
        (12, "Australia", 49),
        (16, "England", 55),
        (23, "Pakistan", 50),
    ]

    match_id_counter = 1
    for p_id, team_name, base_runs in tracked_batters:
        for q_idx, (yr, qtr, dates_list) in enumerate(quarters_timeline):
            for d_str in dates_list:
                m_id = ((match_id_counter - 1) % len(matches_data)) + 1
                v_id = ((m_id - 1) % 6) + 1
                trend_boost = (q_idx * 3) if p_id in (1, 3, 11) else (-q_idx * 2 if p_id == 23 else 0)
                runs = max(12, int(base_runs + trend_boost + random.randint(-18, 28)))
                balls = max(12, int(runs / random.uniform(0.85, 1.35)))
                sr = round((runs / balls) * 100, 2)
                perf_rows.append((
                    m_id, p_id, team_name, v_id, "ODI", d_str, yr, qtr,
                    runs, balls, sr, 0.0, 0, 0, 0.0, 1
                ))
                match_id_counter += 1

    tracked_bowlers = [
        (8, "India", 4.35, 2),
        (9, "India", 5.15, 2),
        (10, "India", 4.75, 2),
        (14, "Australia", 5.10, 2),
        (15, "Australia", 5.25, 2),
        (22, "South Africa", 4.95, 2),
        (24, "Pakistan", 5.30, 2),
        (7, "India", 4.65, 1),
    ]
    for p_id, team_name, base_econ, base_wkts in tracked_bowlers:
        for idx in range(12):
            m_id = (idx % len(matches_data)) + 1
            v_id = (idx % 3) + 1
            fmt = "ODI" if idx % 2 == 0 else "T20I"
            overs = 10.0 if fmt == "ODI" else 4.0
            econ = round(base_econ + random.uniform(-0.4, 0.5), 2)
            runs_conc = int(round(overs * econ))
            wkts = max(0, base_wkts + random.choice([-1, 0, 1, 2]))
            d_str = f"2025-0{(idx % 9) + 1}-15"
            perf_rows.append((
                m_id, p_id, team_name, v_id, fmt, d_str, 2025, "2025-Q2",
                8, 10, 80.0, overs, runs_conc, wkts, econ, 0
            ))

    cursor.executemany(
        """INSERT INTO match_performances
        (match_id, player_id, team_name, venue_id, cricket_format, match_date, match_year,
         match_quarter, runs_scored, balls_faced, strike_rate, overs_bowled, runs_conceded,
         wickets_taken, economy_rate, batted_in_match)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
        perf_rows,
    )

    partnerships_data = [
        (1, 1, 2, "Rohit Sharma", 1, 3, "Shubman Gill", 2, 142),
        (2, 1, 2, "Rohit Sharma", 1, 3, "Shubman Gill", 2, 118),
        (3, 1, 2, "Rohit Sharma", 1, 3, "Shubman Gill", 2, 84),
        (4, 1, 2, "Rohit Sharma", 1, 3, "Shubman Gill", 2, 65),
        (5, 1, 2, "Rohit Sharma", 1, 3, "Shubman Gill", 2, 42),
        (9, 1, 2, "Rohit Sharma", 1, 3, "Shubman Gill", 2, 165),
        (1, 1, 3, "Shubman Gill", 2, 1, "Virat Kohli", 3, 128),
        (2, 1, 3, "Shubman Gill", 2, 1, "Virat Kohli", 3, 96),
        (3, 1, 3, "Shubman Gill", 2, 1, "Virat Kohli", 3, 112),
        (5, 1, 3, "Shubman Gill", 2, 1, "Virat Kohli", 3, 58),
        (10, 1, 3, "Shubman Gill", 2, 1, "Virat Kohli", 3, 34),
        (11, 2, 3, "Shubman Gill", 2, 1, "Virat Kohli", 3, 134),
        (1, 1, 1, "Virat Kohli", 3, 4, "KL Rahul", 4, 155),
        (4, 2, 1, "Virat Kohli", 3, 4, "KL Rahul", 4, 108),
        (9, 1, 1, "Virat Kohli", 3, 4, "KL Rahul", 4, 74),
        (14, 1, 1, "Virat Kohli", 3, 4, "KL Rahul", 4, 62),
        (20, 2, 1, "Virat Kohli", 3, 4, "KL Rahul", 4, 29),
        (11, 1, 11, "Travis Head", 1, 12, "Steve Smith", 2, 138),
        (12, 1, 11, "Travis Head", 1, 12, "Steve Smith", 2, 88),
        (13, 2, 11, "Travis Head", 1, 12, "Steve Smith", 2, 119),
        (19, 1, 11, "Travis Head", 1, 12, "Steve Smith", 2, 54),
        (21, 1, 11, "Travis Head", 1, 12, "Steve Smith", 2, 41),
    ]
    cursor.executemany(
        """INSERT INTO partnerships
        (match_id, innings_number, player1_id, player1_name, player1_batting_pos,
         player2_id, player2_name, player2_batting_pos, partnership_runs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
        partnerships_data,
    )


def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        create_schema(cursor)
        seed_data(cursor)
        conn.commit()
        print(f"✅ Database initialized and seeded successfully at: {DB_PATH}")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"❌ Error seeding database: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()