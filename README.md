# mux-extensions

Extensions for [Mux-Swarm](https://github.com/jnotsknab/mux-swarm). Each folder under `extensions/` is a drop-in extension.

## Install

Copy a folder into your Mux install's `Extensions/` directory and run `/extensions` (or `/refresh`).
Extensions that run a process (`cusage`, `meter`, `notes`) must be trusted first: `/extensions trust <name>`.

## Extensions

| Name | Type | What it does |
|---|---|---|
| `hearth` | theme | Ember-palette rounded outline UI: boxed input, full status line, themed prompts, panels, animations |
| `ember` | theme | Warm theme that restyles every TUI region (demo) |
| `crt` | theme | Green-phosphor terminal look (demo) |
| `bubble` | theme | Chat-bubble input with a status strip (demo) |
| `cusage` | process | Footer chip with live Claude subscription usage (5h / 7d). Reads the local CLIProxy Claude auth file at runtime; nothing is stored here. Add `{cusage.q}` to your active theme's `footer.template` |
| `meter` | process | Docked panel demo: `/meter side\|band\|auto\|screen` |
| `notes` | process | Full-screen panel demo: `/notes` |

Review any extension before trusting it: process extensions run code on your machine.
