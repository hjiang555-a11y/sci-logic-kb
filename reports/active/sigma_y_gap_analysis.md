# Sigma_y(1s) Evidence Gap Analysis

This report analyzes which parts of the la.sigma_y_1s logic chain are supported by the current evidence layer.

## 1. Logic Node Coverage

| Logic Node | Evidence Count | Status | Primary Sources |
| :--- | :---: | :---: | :--- |
| la.mirror_coating_noise | 0 | ❌ BLANK |  |
| la.substrate_thermal_noise | 27 | ✅ Covered | li2018, schioppo2021, wu2016... |
| la.cavity_geometry | 2 | ✅ Covered | li2018, chen2014 |
| la.vibration_sensitivity | 1 | ✅ Covered | lezius2016 |
| la.thermal_gradients | 0 | ❌ BLANK |  |
| la.acceleration_noise | 2 | ✅ Covered | sinclair2019_5xulcnp3, dix-matthews2021_bv4dl5z6 |
| la.pdh_locking_error | 8 | ✅ Covered | young1999, kudelin2024, torcheboeuf2017... |
| la.shot_noise_limit | 0 | ❌ BLANK |  |
| la.electronic_drift | 3 | ✅ Covered | xia2025, wang2025, coddington2010 |


## 2. Unmapped Evidence Nodes
Total unmapped nodes: 1609
These nodes are existing in the evidence layer but don't fit the current la.sigma_y_1s la.decomposition markers.

- evrel_YYXGH9X3_rel.schliesser_2011_12_13: None
- evrel_KH82PQJ2_rel.hu_2015_U15_01: None
- evrel_BWX8NI2P_rel.lezius_2016_ez04: None
- evrel_LBSZCU7P_rel.cai_2020_ai20_06: None
- evrel_CA55MEKS_rel.rao_2019_19_05: None
- evrel_BG93PZPK_rel.papp_2013_13_07: None
- evrel_5R8PUBX7_rel.cuyvers_2021_V21_05: None
- evid_QIFVVUIH_ent.pku_dual_comb_microwave_sync_c24: 北大双梳增强微波钟同步系统（Chen Z. 2024）
- evrel_Y7KZ89LA_rel.inaba_2013_na13_03: None
- evrel_5NSQLZTS_rel.droste_2016_R16_03: None
- evrel_EBNL35EE_rel.stern_2018_18_05: None
- evrel_T8JR8IJ7_rel.jiang_2010_01: None
- evrel_BACON2021_rel.bacon_2021_ac21_03: None
- evid_SCI-ESA-HRE-ESR-ISOC_ent.space_frequency_comb_sfc: 空间频率梳 SFC（I-SOC 光↔微波桥）
- evrel_EGAZKLXR_rel.young_1999_13: None
- evrel_4QVEXY63_rel.lee_2026_01: None
- evrel_52N4T2DE_rel.lamb_2018_M18_01: None
- evrel_CEB7L6EM_rel.wang_2025_25_09: None
- evrel_K5JMAYPZ_rel.schioppo_2021_c03: None
- evrel_HSRPL6ZX_rel.del_2014_14_05: None
- ... and 1589 more.
