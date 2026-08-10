# Siyi (Ruth) Yu - Academic Profile

Source repository for [https://siyi-yu-epi.github.io](https://siyi-yu-epi.github.io).

The site uses GitHub Pages and the official Minimal Jekyll theme.

## Updating the site

- Edit academic profile content in **index.md**. The page is organised into tabs: each `<div class="tab-panel" ... markdown="1">` block is one tab, its label comes from `data-tab-title`, and its `id` is the URL fragment (for example `/#research`). Keep `markdown="1"` so the body of each panel stays plain Markdown.
- Edit the sidebar (name, role, affiliation, contact line, profile photo, external links) in **_config.yml**.
- Replace the public portrait at **assets/img/profile.jpg**. It is displayed as a small circular thumbnail; sizing lives in `assets/css/site.css`.
- Replace the phone-free public CV at **assets/files/Siyi-Yu-CV.pdf**.
- To rebuild both public assets from their private sources, run **scripts/prepare_assets.py** with explicit source paths.

## Layout and behaviour

- **assets/css/site.css** overrides the Minimal theme: it widens the content column, narrows the outer page margins, sizes the profile photo, and styles the tab strip.
- **assets/js/tabs.js** turns the panels in `index.md` into an accessible tab set. Without JavaScript the panels render stacked, so no content is ever hidden from readers or crawlers.
- Both files are loaded by **_includes/head-custom.html**.

## Conventions

- The email address is published in obfuscated form (`yu1344 at purdue dot edu`) and there is no `mailto:` link anywhere on the site, to keep it away from address harvesters. `tests/test_site_contract.py` enforces this.
- Keep public claims aligned with the latest approved CV. Do not commit private source files or contact information that is not intended for publication.

## Tests

```
python -m unittest discover -s tests
```
