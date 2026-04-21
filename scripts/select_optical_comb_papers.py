#!/usr/bin/env python3
"""
选择30篇光频梳未处理论文PDF并上传到GitHub
"""

import os
import sys
import json
import sqlite3
import shutil
from pathlib import Path
import subprocess
import re
import glob

# 配置
ZOTERO_DB_PATH = "/mnt/d/Users/hjian/Zotero/zotero.sqlite"
REPO_ROOT = "/home/hjian/sci-logic-kb/sci-logic-kb"
PDFS_DIR = os.path.join(REPO_ROOT, "pdfs")
TOPIC_DIR = os.path.join(REPO_ROOT, "topics/optical-frequency-combs")
PAPERS_DIR = os.path.join(TOPIC_DIR, "papers")
TARGET_COUNT = 30

# 光学频率梳关键词
OPTICAL_COMB_KEYWORDS = [
    "comb", "frequency comb", "optical comb", "dual-comb",
    "astrocomb", "microcomb", "electro-optic comb", "kerr comb",
    "soliton comb", "optical frequency metrology",
    "optical frequency synthesizer", "femtosecond comb",
    "microresonator comb", "dual comb spectroscopy"
]

def extract_existing_zotero_keys():
    """从光学频率梳专题的YAML文件中提取已处理的zotero_key集合"""
    existing_keys = set()
    
    if not os.path.exists(PAPERS_DIR):
        print(f"警告: papers目录不存在: {PAPERS_DIR}")
        return existing_keys
    
    yaml_files = glob.glob(os.path.join(PAPERS_DIR, "*.yaml"))
    print(f"找到 {len(yaml_files)} 个YAML文件")
    
    # 正则表达式匹配 zotero_key: "XXXXX"
    pattern = re.compile(r'zotero_key:\s*[\"\']?([^\"\'\s]+)')
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()
                match = pattern.search(content)
                if match:
                    key = match.group(1).strip('"\'')
                    if key and key != 'zotero_key':  # 过滤错误匹配
                        existing_keys.add(key)
        except Exception as e:
            print(f"读取 {yaml_file} 时出错: {e}")
    
    print(f"从YAML文件中提取了 {len(existing_keys)} 个已处理的zotero_key")
    return existing_keys

def query_optical_comb_papers(existing_keys):
    """从Zotero数据库查询光学频率梳相关论文，排除已处理的"""
    conn = sqlite3.connect(ZOTERO_DB_PATH)
    cursor = conn.cursor()
    
    # 构建关键词查询条件
    keyword_conditions = []
    params = []
    for keyword in OPTICAL_COMB_KEYWORDS:
        keyword_conditions.append("LOWER(itemDataValues.value) LIKE ?")
        params.append(f"%{keyword.lower()}%")
    
    where_clause = " OR ".join(keyword_conditions)
    
    # 查询有PDF附件的光频梳论文
    query = f"""
    SELECT DISTINCT items.key as parentKey, items.itemID, itemDataValues.value as title,
           attachments.key as attachmentKey, itemAttachments.path
    FROM items
    JOIN itemAttachments ON items.itemID = itemAttachments.parentItemID
    JOIN items as attachments ON itemAttachments.itemID = attachments.itemID
    JOIN itemData ON items.itemID = itemData.itemID
    JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
    JOIN fields ON itemData.fieldID = fields.fieldID
    WHERE items.itemTypeID = 22  -- journalArticle
      AND itemAttachments.path LIKE 'storage:%'
      AND attachments.itemTypeID = 3  -- attachment type
      AND fields.fieldName = 'title'
      AND items.key NOT IN ({','.join(['?'] * len(existing_keys))})
      AND ({where_clause})
    ORDER BY items.key
    LIMIT ?;
    """
    
    # 合并参数
    params_all = list(existing_keys) + params + [TARGET_COUNT * 2]  # 多查一些，确保有足够的有PDF附件的论文
    
    print(f"查询数据库，排除 {len(existing_keys)} 个已处理键...")
    cursor.execute(query, params_all)
    papers = cursor.fetchall()
    
    conn.close()
    print(f"查询到 {len(papers)} 篇相关论文")
    return papers

