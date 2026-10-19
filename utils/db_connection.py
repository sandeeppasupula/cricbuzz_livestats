"""
Centralized SQL Database Connection & Query Execution Module.
Handles SQLite connections, custom aggregate functions (STDDEV),
SELECT queries (returning Pandas DataFrames), and CRUD transactions.
"""

import os
import sqlite3
import math
import pandas as pd
import streamlit as st

# Dynamically compute the absolute path to 'cricbuzz.db' in the root folder
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cricbuzz.db")


class StdevFunc:
    """
    Custom SQLite aggregate class to calculate Standard Deviation: STDDEV(column).
    Needed for Advanced SQL Questions 19 and 23 (Player Consistency Analysis).
    """
    def __init__(self):
        self.values = []

    def step(self, value):
        if value is not None:
            self.values.append(float(value))

    def finalize(self):
        n = len(self.values)
        if n < 2:
            return 0.0
        mean = sum(self.values) / n
        variance = sum((x - mean) ** 2 for x in self.values) / (n - 1)
        return round(math.sqrt(variance), 2)


def get_db_connection():
    """
    Establishes a connection to the SQLite database and registers STDDEV().
    """
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.create_aggregate("STDDEV", 1, StdevFunc)
        return conn
    except sqlite3.Error as e:
        st.error(f"Database Connection Error: {e}")
        return None


def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """
    Executes a READ (SELECT) SQL query and returns the result as a Pandas DataFrame.
    """
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"SQL Query Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def execute_crud(query: str, params: tuple = ()) -> tuple[bool, str]:
    """
    Executes a WRITE (INSERT, UPDATE, DELETE) SQL statement.
    """
    conn = get_db_connection()
    if conn is None:
        return False, "Could not connect to the database."
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount
        return True, f"Success! {affected} record(s) updated."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Database Error: {e}"
    finally:
        conn.close()