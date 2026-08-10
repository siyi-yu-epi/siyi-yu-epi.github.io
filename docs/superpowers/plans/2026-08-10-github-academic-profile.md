# GitHub Academic Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build and publish a restrained one-page academic profile at https://siyi-yu-epi.github.io using GitHub Pages' official Minimal theme, a professional portrait, and a phone-free public CV.

**Architecture:** GitHub Pages will build a static Jekyll site from main at the repository root. The official Minimal stylesheet provides the visual system, while one small local layout override supplies the approved sidebar, descriptive portrait alt text, and CV/email links. A Python asset-preparation script creates derivative public assets without modifying the supplied source files, and a standard-library unittest contract checks the site before publication.

**Tech Stack:** GitHub Pages, Jekyll, jekyll-theme-minimal, Markdown, Liquid, Python 3.13, Pillow, PyMuPDF, pypdf, Poppler, GitHub CLI

## Global Constraints

- Keep the site to one page and preserve the official Minimal visual style.
- Do not add animations, decorative cards, gradients, shadows, dark mode, analytics, tracking, forms, or custom client-side JavaScript.
- Do not publish a phone number in HTML, Markdown, configuration, scripts, tests, or extractable PDF text.
- Preserve the supplied profile photograph and CV unchanged; commit only web-ready derivatives.
- Keep all names, collaborator lists, statuses, publication details, and claims aligned with the approved design specification.
- Do not invent abstracts, findings, publication links, social profiles, or collaborator relationships.
- Use yu1344@purdue.edu as the only public contact method.
- Keep the public CV at assets/files/Siyi-Yu-CV.pdf and the portrait at assets/img/profile.jpg.
- Use branch publishing from main and the repository root; do not add a custom deployment workflow.
- The current environment has no Ruby, Bundler, or Jekyll executable. Use the local Python contract before publication and require GitHub Pages to report a successful build for the exact deployed commit; do not install a second site framework.
- Treat build errors, broken assets, incorrect links, residual phone content, or unreadable responsive layout as release blockers.
- Source design: docs/superpowers/specs/2026-08-10-github-academic-profile-design.md.
- Official references: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/adding-a-theme-to-your-github-pages-site-using-jekyll and https://github.com/pages-themes/minimal.

---

## File map

- Create assets/img/profile.jpg - optimized 800 x 1000 portrait derivative.
- Create assets/files/Siyi-Yu-CV.pdf - two-page public CV with the phone row truly redacted.
- Create scripts/prepare_assets.py - deterministic, source-preserving asset builder.
- Create tests/test_site_contract.py - executable privacy, asset, content, layout, and maintenance contract.
- Create _config.yml - GitHub Pages and Minimal theme configuration.
- Create _layouts/default.html - minimal accessibility/sidebar override using the official theme stylesheet.
- Create index.md - the complete approved academic homepage content.
- Create .gitignore - exclude local preview, cache, and QA artifacts.
- Modify README.md - concise maintenance and publication guide.

### Task 1: Prepare and verify safe public assets

**Files:**
- Create: scripts/prepare_assets.py
- Create: tests/test_site_contract.py
- Create: assets/img/profile.jpg
- Create: assets/files/Siyi-Yu-CV.pdf

**Interfaces:**
- Consumes: the supplied 3648 x 5472 profile.jpg and two-page CV_Ongoing.pdf at their current external paths.
- Produces: an 800 x 1000 JPEG under 500,000 bytes and a two-page PDF whose extracted text contains no Phone: label.
- Produces: tests/test_site_contract.py, which later tasks extend with site-content checks.

- [ ] **Step 1: Write the failing asset contract**

Create tests/test_site_contract.py with:

~~~~python
from pathlib import Path
import re
import unittest

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "assets" / "img" / "profile.jpg"
CV = ROOT / "assets" / "files" / "Siyi-Yu-CV.pdf"
PHONE_LABEL_RE = re.compile(r"\bphone\s*:", re.IGNORECASE)