def verify_and_select_papers(papers, target_count):
    """验证论文是否有PDF附件，并选择目标数量的论文"""
    selected = []
    failed = []
    
    for i, (parentKey, itemID, title, attachmentKey, path) in enumerate(papers, 1):
        if len(selected) >= target_count:
            break
            
        # 检查路径格式并构建PDF路径
        if path.startswith("storage:"):
            filename = path.split(":", 1)[1]
            # 假设Zotero安装在D盘
            storage_dir = f"/mnt/d/Users/hjian/Zotero/storage/{attachmentKey}"
            pdf_path = os.path.join(storage_dir, filename)
            
            if os.path.exists(pdf_path):
                selected.append({
                    'parentKey': parentKey,
                    'itemID': itemID,
                    'title': title,
                    'attachmentKey': attachmentKey,
                    'path': pdf_path,
                    'filename': filename
                })
                print(f"✓ {i:3d}. {parentKey}: {title[:80]}...")
            else:
                print(f"✗ {i:3d}. {parentKey}: PDF文件不存在 - {pdf_path}")
                failed.append({'key': parentKey, 'reason': 'PDF文件不存在'})
        else:
            print(f"✗ {i:3d}. {parentKey}: 未知路径格式 - {path}")
            failed.append({'key': parentKey, 'reason': f'未知路径格式: {path}'})
    
    print(f"\n选择结果: {len(selected)} 篇成功，{len(failed)} 篇失败")
    return selected

def clear_pdfs_directory():
    """清空pdfs目录"""
    print(f"\n=== 清空pdfs目录 ===")
    
    if not os.path.exists(PDFS_DIR):
        os.makedirs(PDFS_DIR)
        print(f"创建pdfs目录: {PDFS_DIR}")
        return
    
    # 删除所有PDF文件
    pdf_files = glob.glob(os.path.join(PDFS_DIR, "*.pdf"))
    for pdf_file in pdf_files:
        try:
            os.remove(pdf_file)
            print(f"删除: {os.path.basename(pdf_file)}")
        except Exception as e:
            print(f"删除 {pdf_file} 失败: {e}")
    
    # 删除JSON文件（保留选择记录）
    json_files = glob.glob(os.path.join(PDFS_DIR, "*.json"))
    for json_file in json_files:
        if "batch_info.json" in json_file or "selected_papers.json" in json_file:
            try:
                os.remove(json_file)
                print(f"删除: {os.path.basename(json_file)}")
            except Exception as e:
                print(f"删除 {json_file} 失败: {e}")
    
    print(f"pdfs目录已清空")

def copy_pdfs_to_repo(selected_papers):
    """复制PDF文件到pdfs目录"""
    print(f"\n=== 复制PDF文件 ===")
    
    os.makedirs(PDFS_DIR, exist_ok=True)
    
    successful = []
    failed = []
    
    for i, paper in enumerate(selected_papers, 1):
        parent_key = paper['parentKey']
        src_path = paper['path']
        title = paper['title']
        
        dest_filename = f"{parent_key}.pdf"
        dest_path = os.path.join(PDFS_DIR, dest_filename)
        
        try:
            shutil.copy2(src_path, dest_path)
            file_size = os.path.getsize(dest_path) / 1024 / 1024  # MB
            print(f"✓ {i:2d}. {parent_key}: {title[:60]}... ({file_size:.1f} MB)")
            successful.append({
                'key': parent_key,
                'title': title,
                'src': src_path,
                'dest': dest_path,
                'size_mb': file_size
            })
        except Exception as e:
            print(f"✗ {i:2d}. {parent_key}: 复制失败 - {e}")
            failed.append({'key': parent_key, 'reason': str(e)})
    
    return successful, failed

