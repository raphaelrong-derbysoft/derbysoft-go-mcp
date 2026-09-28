# DerbySoft GO plugins

Install DerbySoft GO certification workflows in **Codex** and **Claude Code** from a single GitHub repository.

- Marketplace: `derbysoft-go`
- Plugin: `derbysoft-connectivity-mcp`
- Version: `0.1.3`
- Capabilities: account context, certification progress, connection profiles, next steps, and source-based GO onboarding guidance.

This repository distributes a GO certification skill and a public MCP connection for both clients. **The MCP endpoint is bundled; each user configures their own GO API Token in their client.** For Codex, the `X-GO-Token` header name is preset with an empty value. Each user fills in only their own API key in their personal `go-certification` MCP configuration. No `GO_TOKEN` environment variable is required for that setup. Claude Code uses `GO_TOKEN`; Codex users can still choose an explicit environment-based personal configuration.

MCP service: [GO certification MCP](https://open.travelterminal.derbysoft-test.com/mcp). This is a test environment endpoint. The repository contains no real tokens or legacy server binaries.

This is a custom marketplace distributed through GitHub. It does not imply a listing in the official OpenAI or Anthropic public directories.

## Install in Codex

Use a Codex version that supports `codex plugin`. Run these commands in your terminal:

```sh
codex plugin marketplace add https://github.com/raphaelrong-derbysoft/derbysoft-go-mcp.git
codex plugin add derbysoft-connectivity-mcp@derbysoft-go
```

Return to Codex and start a new task to use the plugin. If you already have the older `derbysoft-connectivity-mcp@personal` plugin installed, confirm that the version from the new marketplace is installed before disabling the old version in the plugin interface to avoid duplicate loading. Preserve your existing `go-certification` MCP connection.

Before checking your account, follow [Configure your API key in Codex](plugins/derbysoft-connectivity-mcp/skills/go-concept-retrieval/references/connection-setup.md#codex-configure-your-api-key-in-codex). Each user saves their own key in their user-level Codex configuration. The shared plugin contains no user credentials, and plugin upgrades do not overwrite those personal settings.

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

Follow the [connection setup guide](plugins/derbysoft-connectivity-mcp/skills/go-concept-retrieval/references/connection-setup.md) for your client. Obtain your personal API key from the GO service administrator; installing the plugin does not grant account access. In Codex, use the exact server name `go-certification` for your user-level settings so they take precedence over the bundled server definition. If you already have a working connection, keep its credentials rather than creating a duplicate.

After saving your Codex settings, use the MCP reload or restart control available in your client and follow any restart prompt. Start a new task to pick up updated plugin skills. Saving a key in Codex configuration avoids the need to restart solely to inherit a new environment variable; it does not guarantee that every client version refreshes its tools without a restart. The plugin does not provide an automatic API-key prompt during installation.

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

The Codex manifest supplies `http_headers: {"X-GO-Token": ""}` so the header name is preset without distributing a credential. Each user's same-name `go-certification` configuration supplies the actual value and takes precedence over that bundled definition. Users upgrading from the bundled environment-based setup must use the explicit environment configuration in the connection guide if they want to keep using `GO_TOKEN`. Claude's `.mcp.json` uses `${GO_TOKEN}`. Both clients connect to the same endpoint and authenticate with the `X-GO-Token` header. Keep all real API keys out of distributed plugin files.

The repository's automated checks validate marketplace entries, file paths, version consistency, MCP endpoints, token references, and package boundaries. Actual account connectivity must be verified in a client with access to the GO service.

References: [OpenAI plugins and marketplaces](https://developers.openai.com/plugins/build/plugins), [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

## License

[Apache-2.0](LICENSE)
