# Ultrastable Laser — Metric Chains (Curated)

> **Curated from knowledge graph + `_meta/architecture.md` 四栏对照表.**
> Each chain = one real research trajectory, not a combinatorial permutation.
>
> Auto-generated v1 (591 chains, combinatorial) → [`reports/archive/metric_chains_ultrastable-laser_v1_auto.md`](../archive/metric_chains_ultrastable-laser_v1_auto.md).
>
> **Related**: [`_meta/architecture.md`]../../topics/ultrastable-laser/_meta/architecture.md) (limitation→breakthrough table) · [`synthesis/breakthrough_paths_matrix.md`]../../topics/ultrastable-laser/synthesis/breakthrough_paths_matrix.md) (path×condition matrix).

---

## Chain Structure

Each chain follows the pattern:

```
Start Metric → Entity → Bounding Principle → Resolution Method → Improved Metric
```

**Start Metric** = the performance bottleneck (e.g. σ_y instability).
**Bounding Principle** = the physical mechanism that limits performance.
**Resolution Method** = how researchers overcome (or partially overcome) that limit.
**Improved Metric** = the resulting performance gain (quantified where possible).

---

## Chain Group A: Brownian Thermal Noise (`pri.brownian_thermal_noise_fdt`)

**Limitation**: Mirror substrate (~84%), coating (~15%), and spacer (~1%) Brownian motion sets the fundamental σ_y floor for FP-cavity-stabilized lasers. Governed by fluctuation-dissipation theorem (FDT).

### A1. Crystalline Coating → Reduced Coating Loss

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.fractional_freq_instability_m17` | σ_y = 4×10⁻¹⁷ (Matei 2017, Si cavity IBS coating limit) |
| Entity | `ent.si_crystal_fp_cavity_k12` | Si single-crystal cryogenic FP reference cavity |
| Bounding Principle | `pri.brownian_thermal_noise_fdt` | Brownian thermal noise — FDT |
| Resolution Method | `meth.crystalline_coating_deposition` | AlGaAs/GaAs epitaxial crystalline coating |
| → Improved Metric | `met.algaas_coating_loss_angle_c13` | AlGaAs coating loss angle φ < 2.3×10⁻⁵ @ 17 K (Lee 2026) |

**σ_y contribution**: ~4× improvement in coating thermal noise (Matei 2017 IBS → Lee 2026 AlGaAs).  
**Key papers**: Cole 2013 (first demo), Matei 2017 (IBS limit exposed), Kedar 2023 (further characterization), **Lee 2026** (current world record 2.5×10⁻¹⁷ with AlGaAs @ 17 K).  
**Status**: ✅ Demonstrated. Active area — further material optimization ongoing.

### A2. Cryogenic Si Cavity → Enhanced Mechanical Q

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.fractional_freq_instability_k12` | σ_y ~1×10⁻¹⁶ (Kessler 2012, first cryogenic Si demo) |
| Entity | `ent.si_crystal_fp_cavity_k12` | Si single-crystal cryogenic FP reference cavity |
| Bounding Principle | `pri.brownian_thermal_noise_fdt` | Brownian thermal noise — FDT |
| Resolution Method | `meth.cryogenic_silicon_stabilization` | Cryogenic Si operation (124 K → 17 K → 4 K → sub-5 K) |
| → Improved Metric | `met.allan_deviation_cryo` | σ_y = 2.5×10⁻¹⁷ (Lee 2026, 17 K + AlGaAs + dual-cavity averaging) |

**σ_y contribution**: σ_y ∝ √T — cooling from 300 K → 17 K gives ~4× thermal noise reduction.  
**Key papers**: Kessler 2012 (124 K first demo, ~1×10⁻¹⁶), Robinson 2019 (4 K Si4, σ_y ~10⁻¹⁷), Chen 2025 (sub-5 K Si1, MDEV ~10⁻¹⁷), **Lee 2026** (17 K + AlGaAs, 2.5×10⁻¹⁷ current record).  
**Status**: ✅ Demonstrated. Next frontier: sub-5 K + crystalline coating combination targeting ~10⁻¹⁸.

