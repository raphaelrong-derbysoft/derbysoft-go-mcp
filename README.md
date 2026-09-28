# DerbySoft GO plugins

通过一个 GitHub 仓库，在 **Codex** 和 **Claude Code** 中安装 DerbySoft GO 认证工作流。

- Marketplace：`derbysoft-go`
- Plugin：`derbysoft-connectivity-mcp`
- 版本：`0.1.1`
- 能力：账号上下文、认证进度、连接配置、认证下一步及基于来源的 GO 接入指导。

本仓库分发 GO 认证 Skill 与公网 MCP 连接，兼容两种客户端。**MCP 地址已内置；每位用户仍需提供自己的 GO API Token。** 插件从客户端进程的 `GO_TOKEN` 环境变量读取令牌，并发送为 `X-GO-Token` 请求头。

MCP 服务：[https://open.travelterminal.derbysoft-test.com/mcp](https://open.travelterminal.derbysoft-test.com/mcp)。这是测试环境地址。仓库不包含真实令牌或旧版服务器二进制。

这是 GitHub 自建 Marketplace 分发，不表示已经进入 OpenAI 或 Anthropic 官方公共目录。

## 在 Codex 安装

需要支持 `codex plugin` 的 Codex 版本。在终端执行：

```sh
codex plugin marketplace add https://github.com/raphaelrong-derbysoft/derbysoft-go-mcp.git
codex plugin add derbysoft-connectivity-mcp@derbysoft-go
```

回到 Codex，开启新任务后使用。如果已经安装旧的 `derbysoft-connectivity-mcp@personal`，先确认新市场版本已安装，再在插件界面禁用旧版本，避免重复加载；保留原有 `go-certification` MCP 连接。

## 在 Claude Code 安装

在 Claude Code 对话中执行：

```text
/plugin marketplace add raphaelrong-derbysoft/derbysoft-go-mcp
/plugin install derbysoft-connectivity-mcp@derbysoft-go
```

或者在终端执行：

```sh
claude plugin marketplace add raphaelrong-derbysoft/derbysoft-go-mcp
claude plugin install derbysoft-connectivity-mcp@derbysoft-go
```

重新开启会话后，直接描述 GO 问题，或调用 `/derbysoft-connectivity-mcp:go-concept-retrieval`。

## 首次连接与使用

按 [连接说明](plugins/derbysoft-connectivity-mcp/skills/go-concept-retrieval/references/connection-setup.md) 向启动客户端的环境提供 `GO_TOKEN`，然后开启新会话。MCP 地址无需填写。令牌由 GO 服务管理员提供，插件安装不授予账号访问权。已有独立认证连接的用户可以继续复用；插件连接不会自动继承它的请求头。

可以询问：

- “检查我的 GO 认证进度，并说明下一步。”
- “展示我的 GO connection profile。”
- “根据当前认证状态，解释我还缺哪些条件。”

Skill 会先读取 `get_my_context`，需要时查询 `get_run_status` 或 `get_connection_profile`。仅询问状态不会触发认证提交；执行认证操作时遵循服务的能力声明与确认要求。

## 更新

Codex 刷新市场后重新安装该插件以拉取新版本：

```sh
codex plugin marketplace upgrade derbysoft-go
codex plugin add derbysoft-connectivity-mcp@derbysoft-go
```

Claude Code：

```sh
claude plugin marketplace update derbysoft-go
claude plugin update derbysoft-connectivity-mcp@derbysoft-go
```

更新后开启新会话。

## 目录与维护

```text
.agents/plugins/marketplace.json          Codex 市场索引
.claude-plugin/marketplace.json           Claude Code 市场索引
plugins/derbysoft-connectivity-mcp/
  .codex-plugin/plugin.json               Codex 插件清单
  .claude-plugin/plugin.json              Claude Code 插件清单
  .mcp.json                               Claude MCP 与环境变量请求头
  skills/go-concept-retrieval/            两端共享的认证 Skill 和配置说明
scripts/validate.py                      市场及插件文件检查（Python 3）
```

维护时修改共享 Skill，并同步增加两份插件清单中的版本号。验证后将改动推送到 GitHub：

```sh
python3 scripts/validate.py
claude plugin validate .
claude plugin validate plugins/derbysoft-connectivity-mcp
```

Codex 清单中的 `mcpServers` 使用 `env_http_headers`；Claude 的 `.mcp.json` 使用 `${GO_TOKEN}`。两份配置连接相同地址，按客户端各自支持的语法读取同一环境变量。

仓库内的自动检查会检查市场条目、文件路径、版本一致性、MCP 地址与令牌引用及安装包边界。实际账号连通性需要在具备 GO 服务访问权限的客户端中验证。

参考：[OpenAI 插件与 Marketplace](https://developers.openai.com/plugins/build/plugins)、[Claude Code Marketplace](https://code.claude.com/docs/en/plugin-marketplaces)。

## License

[Apache-2.0](LICENSE)
