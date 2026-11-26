#!/usr/bin/env python3
"""Build the AI in energy planning long-read page."""
import re, json, pathlib

ROOT = pathlib.Path(__file__).parent

REFS = {
 1: ("COP31 Presidency (2026). COP31 President Designate and Minister Kurum unveils COP31 Action Agenda.", "https://iklim.gov.tr/en/cop31-president-designate-and-minister-kurum-unveils-cop31-action-agenda-news-4985"),
 2: ("European Commission (2026). Report on the energy efficiency of data centres in the EU.", "https://build-up.ec.europa.eu/en/resources-and-tools/publications/report-energy-efficiency-data-centres-eu"),
 3: ("EY (2025). Future of Energy survey: technology adoption and workforce readiness.", "https://www.ey.com/content/dam/ey-unified-site/ey-com/en-us/campaigns/energy-resources/documents/ey-ogc-future-of-energy-external-report.pdf"),
 4: ("IRENA (2026). Digitalisation and AI for transforming power systems: case studies from IRENA Innovation Week 2025.", "https://www.irena.org/Publications/2026/May/Digitalisation-and-AI-for-transforming-power-systems"),
 5: ("TransitionZero (2024). TransitionZero launches global solar plant dataset.", "https://www.transitionzero.org/press/transitionzero-launches-tz-sam"),
 6: ("VIDA. Planning.", "https://vida.place/applications/planning"),
 7: ("Stockholm Environment Institute (2026). Responsible use of AI for climate planning: a preview of LEAP 2027.", "https://leap.sei.org/"),
 8: ("Tkachenko, N. et al. (2026). Governing artificial intelligence for energy planning and transition: Shared AI Governance for Energy Systems (SAGES), a briefing note. Cambridge Open Engage.", "https://doi.org/10.33774/coe-2026-0gzfx"),
 9: ("LTES Network (2025). Plan to Accelerate Solution: AI. UNFCCC Plans to Accelerate Solutions catalogue.", "https://climateaction.unfccc.int/assets/documents/121_.pdf"),
 10: ("COP31 Presidency and ITU (2026). Antalya Artificial Intelligence Pledge.", "https://cop31.tr/assets/docs/action-agenda/cop31-antalya-ai-pledge-text.pdf"),
 11: ("IRENA (2026). Energy Planning Week 2026.", "https://www.irena.org/Events/2026/Dec/Energy-Planning-Week-2026"),
 12: ("Rural Electrification Agency (2026). Nigeria Electrification Programme and DARES.", "https://nep.rea.gov.ng/"),
 13: ("TransitionZero (2026). Introducing Conductor and TZ-HiGHS: launch webinar.", "https://www.transitionzero.org/events/introducing-conductor-and-tz-highs-launch-webinar"),
 14: ("TransitionZero (2026). AMP AI assistant.", "https://docs.transitionzero.org/platform/amp-ai-assistant"),
}

BODY = []


def h2(num, text, anchor):
    if text:
        BODY.append(f'<section class="sec" id="{anchor}"><h2>{text}</h2>')
    else:
        BODY.append(f'<section class="sec sec-first" id="{anchor}">')


def p(text, cls=""):
    c = f' class="{cls}"' if cls else ""
    BODY.append(f"<p{c}>{text}</p>")


def endsec():
    BODY.append("</section>")


def figure(fid, title, sub, note, chart_js, height="360px", cls=""):
    BODY.append(f"""
<figure class="fig {cls}" id="{fid}">
  <div class="fig-head"><h3>{title}</h3><p>{sub}</p></div>
  <div class="chart" id="{fid}-chart" style="height:{height}"></div>
  <figcaption>{note}</figcaption>
</figure>""")


def stat_band(items):
    cells = "".join(
        f'<div class="stat"><p class="stat-n">{v}</p><p class="stat-l">{l}</p></div>' for v, l in items
    )
    BODY.append(f'<div class="stats">{cells}</div>')


