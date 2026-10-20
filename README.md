# wdocs

My personal Claude Code skills for the docs I write. Claude follows them when it writes or updates a document.

| Skill | Document | Answers |
|---|---|---|
| `wdocs-roadmap` | Roadmap page | Which workstreams, in what order, judged by what |
| `wdocs-poc` | PoC doc | Does this work? (hypothesis, success and kill criteria, live progress, verdict) |
| `wdocs-prd` | PRD | What to build and why |
| `wdocs-design` | Design Doc | How to build it (links the PRD, does not repeat it) |

The docs are in Korean. `shared/style.md` has the shared style rules, and `shared/check_style.py --kind <roadmap|poc|prd|design>` checks them.

## Install

```
/plugin marketplace add rollo231/wdocs
/plugin install wdocs@wdocs
```

## License

MIT
