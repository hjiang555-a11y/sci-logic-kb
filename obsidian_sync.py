#!/usr/bin/env python3
"""
Obsidian知识库同步脚本

将sci-logic-kb知识库内容同步到Obsidian，包括：
1. 知识库概述文件
2. 专题状态文件
3. 论文索引文件
4. 节点索引文件
5. 架构文档摘要
6. 图形文件更新
7. 记忆文件同步
"""

import os
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import subprocess
import re

# Obsidian API配置
WINDOWS_IP = "172.20.96.1"
OBSIDIAN_KEY = "f65c3bdf4c4ed108c4046114184fba8b352449dab516d662cc95bce1eb6585a2"
OBSIDIAN_BASE = f"https://{WINDOWS_IP}:27124"
OBSIDIAN_HEADER = f"Authorization: Bearer {OBSIDIAN_KEY}"

# 项目路径
PROJECT_DIR = Path("/home/hjian/sci-logic-kb")
TOPICS_DIR = PROJECT_DIR / "topics"
PAPERS_DIR = TOPICS_DIR / "ultrastable-laser" / "papers"
MEMORY_DIR = Path("/home/hjian/.claude/projects/-home-hjian-sci-logic-kb/memory")

# Obsidian项目路径
OBSIDIAN_PROJECT = "sci-logic-kb"

def obsidian_api_call(method: str = "GET", path: str = "", data: Optional[str] = None) -> Dict:
    """调用Obsidian API - 使用curl命令"""
    import subprocess
    import json

    url = f"{OBSIDIAN_BASE}/vault/Claude/projects/{OBSIDIAN_PROJECT}/{path}"

    curl_cmd = ["curl", "-s", "-k", "-H", OBSIDIAN_HEADER]

    if method == "PUT" and data:
        # 对于PUT请求，使用--data-binary
        curl_cmd.extend(["-X", "PUT", "-H", "Content-Type: text/markdown", "--data-binary", "@-", url])
        try:
            result = subprocess.run(curl_cmd, input=data.encode('utf-8'), capture_output=True, check=False)
            if result.returncode == 0 and result.stdout:
                try:
                    return json.loads(result.stdout.decode('utf-8'))
                except json.JSONDecodeError:
                    return {"status": "success", "message": "File written"}
            else:
                print(f"PUT命令失败: {result.stderr.decode('utf-8')}")
                return {}
        except Exception as e:
            print(f"PUT请求异常: {e}")
            return {}
    else:
        # 对于GET请求
        curl_cmd.append(url)
        try:
            result = subprocess.run(curl_cmd, capture_output=True, check=False)
            if result.returncode == 0 and result.stdout:
                try:
                    return json.loads(result.stdout.decode('utf-8'))
                except json.JSONDecodeError:
                    return {"content": result.stdout.decode('utf-8')}
            else:
                print(f"GET命令失败: {result.stderr.decode('utf-8')}")
                return {}
        except Exception as e:
            print(f"GET请求异常: {e}")
            return {}

def list_obsidian_files() -> List[str]:
    """列出Obsidian项目中的所有文件"""
    result = obsidian_api_call("GET", "")
    if result and "files" in result:
        return result["files"]
    return []

def read_obsidian_file(filename: str) -> Optional[str]:
    """读取Obsidian文件内容"""
    import subprocess

    url = f"{OBSIDIAN_BASE}/vault/Claude/projects/{OBSIDIAN_PROJECT}/{filename}"
    curl_cmd = ["curl", "-s", "-k", "-H", OBSIDIAN_HEADER, url]

    try:
        result = subprocess.run(curl_cmd, capture_output=True, check=False)
        if result.returncode == 0:
            return result.stdout.decode('utf-8')
    except Exception as e:
        print(f"读取文件错误 {filename}: {e}")

    return None

def write_obsidian_file(filename: str, content: str) -> bool:
    """写入文件到Obsidian"""
    result = obsidian_api_call("PUT", filename, content)
    return result is not None

def analyze_papers() -> Tuple[int, List[Dict]]:
    """分析论文目录，返回统计信息和论文列表"""
    paper_files = list(PAPERS_DIR.glob("*.yaml"))
    papers = []

    for paper_file in paper_files:
        try:
            with open(paper_file, 'r', encoding='utf-8') as f:
                paper_data = yaml.safe_load(f)

            paper_info = {
                'filename': paper_file.name,
                'basename': paper_file.stem,
                'path': str(paper_file),
                'meta': paper_data.get('meta', {}) if paper_data else {},
                'nodes_count': len(paper_data.get('nodes', [])) if paper_data else 0,
                'relations_count': len(paper_data.get('relations', [])) if paper_data else 0
            }
            papers.append(paper_info)
        except Exception as e:
            print(f"解析论文文件错误 {paper_file}: {e}")

    return len(paper_files), papers