def clusters():
    items = [
        ("01", "Monitoring"),
        ("02", "Forecasting"),
        ("03", "Operational optimisation"),
        ("04", "End-user automation"),
        ("05", "Transparency"),
    ]
    cards = "".join(
        f'<li class="cluster"><span class="cluster-n">{n}</span><h3>{t}</h3></li>'
        for n, t in items
    )
    BODY.append(f"""
<figure class="fig info" id="clusters">
  <div class="fig-head"><h3>Five value clusters</h3><p>How IRENA's 2026 review sorts digital and AI applications in power systems.</p></div>
  <ol class="cluster-grid">{cards}</ol>
  <figcaption>Source: IRENA (2026), Digitalisation and AI for transforming power systems.</figcaption>
</figure>""")


def commitments():
    items = [
        "AI as an empowering partner",
        "Human accountability for final decisions",
        "Trust that is proportional, purposeful and testable",
        "Respect for national sovereignty",
        "Collective progress towards just energy futures",
    ]
    rows = "".join(
        f'<li><span class="cm-n">{i}</span><h3>{t}</h3></li>'
        for i, t in enumerate(items, 1)
    )
    BODY.append(f"""
<figure class="fig info" id="sages">
  <div class="fig-head"><h3>Five commitments of the SAGES framework</h3><p>Published in June 2026, with IRENA among its co-authors.</p></div>
  <ol class="commit">{rows}</ol>
  <figcaption>Source: Tkachenko et al. (2026), Shared AI Governance for Energy Systems.</figcaption>
</figure>""")


def actions():
    items = [
        "Planning frameworks that treat data centre demand as a variable",
        "A knowledge platform",
        "Flexible connection rules",
        "Standards for secure data exchange",
        "Skills programmes",
        "Guidance for development finance",
    ]
    chips = "".join(f"<li>{x}</li>" for x in items)
    BODY.append(f"""
<figure class="fig info" id="actions">
  <div class="fig-head"><h3>Actions for 2026 to 2028</h3><p>Under the LTES Network plan on AI and digitalisation.</p></div>
  <ol class="chips">{chips}</ol>
  <figcaption>Source: LTES Network (2025), Plan to Accelerate Solution: AI.</figcaption>
</figure>""")


# ---------------------------------------------------------------- article
h2("01", "", "s1")
p("COP31 closed with electrification at the centre of the climate agenda. The Presidency's target of a 35% share for electricity in final energy demand by 2035 sits alongside the global goal of tripling renewable capacity and doubling energy efficiency by 2030 [1][9]. Both land on national planning offices, which must turn them into grids, storage and project pipelines inside budget cycles of months.")
p("Demand pressure is arriving fastest in Europe. Data centres in the EU consumed 68 TWh of electricity in 2024, a figure the European Commission projects will reach 114 TWh by 2030, or 3.2% of EU electricity demand [2].")
figure("eu-dc", "Data centre electricity demand in the EU",
       "Terawatt hours consumed, 2024 and projected 2030.",
       "Data: European Commission (2026), Report on the energy efficiency of data centres in the EU. The 2030 figure equals 3.2% of projected EU electricity demand.",
       "euDC()")
p("Skills set a second limit. In EY's 2025 survey of oil and gas and chemicals executives, 82% cited too few workers with the right skills as a challenge to adopting new technology [3]. A model that cannot be fed, checked or explained becomes a liability in a ministry.")
endsec()