def generate_file_list(successful_papers):
    """生成PDF文件列表"""
    list_path = os.path.join(PDFS_DIR, "pdf_list.txt")
    
    with open(list_path, 'w', encoding='utf-8') as f:
        f.write(f"光学频率梳专题论文PDF文件列表 - 总计{len(successful_papers)}篇\n")
        f.write("=" * 80 + "\n\n")
        
        for i, paper in enumerate(successful_papers, 1):
            f.write(f"{i:2d}. {paper['key']}.pdf\n")
            f.write(f"    标题: {paper['title']}\n")
            f.write(f"    大小: {paper['size_mb']:.1f} MB\n\n")
    
    print(f"文件列表已生成: {list_path}")
    return list_path

def create_batch_info(selected_papers, existing_keys):
    """创建批次信息文件"""
    batch_info_path = os.path.join(PDFS_DIR, "batch_info.json")
    
    # 从Zotero获取更多信息
    conn = sqlite3.connect(ZOTERO_DB_PATH)
    cursor = conn.cursor()
    
    enriched_papers = []
    for paper in selected_papers:
        # 查询作者和年份
        query = """
        SELECT itemDataValues.value, fields.fieldName
        FROM itemData
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        JOIN fields ON itemData.fieldID = fields.fieldID
        WHERE itemData.itemID = ?
          AND fields.fieldName IN ('firstName', 'lastName', 'date')
        """
        cursor.execute(query, (paper['itemID'],))
        rows = cursor.fetchall()
        
        authors = []
        year = ""
        for value, field_name in rows:
            if field_name in ['firstName', 'lastName']:
                authors.append(value)
            elif field_name == 'date':
                # 提取年份
                match = re.search(r'\d{4}', value)
                if match:
                    year = match.group(0)
        
        enriched_papers.append({
            'parentKey': paper['parentKey'],
            'title': paper['title'],
            'authors': authors,
            'year': year,
            'attachmentKey': paper['attachmentKey'],
            'filename': paper['filename']
        })
    
    conn.close()
    
    batch_info = {
        'topic': 'optical-frequency-combs',
        'selection_date': subprocess.run(['date', '+%Y-%m-%d %H:%M:%S'], capture_output=True, text=True).stdout.strip(),
        'target_count': TARGET_COUNT,
        'selected_count': len(selected_papers),
        'processed_keys_excluded': list(existing_keys),
        'keywords_used': OPTICAL_COMB_KEYWORDS,
        'all_papers': enriched_papers
    }
    
    with open(batch_info_path, 'w', encoding='utf-8') as f:
        json.dump(batch_info, f, indent=2, ensure_ascii=False)
    
    print(f"批次信息已保存: {batch_info_path}")
    return batch_info_path

