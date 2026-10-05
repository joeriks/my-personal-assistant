# ChatGPT and Codex

Codex can work directly in a local clone, but a local clone is optional: it can also work with a remote connector when one is available and authorized. ChatGPT can use GitHub as a source, but it does not automatically read `AGENTS.md` and may not have the same access as Codex.

Start a new ChatGPT session with a clear request to read `AGENTS.md`, `README.md`, and your personal profile settings from the available repository or connector before it suggests or makes changes. For example:

> Before suggesting or making changes, read `AGENTS.md`, `README.md`, and my profile settings in the repository. Always read the latest version of the affected files before writing. Treat the files as the source of truth, capture new tasks in the inbox, and show one concrete next step.

Check each client's actual tools and permissions separately before relying on it to read or write files, GitHub Issues, or GitHub Projects. There is no guarantee that every client can write to each of these resources. A read-only client must not claim that it saved anything; ask it to provide content that can be applied in Codex instead.

Always read the latest version before writing, and refresh it again when needed. Keep the shared files as the source of truth; do not build a divergent memory that exists only in a chat.
