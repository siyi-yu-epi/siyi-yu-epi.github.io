from pathlib import Path
import re
import unittest

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
PHONE_LABEL_RE = re.compile(r"\bphone\s*:", re.IGNORECASE)
HARVESTABLE_EMAIL_RE = re.compile(r"mailto:|yu1344@purdue\.edu", re.IGNORECASE)
OBFUSCATED_EMAIL = "yu1344 at purdue dot edu"
TAB_TITLES = ("About", "Research", "Teaching", "Engagement")


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

    def test_config_selects_minimal_and_stable_assets(self):
        self.assertTrue(CONFIG.is_file(), f"Missing {CONFIG}")
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
        self.assertTrue(LAYOUT.is_file(), f"Missing {LAYOUT}")
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

        stylesheet = STYLESHEET.read_text(encoding="utf-8")
        self.assertIn(".profile-photo", stylesheet)
        self.assertIn(".tabs__list", stylesheet)
        # The theme's fixed 860px column is what creates the wide side margins.
        self.assertIn("div.wrapper", stylesheet)
        self.assertIn("max-width: 1500px", stylesheet)

        script = TABS_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('setAttribute("role", "tab")', script)
        self.assertIn('setAttribute("role", "tabpanel")', script)

    def test_index_declares_four_tabs_with_all_approved_content(self):
        self.assertTrue(INDEX.is_file(), f"Missing {INDEX}")
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("<div class=\"tabs\" data-tabs", index)
        for title in TAB_TITLES:
            self.assertIn(f'data-tab-title="{title}"', index)
            self.assertIn(f"## {title}", index)
            # Without an explicit id, kramdown auto-generates one from the
            # heading text that collides with the panel's own id.
            self.assertIn(f"{{: #{title.lower()}-heading}}", index)
        self.assertEqual(index.count('class="tab-panel"'), len(TAB_TITLES))
        # markdown="1" is what lets kramdown parse Markdown inside the panels.
        self.assertEqual(index.count('markdown="1"'), len(TAB_TITLES))
        for required_text in (
            "### Research themes",
            "### Selected publications",
            "### Work in progress",
            "The Birth Control Service Mix Post-Dobbs",
            "Impeding Drug Newcomers?",
            "Demand Displacement in the GLP-1 Market",
            "Artificial Intelligence in Marketing Research",
            "Price versus service satisfaction",
            "Pharmaceutical Pricing",
            "{{ site.email_display }}",
            "site.cv_path | relative_url",
            "https://business.purdue.edu/",
        ):
            self.assertIn(required_text, index)
        self.assertNotRegex(index, HARVESTABLE_EMAIL_RE)
        self.assertNotRegex(index, PHONE_LABEL_RE)

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
        ):
            self.assertIn(expected, readme)
        self.assertNotRegex(readme, PHONE_LABEL_RE)


if __name__ == "__main__":
    unittest.main()
