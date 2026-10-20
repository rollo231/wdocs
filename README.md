# wdocs

A Claude Code plugin for the Korean team documents I actually write at work. Claude follows these skills when it writes or updates a document; the shared checker keeps the plain-sentence style.

| Skill | Document | Answers |
|---|---|---|
| `wdocs-roadmap` | Roadmap page | Which workstreams, in what order, judged by what |
| `wdocs-poc` | PoC doc | Does this work? (hypothesis, success and kill criteria, live progress, verdict) |
| `wdocs-prd` | PRD | What to build and why |
| `wdocs-design` | Design Doc | How to build it (links the PRD, does not repeat it) |

Documents are written in Korean. `shared/style.md` holds the common style rules and `shared/check_style.py --kind <roadmap|poc|prd|design>` checks them.

## Install

```
/plugin marketplace add rollo231/wdocs
/plugin install wdocs@wdocs
```

## License

MIT
