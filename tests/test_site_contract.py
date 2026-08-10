from pathlib import Path
import re
import unittest

import yaml
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "assets" / "img" / "profile.jpg"
CV = ROOT / "assets" / "files" / "Siyi-Yu-CV.pdf"
CONFIG = ROOT / "_config.yml"
LAYOUT = ROOT / "_layouts" / "default.html"
HEAD_CUSTOM = ROOT / "_includes" / "head-custom.html"
STYLESHEET = ROOT / "assets" / "css" / "site.css"
TABS_SCRIPT = ROOT / "assets" / "js" / "tabs.js"
INDEX = ROOT / "index.md"
README = ROOT / "README.md"
DATA = ROOT / "_data"
INCLUDES = ROOT / "_includes"

PHONE_LABEL_RE = re.compile(r"\bphone\s*:", re.IGNORECASE)
HARVESTABLE_EMAIL_RE = re.compile(r"mailto:|yu1344@purdue\.edu", re.IGNORECASE)
OBFUSCATED_EMAIL = "yu1344 at purdue dot edu"
TAB_TITLES = ("About", "Research", "Teaching", "Engagement")
DATA_FILES = ("publications", "working_papers", "news", "courses", "service")


def load_data(name):
    return yaml.safe_load((DATA / f"{name}.yml").read_text(encoding="utf-8"))


class AssetTests(unittest.TestCase):
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


class ConfigAndLayoutTests(unittest.TestCase):
    def test_config_selects_minimal_and_stable_assets(self):
        config = CONFIG.read_text(encoding="utf-8")
        for expected in (
            "theme: jekyll-theme-minimal",
            "cv_path: /assets/files/Siyi-Yu-CV.pdf",
            f'email_display: "{OBFUSCATED_EMAIL}"',
            "profile_image: /assets/img/profile.jpg",
            'profile_alt: "Portrait of Siyi (Ruth) Yu"',
            'google_scholar: "https://scholar.google.com/citations?user=kr3FpVwAAAAJ&hl=en"',
            'ssrn: "https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=10640376"',
            'linkedin: "https://www.linkedin.com/in/siyi-yu-407553239/"',
            "show_downloads: false",
        ):
            self.assertIn(expected, config)
        self.assertNotRegex(config, PHONE_LABEL_RE)

    def test_layout_shows_photo_and_never_exposes_a_harvestable_address(self):
        layout = LAYOUT.read_text(encoding="utf-8")
        self.assertIn('class="profile-photo"', layout)
        self.assertIn("site.profile_image | relative_url", layout)
        self.assertIn('alt="{{ site.profile_alt | escape }}"', layout)
        self.assertIn("{{ site.email_display }}", layout)
        self.assertIn("site.cv_path | relative_url", layout)
        for expected in (
            'href="{{ site.google_scholar }}" aria-label="Google Scholar"',
            'href="{{ site.ssrn }}" aria-label="SSRN"',
            'href="{{ site.linkedin }}" aria-label="LinkedIn"',
        ):
            self.assertIn(expected, layout)
        self.assertIn("head-custom.html", layout)
        self.assertIn('class="site-footer"', layout)
        self.assertNotIn("Hosted on GitHub Pages using the Minimal theme.", layout)
        self.assertNotIn("<script", layout.lower())
        self.assertNotRegex(layout, HARVESTABLE_EMAIL_RE)
        self.assertNotRegex(layout, PHONE_LABEL_RE)

    def test_custom_css_and_tabs_script_are_wired_up(self):
        for asset in (HEAD_CUSTOM, STYLESHEET, TABS_SCRIPT):
            self.assertTrue(asset.is_file(), f"Missing {asset}")
        head_custom = HEAD_CUSTOM.read_text(encoding="utf-8")
        self.assertIn("/assets/css/site.css", head_custom)
        self.assertIn("/assets/js/tabs.js", head_custom)
        self.assertIn("defer", head_custom)

        script = TABS_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('setAttribute("role", "tab")', script)
        self.assertIn('setAttribute("role", "tabpanel")', script)

    def test_stylesheet_keeps_conventional_page_margins_and_components(self):
        stylesheet = STYLESHEET.read_text(encoding="utf-8")
        # The theme's fixed 860px column is what the overrides replace; the
        # content column must stay a readable width rather than full-bleed.
        self.assertIn("max-width: 1100px", stylesheet)
        for component in (
            ".profile-photo",
            ".tabs__list",
            ".paper-list",
            ".entry-list",
            ".news-list",
            ".link-list",
            ".site-footer",
        ):
            self.assertIn(component, stylesheet)
        # Tabs must not hide three quarters of the page when printed.
        self.assertIn("@media print", stylesheet)


