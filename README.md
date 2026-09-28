# DerbySoft GO plugins

Install DerbySoft GO certification workflows in **Codex** and **Claude Code** from a single GitHub repository.

- Marketplace: `derbysoft-go`
- Plugin: `derbysoft-connectivity-mcp`
- Version: `0.1.1`
- Capabilities: account context, certification progress, connection profiles, next steps, and source-based GO onboarding guidance.

This repository distributes a GO certification skill and a public MCP connection for both clients. **The MCP endpoint is bundled; each user must still provide their own GO API Token.** The plugin reads the token from the client process's `GO_TOKEN` environment variable and sends it in the `X-GO-Token` request header.

MCP service: [GO certification MCP](https://open.travelterminal.derbysoft-test.com/mcp). This is a test environment endpoint. The repository contains no real tokens or legacy server binaries.

This is a custom marketplace distributed through GitHub. It does not imply a listing in the official OpenAI or Anthropic public directories.

## Install in Codex

Use a Codex version that supports `codex plugin`. Run these commands in your terminal:

```sh
codex plugin marketplace add https://github.com/raphaelrong-derbysoft/derbysoft-go-mcp.git
codex plugin add derbysoft-connectivity-mcp@derbysoft-go
```

Return to Codex and start a new task to use the plugin. If you already have the older `derbysoft-connectivity-mcp@personal` plugin installed, confirm that the version from the new marketplace is installed before disabling the old version in the plugin interface to avoid duplicate loading. Preserve your existing `go-certification` MCP connection.

## Install in Claude Code

Run these commands in a Claude Code conversation:

```text
/plugin marketplace add raphaelrong-derbysoft/derbysoft-go-mcp
/plugin install derbysoft-connectivity-mcp@derbysoft-go
```

Alternatively, run these commands in your terminal:

```sh
claude plugin marketplace add raphaelrong-derbysoft/derbysoft-go-mcp
claude plugin install derbysoft-connectivity-mcp@derbysoft-go
```

Start a new session, then describe your GO question or invoke `/derbysoft-connectivity-mcp:go-concept-retrieval`.

## First connection and usage

Follow the [connection setup guide](plugins/derbysoft-connectivity-mcp/skills/go-concept-retrieval/references/connection-setup.md) to provide `GO_TOKEN` in the environment used to launch your client, then start a new session. You do not need to enter the MCP endpoint. Obtain your token from the GO service administrator; installing the plugin does not grant account access. If you already have a separately authenticated connection, you can continue using it. The plugin connection does not automatically inherit that connection's request headers.

Example prompts:

- "Check my GO certification progress and explain the next steps."
- "Show my GO connection profile."
- "Based on my current certification status, explain which requirements I still need to meet."

The skill calls `get_my_context` first, then queries `get_run_status` or `get_connection_profile` when needed. Status questions do not trigger certification submissions. Certification actions follow the service's declared capabilities and confirmation requirements.

## Update

In Codex, refresh the marketplace and reinstall the plugin to get the new version:

```sh
codex plugin marketplace upgrade derbysoft-go
codex plugin add derbysoft-connectivity-mcp@derbysoft-go
```

In Claude Code:

```sh
claude plugin marketplace update derbysoft-go
claude plugin update derbysoft-connectivity-mcp@derbysoft-go
```

Start a new session after updating.

## Repository structure and maintenance

```text
.agents/plugins/marketplace.json          Codex marketplace index
.claude-plugin/marketplace.json           Claude Code marketplace index
plugins/derbysoft-connectivity-mcp/
  .codex-plugin/plugin.json               Codex plugin manifest
  .claude-plugin/plugin.json              Claude Code plugin manifest
  .mcp.json                               Claude MCP configuration and environment-based headers
  skills/go-concept-retrieval/            Shared certification skill and connection setup guide
scripts/validate.py                      Marketplace and plugin validation (Python 3)
```

When updating the shared skill, increment the version in both plugin manifests together. Validate the changes before pushing them to GitHub:

```sh
python3 scripts/validate.py
claude plugin validate .
claude plugin validate plugins/derbysoft-connectivity-mcp
```

The Codex manifest's `mcpServers` configuration uses `env_http_headers`; Claude's `.mcp.json` uses `${GO_TOKEN}`. Both configurations connect to the same endpoint and read the same environment variable using each client's supported syntax.

The repository's automated checks validate marketplace entries, file paths, version consistency, MCP endpoints, token references, and package boundaries. Actual account connectivity must be verified in a client with access to the GO service.

References: [OpenAI plugins and marketplaces](https://developers.openai.com/plugins/build/plugins), [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

## License

[Apache-2.0](LICENSE)
