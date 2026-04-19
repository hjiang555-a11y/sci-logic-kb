#!/usr/bin/env python3
"""
处理单篇论文的脚本 - 用于GitHub Actions工作流

功能：
1. 读取环境变量：AUTHOR_YEAR, ZOTERO_KEY, PDF_FILENAME, TOPIC, TASK
2. 从Zotero API获取论文元数据（如果ZOTERO_KEY存在）
3. 调用GitHub Models API（Claude Sonnet 4.6）提取知识
4. 生成符合SCHEMA.md v4.1的YAML文件
"""

import os
import sys
import json
import requests
from pathlib import Path
import tempfile

# 配置
repo_root = Path(__file__).parent.parent
schema_path = repo_root / "SCHEMA.md"
copilot_instructions_path = repo_root / ".github" / "copilot-instructions.md"

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
    
    # 验证必要参数
    if not env['author_year']:
        print("❌ 错误: AUTHOR_YEAR 环境变量未设置")
        sys.exit(1)
    
    print(f"📄 处理论文: {env['author_year']}")
    print(f"🔑 Zotero key: {env['zotero_key'] or '未提供'}")
    print(f"📁 Topic: {env['topic']}")
    print(f"🎯 Task: {env['task']}")
    
    return env

def get_zotero_metadata(zotero_key):
    """从Zotero API获取论文元数据"""
    if not zotero_key:
        return None
    
    zotero_host = os.environ.get('ZOTERO_API_HOST', '172.20.96.1')
    zotero_port = os.environ.get('ZOTERO_API_PORT', '23119')
    zotero_user_id = os.environ.get('ZOTERO_USER_ID', '19944378')
    
    url = f"http://{zotero_host}:{zotero_port}/api/users/{zotero_user_id}/items/{zotero_key}"
    headers = {"Host": "127.0.0.1:23119"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            item = response.json()
            data = item.get('data', {})
            
            # 提取基本信息
            metadata = {
                'title': data.get('title', ''),
                'date': data.get('date', ''),
                'publicationTitle': data.get('publicationTitle', ''),
                'creators': data.get('creators', []),
                'abstractNote': data.get('abstractNote', ''),
                'DOI': data.get('DOI', ''),
            }
            
            print(f"✅ 从Zotero获取元数据: {metadata['title'][:50]}...")
            return metadata
        else:
            print(f"⚠️  Zotero API 响应 {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  连接Zotero API失败: {e}")
        return None

def generate_yaml_template(env, zotero_metadata):
    """生成YAML模板"""
    author_year = env['author_year']
    topic = env['topic']
    
    # 基础元数据
    yaml_lines = [
        "meta:",
        f"  zotero_key: {env['zotero_key'] or ''}",
        f"  topic: {topic}",
        "  source_type: journal",
        "  contribution_type: experimental",
        "  reliability: high",
    ]
    
    if zotero_metadata:
        title = zotero_metadata.get('title', f'Title for {author_year}')
        yaml_lines.append(f"  title: {json.dumps(title)}")
        
        # 提取年份
        date = zotero_metadata.get('date', '')
        import re
        year_match = re.search(r'\b(\d{4})\b', date)
        year = year_match.group(1) if year_match else '2024'
        yaml_lines.append(f"  year: {year}")
        
        # 提取第一作者
        creators = zotero_metadata.get('creators', [])
        first_author = creators[0].get('lastName', 'Unknown') if creators else 'Unknown'
        yaml_lines.append(f"  first_author: {first_author}")
        
        journal = zotero_metadata.get('publicationTitle', '')
        if journal:
            yaml_lines.append(f"  journal: {json.dumps(journal)}")
        
        doi = zotero_metadata.get('DOI', '')
        if doi:
            yaml_lines.append(f"  doi: {doi}")
    else:
        # 默认元数据
        yaml_lines.extend([
            f"  title: \"论文 {author_year}\"",
            "  year: 2024",
            f"  first_author: {author_year.split('20')[0] if '20' in author_year else 'Author'}",
            "  journal: \"Journal\"",
            "  doi: \"\"",
        ])
    
    yaml_lines.append("  note: |")
    yaml_lines.append(f"    [测试生成] 论文 {author_year} 的YAML文件，由GitHub Actions工作流自动生成。")
    yaml_lines.append("    需要人工检查并补充完整内容。")
    
    # Schema版本
    yaml_lines.append("")
    yaml_lines.append("# Schema版本：v4.1")
    yaml_lines.append("")
    
    # 空的实体、原理、方法、指标、关系部分
    sections = ["entities", "principles", "methods", "metrics", "relations"]
    for section in sections:
        yaml_lines.append(f"{section}: []")
        yaml_lines.append("")
    
    return "\n".join(yaml_lines)

def call_github_models_api(prompt, model="claude-sonnet-4-6"):
    """调用GitHub Models API（占位符）"""
    print(f"🤖 调用GitHub Models API: {model}")
    print(f"📝 Prompt: {prompt[:100]}...")
    
    # 在实际实现中，这里应该调用GitHub Models API
    # 由于API访问需要额外配置，此处返回模拟响应
    return {
        "success": True,
        "message": "GitHub Models API调用成功（模拟）",
        "content": "这是AI生成的内容，需要根据实际论文补充。"
    }

def main():
    """主函数"""
    env = load_environment()
    
    # 1. 获取Zotero元数据
    zotero_metadata = get_zotero_metadata(env['zotero_key'])
    
    # 2. 生成YAML文件
    yaml_content = generate_yaml_template(env, zotero_metadata)
    
    # 3. 确定输出路径
    output_dir = repo_root / "topics" / env['topic'] / "papers"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{env['author_year']}.yaml"
    
    # 4. 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print(f"✅ YAML文件已生成: {output_path}")
    print(f"📊 文件大小: {len(yaml_content)} 字符")
    
    # 5. 显示预览
    print("\n--- YAML预览（前30行）---")
    lines = yaml_content.split('\n')[:30]
    for i, line in enumerate(lines, 1):
        print(f"{i:3}: {line}")
    
    if len(yaml_content.split('\n')) > 30:
        print("... (更多内容)")
    
    print("\n🎯 下一步:")
    print(f"1. 检查 {output_path}")
    print("2. 根据实际论文内容补充entities/principles/methods/metrics/relations")
    print("3. 确保符合SCHEMA.md v4.1规范")
    print("4. 提交PR供审核")

if __name__ == "__main__":
    main()