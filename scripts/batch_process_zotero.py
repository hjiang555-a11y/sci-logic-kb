#!/usr/bin/env python3
"""
批量处理Zotero中未处理的超稳激光论文

功能：
1. 从QUEUE.md读取未处理论文（[ ]状态）
2. 通过Zotero API获取PDF文件
3. 复制PDF到pdfs/目录
4. 分批创建GitHub Issue（每10篇）
5. 处理完成后可选择性清理PDF文件

注意事项：
- 需要Zotero API访问权限
- 需要GitHub token创建Issue
- 遵循Schema v3.2规范
- 新开节点标注未审核
"""

import re
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import requests
from typing import List, Dict, Tuple, Optional


class ZoteroPaper:
    """表示Zotero中的一篇论文"""
    def __init__(self, zotero_key: str, title: str, author_year: str, pdf_filename: str = None):
        self.zotero_key = zotero_key
        self.title = title
        self.author_year = author_year
        self.pdf_filename = pdf_filename
        self.pdf_path = None
        self.storage_key = None

    def __str__(self):
        return f"{self.zotero_key} | {self.author_year} | {self.title[:50]}..."


class BatchProcessor:
    """批量处理器"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.queue_path = self.repo_path / "QUEUE.md"
        self.pdfs_dir = self.repo_path / "pdfs"
        self.pdfs_dir.mkdir(exist_ok=True)

        # 从环境变量获取配置
        self.zotero_user_id = os.getenv("ZOTERO_USER_ID", "19944378")
        self.windows_ip = self._get_windows_ip()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPOSITORY", "hjiang555-a11y/sci-logic-kb")

    def _get_windows_ip(self) -> str:
        """获取Windows宿主机的IP地址"""
        try:
            result = subprocess.run(
                "ip route | grep default | awk '{print $3}'",
                shell=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"获取Windows IP失败: {e}")
            return "127.0.0.1"

    def parse_queue(self) -> List[ZoteroPaper]:
        """解析QUEUE.md，提取未处理的论文"""
        papers = []

        with open(self.queue_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配论文行：[ ] `ZOTERO_KEY` | Author Year | Title
        pattern = r'\[ \]\s*`([A-Z0-9]{8})`\s*\|\s*([^|]+)\s*\|\s*(.+)'
        matches = re.findall(pattern, content)

        for match in matches:
            zotero_key = match[0]
            author_year = match[1].strip()
            title = match[2].strip()

            # 生成预期的PDF文件名
            # 从author_year提取作者和年份
            author_match = re.match(r'([A-Za-z]+)\s+(\d{4})', author_year)
            if author_match:
                author = author_match.group(1).lower()
                year = author_match.group(2)
                pdf_filename = f"{zotero_key}_{author}{year}.pdf"
            else:
                # 如果格式不符合预期，使用简单格式
                pdf_filename = f"{zotero_key}_{author_year.replace(' ', '_')}.pdf"

            paper = ZoteroPaper(zotero_key, title, author_year, pdf_filename)
            papers.append(paper)

        print(f"从QUEUE.md中找到 {len(papers)} 篇未处理论文")
        return papers

    def fetch_zotero_pdf(self, paper: ZoteroPaper) -> Optional[Path]:
        """从Zotero获取PDF文件"""
        try:
            # 获取论文附件信息
            url = f"http://{self.windows_ip}:23119/api/users/{self.zotero_user_id}/items/{paper.zotero_key}/children"
            headers = {"Host": "127.0.0.1:23119"}

            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code != 200:
                print(f"  {paper.zotero_key}: Zotero API请求失败: {response.status_code}")
                return None

            items = response.json()

            for item in items:
                data = item.get('data', {})
                if data.get('itemType') == 'attachment':
                    storage_key = data.get('key', '')
                    filename = data.get('filename', '')

                    if not filename.lower().endswith('.pdf'):
                        continue

                    # PDF在WSL中的路径
                    pdf_path = Path(f"/mnt/d/Users/hjian/Zotero/storage/{storage_key}/{filename}")

                    if pdf_path.exists():
                        paper.storage_key = storage_key
                        paper.pdf_path = pdf_path
                        return pdf_path
                    else:
                        print(f"  {paper.zotero_key}: PDF文件不存在: {pdf_path}")

            print(f"  {paper.zotero_key}: 未找到PDF附件")
            return None

        except Exception as e:
            print(f"  {paper.zotero_key}: 获取PDF失败: {e}")
            return None

    def copy_pdf_to_repo(self, paper: ZoteroPaper) -> bool:
        """复制PDF到仓库的pdfs/目录"""
        if not paper.pdf_path:
            print(f"  {paper.zotero_key}: 无PDF路径")
            return False

        target_path = self.pdfs_dir / paper.pdf_filename

        try:
            shutil.copy2(paper.pdf_path, target_path)
            print(f"  {paper.zotero_key}: 复制PDF -> {target_path}")
            return True
        except Exception as e:
            print(f"  {paper.zotero_key}: 复制PDF失败: {e}")
            return False

    def create_github_issue(self, paper: ZoteroPaper) -> bool:
        """创建GitHub Issue触发论文处理"""
        if not self.github_token:
            print(f"  警告: 未设置GITHUB_TOKEN，跳过Issue创建 (env: {os.environ.get('GITHUB_TOKEN', '未设置')[:10]}...)")
            return False

        # Issue模板数据
        issue_data = {
            "title": f"Process: {paper.author_year}",
            "body": f"处理论文: {paper.title}\n\n"
                   f"**Author Year**: {paper.author_year}\n"
                   f"**Zotero Key**: {paper.zotero_key}\n"
                   f"**PDF**: {paper.pdf_filename}\n"
                   f"**Notes**: 批量处理 - 新节点标注未审核，优先复用已有节点",
            "labels": ["process-paper", "batch-process"]
        }

        try:
            url = f"https://api.github.com/repos/{self.github_repo}/issues"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            response = requests.post(url, headers=headers, json=issue_data, timeout=30)

            if response.status_code == 201:
                issue_number = response.json()["number"]
                print(f"  {paper.zotero_key}: 创建Issue #{issue_number}")
                return True
            else:
                print(f"  {paper.zotero_key}: 创建Issue失败: {response.status_code}")
                return False

        except Exception as e:
            print(f"  {paper.zotero_key}: 创建Issue异常: {e}")
            return False

    def batch_process(self, batch_size: int = 10, non_interactive: bool = False):
        """批量处理论文"""
        # 获取未处理论文
        papers = self.parse_queue()

        if not papers:
            print("没有未处理的论文")
            return

        print(f"开始批量处理 {len(papers)} 篇论文，每 {batch_size} 篇一批")
        if non_interactive:
            print("非交互模式：自动继续所有批次")

        # 分批处理
        for batch_idx in range(0, len(papers), batch_size):
            batch = papers[batch_idx:batch_idx + batch_size]
            batch_num = batch_idx // batch_size + 1

            print(f"\n{'='*60}")
            print(f"处理第 {batch_num} 批 ({len(batch)} 篇论文)")
            print(f"{'='*60}")

            # 处理本批论文
            for i, paper in enumerate(batch, 1):
                print(f"\n[{i}/{len(batch)}] 处理: {paper}")

                # 1. 获取PDF
                pdf_found = self.fetch_zotero_pdf(paper)
                if not pdf_found:
                    print(f"  跳过: 未找到PDF")
                    continue

                # 2. 复制到仓库
                copied = self.copy_pdf_to_repo(paper)
                if not copied:
                    print(f"  跳过: 复制PDF失败")
                    continue

                # 3. 创建GitHub Issue
                issue_created = self.create_github_issue(paper)
                if not issue_created:
                    print(f"  警告: Issue创建失败，但PDF已复制")

            print(f"\n第 {batch_num} 批处理完成")

            # 如果不是最后一批，询问是否继续
            if batch_idx + batch_size < len(papers):
                if non_interactive:
                    print("非交互模式：自动继续下一批")
                    continue
                else:
                    print("等待用户确认或自动继续...")
                    print("(按Ctrl+C中断，或等待继续下一批)")
                    try:
                        input("按Enter继续下一批，或Ctrl+C中断: ")
                    except KeyboardInterrupt:
                        print("\n用户中断")
                        break

        print(f"\n{'='*60}")
        print(f"批量处理完成")
        print(f"总共处理了 {len([p for p in papers if p.pdf_path])} 篇论文")
        print(f"PDF文件保存在: {self.pdfs_dir}")
        print(f"注意: 处理完成后可运行 cleanup_pdfs.py 清理PDF文件")

    def cleanup_processed_pdfs(self):
        """清理已处理的PDF文件"""
        # 读取SCHEMA.md中的已处理论文列表
        schema_path = self.repo_path / "SCHEMA.md"

        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 查找已处理论文表格
            # 这里需要根据实际格式解析

            print("清理功能待实现")
            print("请手动删除已处理的PDF文件:")

            for pdf_file in self.pdfs_dir.glob("*.pdf"):
                print(f"  rm {pdf_file}")

        except Exception as e:
            print(f"清理失败: {e}")


def main():
    """主函数"""
    processor = BatchProcessor()

    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description="批量处理Zotero未处理论文")
    parser.add_argument("--batch-size", type=int, default=10, help="每批处理数量")
    parser.add_argument("--non-interactive", action="store_true", help="非交互模式，自动继续所有批次")
    parser.add_argument("--cleanup", action="store_true", help="清理已处理的PDF文件")

    args = parser.parse_args()

    if args.cleanup:
        processor.cleanup_processed_pdfs()
    else:
        processor.batch_process(args.batch_size, args.non_interactive)


if __name__ == "__main__":
    main()