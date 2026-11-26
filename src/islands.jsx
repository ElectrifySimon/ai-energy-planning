import React from 'react';
import { createRoot } from 'react-dom/client';
import SplitText from './reactbits/SplitText.jsx';
import GradientText from './reactbits/GradientText.jsx';
import CountUp from './reactbits/CountUp.jsx';
import Aurora from './reactbits/Aurora.jsx';
import './reactbits/GradientText.css';
import './reactbits/Aurora.css';

function mount(el, node) {
  if (!el) return;
  createRoot(el).render(node);
}

/* headline: chars rise out of a mask, once, on load */
const h1 = document.querySelector('[data-island="headline"]');
if (h1) {
  const text = h1.dataset.text || h1.textContent.trim();
  mount(h1, (
    <SplitText
      text={text}
      tag="span"
      className="hero-h1"
      splitType="chars"
      effect="rise"
      mask
      duration={1.15}
      delay={22}
      threshold={0}
      rootMargin="0px"
      textAlign="left"
      ease="power4.out"
    />
  ));
}

/* kicker: slow gradient sweep on the eyebrow */
const kicker = document.querySelector('[data-island="kicker"]');
if (kicker) {
  const text = kicker.dataset.text || kicker.textContent.trim();
  mount(kicker, (
    <GradientText
      colors={['#95ADC9', '#5CA8D8', '#0073AB', '#5CA8D8']}
      animationSpeed={9}
      angle={90}
      yoyo
      className="hero-kicker"
    >
      {text}
    </GradientText>
  ));
}

/* counters: every element that declares data-to */
document.querySelectorAll('[data-count]').forEach((el) => {
  const to = parseFloat(el.dataset.count);
  const decimals = parseInt(el.dataset.decimals || '0', 10);
  const suffix = el.dataset.suffix || '';
  const prefix = el.dataset.prefix || '';
  mount(el, (
    <CountUp
      to={to}
      from={0}
      duration={1.9}
      decimals={decimals}
      prefix={prefix}
      suffix={suffix}
      separator={el.dataset.separator || ''}
      trigger="view"
      className="count"
    />
  ));
});

/* hero background */
const aurora = document.querySelector('[data-island="aurora"]');
if (aurora) {
  mount(aurora, (
    <Aurora
      colorStops={['#002339', '#0073AB', '#00537D']}
      amplitude={1.15}
      blend={0.34}
      speed={0.55}
      layers={2}
      height={0.55}
      glow={1}
      brightness={1.0}
      opacity={0.78}
      mouseInteraction
    />
  ));
}
