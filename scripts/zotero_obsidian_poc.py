#!/usr/bin/env python3
"""
Zotero-Obsidian集成概念验证
从Zotero获取单篇论文，在Obsidian中创建文献笔记
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

class ZoteroObsidianIntegration:
    def __init__(self):
        # Zotero配置
        self.zotero_user_id = os.getenv("ZOTERO_USER_ID", "19944378")
        self.zotero_host = os.getenv("ZOTERO_API_HOST", "172.20.96.1")
        self.zotero_port = os.getenv("ZOTERO_API_PORT", "23119")
        
        # Obsidian配置
        self.obsidian_host = os.getenv("OBSIDIAN_API_HOST", "172.20.96.1")
        self.obsidian_port = os.getenv("OBSIDIAN_API_PORT", "27124")
        self.obsidian_token = os.getenv("OBSIDIAN_API_TOKEN", "")
        
        # 路径配置
        self.literature_notes_path = "LiteratureNotes"
        
        # 禁用SSL警告（本地开发）
        requests.packages.urllib3.disable_warnings()
    
    def get_zotero_item(self, item_key: str) -> Optional[Dict[str, Any]]:
        """从Zotero获取单篇论文信息"""
        url = f"http://{self.zotero_host}:{self.zotero_port}/api/users/{self.zotero_user_id}/items/{item_key}"
        headers = {"Host": "127.0.0.1:23119"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Zotero API错误: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"获取Zotero数据异常: {e}")
            return None
    
    def get_zotero_attachment(self, item_key: str) -> Optional[Dict[str, Any]]:
        """获取论文的附件信息（如PDF）"""
        url = f"http://{self.zotero_host}:{self.zotero_port}/api/users/{self.zotero_user_id}/items/{item_key}/children"
        headers = {"Host": "127.0.0.1:23119"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    data = item.get('data', {})
                    if data.get('itemType') == 'attachment':
                        return item
            return None
        except Exception as e:
            print(f"获取附件信息异常: {e}")
            return None
    
    def create_obsidian_note(self, zotero_item: Dict[str, Any]) -> bool:
        """在Obsidian中创建文献笔记"""
        # 提取论文信息
        data = zotero_item.get('data', {})
        meta = zotero_item.get('meta', {})
        
        zotero_key = data.get('key', '')
        title = data.get('title', 'Untitled')
        authors = meta.get('creatorSummary', 'Unknown')
        year = meta.get('parsedDate', '') or data.get('date', '').split('-')[0]
        abstract = data.get('abstractNote', '')
        doi = data.get('DOI', '')
        url = data.get('url', '')
        
        # 生成文件名（使用Zotero Key）
        filename = f"{zotero_key}.md"
        filepath = f"{self.literature_notes_path}/{filename}"
        
        # 获取当前日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 读取模板
        template_path = Path(__file__).parent / "templates" / "Zotero Literature Note.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        else:
            # 使用简化模板
            template_content = """---
zotero_key: "{{zotero_key}}"
title: "{{title}}"
authors: "{{authors}}"
year: {{year}}
doi: "{{doi}}"
url: "{{url}}"
tags:
  - literature-note
status: "unprocessed"
created: "{{date}}"
---

# {{title}}

**Authors:** {{authors}}  
**Year:** {{year}}  
**DOI:** {{doi}}  
**Zotero Key:** `{{zotero_key}}`  
**Status:** unprocessed

## Abstract
{{abstract}}

## 专家笔记
> 在此处添加您的分析、评论和见解

## 参考文献
```bibtex
{{citation}}
```

*此笔记由Zotero-Obsidian集成系统自动生成*"""
        
        # 替换模板变量
        content = template_content
        content = content.replace("{{zotero_key}}", zotero_key)
        content = content.replace("{{title}}", title)
        content = content.replace("{{authors}}", authors)
        content = content.replace("{{year}}", str(year))
        content = content.replace("{{doi}}", doi)
        content = content.replace("{{url}}", url)
        content = content.replace("{{abstract}}", abstract)
        content = content.replace("{{date}}", current_date)
        
        # 生成简单引用
        citation = f"@article{{{zotero_key},\n  title = {{{title}}},\n  author = {{{authors}}},\n  year = {{{year}}},\n  doi = {{{doi}}},\n  url = {{{url}}}\n}}"
        content = content.replace("{{citation}}", citation)
        
        # 创建Obsidian笔记
        url = f"https://{self.obsidian_host}:{self.obsidian_port}/vault/{filepath}"
        headers = {
            "Authorization": f"Bearer {self.obsidian_token}",
            "Content-Type": "text/markdown"
        }
        
        try:
            response = requests.put(url, headers=headers, data=content.encode('utf-8'), verify=False, timeout=30)
            if response.status_code == 200:
                print(f"✅ 成功创建笔记: {filepath}")
                print(f"   标题: {title}")
                print(f"   作者: {authors} ({year})")
                return True
            else:
                print(f"❌ 创建笔记失败: HTTP {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ 创建笔记异常: {e}")
            return False
    
    def test_connection(self):
        """测试所有连接"""
        print("测试Zotero-Obsidian连接...")
        
        # 测试Zotero连接
        test_key = "TRFV3Y5G"  # 已知存在的论文
        item = self.get_zotero_item(test_key)
        if item:
            print(f"✅ Zotero连接正常，获取到论文: {item.get('data', {}).get('title', '')[:50]}...")
        else:
            print("❌ Zotero连接失败")
            return False
        
        # 测试Obsidian连接
        url = f"https://{self.obsidian_host}:{self.obsidian_port}/vault/"
        headers = {"Authorization": f"Bearer {self.obsidian_token}"}
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            if response.status_code == 200:
                print("✅ Obsidian连接正常")
            else:
                print(f"❌ Obsidian连接失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Obsidian连接异常: {e}")
            return False
        
        return True
    
    def process_paper(self, zotero_key: str):
        """处理单篇论文"""
        print(f"\n处理论文: {zotero_key}")
        print("-" * 40)
        
        # 1. 从Zotero获取论文信息
        item = self.get_zotero_item(zotero_key)
        if not item:
            print("❌ 无法从Zotero获取论文信息")
            return False
        
        # 2. 在Obsidian中创建笔记
        success = self.create_obsidian_note(item)
        if success:
            print("✅ 论文处理完成")
        else:
            print("❌ 论文处理失败")
        
        return success

def main():
    """主函数"""
    integration = ZoteroObsidianIntegration()
    
    print("=" * 60)
    print("Zotero-Obsidian 自动关联测试")
    print("=" * 60)
    
    # 测试连接
    if not integration.test_connection():
        print("\n⚠️ 连接测试失败，请检查配置")
        return
    
    # 处理单篇论文（使用已知存在的论文）
    test_key = "TRFV3Y5G"  # Dissipative Kerr solitons论文
    integration.process_paper(test_key)
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 在Obsidian中打开 LiteratureNotes/TRFV3Y5G.md")
    print("2. 检查笔记内容是否正确")
    print("3. 手动添加知识库节点链接")
    print("\n扩展功能:")
    print("- 批量处理: 修改脚本处理多篇论文")
    print("- AI提取: 添加LLM分析PDF功能")
    print("- 知识库集成: 自动创建YAML节点")

if __name__ == "__main__":
    main()