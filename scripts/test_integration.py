#!/usr/bin/env python3
"""
Zotero-Obsidian集成测试脚本
测试API连接性和基本工作流
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def load_env():
    """加载环境变量"""
    env_path = project_root / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
    
    # 默认配置（从现有脚本继承）
    config = {
        "zotero_user_id": os.getenv("ZOTERO_USER_ID", "19944378"),
        "zotero_host": os.getenv("ZOTERO_API_HOST", "172.20.96.1"),
        "zotero_port": os.getenv("ZOTERO_API_PORT", "23119"),
        "obsidian_host": os.getenv("OBSIDIAN_API_HOST", "172.20.96.1"),
        "obsidian_port": os.getenv("OBSIDIAN_API_PORT", "27124"),
        "obsidian_token": os.getenv("OBSIDIAN_API_TOKEN", ""),
    }
    return config

def test_zotero_api(config: Dict[str, Any]) -> bool:
    """测试Zotero API连接"""
    url = f"http://{config['zotero_host']}:{config['zotero_port']}/api/users/{config['zotero_user_id']}/items?limit=1"
    headers = {"Host": "127.0.0.1:23119"}
    
    print(f"测试Zotero API: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                item = data[0]
                print(f"  ✅ 成功! 获取到论文: {item.get('key', '未知')}")
                print(f"     标题: {item.get('data', {}).get('title', '未知')[:50]}...")
                return True
            else:
                print(f"  ⚠️  成功但无数据")
                return True
        else:
            print(f"  ❌ 失败: HTTP {response.status_code}")
            print(f"     响应: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False

def test_obsidian_api(config: Dict[str, Any]) -> bool:
    """测试Obsidian API连接"""
    url = f"https://{config['obsidian_host']}:{config['obsidian_port']}/vault/"
    headers = {}
    
    if config['obsidian_token']:
        headers["Authorization"] = f"Bearer {config['obsidian_token']}"
    
    print(f"测试Obsidian API: {url}")
    
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            print(f"  ✅ 成功! Obsidian API可访问")
            return True
        elif response.status_code == 401:
            print(f"  ⚠️  需要认证 (401 Unauthorized)")
            print(f"     说明: API已启用但需要有效的token")
            if not config['obsidian_token']:
                print(f"     提示: 请设置OBSIDIAN_API_TOKEN环境变量")
            return True  # 仍算连接成功，只是需要认证
        else:
            print(f"  ❌ 失败: HTTP {response.status_code}")
            print(f"     响应: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False

def test_pdf_access(config: Dict[str, Any]) -> bool:
    """测试PDF文件访问（通过Zotero存储路径）"""
    # 测试路径：Zotero在Windows中的存储路径
    test_paths = [
        "/mnt/d/Users/hjian/Zotero/storage/",
        "/mnt/c/Users/hjian/Zotero/storage/",
    ]
    
    print("测试Zotero PDF存储路径...")
    
    for path in test_paths:
        storage_path = Path(path)
        if storage_path.exists():
            print(f"  ✅ 找到Zotero存储目录: {path}")
            
            # 列出前3个目录（如果有）
            subdirs = list(storage_path.iterdir())[:3]
            if subdirs:
                print(f"     示例目录: {', '.join([d.name for d in subdirs[:2]])}")
                return True
        else:
            print(f"  ❌ 路径不存在: {path}")
    
    print("  ⚠️  未找到Zotero存储目录")
    print("     提示: Zotero可能安装在其它位置")
    return False

def test_sci_logic_kb_structure() -> bool:
    """测试sci-logic-kb目录结构"""
    required_paths = [
        project_root / "SCHEMA.md",
        project_root / "topics",
        project_root / "scripts",
    ]
    
    print("测试sci-logic-kb结构...")
    
    all_exist = True
    for path in required_paths:
        if path.exists():
            print(f"  ✅ {path.name}: 存在")
        else:
            print(f"  ❌ {path.name}: 不存在")
            all_exist = False
    
    # 检查topics目录内容
    topics_dir = project_root / "topics"
    if topics_dir.exists():
        topics = list(topics_dir.iterdir())
        print(f"     专题目录: {', '.join([t.name for t in topics if t.is_dir()][:3])}")
    
    return all_exist

def create_sample_config() -> None:
    """创建示例配置文件"""
    env_example = """# Zotero-Obsidian智能集成配置
# 复制此文件为 .env 并填入实际值

# Zotero配置
ZOTERO_USER_ID=19944378
ZOTERO_API_HOST=172.20.96.1
ZOTERO_API_PORT=23119

# Obsidian配置 (需要Local REST API插件)
OBSIDIAN_API_HOST=172.20.96.1
OBSIDIAN_API_PORT=27124
OBSIDIAN_API_TOKEN=your_obsidian_token_here
# 获取token: Obsidian设置 → Community plugins → Local REST API → API Token

# AI配置 (可选，用于智能提取)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# 路径配置
SCI_LOGIC_KB_PATH=/home/hjian/sci-logic-kb/sci-logic-kb
PDF_STORAGE_PATH=/home/hjian/sci-logic-kb/sci-logic-kb/pdfs
LITERATURE_NOTES_PATH=LiteratureNotes
"""
    
    env_path = project_root / ".env.example"
    if not env_path.exists():
        env_path.write_text(env_example)
        print(f"\n已创建示例配置文件: {env_path}")
        print("请复制为 .env 并填入实际值")

def main():
    """主测试函数"""
    print("=" * 60)
    print("Zotero-Obsidian-sci-logic-kb 集成环境测试")
    print("=" * 60)
    
    # 加载配置
    config = load_env()
    
    # 运行测试
    tests = [
        ("Zotero API连接", lambda: test_zotero_api(config)),
        ("Obsidian API连接", lambda: test_obsidian_api(config)),
        ("PDF存储路径", lambda: test_pdf_access(config)),
        ("sci-logic-kb结构", test_sci_logic_kb_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        result = test_func()
        results.append((test_name, result))
    
    # 显示总结
    print("\n" + "=" * 60)
    print("测试总结:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name:25} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！环境已就绪。")
        print("下一步: 运行 python scripts/batch_process_zotero.py --batch-size=1")
    else:
        print("⚠️  部分测试失败，需要修复配置。")
        print("建议步骤:")
        print("  1. 检查Zotero是否运行且启用了API")
        print("  2. 检查Obsidian Local REST API插件是否启用")
        print("  3. 确认Zotero存储路径是否正确")
        print("  4. 创建 .env 文件配置API密钥")
    
    # 创建示例配置文件（如果不存在）
    create_sample_config()
    
    print("\n详细文档请参考:")
    print("  - ZOTERO_OBSIDIAN_AI_INTEGRATION.md (智能集成方案)")
    print("  - ZOTERO_OBSIDIAN_INTEGRATION_PLAN.md (基础集成方案)")

if __name__ == "__main__":
    main()