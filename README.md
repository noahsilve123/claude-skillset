# claude-skillset (Gurta Agent Skillset)

A Gamut-compatible skillset (`index.json` at root) for the Gurta project agents.

**Add to a Gamut agent:** Settings -> Skillsets -> paste
`https://github.com/noahsilve123/claude-skillset`, then toggle the skills each agent needs.

## What's inside (37 skills)

| Group | Skills | Best for |
|-------|--------|----------|
| Gurta | `gurta-context` | Every Gurta agent (repo map, API, holdout + safety rules) |
| Orchestration | `dispatching-parallel-agents`, `writing-plans`, `executing-plans`, `brainstorming`, `subagent-driven-development`, `requesting-code-review`, `verification-before-completion` | Manager / Orchestrator |
| Engineering | `systematic-debugging`, `test-driven-development`, `pytest-skill`, `vitest-skill` | Research, UI, RAG |
| Browser / scraping | `playwright-skill`, `puppeteer-skill`, `webapp-testing`, `firecrawl-build-interact`, `firecrawl-build-scrape`, `firecrawl-build-search`, `firecrawl-research-index` | API Key Factory, Research |
| Data / RAG | `huggingface-datasets`, `train-sentence-transformers` | RAG Verifier |
| Frontend / design | `frontend-design`, `web-artifacts-builder`, `theme-factory`, `canvas-design`, `algorithmic-art` | UI Overhaul |
| Docs | `pdf`, `docx`, `xlsx`, `pptx`, `doc-coauthoring`, `internal-comms` | Reports, briefs |
| Meta | `mcp-builder`, `skill-creator`, `claude-api`, `brand-guidelines`, `slack-gif-creator` | Tooling |

## Sources

Official Anthropic skills (`github.com/anthropics/skills`) plus community skills from
`obra/superpowers`, `LambdaTest/agent-skills`, `firecrawl/skills`, and `huggingface/skills`,
each keeping its original `SKILL.md`. The `gurta-context` skill is custom.

## Regenerate the manifest

After adding/removing a skill folder under `skills/`, run:

```bash
python build_index.py
```

`index.json` is generated from each skill's `SKILL.md` frontmatter. Do not edit it by hand.
