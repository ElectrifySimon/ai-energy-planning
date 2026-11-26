#!/usr/bin/env python3
"""Build the AI in energy planning long-read page."""
import re, math, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT

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

B = []

def p(text, cls=""):
    c = f' class="{cls}"' if cls else ""
    B.append(f"<p{c}>{text}</p>")

def sec(anchor, title=None):
    if title:
        B.append(f'<section class="sec" id="{anchor}" data-reveal><div class="text"><h2>{title}</h2>')
    else:
        B.append(f'<section class="sec" id="{anchor}" data-reveal><div class="text">')

def endsec():
    B.append("</div></section>")

def openfig(fid, title, tag, sub):
    B.append(f"""
<figure class="fig" id="{fid}" data-reveal>
  <div class="fig-top"><h3>{title}</h3><span class="tag">{tag}</span></div>
  <p class="fig-sub">{sub}</p>""")

def closefig(caption):
    B.append(f"  <figcaption>{caption}</figcaption>\n</figure>")

def fig_demand():
    openfig("f-demand", "Data centre electricity demand, EU", "One scale",
            "Terawatt hours consumed in 2024 and projected for 2030.")
    B.append('<div class="rails">')
    for year, kind, v, cls in [("2024", "actual", 68, ""), ("2030", "projected", 114, " future")]:
        fill = round(v / 120 * 100, 2)
        B.append(f"""
  <div class="rail" data-rail="{v}">
    <div class="rail-year">{year}<small>{kind}</small></div>
    <div class="track"><span class="fill{cls}" style="--fill:{fill}%"></span></div>
    <div class="rail-v">{v}<small>TWh</small></div>
  </div>""")
    B.append("""</div>
  <div class="scale"><span>0</span><span>30</span><span>60</span><span>90</span><span>120 TWh</span></div>
  <div class="rail-note">
    <span><span class="delta">+46 TWh</span> over six years</span>
    <span>2030 share of EU electricity demand: <b>3.2%</b></span>
  </div>""")
    closefig("Data: European Commission (2026). Bars share one scale from 0 to 120 TWh.")

def fig_clusters():
    items = [("01", "Monitoring"), ("02", "Forecasting"), ("03", "Operational optimisation"),
             ("04", "End-user automation"), ("05", "Transparency")]
    B.append('<figure class="fig" id="f-clusters" data-reveal>')
    B.append('<div class="fig-top"><h3>Five value clusters</h3><span class="tag">Framework</span></div>')
    B.append('<p class="fig-sub">How IRENA\'s 2026 review sorts digital and AI applications in power systems.</p>')
    B.append('<ol class="band">')
    for n, t in items:
        B.append(f'<li><span class="idx">{n}</span><h3>{t}</h3></li>')
    B.append('</ol>')
    closefig("Source: IRENA (2026), Digitalisation and AI for transforming power systems.")

def fig_nigeria():
    reached, target, scale = 7.8, 17.5, 20.0
    openfig("f-nigeria", "People reached against the DARES target", "Progress",
            "Millions of people with new or improved electricity. Both lanes share one scale to 20 million.")
    f1 = round(reached / scale * 100, 2)
    f2 = round(target / scale * 100, 2)
    gap = round(f2 - f1, 2)
    B.append(f"""
  <div class="lanes">
    <div class="lane">
      <div class="lane-h"><span>Reached, Nigeria Electrification Programme</span><b>7.8 m</b></div>
      <div class="lane-track"><span class="lane-fill" style="--fill:{f1}%"></span></div>
    </div>
    <div class="lane">
      <div class="lane-h"><span>Target, DARES</span><b>17.5 m</b></div>
      <div class="lane-track"><span class="lane-fill" style="--fill:{f2}%"></span><span class="gap" style="--from:{f1}%;--gapw:{gap}%"><em>9.7 m gap</em></span></div>
    </div>
  </div>
  <div class="scale"><span>0</span><span>5</span><span>10</span><span>15</span><span>20 million</span></div>
  <div class="legend">
    <span><i class="sw-blue"></i>People reached</span>
    <span><i class="sw-hatch"></i>Gap to the DARES target</span>
  </div>""")
    closefig("Data: Rural Electrification Agency (2026), Nigeria Electrification Programme and DARES.")