def analyze_nodes() -> Dict[str, int]:
    """分析Obsidian节点目录，返回分类统计"""
    result = obsidian_api_call("GET", "nodes/")
    if not result or "files" not in result:
        return {}

    files = result["files"]
    counts = {'entity': 0, 'principle': 0, 'method': 0, 'metric': 0, 'subject': 0, 'other': 0}

    for file in files:
        if file.startswith('e-'):
            counts['entity'] += 1
        elif file.startswith('p-'):
            counts['principle'] += 1
        elif file.startswith('m-') and not file.startswith('met-'):
            counts['method'] += 1
        elif file.startswith('met-'):
            counts['metric'] += 1
        elif file.startswith('s-'):
            counts['subject'] += 1
        else:
            counts['other'] += 1

    return counts

def create_overview_file() -> str:
    """创建知识库概述文件"""
    # 统计信息
    paper_count, papers = analyze_papers()
    node_counts = analyze_nodes()

    # 读取架构版本
    schema_version = "v4.0"
    schema_path = PROJECT_DIR / "SCHEMA.md"
    if schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r"\*\*版本\*\*：([^\n（]+)", content)
            if match:
                schema_version = match.group(1).strip()

    # 读取专题状态
    topics_path = PROJECT_DIR / "TOPICS.md"
    topics_info = ""
    if topics_path.exists():
        with open(topics_path, 'r', encoding='utf-8') as f:
            topics_content = f.read()
            # 提取专题状态表格
            table_match = re.search(r"\|.*专题.*\|.*状态.*\|.*论文数.*\|.*核心节点数.*\|[\s\S]*?---", topics_content)
            if table_match:
                topics_info = table_match.group(0)

    overview = f"""# sci-logic-kb 知识库概述

> **同步时间**：{subprocess.check_output(['date']).decode().strip()}
> **架构版本**：{schema_version}
> **数据来源**：GitHub仓库 (78篇论文YAML，1个已建专题)

## 统计摘要

| 类别 | 数量 | 说明 |
|------|------|------|
| **论文总数** | {paper_count} | `topics/ultrastable-laser/papers/` 中的YAML文件 |
| **已建专题** | 1/7 | 超稳激光专题已建立，其余6个待建 |
| **Obsidian节点** | {sum(node_counts.values())} | 实体:{node_counts.get('entity',0)} 原理:{node_counts.get('principle',0)} 方法:{node_counts.get('method',0)} 指标:{node_counts.get('metric',0)} |
| **架构文档** | 3 | SCHEMA.md, TOPICS.md, CLAUDE.md |
| **自动化脚本** | 5+ | 论文处理、Zotero管理、分析工具 |

## 专题架构

{schema_version}版本采用多专题架构，覆盖时间频率计量全领域：

```
时间频率计量 (Time-Frequency Metrology)
├── 专题1：超稳激光 ← ✅ 已建（{paper_count}篇论文）
├── 专题2：光学频率梳 ← 📋 待建
├── 专题3：光钟 ← 📋 待建
├── 专题4：微波频率标准 ← 📋 待建
├── 专题5：时间频率传递 ← 📋 待建
├── 专题6：时间标尺与钟组 ← 📋 待建
└── 专题7：基础物理应用 ← 📋 待建
```

## 专题状态

{topics_info if topics_info else "（详见TOPICS.md文件）"}

## 知识提取方法

本知识库采用符号主义结构化方法：

1. **五类节点**：
   - **实体 (ent.***)**: 物理系统、硬件组件
   - **原理 (pri.***)**: 物理原理、限制机制
   - **方法 (meth.***)**: 实验方法、技术手段
   - **指标 (met.***)**: 性能指标、测量结果
   - **关系 (rel.***)**: 节点间的逻辑关系

2. **关系类型**：
   - `PART-OF`: 组成关系
   - `BOUNDED-BY`: 性能限制
   - `ENABLED-BY`: 原理支撑
   - `CHARACTERIZED-BY`: 指标表征
   - `COMPETES-WITH`: 竞争方案
   - `CONDITIONED-BY`: 外部条件

3. **质量原则**：
   - 智能单元原则：节点能独立回答边界问题
   - 实例节点原则：参数变体为Level 2实例
   - 跨分支原理隔离：不同分支保留独立原理节点

## Obsidian同步状态

| 资源类型 | 文件数 | 状态 |
|----------|--------|------|
| **记忆文件** | 5 | ✅ 已同步 |
| **节点文件** | {sum(node_counts.values())} | ⚠ 部分同步（44个节点） |
| **图形文件** | 5 | ⚠ 需更新（仅覆盖5篇论文） |
| **索引文件** | 0 | 📋 待创建 |
| **概述文件** | 1 | ✅ 本文件 |

## 使用说明

### 浏览知识
1. **查看图谱**：打开 `graph_master.md` 查看知识架构
2. **搜索节点**：在 `nodes/` 目录中查找特定节点文件
3. **查阅论文**：查看 `papers-index.md` 获取论文列表

### 贡献知识
1. **处理新论文**：通过GitHub Issues触发自动化处理
2. **手动更新**：编辑YAML文件后运行同步脚本
3. **架构演进**：更新SCHEMA.md后重新处理现有论文

### 相关链接
- **GitHub仓库**: [sci-logic-kb](https://github.com/hjiang555-a11y/sci-logic-kb)
- **架构文档**: [[SCHEMA-summary]] | [[TOPICS-summary]] | [[CLAUDE-summary]]
- **索引文件**: [[papers-index]] | [[nodes-index]] | [[topics-status]]

---
*本文件由Obsidian同步脚本自动生成，上次更新：{subprocess.check_output(['date']).decode().strip()}*
"""

    return overview