h2("02", "What AI changes", "s2")
p("IRENA's 2026 review of digitalisation and AI in power systems maps the field into five value clusters: monitoring, forecasting, operational optimisation, end-user automation and transparency [4]. Six case studies from IRENA Innovation Week 2025 cover congestion management, predictive maintenance, non-firm connections, interoperability standards and virtual power plants. Digital tools unlock latent grid capacity, reduce curtailment and improve asset performance.")
clusters()
p("In Sierra Leone, a national electrification platform built with the geospatial firm VIDA maps settlements, buildings and grid lines with machine learning, then matches each community to grid extension, a mini-grid or standalone solar. Its site list holds 21,075 settlements [6]. Ministries, funders and developers work from one living picture instead of separate spreadsheets, which shortens the distance between a least-cost plan and a project pipeline.")
p("Nigeria runs the same logic at national scale. The Rural Electrification Agency reports the same chain of figures for the Nigeria Electrification Programme and the DARES programme that builds on it: pipeline, mini-grid sites, connections, installed capacity and disbursement [12]. It counts 176 mini-grids and 7.8 million people reached, against a DARES target of 17.5 million [12].")
stat_band([("176", "mini-grids deployed under the Nigeria Electrification Programme"),
           ("7.8 m", "people reached with new or improved electricity"),
           ("17.5 m", "people the DARES programme aims to reach")])
p("Almost 80,000 people in 210 countries and territories use LEAP, the Low Emissions Analysis Platform developed by the Stockholm Environment Institute, and at least 65 countries have used it for their nationally determined contributions, long-term strategies or transparency reports [7]. The 2027 version adds AI that lets non-specialist planners explore a model in natural language and interrogate its assumptions. AI widens who can test a pathway, while the calculations stay in the model.")
figure("leap", "Who uses LEAP",
       "Each square is one country or territory. Filled squares are the 65 that have used LEAP for a nationally determined contribution, long-term strategy or transparency report.",
       "Data: Stockholm Environment Institute (2026). User figure of almost 80,000 people across 210 countries and territories.",
       "leapWaffle()", height="300px")
p("The same shift reaches the tools themselves. TransitionZero, a non-profit, set AI agents on the interior-point method of HiGHS, the open-source solver under many energy models, and reports a prototype up to 16 times faster than the current release on the Open Energy Benchmark [13]. Solver time sets how many scenarios a ministry can test before a decision is due, so a gain inside the code changes what a planning office can put in front of a minister.")
figure("solver", "Solver speed, relative to the current HiGHS release",
       "Reported speed-up of the interior-point method on the Open Energy Benchmark. HiGHS current release = 1.",
       "Data: TransitionZero (2026), for a prototype fork. Vendor-reported benchmark; not an independent evaluation.",
       "solver()", height="280px")
p("One layer up, the assistant is becoming part of the workflow. A planner can ask it to draft a scenario, check inputs against regional data or explain why a run failed, then accept or reject each edit before it is applied [14]. The instructive part is how the safeguards are split: a tightly constrained assistant for general users, and a local tool where an experienced modeller connects their own AI and keeps the model and data on their own machine [13]. Control follows expertise.")
endsec()

h2("03", "Who governs the result", "s3")
p("Institutional risk matters more than technical risk. A government that cannot inspect a model, trace its inputs or reproduce its output has lost control of the plan, whatever the accuracy of the forecast. The Shared AI Governance for Energy Systems (SAGES) framework, published in June 2026 with IRENA among its co-authors, sets five commitments [8]:")
commitments()
p("Working groups cover vendor engagement, demonstration tools, sovereignty, and capacity building.")
endsec()

h2("04", "The delivery route", "s4")
p("Delivery now has a vehicle in the COP Action Agenda. The LTES Network hosts a Plan to Accelerate Solutions on AI and digitalisation for a smart, resilient and efficient energy system, tied to tripling renewables and doubling energy efficiency [9]. Actions for 2026 to 2028 include planning frameworks that treat data centre demand as a variable, a knowledge platform, flexible connection rules, standards for secure data exchange, skills programmes and guidance for development finance.")
actions()
p("At COP31, IRENA also supported the Antalya AI Pledge, which asks signatories to power AI infrastructure with zero- and low-emission energy and to integrate it into electricity grids [10].")
endsec()