def fig_leap():
    openfig("f-leap", "Who uses LEAP", "Unit chart",
            "One dot for each country or territory, 210 in total. Filled dots are the 65 that have used LEAP for a nationally determined contribution, long-term strategy or transparency report.")
    B.append("""
  <div class="dots-wrap">
    <svg id="leap-grid" role="img" aria-label="Unit chart: 65 of 210 countries and territories have used LEAP for a nationally determined contribution, long-term strategy or transparency report."></svg>
    <div class="dot-caption">
      <p class="big"><span data-count="31" data-suffix="%">31%</span></p>
      <p>of countries and territories have put LEAP behind a formal submission. The remaining 145 dots are states with no recorded use.</p>
    </div>
  </div>""")
    closefig("Data: Stockholm Environment Institute (2026). 65 of 210, rounded to 31 per cent.")

def fig_solver():
    openfig("f-solver", "Solver speed against the current release", "Vendor benchmark",
            "Reported speed-up of the interior-point method. Ticks are spaced logarithmically, current HiGHS release at 1\u00d7.")
    x0, x1, y = 74, 880, 128
    def X(v): return round(x0 + (math.log2(v) / 4) * (x1 - x0), 1)
    parts = ['<svg class="ruler" viewBox="0 0 960 190" role="img" aria-label="Scale showing the prototype at 16 times the speed of the current HiGHS release.">']
    parts.append(f'<line class="axis" x1="{x0}" y1="{y}" x2="{x1+10}" y2="{y}"/>')
    parts.append(f'<line class="seg" x1="{x0}" y1="{y}" x2="{X(16):.1f}" y2="{y}"/>')
    for t in [1, 2, 4, 8, 16]:
        cls = "tick-major" if t in (1, 16) else "tick"
        parts.append(f'<line class="{cls}" x1="{X(t):.1f}" y1="{y-13}" x2="{X(t):.1f}" y2="{y+13}"/>')
        if t != 16:
            parts.append(f'<text x="{X(t):.1f}" y="{y+36}" text-anchor="middle">{t}\u00d7</text>')
    parts.append(f'<text class="lbl" x="{x0}" y="{y-34}">Current HiGHS release</text>')
    parts.append(f'<text class="lbl" x="{x1+10}" y="{y-34}" text-anchor="end">TZ-HiGHS prototype</text>')
    parts.append(f'<text class="x16" x="{X(16):.1f}" y="{y+84}" text-anchor="middle">16\u00d7</text>')
    parts.append(f'<text x="{X(16):.1f}" y="{y+104}" text-anchor="middle">reported speed-up</text>')
    parts.append("</svg>")
    B.append("".join(parts))
    closefig("Data: TransitionZero (2026), prototype on the Open Energy Benchmark. Vendor-reported, not an independent evaluation.")

def fig_pledges():
    items = [
        "AI as an empowering partner",
        "Human accountability for final decisions",
        "Trust that is proportional, purposeful and testable",
        "Respect for national sovereignty",
        "Collective progress towards just energy futures",
    ]
    B.append('<figure class="fig" id="f-pledges" data-reveal>')
    B.append('<div class="fig-top"><h3>Five commitments of the SAGES framework</h3><span class="tag">June 2026</span></div>')
    B.append('<p class="fig-sub">Published with IRENA among the co-authors.</p>')
    B.append('<ol class="pledges">')
    for i, t in enumerate(items, 1):
        B.append(f'<li><span class="n">{i:02d}</span><h3>{t}</h3></li>')
    B.append('</ol>')
    closefig("Source: Tkachenko et al. (2026), Shared AI Governance for Energy Systems.")

def fig_road():
    items = [("Planning frameworks", "that treat data centre demand as a variable"),
             ("Knowledge platform", "shared across the planning community"),
             ("Connection rules", "flexible enough for storage and data centres"),
             ("Data standards", "for secure exchange between institutions"),
             ("Skills programmes", "for the planners who run the models"),
             ("Finance guidance", "for development finance institutions")]
    B.append('<figure class="fig" id="f-road" data-reveal>')
    B.append('<div class="fig-top"><h3>Six actions for 2026 to 2028</h3><span class="tag">LTES Network</span></div>')
    B.append('<p class="fig-sub">The plan to accelerate solutions on AI and digitalisation, as written into the COP Action Agenda. The six run in parallel, not in sequence.</p>')
    B.append('<ol class="acts">')
    for i, (t, d) in enumerate(items, 1):
        B.append(f'<li><span class="idx">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>')
    B.append('</ol>')
    closefig("Source: LTES Network (2025), Plan to Accelerate Solution: AI.")

