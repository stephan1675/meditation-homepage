#!/usr/bin/env python3
"""Build a multi-branch static site for GitHub Pages with a centered top branch switcher.

Publishes:
  - main     -> <output>/
  - develop  -> <output>/branches/develop/
  - *claude* -> <output>/branches/<branch-name>/

Every HTML page receives a centered, theme-aware top branch switcher linking to all
published branches via relative paths (works on GitHub Pages subpaths and locally).
"""

from __future__ import annotations

import argparse
import html
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote


EXCLUDED_TOP_LEVEL = {
    ".git",
    ".github",
    ".gitignore",
    "_site",
}

SWITCHER_CSS = """
<style id="gh-branch-switcher-styles">
  .gh-branch-bar {
    position: sticky;
    top: 0;
    z-index: 900;
    width: 100%;
    padding: 0.55rem 1rem;
    background: rgba(250, 247, 242, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border, #e3dbce);
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    transition: background-color 0.25s ease, border-color 0.25s ease;
  }

  :root[data-theme="dark"] .gh-branch-bar {
    background: rgba(21, 24, 22, 0.9);
  }

  .gh-branch-switcher {
    max-width: 1120px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.45rem 0.65rem;
  }

  .gh-branch-prefix {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted, #5c635e);
    user-select: none;
  }

  .gh-branch-prefix svg {
    width: 14px;
    height: 14px;
    flex-shrink: 0;
    opacity: 0.85;
  }

  .gh-branch-list {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
  }

  .gh-branch-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.42rem;
    padding: 0.3rem 0.78rem;
    border-radius: 999px;
    border: 1px solid var(--border, #e3dbce);
    background: var(--surface, #ffffff);
    color: var(--text, #1f2421);
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 500;
    line-height: 1.3;
    transition: border-color 0.18s ease, background-color 0.18s ease, color 0.18s ease, transform 0.18s ease;
  }

  .gh-branch-pill:hover {
    border-color: var(--accent, #9c7449);
    transform: translateY(-1px);
  }

  .gh-branch-pill:focus-visible {
    outline: 2px solid var(--accent, #9c7449);
    outline-offset: 2px;
  }

  .gh-branch-pill.is-active {
    background: var(--text, #1f2421);
    border-color: var(--text, #1f2421);
    color: var(--on-text, #ffffff);
    font-weight: 600;
  }

  .gh-branch-pill.is-active:hover {
    transform: none;
  }

  .gh-branch-dot {
    width: 0.46rem;
    height: 0.46rem;
    border-radius: 50%;
    flex-shrink: 0;
    background: var(--accent, #9c7449);
  }

  .gh-branch-pill[data-branch-kind="main"] .gh-branch-dot {
    background: #2f855a;
  }

  .gh-branch-pill[data-branch-kind="develop"] .gh-branch-dot {
    background: #c6862a;
  }

  .gh-branch-pill[data-branch-kind="claude"] .gh-branch-dot {
    background: #8b5a9b;
  }

  .gh-branch-pill.is-active[data-branch-kind="main"] .gh-branch-dot {
    background: #68d391;
  }

  .gh-branch-pill.is-active[data-branch-kind="develop"] .gh-branch-dot {
    background: #f6ad55;
  }

  .gh-branch-pill.is-active[data-branch-kind="claude"] .gh-branch-dot {
    background: #d6bcfa;
  }

  .gh-branch-sha {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.7rem;
    opacity: 0.65;
  }

  @media (max-width: 600px) {
    .gh-branch-bar {
      padding: 0.5rem 0.65rem;
    }

    .gh-branch-prefix span {
      display: none;
    }

    .gh-branch-pill {
      padding: 0.28rem 0.65rem;
      font-size: 0.78rem;
    }

    .gh-branch-sha {
      display: none;
    }
  }
</style>
""".strip()


BRANCH_ICON_SVG = (
    '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
    '<path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 '
    '1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 '
    '0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Zm-6 0a.75.75 0 1 0 '
    '1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25 '
    '12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"/></svg>'
)


@dataclass(frozen=True)
class BranchInfo:
    name: str
    ref: str
    kind: str  # "main" | "develop" | "claude"
    rel_dir: str  # "" for main, "branches/<name>" for others
    sha: str
    date: str
    subject: str


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def run_git_bytes(args: list[str], cwd: Path) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )
    return result.stdout


