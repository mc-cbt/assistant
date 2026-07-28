#!/usr/bin/env python3
"""Pull metadata about pull requests in andavo-dev/andavo and store it in a
SQLite database (analytics.db) next to this script.

By default it pulls *merged* PRs over a time period. Pass --state open to pull
the currently-open PRs instead (handy for the open-PR / age dashboard).

Authentication is handled by the GitHub CLI (`gh`), which must be installed and
logged in (`gh auth status`). No tokens are read or stored by this script.

Examples:
    # PRs merged in May 2026
    python3 pull_pr_metadata.py --start 2026-05-01 --end 2026-05-31

    # Everything merged on or after a date
    python3 pull_pr_metadata.py --start 2026-06-01

    # All currently-open PRs (for the open-PR dashboard)
    python3 pull_pr_metadata.py --state open

    # A different repo / db location
    python3 pull_pr_metadata.py --start 2026-01-01 --repo owner/name --db /tmp/out.db
"""

import argparse
import datetime as dt
import json
import os
import shutil
import sqlite3
import subprocess
import sys

DEFAULT_REPO = "andavo-dev/andavo"
DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics.db")

# Fields requested from `gh pr list --json`. Keep in sync with the table schema.
PR_FIELDS = [
    "number", "title", "state", "author", "url",
    "createdAt", "mergedAt", "closedAt", "updatedAt",
    "baseRefName", "headRefName", "mergeCommit",
    "additions", "deletions", "changedFiles",
    "isDraft", "labels",
]


def valid_date(s):
    """Validate a YYYY-MM-DD argument."""
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d").date().isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not a valid date (expected YYYY-MM-DD): {s!r}")


# The date qualifier each state filters on. Open PRs aren't merged, so a
# date bound there applies to when the PR was created.
DATE_QUALIFIER = {"merged": "merged", "open": "created", "closed": "closed"}


def build_search_query(start, end, state):
    """Build the date search qualifier from start/end dates for the given state."""
    field = DATE_QUALIFIER.get(state, "created")
    if start and end:
        return f"{field}:{start}..{end}"
    if start:
        return f"{field}:>={start}"
    if end:
        return f"{field}:<={end}"
    return None  # no date bound -> all PRs in this state