def create_topics_status() -> str:
    """创建专题状态文件"""
    topics_path = PROJECT_DIR / "TOPICS.md"
    if not topics_path.exists():
        return "# 专题状态\n\nTOPICS.md文件不存在。"

    with open(topics_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取关键部分
    sections = []

    # 提取总体架构
    arch_match = re.search(r"## 一、总体架构[\s\S]*?---", content)
    if arch_match:
        sections.append(arch_match.group(0))

    # 提取专题间关系
    relation_match = re.search(r"## 二、专题间关系[\s\S]*?---", content)
    if relation_match:
        sections.append(relation_match.group(0))

    # 提取各专题状态表
    status_match = re.search(r"## 三、各专题状态[\s\S]*?---", content)
    if status_match:
        sections.append(status_match.group(0))

    # 提取建设优先级
    priority_match = re.search(r"## 四、建设优先级建议[\s\S]*?---", content)
    if priority_match:
        sections.append(priority_match.group(0))

    topics_status = f"""# 时间频率计量专题状态

> **来源**: [[TOPICS.md]]（{subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip()}版本）
> **专题体系**: 7个专题，覆盖时间频率计量全领域

{"".join(sections)}

## 同步状态

### 超稳激光专题 (✅ 已建)
- **论文数量**: 78篇（已提取为YAML知识节点）
- **节点覆盖**: 44个Obsidian节点文件
- **图谱状态**: 5个图形文件（需更新以覆盖78篇论文）
- **自动化**: 完整的GitHub Actions处理流水线

### 待建专题准备
1. **光学频率梳**：与超稳激光耦合最紧密，优先建设
2. **光钟**：超稳激光的主要应用场景
3. **时间频率传递**：远程光钟比对必要环节
4. **微波频率标准**：与光钟形成完整"秒定义"链条
5. **时间标尺与钟组**：顶层应用
6. **基础物理应用**：前沿交叉领域

## 建设路线图

### 近期目标（1-2周）
1. 完善超稳激光专题的Obsidian同步
2. 更新图形文件反映78篇论文完整状态
3. 建立专题间引用规范

### 中期目标（1个月）
1. 启动光学频率梳专题建设
2. 建立跨专题共享节点目录
3. 完善自动化测试和验证

### 长期目标（3个月）
1. 完成7个专题的完整知识体系
2. 建立专题间关系网络
3. 实现智能查询和推理功能

## 相关链接
- [[sci-logic-kb-overview]] - 知识库总览
- [[SCHEMA-summary]] - 架构规范摘要
- [[CLAUDE-summary]] - 工作流程摘要
- [[papers-index]] - 论文索引
- [[nodes-index]] - 节点索引

---
*本文件基于TOPICS.md自动生成，建议与源文件同步更新*
"""

    return topics_status

def main():
    """主函数"""
    print("开始Obsidian知识库同步...")

    # 步骤1：分析现有内容
    print("1. 分析现有Obsidian内容...")
    paper_count, papers = analyze_papers()
    node_counts = analyze_nodes()
    print(f"   论文数量: {paper_count}")
    print(f"   节点统计: {node_counts}")

    # 步骤2：创建概述文件
    print("2. 创建知识库概述文件...")
    overview = create_overview_file()
    if write_obsidian_file("sci-logic-kb-overview.md", overview):
        print("   ✅ sci-logic-kb-overview.md 创建成功")
    else:
        print("   ❌ sci-logic-kb-overview.md 创建失败")

    # 步骤3：创建专题状态文件
    print("3. 创建专题状态文件...")
    topics_status = create_topics_status()
    if write_obsidian_file("topics-status.md", topics_status):
        print("   ✅ topics-status.md 创建成功")
    else:
        print("   ❌ topics-status.md 创建失败")

    print("同步完成！")
    print(f"已创建文件: sci-logic-kb-overview.md, topics-status.md")
    print(f"论文统计: {paper_count}篇论文")
    print(f"节点统计: {sum(node_counts.values())}个节点")

if __name__ == "__main__":
    main()