def classify_branch(name: str) -> str | None:
    if name == "main":
        return "main"
    if name == "develop":
        return "develop"
    if "claude" in name.lower():
        return "claude"
    return None


def validate_branch_rel_dir(name: str) -> str:
    if name == "main":
        return ""
    segments = [seg for seg in name.split("/") if seg]
    if not segments or any(seg in {".", ".."} for seg in segments):
        raise ValueError(f"Unsafe branch name for output directory: {name!r}")
    return posixpath.join("branches", *segments)


def discover_branches(repo_dir: Path, remote: str) -> list[BranchInfo]:
    prefix = f"refs/remotes/{remote}/"
    raw = run_git(["for-each-ref", "--format=%(refname)", prefix], cwd=repo_dir)
    found: dict[str, str] = {}

    for line in raw.splitlines():
        ref = line.strip()
        if not ref or not ref.startswith(prefix):
            continue
        name = ref[len(prefix) :]
        if name == "HEAD":
            continue
        if classify_branch(name) is not None:
            found[name] = ref

    # Fallback to local branches if remote refs are absent (e.g. local-only test repo)
    if not found:
        local_prefix = "refs/heads/"
        raw_local = run_git(
            ["for-each-ref", "--format=%(refname)", local_prefix], cwd=repo_dir
        )
        for line in raw_local.splitlines():
            ref = line.strip()
            if not ref or not ref.startswith(local_prefix):
                continue
            name = ref[len(local_prefix) :]
            if classify_branch(name) is not None:
                found[name] = ref

    branches: list[BranchInfo] = []
    for name, ref in found.items():
        kind = classify_branch(name)
        assert kind is not None
        meta = run_git(
            ["log", "-1", "--format=%h%x1f%cs%x1f%s", ref], cwd=repo_dir
        ).strip()
        parts = meta.split("\x1f", 2)
        sha = parts[0] if len(parts) > 0 else ""
        date = parts[1] if len(parts) > 1 else ""
        subject = parts[2] if len(parts) > 2 else ""
        branches.append(
            BranchInfo(
                name=name,
                ref=ref,
                kind=kind,
                rel_dir=validate_branch_rel_dir(name),
                sha=sha,
                date=date,
                subject=subject,
            )
        )

    order = {"main": 0, "develop": 1, "claude": 2}
    branches.sort(key=lambda b: (order[b.kind], b.name.lower()))
    return branches


