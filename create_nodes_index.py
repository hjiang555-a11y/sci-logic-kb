#!/usr/bin/env python3
"""
创建节点索引文件
"""

import os
import json
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

def read_obsidian_file(filename: str) -> str:
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

    return ""

def get_nodes_list() -> List[str]:
    """获取所有节点文件列表"""
    import subprocess

    url = f"{OBSIDIAN_BASE}/vault/Claude/projects/{OBSIDIAN_PROJECT}/nodes/"
    curl_cmd = ["curl", "-s", "-k", "-H", OBSIDIAN_HEADER, url]

    try:
        result = subprocess.run(curl_cmd, capture_output=True, check=False)
        if result.returncode == 0:
            data = json.loads(result.stdout.decode('utf-8'))
            return data.get('files', [])
    except Exception as e:
        print(f"获取节点列表错误: {e}")

    return []

def analyze_node_file(filename: str) -> Dict[str, Any]:
    """分析单个节点文件"""
    content = read_obsidian_file(f"nodes/{filename}")

    if not content:
        return {"name": filename, "error": "无法读取文件"}

    # 解析frontmatter
    frontmatter_match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
    node_type = "unknown"
    node_label = ""

    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        type_match = re.search(r'type:\s*(.+)', frontmatter)
        label_match = re.search(r'label:\s*"([^"]+)"', frontmatter)

        if type_match:
            node_type = type_match.group(1).strip()
        if label_match:
            node_label = label_match.group(1).strip()

    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename.replace('.md', '').replace('-', ' ').title()

    # 提取描述（第一段）
    description = ""
    lines = content.split('\n')
    in_frontmatter = False
    after_frontmatter = False

    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                after_frontmatter = True
                continue

        if after_frontmatter and line.strip() and not line.startswith('#') and not line.startswith('[') and not line.startswith('|'):
            description = line.strip()
            if len(description) > 100:
                description = description[:97] + "..."
            break

    # 提取链接
    links = re.findall(r'\[\[([^\]]+)\]\]', content)
    backlinks = links if links else []

    # 确定节点类型前缀
    type_prefix = "unknown"
    type_name = "未知"

    if filename.startswith('e-'):
        type_prefix = "entity"
        type_name = "实体"
    elif filename.startswith('p-'):
        type_prefix = "principle"
        type_name = "原理"
    elif filename.startswith('m-') and not filename.startswith('met-'):
        type_prefix = "method"
        type_name = "方法"
    elif filename.startswith('met-'):
        type_prefix = "metric"
        type_name = "指标"
    elif filename.startswith('s-'):
        type_prefix = "subject"
        type_name = "专题"

    return {
        "filename": filename,
        "basename": filename.replace('.md', ''),
        "type_prefix": type_prefix,
        "type_name": type_name,
        "node_type": node_type,
        "node_label": node_label,
        "title": title,
        "description": description,
        "backlinks_count": len(backlinks),
        "backlinks": backlinks[:5]  # 前5个链接
    }

