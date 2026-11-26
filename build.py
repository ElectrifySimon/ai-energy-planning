#!/usr/bin/env python3
"""Build the AI in energy planning long-read page."""
import re, pathlib

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

# ------------------------------------------------------------------ icons
ICONS = {
 "eye": '<circle cx="12" cy="12" r="3.2"/><path d="M2.6 12S6 5.8 12 5.8 21.4 12 21.4 12 18 18.2 12 18.2 2.6 12 2.6 12Z"/>',
 "trend": '<path d="M3 17.5 8.6 11l3.6 3.2L21 5.6"/><path d="M21 10.4V5.6h-4.8"/><path d="M3 21h18"/>',
 "forecast": '<path d="M3 18.5h3.2l2.4-6.2 3 4.4 2.6-8.2 3 6.4H21"/><circle cx="17.2" cy="14.9" r="1.4"/>',
 "home": '<path d="M4 10.6 12 4l8 6.6V20a1 1 0 0 1-1 1h-4.4v-5.6H9.4V21H5a1 1 0 0 1-1-1Z"/><path d="M15.4 3v4.4"/>',
 "doclines": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/><path d="M8.6 13h6.8M8.6 16.6h4.4"/>',
 "sliders": '<path d="M4 7h5"/><path d="M15 7h5"/><circle cx="12" cy="7" r="2.6"/><path d="M4 17h9"/><path d="M19 17h1"/><circle cx="16" cy="17" r="2.6"/>',
 "plug": '<path d="M9 3v5"/><path d="M15 3v5"/><path d="M6.5 8h11v3.2a5.5 5.5 0 0 1-11 0Z"/><path d="M12 16.7V21"/>',
 "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h7"/><path d="M14 3v6h6"/><circle cx="16.4" cy="16.4" r="3.1"/><path d="M18.7 18.7 21 21"/>',
 "layers": '<path d="M12 3 3 7.6l9 4.6 9-4.6Z"/><path d="m3 12.4 9 4.6 9-4.6"/><path d="m3 17 9 4.6L21 17"/>',
 "database": '<ellipse cx="12" cy="6" rx="7.5" ry="3"/><path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6"/><path d="M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/>',
 "link": '<path d="M9.4 14.6 14.6 9.4"/><path d="M7 17a3.9 3.9 0 0 1 0-5.5l2.8-2.8"/><path d="M17 7a3.9 3.9 0 0 1 0 5.5l-2.8 2.8"/>',
 "shield": '<path d="M12 3 5 5.8v5.6c0 4.3 2.9 7.6 7 9.6 4.1-2 7-5.3 7-9.6V5.8Z"/><path d="m9 12 2.2 2.2L15.4 10"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.4 4 5.6 4 9s-1.4 6.6-4 9c-2.6-2.4-4-5.6-4-9s1.4-6.6 4-9Z"/>',
 "scales": '<path d="M12 4v16"/><path d="M6 8h12"/><path d="M9 20h6"/><path d="M4 8 6.6 14h-5.2Z"/><path d="M20 8l2.6 6h-5.2Z"/>',
 "coins": '<ellipse cx="9" cy="7" rx="5.4" ry="2.6"/><path d="M3.6 7v4c0 1.4 2.4 2.6 5.4 2.6s5.4-1.2 5.4-2.6V7"/><path d="M9 13.6V17c0 1.4 2.4 2.6 5.4 2.6s5.4-1.2 5.4-2.6v-4"/>',
 "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c0-3 2.5-5.2 5.5-5.2s5.5 2.2 5.5 5.2"/><circle cx="17" cy="9" r="2.4"/><path d="M15.6 14.9c2.6 0 4.6 2 4.6 4.6"/>',
 "cpu": '<rect x="7" y="7" width="10" height="10" rx="1.6"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
 "bolt": '<path d="M13 2 5 13.5h6L10 22l8-11.5h-6Z"/>',
 "tower": '<path d="M12 3v18"/><path d="M6 21 12 3l6 18"/><path d="M8.4 14h7.2"/><path d="M9.6 9.5h4.8"/>',
}

def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" '
            f'fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')

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

FIGNO = {"f-clusters": 1, "f-demand": 2, "f-nigeria": 3, "f-leap": 4,
         "f-solver": 5, "f-pledges": 6, "f-road": 7}

