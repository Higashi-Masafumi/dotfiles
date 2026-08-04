#!/usr/bin/env python3
"""Fetch metadata + diff for a list of GitHub PR URLs via `gh`.

Each PR URL is parsed independently for owner/repo/number, so PRs from
different repositories can be mixed in a single invocation.

Usage:
    fetch_pr_diffs.py <PR URL> [<PR URL> ...] [--out-dir DIR]

Writes one Markdown file per PR (metadata + description + diff) into
the output directory, plus a _summary.json index, and prints the
output directory path on the last line of stdout.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PR_URL_RE = re.compile(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)")

PR_VIEW_FIELDS = (
    "number,title,body,url,author,baseRefName,headRefName,"
    "additions,deletions,changedFiles,state,isDraft,mergedAt"
)


def run_gh(args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "gh command failed")
    return result.stdout


def fetch_pr(owner, repo, number, out_dir):
    repo_slug = f"{owner}/{repo}"
    meta = json.loads(
        run_gh(["pr", "view", str(number), "--repo", repo_slug, "--json", PR_VIEW_FIELDS])
    )
    diff_text = run_gh(["pr", "diff", str(number), "--repo", repo_slug])

    out_file = out_dir / f"{owner}__{repo}__{number}.md"
    with out_file.open("w") as f:
        f.write(f"# PR #{number}: {meta['title']}\n\n")
        f.write(f"- URL: {meta['url']}\n")
        f.write(f"- Repo: {repo_slug}\n")
        f.write(f"- Author: {meta['author']['login']}\n")
        f.write(f"- Base: {meta['baseRefName']} <- Head: {meta['headRefName']}\n")
        f.write(f"- State: {meta['state']} (draft={meta['isDraft']})\n")
        f.write(
            f"- Changed files: {meta['changedFiles']} "
            f"(+{meta['additions']}/-{meta['deletions']})\n\n"
        )
        f.write("## Description\n\n")
        f.write((meta.get("body") or "(no description)").strip() + "\n\n")
        f.write("## Diff\n\n```diff\n")
        f.write(diff_text)
        f.write("\n```\n")

    return out_file, meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="GitHub PR URLs")
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory (default: a fresh temp dir under /tmp)",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else Path(tempfile.mkdtemp(prefix="release-qa-"))
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    had_error = False
    for url in args.urls:
        match = PR_URL_RE.search(url)
        if not match:
            print(f"SKIP (not a GitHub PR URL): {url}", file=sys.stderr)
            had_error = True
            continue

        owner, repo, number = match.group(1), match.group(2), match.group(3)
        try:
            out_file, meta = fetch_pr(owner, repo, number, out_dir)
        except RuntimeError as e:
            print(f"ERROR fetching {url}: {e}", file=sys.stderr)
            had_error = True
            continue

        results.append(
            {
                "url": url,
                "file": str(out_file),
                "title": meta["title"],
                "changed_files": meta["changedFiles"],
            }
        )
        print(f"OK  #{number} {meta['title']} -> {out_file}")

    summary_file = out_dir / "_summary.json"
    summary_file.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")

    print(f"\nOutput dir: {out_dir}")
    if had_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
