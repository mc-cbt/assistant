# AI Voice Agent

## Purpose

Investigate and build a **prototype voice AI system** that works with the **booking APIs in Andavo**.

## Current state

- Investigation phase. First use case scoped: **call in and ask about my current itinerary.**

## Notes

- [[Pipecat + Andavo Itinerary Setup]] — reference architecture and step-by-step setup for the itinerary lookup prototype (Pipecat ⇄ Andavo MCP server).

## Technical notes

- **Pipecat** (Python) is the orchestration layer: transport → STT → LLM (+tools) → TTS.
- Integrate via Andavo's existing **AiApi MCP server** (`/v1/mcp`, Julia) — Pipecat's `MCPClient` auto-registers its tools. The `get-user` tool (`userId="me"`) returns trip discovery, which is the itinerary use case.
- Biggest open question: how a **headless** voice agent gets a bearer token AiApi accepts (its OAuth2/Auth0 flow is browser-based). See the setup note §6.

## Next steps

- [ ] Confirm the sanctioned bearer-token path for a non-browser client.
- [ ] Confirm how to run `AiApi` locally; smoke-test `get-user(userId="me")` over `/v1/mcp`.
- [ ] Build the Daily/WebRTC prototype pipeline; demo "what's my next trip?".
