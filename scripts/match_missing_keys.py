#!/usr/bin/env python3
"""
匹配缺少zotero_key的YAML文件与Zotero论文
支持自动更新和手动确认模式
"""

import os
import yaml
import json
import re
import requests
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
project_root = Path(__file__).parent.parent
zotero_user_id = os.getenv("ZOTERO_USER_ID", "19944378")
zotero_host = os.getenv("ZOTERO_API_HOST", "172.20.96.1")
zotero_port = os.getenv("ZOTERO_API_PORT", "23119")

def get_zotero_items():
    """从Zotero获取所有期刊文章"""
    url = f"http://{zotero_host}:{zotero_port}/api/users/{zotero_user_id}/items?itemType=journalArticle"
    headers = {"Host": "127.0.0.1:23119"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Zotero API错误: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"获取Zotero数据异常: {e}")
        return []

def normalize_text(text: str) -> str:
    """标准化文本以进行匹配"""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def find_missing_keys_yaml(specific_file: str = None) -> List[Dict]:
    """查找缺少zotero_key的YAML文件"""
    missing_files = []
    
    if specific_file:
        yaml_files = [project_root / specific_file]
    else:
        yaml_files = list(project_root.glob("topics/**/*.yaml"))
    
    for yaml_path in yaml_files:
        if not yaml_path.exists():
            print(f"文件不存在: {yaml_path}")
            continue
            
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            data = yaml.safe_load(content)
            if not data:
                continue
                
            meta = data.get('meta', {})
            zotero_key = meta.get('zotero_key')
            
            if not zotero_key:
                missing_files.append({
                    'path': yaml_path,
                    'meta': meta,
                    'title': meta.get('title', ''),
                    'first_author': meta.get('first_author', ''),
                    'year': str(meta.get('year', '')) if meta.get('year') else '',
                    'normalized_title': normalize_text(meta.get('title', ''))
                })
                
        except Exception as e:
            print(f"解析失败 {yaml_path}: {e}")
    
    return missing_files

def match_yaml_to_zotero(missing_files: List[Dict], zotero_items: List[Dict]) -> List[Dict]:
    """匹配YAML文件与Zotero项目"""
    matches = []
    
    # 预处理Zotero项目
    zotero_map = {}
    for item in zotero_items:
        data = item.get('data', {})
        key = item.get('key', '')
        title = data.get('title', '')
        date = data.get('date', '')
        meta = item.get('meta', {})
        creator_summary = meta.get('creatorSummary', '')
        
        # 提取年份
        year_match = re.search(r'\b(\d{4})\b', date) if date else None
        year = year_match.group(1) if year_match else ''
        
        zotero_map[key] = {
            'key': key,
            'title': title,
            'normalized_title': normalize_text(title),
            'year': year,
            'creator_summary': creator_summary,
            'item': item
        }
    
    # 尝试匹配每个缺少key的YAML文件
    for yaml_file in missing_files:
        yaml_path = yaml_file['path']
        yaml_title = yaml_file['title']
        yaml_norm_title = yaml_file['normalized_title']
        yaml_author = yaml_file['first_author']
        yaml_year = yaml_file['year']
        
        best_match = None
        best_score = 0
        
        for z_key, z_item in zotero_map.items():
            score = 0
            
            # 1. 标题匹配（主要依据）
            if yaml_norm_title and z_item['normalized_title']:
                # 检查相互包含关系
                if yaml_norm_title in z_item['normalized_title']:
                    score += 2.0
                elif z_item['normalized_title'] in yaml_norm_title:
                    score += 2.0
                # 检查单词重叠
                yaml_words = set(yaml_norm_title.split())
                zotero_words = set(z_item['normalized_title'].split())
                common_words = yaml_words.intersection(zotero_words)
                if len(common_words) >= 3:
                    score += 1.0
            
            # 2. 作者匹配
            if yaml_author and z_item['creator_summary']:
                if yaml_author.lower() in z_item['creator_summary'].lower():
                    score += 1.0
            
            # 3. 年份匹配
            if yaml_year and z_item['year'] and yaml_year == z_item['year']:
                score += 0.5
            
            if score > best_score:
                best_score = score
                best_match = z_item
        
        if best_match and best_score >= 2.0:
            matches.append({
                'yaml_path': yaml_path,
                'yaml_title': yaml_title[:80],
                'yaml_author': yaml_author,
                'yaml_year': yaml_year,
                'matched_key': best_match['key'],
                'matched_title': best_match['title'][:80],
                'matched_year': best_match['year'],
                'match_score': best_score,
                'confidence': 'high' if best_score >= 3.0 else 'medium'
            })
        else:
            matches.append({
                'yaml_path': yaml_path,
                'yaml_title': yaml_title[:80],
                'yaml_author': yaml_author,
                'yaml_year': yaml_year,
                'matched_key': None,
                'matched_title': None,
                'match_score': best_score,
                'confidence': 'low'
            })
    
    return matches

