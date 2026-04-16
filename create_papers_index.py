#!/usr/bin/env python3
"""
创建论文索引文件
"""

import os
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any
import subprocess

# Obsidian API配置
WINDOWS_IP = "172.20.96.1"
OBSIDIAN_KEY = "f65c3bdf4c4ed108c4046114184fba8b352449dab516d662cc95bce1eb6585a2"
OBSIDIAN_BASE = f"https://{WINDOWS_IP}:27124"
OBSIDIAN_HEADER = f"Authorization: Bearer {OBSIDIAN_KEY}"
OBSIDIAN_PROJECT = "sci-logic-kb"

# 项目路径
PROJECT_DIR = Path("/home/hjian/sci-logic-kb")
PAPERS_DIR = PROJECT_DIR / "topics" / "ultrastable-laser" / "papers"

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

def analyze_paper_yaml(paper_file: Path) -> Dict[str, Any]:
    """分析单个论文YAML文件"""
    try:
        with open(paper_file, 'r', encoding='utf-8') as f:
            paper_data = yaml.safe_load(f)

        if not paper_data:
            return {"error": "空文件"}

        meta = paper_data.get('meta', {})

        # 提取基本信息
        info = {
            'filename': paper_file.name,
            'basename': paper_file.stem,  # 如 drever1983
            'title': meta.get('title', ''),
            'year': meta.get('year', ''),
            'first_author': meta.get('first_author', ''),
            'journal': meta.get('journal', ''),
            'doi': meta.get('doi', ''),
            'zotero_key': meta.get('zotero_key', ''),
            'reliability': meta.get('reliability', ''),
            'note': meta.get('note', ''),
            'source_type': meta.get('source_type', ''),
            # 统计
            'entities_count': len(paper_data.get('entities', [])),
            'principles_count': len(paper_data.get('principles', [])),
            'methods_count': len(paper_data.get('methods', [])),
            'metrics_count': len(paper_data.get('metrics', [])),
            'relations_count': len(paper_data.get('relations', []))
        }

        # 从note中提取核心贡献摘要
        note = meta.get('note', '')
        if note:
            # 提取第一句或前100字符
            lines = note.split('\n')
            first_line = lines[0].strip()
            if len(first_line) > 150:
                first_line = first_line[:147] + "..."
            info['summary'] = first_line
        else:
            info['summary'] = ""

        return info

    except Exception as e:
        print(f"解析论文文件错误 {paper_file}: {e}")
        return {"error": str(e), 'filename': paper_file.name}

