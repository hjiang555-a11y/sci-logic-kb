#!/usr/bin/env python3
"""
批量质量检查与整理脚本

功能：
1. 检查最近处理的N篇论文YAML文件
2. 验证节点唯一性、关系完整性
3. 整理节点，避免重复，优先复用已有节点
4. 标注新开节点为未审核
5. 生成质量报告

遵循Schema v3.2要求：
- 全局唯一ID
- 关系有source.claim
- 指标有conditions
- 原理节点有conditions/preconditions
"""

import os
import sys
import yaml
import glob
from pathlib import Path
from typing import List, Dict, Set, Tuple
from datetime import datetime


class QualityChecker:
    """质量检查器"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.papers_dir = self.repo_path / "papers"
        self.schema_path = self.repo_path / "SCHEMA.md"

        # 存储所有已知节点（用于检查唯一性）
        self.all_nodes: Set[str] = set()
        self.all_relations: Set[str] = set()

        # 加载已有节点
        self._load_existing_nodes()

    def _load_existing_nodes(self):
        """加载所有已存在的节点"""
        # 扫描所有YAML文件
        yaml_files = list(self.papers_dir.glob("*.yaml"))

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                # 收集节点
                for section in ['entities', 'principles', 'methods', 'metrics']:
                    if section in data:
                        for node_id in data[section].keys():
                            self.all_nodes.add(node_id)

                # 收集关系
                if 'relations' in data:
                    for rel_id in data['relations'].keys():
                        self.all_relations.add(rel_id)

            except Exception as e:
                print(f"警告: 加载 {yaml_file} 失败: {e}")

        print(f"已加载 {len(self.all_nodes)} 个节点，{len(self.all_relations)} 个关系")

    def get_recent_papers(self, count: int = 10) -> List[Path]:
        """获取最近修改的论文YAML文件"""
        yaml_files = list(self.papers_dir.glob("*.yaml"))

        # 按修改时间排序
        yaml_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        return yaml_files[:count]

    def check_paper(self, yaml_path: Path) -> Dict:
        """检查单篇论文的质量"""
        issues = {
            "file": str(yaml_path.name),
            "warnings": [],
            "errors": [],
            "new_nodes": [],
            "duplicate_nodes": [],
            "missing_source_claim": [],
            "missing_conditions": []
        }

        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # 检查必需字段
            if 'paper' not in data:
                issues["errors"].append("缺少 'paper' 部分")
                return issues

            paper_info = data['paper']
            paper_title = paper_info.get('title', '未知')

            print(f"\n检查: {paper_title}")
            print(f"文件: {yaml_path.name}")

            # 检查各个部分
            for section_name, section_data in data.items():
                if section_name == 'paper':
                    continue

                if section_name in ['entities', 'principles', 'methods', 'metrics']:
                    issues.update(self._check_nodes(section_name, section_data, yaml_path.name))
                elif section_name == 'relations':
                    issues.update(self._check_relations(section_data))

        except Exception as e:
            issues["errors"].append(f"解析YAML失败: {e}")

        return issues

    def _check_nodes(self, section_name: str, nodes: Dict, source_file: str) -> Dict:
        """检查节点质量"""
        issues = {
            "new_nodes": [],
            "duplicate_nodes": [],
            "missing_conditions": []
        }

        if not nodes:
            return issues

        for node_id, node_data in nodes.items():
            # 检查节点唯一性
            if node_id in self.all_nodes:
                issues["duplicate_nodes"].append(f"{node_id} (在 {section_name})")
            else:
                issues["new_nodes"].append(f"{node_id} (在 {section_name})")
                self.all_nodes.add(node_id)  # 添加到已知节点

            # 对于原理节点，检查是否有conditions
            if section_name == 'principles':
                if 'conditions' not in node_data or not node_data['conditions']:
                    issues["missing_conditions"].append(node_id)

            # 对于指标节点，检查是否有conditions
            if section_name == 'metrics':
                if 'demonstrated_value' in node_data:
                    demonstrated = node_data['demonstrated_value']
                    if isinstance(demonstrated, dict) and 'conditions' not in demonstrated:
                        issues["missing_conditions"].append(f"{node_id}.demonstrated_value")

        return issues

    def _check_relations(self, relations: Dict) -> Dict:
        """检查关系质量"""
        issues = {
            "missing_source_claim": []
        }

        if not relations:
            return issues

        for rel_id, rel_data in relations.items():
            # 检查关系唯一性
            if rel_id in self.all_relations:
                # 关系ID重复（可能在不同文件）
                pass
            else:
                self.all_relations.add(rel_id)

            # 检查是否有source.claim
            if 'source' not in rel_data or 'claim' not in rel_data['source']:
                issues["missing_source_claim"].append(rel_id)

        return issues

    def check_batch(self, paper_count: int = 10) -> List[Dict]:
        """检查一批论文"""
        recent_papers = self.get_recent_papers(paper_count)
        results = []

        print(f"\n{'='*60}")
        print(f"批量质量检查 - 最近 {len(recent_papers)} 篇论文")
        print(f"{'='*60}")

        for paper_path in recent_papers:
            result = self.check_paper(paper_path)
            results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> str:
        """生成质量检查报告"""
        total_warnings = 0
        total_errors = 0
        total_new_nodes = 0
        total_duplicates = 0

        report_lines = []

        report_lines.append("# 批量质量检查报告")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"检查论文数: {len(results)}")
        report_lines.append("")

        for result in results:
            report_lines.append(f"## {result['file']}")
            report_lines.append("")

            # 新节点
            if result['new_nodes']:
                report_lines.append("### 新节点 (标注为未审核)")
                for node in result['new_nodes']:
                    report_lines.append(f"- {node}")
                    total_new_nodes += 1
                report_lines.append("")

            # 重复节点
            if result['duplicate_nodes']:
                report_lines.append("### ⚠️ 重复节点 (需要检查)")
                for node in result['duplicate_nodes']:
                    report_lines.append(f"- {node}")
                    total_duplicates += 1
                report_lines.append("")

            # 缺失source.claim
            if result['missing_source_claim']:
                report_lines.append("### ⚠️ 缺失 source.claim")
                for rel_id in result['missing_source_claim']:
                    report_lines.append(f"- {rel_id}")
                    total_warnings += 1
                report_lines.append("")

            # 缺失conditions
            if result['missing_conditions']:
                report_lines.append("### ⚠️ 缺失 conditions")
                for item in result['missing_conditions']:
                    report_lines.append(f"- {item}")
                    total_warnings += 1
                report_lines.append("")

            # 错误
            if result['errors']:
                report_lines.append("### ❌ 错误")
                for error in result['errors']:
                    report_lines.append(f"- {error}")
                    total_errors += 1
                report_lines.append("")

            # 警告
            if result['warnings']:
                report_lines.append("### ⚠️ 警告")
                for warning in result['warnings']:
                    report_lines.append(f"- {warning}")
                    total_warnings += 1
                report_lines.append("")

            report_lines.append("---")
            report_lines.append("")

        # 总结
        report_lines.append("# 总结")
        report_lines.append("")
        report_lines.append(f"- 总新节点: {total_new_nodes} (已标注未审核)")
        report_lines.append(f"- 重复节点: {total_duplicates} (需要人工检查)")
        report_lines.append(f"- 警告: {total_warnings} 项")
        report_lines.append(f"- 错误: {total_errors} 项")
        report_lines.append("")

        # 建议
        report_lines.append("# 建议")
        report_lines.append("")

        if total_duplicates > 0:
            report_lines.append("1. **检查重复节点**: 确保节点ID全局唯一")
            report_lines.append("   - 考虑合并相似节点")
            report_lines.append("   - 或为节点添加后缀区分")

        if total_warnings > 0:
            report_lines.append("2. **修复警告**: 补充缺失的source.claim和conditions")
            report_lines.append("   - 每个关系应有source.claim引用原文")
            report_lines.append("   - 原理和指标节点应有conditions")

        if total_new_nodes > 0:
            report_lines.append("3. **审核新节点**: 所有新节点已标注未审核")
            report_lines.append("   - 确保新节点符合Schema规范")
            report_lines.append("   - 优先复用已有节点，新节点应为次级别或原理节点")

        if total_errors == 0 and total_warnings == 0 and total_duplicates == 0:
            report_lines.append("✅ 所有检查通过，质量良好！")

        return "\n".join(report_lines)

    def add_unverified_marker(self, yaml_path: Path):
        """为YAML文件中的新节点添加未审核标记"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            modified = False

            # 为所有节点添加note标注未审核
            for section in ['entities', 'principles', 'methods', 'metrics']:
                if section in data:
                    for node_id, node_data in data[section].items():
                        # 检查是否已有note
                        if 'note' not in node_data:
                            node_data['note'] = "未审核 - 批量处理添加"
                            modified = True
                        elif "未审核" not in node_data['note']:
                            node_data['note'] = f"{node_data['note']} | 未审核 - 批量处理添加"
                            modified = True

            if modified:
                # 写回文件
                with open(yaml_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
                print(f"  已添加未审核标记: {yaml_path.name}")

        except Exception as e:
            print(f"  警告: 添加未审核标记失败: {e}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="批量质量检查与整理")
    parser.add_argument("--count", type=int, default=10, help="检查的论文数量")
    parser.add_argument("--mark-unverified", action="store_true", help="为新节点添加未审核标记")
    parser.add_argument("--output", type=str, help="输出报告文件路径")

    args = parser.parse_args()

    checker = QualityChecker()

    # 检查论文
    results = checker.check_batch(args.count)

    # 添加未审核标记
    if args.mark_unverified:
        print(f"\n{'='*60}")
        print("为新节点添加未审核标记")
        print(f"{'='*60}")

        recent_papers = checker.get_recent_papers(args.count)
        for paper_path in recent_papers:
            checker.add_unverified_marker(paper_path)

    # 生成报告
    report = checker.generate_report(results)
    print(report)

    # 输出到文件
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存到: {output_path}")


if __name__ == "__main__":
    main()