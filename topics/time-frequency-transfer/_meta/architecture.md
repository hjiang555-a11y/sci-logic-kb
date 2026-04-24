# Time-Frequency Transfer — Topic Architecture

> **Status**: 🟢 `growing` — 已从 framework 骨架扩展为多批 evidence 规模（精确数字见 [`INDEX.md`](../INDEX.md) / `python scripts/stats.py`）；Level 1 骨架已填充 4 个总节点。论文覆盖欧洲光纤相干链路（Calonico/Raupach/Lopez/Guéna）、中国光纤链路（Cheng/Xu/Chen/Wang/Shen/Zhang/Xue/Quan）、自由空间（Sinclair/Swann/Bodine/Dix-Matthews/Caldwell）、卫星/微波（Exertier/Nakamura/Kim/Turza/Zeng）五大分支。
>
> Source of truth: SCHEMA.md

## Architecture (v4.5, after 2026-04-23 batch ingest)

```
时间频率传递系统
├── 空间光钟任务（framework, cacciapuoti2017）
│   ├── ent.space_optical_clock_mission（I-SOC 代表实例，Level 1）
│   ├── ent.space_lattice_optical_clock_sloc / ent.space_frequency_comb_sfc
│   ├── ent.microwave_link_mwl / ent.pulsed_optical_link_elt_plus / ent.frequency_comb_optical_link_fcol
│
├── 光纤相干光学链路（Level 1 ent.coherent_optical_fiber_link，calonico2015 建立）
│   ├── Calonico 2015（INRIM 642 km, 3×10⁻¹⁹）
│   ├── Raupach 2015（PTB 1400 km Brillouin-only, 10⁻²⁰）
│   ├── Lopez 2015（telecom coexistence）
│   ├── Guéna 2017（SYRTE↔PTB Cs 喷泉 5×10⁻¹⁷）
│   ├── Xu 2019（10⁻²¹ 互易性）
│   ├── Wang 2020 / Shen 2021 / Zhang 2022×2（中国链路）
│   ├── Clivati 2020（双偏振相干接收）
│
├── RF-over-fiber 链路（Level 1 ent.rf_over_fiber_time_transfer_link，krehlik2015 建立）
│   ├── Krehlik 2015（AGH hybrid delay comp）
│   ├── Raupach 2014（PTB 149 km chirped carrier）
│   ├── Cheng 2019 / Chen 2021（中国光纤 RF）
│   ├── Xue 2020 / Quan 2021 / Quan 2022（NTSC 光纤 RF，212 km 级联 10⁻¹⁸）
│   ├── Turza 2019（DWDM DCF 温度补偿）
│
├── 自由空间光学链路（Level 1 ent.free_space_optical_tf_link，sinclair2019 建立）
│   ├── Sinclair 2014（大气光相位 PSD ∝f⁻²·³）
│   ├── Sinclair 2019（运动平台 fs sync）
│   ├── Swann 2019（anisoplanatism）
│   ├── Bodine 2020（三节点网络）
│   ├── Dix-Matthews 2021（UWA 265 m tip-tilt, 1.6×10⁻¹⁹）
│   ├── Caldwell 2023/2024（量子极限 102 dB 链路损耗，ground↔GEO 使能）
│
├── 卫星链路（Level 1 ent.satellite_microwave_time_transfer_link，exertier2016 建立）
│   ├── Exertier 2016（GPS CV vs T2L2 sub-ns）
│   ├── Nakamura 2020（光→10 GHz 下转换 10⁻¹⁸）
│   ├── Kim 2023（跨种光钟差分光谱）
│   ├── Zeng 2024（卫星 TWTFT 大气非互易）
│
├── 核心原理（已建）
│   ├── foundational：pri.gravitational_time_dilation, pri.einstein_equivalence_principle
│   ├── domain：pri.common_view_clock_comparison, pri.non_common_view_clock_comparison,
│   │          pri.noise_cancellation_frequency_transfer, pri.fiber_propagation_reciprocity,
│   │          pri.atmospheric_optical_phase_noise_power_law,
│   │          pri.turbulence_anisoplanatism_tf_degradation,
│   │          pri.o_twtft_motion_reciprocity_breakdown,
│   │          pri.quantum_limited_photon_counted_ott,
│   │          pri.passive_reciprocal_fiber_noise_cancellation,
│   │          pri.atmospheric_non_reciprocity_satellite_twtft,
│   │          pri.differential_spectroscopy_lo_coherence_bypass
│   ├── engineering：pri.roundtrip_phase_compensation_rf_transfer,
│   │               pri.dual_polarization_coherent_endless_phase_tracking,
│   │               pri.dcf_induced_differential_delay_temp_compensation,
│   │               pri.active_tiptilt_beam_wander_suppression,
│   │               pri.cascaded_rf_stages_crosstalk_mitigation,
│   │               pri.multi_node_tf_network_closure,
│   │               pri.telecom_network_metrology_coexistence
│
└── 外围接口层（跨专题 CONDITIONED-BY）
    ├── CONDITIONED-BY ultrastable-laser（ent.fp_cavity_system，作为 LO 与干涉参考）
    ├── CONDITIONED-BY optical-frequency-combs（ent.optical_frequency_comb，Nakamura/Leopardi）
    └── CONDITIONED-BY frequency-standards（ent.optical_frequency_standard, Caldwell 2024 / Bacon 2021）
```

## Status: Growing (31 papers)

- 下一步重点：**synthesis/** 综合页（fiber / free-space / satellite 三大路线的跨论文对比）
- 4 篇可考虑升 breakthrough：Caldwell 2023（near-quantum-limit）、Bothwell 2022（mm 红移）、
  Bacon 2021（18-digit 三钟比）、Guéna 2017（首次 fiber-link Cs 喷泉比对）
- 待清理：6 篇 PDF 损坏论文（bothwell2019/2022、oelker2019、bacon2021、sullivan2001、adler2009）
  的具体参数数值需专家补充确认

---

Priority papers to ingest (从此处继续):
- Fiber link 经典早期：Ma 1994, Predehl 2012, Droste 2013
- Free-space 经典：Giorgetta 2013, Bergeron 2019

- Satellite: Fujieda 2018