### A3. Long Cavity → Thermal Noise Dilution

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.fractional_freq_instability_w08` | σ_y (Webster 2008, ULE cavity thermal noise limit) |
| Entity | `ent.fp_cavity_system` | Rigid F-P reference cavity system |
| Bounding Principle | `pri.brownian_thermal_noise_fdt` | Brownian thermal noise — FDT |
| Resolution Method | (long cavity design) | σ_y ∝ 1/L — doubling cavity length halves thermal noise contribution |
| → Improved Metric | `met.allan_deviation_cryo` | σ_y < 1×10⁻¹⁶ (Häfner 2015, 48 cm), σ_y improved (Parke 2025, 68 cm) |

**σ_y contribution**: L: 10 cm → 48 cm ≈ 5× improvement; 10 cm → 68 cm ≈ 7× improvement.  
**Key papers**: Häfner 2015 (48 cm ULE, σ_y < 1×10⁻¹⁶), Parke 2025 (68 cm, longest to date).  
**Status**: ✅ Demonstrated. Diminishing returns from volume/engineering cost beyond ~50 cm.

### A4. Multi-Cavity Frequency Averaging → √N Noise Reduction

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.fractional_freq_instability_m17` | σ_y = 4×10⁻¹⁷ (Matei 2017, single cavity) |
| Entity | `ent.si_crystal_fp_cavity_k12` | Si single-crystal cryogenic FP reference cavity |
| Bounding Principle | `pri.brownian_thermal_noise_fdt` | Brownian thermal noise — FDT |
| Resolution Method | (dual/triple cavity averaging) | Independent cavities → uncorrelated noise averages as 1/√N |
| → Improved Metric | `met.allan_deviation_cryo` | σ_y = 1.8×10⁻¹⁷ (Lee 2026, Si2-Si3 dual-cavity average) |

**σ_y contribution**: √2 improvement for 2 cavities (Lee 2026, 2.5×10⁻¹⁷ → 1.8×10⁻¹⁷).  
**Key papers**: Chen 2020 (dual cubic cavity, ULE), Lee 2026 (Si2-Si3 dual-cavity average).  
**Status**: ✅ Demonstrated. Path to sub-10⁻¹⁷ single-cavity equivalent via 3+ cavity averaging.

---

## Chain Group B: RAM-Induced PDH Frequency Offset (`pri.ram_pdh_frequency_offset`)

**Limitation**: Residual Amplitude Modulation (RAM) in EOM creates a false PDH error signal zero-crossing, biasing the locked laser frequency.

### B1. Brewster-Angle EOM → Passive RAM Suppression

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.ram_fractional_instability` | RAM-induced fractional frequency instability |
| Entity | `ent.brewster_eom_t16` | Brewster-angle EOM (Tai 2016) |
| Bounding Principle | `pri.ram_pdh_frequency_offset` | RAM → PDH frequency offset |
| Resolution Method | `pri.brewster_angle_ram_suppression` | Brewster-angle EOM passively suppresses etalon RAM |
| → Improved Metric | (σ_y RAM contribution reduced to ~10⁻¹⁶ level) |

**σ_y contribution**: Engineering-enabling — suppresses RAM below thermal noise floor so it doesn't eat σ_y margin.  
**Key papers**: Tai 2016 (Brewster EOM demo), Zhang 2014 (active RAM servo, κ=28 kHz/(m/s²) bias eliminated).  
**Status**: ✅ Demonstrated. Not a current σ_y bottleneck but essential for reaching thermal noise limit.

---

## Chain Group C: Fiber Thermal Phase Noise (`pri.fiber_thermal_noise_wanser`)

**Limitation**: Thermodynamic phase noise in optical fiber (Wanser model) limits fiber-based frequency references to σ_y ~10⁻¹⁴.

### C1. Hollow-Core Fiber → Reduced Thermal Noise

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.freq_spectral_density` | Laser frequency noise spectral density (fiber interferometer) |
| Entity | `ent.fiber_interferometer` | Fiber Michelson interferometer (frequency reference) |
| Bounding Principle | `pri.fiber_thermal_noise_wanser` | Fiber intrinsic thermal noise (Wanser model) |
| Resolution Method | (hollow-core fiber) | HC-ARF / ULE-HCF — light propagates in air/vacuum, not silica |
| → Improved Metric | (σ_y: ~10⁻¹⁴ → ~10⁻¹⁵, fiber-branch SOTA) |

