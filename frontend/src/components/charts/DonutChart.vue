<script setup>
import { computed } from 'vue';

const props = defineProps({
  data: { type: Array, required: true }, // [{ label, value }]
  size: { type: Number, default: 260 },
  thickness: { type: Number, default: 26 },
  // Wenn leer, werden automatisch farbenfrohe HSL-Farben erzeugt
  colors: { type: Array, default: () => [] },
  showLegend: { type: Boolean, default: true },
  title: { type: String, default: '' },
});

const total = computed(() => props.data.reduce((s, d) => s + (Number(d.value) || 0), 0));

// Generate vivid, distinct fallback colors if more slices than provided colors
const hashString = (str) => {
  let h = 5381;
  for (let i = 0; i < String(str).length; i++) h = ((h << 5) + h) ^ String(str).charCodeAt(i);
  return Math.abs(h);
};

const colorFor = (label, idx) => {
  const list = props.colors || [];
  if (list.length > 0) return list[idx % list.length];
  // Golden-Angle-Spacing für maximal unterschiedliche Farbtöne
  const GOLDEN_ANGLE = 137.508;
  const base = hashString(label ?? idx) % 360;
  const hue = (base + idx * GOLDEN_ANGLE) % 360;
  const saturation = 78; // kräftig, aber nicht neon
  const lightness = 55;  // gute Sichtbarkeit in Light/Dark
  return `hsl(${hue} ${saturation}% ${lightness}%)`;
};

const radius = computed(() => (props.size / 2) - props.thickness / 2);
const circumference = computed(() => 2 * Math.PI * radius.value);

const segments = computed(() => {
  let offset = 0;
  const c = circumference.value;
  const t = total.value || 1;
  return props.data.map((d, i) => {
    const val = Number(d.value) || 0;
    const frac = Math.max(0, val / t);
    const length = frac * c;
    const seg = {
      label: d.label,
      value: val,
      color: colorFor(d.label, i),
      dasharray: `${length} ${c - length}`,
      dashoffset: -offset,
      percent: Math.round(frac * 100),
    };
    offset += length;
    return seg;
  });
});
</script>

<template>
  <div class="donut-card">
    <div v-if="title" class="title">{{ title }}</div>
    <div class="chart-row">
      <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" class="donut">
        <g :transform="`translate(${size/2}, ${size/2})`">
          <circle class="track" :r="radius" :cx="0" :cy="0" :stroke-width="thickness" fill="none" />
          <template v-for="(s, idx) in segments" :key="idx">
            <circle
              class="seg"
              :r="radius"
              :cx="0"
              :cy="0"
              :stroke="s.color"
              :stroke-dasharray="s.dasharray"
              :stroke-dashoffset="s.dashoffset"
              :stroke-width="thickness"
              fill="none"
            />
          </template>
          <text class="center-value" text-anchor="middle" dominant-baseline="middle">
            {{ total }}
          </text>
        </g>
      </svg>
      <ul v-if="showLegend" class="legend">
        <li v-for="(s, idx) in segments" :key="idx">
          <span class="dot" :style="{ backgroundColor: s.color }"></span>
          <span class="lbl">{{ s.label }}</span>
          <span class="pct">{{ s.percent }}%</span>
        </li>
      </ul>
    </div>
  </div>
  
</template>

<style scoped>
.donut-card { display: flex; flex-direction: column; gap: 0.5rem; }
.title { font-weight: 700; color: var(--text-strong); }
.chart-row { display: grid; grid-template-columns: auto 1fr; gap: 1rem; align-items: center; }
.donut { block-size: auto; }
.track { stroke: var(--color-border); opacity: 0.6; }
.seg { fill: none; stroke-linecap: butt; transition: opacity 0.2s; }
.seg:hover { opacity: 0.85; }
.center-value { font-size: 1.25rem; font-weight: 800; fill: var(--text-strong); }
.legend { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.35rem; }
.legend li { display: grid; grid-template-columns: 14px 1fr auto; gap: 0.5rem; align-items: center; color: var(--text-strong); }
.legend .dot { width: 10px; height: 10px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.1); }
.legend .lbl { opacity: 0.9; }
.legend .pct { color: var(--text-muted); font-variant-numeric: tabular-nums; }
</style>


