#!/usr/bin/env python3
"""
GitHub PDF批次更新：删除已处理PDF，添加13篇新的光频梳论文
"""

import os
import json
import shutil
import sqlite3
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """运行shell命令"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
    return result

def get_pdf_from_zotero(parent_key, zotero_db_path):
    """从Zotero数据库获取单篇论文的PDF文件路径"""
    conn = sqlite3.connect(zotero_db_path)
    cursor = conn.cursor()
    
    # 1. 根据parentKey获取itemID
    cursor.execute("SELECT itemID FROM items WHERE key = ?", (parent_key,))
    row = cursor.fetchone()
    if not row:
        print(f"  ✗ 未找到论文 {parent_key}")
        conn.close()
        return None, None
    
    item_id = row[0]
    
    # 2. 查找PDF附件
    query = """
    SELECT ia.path, i.key as attachmentKey
    FROM itemAttachments ia
    JOIN items i ON ia.itemID = i.itemID
    WHERE ia.parentItemID = ?
      AND ia.path LIKE 'storage:%'
      AND i.itemTypeID = 3  -- attachment type
    """
    cursor.execute(query, (item_id,))
    rows = cursor.fetchall()
    
    pdf_info = None
    for path, attachment_key in rows:
        if path and path.startswith("storage:"):
            filename = path.split(":", 1)[1]
            if filename.lower().endswith('.pdf'):
                pdf_info = (attachment_key, filename)
                break
    
    conn.close()
    
    if not pdf_info:
        print(f"  ✗ 未找到PDF附件 {parent_key}")
        return None, None
    
    attachment_key, filename = pdf_info
    
    # 构建PDF路径（假设Zotero安装在D盘）
    storage_dir = f"/mnt/d/Users/hjian/Zotero/storage/{attachment_key}"
    pdf_path = os.path.join(storage_dir, filename)
    
    if not os.path.exists(pdf_path):
        print(f"  ✗ PDF文件不存在 {pdf_path}")
        return None, None
    
    return pdf_path, filename

def copy_pdfs_to_repo(selected_papers, pdfs_dir, zotero_db_path):
    """复制PDF文件到仓库pdfs目录"""
    print("\n=== 复制PDF文件 ===")
    
    successful = []
    failed = []
    
    for paper in selected_papers:
        parent_key = paper["parentKey"]
        title = paper["title"]
        
        print(f"\n处理: {parent_key}")
        
        pdf_path, filename = get_pdf_from_zotero(parent_key, zotero_db_path)
        if not pdf_path:
            failed.append({"key": parent_key, "reason": "未找到PDF"})
            continue
        
        # 目标文件名
        dest_filename = f"{parent_key}.pdf"
        dest_path = os.path.join(pdfs_dir, dest_filename)
        
        try:
            shutil.copy2(pdf_path, dest_path)
            file_size = os.path.getsize(dest_path) / 1024 / 1024
            print(f"  ✓ 复制成功: {dest_filename} ({file_size:.1f} MB)")
            successful.append({
                "key": parent_key,
                "title": title,
                "src": pdf_path,
                "dest": dest_path,
                "size_mb": file_size
            })
        except Exception as e:
            print(f"  ✗ 复制失败: {e}")
            failed.append({"key": parent_key, "reason": str(e)})
    
    return successful, failed

def get_paper_titles_from_zotero(paper_keys, zotero_db_path):
    """从Zotero数据库获取论文标题"""
    conn = sqlite3.connect(zotero_db_path)
    cursor = conn.cursor()
    
    papers_with_titles = []
    
    for key in paper_keys:
        query = """
        SELECT items.key, itemDataValues.value as title
        FROM items
        JOIN itemData ON items.itemID = itemData.itemID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        JOIN fields ON itemData.fieldID = fields.fieldID
        WHERE items.itemTypeID = 22  -- journalArticle
          AND items.key = ?
          AND fields.fieldName = 'title'
        """
        
        cursor.execute(query, (key,))
        row = cursor.fetchone()
        
        if row:
            parent_key, title = row
            papers_with_titles.append({
                "parentKey": parent_key,
                "title": title
            })
        else:
            print(f"警告: 未找到论文 {key} 的标题信息")
            papers_with_titles.append({
                "parentKey": key,
                "title": f"Unknown title for {key}"
            })
    
    conn.close()
    return papers_with_titles

def cleanup_old_pdfs(pdfs_dir):
    """清理旧的PDF文件"""
    print("\n=== 清理旧PDF文件 ===")
    
    # 获取所有PDF文件
    existing_pdfs = [f for f in os.listdir(pdfs_dir) if f.lower().endswith('.pdf')]
    
    print(f"pdfs目录现有 {len(existing_pdfs)} 个PDF文件")
    
    if existing_pdfs:
        print(f"将删除以下PDF文件:")
        for i, pdf in enumerate(existing_pdfs[:10], 1):
            print(f"  {i}. {pdf}")
        if len(existing_pdfs) > 10:
            print(f"  ... 共 {len(existing_pdfs)} 个文件")
        
        # 确认删除
        response = input("\n确认删除所有旧PDF文件？(y/n): ")
        if response.lower() != 'y':
            print("取消删除操作")
            return False
        
        # 删除文件
        deleted_count = 0
        for pdf in existing_pdfs:
            pdf_path = os.path.join(pdfs_dir, pdf)
            try:
                os.remove(pdf_path)
                deleted_count += 1
            except Exception as e:
                print(f"删除失败 {pdf}: {e}")
        
        print(f"已删除 {deleted_count} 个PDF文件")
        return True
    else:
        print("pdfs目录为空，无需清理")
        return True

def git_commit_and_push(repo_dir, delete_count, add_count, paper_keys, successful_papers):
    """提交更改并推送到GitHub"""
    print("\n=== 提交到Git ===")
    
    os.chdir(repo_dir)
    
    # 备份并临时修改.gitignore
    print("1. 临时修改.gitignore以允许PDF上传...")
    gitignore_path = os.path.join(repo_dir, ".gitignore")
    backup_path = gitignore_path + ".backup"
    
    if os.path.exists(gitignore_path):
        shutil.copy2(gitignore_path, backup_path)
        
        # 读取内容
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 临时注释掉pdfs/忽略规则
        import re
        new_content = re.sub(r'^pdfs/', '# pdfs/  # 临时取消忽略以上传PDF', content, flags=re.MULTILINE)
        
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    # 添加PDF文件
    print("2. 添加PDF文件到Git...")
    run_command("git add pdfs/*.pdf")
    
    # 生成提交信息
    paper_titles = "\n".join([f"- {p['key']}: {p['title'][:60]}..." for p in successful_papers[:5]])
    if len(successful_papers) > 5:
        paper_titles += f"\n- ... 共 {len(successful_papers)} 篇论文"
    
    commit_msg = f"""更新光频梳专题PDF文件：删除{delete_count}篇已处理论文，新增{add_count}篇未处理论文

