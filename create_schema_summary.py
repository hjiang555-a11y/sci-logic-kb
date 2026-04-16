#!/usr/bin/env python3
"""
创建SCHEMA.md摘要文件
"""

import os
import re
from pathlib import Path
import subprocess

# Obsidian API配置（复用现有配置）
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

def extract_schema_summary() -> str:
    """提取SCHEMA.md的关键摘要"""
    schema_path = Path("/home/hjian/sci-logic-kb/SCHEMA.md")

    if not schema_path.exists():
        return "# SCHEMA.md 摘要\n\nSCHEMA.md文件不存在。"

    with open(schema_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取关键部分
    sections = []

    # 提取版本信息
    version_match = re.search(r"\*\*版本\*\*：([^\n（]+)", content)
    version = version_match.group(1).strip() if version_match else "未知"

    # 提取变更摘要
    change_match = re.search(r"\*\*变更摘要\*\*：([\s\S]*?)---", content)
    change_summary = change_match.group(1).strip() if change_match else ""

    # 提取核心原则部分
    principles_match = re.search(r"## 一、知识库定位与核心原则[\s\S]*?---", content)
    principles = principles_match.group(0) if principles_match else ""

    # 提取系统架构部分
    architecture_match = re.search(r"## 二、系统架构[\s\S]*?---", content)
    architecture = architecture_match.group(0) if architecture_match else ""

    # 提取节点类型部分
    node_types_match = re.search(r"## 三、节点类型与属性[\s\S]*?---", content)
    node_types = node_types_match.group(0) if node_types_match else ""

    # 提取关系类型部分
    relation_types_match = re.search(r"## 四、关系类型[\s\S]*?---", content)
    relation_types = relation_types_match.group(0) if relation_types_match else ""

    # 生成摘要
    summary = f"""# SCHEMA.md 架构规范摘要

> **来源**: [[SCHEMA.md]]（{version}版本）
> **提取时间**: {subprocess.check_output(['date']).decode().strip()}
> **主题**: 知识库架构规范、节点类型、关系类型、质量原则

## 版本信息

- **当前版本**: {version}
- **变更摘要**:
{change_summary[:300] if change_summary else "无变更摘要"}
- **同步原则**: SCHEMA.md 是唯一Schema真源（source of truth）

## 核心原则摘要

{principles[:800] + "..." if len(principles) > 800 else principles}

## 系统架构摘要

{architecture[:1000] + "..." if len(architecture) > 1000 else architecture}

## 节点类型摘要

{node_types[:1500] + "..." if len(node_types) > 1500 else node_types}

## 关系类型摘要

{relation_types[:1000] + "..." if len(relation_types) > 1000 else relation_types}

## 快速参考

### 节点类型
| 类型 | 前缀 | 示例ID | 描述 |
|------|------|--------|------|
| 实体 | `ent.` | `ent.fp_cavity_system` | 物理系统、硬件组件 |
| 原理 | `pri.` | `pri.brownian_thermal_noise_fdt` | 物理原理、限制机制 |
| 方法 | `meth.` | `meth.pdh_locking` | 实验方法、技术手段 |
| 指标 | `met.` | `met.laser_linewidth` | 性能指标、测量结果 |

### 关键关系类型
- **PART-OF**: 组成关系
- **BOUNDED-BY**: 性能限制关系（必须包含 `is_system_limit` 和 `breakthrough_paths`）
- **ENABLED-BY**: 原理支撑
- **CHARACTERIZED-BY**: 指标表征
- **COMPETES-WITH**: 竞争方案
- **CONDITIONED-BY**: 外部条件（接口节点）

### 质量检查清单
1. 节点ID全局唯一
2. 所有BOUNDED-BY关系有 `is_system_limit` + `breakthrough_paths`
3. 不使用已弃用关系类型（GOVERNED-BY, SUPPORTED-BY, BREAKTHROUGH-VIA）
4. 外部条件使用CONDITIONED-BY关系
5. 跨文件引用正确标注来源

## 相关链接
- [[sci-logic-kb-overview]] - 知识库总览
- [[TOPICS-summary]] - 专题体系摘要
- [[CLAUDE-summary]] - 工作流程摘要
- [[papers-index]] - 论文索引
- [[nodes-index]] - 节点索引

---
*本摘要由自动化脚本生成，基于SCHEMA.md版本：{version}*
*建议与SCHEMA.md源文件同步更新*
"""

    return summary

def main():
    """主函数"""
    print("开始创建SCHEMA摘要...")

    content = extract_schema_summary()

    if write_obsidian_file("SCHEMA-summary.md", content):
        print("✅ SCHEMA-summary.md 创建成功")
    else:
        print("❌ SCHEMA-summary.md 创建失败")

if __name__ == "__main__":
    main()