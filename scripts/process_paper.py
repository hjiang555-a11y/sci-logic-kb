#!/usr/bin/env python3
"""
处理单篇论文的脚本 - 用于GitHub Actions工作流

功能：
1. 读取环境变量：AUTHOR_YEAR, ZOTERO_KEY, PDF_FILENAME, TOPIC, TASK
2. 如果YAML文件已存在，确保有Schema版本行（v4.1），保留原有内容
3. 如果YAML文件不存在，生成基本模板
4. 不覆盖已有丰富内容的文件
"""

import os
import sys
import json
import re
from pathlib import Path

def load_environment():
    """加载环境变量"""
    env = {
        'author_year': os.environ.get('AUTHOR_YEAR', '').strip(),
        'zotero_key': os.environ.get('ZOTERO_KEY', '').strip(),
        'pdf_filename': os.environ.get('PDF_FILENAME', '').strip(),
        'topic': os.environ.get('TOPIC', 'ultrastable-laser').strip(),
        'task': os.environ.get('TASK', 'process').strip(),
        'github_token': os.environ.get('GITHUB_TOKEN', '').strip(),
    }
    
    if not env['author_year']:
        print("❌ 错误: AUTHOR_YEAR 环境变量未设置")
        sys.exit(1)
    
    print(f"📄 处理论文: {env['author_year']}")
    print(f"🔑 Zotero key: {env['zotero_key'] or '未提供'}")
    print(f"📁 Topic: {env['topic']}")
    print(f"🎯 Task: {env['task']}")
    
    return env

def ensure_schema_version(file_path, task):
    """确保YAML文件有Schema版本行"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # 检查是否已有Schema版本行
    schema_pattern = re.compile(r'^#\s*Schema版本\s*:\s*v\d+\.\d+')
    schema_line_index = -1
    for i, line in enumerate(lines):
        if schema_pattern.match(line.strip()):
            schema_line_index = i
            break
    
    # 确定目标Schema版本
    target_version = "v4.1"
    
    if schema_line_index >= 0:
        # 已有Schema版本行，检查是否需要更新
        current_line = lines[schema_line_index]
        current_version_match = re.search(r'v\d+\.\d+', current_line)
        if current_version_match:
            current_version = current_version_match.group(0)
            if current_version != target_version:
                print(f"🔄 更新Schema版本: {current_version} -> {target_version}")
                lines[schema_line_index] = f"# Schema版本：{target_version}"
            else:
                print(f"✅ Schema版本已是最新: {target_version}")
        return '\n'.join(lines)
    else:
        # 没有Schema版本行，添加在meta部分之后
        # 查找meta部分结束位置（entities:或principles:或#开头的注释之后）
        insert_index = -1
        for i, line in enumerate(lines):
            if line.startswith('entities:') or line.startswith('principles:') or line.startswith('methods:') or line.startswith('metrics:') or line.startswith('relations:'):
                insert_index = i
                break
        
        if insert_index == -1:
            # 如果没有找到，添加到文件末尾
            insert_index = len(lines)
        
        # 在插入位置添加空行和Schema版本行
        schema_line = f"# Schema版本：{target_version}"
        if insert_index > 0 and lines[insert_index-1].strip() != '':
            lines.insert(insert_index, '')
            insert_index += 1
        lines.insert(insert_index, schema_line)
        print(f"✅ 添加Schema版本行: {target_version}")
        
        return '\n'.join(lines)

def generate_basic_yaml(env):
    """生成基本YAML模板（仅当文件不存在时）"""
    author_year = env['author_year']
    topic = env['topic']
    
    yaml_lines = [
        "meta:",
        f"  zotero_key: {env['zotero_key'] or ''}",
        f"  topic: {topic}",
        "  source_type: journal",
        "  contribution_type: experimental",
        "  reliability: high",
        f"  title: \"论文 {author_year}\"",
        "  year: 2024",
        f"  first_author: {author_year.split('20')[0] if '20' in author_year else 'Author'}",
        "  journal: \"Journal\"",
        "  doi: \"\"",
        "  note: |",
        f"    [测试生成] 论文 {author_year} 的YAML文件，由GitHub Actions工作流自动生成。",
        "    需要人工检查并补充完整内容。",
        "",
        "# Schema版本：v4.1",
        "",
        "entities: []",
        "",
        "principles: []",
        "",
        "methods: []",
        "",
        "metrics: []",
        "",
        "relations: []",
    ]
    
    return '\n'.join(yaml_lines)

def main():
    """主函数"""
    env = load_environment()
    
    # 确定输出路径
    repo_root = Path(__file__).parent.parent
    output_dir = repo_root / "topics" / env['topic'] / "papers"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{env['author_year']}.yaml"
    
    # 检查文件是否存在
    if output_path.exists():
        print(f"📁 文件已存在: {output_path}")
        print("🔧 确保Schema版本正确...")
        
        # 获取文件大小判断内容是否丰富
        file_size = output_path.stat().st_size
        if file_size > 1000:
            print(f"📊 文件较大 ({file_size} 字节)，推测已有丰富内容，保留原有内容")
        
        # 确保Schema版本行存在
        new_content = ensure_schema_version(output_path, env['task'])
        
        # 写入更新后的内容
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 文件已更新: {output_path}")
        
        # 显示预览
        print("\n--- 更新后预览（前10行）---")
        lines = new_content.split('\n')[:10]
        for i, line in enumerate(lines, 1):
            print(f"{i:3}: {line}")
            
    else:
        print(f"📝 文件不存在，生成基本模板: {output_path}")
        yaml_content = generate_basic_yaml(env)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"✅ 新文件已创建: {output_path}")
        print("\n--- 生成内容预览（前15行）---")
        lines = yaml_content.split('\n')[:15]
        for i, line in enumerate(lines, 1):
            print(f"{i:3}: {line}")
    
    print("\n🎯 工作流状态:")
    print(f"- 任务: {env['task']}")
    print(f"- 论文: {env['author_year']}")
    print(f"- 主题: {env['topic']}")
    print(f"- 输出: {output_path}")
    print("\n📋 下一步: GitHub Actions将提交更改并创建PR")

if __name__ == "__main__":
    main()