**σ_y contribution**: ~10× improvement over solid-core fiber. Enables compact fiber-based references approaching cavity performance regime.  
**Key papers**: Belardi 2015 (HC-ARF concept), Michaud-Belleau 2022 (demonstration), Ding 2025 (ULE-HCF).  
**Status**: ✅ Demonstrated. Active area — further loss reduction needed.

### C2. Double-Winding → Vibration Sensitivity Cancellation

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.freq_noise_from_vibration` | Vibration-induced frequency noise (fiber spool) |
| Entity | `ent.double_winding_fiber_spool_hjc19` | Double-winding anti-vibration fiber spool (Huang JC 2019b) |
| Bounding Principle | `pri.fiber_thermal_noise_wanser` | Fiber thermal noise |
| Resolution Method | `pri.double_winding_vibration_cancellation_hjc19` | Symmetric double-winding cancels vibration sensitivity |
| → Improved Metric | (σ_y improved ~2–3× via vibration cancellation) |

**σ_y contribution**: ~2–3× improvement within fiber branch.  
**Key papers**: Huang JC 2019b.  
**Status**: ✅ Demonstrated.

---

## Chain Group D: Rayleigh Backscattering Noise (`pri.rayleigh_backscattering_noise`)

**Limitation**: Rayleigh backscattering in fiber creates spurious interferometer signals, limiting fiber delay line (FDL) frequency discrimination.

### D1. AOM Heterodyne Frequency Shift → Backscatter Rejection

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.freq_spectral_density` | Frequency noise spectral density (FDL) |
| Entity | `ent.fiber_delay_line_reference` | Fiber delay line reference system |
| Bounding Principle | `pri.rayleigh_backscattering_noise` | Rayleigh backscattering noise |
| Resolution Method | `pri.aom_heterodyne_fiber_detection` | AOM heterodyne detection — frequency-shifts signal away from backscatter |
| → Improved Metric | (FDL σ_y enabled to ~10⁻¹⁴ level) |

**σ_y contribution**: Enabling — without AOM shift, backscatter would dominate and prevent usable FDL operation.  
**Key papers**: Jiang 2010.  
**Status**: ✅ Demonstrated.

---

## Chain Group E: Vibration / Acceleration Sensitivity

**Limitation**: Environmental vibration couples into cavity length via acceleration sensitivity κ (kHz/g), degrading σ_y especially at low Fourier frequencies.

### E1. Symmetric Geometry + Deformation Compensation → Force-Insensitive Cavity

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.acceleration_sensitivity_millo09` | Acceleration sensitivity (Millo 2009, vertical/horizontal cavities) |
| Entity | `ent.fp_cavity_system` | Rigid F-P reference cavity system |
| Bounding Principle | `pri.cavity_deformation_compensation` | Cavity deformation compensation — vibration-insensitive design |
| Resolution Method | (symmetric mounting + cutout optimization) | Support points at Airy points; cutout cavity mount design |
| → Improved Metric | `met.acceleration_sensitivity_t18` | κ < 2×10⁻¹⁰/g (Häfner 2015), κ ~10⁻¹¹/g (Webster 2011 cubic) |

**σ_y contribution**: Engineering-enabling — κ from kHz/g → 0.1 kHz/g suppresses vibration-induced σ_y by >10×, exposing thermal noise floor.  
**Key papers**: Webster 2007 (cutout mount), Webster 2011 (cubic force-insensitive), Chen 2020 (cubic dual cavity), Sanjuan 2019 (BOOST cubic), Häfner 2015 (self-balancing 48 cm).  
**Status**: ✅ Demonstrated. Mature engineering — not a primary research frontier.

---

## Chain Group F: Shot Noise Frequency Limit (`pri.shot_noise_frequency_limit`)

**Limitation**: Quantum shot noise in PDH detection sets the ultimate frequency discrimination floor.

### F1. Higher Optical Power + Precision Detection

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.freq_spectral_density` | Frequency noise spectral density (detection limit) |
| Entity | `ent.fp_cavity_system` | Rigid F-P reference cavity system |
| Bounding Principle | `pri.shot_noise_frequency_limit` | Shot noise frequency discrimination limit |
| Resolution Method | (higher power + low-noise photodetection) | Increase cavity transmitted power; reduce detector NEP |
| → Improved Metric | (shot noise floor well below thermal noise for current systems) |