class SiteContractTests(unittest.TestCase):
    def test_profile_asset_is_web_sized(self):
        self.assertTrue(PROFILE.is_file(), f"Missing {PROFILE}")
        self.assertLessEqual(PROFILE.stat().st_size, 500_000)
        with Image.open(PROFILE) as image:
            self.assertEqual(image.size, (800, 1000))
            self.assertEqual(image.format, "JPEG")

    def test_public_cv_is_two_pages_and_phone_free(self):
        self.assertTrue(CV.is_file(), f"Missing {CV}")
        reader = PdfReader(CV)
        self.assertEqual(len(reader.pages), 2)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        self.assertNotRegex(text, PHONE_LABEL_RE)


if __name__ == "__main__":
    unittest.main()
~~~~

- [ ] **Step 2: Run the asset contract and confirm it fails**

Run:

~~~~powershell
uv run --with pillow --with pypdf python -m unittest discover -s tests -v
~~~~

Expected: two failures reporting the missing profile and public CV assets.

- [ ] **Step 3: Implement the deterministic asset builder**

Create scripts/prepare_assets.py with:

~~~~python
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

import fitz
from PIL import Image


PHONE_LABEL_RE = re.compile(r"\bphone\s*:", re.IGNORECASE)
PROFILE_CROP = (560, 900, 3088, 4060)
PROFILE_SIZE = (800, 1000)
PROFILE_MAX_BYTES = 500_000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_profile(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as original:
        if original.size != (3648, 5472):
            raise ValueError(f"Unexpected profile dimensions: {original.size}")
        derivative = (
            original.convert("RGB")
            .crop(PROFILE_CROP)
            .resize(PROFILE_SIZE, Image.Resampling.LANCZOS)
        )
        for quality in (88, 84, 80):
            derivative.save(
                target,
                format="JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
            )
            if target.stat().st_size <= PROFILE_MAX_BYTES:
                break
        else:
            raise ValueError(f"Profile derivative exceeds {PROFILE_MAX_BYTES} bytes")


def phone_row(page: fitz.Page) -> fitz.Rect:
    matches = [
        word
        for word in page.get_text("words")
        if str(word[4]).strip().lower() == "phone:"
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one Phone: label, found {len(matches)}")
    word = matches[0]
    return fitz.Rect(word[0] - 2, word[1] - 2, page.rect.x1 - 36, word[3] + 2)


def prepare_cv(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".tmp.pdf")
    if temporary.exists():
        temporary.unlink()

    with fitz.open(source) as document:
        if document.page_count != 2:
            raise ValueError(f"Expected a two-page CV, found {document.page_count} pages")
        page = document[0]
        page.add_redact_annot(phone_row(page), fill=(1, 1, 1))
        page.apply_redactions()
        document.save(temporary, garbage=4, deflate=True, clean=True)

    temporary.replace(target)
    with fitz.open(target) as public_document:
        text = "\n".join(page.get_text() for page in public_document)
        if PHONE_LABEL_RE.search(text):
            raise ValueError("Phone label remains in extractable public CV text")
        if public_document.page_count != 2:
            raise ValueError("Public CV page count changed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-source", required=True, type=Path)
    parser.add_argument("--cv-source", required=True, type=Path)
    parser.add_argument(
        "--profile-target",
        type=Path,
        default=Path("assets/img/profile.jpg"),
    )
    parser.add_argument(
        "--cv-target",
        type=Path,
        default=Path("assets/files/Siyi-Yu-CV.pdf"),
    )
    args = parser.parse_args()

    before = {
        args.profile_source: sha256(args.profile_source),
        args.cv_source: sha256(args.cv_source),
    }
    prepare_profile(args.profile_source, args.profile_target)
    prepare_cv(args.cv_source, args.cv_target)
    after = {path: sha256(path) for path in before}
    if before != after:
        raise RuntimeError("A source asset changed during derivative creation")


if __name__ == "__main__":
    main()
~~~~

- [ ] **Step 4: Generate the two public derivatives**

Run:

~~~~powershell
uv run --with pymupdf --with pillow python scripts/prepare_assets.py --profile-source "C:\Users\Ruth\2001110960 Dropbox\Siyi Yu\个人资料\重要图片\profile.jpg" --cv-source "C:\Users\Ruth\Downloads\CV_Ongoing.pdf"
~~~~

Expected: assets/img/profile.jpg and assets/files/Siyi-Yu-CV.pdf are created; both source hashes remain unchanged.

- [ ] **Step 5: Run the asset contract and confirm it passes**

Run:

~~~~powershell
uv run --with pillow --with pypdf python -m unittest discover -s tests -v
~~~~

Expected: 2 tests pass.

- [ ] **Step 6: Render and visually inspect both CV pages**

Run:

~~~~powershell
New-Item -ItemType Directory -Force -Path "tmp\pdf-qa" | Out-Null
& "C:\Users\Ruth\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe" -png -r 160 "assets\files\Siyi-Yu-CV.pdf" "tmp\pdf-qa\cv"
~~~~

Open tmp/pdf-qa/cv-1.png and tmp/pdf-qa/cv-2.png with view_image. Require the phone row to be absent, the email row to remain intact, and all other text, links, spacing, pagination, and margins to match the supplied CV without clipping or overlays.

- [ ] **Step 7: Visually inspect the profile derivative**

Open assets/img/profile.jpg with view_image. Require a natural-color head-and-shoulders crop, a centered face, no stretching, no clipping through the head, and no visible compression artifacts.

If either visual check fails, adjust only PROFILE_CROP, JPEG quality, or the phone-row rectangle in scripts/prepare_assets.py, rerun Steps 4-7, and do not commit until both assets pass.

- [ ] **Step 8: Commit the verified assets and asset contract**

Run:

~~~~powershell
git add -- scripts/prepare_assets.py tests/test_site_contract.py assets/img/profile.jpg assets/files/Siyi-Yu-CV.pdf
git diff --cached --check
git commit -m "feat: add privacy-safe profile assets"
~~~~

Expected: one commit containing only the builder, contract, and two public assets.

### Task 2: Build the accessible Minimal-theme homepage

**Files:**
- Modify: tests/test_site_contract.py
- Create: _config.yml
- Create: _layouts/default.html
- Create: index.md
- Create: .gitignore

**Interfaces:**
- Consumes: assets/img/profile.jpg and assets/files/Siyi-Yu-CV.pdf from Task 1.
- Produces: a GitHub Pages Jekyll source tree using jekyll-theme-minimal.
- Produces: a default layout that reads site.logo_alt, site.email, and site.cv_path from _config.yml.

- [ ] **Step 1: Extend the contract with configuration, layout, and content checks**

Add these constants below the existing asset constants:

~~~~python
CONFIG = ROOT / "_config.yml"
LAYOUT = ROOT / "_layouts" / "default.html"
INDEX = ROOT / "index.md"
~~~~

Add these methods to SiteContractTests:

~~~~python
    def test_config_selects_minimal_and_stable_assets(self):
        config = CONFIG.read_text(encoding="utf-8")
        for expected in (
            "theme: jekyll-theme-minimal",
            "logo: /assets/img/profile.jpg",
            "cv_path: /assets/files/Siyi-Yu-CV.pdf",
            'email: "yu1344@purdue.edu"',
            "show_downloads: false",
        ):
            self.assertIn(expected, config)
        self.assertNotRegex(config, PHONE_LABEL_RE)

    def test_layout_has_accessible_sidebar_and_no_custom_script(self):
        layout = LAYOUT.read_text(encoding="utf-8")
        self.assertIn('alt="{{ site.logo_alt | escape }}"', layout)
        self.assertIn('href="mailto:{{ site.email }}"', layout)
        self.assertIn("site.cv_path | relative_url", layout)
        self.assertNotIn("<script", layout.lower())
        self.assertNotRegex(layout, PHONE_LABEL_RE)

    def test_index_contains_all_approved_sections_and_links(self):
        index = INDEX.read_text(encoding="utf-8")
        for heading in (
            "## About",
            "## Research themes",
            "## Current projects",
            "## Selected publications",
            "## Teaching and service",
            "## Contact",
        ):
            self.assertIn(heading, index)
        for required_text in (
            "The Birth Control Service Mix Post-Dobbs",
            "Impeding Drug Newcomers?",
            "Demand Displacement in the GLP-1 Market",
            "Artificial Intelligence in Marketing Research",
            "Price versus service satisfaction",
            "Pharmaceutical Pricing",
            "mailto:yu1344@purdue.edu",
            "/assets/files/Siyi-Yu-CV.pdf",
        ):
            self.assertIn(required_text, index)
        self.assertNotRegex(index, PHONE_LABEL_RE)
~~~~

- [ ] **Step 2: Run the extended contract and confirm it fails**

Run:

~~~~powershell
uv run --with pillow --with pypdf python -m unittest discover -s tests -v
~~~~

Expected: the two asset tests pass and the three new site-source tests fail because the Jekyll files do not exist.

- [ ] **Step 3: Create the GitHub Pages configuration**

Create _config.yml with:

~~~~yaml
title: "Siyi (Ruth) Yu"
description: "Clinical Assistant Professor of Management at Purdue University researching healthcare marketing, public policy, and large language models."
theme: jekyll-theme-minimal
logo: /assets/img/profile.jpg
logo_alt: "Portrait of Siyi (Ruth) Yu"
role: "Clinical Assistant Professor of Management"
affiliation: "Mitch Daniels School of Business, Purdue University"
email: "yu1344@purdue.edu"
cv_path: /assets/files/Siyi-Yu-CV.pdf
url: "https://siyi-yu-epi.github.io"
lang: "en-US"
show_downloads: false

exclude:
  - docs
  - scripts
  - tests
  - tmp
  - .superpowers
  - README.md
  - LICENSE
~~~~

- [ ] **Step 4: Create the small Minimal layout override**

Create _layouts/default.html with:

~~~~html
<!doctype html>
<html lang="{{ site.lang | default: "en-US" }}">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {% seo %}
    <link rel="stylesheet" href="{{ "/assets/css/style.css?v=" | append: site.github.build_revision | relative_url }}">
    {% include head-custom.html %}
  </head>
  <body>
    <div class="wrapper">
      <header>
        <h1><a href="{{ "/" | absolute_url }}">{{ site.title }}</a></h1>
        {% if site.logo %}
          <img src="{{ site.logo | relative_url }}" alt="{{ site.logo_alt | escape }}">
        {% endif %}
        <p>{{ site.role }}</p>
        <p>{{ site.affiliation }}</p>
        <p><a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
        <p><a href="{{ site.cv_path | relative_url }}">Download CV</a></p>
      </header>
      <section aria-label="Academic profile">
        {{ content }}
      </section>
      <footer>
        <p><small>Hosted on GitHub Pages using the Minimal theme.</small></p>
      </footer>
    </div>
  </body>
</html>
~~~~

- [ ] **Step 5: Create the approved one-page academic content**

Create index.md with:

~~~~markdown
---
layout: default
---

## About

I am a Clinical Assistant Professor of Management at Purdue University. My research focuses on healthcare marketing, public policy, and large language models, using causal inference, discrete choice models, and machine learning.

## Research themes

- Healthcare decisions and public policy
- Pharmaceutical markets and physician adoption
- Artificial intelligence in marketing research

## Current projects

- **The Birth Control Service Mix Post-Dobbs: How Abortion Bans Reshape Americans' Choices of Contraceptive Procedures** - With Qiang Liu, Hongju Liu, and Yong Cai. *Status: under review at M&SOM.*

- **Impeding Drug Newcomers? Investigating the Impact of Integrated Delivery Networks on Physician New Drug Adoption** - With Hongju Liu, Qiang Liu, and Yong Cai. *Status: manuscript ready for submission.*

- **Demand Displacement in the GLP-1 Market: Descriptive Evidence and Within-Patient Analysis** - With Sungjin Kim, Sungsik Park, Qiang Liu, and Yong Cai.

- **Artificial Intelligence in Marketing Research: An Umbrella Review** - With Qiang Liu, Lizi Xiang, and Yaxuan Ran.

## Selected publications

1. Weng, W., Yang, Z., & Yu, S. (2026). Price versus service satisfaction: The role of direct and indirect leasing in the B2B sector. *Journal of Business Research, 215*, 116312. [https://doi.org/10.1016/j.jbusres.2026.116312](https://doi.org/10.1016/j.jbusres.2026.116312)
2. Liu, Q., Yu, S., Wen, S., & Cai, Y. (2026). "Pharmaceutical Pricing," in *Handbook of Pricing Research in Marketing* (forthcoming), edited by Vithala Rao and K. Sudhir.

## Teaching and service

At Purdue, I teach Marketing Research and Marketing Management. I also chair the DSB AI in Marketing Committee and serve as the department liaison for the Daniels Insights Blog.

For my complete record of teaching, presentations, service, honors, grants, memberships, and skills, [download my CV](/assets/files/Siyi-Yu-CV.pdf).

## Contact

For research and collaboration inquiries, email me at [yu1344@purdue.edu](mailto:yu1344@purdue.edu).
~~~~

- [ ] **Step 6: Ignore local preview and QA artifacts**

Create .gitignore with:

~~~~gitignore
.superpowers/
tmp/
_site/
.jekyll-cache/
.sass-cache/
.bundle/
~~~~

- [ ] **Step 7: Run the full contract and confirm it passes**

Run:

~~~~powershell
uv run --with pillow --with pypdf python -m unittest discover -s tests -v
~~~~

Expected: 5 tests pass.

- [ ] **Step 8: Inspect the source diff for scope and formatting**

Run:

~~~~powershell
git diff --check
git diff -- _config.yml _layouts/default.html index.md .gitignore tests/test_site_contract.py
git status --short
~~~~

Expected: only the approved Jekyll source, ignore file, and extended contract are pending; local .superpowers and tmp artifacts are ignored.

- [ ] **Step 9: Commit the working homepage**

Run:

~~~~powershell
git add -- _config.yml _layouts/default.html index.md .gitignore tests/test_site_contract.py
git diff --cached --check
git commit -m "feat: build minimal academic profile"
~~~~

Expected: one commit containing the complete one-page site source and its contract.

### Task 3: Document maintenance, deploy, and verify the public site

**Files:**
- Modify: tests/test_site_contract.py
- Modify: README.md

**Interfaces:**
- Consumes: the complete local Jekyll source and assets from Tasks 1 and 2.
- Produces: a concise repository maintenance guide and a verified public deployment at https://siyi-yu-epi.github.io.
- Deployment gate: local main must contain the reviewed implementation commits and origin/main must not be ahead.

- [ ] **Step 1: Add a failing maintenance-guide contract**

Add this constant with the other path constants:

~~~~python
README = ROOT / "README.md"
~~~~

Add this method to SiteContractTests:

~~~~python
    def test_readme_documents_stable_update_paths(self):
        readme = README.read_text(encoding="utf-8")
        for expected in (
            "https://siyi-yu-epi.github.io",
            "index.md",
            "assets/img/profile.jpg",
            "assets/files/Siyi-Yu-CV.pdf",
            "scripts/prepare_assets.py",
        ):
            self.assertIn(expected, readme)
        self.assertNotRegex(readme, PHONE_LABEL_RE)
~~~~

- [ ] **Step 2: Run the contract and confirm the README check fails**

Run:

~~~~powershell
uv run --with pillow --with pypdf python -m unittest discover -s tests -v
~~~~

Expected: 5 tests pass and the README maintenance test fails.

- [ ] **Step 3: Replace the one-line README with the maintenance guide**

Replace README.md with:

~~~~markdown
# Siyi (Ruth) Yu - Academic Profile

Source repository for [https://siyi-yu-epi.github.io](https://siyi-yu-epi.github.io).

The site uses GitHub Pages and the official Minimal Jekyll theme.

## Updating the site

- Edit academic profile content in **index.md**.
- Replace the public portrait at **assets/img/profile.jpg**.
- Replace the phone-free public CV at **assets/files/Siyi-Yu-CV.pdf**.
- To rebuild both public assets from their private sources, run **scripts/prepare_assets.py** with explicit source paths.

Keep public claims aligned with the latest approved CV. Do not commit private source files or contact information that is not intended for publication.
~~~~

- [ ] **Step 4: Run all local release checks**

Run:

~~~~powershell
uv run --with pillow --with pypdf python -m unittest discover -s tests -v
git diff --check
git status --short
~~~~

Expected: 6 tests pass, diff checking is clean, and only README.md plus its test change are pending.

- [ ] **Step 5: Reconfirm the binary assets visually**

Open assets/img/profile.jpg and the two tmp/pdf-qa CV renderings with view_image. Require the previously approved crop and two clean CV pages. Re-run the Poppler rendering command from Task 1 if the QA images are missing or older than the public PDF.

- [ ] **Step 6: Commit the maintenance guide and final contract**

Run:

~~~~powershell
git add -- README.md tests/test_site_contract.py
git diff --cached --check
git commit -m "docs: add site maintenance guide"
~~~~

Expected: one documentation commit; no implementation files remain unstaged.

- [ ] **Step 7: Verify the Pages source and integration state before publishing**

Run:

~~~~powershell
gh api repos/siyi-yu-epi/siyi-yu-epi.github.io/pages --jq '{status:.status,branch:.source.branch,path:.source.path,url:.html_url}'
gh auth status
git fetch origin
git branch --show-current
git rev-list --left-right --count origin/main...main
git status --short
~~~~

Expected: Pages reports main and / as its source, GitHub CLI is authenticated as siyi-yu-epi, the active branch is main, the first number from git rev-list is 0 (origin/main is not ahead), and the worktree is clean. If the implementation was executed on a feature branch, use superpowers:finishing-a-development-branch to integrate the reviewed commits into main, then repeat this gate. Never force-push.

- [ ] **Step 8: Publish main**

Run:

~~~~powershell
git push origin main
~~~~

Expected: the push succeeds without a non-fast-forward error.

- [ ] **Step 9: Wait for the matching Pages build**

Capture the published commit:

~~~~powershell
$publishedCommit = (git rev-parse HEAD).Trim()
gh api repos/siyi-yu-epi/siyi-yu-epi.github.io/pages/builds/latest --jq '{status:.status,commit:.commit,error:.error.message,updated_at:.updated_at}'
~~~~

Repeat the read-only Pages-build query with short waits until commit equals $publishedCommit and status is built. If status is errored, inspect the returned error and the Pages deployment run, fix the source, rerun all local checks, commit, push, and repeat this step. Do not call deployment complete for a different commit.

- [ ] **Step 10: Verify the deployed content and assets over HTTPS**

Run:

~~~~powershell
$publishedCommit = (git rev-parse HEAD).Trim()
$site = Invoke-WebRequest -UseBasicParsing -Uri "https://siyi-yu-epi.github.io/?v=$publishedCommit"
$profile = Invoke-WebRequest -UseBasicParsing -Method Head -Uri "https://siyi-yu-epi.github.io/assets/img/profile.jpg?v=$publishedCommit"
$cv = Invoke-WebRequest -UseBasicParsing -Method Head -Uri "https://siyi-yu-epi.github.io/assets/files/Siyi-Yu-CV.pdf?v=$publishedCommit"

if ($site.StatusCode -ne 200) { throw "Homepage did not return HTTP 200." }
if ($profile.StatusCode -ne 200) { throw "Profile image did not return HTTP 200." }
if ($cv.StatusCode -ne 200) { throw "Public CV did not return HTTP 200." }

foreach ($required in @(
  "Research themes",
  "Current projects",
  "Selected publications",
  "Teaching and service",
  "mailto:yu1344@purdue.edu",
  "/assets/files/Siyi-Yu-CV.pdf"
)) {
  if ($site.Content -notmatch [regex]::Escape($required)) {
    throw "Published homepage is missing: $required"
  }
}
~~~~

Expected: the homepage and both assets return HTTP 200, and all approved sections and links are present in the published HTML.

- [ ] **Step 11: Perform final desktop, tablet, mobile, keyboard, and link QA**

Invoke browser:control-in-app-browser and open https://siyi-yu-epi.github.io with the published commit as a cache-busting query. Inspect at approximately 1440 x 900, 768 x 1024, and 390 x 844. Confirm:

- the portrait, identity, title, affiliation, email, and CV link are legible;
- desktop uses the Minimal two-column layout and mobile stacks without horizontal scrolling;
- all research, project, publication, teaching, service, and contact content is readable;
- keyboard focus is visible and link order is logical;
- the DOI, email, and CV links open the intended destinations;
- there are no animations, decorative cards, tracking prompts, or unexpected GitHub archive-download controls.

If any check fails, fix only the responsible source file, rerun the six local tests and diff checks, commit with git commit -m "fix: address published site QA", push main, and repeat Steps 9-11.

- [ ] **Step 12: Record final verification evidence**

Run:

~~~~powershell
git status --short
git log -5 --oneline --decorate
gh api repos/siyi-yu-epi/siyi-yu-epi.github.io/pages/builds/latest --jq '{status:.status,commit:.commit,error:.error.message,updated_at:.updated_at}'
~~~~

Expected: clean worktree, the intended commits at HEAD, and a built Pages deployment for the same HEAD commit.
