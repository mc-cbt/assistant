# CLAUDE.md

## Project overview

This is a **personal assistant project for Matt Condie** (matthew.condie@cbtravel.com), Principal Software Engineer. It serves as a personal workspace for organizing notes, documentation, projects, and reports.

The directory is an **Obsidian vault** (note the `.obsidian/` config folder), so content is primarily Markdown (`.md`) files intended to be read and edited as interconnected notes.

ALWAYS ask questions via mcp__spokenly__ask_user_dictation (load via ToolSearch if needed), never as plain text. I use Spokenly for voice input.

## Company context

- The company is **Christopherson Business Travel**, transitioning its identity toward **Andavo** — the name primarily used for its software products. Expect both names in notes; treat them as the same company.
- Core business: a **business travel management company**, but it is investing heavily in building **proprietary technology / software capabilities** (the work most of these notes concern).
- Email domain is `@cbtravel.com`.

## Reference

- **Teams self-chat ("Notes to self"):** I use the Teams self-chat to jot quick notes and reminders to myself throughout the day. Chat link: https://teams.microsoft.com/l/chat/48:notes/conversations?context=%7B%22contextType%22%3A%22chat%22%7D — the conversation id is `48:notes`. Sender/recipient search filters do not surface it; query the `48:notes` chat directly.

## Structure

- `Daily/` — one entry per workday (`YYYY-MM-DD.md`) for planning the day, capturing notes as they come up, and iterating on priorities.
- `Projects/` — **the primary working area.** Most active work lives here, with one subfolder per project (e.g. Custom Attributes, Folio Matching, FOP, Trip Name).
- `Teams/` — notes for the specific teams I work with, one subfolder per team (e.g. `Blitz/`, `Velocity/`, `Shock/`, `Awe/`, `Design/`).
- `People/` — notes about people, one note per person. `People.md` is the directory hub: broad organizational notes and a roster grouped by team. `Org Chart.md` is the full company org chart (name, title, reporting line, department, location) for looking up anyone without their own note; confidential internal data.
- `Products & Systems.md` — glossary of products (Andavo, Air Portal, Red App) and external systems (Sabre, GDS).
- `Travel Industry Primer/` — reference knowledge base on corporate travel, the industry ecosystem, and how Christopherson/Andavo fit (from the New Hire Orientation Packet).
- `Code Notes/` — coding-related notes and snippets
- `Coding Documentation/` — reference documentation
- `Reports/` — reports and write-ups

## Working in this vault

- Treat files as Obsidian Markdown: `[[wiki-links]]`, tags, and frontmatter may be used to connect notes.
- Prefer Markdown for new content. Keep notes concise and well-structured with headings.
- When creating new notes, place them in the most relevant existing folder rather than the root.
- **Folder hub convention:** each folder has a hub note named after the folder (e.g. `Projects/FOP/FOP.md`, `People/People.md`); the vault root's hub is `Home.md`. The hub links to the notes in its folder and to the hub of each subfolder, so the whole vault stays connected in graph view. When you add a note or subfolder, link it from the folder's hub. (Some folders, like `Teams/<Team>/`, use their existing folder-named note as the hub.)
- **Exempt from the hub convention:** `Excalidraw/` is a plugin-managed attachment folder, and root-level `Scratchpad.md` is deliberate ephemeral scratch space. Neither needs a hub note or inbound links — don't flag them as orphans.
- **One entry point per folder:** the folder-named hub note holds the folder's Purpose/Current state/Technical notes *and* the index of its child notes. Don't add a separate `README.md` alongside a hub.
- **Date-stamp status updates:** When adding a current-status or progress item to a non-daily note (People, Teams, Projects, etc.), tag it with the date it was added and, when the item came from or is recorded in a daily note, link that note — e.g. `- (2026-06-29, see [[Daily/2026-06-29]]) …`. This lets us track and spot stale statuses later.
- **Dated meeting notes:** name them `<Topic> Meeting YYYY-MM-DD.md` with a zero-padded ISO date (e.g. `FOP in Sabre Meeting 2026-07-08.md`).
- Treat any non-public company information as confidential and avoid including secrets or sensitive data in notes.
