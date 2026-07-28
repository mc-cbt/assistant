#!/usr/bin/env python3
"""Streamlit dashboard for merged-PR metadata in analytics.db.

Run with:
    streamlit run dashboard.py

Charts (all bucketed over time by merge date):
  * Number of merges
  * Number of distinct authors (author_login)
  * Total additions and deletions
  * Average additions and deletions per PR
"""

import os
import sqlite3

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics.db")

# Pandas resample rules for each granularity label.
FREQ = {"Day": "D", "Week": "W-MON", "Month": "MS"}

st.set_page_config(page_title="Andavo PR Analytics", layout="wide")


@st.cache_data
def load_data(db_path):
    """Load merged PRs, parsed and sorted by merge date."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(
            """
            SELECT number, author_login, merged_at, additions, deletions
            FROM pull_requests
            WHERE merged_at IS NOT NULL
            """,
            conn,
        )
    df["merged_at"] = pd.to_datetime(df["merged_at"], utc=True, errors="coerce")
    df = df.dropna(subset=["merged_at"]).sort_values("merged_at")
    for col in ("additions", "deletions"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


def bucket(df, freq):
    """Aggregate per time bucket. Returns a frame indexed by period start."""
    indexed = df.set_index("merged_at")
    out = indexed.resample(freq).agg(
        merges=("number", "count"),
        authors=("author_login", "nunique"),
        additions=("additions", "sum"),
        deletions=("deletions", "sum"),
    )
    out["avg_additions"] = (out["additions"] / out["merges"]).fillna(0)
    out["avg_deletions"] = (out["deletions"] / out["merges"]).fillna(0)

    # PRs per author within each bucket -> max and average across authors.
    per_author = indexed.groupby([pd.Grouper(freq=freq), "author_login"]).size()
    stats = per_author.groupby(level=0).agg(
        max_prs_per_author="max", avg_prs_per_author="mean"
    )
    out = out.join(stats)
    out[["max_prs_per_author", "avg_prs_per_author"]] = (
        out[["max_prs_per_author", "avg_prs_per_author"]].fillna(0)
    )
    return out.reset_index()


# ── Load ────────────────────────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    st.error(f"Database not found at {DB_PATH}. Run pull_pr_metadata.py first.")
    st.stop()

df = load_data(DB_PATH)
if df.empty:
    st.warning("No merged PRs found in the database.")
    st.stop()

# ── Controls ──────────────────────────────────────────────────────────────────
st.title("Andavo PR Analytics")
st.caption(f"Source: `{DB_PATH}`")

min_date = df["merged_at"].min().date()
max_date = df["merged_at"].max().date()

c1, c2 = st.columns([1, 2])
with c1:
    gran = st.radio("Bucket by", list(FREQ), index=1, horizontal=True)
with c2:
    date_range = st.date_input(
        "Merge date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

# date_input returns a single date until both ends are picked.
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    mask = (df["merged_at"].dt.date >= start) & (df["merged_at"].dt.date <= end)
    df = df.loc[mask]

if df.empty:
    st.warning("No PRs in the selected date range.")
    st.stop()

agg = bucket(df, FREQ[gran])

# ── Headline metrics ──────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Merged PRs", f"{len(df):,}")
m2.metric("Distinct authors", f"{df['author_login'].nunique():,}")
m3.metric("Total additions", f"{int(df['additions'].sum()):,}")
m4.metric("Total deletions", f"{int(df['deletions'].sum()):,}")

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("Merges over time")
    fig = px.bar(agg, x="merged_at", y="merges", labels={"merged_at": "", "merges": "Merged PRs"})
    st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Distinct authors over time")
    fig = px.line(agg, x="merged_at", y="authors", markers=True,
                  labels={"merged_at": "", "authors": "Authors"})
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, width="stretch")

left, right = st.columns(2)

with left:
    st.subheader("Additions & deletions over time")
    fig = go.Figure()
    fig.add_bar(x=agg["merged_at"], y=agg["additions"], name="Additions",
                marker_color="#2ca02c")
    fig.add_bar(x=agg["merged_at"], y=agg["deletions"], name="Deletions",
                marker_color="#d62728")
    fig.update_layout(barmode="group", xaxis_title="", yaxis_title="Lines",
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Avg additions & deletions per PR over time")
    fig = go.Figure()
    fig.add_scatter(x=agg["merged_at"], y=agg["avg_additions"], mode="lines+markers",
                    name="Avg additions", line=dict(color="#2ca02c"))
    fig.add_scatter(x=agg["merged_at"], y=agg["avg_deletions"], mode="lines+markers",
                    name="Avg deletions", line=dict(color="#d62728"))
    fig.update_layout(xaxis_title="", yaxis_title="Lines per PR",
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, width="stretch")

left, right = st.columns(2)

with left:
    st.subheader("Max & avg PRs per author over time")
    fig = go.Figure()
    fig.add_scatter(x=agg["merged_at"], y=agg["max_prs_per_author"], mode="lines+markers",
                    name="Max PRs/author", line=dict(color="#1f77b4"))
    fig.add_scatter(x=agg["merged_at"], y=agg["avg_prs_per_author"], mode="lines+markers",
                    name="Avg PRs/author", line=dict(color="#ff7f0e"))
    fig.update_layout(xaxis_title="", yaxis_title="PRs per author",
                      legend=dict(orientation="h", y=1.1))
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, width="stretch")

with st.expander("Show aggregated data"):
    st.dataframe(agg, width="stretch")