def upload_to_github(successful, failed):
    """上传PDF文件到GitHub"""
    print(f"\n=== 上传到GitHub ===")
    
    os.chdir(REPO_ROOT)
    
    # 检查git状态
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Git错误: {result.stderr}")
        return False
    
    # 临时修改.gitignore允许上传PDF
    gitignore_path = os.path.join(REPO_ROOT, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        # 备份
        with open(gitignore_path + ".backup", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        # 注释掉pdfs/行
        new_content = re.sub(r'^pdfs/', '# pdfs/  # 临时取消忽略以上传PDF', gitignore_content, flags=re.MULTILINE)
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("临时修改.gitignore以允许上传PDF")
    
    # 添加文件
    subprocess.run(['git', 'add', 'pdfs/'], capture_output=True)
    subprocess.run(['git', 'add', '.gitignore'], capture_output=True)
    
    # 获取文件列表用于提交信息
    pdf_files = glob.glob(os.path.join(PDFS_DIR, "*.pdf"))
    pdf_count = len(pdf_files)
    sample_keys = [os.path.basename(f).replace('.pdf', '') for f in pdf_files[:5]]
    
    # 提交
    commit_msg = f"""添加{len(successful)}篇光频梳未处理论文PDF文件

目标：选择30篇光学频率梳专题未处理论文PDF
实际：成功复制{len(successful)}篇，失败{len(failed)}篇

包含论文：
{chr(10).join([f"- {p['key']}: {p['title'][:60]}..." for p in successful[:10]])}

完整列表见：pdfs/pdf_list.txt
批次信息：pdfs/batch_info.json
"""
    
    commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
    if commit_result.returncode != 0:
        print(f"提交失败: {commit_result.stderr}")
        return False
    
    print("提交成功")
    
    # 推送到GitHub
    print("推送到GitHub...")
    push_result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
    if push_result.returncode != 0:
        print(f"推送失败: {push_result.stderr}")
        return False
    
    print("推送成功")
    
    # 恢复.gitignore
    if os.path.exists(gitignore_path + ".backup"):
        with open(gitignore_path + ".backup", 'r', encoding='utf-8') as f:
            original_content = f.read()
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        os.remove(gitignore_path + ".backup")
        
        # 提交.gitignore恢复
        subprocess.run(['git', 'add', '.gitignore'], capture_output=True)
        subprocess.run(['git', 'commit', '-m', '恢复.gitignore，pdfs/目录恢复忽略状态'], capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True)
        print("恢复.gitignore并提交")
    
    return True

def main():
    """主函数"""
    print("=" * 80)
    print("选择30篇光频梳未处理论文PDF并上传到GitHub")
    print("=" * 80)
    
    # 1. 提取已处理的zotero_key
    existing_keys = extract_existing_zotero_keys()
    
    # 2. 查询Zotero数据库
    papers = query_optical_comb_papers(existing_keys)
    
    if len(papers) < TARGET_COUNT:
        print(f"警告: 只找到 {len(papers)} 篇相关论文，少于目标 {TARGET_COUNT} 篇")
        # 继续处理，但用户可能需要调整目标
    
    # 3. 验证并选择论文
    selected_papers = verify_and_select_papers(papers, TARGET_COUNT)
    
    if len(selected_papers) < TARGET_COUNT:
        print(f"⚠️  严重: 只有 {len(selected_papers)} 篇论文有有效PDF附件，少于目标 {TARGET_COUNT} 篇")
        print("可能需要放宽搜索条件或选择其他专题论文")
        # 询问是否继续
        response = input(f"是否继续处理 {len(selected_papers)} 篇论文? (y/n): ")
        if response.lower() != 'y':
            print("用户取消操作")
            return
    
    # 4. 清空pdfs目录
    clear_pdfs_directory()
    
    # 5. 复制PDF文件
    successful, failed = copy_pdfs_to_repo(selected_papers)
    
    if not successful:
        print("错误: 没有成功复制任何PDF文件")
        return
    
    # 6. 生成文件列表
    generate_file_list(successful)
    
    # 7. 创建批次信息
    create_batch_info(selected_papers, existing_keys)
    
    # 8. 上传到GitHub
    upload_success = upload_to_github(successful, failed)
    
    # 9. 报告
    print(f"\n{'=' * 80}")
    print("处理完成报告")
    print(f"{'=' * 80}")
    print(f"目标数量: {TARGET_COUNT} 篇")
    print(f"成功处理: {len(successful)} 篇")
    print(f"失败处理: {len(failed)} 篇")
    
    total_size = sum(p['size_mb'] for p in successful)
    print(f"总文件大小: {total_size:.1f} MB")
    
    print(f"\n成功论文 (前10篇):")
    for i, paper in enumerate(successful[:10], 1):
        print(f"  {i:2d}. {paper['key']}: {paper['title'][:60]}...")
    
    if failed:
        print(f"\n失败论文:")
        for f in failed:
            print(f"  ✗ {f['key']}: {f['reason']}")
    
    if upload_success:
        print(f"\n✅ 所有操作完成！PDF文件已上传到GitHub。")
        print(f"📁 PDF目录: {PDFS_DIR}")
        print(f"📋 文件列表: {PDFS_DIR}/pdf_list.txt")
        print(f"📊 批次信息: {PDFS_DIR}/batch_info.json")
    else:
        print(f"\n⚠️  GitHub上传失败，但PDF文件已复制到本地目录。")

if __name__ == "__main__":
    main()