# dotfiles

my dotfiles

## Agent Skills

`skills/` 以下は [Agent Skills 仕様](https://agentskills.io/specification) に準拠しており、`gh skill` (GitHub CLI 2.95.0 以降, preview) でインストールできる。

| スキル | 内容 |
|--------|------|
| [release-qa](skills/release-qa/) | GitHub PRのURLリストから、非エンジニアのQA担当者がそのまま実施できるリリースQAチェックリストを生成する |

### インストール

ユーザースコープ (どのプロジェクトでも使える) に入れる場合:

```bash
gh skill install Higashi-Masafumi/dotfiles release-qa --agent claude-code --scope user
gh skill install Higashi-Masafumi/dotfiles release-qa --agent codex --scope user
```

プロジェクトスコープ (そのリポジトリ内だけで使う) に入れる場合:

```bash
gh skill install Higashi-Masafumi/dotfiles release-qa --agent claude-code --scope project
gh skill install Higashi-Masafumi/dotfiles release-qa --agent codex --scope project
```

- Claude Code は `.claude/skills/`、Codex は `.agents/skills/` に配置される (Codex・Copilot・Cursor などは `.agents/skills/` を共有する)
- リリースタグを切っていない間は default branch の HEAD が使われる。バージョンを固定するなら `release-qa@v0.1.0` や `--pin <SHA>` を指定する
- 更新は `gh skill update`、確認は `gh skill list`
- スキルの実行には `gh` の認証が必要 (`gh auth status`)

### このリポジトリで開発する場合

自分のマシンでは、インストール (コピー) ではなく symlink を張って編集を即反映させている。

```bash
ln -s ../../dev/dotfiles/skills/release-qa ~/.claude/skills/release-qa
ln -s ../../dev/dotfiles/skills/release-qa ~/.codex/skills/release-qa
```

仕様準拠の検証は publish の dry-run で行う。

```bash
gh skill publish --dry-run
```