def openfig(fid, title, sub):
    n = FIGNO[fid]
    B.append(f"""
<figure class="fig" id="{fid}" data-reveal>
  <p class="fig-no">Figure {n:02d}</p>
  <h3 class="fig-title">{title}</h3>
  <p class="fig-sub">{sub}</p>""")

def closefig(source):
    src = source.replace("Source: ", "").rstrip(".")
    B.append(f'  <figcaption><span>Source</span>{src}</figcaption>\n</figure>')

def rails(rows, maximum, unit, step, note, future_cls=" future"):
    B.append('<div class="rails">')
    for year, kind, v in rows:
        fill = round(v / maximum * 100, 2)
        cls = future_cls if kind == "projected" else ""
        inside = ""
        B.append(f"""
  <div class="rail">
    <div class="rail-year">{year}<small>{kind}</small></div>
    <div class="track" style="--fill:{fill}%"><span class="fill{cls}"></span><span class="rail-v{inside}" style="--fill:{fill}%">{v}<small>{unit}</small></span></div>
  </div>""")
    B.append("</div>")
    ticks = "".join(f"<span>{t}</span>" for t in step)
    B.append(f'<div class="scale">{ticks}</div>')
    if note:
        B.append(f'<div class="rail-note">{note}</div>')

def fig_demand():
    openfig("f-demand", "Data centre electricity demand, EU",
            "Terawatt hours, 2024 and 2030.")
    rails([("2024", "actual", 68), ("2030", "projected", 114)], 120, "TWh",
          ["0", "30", "60", "90", "120 TWh"], None)
    closefig("Source: European Commission (2026).")

def fig_solver():
    openfig("f-solver", "Solver speed against the current release",
            "Reported speed-up, current release at 1\u00d7.")
    rails([("TZ-HiGHS", "prototype", 16), ("HiGHS", "current release", 1)], 16, "\u00d7",
          ["0", "4\u00d7", "8\u00d7", "12\u00d7", "16\u00d7"], None)
    closefig("Source: TransitionZero (2026), Open Energy Benchmark. Vendor-reported, not an independent evaluation.")

def fig_clusters():
    items = [("01", "Monitoring", "eye"), ("02", "Forecasting", "forecast"),
             ("03", "Operational optimisation", "sliders"), ("04", "End-user automation", "home"),
             ("05", "Transparency", "doclines")]
    B.append('<figure class="fig" id="f-clusters" data-reveal>')
    B.append('<p class="fig-no">Figure 01</p>')
    B.append('<h3 class="fig-title">Five value clusters</h3>')
    B.append('<p class="fig-sub">IRENA\'s five application areas.</p>')
    B.append('<ol class="band">')
    for n, t, ic in items:
        B.append(f'<li><span class="num">{n}</span>{icon(ic, "ic band-ic")}<h3>{t}</h3></li>')
    B.append('</ol>')
    closefig("Source: IRENA (2026), Digitalisation and AI for transforming power systems.")

def fig_nigeria():
    reached, target, scale = 7.8, 17.5, 20.0
    openfig("f-nigeria", "People reached against the DARES target",
            "Millions of people. The bar runs to the DARES target of 17.5 million.")
    f1 = round(reached / scale * 100, 2)
    f2 = round(target / scale * 100, 2)
    gap = round(f2 - f1, 2)
    B.append(f"""
  <div class="stack">
    <div class="stack-h"><span>Nigeria, people with new access to electricity</span><b>7.8 of 17.5 million</b></div>
    <div class="stack-track">
      <span class="seg seg-reached" style="width:{f1}%">7.8 m reached</span>
      <span class="seg seg-gap" style="width:{gap}%">9.7 m still to reach</span>
    </div>
  </div>
  <div class="scale"><span>0</span><span>5</span><span>10</span><span>15</span><span>20 million</span></div>
""")
    closefig("Source: Rural Electrification Agency (2026).")

