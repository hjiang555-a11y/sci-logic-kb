# Optical Frequency Combs — Metric Chains (Curated · Multi-Track)

> **Curated from `_meta/architecture.md` + `_meta/scoping_principles.md` v2.**
> OFC is a **multi-track** topic: unlike ultrastable-laser's single-axis σ_y, each sub-domain has its own primary metric and breakthrough criterion.
>
> **Template note**: Most sci-logic-kb topics are single-axis (Type A, like ultrastable-laser). OFC is the exception. This report adapts the metric chains format for multi-track architecture.
>
> **Related**: [`_meta/scoping_principles.md`](../../topics/optical-frequency-combs/_meta/scoping_principles.md) (9-track definitions) · [`_meta/architecture.md`](../../topics/optical-frequency-combs/_meta/architecture.md) (tech/app separation) · [`synthesis/a1_femtosecond_comb_platforms_timeline.md`](../../topics/optical-frequency-combs/synthesis/a1_femtosecond_comb_platforms_timeline.md) (A1 deep-dive).

---

## Multi-Track Principle

> **光学频率梳专题不适合单一主线指标；按应用子域分别定义。** — scoping_principles.md §1.1

Each track has its own:
- **Primary metric** — what "better" means on this track
- **Enabling principles** — the physics that makes progress possible
- **Current SOTA** — the best demonstrated value and who holds it
- **Key papers** — representative breakthroughs

A paper qualifies as `breakthrough` if it refreshes **any one** track's primary metric record (scoping_principles §1.3).

---

## Track Group A: Comb Technology

### A1-Rep: High Repetition-Rate Combs

| | |
|---|---|
| **Primary metric** | Base f_rep (non-harmonic, direct locking) + self-referencing feasibility |
| **Secondary metrics** | f_CEO SNR (@ RBW), per-tooth power, octave-span coverage |
| **Core principle** | `pri.high_frep_bandwidth_power_tradeoff` — E_pulse = P_avg / f_rep; f_rep ↑ ⇒ pulse energy ↓ ⇒ supercontinuum threshold harder to reach |
| **Current SOTA** | **10 GHz** base f_rep with self-referencing (Bartels 2009, Ti:sapphire KLM) |
| **Key papers** | Bartels 2009 (10 GHz 🏆), Wang 2014 (500 MHz Yb), Ma 2018 (750 MHz Yb) |
| **Next bottleneck** | >10 GHz needs harmonic mode-locking or microcomb hybrid (→ A2) |

### A1-Noise: Low Phase-Noise / Low Timing Jitter Combs

| | |
|---|---|
| **Primary metric** | f_CEO integrated phase noise (rad, specify integration band) or integrated timing jitter (as) |
| **Secondary metrics** | In-loop σ_y(1 s), per-tooth linewidth |
| **Core principle** | `meth.nalm_locking` — NALM (Nonlinear Amplifying Loop Mirror) replaces NPR, enabling PM-compatible low-noise mode-locking |
| **Current SOTA** | **<40 as** integrated timing jitter (Kuse 2016, all-PM Er:fiber NALM) |
| **Key papers** | Kuse 2015 (all-PM groundwork), Kuse 2016 (<40 as 🏆), Li 2017b (Yb PM NALM first), Ma 2018 (<1 rad f_CEO + in-loop σ_y ~10⁻¹⁸) |
| **Structural insight** | NPR → NALM paradigm shift was the decisive transition: PM compatibility + environmental robustness + lower jitter obtained simultaneously |

### A1-Robust: Engineered / All-PM / Compact Combs

| | |
|---|---|
| **Primary metric** | Continuous stable lock duration + SWaP (footprint / power consumption) |
| **Secondary metrics** | Single-actuator bandwidth, environmental tolerance range, H-maser comparison residual |
| **Core principle** | Single-actuator simplification — fewer degrees of freedom = lower assembly complexity + better long-term stability |
| **Current SOTA** | Single fiber mechanical actuator, H-maser 1 s Allan 330 μHz (Cai 2020) |
| **Key papers** | Zhang 2015 (intracavity EOM), Kuse 2016 (all-PM NALM), Li 2017b (Yb all-PM), Cai 2020 (single-actuator compact) |
| **Note** | Cai 2020's 330 μHz is not a record-breaking σ_y value, but represents the frontier of simultaneous compactness + stability — tier `evidence` |