def update_yaml_with_key(yaml_path: Path, zotero_key: str) -> bool:
    """更新YAML文件，添加zotero_key字段"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析YAML
        data = yaml.safe_load(content)
        if not data:
            return False
        
        # 确保有meta部分
        if 'meta' not in data:
            data['meta'] = {}
        
        # 添加zotero_key
        data['meta']['zotero_key'] = zotero_key
        
        # 写回文件
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        return True
        
    except Exception as e:
        print(f"更新YAML文件失败 {yaml_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="匹配缺少zotero_key的YAML文件")
    parser.add_argument("--dry-run", action="store_true", help="只显示匹配结果，不更新文件")
    parser.add_argument("--auto-update", action="store_true", help="自动更新高置信度匹配")
    parser.add_argument("--file", type=str, help="只处理指定文件")
    parser.add_argument("--force", action="store_true", help="强制更新所有匹配（包括中置信度）")
    
    args = parser.parse_args()
    
    print("匹配缺少zotero_key的YAML文件")
    print("=" * 60)
    
    # 1. 查找缺少key的YAML文件
    missing_files = find_missing_keys_yaml(args.file)
    print(f"找到 {len(missing_files)} 个缺少zotero_key的YAML文件")
    
    if not missing_files:
        print("所有YAML文件都已有关联！")
        return
    
    # 显示缺少key的文件
    print("\n缺少zotero_key的文件:")
    for i, file_info in enumerate(missing_files):
        rel_path = file_info['path'].relative_to(project_root)
        print(f"  {i+1}. {rel_path}")
        print(f"     标题: {file_info['title'][:60]}...")
        print(f"     作者: {file_info['first_author']}, 年份: {file_info['year']}")
    
    # 2. 从Zotero获取论文
    print(f"\n正在从Zotero加载论文数据...")
    zotero_items = get_zotero_items()
    print(f"从Zotero加载了 {len(zotero_items)} 篇期刊文章")
    
    if not zotero_items:
        print("警告: 未获取到Zotero数据，无法匹配")
        return
    
    # 3. 匹配
    print(f"\n正在匹配...")
    matches = match_yaml_to_zotero(missing_files, zotero_items)
    
    # 4. 分类匹配结果
    high_conf_matches = [m for m in matches if m['confidence'] == 'high']
    medium_conf_matches = [m for m in matches if m['confidence'] == 'medium']
    low_conf_matches = [m for m in matches if m['confidence'] == 'low']
    
    print(f"\n匹配结果:")
    print(f"  高置信度匹配: {len(high_conf_matches)}")
    print(f"  中置信度匹配: {len(medium_conf_matches)}")
    print(f"  低置信度/无匹配: {len(low_conf_matches)}")
    
    # 显示匹配详情
    if high_conf_matches:
        print(f"\n高置信度匹配:")
        for match in high_conf_matches:
            rel_path = match['yaml_path'].relative_to(project_root)
            print(f"  ✓ {rel_path}")
            print(f"     匹配: {match['matched_key']}")
            print(f"     标题: {match['matched_title']}")
            print(f"     分数: {match['match_score']:.1f}")
    
    if medium_conf_matches:
        print(f"\n中置信度匹配 (需要确认):")
        for match in medium_conf_matches:
            rel_path = match['yaml_path'].relative_to(project_root)
            print(f"  ~ {rel_path}")
            print(f"     匹配: {match['matched_key']}")
            print(f"     标题: {match['matched_title']}")
            print(f"     分数: {match['match_score']:.1f}")
    
    if low_conf_matches:
        print(f"\n低置信度/无匹配 (需要手动检查):")
        for match in low_conf_matches:
            rel_path = match['yaml_path'].relative_to(project_root)
            print(f"  ? {rel_path}")
            print(f"     最佳分数: {match['match_score']:.1f}")
    
    # 5. 更新逻辑
    if args.dry_run:
        print(f"\n干运行模式：不更新文件")
        return
    
    updated_count = 0
    if args.auto_update or args.force:
        print(f"\n自动更新模式...")
        
        matches_to_update = []
        if args.force:
            # 强制更新所有匹配
            matches_to_update = [m for m in matches if m['matched_key']]
        else:
            # 只更新高置信度匹配
            matches_to_update = high_conf_matches
        
        for match in matches_to_update:
            success = update_yaml_with_key(match['yaml_path'], match['matched_key'])
            if success:
                print(f"  ✓ 更新成功: {match['yaml_path'].relative_to(project_root)}")
                print(f"     添加: zotero_key: \"{match['matched_key']}\"")
                updated_count += 1
            else:
                print(f"  ✗ 更新失败: {match['yaml_path'].relative_to(project_root)}")
    else:
        # 交互模式
        if high_conf_matches:
            print(f"\n是否更新高置信度匹配? (y/n): ", end="")
            response = input().strip().lower()
            
            if response == 'y':
                for match in high_conf_matches:
                    success = update_yaml_with_key(match['yaml_path'], match['matched_key'])
                    if success:
                        print(f"  ✓ 更新成功: {match['yaml_path'].relative_to(project_root)}")
                        updated_count += 1
                    else:
                        print(f"  ✗ 更新失败: {match['yaml_path'].relative_to(project_root)}")
        
        if medium_conf_matches:
            print(f"\n是否更新中置信度匹配? (y/n): ", end="")
            response = input().strip().lower()
            
            if response == 'y':
                for match in medium_conf_matches:
                    print(f"  更新 {match['yaml_path'].relative_to(project_root)}? (y/n): ", end="")
                    confirm = input().strip().lower()
                    if confirm == 'y':
                        success = update_yaml_with_key(match['yaml_path'], match['matched_key'])
                        if success:
                            print(f"    ✓ 更新成功")
                            updated_count += 1
                        else:
                            print(f"    ✗ 更新失败")
    
    # 6. 生成报告
    report_content = f"""# Zotero Key匹配更新报告
