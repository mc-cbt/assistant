# Embedded Reports

## Purpose

Embed analytics pages from **Domo** directly into the Andavo admin app, so users can view reporting/dashboards without leaving Andavo.

## Current state

- Embedding has been implemented.
- I need to review the code that handles the embedding to make sure it was done correctly.

## Technical notes

- **Domo** — external analytics/BI platform providing the embedded analytics pages.
- Target: the Andavo **admin app**.
- Review focus: verify the embedding is implemented correctly (e.g. authentication/token handling, secure embed approach, correct scoping of data shown).
