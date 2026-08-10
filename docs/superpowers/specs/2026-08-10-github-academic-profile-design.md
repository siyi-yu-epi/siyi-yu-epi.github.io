# GitHub Academic Profile Design

Date: 2026-08-10

## Purpose

Create a restrained, one-page academic profile for Siyi (Ruth) Yu at `https://siyi-yu-epi.github.io`. The page should help academic peers and prospective collaborators understand her research quickly, find selected work, and download a public CV.

## Audience and success criteria

The primary audience is academic peers and prospective collaborators. The first screen should establish Ruth's identity, appointment, institution, and research focus without promotional language or visual clutter.

The first version succeeds when:

- a visitor can identify Ruth's appointment, institution, and research themes within a few seconds;
- current projects and selected publications are easy to scan;
- the public CV is prominent and contains no phone number;
- the profile photograph displays cleanly on desktop and mobile;
- the site builds and publishes through GitHub Pages without a custom deployment service;
- content can be maintained by editing straightforward text files.

## Visual direction

Use GitHub Pages' official `jekyll-theme-minimal` theme with its familiar two-column desktop layout and stacked mobile layout. Preserve the theme's quiet typography, white background, blue links, and generous whitespace.

Do not add animations, oversized slogans, decorative cards, gradients, shadows, a dark mode, or a custom color system. The page should look like a classic academic GitHub Pages site.

## Page structure

### Sidebar

The sidebar contains, in order:

1. A web-optimized 4:5 head-and-shoulders derivative of the supplied profile photograph. Use a simple rectangular presentation with no filter, shadow, decorative frame, or circular crop. Keep the source photograph unchanged.
2. `Siyi (Ruth) Yu`
3. `Clinical Assistant Professor of Management`
4. `Mitch Daniels School of Business, Purdue University`
5. A mail link for `yu1344@purdue.edu`
6. A prominent `Download CV` link to the sanitized public PDF

Do not display a phone number.

### Main column

The main column contains these sections:

1. **About**
2. **Research themes**
3. **Current projects**
4. **Selected publications**
5. **Teaching and service**
6. **Contact**

The site is a single page. It does not need separate navigation pages or a blog.

## Approved content direction

### About

Use this concise first-person opening:

> I am a Clinical Assistant Professor of Management at Purdue University. My research focuses on healthcare marketing, public policy, and large language models, using causal inference, discrete choice models, and machine learning.

### Research themes

Present three short themes rather than long prose:

- Healthcare decisions and public policy
- Pharmaceutical markets and physician adoption
- Artificial intelligence in marketing research

### Current projects

List the following projects with collaborators and status where the CV supplies them:

- **The Birth Control Service Mix Post-Dobbs: How Abortion Bans Reshape Americans' Choices of Contraceptive Procedures** - with Qiang Liu, Hongju Liu, and Yong Cai; under review at M&SOM.
- **Impeding Drug Newcomers? Investigating the Impact of Integrated Delivery Networks on Physician New Drug Adoption** - with Hongju Liu, Qiang Liu, and Yong Cai; manuscript ready for submission.
- **Demand Displacement in the GLP-1 Market: Descriptive Evidence and Within-Patient Analysis** - with Sungjin Kim, Sungsik Park, Qiang Liu, and Yong Cai.
- **Artificial Intelligence in Marketing Research: An Umbrella Review** - with Qiang Liu, Lizi Xiang, and Yaxuan Ran.

Statuses are factual labels, not visual badges. Do not invent abstracts, findings, links, or publication claims.

### Selected publications

Use ordinary citation text rather than cards and include these two entries:

- Weng, W., Yang, Z., & Yu, S. (2026). Price versus service satisfaction: The role of direct and indirect leasing in the B2B sector. *Journal of Business Research, 215*, 116312. https://doi.org/10.1016/j.jbusres.2026.116312
- Liu, Q., Yu, S., Wen, S., & Cai, Y. (2026). "Pharmaceutical Pricing," in *Handbook of Pricing Research in Marketing* (forthcoming), edited by Vithala Rao and K. Sudhir.

