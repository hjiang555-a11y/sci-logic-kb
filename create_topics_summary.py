#!/usr/bin/env python3
"""
创建TOPICS.md摘要文件
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

def extract_topics_summary() -> str:
    """提取TOPICS.md的关键摘要"""
    topics_path = Path("/home/hjian/sci-logic-kb/TOPICS.md")

    if not topics_path.exists():
        return "# TOPICS.md 摘要\n\nTOPICS.md文件不存在。"

    with open(topics_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取版本信息
    version_match = re.search(r"\*\*版本\*\*：([^\n（]+)", content)
    version = version_match.group(1).strip() if version_match else "未知"

    # 提取定位
    purpose_match = re.search(r"\*\*定位\*\*：([^\n]+)", content)
    purpose = purpose_match.group(1).strip() if purpose_match else ""

    # 提取总体架构
    architecture_match = re.search(r"## 一、总体架构[\s\S]*?---", content)
    architecture = architecture_match.group(0) if architecture_match else ""

    # 提取专题间关系
    relations_match = re.search(r"## 二、专题间关系[\s\S]*?---", content)
    relations = relations_match.group(0) if relations_match else ""

    # 提取各专题状态
    status_match = re.search(r"## 三、各专题状态[\s\S]*?---", content)
    status = status_match.group(0) if status_match else ""

    # 提取建设优先级建议
    priority_match = re.search(r"## 四、建设优先级建议[\s\S]*?---", content)
    priority = priority_match.group(0) if priority_match else ""

    # 生成摘要
    summary = f"""# TOPICS.md 专题体系摘要

> **来源**: [[TOPICS.md]]（{version}版本）
> **提取时间**: {subprocess.check_output(['date']).decode().strip()}
> **定位**: {purpose}
> **专题体系**: 7个专题，覆盖时间频率计量全领域

## 总体架构

{architecture[:1500] + "..." if len(architecture) > 1500 else architecture}

## 专题间关系

{relations[:1500] + "..." if len(relations) > 1500 else relations}

## 各专题状态

{status[:1000] + "..." if len(status) > 1000 else status}

## 建设优先级

{priority[:2000] + "..." if len(priority) > 2000 else priority}

## 快速参考

### 7个专题概览
1. **超稳激光** (Ultra-stable Lasers) - ✅ 已建
   - 目录: `topics/ultrastable-laser/`
   - 论文数: 78篇
   - 核心节点: ~200+

2. **光学频率梳** (Optical Frequency Combs) - 📋 待建
   - 目录: `topics/optical-frequency-combs/`
   - 与超稳激光耦合最紧密，优先建设

3. **光钟** (Optical Clocks) - 📋 待建
   - 目录: `topics/optical-clocks/`
   - 超稳激光的主要应用场景

4. **微波频率标准** (Microwave Frequency Standards) - 📋 待建
   - 目录: `topics/microwave-standards/`
   - 与光钟形成完整"秒定义"链条

5. **时间频率传递** (Time & Frequency Transfer) - 📋 待建
   - 目录: `topics/time-frequency-transfer/`
   - 远程光钟比对必要环节

6. **时间标尺与钟组** (Timescales & Clock Ensembles) - 📋 待建
   - 目录: `topics/timescales/`
   - 顶层应用

7. **基础物理应用** (Fundamental Physics Applications) - 📋 待建
   - 目录: `topics/fundamental-physics/`
   - 前沿交叉领域

### 关键接口关系
- **超稳激光 → 光钟**: 询问激光稳定性决定钟性能
- **超稳激光 + 光学频率梳 → 光钟比对**: 梳齿锁定质量影响比对精度
- **超稳激光 → 时间频率传递**: 相干光源为远程比对提供基础
- **光学频率梳 → 微波标准**: 光-微波分频链接SI秒定义

## 建设路线图建议

### 近期（1-2周）
1. 完善超稳激光专题的Obsidian同步
2. 更新图形文件反映78篇论文完整状态
3. 建立专题间引用规范

### 中期（1个月）
1. 启动光学频率梳专题建设
2. 建立跨专题共享节点目录
3. 完善自动化测试和验证

### 长期（3个月）
1. 完成7个专题的完整知识体系
2. 建立专题间关系网络
3. 实现智能查询和推理功能

## 相关链接
- [[sci-logic-kb-overview]] - 知识库总览
- [[SCHEMA-summary]] - 架构规范摘要
- [[CLAUDE-summary]] - 工作流程摘要
- [[papers-index]] - 论文索引
- [[nodes-index]] - 节点索引
- [[topics-status]] - 详细专题状态

---
*本摘要由自动化脚本生成，基于TOPICS.md版本：{version}*
*建议与TOPICS.md源文件同步更新*
"""

    return summary

def main():
    """主函数"""
    print("开始创建TOPICS摘要...")

    content = extract_topics_summary()

    if write_obsidian_file("TOPICS-summary.md", content):
        print("✅ TOPICS-summary.md 创建成功")
    else:
        print("❌ TOPICS-summary.md 创建失败")

if __name__ == "__main__":
    main()