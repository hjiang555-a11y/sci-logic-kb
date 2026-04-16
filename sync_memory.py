#!/usr/bin/env python3
"""
同步本地记忆文件到Obsidian
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

def sync_memory_files():
    """同步本地记忆文件到Obsidian"""
    memory_dir = Path("/home/hjian/.claude/projects/-home-hjian-sci-logic-kb/memory")

    if not memory_dir.exists():
        print("❌ 本地记忆目录不存在")
        return False

    # 列出所有记忆文件（不包括MEMORY.md）
    memory_files = list(memory_dir.glob("*.md"))
    memory_files = [f for f in memory_files if f.name != "MEMORY.md"]

    print(f"找到 {len(memory_files)} 个本地记忆文件")

    synced_count = 0
    for mem_file in memory_files:
        print(f"  处理: {mem_file.name}")

        # 读取本地文件内容
        try:
            with open(mem_file, 'r', encoding='utf-8') as f:
                local_content = f.read()
        except Exception as e:
            print(f"     ❌ 读取本地文件失败: {e}")
            continue

        # 检查Obsidian中是否有该文件
        obsidian_content = read_obsidian_file(mem_file.name)

        if obsidian_content and obsidian_content.strip() == local_content.strip():
            print(f"     ✅ 已同步（内容一致）")
        else:
            # 写入Obsidian
            if write_obsidian_file(mem_file.name, local_content):
                print(f"     ✅ 同步成功")
                synced_count += 1
            else:
                print(f"     ❌ 同步失败")

    # 同步MEMORY.md索引文件
    memory_index_path = memory_dir / "MEMORY.md"
    if memory_index_path.exists():
        print(f"处理索引文件: MEMORY.md")
        try:
            with open(memory_index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()

            # 写入Obsidian
            if write_obsidian_file("MEMORY.md", index_content):
                print(f"     ✅ MEMORY.md 同步成功")
            else:
                print(f"     ❌ MEMORY.md 同步失败")
        except Exception as e:
            print(f"     ❌ 处理MEMORY.md失败: {e}")

    return synced_count

def main():
    """主函数"""
    print("开始同步记忆文件到Obsidian...")

    synced = sync_memory_files()

    print(f"\n同步完成！")
    print(f"成功同步文件数: {synced}")

    # 列出Obsidian中的记忆文件进行验证
    print("\n验证Obsidian中的记忆文件...")
    WINDOWS_IP = "172.20.96.1"
    OBSIDIAN_KEY = "f65c3bdf4c4ed108c4046114184fba8b352449dab516d662cc95bce1eb6585a2"

    cmd = f'curl -s -k -H "Authorization: Bearer {OBSIDIAN_KEY}" "https://{WINDOWS_IP}:27124/vault/Claude/projects/{OBSIDIAN_PROJECT}/" | python3 -c "import sys, json; data=json.load(sys.stdin); files=[f for f in data.get(\"files\", []) if f.endswith(\".md\")]; print(f\"Obsidian中的Markdown文件: {len(files)}个\"); for f in sorted(files): print(f\"  - {f}\")"'

    try:
        subprocess.run(cmd, shell=True, check=False)
    except Exception as e:
        print(f"验证失败: {e}")

if __name__ == "__main__":
    main()