hero_h1 = "AI in energy planning: closing the delivery gap"
kicker = "Artificial intelligence and energy planning"

HERO = f"""
<header class="hero">
  <div class="hero-canvas" data-island="aurora"></div>
  <div class="hero-veil"></div>
  <div class="hero-in">
    <div class="hero-top">
      <p class="brand">IRENA <em>Expert Insight</em></p>
      <p class="ev">Energy Planning Week 2026 &middot; Bonn, 1 to 4 December</p>
    </div>
    <div class="hero-body">
      <p class="hero-kicker" data-island="kicker" data-text="{kicker}">{kicker}</p>
      <h1 class="hero-h1" data-island="headline" data-text="{hero_h1}">{hero_h1}</h1>
      <p class="hero-dek">Planning offices must turn COP31's electrification targets into grids and projects. AI is already shortening parts of that work, and governance now decides whether the gain holds.</p>
    </div>
    <div class="hero-foot">
      <div class="hero-meta">
        <span><b>Simon Benmarraze, Nadeem Goussous and Juan Jose Garcia Mendez</b></span>
        <span class="sep"></span>
        <span>IRENA</span>
        <span class="sep"></span>
        <span>26 November 2026</span>
        <span class="sep"></span>
        <span>7 minute read</span>
      </div>
      <a class="scroll-cue" href="#main"><i></i>Read the argument</a>
    </div>
  </div>
</header>"""

sec("s1")
p("COP31 closed with electrification at the centre of the climate agenda. The Presidency's target of a 35% share for electricity in final energy demand by 2035 sits alongside the global goal of tripling renewable capacity and doubling energy efficiency by 2030 [1][9]. Both land on national planning offices, which must turn them into grids, storage and project pipelines inside budget cycles of months.", "lead")
p("Demand pressure is arriving fastest in Europe. Data centres in the EU consumed 68 TWh of electricity in 2024, a figure the European Commission projects will reach 114 TWh by 2030, or 3.2% of EU electricity demand [2].")
fig_demand()
p("Skills set a second limit. In EY's 2025 survey of oil and gas and chemicals executives, 82% cited too few workers with the right skills as a challenge to adopting new technology [3]. A model that cannot be fed, checked or explained becomes a liability in a ministry.")
endsec()

sec("s2", "What AI changes")
p("IRENA's 2026 review of digitalisation and AI in power systems maps the field into five value clusters: monitoring, forecasting, operational optimisation, end-user automation and transparency [4]. Six case studies from IRENA Innovation Week 2025 cover congestion management, predictive maintenance, non-firm connections, interoperability standards and virtual power plants. Digital tools unlock latent grid capacity, reduce curtailment and improve asset performance.")
fig_clusters()
p("In Sierra Leone, a national electrification platform built with the geospatial firm VIDA maps settlements, buildings and grid lines with machine learning, then matches each community to grid extension, a mini-grid or standalone solar. Its site list holds 21,075 settlements [6]. Ministries, funders and developers work from one living picture instead of separate spreadsheets, which shortens the distance between a least-cost plan and a project pipeline.")
p("Nigeria runs the same logic at national scale. The Rural Electrification Agency reports the same chain of figures for the Nigeria Electrification Programme and the DARES programme that builds on it: pipeline, mini-grid sites, connections, installed capacity and disbursement [12]. It counts 176 mini-grids and 7.8 million people reached, against a DARES target of 17.5 million [12].")
fig_nigeria()
p("Almost 80,000 people in 210 countries and territories use LEAP, the Low Emissions Analysis Platform developed by the Stockholm Environment Institute, and at least 65 countries have used it for their nationally determined contributions, long-term strategies or transparency reports [7]. The 2027 version adds AI that lets non-specialist planners explore a model in natural language and interrogate its assumptions. AI widens who can test a pathway, while the calculations stay in the model.")
fig_leap()
p("The same shift reaches the tools themselves. TransitionZero, a non-profit, set AI agents on the interior-point method of HiGHS, the open-source solver under many energy models, and reports a prototype up to 16 times faster than the current release on the Open Energy Benchmark [13]. Solver time sets how many scenarios a ministry can test before a decision is due, so a gain inside the code changes what a planning office can put in front of a minister.")
fig_solver()
p("One layer up, the assistant is becoming part of the workflow. A planner can ask it to draft a scenario, check inputs against regional data or explain why a run failed, then accept or reject each edit before it is applied [14]. The instructive part is how the safeguards are split: a tightly constrained assistant for general users, and a local tool where an experienced modeller connects their own AI and keeps the model and data on their own machine [13]. Control follows expertise.")
endsec()