### A2-DKS: Dissipative Kerr Soliton Microcombs

| | |
|---|---|
| **Primary metric** | Phase noise @ offset + **pump-to-comb conversion efficiency** + integration SWaP |
| **Secondary metrics** | f_rep, bandwidth, post-broadening bandwidth |
| **Core principle** | `pri.dissipative_kerr_soliton` — DKS paradigm: CW pump → Kerr nonlinearity + anomalous dispersion → soliton pulse train |
| **Current SOTA** | Battery-operated fully integrated III–V/Si₃N₄ Kerr microcomb (Stern 2018) |
| **Key papers** | Papp 2013 (first microcomb), Stern 2018 (battery-operated integrated 🏆), Shu 2022 (AlGaAsOI dark pulse) |
| **Synthesis** | Synthesis page pending (B-2 target) |

### A3-Astro: Astrocombs

| | |
|---|---|
| **Primary metric** | Comb line uniformity (dB, mode-filtered) + long-term stability (hours-scale) |
| **Secondary metrics** | Wavelength coverage, single-tooth repeatability |
| **Core principle** | Mode filtering for uniform comb tooth spacing at astronomical spectrograph resolution |
| **Current SOTA** | Continuous UV–blue-green astrocomb (Cheng 2024) |
| **Key papers** | Metcalf 2019 (HPF NIR astrocomb), Cheng 2024 (UV–blue-green continuous 🏆) |
| **Synthesis** | Pending (paper count < 5; hold per A1 synthesis §7) |

---

## Track Group B: Comb Applications

### B-Spec: Spectral Broadening / Wavelength Extension

| | |
|---|---|
| **Primary metric** | **Absolute spectral PSD at transferred band** (W/Hz or dBm/Hz) + **pump-to-signal conversion efficiency** |
| **Secondary metrics** | Coverage band, coherent transfer fidelity, σ_y transfer residual |
| **Core principle** | `pri.supercontinuum_coherence` — coherent spectral broadening via χ³ nonlinearity in HNLF/waveguide; coherence preserved when soliton fission avoided |
| **Current SOTA** | XUV comb generation (L88UAAEQ); UV–blue-green transfer (NDSVHPF5) |
| **Key papers** | Newbury 2005 (supercontinuum coherence theory), Diddams 2000 (PCF octave), Lesko 2022 (CEP HHG comb) |
| **Critical distinction** | Judged by **transferred PSD + conversion efficiency**, NOT by coverage bandwidth alone (per user directive in scoping_principles v2) |

### B-FreqSyn: Frequency Synthesis / Metrology Links

| | |
|---|---|
| **Primary metric** | σ_y(τ = 1 s) optical-to-optical / optical-to-microwave transfer residual + distribution distance |
| **Secondary metrics** | Comb-tooth-CW beat SNR, multi-branch phase synchronization, coherent link length |
| **Core principle** | `pri.optical_frequency_division_microwave` — optical reference → comb → microwave with σ_y transfer at or below 10⁻¹⁷ level |
| **Current SOTA** | Photonic microwave synthesis: −171 dBc/Hz @ 1 Hz, 10 GHz (Giunta 2019); broadband synthesis accuracy < 2×10⁻¹⁹ 35h (Giunta 2020) |
| **Key papers** | Fortier 2011 (OFD first <10⁻¹⁵ microwave), Fortier 2012 (hybrid osc 420 as jitter), Leopardi 2017 (3×10⁻¹⁸), Giunta 2019 (−171 dBc/Hz 🏆), Giunta 2020 (10⁻²⁰ accuracy 🏆) |
| **Synthesis** | [`b_freqsyn_frequency_synthesis.md`](../../topics/optical-frequency-combs/synthesis/b_freqsyn_frequency_synthesis.md) |

### B-DCS: Dual-Comb Spectroscopy

