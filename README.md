# Siyi (Ruth) Yu - Academic Profile

Source repository for [https://siyi-yu-epi.github.io](https://siyi-yu-epi.github.io).

The site uses GitHub Pages and the official Minimal Jekyll theme.

## Where each kind of content lives

Prose lives in Markdown; anything that is a *list of things* lives in `_data/`, so
adding a paper is a few lines of YAML instead of hand-formatted Markdown.

| To change | Edit |
| --- | --- |
| Bio, section intros, contact text | **index.md** |
| Published and forthcoming papers | **_data/publications.yml** |
| Work in progress | **_data/working_papers.yml** |
| News items on the About tab | **_data/news.yml** |
| Courses taught | **_data/courses.yml** |
| Service and leadership roles | **_data/service.yml** |
| Name, role, affiliation, contact line, photo, CV date, external links | **_config.yml** |

Every data file starts with a comment listing the fields it accepts. All fields
except `title` are optional, so short entries stay short.

### Adding a publication

```yaml
- title: "Paper title"
  authors: "Author, A., & Yu, S."
  venue: "Journal Name"
  detail: "12, 345678"
  year: 2027
  status: "Forthcoming"        # optional badge
  abstract: "Renders as a collapsible Abstract toggle."
  links:
    - label: "DOI"
      url: "https://doi.org/..."
```

### Adding or renaming a tab

Each `<div class="tab-panel" ... markdown="1">` block in **index.md** is one tab.
The label comes from `data-tab-title` and the `id` is the URL fragment (for
example `/#research`). Keep `markdown="1"` so the panel's prose stays ordinary
Markdown, and give each heading an explicit id (`{: #about-heading}`) so it does
not collide with the panel's own id.

## Assets

- Replace the public portrait at **assets/img/profile.jpg**. It renders as a small
  circular thumbnail; sizing lives in `assets/css/site.css`.
- Replace the phone-free public CV at **assets/files/Siyi-Yu-CV.pdf**, and update
  `cv_updated` in `_config.yml` so the sidebar date stays honest.
- To rebuild both public assets from their private sources, run
  **scripts/prepare_assets.py** with explicit source paths.

## Layout and behaviour

- **assets/css/site.css** overrides the Minimal theme: page frame and margins, the
  sidebar, and the paper / entry / news / link list components.
  The design uses a white background, charcoal system typography, and a deep
  blue accent for links and the active tab. Lists are separated by whitespace;
  the profile becomes a compact header on smaller screens. Scholar, SSRN, and
  LinkedIn use text links rather than externally loaded icons.
- **assets/js/tabs.js** turns the panels in `index.md` into an accessible tab set
  with arrow-key navigation and `#fragment` deep links. Without JavaScript the
  panels render stacked, so no content is ever hidden from readers or crawlers.
  Printing also shows every panel.
- Both files are loaded by **_includes/head-custom.html**.
- **_includes/papers.html**, **entries.html**, and **news.html** render the data files.

## Conventions

- The email address is published in obfuscated form (`yu1344 at purdue dot edu`)
  and there is no `mailto:` link anywhere on the site, to keep it away from
  address harvesters. `tests/test_site_contract.py` enforces this.
- Keep public claims aligned with the latest approved CV. Do not commit private
  source files or contact information that is not intended for publication.

## Tests

```
python -m unittest discover -s tests
```
