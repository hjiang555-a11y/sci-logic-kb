#!/usr/bin/env python3
"""
从Zotero获取4篇特定论文的PDF文件
用户要求的论文：
1. "20 Years and 20 Decimal Digits: A Journey With Optical Frequency Combs" - KTHCQRJ2
2. "Real-time phase tracking for wide-band optical frequency measurements at the 20th decimal place" - UFWLAXMA
3. "Optical atomic clocks: defining the future of time and frequency metrology" - BWR7TEZ6
4. "Roadmap towards the redefinition of the second" - SDG6KXNZ
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import requests
from typing import Optional

# 论文配置：Zotero Key, 作者, 年份, 主题
PAPERS = [
    {
        "zotero_key": "KTHCQRJ2",
        "author": "Giunta",
        "year": "2019",
        "title": "20 Years and 20 Decimal Digits: A Journey With Optical Frequency Combs",
        "topic": "optical-frequency-combs"
    },
    {
        "zotero_key": "UFWLAXMA",
        "author": "Giunta",
        "year": "2020",
        "title": "Real-time phase tracking for wide-band optical frequency measurements at the 20th decimal place",
        "topic": "optical-frequency-combs"
    },
    {
        "zotero_key": "BWR7TEZ6",
        "author": "Fortier",
        "year": "2026",
        "title": "Optical atomic clocks: defining the future of time and frequency metrology",
        "topic": "optical-clocks"
    },
    {
        "zotero_key": "SDG6KXNZ",
        "author": "Dimarcq",
        "year": "2024",
        "title": "Roadmap towards the redefinition of the second",
        "topic": "timescales"
    }
]

class ZoteroPDFFetcher:
    """Zotero PDF获取器"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.pdfs_dir = self.repo_path / "pdfs"
        self.pdfs_dir.mkdir(exist_ok=True)

        # 从环境变量获取配置
        self.zotero_user_id = os.getenv("ZOTERO_USER_ID", "19944378")
        self.windows_ip = self._get_windows_ip()

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

    def fetch_pdf_for_paper(self, paper_info: dict) -> bool:
        """为特定论文获取PDF文件"""
        zotero_key = paper_info["zotero_key"]
        author = paper_info["author"]
        year = paper_info["year"]
        title = paper_info["title"]

        print(f"\n处理论文: {author} {year}")
        print(f"标题: {title[:80]}...")
        print(f"Zotero Key: {zotero_key}")

        # 1. 获取论文附件信息
        try:
            url = f"http://{self.windows_ip}:23119/api/users/{self.zotero_user_id}/items/{zotero_key}/children"
            headers = {"Host": "127.0.0.1:23119"}

            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code != 200:
                print(f"  ❌ Zotero API请求失败: {response.status_code}")
                return False

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
                        # 生成目标文件名
                        pdf_filename = f"{zotero_key}_{author.lower()}{year}.pdf"
                        target_path = self.pdfs_dir / pdf_filename

                        # 复制PDF
                        try:
                            shutil.copy2(pdf_path, target_path)
                            print(f"  ✅ PDF复制成功: {target_path}")
                            print(f"    源文件: {pdf_path}")
                            print(f"    大小: {target_path.stat().st_size / 1024:.1f} KB")
                            return True
                        except Exception as e:
                            print(f"  ❌ 复制PDF失败: {e}")
                            return False
                    else:
                        print(f"  ❌ PDF文件不存在: {pdf_path}")
                        return False

            print(f"  ❌ 未找到PDF附件")
            return False

        except Exception as e:
            print(f"  ❌ 获取PDF失败: {e}")
            return False

    def fetch_all_papers(self):
        """获取所有论文的PDF"""
        print("=" * 80)
        print("开始从Zotero获取4篇论文的PDF文件")
        print("=" * 80)

        success_count = 0
        for paper_info in PAPERS:
            success = self.fetch_pdf_for_paper(paper_info)
            if success:
                success_count += 1

        print(f"\n{'='*80}")
        print(f"获取完成：成功 {success_count}/{len(PAPERS)} 篇论文")

        # 列出pdfs目录中的文件
        pdf_files = list(self.pdfs_dir.glob("*.pdf"))
        if pdf_files:
            print(f"\nPDF文件列表:")
            for pdf_file in pdf_files:
                print(f"  - {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"\n❌ pdfs/目录中没有PDF文件")

        return success_count == len(PAPERS)

def main():
    """主函数"""
    # 切换到仓库根目录
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)

    print(f"工作目录: {repo_root}")
    print(f"PDF目录: {repo_root}/pdfs/")

    fetcher = ZoteroPDFFetcher(repo_root)
    success = fetcher.fetch_all_papers()

    if success:
        print(f"\n✅ 所有4篇论文的PDF已成功获取")
        print(f"下一步：GitHub Actions将自动处理这些论文")
    else:
        print(f"\n⚠️  部分论文获取失败，请检查Zotero中的PDF附件")
        sys.exit(1)

if __name__ == "__main__":
    main()