# dotfiles

Claude Code / Codex の設定と Agent Skills を管理するリポジトリ。

## 構成

| パス | 内容 |
|------|------|
| `CLAUDE.md` (`AGENTS.md` はsymlink) | 実装ルール |
| `.claude/settings.json` | Claude Code の設定 |
| `.claude/agents/` | subagent 定義 |
| `.mcp.json` | MCP サーバー定義 |
| `skills/` | Agent Skills |

`skills/` を除くいずれも、このリポジトリを開いたときのプロジェクト設定として機能する。ホームディレクトリへの展開はしていない。

## スキルのインストール

| スキル | 内容 |
|--------|------|
| [release-qa](skills/release-qa/) | GitHub PR のURLリストからリリースQAチェックリストを生成する |

```bash
gh skill install Higashi-Masafumi/dotfiles release-qa --agent claude-code --scope user
gh skill install Higashi-Masafumi/dotfiles release-qa --agent codex --scope user
```

- `gh skill` は GitHub CLI 2.95.0 以降の preview 機能
- `--scope project` にするとカレントリポジトリ内だけに入る
- インストール済みの一覧は `gh skill list`

## スキルを編集するとき

インストール済みのスキルはコピーなので、編集を反映するには push と update が必要。

```bash
# 1. skills/<skill-name>/ を編集する

gh skill publish --dry-run    # 2. Agent Skills 仕様に沿っているか検証する
git commit && git push        # 3. push する
gh skill update release-qa    # 4. インストール済み環境へ反映する
```