| | |
|---|---|
| **Primary metric** | Mutual coherence time + spectral coverage bandwidth |
| **Secondary metrics** | Resolution × bandwidth product, acquisition rate (high-f_rep speed advantage) |
| **Core principle** | `pri.dual_comb_interferometry` — two mutually coherent combs with slight f_rep offset; heterodyne down-conversion maps optical spectrum to RF |
| **Current SOTA** | 113 km open-path bidirectional DCS (Han 2024); 1 GHz f_rep DCS (Lesko 2020); space-qualified DCS (Probst 2021) |
| **Key papers** | Coddington 2010 (coherent DCS first demo), Cossel 2017 (airborne open-path), Coburn 2018 (field-deployed 🏆), Lesko 2020 (1 GHz f_rep), Probst 2021 (space-qualified), Han 2024 (113 km bidirectional 🏆) |
| **Synthesis** | [`b_dcs_dual_comb_spectroscopy.md`](../../topics/optical-frequency-combs/synthesis/b_dcs_dual_comb_spectroscopy.md) |

### B-MIR: Mid-Infrared Comb Spectroscopy

| | |
|---|---|
| **Primary metric** | Detection sensitivity (cm⁻¹/√Hz) + coverage band (μm) |
| **Secondary metrics** | Single-mode power, molecular fingerprint cross-sensitivity |
| **Core principle** | MIR comb generation via difference frequency generation (DFG) or OPO from near-IR comb |
| **Current SOTA** | 1 GHz broadband MIR comb (Hoghooghi 2022) |
| **Key papers** | Hoghooghi 2022 (1 GHz MIR 🏆) |
| **Synthesis** | Pending (paper count still accumulating) |

---

## Cross-Topic Interfaces

OFC connects to other topics through three CONDITIONED-BY / ENABLES edges:

| From | Edge | To | Metric Chain |
|------|------|-----|-------------|
| Ultrastable laser | CONDITIONED-BY | OFC | `ent.fp_cavity_system` → `met.laser_linewidth_*` → comb tooth linewidth floor |
| OFC | ENABLES | Frequency standards | `pri.optical_frequency_division_microwave` → `met.σ_y_transfer_residual` → optical clock comparison |
| OFC | ENABLES | Time-frequency transfer | Comb as coherent link bridge; phase noise transfer across km-scale fiber/free-space |

---

## Track × Breakthrough Paper Matrix

| Paper | Track(s) | Record | Tier |
|-------|----------|--------|------|
| Bartels 2009 | A1-Rep | 10 GHz base f_rep + self-ref | breakthrough |
| Kuse 2016 | A1-Noise + A1-Robust | <40 as jitter + all-PM NALM | breakthrough |
| Ma 2018 | A1-Rep + A1-Noise | 750 MHz + <1 rad f_CEO | breakthrough |
| Stern 2018 | A2-DKS | Battery-operated integrated DKS | breakthrough |
| Cheng 2024 | A3-Astro | UV–blue-green continuous | breakthrough |
| Coburn 2018 | B-DCS | Field-deployed DCS | breakthrough |
| Coddington 2010 | B-DCS | First coherent DCS | breakthrough |

> Full matrix at paper level is maintained in YAML `meta.breakthrough_tracks` and synthesis pages.

---

## Synthesis Coverage Status

| Track | Synthesis Page | Status |
|-------|---------------|--------|
| A1 (Rep + Noise + Robust) | [`a1_femtosecond_comb_platforms_timeline.md`](../../topics/optical-frequency-combs/synthesis/a1_femtosecond_comb_platforms_timeline.md) | ✅ Active |
| A2-DKS | [`a2_dks_microcombs.md`](../../topics/optical-frequency-combs/synthesis/a2_dks_microcombs.md) | ✅ Active |
| A3-Astro | — | ⬜ Hold (<5 papers) |
| B-Spec | — | ⬜ Hold |
| B-FreqSyn | [`b_freqsyn_frequency_synthesis.md`](../../topics/optical-frequency-combs/synthesis/b_freqsyn_frequency_synthesis.md) | ✅ Active |
| B-DCS | [`b_dcs_dual_comb_spectroscopy.md`](../../topics/optical-frequency-combs/synthesis/b_dcs_dual_comb_spectroscopy.md) | ✅ Active |
| B-MIR | — | ⬜ Hold (<5 papers) |

---

*Curated 2026-05-02. Update when: a track record is broken; a new sub-domain emerges; synthesis coverage changes.*
