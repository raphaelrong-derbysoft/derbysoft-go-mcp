# Connect the GO certification MCP

The plugin connects to **https://open.travelterminal.derbysoft-test.com/mcp** (the GO test environment). Ask the GO service administrator for your own GO API key. Installing the plugin does not grant account access.

Each user keeps their own credentials in their client. Never put a real key in this repository, an installed plugin file, a project configuration committed to Git, or a chat message.

## Codex: configure your API key in Codex

The recommended setup stores the key in your user-level Codex MCP configuration. It does not require a `GO_TOKEN` environment variable or an operating-system-specific credential helper.

1. Install `derbysoft-connectivity-mcp@derbysoft-go`.
2. Open your user-level Codex configuration file, `~/.codex/config.toml` (or `config.toml` inside your custom Codex home directory). If your Codex client exposes custom HTTP header fields under **Settings > MCP servers**, you can enter the same values there.
3. Add the following server section, replacing the placeholder with your personal key **locally**. If `[mcp_servers.go-certification]` already exists, edit that section rather than adding a duplicate. Keep an existing working authentication setup unless you intend to change it.

```toml
[mcp_servers.go-certification]
url = "https://open.travelterminal.derbysoft-test.com/mcp"
enabled = true
http_headers = { "X-GO-Token" = "YOUR_GO_API_KEY" }
```

Use the exact name `go-certification`. A user-defined server with this name takes precedence over the plugin's bundled server definition. Include the URL as shown; do not rely on the user configuration being merged field by field with the plugin definition.

If you are migrating this same section from environment-based authentication, remove its `env_http_headers` mapping for `X-GO-Token` after adding the direct `http_headers` value. This avoids configuring two sources for the same header. The key is sent as `X-GO-Token`, without a `Bearer ` prefix.

The direct header value is stored as plaintext in your local Codex configuration. Keep that file private. Plugin upgrades do not overwrite it, and each user's configuration stays separate from the distributed plugin.

### Apply the configuration

Save the file, then use the MCP reload or restart control available in your Codex client and follow any restart prompt. Start a new task after installing or updating the plugin so the updated skill can load. Client versions differ; do not assume that the MCP list or an existing task refreshes automatically.

This setup avoids restarting solely to inherit a changed environment variable. It does not promise that every desktop client can apply every MCP change without restarting. The plugin does not automatically display an API-key form during installation, and this connection uses an API key rather than an OAuth sign-in.

To rotate your key, replace the local `X-GO-Token` value and reload the MCP connection. To stop using a direct key, remove that header value from your personal configuration.

### Optional: retain environment-based authentication

Existing Codex users who already supply `GO_TOKEN` can keep that setup. The bundled server definition still supports it. An explicit user-level configuration for this alternative is:

```toml
[mcp_servers.go-certification]
url = "https://open.travelterminal.derbysoft-test.com/mcp"
enabled = true
env_http_headers = { "X-GO-Token" = "GO_TOKEN" }
```

Choose one of the two configurations above; do not add both sections. Environment variables are read from the client process. Setting one in another terminal or using `launchctl setenv` does not update an already running client's environment. Restart that client from an environment containing the new value; opening a new task alone does not ensure that it receives the new value.

## Claude Code: provide GO_TOKEN

Claude Code uses the plugin's `.mcp.json`, with `headers: {"X-GO-Token": "${GO_TOKEN}"}`. Supply `GO_TOKEN` before launching Claude Code.

For a temporary terminal session on macOS/Linux, use a hidden prompt in **bash**:

```bash
read -r -s -p 'GO API Token: ' GO_TOKEN
printf '\n'
export GO_TOKEN
claude
# After the client exits:
unset GO_TOKEN
```

For PowerShell 7:

```powershell
$env:GO_TOKEN = Read-Host 'GO API Token' -MaskInput
claude
# After the client exits:
Remove-Item Env:GO_TOKEN
```

Use `/mcp` to inspect the connection status. Do not edit the installed plugin to insert a token: upgrades replace its files.

## Verify account access

In Codex, `codex mcp get go-certification` shows the effective configuration with header values masked. A direct-key setup should show `http_headers: X-GO-Token=*****`; it does not need `env_http_headers`. This confirms configuration, not whether the key is valid.

Start a new task or session and ask: "Check my GO certification status and next steps." The client should discover and call `get_my_context`. A successful call confirms account access. `initialize` and `tools/list` work without a token, so seeing the tools alone does not prove authentication.

- Missing `X-GO-Token`: check the effective configuration and reload the connection.
- Rejected key: verify or replace the key locally with one issued for this GO environment.
- Network failure: check access to the MCP endpoint separately from authentication.
- Existing working connection: reuse it; do not request a new key just because a separate connection fails.

Do not initiate certification mutations to test installation.

References: [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Claude Code MCP configuration](https://code.claude.com/docs/en/mcp).
