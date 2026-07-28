# Agent Orchestration

## Purpose

Set up the agent orchestration plugins I've created in my personal GitHub account.

## Next steps

- [ ] Set up / wire in the agent orchestration plugins from my personal GitHub account.
- [ ] Look into **"ultracode"** from Claude.

## Ideas / TODO

- **Code review agent:** update it to run multiple code review processes as sub-agents (fan out the review across parallel sub-agents rather than a single pass).
- **Explainer skill:** add to its instructions that it should document any new endpoints the PR adds.

## Notes

- Qwen 3.6 MLX runs in OpenCode with `ollama run qwen3.6`. Better results achieved using a custom Modelfile: `FROM qwen3.6:35b-mlx` with `num_ctx 32768` (expand context for multi-file reading) and `temperature 0.2`.
