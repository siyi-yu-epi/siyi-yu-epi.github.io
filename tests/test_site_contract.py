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
INDEX = ROOT / "index.md"
README = ROOT / "README.md"
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

    def test_config_selects_minimal_and_stable_assets(self):
        self.assertTrue(CONFIG.is_file(), f"Missing {CONFIG}")
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
        self.assertTrue(LAYOUT.is_file(), f"Missing {LAYOUT}")
        layout = LAYOUT.read_text(encoding="utf-8")
        self.assertIn('alt="{{ site.logo_alt | escape }}"', layout)
        self.assertIn('href="mailto:{{ site.email }}"', layout)
        self.assertIn("site.cv_path | relative_url", layout)
        self.assertNotIn("<script", layout.lower())
        self.assertNotRegex(layout, PHONE_LABEL_RE)

    def test_index_contains_all_approved_sections_and_links(self):
        self.assertTrue(INDEX.is_file(), f"Missing {INDEX}")
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


if __name__ == "__main__":
    unittest.main()
