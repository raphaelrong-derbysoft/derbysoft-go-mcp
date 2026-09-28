# Connect the GO certification MCP

The plugin connects to **https://open.travelterminal.derbysoft-test.com/mcp** (the GO test environment). The endpoint is already bundled. Ask the GO service administrator for your own GO API Token. Installing the plugin does not grant account access.

## Supply the token

Both clients read `GO_TOKEN` from their process environment and send it as the `X-GO-Token` HTTP header. Supply it through your private environment or secret manager before launching the client. Never paste a real token into chat or a checked-in file.

For a temporary terminal session on macOS/Linux, use a hidden prompt in **bash**:

```bash
read -r -s -p 'GO API Token: ' GO_TOKEN
printf '\n'
export GO_TOKEN
codex
# Or run claude instead of codex.
# After the client exits:
unset GO_TOKEN
```

For PowerShell 7:

```powershell
$env:GO_TOKEN = Read-Host 'GO API Token' -MaskInput
claude
# Or run codex instead of claude.
# After the client exits:
Remove-Item Env:GO_TOKEN
```

A variable exported in a terminal does not automatically reach an already running desktop app. For Codex desktop, make sure its launch environment contains `GO_TOKEN`, then restart the app. If the desktop app already has an authenticated `go-certification` connection in private settings, the skill can reuse it. Do not assume the plugin connection inherits that connection's headers, and do not ask for the token again just because the separate plugin connection is unauthenticated.

## How the two clients authenticate

- Codex uses the inline MCP configuration in `.codex-plugin/plugin.json`, with `env_http_headers: {"X-GO-Token": "GO_TOKEN"}`.
- Claude Code uses `.mcp.json`, with `headers: {"X-GO-Token": "${GO_TOKEN}"}`. Use `/mcp` to inspect the connection status.

Do not edit the installed plugin to insert a token: upgrades replace its files. Keep the token in the client process environment or retain an existing private connection.

## Existing Codex connection

If you already use a private `mcp_servers.go-certification` connection, preserve its authentication settings. If its old network address is no longer reachable, update only its `url` to the public endpoint. A private configuration that reads the token from the environment looks like:

```toml
[mcp_servers.go-certification]
url = "https://open.travelterminal.derbysoft-test.com/mcp"
enabled = true
env_http_headers = { "X-GO-Token" = "GO_TOKEN" }
```

This is an optional compatibility route, not a second connection required for new installations. A pre-existing private `http_headers` configuration may be retained; never display credential values.

## Check the result

Start a new session and ask: “Check my GO certification status and next steps.” The client should discover and call `get_my_context`. A successful call confirms account access. `initialize` and `tools/list` work without a token, so seeing the tools alone does not prove authentication. A missing-header error means that connection did not send `X-GO-Token`; a rejected token and a network failure require different fixes. Do not initiate certification mutations to test installation.

References: [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Claude Code MCP configuration](https://code.claude.com/docs/en/mcp).