def fig_leap():
    openfig("f-leap", "Who uses LEAP",
            "One dot per country or territory, 210 in total.")
    COLS, TOTAL, USED = 30, 210, 65
    pitch, r, pad = 30, 8.2, 18
    w, h = COLS * pitch, 7 * pitch
    dots = []
    for i in range(TOTAL):
        col, row = i % COLS, i // COLS
        cx = pad + col * pitch + pitch / 2
        cy = pad + row * pitch + pitch / 2
        cls = "dot lit" if i < USED else "dot"
        dots.append(f'<circle class="{cls}" cx="{cx:g}" cy="{cy:g}" r="{r:g}" style="transition-delay:{(i*7)}ms"/>')
    B.append(f"""
  <div class="dots-wrap">
    <svg id="leap-grid" viewBox="0 0 {w + pad*2} {h + pad*2}" width="{w + pad*2}" height="{h + pad*2}" role="img" aria-label="Unit chart: 65 of 210 countries and territories have used LEAP for a nationally determined contribution, long-term strategy or transparency report.">
      {''.join(dots)}
    </svg>
    <div class="dot-caption">
      <p class="big"><span data-count="31" data-suffix="%">31%</span></p>
      <p>of countries and territories have put LEAP behind a formal submission. The remaining 145 dots are states with no recorded use.</p>
    </div>
  </div>""")
    closefig("Source: Stockholm Environment Institute (2026).")

def fig_pledges():
    items = [("AI as an empowering partner", "people"),
             ("Human accountability for final decisions", "shield"),
             ("Trust that is proportional, purposeful and testable", "scales"),
             ("Respect for national sovereignty", "globe"),
             ("Collective progress towards just energy futures", "bolt")]
    B.append('<figure class="fig" id="f-pledges" data-reveal>')
    B.append('<p class="fig-no">Figure 06</p>')
    B.append('<h3 class="fig-title">Five commitments of the SAGES framework</h3>')
    B.append('<ol class="pledges">')
    for i, (t, ic) in enumerate(items, 1):
        B.append(f'<li>{icon(ic, "ic pledge-ic")}<span class="n">{i:02d}</span><h3>{t}</h3></li>')
    B.append('</ol>')
    closefig("Source: Tkachenko et al. (2026), Shared AI Governance for Energy Systems.")

def fig_road():
    items = [("Planning frameworks", "for data centre demand", "layers"),
             ("Knowledge platform", "shared across the community", "database"),
             ("Connection rules", "for storage and data centres", "link"),
             ("Data standards", "for secure exchange", "shield"),
             ("Skills programmes", "for the planners who run the models", "people"),
             ("Finance guidance", "for development finance", "coins")]
    B.append('<figure class="fig" id="f-road" data-reveal>')
    B.append('<p class="fig-no">Figure 07</p>')
    B.append('<h3 class="fig-title">Six actions for 2026 to 2028</h3>')
    B.append('<p class="fig-sub">All six run at once.</p>')
    B.append('<ol class="acts">')
    for i, (t, d, ic) in enumerate(items, 1):
        B.append(f'<li>{icon(ic, "ic act-ic")}<h3>{t}</h3><p>{d}</p></li>')
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
      <a class="scroll-cue" href="#main">{icon("bolt", "ic cue-ic")}Read the argument</a>
    </div>
  </div>