h2("05", "What Energy Planning Week adds", "s5")
p("Energy Planning Week 2026, co-hosted by IRENA and GET.transform in Bonn from 1 to 4 December 2026, is the first working gathering of the planning community after COP31 [11]. It brings together the teams behind these tools, with applications grouped around demand and load forecasting, scenario development, and data quality assurance. A session on AI for energy planning is built for adoption: a planner can see how a method performs on a real system, and that evidence feeds the LTES Network's 2026 to 2028 actions, which depend on countries willing to test new methods in live cases.")
p("The promise of AI in energy planning is narrower than the publicity and more useful. It gives a small team the coverage of a larger one, provided the institution keeps ownership of the model, the data and the decision.", "closing")
endsec()

BODY_HTML = "\n".join(BODY)

# ------------------------------------------------- renumber citations
used = []
for m in re.finditer(r"\[(\d+)\]", BODY_HTML):
    n = int(m.group(1))
    if n not in used:
        used.append(n)
missing = [n for n in used if n not in REFS]
assert not missing, f"cited but undefined: {missing}"
order = sorted(used, key=lambda n: used.index(n))
new = {old: i + 1 for i, old in enumerate(order)}

def sub(m):
    return f'<a class="cite" href="#r{new[int(m.group(1))]}" title="Reference {new[int(m.group(1))]}">[{new[int(m.group(1))]}]</a>'

BODY_HTML = re.sub(r"\s?\[(\d+)\]", lambda m: "\u00a0" + sub(m), BODY_HTML)

refs_html = "\n".join(
    f'<li id="r{new[o]}"><span class="ref-n">{new[o]}</span><span>{REFS[o][0]} <a href="{REFS[o][1]}" target="_blank" rel="noopener">{REFS[o][1]}</a></span></li>'
    for o in order
)

CSS = (ROOT / "styles.css").read_text()
JS = (ROOT / "app.js").read_text()

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI in energy planning: closing the delivery gap | IRENA Expert Insight</title>
<meta name="description" content="Planning offices must turn COP31's electrification targets into grids and projects. Where AI shortens the work, and why governance decides whether the gain holds.">
<meta property="og:title" content="AI in energy planning: closing the delivery gap">
<meta property="og:description" content="Where AI shortens the planning work, and why governance decides whether the gain holds.">
<meta property="og:type" content="article">
<link rel="preload" href="fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap mast-in">
    <p class="brand">IRENA <span>Expert Insight</span></p>
    <p class="mast-meta">Energy Planning Week 2026 · Bonn, 1 to 4 December</p>
  </div>
</header>
<main id="main">
  <article>
    <div class="wrap lede">
      <p class="kicker">Artificial intelligence and energy planning</p>
      <h1>AI in energy planning:<br>closing the delivery gap</h1>
      <p class="dek">Planning offices must turn COP31's electrification targets into grids and projects. AI is already shortening parts of that work, and governance now decides whether the gain holds.</p>
      <p class="byline">Simon Benmarraze, Nadeem Goussous and Juan Jose Garcia Mendez<span class="affil">IRENA</span></p>
      <p class="dateline">26 November 2026 · 7 minute read</p>
    </div>
    <div class="wrap prose">
{BODY_HTML}
      <section class="sec refs" id="refs">
        <h2>References</h2>
        <ol class="reflist">{refs_html}</ol>
      </section>
    </div>
  </article>
</main>
<footer class="foot">
  <div class="wrap">
    <p class="foot-note">The designations employed and the presentation of material herein do not imply the expression of any opinion on the part of IRENA concerning the legal status of any region, country, territory, city or area or of its authorities, or concerning the delimitation of frontiers or boundaries. The mention of specific companies, projects or products does not imply that they are endorsed or recommended by IRENA in preference to others of a similar nature that are not mentioned.</p>
    <p class="foot-credit">IRENA Expert Insight · Draft text for Energy Planning Week 2026</p>
  </div>
</footer>
<script src="vendor/echarts.min.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

(ROOT / "index.html").write_text(page)
(ROOT / "styles.css").write_text(CSS)
(ROOT / "app.js").write_text(JS)
print("built index.html", len(page), "bytes")
print("citations used:", used)
print("renumber:", new)