def fetch_prs(repo, start, end, limit, state):
    """Return a list of PR dicts for the given state via the gh CLI."""
    if shutil.which("gh") is None:
        sys.exit("error: the GitHub CLI ('gh') is not installed or not on PATH.")

    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--state", state,
        "--limit", str(limit),
        "--json", ",".join(PR_FIELDS),
    ]
    query = build_search_query(start, end, state)
    if query:
        cmd += ["--search", query]

    print(f"Fetching {state} PRs from {repo} ({query or 'all time'})...", file=sys.stderr)
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("error: 'gh' not found on PATH.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"error: gh failed (exit {e.returncode}):\n{e.stderr.strip()}")

    prs = json.loads(result.stdout or "[]")
    if len(prs) >= limit:
        print(
            f"warning: hit the --limit of {limit}; results may be truncated. "
            "Re-run with a larger --limit or a narrower date range.",
            file=sys.stderr,
        )
    return prs


def init_db(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS pull_requests (
            number       INTEGER PRIMARY KEY,
            title        TEXT,
            state        TEXT,
            author_login TEXT,
            author_name  TEXT,
            url          TEXT,
            created_at   TEXT,
            merged_at    TEXT,
            closed_at    TEXT,
            updated_at   TEXT,
            base_ref     TEXT,
            head_ref     TEXT,
            merge_commit TEXT,
            additions    INTEGER,
            deletions    INTEGER,
            changed_files INTEGER,
            is_draft     INTEGER,
            labels       TEXT,           -- comma-separated, for convenience
            fetched_at   TEXT
        );

        -- Normalized label rows for easy grouping/filtering.
        CREATE TABLE IF NOT EXISTS pr_labels (
            pr_number INTEGER NOT NULL,
            label     TEXT NOT NULL,
            PRIMARY KEY (pr_number, label),
            FOREIGN KEY (pr_number) REFERENCES pull_requests(number) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_pr_merged_at ON pull_requests(merged_at);
        CREATE INDEX IF NOT EXISTS idx_pr_author    ON pull_requests(author_login);
        CREATE INDEX IF NOT EXISTS idx_label        ON pr_labels(label);
        """
    )


def store_prs(conn, prs, repo):
    fetched_at = dt.datetime.now(dt.timezone.utc).isoformat()
    inserted = 0
    for pr in prs:
        author = pr.get("author") or {}
        merge_commit = pr.get("mergeCommit") or {}
        labels = [lb["name"] for lb in (pr.get("labels") or [])]
        row = (
            pr["number"],
            pr.get("title"),
            pr.get("state"),
            author.get("login"),
            author.get("name"),
            pr.get("url"),
            pr.get("createdAt"),
            pr.get("mergedAt"),
            pr.get("closedAt"),
            pr.get("updatedAt"),
            pr.get("baseRefName"),
            pr.get("headRefName"),
            merge_commit.get("oid"),
            pr.get("additions"),
            pr.get("deletions"),
            pr.get("changedFiles"),
            1 if pr.get("isDraft") else 0,
            ", ".join(labels),
            fetched_at,
        )
        conn.execute(
            """
            INSERT INTO pull_requests (
                number, title, state, author_login, author_name, url,
                created_at, merged_at, closed_at, updated_at,
                base_ref, head_ref, merge_commit,
                additions, deletions, changed_files, is_draft, labels, fetched_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(number) DO UPDATE SET
                title=excluded.title, state=excluded.state,
                author_login=excluded.author_login, author_name=excluded.author_name,
                url=excluded.url, created_at=excluded.created_at,
                merged_at=excluded.merged_at, closed_at=excluded.closed_at,
                updated_at=excluded.updated_at, base_ref=excluded.base_ref,
                head_ref=excluded.head_ref, merge_commit=excluded.merge_commit,
                additions=excluded.additions, deletions=excluded.deletions,
                changed_files=excluded.changed_files, is_draft=excluded.is_draft,
                labels=excluded.labels, fetched_at=excluded.fetched_at
            """,
            row,
        )
        # Refresh label rows for this PR.
        conn.execute("DELETE FROM pr_labels WHERE pr_number = ?", (pr["number"],))
        conn.executemany(
            "INSERT OR IGNORE INTO pr_labels (pr_number, label) VALUES (?, ?)",
            [(pr["number"], name) for name in labels],
        )
        inserted += 1
    conn.commit()
    return inserted


def reconcile_open(conn, prs):
    """Remove rows still marked OPEN that aren't in the freshly-fetched open set.

    Only safe when `prs` is the complete current open set (no date bound). Such
    rows have since merged/closed; deleting them keeps the open dashboard
    accurate, and a merged/closed run will re-capture them. Returns the count
    removed.
    """
    current = {pr["number"] for pr in prs}
    stale = [
        n for (n,) in conn.execute("SELECT number FROM pull_requests WHERE state = 'OPEN'")
        if n not in current
    ]
    conn.executemany("DELETE FROM pull_requests WHERE number = ?", [(n,) for n in stale])
    conn.commit()
    return len(stale)


def main():
    parser = argparse.ArgumentParser(
        description="Pull merged-PR metadata into a SQLite database.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--start", type=valid_date,
                        help="Start date (YYYY-MM-DD), inclusive, by merge date.")
    parser.add_argument("--end", type=valid_date,
                        help="End date (YYYY-MM-DD), inclusive, by merge date.")
    parser.add_argument("--state", choices=("merged", "open", "closed"),
                        default="merged",
                        help="Which PRs to fetch (default: merged). "
                             "Use 'open' for the open-PR / age dashboard.")
    parser.add_argument("--repo", default=DEFAULT_REPO,
                        help=f"owner/name repo (default: {DEFAULT_REPO}).")
    parser.add_argument("--db", default=DEFAULT_DB,
                        help=f"SQLite database path (default: {DEFAULT_DB}).")
    parser.add_argument("--limit", type=int, default=2000,
                        help="Max PRs to fetch (default: 2000).")
    args = parser.parse_args()

    if not args.start and not args.end:
        print(f"note: no --start/--end given; fetching ALL {args.state} PRs.",
              file=sys.stderr)

    prs = fetch_prs(args.repo, args.start, args.end, args.limit, args.state)

    conn = sqlite3.connect(args.db)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        init_db(conn)
        n = store_prs(conn, prs, args.repo)
        # When we pulled the complete open set (no date bound), reconcile: drop
        # rows still marked OPEN that GitHub no longer reports as open — they've
        # since merged or closed and will be re-captured by a merged/closed run.
        reconciled = 0
        if args.state == "open" and not args.start and not args.end:
            reconciled = reconcile_open(conn, prs)
    finally:
        conn.close()

    msg = f"Stored {n} {args.state} PR(s) into {args.db}"
    if args.state == "open" and not args.start and not args.end:
        msg += f" (dropped {reconciled} stale open row(s))"
    print(msg)


if __name__ == "__main__":
    main()