### Teaching and service

Keep this section compact. Mention current Purdue teaching in Marketing Research and Marketing Management, followed by the current AI in Marketing Committee chair role and Daniels Insights Blog liaison role. Direct visitors to the CV for the complete record of teaching, presentations, service, honors, grants, memberships, and skills.

### Contact

End with one sentence inviting research and collaboration inquiries through the institutional email address. Do not add a contact form, phone number, or social-media links that the user has not supplied.

## Assets and privacy

### Profile photograph

- Source: the user-supplied `profile.jpg` outside the repository.
- Repository target: `assets/img/profile.jpg`.
- Create a web-sized derivative suitable for the sidebar; do not modify the source file.
- Use alt text `Portrait of Siyi (Ruth) Yu`.
- Preserve natural color and appearance.

### Public CV

- Source: the user-supplied `CV_Ongoing.pdf` outside the repository.
- Repository target: `assets/files/Siyi-Yu-CV.pdf`.
- Create a public derivative that removes the phone number from both visible page content and extractable PDF text.
- Preserve the source PDF unchanged.
- Keep the institutional email and office information unless another privacy issue is discovered during verification.
- Confirm the public derivative still renders as a polished two-page CV.

## Technical architecture and data flow

Use GitHub Pages' native Jekyll support:

- `_config.yml` selects `jekyll-theme-minimal`, sets the site title and description, and points the theme's logo field to the profile image.
- `_layouts/default.html` is a small override of Minimal's stock layout. It keeps the official theme stylesheet while adding descriptive portrait alt text and the approved sidebar email and CV links.
- `index.md` contains the approved homepage text and links.
- `assets/img/profile.jpg` contains the optimized profile derivative.
- `assets/files/Siyi-Yu-CV.pdf` contains the sanitized public CV.

GitHub Pages reads the repository from the configured publishing branch, runs the supported Jekyll build, and serves static HTML and assets. The browser loads only static content. There is no application state, database, form submission, analytics, tracking, or client-side JavaScript.

## Failure handling

Because the site is static, failures are limited to build errors, broken links, or missing assets. Treat any of these as a release blocker:

- GitHub Pages/Jekyll cannot build the repository;
- the profile image or CV link returns a missing-file response;
- an external publication link is malformed;
- the public CV still contains the phone number visually or in extracted text;
- content overflows or becomes unreadable on a narrow screen.

Do not add custom error UI. Prevent these failures through pre-publication checks.

## Accessibility and responsive behavior

- Use one page-level heading followed by correctly nested section headings.
- Use descriptive link text such as `Download CV`, not `click here`.
- Add alt text to the profile photograph.
- Retain the Minimal theme's readable contrast and visible keyboard focus styles.
- Ensure the sidebar stacks above the main content on small screens without horizontal scrolling.
- Do not encode meaning through color alone.

## Verification and acceptance checks

Before publication:

1. Run `bundle exec jekyll build` when a compatible local GitHub Pages runtime is available. Otherwise, validate YAML, front matter, internal paths, and assets locally, then require the GitHub Pages build to succeed before calling publication complete.
2. Verify the homepage, profile image, email link, CV link, DOI, and any other external links.
3. Render and inspect both pages of the sanitized CV.
4. Extract text from the public CV and search the repository to confirm the phone number is absent.
5. Review the homepage at narrow mobile, tablet, and desktop widths.
6. Confirm headings, link focus, alt text, and keyboard navigation.
7. Confirm the source photograph and source CV were not modified.
8. Verify the published `https://siyi-yu-epi.github.io` page after deployment.

## Maintenance

Future research, publication, teaching, and service updates should be made in `index.md`. Replace the public CV at the same stable path so existing links continue to work. Keep all claims aligned with the latest approved CV and do not infer new statuses or collaborators.

## Out of scope for the first version

- Custom domain
- Blog or news feed
- Contact form
- Analytics or visitor tracking
- Dark mode
- Search
- Multiple pages or routes
- Automated publication syncing