sec("s3", "Who governs the result")
p("Institutional risk matters more than technical risk. A government that cannot inspect a model, trace its inputs or reproduce its output has lost control of the plan, whatever the accuracy of the forecast. The Shared AI Governance for Energy Systems (SAGES) framework, published in June 2026 with IRENA among its co-authors, sets five commitments [8]:")
fig_pledges()
p("Working groups cover vendor engagement, demonstration tools, sovereignty, and capacity building.")
endsec()

sec("s4", "The delivery route")
p("Delivery now has a vehicle in the COP Action Agenda. The LTES Network hosts a Plan to Accelerate Solutions on AI and digitalisation for a smart, resilient and efficient energy system, tied to tripling renewables and doubling energy efficiency [9]. Actions for 2026 to 2028 include planning frameworks that treat data centre demand as a variable, a knowledge platform, flexible connection rules, standards for secure data exchange, skills programmes and guidance for development finance.")
fig_road()
p("At COP31, IRENA also supported the Antalya AI Pledge, which asks signatories to power AI infrastructure with zero- and low-emission energy and to integrate it into electricity grids [10].")
endsec()

sec("s5", "What Energy Planning Week adds")
p("Energy Planning Week 2026, co-hosted by IRENA and GET.transform in Bonn from 1 to 4 December 2026, is the first working gathering of the planning community after COP31 [11]. It brings together the teams behind these tools, with applications grouped around demand and load forecasting, scenario development, and data quality assurance. A session on AI for energy planning is built for adoption: a planner can see how a method performs on a real system, and that evidence feeds the LTES Network's 2026 to 2028 actions, which depend on countries willing to test new methods in live cases.")
p("The promise of AI in energy planning is narrower than the publicity and more useful. It gives a small team the coverage of a larger one, provided the institution keeps ownership of the model, the data and the decision.", "closing")
endsec()

BODY = "\n".join(B)

used = []
for m in re.finditer(r"\[(\d+)\]", BODY):
    n = int(m.group(1))
    if n not in used:
        used.append(n)
missing = [n for n in used if n not in REFS]
assert not missing, f"cited but undefined: {missing}"
order = sorted(used, key=lambda n: used.index(n))
new = {old: i + 1 for i, old in enumerate(order)}

def cite(m):
    k = new[int(m.group(1))]
    return f'\u00a0<a class="cite" href="#r{k}" title="Reference {k}">[{k}]</a>'

BODY = re.sub(r"\s?\[(\d+)\]", cite, BODY)

refs_html = "\n".join(
    f'<li id="r{new[o]}"><span class="ref-n">{new[o]}</span><span>{REFS[o][0]} <a href="{REFS[o][1]}" target="_blank" rel="noopener">{REFS[o][1]}</a></span></li>'
    for o in order
)

CSS = (ROOT / "styles.css").read_text()

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
<link rel="preload" href="fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="vendor/islands.css">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress"><i></i></div>
{HERO}
<main id="main">
  <article class="prose">
{BODY}
    <section class="sec refs" id="refs">
      <div class="text"><h2>References</h2></div>
      <ol class="reflist">{refs_html}</ol>
    </section>
  </article>
</main>
<footer class="foot">
  <div class="wrap">
    <p class="foot-note">The designations employed and the presentation of material herein do not imply the expression of any opinion on the part of IRENA concerning the legal status of any region, country, territory, city or area or of its authorities, or concerning the delimitation of frontiers or boundaries. The mention of specific companies, projects or products does not imply that they are endorsed or recommended by IRENA in preference to others of a similar nature that are not mentioned.</p>
    <p class="foot-credit">IRENA Expert Insight &middot; Energy Planning Week 2026</p>
  </div>
</footer>
<script src="vendor/islands.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

OUT.mkdir(exist_ok=True)
(OUT / "index.plain.html").write_text(page)
print("built index.plain.html", len(page), "bytes")
print("citations:", used, "-> ordered")
