#!/usr/bin/env python3
"""
验证所有YAML文件的zotero_key有效性
"""

import os
import yaml
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
project_root = Path(__file__).parent.parent
zotero_user_id = os.getenv("ZOTERO_USER_ID", "19944378")
zotero_host = os.getenv("ZOTERO_API_HOST", "172.20.96.1")
zotero_port = os.getenv("ZOTERO_API_PORT", "23119")

def get_all_yaml_files():
    """获取所有YAML论文文件"""
    yaml_files = list(project_root.glob("topics/**/*.yaml"))
    return yaml_files

def extract_zotero_keys(yaml_files):
    """从YAML文件中提取zotero_key信息"""
    keys_info = {}
    
    for yaml_path in yaml_files:
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            data = yaml.safe_load(content)
            if not data:
                continue
                
            meta = data.get('meta', {})
            zotero_key = meta.get('zotero_key')
            
            if zotero_key:
                rel_path = yaml_path.relative_to(project_root)
                keys_info[zotero_key] = {
                    'path': str(rel_path),
                    'title': meta.get('title', '')[:80],
                    'first_author': meta.get('first_author', ''),
                    'year': meta.get('year', ''),
                    'yaml_path': yaml_path
                }
                
        except Exception as e:
            print(f"解析失败 {yaml_path}: {e}")
    
    return keys_info

def check_zotero_keys_exist(zotero_keys):
    """检查zotero_key是否在Zotero中存在"""
    results = {}
    
    batch_size = 20
    for i in range(0, len(zotero_keys), batch_size):
        batch = zotero_keys[i:i+batch_size]
        
        for key in batch:
            url = f"http://{zotero_host}:{zotero_port}/api/users/{zotero_user_id}/items/{key}"
            headers = {"Host": "127.0.0.1:23119"}
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    item = response.json()
                    data = item.get('data', {})
                    title = data.get('title', '')
                    
                    results[key] = {
                        'exists': True,
                        'title': title[:80] if title else '',
                        'item_type': data.get('itemType', ''),
                        'status_code': response.status_code
                    }
                else:
                    results[key] = {
                        'exists': False,
                        'error': f"HTTP {response.status_code}",
                        'status_code': response.status_code
                    }
                    
            except Exception as e:
                results[key] = {
                    'exists': False,
                    'error': str(e),
                    'status_code': 0
                }
        
        processed = min(i + batch_size, len(zotero_keys))
        print(f"  已检查 {processed}/{len(zotero_keys)} 个key")
    
    return results

def main():
    print("验证sci-logic-kb中所有zotero_key的有效性")
    print("=" * 60)
    
    # 1. 获取所有YAML文件
    yaml_files = get_all_yaml_files()
    print(f"找到 {len(yaml_files)} 个YAML论文文件")
    
    # 2. 提取zotero_key
    keys_info = extract_zotero_keys(yaml_files)
    print(f"提取到 {len(keys_info)} 个zotero_key")
    
    if not keys_info:
        print("未找到zotero_key，无需验证")
        return
    
    # 3. 检查key是否存在
    print(f"\n正在检查zotero_key有效性...")
    check_results = check_zotero_keys_exist(list(keys_info.keys()))
    
    # 4. 统计结果
    valid_count = sum(1 for result in check_results.values() if result.get('exists'))
    invalid_count = len(keys_info) - valid_count
    
    print(f"\n验证结果:")
    print(f"  有效: {valid_count} ({valid_count/len(keys_info)*100:.1f}%)")
    print(f"  无效: {invalid_count} ({invalid_count/len(keys_info)*100:.1f}%)")
    
    # 5. 生成报告
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("Zotero Key 有效性验证报告")
    report_lines.append("=" * 80)
    report_lines.append(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"YAML文件总数: {len(yaml_files)}")
    report_lines.append(f"包含zotero_key的文件: {len(keys_info)}")
    report_lines.append(f"有效key: {valid_count} ({valid_count/len(keys_info)*100:.1f}%)")
    report_lines.append(f"无效key: {invalid_count} ({invalid_count/len(keys_info)*100:.1f}%)")
    
    if invalid_count > 0:
        report_lines.append("\n无效key详情:")
        report_lines.append("-" * 40)
        for key, info in keys_info.items():
            if not check_results.get(key, {}).get('exists'):
                result = check_results.get(key, {})
                report_lines.append(f"- {key}")
                report_lines.append(f"  文件: {info['path']}")
                report_lines.append(f"  标题: {info['title']}")
                report_lines.append(f"  错误: {result.get('error', '未知错误')}")
                report_lines.append("")
    else:
        report_lines.append("\n✓ 所有zotero_key都有效，关联状态良好")
    
    report = "\n".join(report_lines)
    print(f"\n{report}")
    
    # 6. 保存报告
    report_path = project_root / "ZOTERO_KEY_VALIDATION_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n详细报告已保存到: {report_path}")
    
    # 7. 退出码
    if invalid_count > 0:
        print(f"\n发现 {invalid_count} 个无效key，请处理！")
        sys.exit(1)
    else:
        print(f"\n验证通过！")
        sys.exit(0)

if __name__ == "__main__":
    import sys
    main()