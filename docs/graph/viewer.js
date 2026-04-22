// sci-logic-kb · interactive graph viewer
// Read-only front-end over docs/graph/graph.json (produced by graph.py).

(async function () {
  "use strict";

  const TYPE_COLORS = {
    entity:    "#4e79a7",
    principle: "#e15759",
    method:    "#59a14f",
    metric:    "#f28e2b",
  };
  const DEFAULT_COLOR = "#888";

  const palette = [
    "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
    "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac",
  ];

  const statsEl = document.getElementById("stats");
  const infoEl = document.getElementById("info");

  let cy;
  let payload;

  try {
    const resp = await fetch("graph.json", { cache: "no-cache" });
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    payload = await resp.json();
  } catch (err) {
    statsEl.textContent = "Failed to load graph.json: " + err.message;
    return;
  }

  const elements = payload.elements;
  const stats = payload.stats || {};
  statsEl.innerHTML =
    `${stats.total_nodes || elements.nodes.length} nodes · ` +
    `${stats.total_edges || elements.edges.length} edges<br>` +
    `Topics: ${(stats.topics || []).length} · ` +
    `Predicates: ${(stats.predicates || []).length}`;

  // ── Collect universe ──
  const allTypes = new Set();
  const allTopics = new Set();
  const allTiers = new Set();
  const allPreds = new Set();

  elements.nodes.forEach(n => {
    if (n.data.type) allTypes.add(n.data.type);
    if (n.data.topic) allTopics.add(n.data.topic);
    if (n.data.tier) allTiers.add(n.data.tier);
  });
  elements.edges.forEach(e => {
    if (e.data.predicate) allPreds.add(e.data.predicate);
  });

  // ── Filter UI ──
  function makeCheckboxes(containerId, values, onChange, colorLookup) {
    const c = document.getElementById(containerId);
    c.innerHTML = "";
    [...values].sort().forEach(v => {
      const id = containerId + "_" + btoa(unescape(encodeURIComponent(v))).replace(/=/g, "");
      const wrap = document.createElement("label");
      const cb = document.createElement("input");
      cb.type = "checkbox"; cb.checked = true; cb.dataset.value = v; cb.id = id;
      cb.addEventListener("change", onChange);
      wrap.appendChild(cb);
      if (colorLookup) {
        const dot = document.createElement("span");
        dot.className = "legend-dot";
        dot.style.background = colorLookup(v);
        wrap.appendChild(dot);
      }
      wrap.appendChild(document.createTextNode(v));
      c.appendChild(wrap);
    });
  }

  // Deterministic palette for topics and tiers
  const topicColor = {}; let ti = 0;
  [...allTopics].sort().forEach(t => { topicColor[t] = palette[ti++ % palette.length]; });
  const tierColor = {}; let si = 0;
  [...allTiers].sort().forEach(t => { tierColor[t] = palette[si++ % palette.length]; });

  function colorOf(node) {
    const data = node.data();
    const mode = document.getElementById("color-mode").value;
    if (mode === "type") return TYPE_COLORS[data.type] || DEFAULT_COLOR;
    if (mode === "topic") return topicColor[data.topic] || DEFAULT_COLOR;
    if (mode === "tier") return tierColor[data.tier] || DEFAULT_COLOR;
    return DEFAULT_COLOR;
  }

  // ── Initialise cytoscape ──
  cy = cytoscape({
    container: document.getElementById("cy"),
    elements: elements,
    wheelSensitivity: 0.2,
    style: [
      {
        selector: "node",
        style: {
          "background-color": (ele) => colorOf(ele),
          "label": "data(label)",
          "font-size": 8,
          "text-opacity": 0.0,
          "width": 14,
          "height": 14,
          "border-width": 1,
          "border-color": "#333",
        },
      },
      {
        selector: "node:selected",
        style: { "border-width": 3, "border-color": "#000", "text-opacity": 1 },
      },
      {
        selector: "node[?matched]",
        style: { "text-opacity": 1, "font-size": 10 },
      },
      {
        selector: "edge",
        style: {
          "width": 1,
          "line-color": "#bbb",
          "curve-style": "bezier",
          "target-arrow-color": "#bbb",
          "target-arrow-shape": "triangle",
          "arrow-scale": 0.8,
          "opacity": 0.6,
        },
      },
      {
        selector: "edge:selected",
        style: { "line-color": "#000", "target-arrow-color": "#000", "width": 2, "opacity": 1 },
      },
      { selector: ".dimmed", style: { "opacity": 0.08 } },
    ],
    layout: {
      name: (typeof cytoscape.use === "function" && window.fcose) ? "fcose" : "cose",
      animate: false,
      nodeRepulsion: 3000,
      idealEdgeLength: 60,
      edgeElasticity: 0.1,
      randomize: true,
    },
  });

  // Click handler
  cy.on("tap", "node", (evt) => {
    const d = evt.target.data();
    const lines = [
      `id:            ${d.id}`,
      `label:         ${d.label}`,
      `type:          ${d.type}`,
      `topic:         ${d.topic}`,
      d.hierarchy_level ? `hierarchy:    L${d.hierarchy_level}` : null,
      d.tier ? `tier:          ${d.tier}` : null,
      `defining_file: ${d.defining_file}`,
    ].filter(Boolean);
    infoEl.textContent = lines.join("\n");
    infoEl.classList.add("visible");
  });
  cy.on("tap", "edge", (evt) => {
    const d = evt.target.data();
    infoEl.textContent = [
      `id:        ${d.id}`,
      `predicate: ${d.predicate}`,
      `source:    ${d.source}`,
      `target:    ${d.target}`,
      `topic:     ${d.topic}`,
      `file:      ${d.file}`,
    ].join("\n");
    infoEl.classList.add("visible");
  });
  cy.on("tap", (evt) => { if (evt.target === cy) infoEl.classList.remove("visible"); });

  // ── Filters ──
  const updateStyles = () => {
    cy.nodes().forEach(n => n.style("background-color", colorOf(n)));
  };

  const applyFilters = () => {
    const typeSel = new Set([...document.querySelectorAll("#type-filters input:checked")]
      .map(el => el.dataset.value));
    const topicSel = new Set([...document.querySelectorAll("#topic-filters input:checked")]
      .map(el => el.dataset.value));
    const predSel = new Set([...document.querySelectorAll("#pred-filters input:checked")]
      .map(el => el.dataset.value));

    cy.batch(() => {
      cy.nodes().forEach(n => {
        const d = n.data();
        const keep = typeSel.has(d.type) && topicSel.has(d.topic);
        n.style("display", keep ? "element" : "none");
      });
      cy.edges().forEach(e => {
        const d = e.data();
        const keep = predSel.has(d.predicate)
          && e.source().visible() && e.target().visible();
        e.style("display", keep ? "element" : "none");
      });
    });
  };

  makeCheckboxes("type-filters", allTypes, applyFilters, (v) => TYPE_COLORS[v] || DEFAULT_COLOR);
  makeCheckboxes("topic-filters", allTopics, applyFilters, (v) => topicColor[v]);
  makeCheckboxes("pred-filters", allPreds, applyFilters);
  document.getElementById("color-mode").addEventListener("change", updateStyles);

  document.getElementById("fit").addEventListener("click", () => cy.fit());

  // Search: highlight matching nodes
  document.getElementById("search").addEventListener("input", (evt) => {
    const q = evt.target.value.trim().toLowerCase();
    cy.batch(() => {
      if (!q) {
        cy.elements().removeClass("dimmed");
        cy.nodes().forEach(n => n.removeData("matched"));
        return;
      }
      cy.nodes().forEach(n => {
        const d = n.data();
        const hit = (d.id || "").toLowerCase().includes(q)
                 || (d.label || "").toLowerCase().includes(q);
        if (hit) {
          n.removeClass("dimmed");
          n.data("matched", true);
        } else {
          n.addClass("dimmed");
          n.removeData("matched");
        }
      });
      cy.edges().forEach(e => e.addClass("dimmed"));
    });
  });
})();
