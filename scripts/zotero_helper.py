#!/usr/bin/env python3
"""
Zotero辅助工具：帮助未来导入论文时自动关联

功能：
1. 搜索Zotero论文（按标题、作者、年份）
2. 获取zotero_key
3. 生成符合SCHEMA的YAML模板
4. 验证zotero_key有效性

使用场景：
- 通过GitHub Copilot创建新论文YAML时，自动添加zotero_key
- 手动导入论文时，快速查找对应Zotero项目
- 批量验证现有关联
"""

import os
import sys
import json
import re
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
project_root = Path(__file__).parent.parent
zotero_user_id = os.getenv("ZOTERO_USER_ID", "19944378")
zotero_host = os.getenv("ZOTERO_API_HOST", "172.20.96.1")
zotero_port = os.getenv("ZOTERO_API_PORT", "23119")

class ZoteroHelper:
    """Zotero辅助工具类"""
    
    def __init__(self):
        self.base_url = f"http://{zotero_host}:{zotero_port}/api/users/{zotero_user_id}"
        self.headers = {"Host": "127.0.0.1:23119"}
    
    def search_by_title(self, title: str, limit: int = 10) -> List[Dict]:
        """按标题搜索Zotero论文"""
        # Zotero API不支持全文搜索，我们获取所有论文后本地过滤
        url = f"{self.base_url}/items?itemType=journalArticle&limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            if response.status_code != 200:
                print(f"搜索失败: HTTP {response.status_code}")
                return []
            
            items = response.json()
            matched_items = []
            
            title_lower = title.lower()
            for item in items:
                data = item.get('data', {})
                item_title = data.get('title', '')
                
                if title_lower in item_title.lower():
                    matched_items.append({
                        'key': item.get('key', ''),
                        'title': item_title,
                        'date': data.get('date', ''),
                        'creators': data.get('creators', []),
                        'publicationTitle': data.get('publicationTitle', ''),
                        'item': item
                    })
            
            return matched_items
            
        except Exception as e:
            print(f"搜索异常: {e}")
            return []
    
    def search_by_author_year(self, author: str, year: str, limit: int = 10) -> List[Dict]:
        """按作者和年份搜索Zotero论文"""
        url = f"{self.base_url}/items?itemType=journalArticle&limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            if response.status_code != 200:
                print(f"搜索失败: HTTP {response.status_code}")
                return []
            
            items = response.json()
            matched_items = []
            
            author_lower = author.lower()
            for item in items:
                data = item.get('data', {})
                date = data.get('date', '')
                
                # 提取年份
                year_match = re.search(r'\b(\d{4})\b', date) if date else None
                item_year = year_match.group(1) if year_match else ''
                
                # 检查年份匹配
                if year and item_year != year:
                    continue
                
                # 检查作者匹配
                creators = data.get('creators', [])
                author_found = False
                for creator in creators:
                    if creator.get('creatorType') == 'author':
                        name = creator.get('lastName', '') or creator.get('name', '')
                        if author_lower in name.lower():
                            author_found = True
                            break
                
                if author_found or not author:  # 如果未提供作者，只按年份匹配
                    matched_items.append({
                        'key': item.get('key', ''),
                        'title': data.get('title', ''),
                        'date': date,
                        'creators': creators,
                        'publicationTitle': data.get('publicationTitle', ''),
                        'item': item
                    })
            
            return matched_items
            
        except Exception as e:
            print(f"搜索异常: {e}")
            return []
    
    def get_item_by_key(self, zotero_key: str) -> Optional[Dict]:
        """通过zotero_key获取论文详情"""
        url = f"{self.base_url}/items/{zotero_key}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取失败: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"获取异常: {e}")
            return None
    
    def generate_yaml_template(self, zotero_key: str, topic: str = "ultrastable-laser") -> Optional[str]:
        """生成YAML模板"""
        item = self.get_item_by_key(zotero_key)
        if not item:
            return None
        
        data = item.get('data', {})
        meta = item.get('meta', {})
        
        # 提取论文信息
        title = data.get('title', '')
        date = data.get('date', '')
        creators = data.get('creators', [])
        publication_title = data.get('publicationTitle', '')
        
        # 提取第一作者
        first_author = ""
        for creator in creators:
            if creator.get('creatorType') == 'author':
                first_author = creator.get('lastName', '') or creator.get('name', '')
                break
        
        # 提取年份
        year_match = re.search(r'\b(\d{4})\b', date) if date else None
        year = year_match.group(1) if year_match else ''
        
        # 生成文件名（基于作者年份）
        if first_author and year:
            filename = f"{first_author.lower()}{year}.yaml"
        else:
            # 使用标题前几个单词
            words = re.findall(r'\b\w+\b', title)[:3]
            filename = f"{'_'.join(words).lower()}.yaml"
        
        # 生成YAML模板
        from datetime import datetime
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yaml_template = f"""# {title}
# 生成时间: {current_time}
# Zotero Key: {zotero_key}

meta:
  title: "{title}"
  first_author: "{first_author}"
  year: {year}
  zotero_key: "{zotero_key}"
  publication: "{publication_title}"
  status: "未审核"
  tags: []

logical_units:
  # 逻辑单元1: 核心贡献
  - id: "core_contribution"
    claim: "本文的核心贡献是..."
    evidence:
      - type: "experimental_result"
        description: "实验结果表明..."
        source: {{zotero_key: "{zotero_key}", page: "X"}}
      - type: "theoretical_derivation"
        description: "理论推导..."
        source: {{zotero_key: "{zotero_key}", page: "X"}}
    relationships:
      - type: "extends"
        target: "相关论文的ID"
        justification: "扩展了..."

  # 逻辑单元2: 关键技术
  - id: "key_technique"
    claim: "关键技术包括..."
    evidence:
      - type: "method_description"
        description: "方法描述..."
        source: {{zotero_key: "{zotero_key}", page: "X"}}
    relationships:
      - type: "implements"
        target: "技术原理的ID"
        justification: "实现了..."

# 注意:
# 1. 替换...为具体内容
# 2. 填写正确的页码(page字段)
# 3. 建立与已有逻辑单元的关联
# 4. 确保符合SCHEMA规范
"""
        
        return {
            'filename': filename,
            'yaml': yaml_template,
            'paper_info': {
                'title': title,
                'first_author': first_author,
                'year': year,
                'publication': publication_title,
                'zotero_key': zotero_key
            }
        }
    
    def find_best_match(self, title: str = "", author: str = "", year: str = "") -> Optional[Dict]:
        """根据标题、作者、年份找到最佳匹配的Zotero论文"""
        # 优先使用标题搜索
        if title:
            matches = self.search_by_title(title, limit=20)
            if matches:
                # 如果有作者和年份信息，进一步过滤
                if author or year:
                    filtered_matches = []
                    for match in matches:
                        match_author = ""
                        match_year = ""
                        
                        # 提取匹配项的年份
                        date = match.get('date', '')
                        year_match = re.search(r'\b(\d{4})\b', date) if date else None
                        match_year = year_match.group(1) if year_match else ''
                        
                        # 提取匹配项的作者
                        creators = match.get('creators', [])
                        for creator in creators:
                            if creator.get('creatorType') == 'author':
                                match_author = creator.get('lastName', '') or creator.get('name', '')
                                break
                        
                        # 检查匹配
                        author_match = not author or (match_author and author.lower() in match_author.lower())
                        year_match = not year or match_year == year
                        
                        if author_match and year_match:
                            filtered_matches.append(match)
                    
                    if filtered_matches:
                        # 返回第一个匹配项
                        return filtered_matches[0]
                
                # 如果没有过滤条件或过滤后无结果，返回第一个标题匹配
                return matches[0]
        
        # 如果标题搜索无结果，尝试作者+年份搜索
        if author and year:
            matches = self.search_by_author_year(author, year, limit=10)
            if matches:
                return matches[0]
        
        return None

