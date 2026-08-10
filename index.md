---
layout: default
---

<!--
  HOW THIS PAGE IS PUT TOGETHER

  Prose lives here, in Markdown. Anything that is a *list of things* lives in
  _data/ and is rendered by an include, so adding a paper or a news item is a
  few lines of YAML rather than hand-formatted Markdown:

      publications   -> _data/publications.yml
      working papers -> _data/working_papers.yml
      news           -> _data/news.yml
      courses        -> _data/courses.yml
      service        -> _data/service.yml

  Each tab-panel div below becomes one tab. The tab label comes from
  data-tab-title and the id is the URL fragment (e.g. .../#research). Keep the
  markdown attribute on each panel so its prose is still ordinary Markdown, and
  give each heading an explicit id so it does not collide with the panel id.
-->

<div class="tabs" data-tabs data-tabs-label="Profile sections">

<div class="tab-panel" id="about" data-tab-title="About" markdown="1">

## About
{: #about-heading}

I am a Clinical Assistant Professor of Management in the Marketing Department at the [Daniels School of Business](https://business.purdue.edu/), [Purdue University](https://www.purdue.edu/). I have a Ph.D. in Marketing and a B.A. in Economics from Peking University. 
{: .lede}

My research studies how people and physicians make healthcare decisions, and how public policy and market structure reshape those choices. I work on healthcare marketing, pharmaceutical markets, and the use of large language models in marketing research, combining causal inference, discrete choice models, and machine learning. Recent projects examine how state abortion bans changed the contraceptive service mix, how integrated delivery networks affect physician adoption of new drugs, and how demand shifts across the GLP-1 market.

### News
{: #news-heading}

{% include news.html items=site.data.news %}


### Contact
{: #contact-heading}

For research and collaboration inquiries, email me at {{ site.email_display }}.


</div>

<div class="tab-panel" id="research" data-tab-title="Research" markdown="1">

## Research
{: #research-heading}

### Research themes
{: #themes-heading}

- **Healthcare decisions and public policy**
- **Pharmaceutical markets and physician adoption**
- **Artificial intelligence in marketing research**

### Publications
{: #publications-heading}

{% include papers.html items=site.data.publications numbered=true %}

### Work in progress
{: #wip-heading}

{% include papers.html items=site.data.working_papers %}

</div>

<div class="tab-panel" id="teaching" data-tab-title="Teaching" markdown="1">

## Teaching
{: #teaching-heading}

### Courses
{: #courses-heading}

{% include entries.html items=site.data.courses %}



For my complete teaching record, including evaluations and past offerings, see my [curriculum vitae]({{ site.cv_path | relative_url }}).

</div>

<div class="tab-panel" id="engagement" data-tab-title="Engagement" markdown="1">

## Engagement
{: #engagement-heading}

### Service and leadership
{: #service-heading}

{% include entries.html items=site.data.service %}



For my complete record of presentations, service, honors, grants, memberships, and skills, see my [curriculum vitae]({{ site.cv_path | relative_url }}).

</div>

</div>