更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
模式: {'dry-run' if args.dry_run else 'auto-update' if args.auto_update else 'interactive'}

## 摘要
- 缺少zotero_key的文件: {len(missing_files)} 个
- 高置信度匹配: {len(high_conf_matches)} 个
- 中置信度匹配: {len(medium_conf_matches)} 个
- 低置信度匹配: {len(low_conf_matches)} 个
- 更新成功: {updated_count} 个
"""
    
    if updated_count > 0:
        report_content += "\n## 更新详情\n"
        for match in matches:
            if match.get('matched_key'):
                rel_path = match['yaml_path'].relative_to(project_root)
                report_content += f"\n### {rel_path}\n"
                report_content += f"- 原标题: {match['yaml_title']}\n"
                report_content += f"- 匹配Zotero Key: `{match['matched_key']}`\n"
                report_content += f"- 匹配标题: {match['matched_title']}\n"
                report_content += f"- 匹配分数: {match['match_score']:.1f}\n"
                report_content += f"- 置信度: {match['confidence']}\n"
    
    report_path = project_root / "ZOTERO_MATCH_UPDATE_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n详细报告已保存到: {report_path}")
    print(f"\n完成！已更新 {updated_count} 个文件")
    print(f"剩余 {len(medium_conf_matches) + len(low_conf_matches)} 个文件需要手动检查")

if __name__ == "__main__":
    main()