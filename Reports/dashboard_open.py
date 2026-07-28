#!/usr/bin/env python3
"""Streamlit dashboard for currently-open PR metadata in analytics.db.

Run with:
    streamlit run dashboard_open.py

Populate / refresh the open-PR data first with:
    python3 pull_pr_metadata.py --state open

Focuses on how long PRs have been open (age) and their metadata:
  * Headline counts (open PRs, drafts, authors, median & oldest age)
  * Age distribution across buckets
  * Open PRs by author
  * Age vs. size scatter
  * A sortable, filterable table of every open PR
"""

import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics.db")

# Age buckets (in days) used for the distribution chart, longest last.
AGE_BINS = [0, 1, 3, 7, 14, 30, 60, 90, float("inf")]
AGE_LABELS = ["<1d", "1-3d", "3-7d", "1-2w", "2-4w", "1-2m", "2-3m", "3m+"]

st.set_page_config(page_title="Andavo Open PRs", layout="wide")


@st.cache_data
def load_data(db_path):
    """Load open PRs, with age (days) computed from created_at."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(
            """
            SELECT number, title, author_login, author_name, url,
                   created_at, updated_at, base_ref, head_ref,
                   additions, deletions, changed_files, is_draft, labels
            FROM pull_requests
            WHERE state = 'OPEN'
            """,
            conn,
        )

    now = pd.Timestamp.now(tz="UTC")
    for col in ("created_at", "updated_at"):
        df[col] = pd.to_datetime(df[col], utc=True, errors="coerce")
    for col in ("additions", "deletions", "changed_files"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["age_days"] = (now - df["created_at"]).dt.total_seconds() / 86400
    df["stale_days"] = (now - df["updated_at"]).dt.total_seconds() / 86400
    df["churn"] = df["additions"] + df["deletions"]
    df["is_draft"] = df["is_draft"].fillna(0).astype(bool)
    df["author"] = df["author_login"].fillna(df["author_name"]).fillna("unknown")
    df["labels"] = df["labels"].fillna("")
    df["age_bucket"] = pd.cut(df["age_days"], bins=AGE_BINS, labels=AGE_LABELS,
                              right=False, ordered=True)
    return df.sort_values("age_days", ascending=False)


# ── Load ────────────────────────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    st.error(f"Database not found at {DB_PATH}. Run pull_pr_metadata.py first.")
    st.stop()

df = load_data(DB_PATH)

st.title("Andavo Open PRs")
st.caption(
    f"Source: `{DB_PATH}` — refresh with "
    "`python3 pull_pr_metadata.py --state open`"
)

if df.empty:
    st.warning("No open PRs found. Run `python3 pull_pr_metadata.py --state open`.")
    st.stop()

# ── Filters ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    authors = sorted(df["author"].unique())
    picked = st.multiselect("Author", authors, default=[])
    draft_choice = st.radio("Drafts", ["All", "Exclude drafts", "Drafts only"], index=0)
    min_age = st.slider("Minimum age (days)", 0, int(df["age_days"].max()) + 1, 0)
    query = st.text_input("Title contains", "")

view = df.copy()
if picked:
    view = view[view["author"].isin(picked)]
if draft_choice == "Exclude drafts":
    view = view[~view["is_draft"]]
elif draft_choice == "Drafts only":
    view = view[view["is_draft"]]
view = view[view["age_days"] >= min_age]
if query:
    view = view[view["title"].str.contains(query, case=False, na=False)]

if view.empty:
    st.warning("No open PRs match the current filters.")
    st.stop()

# ── Headline metrics ──────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Open PRs", f"{len(view):,}")
m2.metric("Drafts", f"{int(view['is_draft'].sum()):,}")
m3.metric("Distinct authors", f"{view['author'].nunique():,}")
m4.metric("Median age", f"{view['age_days'].median():.0f} d")
m5.metric("Oldest", f"{view['age_days'].max():.0f} d")

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("Open PRs by age")
    counts = (
        view["age_bucket"].value_counts().reindex(AGE_LABELS, fill_value=0).reset_index()
    )
    counts.columns = ["age_bucket", "count"]
    fig = px.bar(counts, x="age_bucket", y="count",
                 labels={"age_bucket": "Age", "count": "Open PRs"})
    fig.update_xaxes(categoryorder="array", categoryarray=AGE_LABELS)
    st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Open PRs by author")
    by_author = (
        view.groupby("author").size().sort_values(ascending=False).head(20).reset_index()
    )
    by_author.columns = ["author", "count"]
    fig = px.bar(by_author, x="count", y="author", orientation="h",
                 labels={"author": "", "count": "Open PRs"})
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, width="stretch")

st.subheader("Age vs. size (bubble = files changed)")
fig = px.scatter(
    view, x="age_days", y="churn", size="changed_files", color="is_draft",
    hover_name="title",
    hover_data={"number": True, "author": True, "age_days": ":.1f", "churn": True},
    labels={"age_days": "Age (days)", "churn": "Lines changed (add+del)",
            "is_draft": "Draft"},
)
fig.update_layout(legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Table ─────────────────────────────────────────────────────────────────────
st.subheader("Open PRs")
table = view.assign(
    age_days=view["age_days"].round(1),
    stale_days=view["stale_days"].round(1),
)[
    ["number", "title", "author", "age_days", "stale_days", "is_draft",
     "additions", "deletions", "changed_files", "base_ref", "head_ref",
     "labels", "url"]
]
st.dataframe(
    table,
    width="stretch",
    hide_index=True,
    column_config={
        "number": st.column_config.NumberColumn("#", format="%d"),
        "title": "Title",
        "author": "Author",
        "age_days": st.column_config.NumberColumn("Age (d)", format="%.1f"),
        "stale_days": st.column_config.NumberColumn("Since update (d)", format="%.1f"),
        "is_draft": st.column_config.CheckboxColumn("Draft"),
        "additions": st.column_config.NumberColumn("+", format="%d"),
        "deletions": st.column_config.NumberColumn("−", format="%d"),
        "changed_files": st.column_config.NumberColumn("Files", format="%d"),
        "base_ref": "Base",
        "head_ref": "Head",
        "labels": "Labels",
        "url": st.column_config.LinkColumn("Link", display_text="open ↗"),
    },
)
