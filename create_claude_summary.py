#!/usr/bin/env python3
"""
创建CLAUDE.md摘要文件
"""

import os
import re
from pathlib import Path
import subprocess

# Obsidian API配置
WINDOWS_IP = "172.20.96.1"
OBSIDIAN_KEY = "f65c3bdf4c4ed108c4046114184fba8b352449dab516d662cc95bce1eb6585a2"
OBSIDIAN_BASE = f"https://{WINDOWS_IP}:27124"
OBSIDIAN_HEADER = f"Authorization: Bearer {OBSIDIAN_KEY}"
OBSIDIAN_PROJECT = "sci-logic-kb"

def write_obsidian_file(filename: str, content: str) -> bool:
    """写入文件到Obsidian"""
    import subprocess

    url = f"{OBSIDIAN_BASE}/vault/Claude/projects/{OBSIDIAN_PROJECT}/{filename}"
    curl_cmd = ["curl", "-s", "-k", "-H", OBSIDIAN_HEADER, "-X", "PUT",
                "-H", "Content-Type: text/markdown", "--data-binary", "@-", url]

    try:
        result = subprocess.run(curl_cmd, input=content.encode('utf-8'), capture_output=True, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"写入文件错误 {filename}: {e}")
        return False

def extract_claude_summary() -> str:
    """提取CLAUDE.md的关键摘要"""
    claude_path = Path("/home/hjian/sci-logic-kb/CLAUDE.md")

    if not claude_path.exists():
        return "# CLAUDE.md 摘要\n\nCLAUDE.md文件不存在。"

    with open(claude_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取仓库用途
    purpose_match = re.search(r"## 仓库用途[\s\S]*?---", content)
    purpose = purpose_match.group(0) if purpose_match else ""

    # 提取GitHub Copilot优先原则
    copilot_match = re.search(r"## GitHub Copilot 优先原则[\s\S]*?---", content)
    copilot = copilot_match.group(0) if copilot_match else ""

    # 提取单篇论文处理流程
    workflow_match = re.search(r"## 单篇论文处理流程[\s\S]*?---", content)
    workflow = workflow_match.group(0) if workflow_match else ""

    # 提取质量检查清单
    quality_match = re.search(r"## 质量检查清单[\s\S]*?---", content)
    quality = quality_match.group(0) if quality_match else ""

    # 提取节点ID命名规范
    naming_match = re.search(r"## 节点 ID 命名规范[\s\S]*?---", content)
    naming = naming_match.group(0) if naming_match else ""

    # 提取已有节点参考
    nodes_match = re.search(r"## 已有节点参考[\s\S]*?---", content)
    nodes = nodes_match.group(0) if nodes_match else ""

    # 提取处理顺序建议
    order_match = re.search(r"## 处理顺序建议[\s\S]*?(?=```|$)", content)
    order = order_match.group(0) if order_match else ""

    # 生成摘要
    summary = f"""# CLAUDE.md 工作流程摘要

> **来源**: [[CLAUDE.md]]
> **提取时间**: {subprocess.check_output(['date']).decode().strip()}
> **主题**: Claude Code行为规范、工作流程、质量检查

## 仓库用途与定位

{purpose[:800] + "..." if len(purpose) > 800 else purpose}

## GitHub Copilot 优先原则

{copilot[:1500] + "..." if len(copilot) > 1500 else copilot}

## 单篇论文处理流程

{workflow[:2500] + "..." if len(workflow) > 2500 else workflow}

## 质量检查清单

{quality[:2000] + "..." if len(quality) > 2000 else quality}

## 节点ID命名规范

{naming[:1000] + "..." if len(naming) > 1000 else naming}

## 已有节点参考（超稳激光专题）

{nodes[:3000] + "..." if len(nodes) > 3000 else nodes}

## 处理顺序建议

{order[:1500] + "..." if len(order) > 1500 else order}

## 快速参考

### 核心工作流程
1. **确定目标论文**：从QUEUE.md选取，记录ZOTERO_KEY
2. **获取论文PDF**：通过Zotero API获取PDF文件路径
3. **阅读PDF**：使用Read工具分批读取（最多20页/次）
4. **提取YAML**：按SCHEMA.md模板提取节点和关系
5. **写入文件**：保存到 `topics/<topic>/papers/{{author}}{{year}}.yaml`
6. **更新队列**：在SCHEMA.md中补充记录
7. **提交**：通过GitHub PR流程提交更改

### 质量检查关键点
- [ ] 节点ID全局唯一（不与同专题及其他专题文件冲突）
- [ ] 所有relation有 `source.claim`（原文论断）
- [ ] 所有metric的 `demonstrated_value` 有 `conditions`
- [ ] 原理节点有 `conditions` 或 `applicable_when`
- [ ] 跨文件引用的节点在 `note` 中注明来源文件
- [ ] 没有把"方法"建为"实体"（PDH是 `meth`，不是 `ent`）

### 节点ID命名规范
| 类型 | 格式 | 示例 |
|------|------|------|
| 实体 | `ent.{{描述词}}_{{可选后缀}}` | `ent.fp_cavity_system` |
| 原理 | `pri.{{描述词}}` | `pri.brownian_thermal_noise_fdt` |
| 方法 | `meth.{{描述词}}` | `meth.pdh_locking` |
| 指标 | `met.{{描述词}}_{{可选后缀}}` | `met.laser_linewidth_563nm` |
| 关系 | `rel.{{文件首字母缩写}}{{两位序号}}` | `rel.N01`（N=Numata） |

### 已有核心节点（部分）
- **drever1983**: `ent.rf_phase_modulator`, `pri.pdh_heterodyne_detection`, `meth.pdh_locking`
- **young1999**: `ent.dye_laser_563nm`, `ent.vibration_isolation`, `pri.ule_zero_cte`
- **numata2004**: `ent.fp_cavity_system`, `ent.mirror_substrate`, `pri.brownian_thermal_noise_fdt`
- **kessler2012**: `ent.si_crystal_fp_cavity_k12`, `pri.silicon_cte_zero_crossing_124k`
- **matei2017**: `pri.flicker_noise_linewidth_divergence`, `met.fractional_freq_instability_m17`

## 相关链接
- [[sci-logic-kb-overview]] - 知识库总览
- [[SCHEMA-summary]] - 架构规范摘要
- [[TOPICS-summary]] - 专题体系摘要
- [[papers-index]] - 论文索引
- [[nodes-index]] - 节点索引
- [[topics-status]] - 专题状态

---
*本摘要由自动化脚本生成，建议与CLAUDE.md源文件同步更新*
"""

    return summary

def main():
    """主函数"""
    print("开始创建CLAUDE摘要...")

    content = extract_claude_summary()

    if write_obsidian_file("CLAUDE-summary.md", content):
        print("✅ CLAUDE-summary.md 创建成功")
    else:
        print("❌ CLAUDE-summary.md 创建失败")

if __name__ == "__main__":
    main()