class ContentTests(unittest.TestCase):
    def test_index_declares_four_tabs_and_pulls_lists_from_data(self):
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn('<div class="tabs" data-tabs', index)
        for title in TAB_TITLES:
            self.assertIn(f'data-tab-title="{title}"', index)
            self.assertIn(f"## {title}", index)
            # Without an explicit id, kramdown auto-generates one from the
            # heading text that collides with the panel's own id.
            self.assertIn(f"{{: #{title.lower()}-heading}}", index)
        self.assertEqual(index.count('class="tab-panel"'), len(TAB_TITLES))
        self.assertEqual(index.count('markdown="1"'), len(TAB_TITLES))

        for include in (
            "{% include news.html items=site.data.news %}",
            "{% include papers.html items=site.data.publications numbered=true %}",
            "{% include papers.html items=site.data.working_papers %}",
            "{% include entries.html items=site.data.courses %}",
            "{% include entries.html items=site.data.service %}",
        ):
            self.assertIn(include, index)

        self.assertIn("{{ site.email_display }}", index)
        self.assertIn("https://business.purdue.edu/", index)
        self.assertNotRegex(index, HARVESTABLE_EMAIL_RE)
        self.assertNotRegex(index, PHONE_LABEL_RE)

    def test_includes_exist_for_every_data_driven_list(self):
        for name in ("papers", "entries", "news"):
            self.assertTrue((INCLUDES / f"{name}.html").is_file(), name)

    def test_data_files_parse_and_keep_the_approved_record(self):
        for name in DATA_FILES:
            self.assertTrue((DATA / f"{name}.yml").is_file(), name)
            self.assertIsInstance(load_data(name), list, name)

        titles = " ".join(p["title"] for p in load_data("publications"))
        self.assertIn("Price versus service satisfaction", titles)
        self.assertIn("Pharmaceutical Pricing", titles)

        wip = " ".join(p["title"] for p in load_data("working_papers"))
        for required in (
            "The Birth Control Service Mix Post-Dobbs",
            "Impeding Drug Newcomers?",
            "Demand Displacement in the GLP-1 Market",
            "Artificial Intelligence in Marketing Research",
        ):
            self.assertIn(required, wip)

        for name in DATA_FILES:
            raw = (DATA / f"{name}.yml").read_text(encoding="utf-8")
            self.assertNotRegex(raw, HARVESTABLE_EMAIL_RE, name)
            self.assertNotRegex(raw, PHONE_LABEL_RE, name)

    def test_readme_documents_stable_update_paths(self):
        readme = README.read_text(encoding="utf-8")
        for expected in (
            "https://siyi-yu-epi.github.io",
            "index.md",
            "assets/img/profile.jpg",
            "assets/files/Siyi-Yu-CV.pdf",
            "assets/css/site.css",
            "scripts/prepare_assets.py",
            "data-tab-title",
            "_data/publications.yml",
        ):
            self.assertIn(expected, readme)
        self.assertNotRegex(readme, PHONE_LABEL_RE)


if __name__ == "__main__":
    unittest.main()