def main():
    """命令行接口"""
    helper = ZoteroHelper()
    
    if len(sys.argv) < 2:
        print("""
Zotero辅助工具 - 帮助未来导入论文时自动关联

用法:
  python zotero_helper.py search --title "论文标题" [--author "作者" --year "年份"]
  python zotero_helper.py get <zotero_key>
  python zotero_helper.py template <zotero_key> [--topic "专题名称"]
  python zotero_helper.py match --title "标题" --author "作者" --year "年份"
  
示例:
  python zotero_helper.py search --title "Mid-infrared frequency combs"
  python zotero_helper.py get YYXGH9X3
  python zotero_helper.py template TRFV3Y5G --topic "optical-frequency-combs"
  python zotero_helper.py match --title "Dissipative Kerr solitons" --author "Kippenberg" --year "2018"
        """)
        return
    
    command = sys.argv[1]
    
    if command == "search":
        # 解析参数
        title = ""
        author = ""
        year = ""
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--title" and i+1 < len(sys.argv):
                title = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--author" and i+1 < len(sys.argv):
                author = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--year" and i+1 < len(sys.argv):
                year = sys.argv[i+1]
                i += 2
            else:
                i += 1
        
        print(f"搜索条件: 标题={title}, 作者={author}, 年份={year}")
        
        if title:
            matches = helper.search_by_title(title)
        elif author or year:
            matches = helper.search_by_author_year(author, year)
        else:
            print("错误: 需要至少一个搜索条件")
            return
        
        if matches:
            print(f"\n找到 {len(matches)} 个匹配项:")
            for i, match in enumerate(matches, 1):
                print(f"\n{i}. {match['key']}")
                print(f"   标题: {match['title'][:80]}...")
                print(f"   日期: {match['date']}")
                if match.get('creators'):
                    authors = [c.get('lastName', c.get('name', '')) for c in match['creators'] if c.get('creatorType') == 'author']
                    print(f"   作者: {', '.join(authors[:3])}")
                if match.get('publicationTitle'):
                    print(f"   期刊: {match['publicationTitle']}")
        else:
            print("未找到匹配项")
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("错误: 需要提供zotero_key")
            return
        
        zotero_key = sys.argv[2]
        item = helper.get_item_by_key(zotero_key)
        
        if item:
            data = item.get('data', {})
            meta = item.get('meta', {})
            
            print(f"论文详情: {zotero_key}")
            print(f"标题: {data.get('title')}")
            print(f"日期: {data.get('date')}")
            print(f"期刊: {data.get('publicationTitle')}")
            print(f"DOI: {data.get('DOI')}")
            
            creators = data.get('creators', [])
            if creators:
                print("作者:")
                for creator in creators:
                    if creator.get('creatorType') == 'author':
                        print(f"  - {creator.get('lastName', '')}, {creator.get('firstName', '')}")
            
            print(f"创建时间: {meta.get('createdDate', '')}")
            print(f"修改时间: {meta.get('modifiedDate', '')}")
        else:
            print(f"未找到论文: {zotero_key}")
    
    elif command == "template":
        if len(sys.argv) < 3:
            print("错误: 需要提供zotero_key")
            return
        
        zotero_key = sys.argv[2]
        topic = "ultrastable-laser"
        
        # 检查是否有--topic参数
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--topic" and i+1 < len(sys.argv):
                topic = sys.argv[i+1]
                break
        
        result = helper.generate_yaml_template(zotero_key, topic)
        if result:
            print(f"生成YAML模板:")
            print(f"文件名: {result['filename']}")
            print(f"建议路径: topics/{topic}/papers/{result['filename']}")
            print(f"\n{result['yaml']}")
            
            # 保存到文件
            save_path = project_root / "templates" / f"{zotero_key}_template.yaml"
            save_path.parent.mkdir(exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(result['yaml'])
            print(f"\n模板已保存到: {save_path}")
        else:
            print(f"无法生成模板: 未找到论文 {zotero_key}")
    
    elif command == "match":
        # 解析参数
        title = ""
        author = ""
        year = ""
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--title" and i+1 < len(sys.argv):
                title = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--author" and i+1 < len(sys.argv):
                author = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--year" and i+1 < len(sys.argv):
                year = sys.argv[i+1]
                i += 2
            else:
                i += 1
        
        if not title and not author:
            print("错误: 需要至少提供标题或作者")
            return
        
        print(f"匹配条件: 标题={title}, 作者={author}, 年份={year}")
        match = helper.find_best_match(title, author, year)
        
        if match:
            print(f"\n找到最佳匹配:")
            print(f"Zotero Key: {match['key']}")
            print(f"标题: {match['title'][:80]}...")
            print(f"日期: {match['date']}")
            
            # 询问是否生成模板
            response = input("\n是否生成YAML模板? (y/n): ").strip().lower()
            if response == 'y':
                topic = input("请输入专题名称 (默认: ultrastable-laser): ").strip()
                if not topic:
                    topic = "ultrastable-laser"
                
                result = helper.generate_yaml_template(match['key'], topic)
                if result:
                    print(f"\n生成YAML模板:")
                    print(f"文件名: {result['filename']}")
                    print(f"建议路径: topics/{topic}/papers/{result['filename']}")
                    print(f"\n{result['yaml'][:500]}...")
        else:
            print("未找到匹配的论文")
    
    else:
        print(f"未知命令: {command}")
        print("使用 'python zotero_helper.py' 查看帮助")

if __name__ == "__main__":
    main()