def create_nodes_index() -> str:
    """创建节点索引文件"""
    print("获取节点列表...")
    node_files = get_nodes_list()

    if not node_files:
        return "# 节点索引\n\n暂无节点文件。"

    print(f"分析 {len(node_files)} 个节点文件...")
    nodes_info = []

    for i, filename in enumerate(node_files):
        if i % 10 == 0:
            print(f"  处理第 {i}/{len(node_files)} 个节点...")

        info = analyze_node_file(filename)
        nodes_info.append(info)

    # 按类型分组
    nodes_by_type = {}
    for node in nodes_info:
        type_name = node["type_name"]
        if type_name not in nodes_by_type:
            nodes_by_type[type_name] = []
        nodes_by_type[type_name].append(node)

    # 生成Markdown内容
    content = f"""# Obsidian 节点索引

> **统计时间**: {subprocess.check_output(['date']).decode().strip()}
> **节点总数**: {len(nodes_info)} 个
> **目录**: `nodes/`

## 节点分类统计

| 类型 | 数量 | 说明 |
|------|------|------|
"""

    for type_name in sorted(nodes_by_type.keys()):
        count = len(nodes_by_type[type_name])
        example = nodes_by_type[type_name][0]["filename"] if count > 0 else ""
        content += f"| **{type_name}** | {count} | 例: `{example}` |\n"

    content += f"| **总计** | **{len(nodes_info)}** | 全部节点文件 |\n"

    content += """

## 按类型索引

"""

    # 为每种类型创建详细列表
    for type_name in sorted(nodes_by_type.keys()):
        type_nodes = nodes_by_type[type_name]
        type_nodes.sort(key=lambda x: x["filename"])

        content += f"### {type_name} ({len(type_nodes)}个)\n\n"

        for node in type_nodes:
            filename = node["filename"]
            basename = filename.replace('.md', '')
            title = node["title"]
            description = node["description"]
            backlinks_count = node["backlinks_count"]

            content += f"#### [[{basename}]]\n\n"
            content += f"- **文件**: `{filename}`\n"
            content += f"- **标题**: {title}\n"
            if description:
                content += f"- **描述**: {description}\n"
            if backlinks_count > 0:
                content += f"- **链接数**: {backlinks_count} 个内部链接\n"

            # 显示部分链接
            backlinks = node.get("backlinks", [])
            if backlinks:
                content += f"- **相关链接**: "
                content += ", ".join(f"[[{link}]]" for link in backlinks[:3])
                if backlinks_count > 3:
                    content += f" 等 {backlinks_count} 个链接"
                content += "\n"

            content += "\n"

    content += f"""
## 节点文件命名规范

Obsidian节点文件使用前缀标识类型：

| 前缀 | 类型 | 示例 | 对应YAML ID |
|------|------|------|------------|
| `e-` | 实体 (Entity) | `e-fp-cavity.md` | `ent.fp_cavity_system` |
| `p-` | 原理 (Principle) | `p-brownian-thermal-noise.md` | `pri.brownian_thermal_noise_fdt` |
| `m-` | 方法 (Method) | `m-pdh-locking.md` | `meth.pdh_locking` |
| `met-` | 指标 (Metric) | `met-linewidth.md` | `met.laser_linewidth` |
| `s-` | 专题 (Subject) | `s-drever1983.md` | 论文知识文件 |

## 使用说明

### 浏览节点
1. **按类型浏览**: 使用上方分类索引
2. **搜索节点**: 在Obsidian中搜索关键词
3. **查看关系**: 点击节点文件查看内部链接

### 节点与知识库对应关系
- **Obsidian节点**: `nodes/` 目录中的Markdown文件
- **YAML源节点**: `topics/ultrastable-laser/papers/*.yaml` 中的节点定义
- **对应规则**: 文件名前缀对应YAML节点类型，名称转换为连字符格式

### 重要节点参考

#### 核心实体节点
- [[e-fp-cavity]] - F-P参考腔（所有腔锁频方案共同核心器件）
- [[e-fiber-interferometer]] - 光纤干涉仪（可捷变替代方案）
- [[e-mirror-substrate]] - 腔镜基底（84%热噪声贡献）
- [[e-mirror-coating]] - 腔镜镀层（15%热噪声贡献）

#### 核心原理节点
- [[p-brownian-thermal-noise]] - 布朗热噪声（涨落耗散定理）
- [[p-pdh-heterodyne]] - PDH射频边带光学外差探测原理
- [[p-shot-noise]] - 散粒噪声频率稳定度极限
- [[p-gouy-phase]] - Gouy相位横模鉴别原理（Tilt Locking基础）

#### 核心方法节点
- [[m-pdh-locking]] - PDH锁频方法（超稳激光标准误差探测手段）
- [[m-tilt-locking]] - Tilt Locking（倾斜锁定）方法
- [[m-fiber-delay-locking]] - 光纤延迟线锁频方法

## 相关链接
- [[sci-logic-kb-overview]] - 知识库总览
- [[papers-index]] - 论文索引
- [[topics-status]] - 专题状态
- [[graph_master]] - 主知识图谱

---
*本索引由自动化脚本生成，上次更新: {subprocess.check_output(['date']).decode().strip()}*
"""

    return content

def main():
    """主函数"""
    print("开始创建节点索引...")

    content = create_nodes_index()

    if write_obsidian_file("nodes-index.md", content):
        print("✅ nodes-index.md 创建成功")
    else:
        print("❌ nodes-index.md 创建失败")

if __name__ == "__main__":
    main()