def export_branch(repo_dir: Path, branch: BranchInfo, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    archive_bytes = run_git_bytes(["archive", "--format=tar", branch.ref], cwd=repo_dir)

    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as tar:
        for member in tar.getmembers():
            rel = Path(member.name)
            if rel.is_absolute() or ".." in rel.parts or not rel.parts:
                continue
            if rel.parts[0] in EXCLUDED_TOP_LEVEL:
                continue
            target = dest_dir / rel
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                extracted = tar.extractfile(member)
                if extracted is not None:
                    with open(target, "wb") as out_f:
                        shutil.copyfileobj(extracted, out_f)


def compute_href(from_dir_rel: str, target_branch: BranchInfo, is_self: bool) -> str:
    depth = len([seg for seg in from_dir_rel.split("/") if seg])
    to_root = "../" * depth
    if not target_branch.rel_dir:
        return "./" if depth == 0 else to_root
    if is_self and from_dir_rel == target_branch.rel_dir:
        return "./"
    encoded = "/".join(quote(seg, safe="") for seg in target_branch.rel_dir.split("/"))
    return f"{to_root}{encoded}/"


def render_switcher_html(
    branches: list[BranchInfo], current: BranchInfo, html_dir_rel: str
) -> str:
    pills: list[str] = []
    for branch in branches:
        is_active = branch.name == current.name
        href = compute_href(html_dir_rel, branch, is_self=is_active)
        active_cls = " is-active" if is_active else ""
        aria_current = ' aria-current="page"' if is_active else ""
        tooltip_parts = [f"Branch: {branch.name}"]
        if branch.sha:
            tooltip_parts.append(f"Commit {branch.sha}")
        if branch.date:
            tooltip_parts.append(f"({branch.date})")
        if branch.subject:
            tooltip_parts.append(f"– {branch.subject}")
        tooltip = html.escape(" ".join(tooltip_parts), quote=True)
        label = html.escape(branch.name)
        sha_html = (
            f'<span class="gh-branch-sha">{html.escape(branch.sha)}</span>'
            if branch.sha
            else ""
        )
        pills.append(
            f'<a class="gh-branch-pill{active_cls}" '
            f'data-branch-kind="{html.escape(branch.kind, quote=True)}" '
            f'href="{html.escape(href, quote=True)}"{aria_current} '
            f'title="{tooltip}">'
            f'<span class="gh-branch-dot" aria-hidden="true"></span>'
            f'<span class="gh-branch-name">{label}</span>'
            f"{sha_html}"
            f"</a>"
        )

    return (
        '<div class="gh-branch-bar" role="region" aria-label="Branch-Switcher">\n'
        '  <nav class="gh-branch-switcher" aria-label="Branch wechseln">\n'
        f'    <span class="gh-branch-prefix">{BRANCH_ICON_SVG}<span>Branch</span></span>\n'
        '    <div class="gh-branch-list">\n'
        + "\n".join(f"      {pill}" for pill in pills)
        + "\n    </div>\n"
        "  </nav>\n"
        "</div>"
    )


def inject_switcher_into_html(
    html_path: Path, site_root: Path, branches: list[BranchInfo], current: BranchInfo
) -> None:
    content = html_path.read_text(encoding="utf-8")
    if 'id="gh-branch-switcher-styles"' in content:
        return

    rel_parent = html_path.parent.relative_to(site_root).as_posix()
    if rel_parent == ".":
        rel_parent = ""

    switcher_html = render_switcher_html(branches, current, rel_parent)

    head_close_re = re.compile(r"</head>", re.IGNORECASE)
    if head_close_re.search(content):
        content = head_close_re.sub(
            lambda _: f"{SWITCHER_CSS}\n</head>", content, count=1
        )
    else:
        content = f"{SWITCHER_CSS}\n{content}"

    body_open_re = re.compile(r"<body\b[^>]*>", re.IGNORECASE)
    if body_open_re.search(content):
        content = body_open_re.sub(
            lambda m: f"{m.group(0)}\n{switcher_html}\n", content, count=1
        )
    else:
        content = f"{switcher_html}\n{content}"

    html_path.write_text(content, encoding="utf-8")


def build_site(repo_dir: Path, output_dir: Path, remote: str) -> list[BranchInfo]:
    branches = discover_branches(repo_dir, remote=remote)
    if not branches:
        raise RuntimeError(
            "No matching branches found (expected main, develop, or *claude*)."
        )

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export main first so its files live at site root, then non-main branches under branches/
    for branch in branches:
        dest = output_dir / branch.rel_dir if branch.rel_dir else output_dir
        export_branch(repo_dir, branch, dest)

    # Inject the centered branch switcher into HTML files belonging to each branch
    for branch in branches:
        branch_root = output_dir / branch.rel_dir if branch.rel_dir else output_dir
        for html_file in branch_root.rglob("*.html"):
            if branch.name == "main":
                rel_to_site = html_file.relative_to(output_dir)
                if rel_to_site.parts and rel_to_site.parts[0] == "branches":
                    continue
            inject_switcher_into_html(html_file, output_dir, branches, branch)

    # Disable Jekyll processing on GitHub Pages
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")

    # Write manifest for inspection/debugging
    manifest = [
        {
            "name": b.name,
            "kind": b.kind,
            "path": f"/{b.rel_dir}/" if b.rel_dir else "/",
            "sha": b.sha,
            "date": b.date,
            "subject": b.subject,
        }
        for b in branches
    ]
    (output_dir / "branches.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return branches


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build multi-branch GitHub Pages output with top branch switcher."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Path to the git repository (default: cwd).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("_site"),
        help="Output directory for the built static site (default: _site).",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Git remote name to read branches from (default: origin).",
    )
    args = parser.parse_args()

    branches = build_site(
        repo_dir=args.repo.resolve(),
        output_dir=args.output.resolve(),
        remote=args.remote,
    )
    print(f"Built multi-branch site with {len(branches)} branch(es):")
    for b in branches:
        url_path = f"/{b.rel_dir}/" if b.rel_dir else "/"
        print(f"  - {b.name} ({b.kind}, {b.sha}) -> {url_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