</header>"""

sec("s1")
p("COP31 put electrification at the centre of the climate agenda. The Presidency target is a 35% share for electricity in final energy demand by 2035, with tripling renewables and doubling efficiency. <a href=\"https://iklim.gov.tr/en/cop31-president-designate-and-minister-kurum-unveils-cop31-action-agenda-news-4985\" target=\"_blank\" rel=\"noopener\">The COP31 Action Agenda</a> sets both. For planning offices they arrive as work: grids, storage and pipelines, inside budget cycles of months.", "lead")

sec("s2", "What AI changes")
p("<a href=\"https://www.irena.org/Publications/2026/May/Digitalisation-and-AI-for-transforming-power-systems\" target=\"_blank\" rel=\"noopener\">IRENA's 2026 review</a> of digitalisation and AI in power systems sorts the field into five areas: monitoring, forecasting, operational optimisation, end-user automation and transparency.")
fig_clusters()
p("Data centres in the EU used 68 TWh in 2024, a figure the <a href=\"https://build-up.ec.europa.eu/en/resources-and-tools/publications/report-energy-efficiency-data-centres-eu\" target=\"_blank\" rel=\"noopener\">European Commission</a> projects at 114 TWh by 2030, 3.2% of EU demand.")
fig_demand()
p("An <a href=\"https://www.ey.com/content/dam/ey-unified-site/ey-com/en-us/campaigns/energy-resources/documents/ey-ogc-future-of-energy-external-report.pdf\" target=\"_blank\" rel=\"noopener\">EY survey from 2025</a> found 82% of energy executives citing too few skilled workers as an obstacle to new technology.")
p("In Sierra Leone, a national platform built with <a href=\"https://vida.place/applications/planning\" target=\"_blank\" rel=\"noopener\">VIDA</a> maps settlements, buildings and grid lines, then matches each community to grid extension, mini-grid or standalone solar. Its list holds 21,075 settlements, and funders, ministries and developers work from one picture instead of separate spreadsheets.")
p("Nigeria runs it at scale. The <a href=\"https://nep.rea.gov.ng/\" target=\"_blank\" rel=\"noopener\">Rural Electrification Agency</a> counts 176 mini-grids and 7.8 million reached, against a DARES target of 17.5 million.")
fig_nigeria()
p("Almost 80,000 people in 210 countries use <a href=\"https://leap.sei.org/\" target=\"_blank\" rel=\"noopener\">LEAP</a>, from the Stockholm Environment Institute. At least 65 countries have used it for climate pledges. The 2027 version adds AI that lets non-specialists explore a model in plain language.")
fig_leap()
p("<a href=\"https://www.transitionzero.org/events/introducing-conductor-and-tz-highs-launch-webinar\" target=\"_blank\" rel=\"noopener\">TransitionZero</a>, a non-profit, set AI agents on the solver underneath many energy models and reports a prototype up to 16 times faster than the current release. Solver time sets how many scenarios a ministry can test before a decision.")
fig_solver()
p("One layer up, the assistant joins the workflow: draft a scenario, check inputs, explain a failed run, each edit accepted or rejected. Control follows expertise. A constrained assistant for general users, a local tool for modellers who keep their own AI and data locally.")
endsec()

sec("s3", "Who governs the result")
p("Institutional risk outweighs technical risk. A government that cannot inspect a model, trace its inputs or reproduce its output has lost control of the plan. The <a href=\"https://doi.org/10.33774/coe-2026-0gzfx\" target=\"_blank\" rel=\"noopener\">Shared AI Governance for Energy Systems</a> framework, published in June 2026 with IRENA among its co-authors, sets five commitments.")
fig_pledges()
p("Working groups cover vendors, demonstration, sovereignty and capacity.")
endsec()

sec("s4", "The delivery route")
p("The COP Action Agenda carries delivery. The <a href=\"https://climateaction.unfccc.int/assets/documents/121_.pdf\" target=\"_blank\" rel=\"noopener\">LTES Network</a> hosts a Plan to Accelerate Solutions on AI and digitalisation, tied to tripling renewables and doubling efficiency. Actions for 2026 to 2028 cover planning frameworks, a knowledge platform, connection rules, data standards, skills and finance.")
fig_road()
p("IRENA also supported the <a href=\"https://cop31.tr/assets/docs/action-agenda/cop31-antalya-ai-pledge-text.pdf\" target=\"_blank\" rel=\"noopener\">Antalya AI Pledge</a> on powering AI infrastructure with clean energy.")
endsec()

sec("s5", "What Energy Planning Week adds")
p("<a href=\"https://www.irena.org/Events/2026/Dec/Energy-Planning-Week-2026\" target=\"_blank\" rel=\"noopener\">Energy Planning Week 2026</a>, co-hosted by IRENA and GET.transform in Bonn from 1 to 4 December 2026, is the first working gathering of the planning community after COP31. It brings together the teams behind these tools, with applications grouped around demand and load forecasting, scenario development, and data quality assurance. A session on AI for energy planning is built for adoption: a planner can see how a method performs on a real system, and that evidence feeds the <a href=\"https://climateaction.unfccc.int/assets/documents/121_.pdf\" target=\"_blank\" rel=\"noopener\">LTES Network</a>\u2019s 2026 to 2028 actions, which depend on countries willing to test new methods in live cases.")
p("The promise of AI in energy planning is narrower than the publicity and more useful. It gives a small team the coverage of a larger one, provided the institution keeps ownership of the model, the data and the decision.", "closing")
endsec()

BODY = "\n".join(B)

words = len(re.sub(r"<[^>]+>", " ", BODY).split())

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

(ROOT / "index.plain.html").write_text(page)
print("built index.plain.html", len(page), "bytes,", words, "words")
