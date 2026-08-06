# Folio Matching

**Team:** [[Blitz]]

## Purpose

Automatically match **folios** (essentially receipts from hotel stays) to their corresponding **expense records** in Andavo, replacing the current manual matching process.

## Current state

- A user manually matches uploaded folios to a trip.
- **Colter** built a manual folio upload flow.
- PDFs are parsed and a row is created in the DB, then matched to a trip.

## Technical notes

- **LlamaParse** — converts PDF → Markdown so LLMs can work with folio contents.
- **Temporal** — currently disabled.
- **Dispi** — Python AI library under consideration.

## Notes

- [[Projects/Folio Matching/Notes from meeting with Ricky|Notes from meeting with Ricky]] — raw meeting notes