删除操作：删除{delete_count}个PDF文件
新增论文:
{paper_titles}

总计: {add_count} 篇新PDF文件
专题: optical-frequency-combs
状态: 未处理，等待GitHub Copilot分析
"""
    
    result = run_command(f'git commit -m "{commit_msg}"')
    if result.returncode != 0:
        print(f"提交失败: {result.stderr}")
        
        # 恢复.gitignore
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, gitignore_path)
            os.remove(backup_path)
        
        return False
    
    print("提交完成")
    
    # 推送到GitHub
    print("\n=== 推送到GitHub ===")
    result = run_command("git push origin main")
    
    # 恢复.gitignore
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, gitignore_path)
        os.remove(backup_path)
        run_command("git add .gitignore")
        run_command('git commit -m "恢复.gitignore，pdfs/目录恢复忽略状态"')
        run_command("git push origin main")
    
    if result.returncode == 0:
        print("推送成功")
        return True
    else:
        print(f"推送失败: {result.stderr}")
        return False

def generate_pdf_list(pdfs_dir, successful_papers):
    """生成PDF文件列表"""
    print("\n=== 生成PDF文件列表 ===")
    
    list_path = os.path.join(pdfs_dir, "pdf_list.txt")
    
    with open(list_path, 'w', encoding='utf-8') as f:
        f.write(f"光频梳专题未处理论文PDF文件列表 - 总计{len(successful_papers)}篇\n")
        f.write("=" * 60 + "\n\n")
        f.write("统计时间: 2026-04-22\n")
        f.write(f"专题: optical-frequency-combs\n")
        f.write(f"状态: 未处理，等待GitHub Copilot分析\n\n")
        
        for i, paper in enumerate(successful_papers, 1):
            f.write(f"{i:2d}. {paper['key']}.pdf\n")
            f.write(f"    标题: {paper['title']}\n")
            f.write(f"    大小: {paper['size_mb']:.1f} MB\n")
            f.write(f"    原路径: {os.path.basename(paper['src'])}\n\n")
    
    print(f"PDF列表已生成: {list_path}")
    return list_path

def main():
    """主函数：完整的PDF批次更新工作流"""
    # 配置路径
    REPO_DIR = "/home/hjian/sci-logic-kb/sci-logic-kb"
    PDFS_DIR = os.path.join(REPO_DIR, "pdfs")
    ZOTERO_DB = "/mnt/d/Users/hjian/Zotero/zotero.sqlite"
    
    # 13篇未处理但有PDF的光频梳论文
    unprocessed_paper_keys = [
        "8NE7UAUR", "LB6RJ2MZ", "WCBMETLH", "WHNQC4FV", "X6KNIXMW",
        "XHCB4X6R", "XZTNQ8D4", "Y7KZ89LA", "YD2MQC49", "ZG45BBYV",
        "ZN7TS37H", "ZNCBFZR5", "ZSWYS26E"
    ]
    
    print("开始GitHub PDF批次更新工作流")
    print(f"目标: 上传 {len(unprocessed_paper_keys)} 篇未处理的光频梳论文PDF")
    
    # 1. 清理旧PDF文件
    if not cleanup_old_pdfs(PDFS_DIR):
        print("清理操作取消，退出")
        return
    
    # 2. 从Zotero获取论文标题
    print("\n=== 获取论文信息 ===")
    selected_papers = get_paper_titles_from_zotero(unprocessed_paper_keys, ZOTERO_DB)
    print(f"获取到 {len(selected_papers)} 篇论文的标题信息")
    
    # 3. 复制PDF文件
    successful, failed = copy_pdfs_to_repo(selected_papers, PDFS_DIR, ZOTERO_DB)
    
    if not successful:
        print("错误: 没有成功获取任何PDF文件")
        return
    
    # 4. 生成PDF列表
    pdf_list_path = generate_pdf_list(PDFS_DIR, successful)
    
    # 5. 提交并推送到GitHub
    old_pdf_count = len([f for f in os.listdir(PDFS_DIR) if f.lower().endswith('.pdf')]) - len(successful)
    git_success = git_commit_and_push(
        REPO_DIR, 
        delete_count=old_pdf_count,
        add_count=len(successful),
        paper_keys=[p["key"] for p in successful],
        successful_papers=successful
    )
    
    # 6. 报告
    print("\n=== 完成报告 ===")
    print(f"成功处理: {len(successful)} 篇论文")
    total_size = sum(p["size_mb"] for p in successful)
    
    print("\n论文列表:")
    for i, paper in enumerate(successful, 1):
        print(f"  {i:2d}. {paper['key']}: {paper['title'][:70]}... ({paper['size_mb']:.1f} MB)")
    
    print(f"\n总大小: {total_size:.1f} MB")
    print(f"平均大小: {total_size/len(successful):.1f} MB/篇")
    
    if failed:
        print(f"\n失败: {len(failed)} 篇论文")
        for f in failed:
            print(f"  ✗ {f['key']}: {f['reason']}")
    
    print(f"\n删除的旧PDF: {old_pdf_count} 个文件")
    
    print(f"\n✅ GitHub PDF批次更新完成！")
    print(f"📋 PDF列表: {pdf_list_path}")
    print(f"📁 PDF目录: {PDFS_DIR}")
    print("\n下一步: 使用GitHub Copilot处理这些PDF文件")

if __name__ == "__main__":
    main()