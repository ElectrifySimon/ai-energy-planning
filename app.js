/* Charts for the AI in energy planning long-read. Apache ECharts, vendored. */
(function () {
  'use strict';

  var BLUE = '#0073AB';
  var BLUE_DEEP = '#08506f';
  var SOFT = '#9db4c2';
  var GRID = '#e3ebf1';
  var RULE = '#dce5eb';
  var INK = '#12222e';
  var MUTED = '#6a7c88';

  function base() {
    return {
      textStyle: { fontFamily: 'Inter, system-ui, sans-serif', color: '#33454f' },
      animationDuration: 650,
      animationEasing: 'cubicOut'
    };
  }

  function mount(id, builder, label) {
    var el = document.getElementById(id);
    if (!el || !window.echarts) return;
    var chart = echarts.init(el, null, { renderer: 'canvas' });
    chart.setOption(builder());
    el.setAttribute('role', 'img');
    el.setAttribute('aria-label', label);
    var redraw = function () { chart.resize(); };
    window.addEventListener('resize', redraw);
    if (window.ResizeObserver) new ResizeObserver(redraw).observe(el);
  }

  /* 1. EU data centre electricity demand */
  function euDC() {
    return Object.assign(base(), {
      grid: { left: 52, right: 28, top: 42, bottom: 38 },
      xAxis: {
        type: 'category',
        data: ['2024', '2030 (projected)'],
        axisTick: { show: false },
        axisLine: { lineStyle: { color: RULE } },
        axisLabel: { fontSize: 13, color: MUTED, margin: 12 }
      },
      yAxis: {
        type: 'value',
        name: 'TWh',
        nameTextStyle: { color: MUTED, fontSize: 12, padding: [0, 0, 6, -34] },
        max: 130,
        splitLine: { lineStyle: { color: GRID } },
        axisLabel: { fontSize: 12, color: MUTED }
      },
      series: [{
        type: 'bar',
        barWidth: '34%',
        data: [
          { value: 68, itemStyle: { color: SOFT } },
          { value: 114, itemStyle: { color: BLUE } }
        ],
        label: {
          show: true,
          position: 'top',
          distance: 8,
          formatter: '{c} TWh',
          fontSize: 15,
          fontWeight: 600,
          color: INK,
          fontFamily: 'Inter, system-ui, sans-serif'
        }
      }]
    });
  }

  /* 2. LEAP footprint: 65 of 210 countries and territories */
  function leapWaffle() {
    var TOTAL = 210, USED = 65, COLS = 30, ROWS = 7;
    var data = [];
    for (var i = 0; i < TOTAL; i++) data.push(i < USED ? 1 : 0);

    return Object.assign(base(), {
      grid: { left: 0, right: 0, top: 6, bottom: 0 },
      xAxis: { show: false, type: 'value', min: 0, max: COLS },
      yAxis: { show: false, type: 'value', min: 0, max: ROWS, inverse: true },
      series: [{
        type: 'custom',
        data: data,
        renderItem: function (params, api) {
          var w = api.getWidth(), h = api.getHeight();
          var cell = Math.min(w / COLS, h / ROWS);
          var gap = Math.max(2, cell * 0.16);
          var size = cell - gap;
          var ox = (w - cell * COLS) / 2;
          var oy = (h - cell * ROWS) / 2;
          var idx = params.dataIndex;
          var c = idx % COLS;
          var r = Math.floor(idx / COLS);
          return {
            type: 'rect',
            shape: { x: ox + c * cell + gap / 2, y: oy + r * cell + gap / 2, width: size, height: size, r: 1 },
            style: { fill: data[idx] ? BLUE : '#dbe6ed' }
          };
        }
      }]
    });
  }

  /* 3. Solver speed, relative to the current HiGHS release */
  function solver() {
    return Object.assign(base(), {
      grid: { left: 196, right: 74, top: 22, bottom: 34 },
      xAxis: {
        type: 'value',
        max: 17.5,
        splitLine: { lineStyle: { color: GRID } },
        axisLabel: { formatter: '{value}\u00d7', fontSize: 12, color: MUTED }
      },
      yAxis: {
        type: 'category',
        data: ['TZ-HiGHS prototype', 'HiGHS, current release'],
        axisTick: { show: false },
        axisLine: { lineStyle: { color: RULE } },
        axisLabel: { fontSize: 13, color: INK, margin: 14 }
      },
      series: [{
        type: 'bar',
        barWidth: 24,
        data: [
          { value: 16, itemStyle: { color: BLUE } },
          { value: 1, itemStyle: { color: SOFT } }
        ],
        label: {
          show: true,
          position: 'right',
          distance: 10,
          formatter: '{c}\u00d7',
          fontSize: 14,
          fontWeight: 600,
          color: INK,
          fontFamily: 'Inter, system-ui, sans-serif'
        }
      }]
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    mount('eu-dc-chart', euDC, 'Bar chart: EU data centre electricity consumption, 68 terawatt hours in 2024 and a projected 114 terawatt hours in 2030.');
    mount('leap-chart', leapWaffle, 'Waffle chart: 65 of 210 countries and territories have used LEAP for a nationally determined contribution, long-term strategy or transparency report.');
    mount('solver-chart', solver, 'Bar chart: the TZ-HiGHS prototype reports a solve up to 16 times faster than the current HiGHS release.');
  });
})();
