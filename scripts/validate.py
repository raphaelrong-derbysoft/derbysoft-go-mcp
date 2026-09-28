#!/usr/bin/env python3
"""Validate the distributable catalogs without credentials or network access."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def component(root, path):
    require(isinstance(path, str) and path.startswith("./"), "Expected a ./ relative path")
    resolved = (root / path).resolve()
    require(root.resolve() in resolved.parents, "Component escapes its root")
    require(resolved.exists(), f"Missing component: {path}")
    return resolved


def main():
    codex = read_json(ROOT / ".agents/plugins/marketplace.json")
    claude = read_json(ROOT / ".claude-plugin/marketplace.json")
    require(codex["name"] == claude["name"], "Marketplace names differ")
    require(bool(claude["owner"]["name"]), "Claude marketplace needs an owner")
    require(codex["plugins"] and claude["plugins"], "Marketplace is empty")
    codex_entries = {p["name"]: p for p in codex["plugins"]}
    claude_entries = {p["name"]: p for p in claude["plugins"]}
    require(len(codex_entries) == len(codex["plugins"]), "Duplicate Codex entries")
    require(len(claude_entries) == len(claude["plugins"]), "Duplicate Claude entries")
    require(codex_entries.keys() == claude_entries.keys(), "Catalog plugins differ")
    for name, entry in codex_entries.items():
        require(entry["source"]["source"] == "local", "Expected a repository-local source")
        root = component(ROOT, entry["source"]["path"])
        require(root == component(ROOT, claude_entries[name]["source"]), "Plugin sources differ")
        require(entry["policy"]["installation"] == "AVAILABLE", "Plugin must be available")
        require(entry["policy"]["authentication"] in ("ON_INSTALL", "ON_USE"), "Invalid auth policy")
        require(bool(entry["category"]), "Missing category")
        manifests = [read_json(root / kind / "plugin.json") for kind in (".codex-plugin", ".claude-plugin")]
        for field in ("name", "version", "description", "author", "repository", "license", "skills"):
            require(manifests[0][field] == manifests[1][field], f"Manifest {field} differs")
        require(manifests[0]["name"] == name == root.name, "Plugin identifiers differ")
        require(re.fullmatch(r"\d+\.\d+\.\d+", manifests[0]["version"]), "Expected a release version")
        codex_mcp = manifests[0]["mcpServers"]["go-certification"]
        claude_mcp = read_json(component(root, manifests[1]["mcpServers"]))["mcpServers"]["go-certification"]
        expected_url = "https://open.travelterminal.derbysoft-test.com/mcp"
        require(codex_mcp["url"] == claude_mcp["url"] == expected_url, "MCP endpoints differ")
        require(codex_mcp["type"] == claude_mcp["type"] == "http", "Expected HTTP MCP")
        require(codex_mcp.get("http_headers") == {"X-GO-Token": ""}, "Codex must preset the header name with an empty key")
        require("env_http_headers" not in codex_mcp and "headers" not in codex_mcp, "Unexpected alternate Codex auth source")
        require(claude_mcp["headers"] == {"X-GO-Token": "${GO_TOKEN}"}, "Claude must use environment auth")
        for manifest in manifests:
            skills = component(root, manifest["skills"])
            skill_files = list(skills.glob("*/SKILL.md"))
            require(bool(skill_files), "No skills found")
            for skill in skill_files:
                text = skill.read_text(encoding="utf-8")
                require(text.startswith("---\n") and "\n---\n" in text[4:], "Missing skill frontmatter")
                require(f"name: {skill.parent.name}\n" in text, "Skill name and directory differ")
                require(re.search(r"^description: .+", text, re.M), "Missing skill description")
                for link in re.findall(r"\]\(([^)]+)\)", text):
                    if "://" not in link and not link.startswith("#"):
                        component(skill.parent, "./" + link)
        for path in root.rglob("*"):
            require(not path.is_symlink(), f"Symlink in plugin: {path.relative_to(ROOT)}")
            if path.is_file():
                require(path.name not in (".env", "server"), "Unexpected runtime or credential file")
                require(path.suffix in (".md", ".json"), f"Unexpected plugin file: {path.name}")
                content = path.read_text(encoding="utf-8")
                require("[TODO:" not in content, "Unfinished scaffold")
                require(not re.search(r"https?://(?:10\.|192\.168\.|127\.|localhost)", content), "Private endpoint in plugin")
                require(not re.search(r"[A-Za-z]:\\Users\\|/Users/|/home/", content), "Machine-specific path in plugin")
    print(f"Validated {len(codex_entries)} plugin(s) for Codex and Claude Code.")


if __name__ == "__main__":
    main()