def create_papers_index() -> str:
    """创建论文索引文件"""
    paper_files = list(PAPERS_DIR.glob("*.yaml"))
    paper_files.sort(key=lambda x: x.stem)  # 按文件名排序

    papers_info = []
    error_count = 0

    print(f"分析 {len(paper_files)} 篇论文...")
    for i, paper_file in enumerate(paper_files):
        if i % 10 == 0:
            print(f"  处理第 {i}/{len(paper_files)} 篇...")

        info = analyze_paper_yaml(paper_file)
        if "error" not in info:
            papers_info.append(info)
        else:
            error_count += 1

    # 按年份排序
    papers_info.sort(key=lambda x: (str(x.get('year', '')), x.get('first_author', '').lower()))

    # 生成Markdown内容
    content = f"""# 超稳激光专题论文索引

> **统计时间**: {subprocess.check_output(['date']).decode().strip()}
> **论文总数**: {len(papers_info)} 篇（{error_count} 篇解析错误）
> **专题路径**: `topics/ultrastable-laser/papers/`

## 论文列表

| 年份 | 作者 | 标题 | 期刊 | 节点统计 | 备注 |
|------|------|------|------|----------|------|
"""

    for paper in papers_info:
        year = paper.get('year', '')
        author = paper.get('first_author', '')
        title = paper.get('title', '')
        if len(title) > 60:
            title = title[:57] + "..."

        journal = paper.get('journal', '')
        if len(journal) > 30:
            journal = journal[:27] + "..."

        # 节点统计
        nodes_stats = f"E:{paper.get('entities_count',0)} P:{paper.get('principles_count',0)} M:{paper.get('methods_count',0)} Met:{paper.get('metrics_count',0)} R:{paper.get('relations_count',0)}"

        # 备注（核心贡献摘要）
        summary = paper.get('summary', '')
        if len(summary) > 40:
            summary = summary[:37] + "..."

        content += f"| {year} | {author} | {title} | {journal} | {nodes_stats} | {summary} |\n"

    content += """

## 详细文件信息

"""

    # 按文件名分组详细列表
    for paper in papers_info:
        basename = paper.get('basename', '')
        title = paper.get('title', '')
        year = paper.get('year', '')
        first_author = paper.get('first_author', '')
        journal = paper.get('journal', '')
        doi = paper.get('doi', '')
        zotero_key = paper.get('zotero_key', '')

        content += f"### {first_author} {year} (`{basename}.yaml`)\n\n"
        content += f"- **标题**: {title}\n"
        if journal:
            content += f"- **期刊**: {journal}\n"
        if doi:
            content += f"- **DOI**: {doi}\n"
        if zotero_key:
            content += f"- **Zotero Key**: {zotero_key}\n"

        content += f"- **节点统计**: "
        content += f"实体({paper.get('entities_count',0)}) "
        content += f"原理({paper.get('principles_count',0)}) "
        content += f"方法({paper.get('methods_count',0)}) "
        content += f"指标({paper.get('metrics_count',0)}) "
        content += f"关系({paper.get('relations_count',0)})\n"

        summary = paper.get('summary', '')
        if summary:
            content += f"- **核心贡献**: {summary}\n"

        content += f"- **文件**: `topics/ultrastable-laser/papers/{basename}.yaml`\n\n"

    content += f"""
## 统计摘要

### 节点总数
- **实体节点**: {sum(p.get('entities_count', 0) for p in papers_info)}
- **原理节点**: {sum(p.get('principles_count', 0) for p in papers_info)}
- **方法节点**: {sum(p.get('methods_count', 0) for p in papers_info)}
- **指标节点**: {sum(p.get('metrics_count', 0) for p in papers_info)}
- **关系**: {sum(p.get('relations_count', 0) for p in papers_info)}

### 按年份分布
"""

    # 年份分布
    year_counts = {}
    for paper in papers_info:
        year = paper.get('year', '未知')
        year_counts[year] = year_counts.get(year, 0) + 1

    for year in sorted(year_counts.keys()):
        count = year_counts[year]
        content += f"- **{year}**: {count} 篇论文\n"

    content += f"""
## 使用说明

### 查找论文
1. **按年份查找**: 使用上方表格按年份排序
2. **按作者查找**: 搜索作者姓氏
3. **按内容查找**: 搜索标题关键词

### 访问论文知识
1. **YAML源文件**: `topics/ultrastable-laser/papers/{basename}.yaml`
2. **Obsidian节点**: 相关节点在 `nodes/` 目录中
3. **知识图谱**: 查看 `graph_master.md` 了解架构

### 相关链接
- [[sci-logic-kb-overview]] - 知识库总览
- [[topics-status]] - 专题状态
- [[nodes-index]] - 节点索引
- [[SCHEMA-summary]] - 架构规范

---
*本索引由自动化脚本生成，上次更新: {subprocess.check_output(['date']).decode().strip()}*
"""

    return content

def main():
    """主函数"""
    print("开始创建论文索引...")

    content = create_papers_index()

    if write_obsidian_file("papers-index.md", content):
        print("✅ papers-index.md 创建成功")

        # 显示统计信息
        paper_files = list(PAPERS_DIR.glob("*.yaml"))
        print(f"   处理论文: {len(paper_files)} 篇")
    else:
        print("❌ papers-index.md 创建失败")

if __name__ == "__main__":
    main()