**σ_y contribution**: Not a current bottleneck — shot noise limit (~10⁻¹⁸ level for typical PDH parameters) is below thermal noise for all demonstrated systems.  
**Key papers**: Drever 1983 (PDH theory), Grote 2016 (high-power low-noise photodetector).  
**Status**: ✅ Resolved — not actively limiting.

---

## Cross-Reference: Synthesis Pages

Each chain group maps to a dedicated synthesis page for deeper reading:

| Chain Group | Synthesis Page |
|-------------|---------------|
| A (Thermal Noise) | [`synthesis/thermal_noise_landscape.md`]../../topics/ultrastable-laser/synthesis/thermal_noise_landscape.md) |
| A1–A2 (Cryogenic + Coating) | [`synthesis/cryogenic_roadmap.md`]../../topics/ultrastable-laser/synthesis/cryogenic_roadmap.md) |
| A1–A4 (All paths matrix) | [`synthesis/breakthrough_paths_matrix.md`]../../topics/ultrastable-laser/synthesis/breakthrough_paths_matrix.md) |
| B (RAM/PDH) | [`synthesis/ram_and_pdh_error_budget.md`]../../topics/ultrastable-laser/synthesis/ram_and_pdh_error_budget.md) |
| C (Fiber) | [`synthesis/fiber_stabilization_landscape.md`]../../topics/ultrastable-laser/synthesis/fiber_stabilization_landscape.md) |
| E (Vibration) | [`synthesis/vibration_insensitivity_landscape.md`]../../topics/ultrastable-laser/synthesis/vibration_insensitivity_landscape.md) |
| Record timeline | [`synthesis/stability_record_timeline.md`]../../topics/ultrastable-laser/synthesis/stability_record_timeline.md) |

---

## Chain Coverage Summary

| Limitation | Breakthrough Paths | Status | σ_y Impact |
|------------|-------------------|--------|-----------|
| Brownian Thermal Noise | Crystalline coating, cryogenic Si, long cavity, multi-cavity averaging | ✅ All demonstrated | ~10⁻¹⁶ → 2.5×10⁻¹⁷ (current record) |
| RAM PDH Offset | Brewster EOM, active servo | ✅ Demonstrated | Engineering-enabling |
| Fiber Thermal Noise | Hollow-core fiber, double-winding | ✅ Demonstrated | Fiber branch: ~10⁻¹⁴ → ~10⁻¹⁵ |
| Rayleigh Backscattering | AOM heterodyne shift, HC low-scatter | ✅ Demonstrated | Enabling for FDL |
| Vibration / Acceleration | Symmetric geometry, external isolation | ✅ Demonstrated | Engineering-enabling |
| Shot Noise | Higher power, precision detection | ✅ Resolved | Not limiting for current systems |

> **Open chain gaps** (from `reports/active/chain_gap_ultrastable_v2.md`): 7 breakthrough-tier gaps **全部清零** (阶段 C closed). Remaining 14 INFO-level gaps are evidence-tier papers where open chains are allowed per SCHEMA §9.1.

---

*Curated 2026-05-02. Replaces auto-generated v1 (591 combinatorial chains, archived).*
*Update this file when: a new σ_y world record is set; a new limitation principle is identified; a new breakthrough path is demonstrated.*
