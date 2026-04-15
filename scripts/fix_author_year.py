#!/usr/bin/env python3
"""
批量修复GitHub Issues中的Author Year格式问题

将"Author Year"字段值中的空格替换为下划线，确保与工作流兼容。
"""

import subprocess
import json
import re
import time

def get_issue_body(issue_number: int) -> dict:
    """获取Issue的当前标题和正文"""
    cmd = ["gh", "issue", "view", str(issue_number), "--json", "body,title"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"获取Issue #{issue_number}失败: {result.stderr}")
        return None
    return json.loads(result.stdout)

def update_issue(issue_number: int, new_body: str, new_title: str = None):
    """更新Issue的正文和标题"""
    cmd = ["gh", "issue", "edit", str(issue_number), "--body", new_body]
    if new_title:
        cmd.extend(["--title", new_title])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 更新Issue #{issue_number}")
    else:
        print(f"❌ 更新Issue #{issue_number}失败: {result.stderr}")

def fix_author_year_format(text: str) -> str:
    """将Author Year字段值中的空格替换为下划线"""
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        # 匹配 "**Author Year**: Belardi 201x" 格式
        if line.strip().startswith("**Author Year**:") or line.strip().startswith("**Author Year**:"):
            # 提取冒号后的部分
            parts = line.split(":", 1)
            if len(parts) == 2:
                label = parts[0]
                value = parts[1].strip()
                # 替换空格为下划线（多个连续空格替换为单个下划线）
                new_value = re.sub(r'\s+', '_', value)
                line = f"{label}: {new_value}"
                print(f"   转换: '{value}' -> '{new_value}'")
        new_lines.append(line)
    return '\n'.join(new_lines)

def fix_title_format(title: str) -> str:
    """修复标题中的Author Year格式（如果存在）"""
    # 标题格式为 "Process: Belardi 201x"
    if title.startswith("Process: "):
        prefix = "Process: "
        value = title[len(prefix):]
        new_value = re.sub(r'\s+', '_', value)
        if new_value != value:
            print(f"   标题转换: '{value}' -> '{new_value}'")
            return prefix + new_value
    return title

def main():
    # 修复Issues #70-#79
    start_issue = 70
    end_issue = 79

    print(f"批量修复Issues #{start_issue}-#{end_issue}中的Author Year格式")
    print("=" * 60)

    for issue_num in range(start_issue, end_issue + 1):
        print(f"\n处理Issue #{issue_num}...")

        # 获取当前Issue数据
        data = get_issue_body(issue_num)
        if not data:
            continue

        old_body = data.get("body", "")
        old_title = data.get("title", "")

        # 修复正文
        new_body = fix_author_year_format(old_body)
        new_title = fix_title_format(old_title)

        # 检查是否有变化
        if new_body == old_body and new_title == old_title:
            print(f"  无需更改")
            continue

        # 更新Issue
        update_issue(issue_num, new_body, new_title if new_title != old_title else None)

        # 避免API速率限制，添加短暂延迟
        time.sleep(1)

    print("\n" + "=" * 60)
    print("批量修复完成")

if __name__ == "__main__":
    main()