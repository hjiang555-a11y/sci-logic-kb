#!/usr/bin/env python3
"""
批量质量检查与整理脚本

功能：
1. 检查最近处理的N篇论文YAML文件
2. 验证节点唯一性、关系完整性
3. 整理节点，避免重复，优先复用已有节点
4. 标注新开节点为未审核
5. 生成质量报告

遵循 Schema v4.0 要求：
- 全局唯一ID
- 关系有source.claim
- 指标有conditions
- 原理节点有conditions/preconditions
"""

import yaml
from pathlib import Path
from typing import Iterable, List, Dict, Set, Tuple
from datetime import datetime


class QualityChecker:
    """质量检查器"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.schema_path = self.repo_path / "SCHEMA.md"

        # 存储所有已知节点/关系及其出现位置（用于检查唯一性）
        self.node_locations: Dict[str, Set[str]] = {}
        self.relation_locations: Dict[str, Set[str]] = {}

        # 加载已有节点
        self._load_existing_nodes()

    def _yaml_files(self) -> List[Path]:
        """返回仓库中的所有论文 YAML 文件。"""
        topic_papers_dirs = list(self.repo_path.glob("topics/*/papers"))
        topic_files = sorted(self.repo_path.glob("topics/*/papers/*.yaml"))
        if topic_papers_dirs:
            return topic_files
        return sorted((self.repo_path / "papers").glob("*.yaml"))

    @staticmethod
    def _iter_collection_items(collection) -> Iterable[Tuple[str, Dict]]:
        """兼容 v3.x dict 结构和 v4.x list 结构。"""
        if isinstance(collection, dict):
            for item_id, item_data in collection.items():
                if isinstance(item_data, dict):
                    yield item_id, item_data
        elif isinstance(collection, list):
            for item_data in collection:
                if isinstance(item_data, dict) and item_data.get("id"):
                    yield item_data["id"], item_data

    def _load_existing_nodes(self):
        """加载所有已存在的节点"""
        yaml_files = self._yaml_files()

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if not isinstance(data, dict):
                    continue

                # 收集节点
                for section in ['entities', 'principles', 'methods', 'metrics']:
                    if section in data:
                        for node_id, _ in self._iter_collection_items(data[section]):
                            self.node_locations.setdefault(node_id, set()).add(str(yaml_file))

                # 收集关系
                if 'relations' in data:
                    for rel_id, _ in self._iter_collection_items(data['relations']):
                        self.relation_locations.setdefault(rel_id, set()).add(str(yaml_file))

            except Exception as e:
                print(f"警告: 加载 {yaml_file} 失败: {e}")

        print(f"已加载 {len(self.node_locations)} 个节点，{len(self.relation_locations)} 个关系")

    def get_recent_papers(self, count: int = 10) -> List[Path]:
        """获取最近修改的论文YAML文件"""
        yaml_files = self._yaml_files()

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

            if not isinstance(data, dict):
                issues["errors"].append("YAML 根节点不是字典结构")
                return issues

            # 检查必需字段
            if 'paper' not in data and 'meta' not in data:
                issues["errors"].append("缺少 'paper' 或 'meta' 部分")
                return issues

            paper_info = data.get('paper') or data.get('meta') or {}
            paper_title = paper_info.get('title', '未知')

            print(f"\n检查: {paper_title}")
            print(f"文件: {yaml_path.name}")

            # 检查各个部分
            for section_name, section_data in data.items():
                if section_name == 'paper':
                    continue

                if section_name in ['entities', 'principles', 'methods', 'metrics']:
                    section_issues = self._check_nodes(section_name, section_data, yaml_path.name)
                    for key, values in section_issues.items():
                        issues[key].extend(values)
                elif section_name == 'relations':
                    relation_issues = self._check_relations(section_data, yaml_path.name)
                    for key, values in relation_issues.items():
                        issues[key].extend(values)

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

        source_name = Path(source_file).name

        for node_id, node_data in self._iter_collection_items(nodes):
            # 检查节点唯一性（仅跨文件重复时告警）
            locations = self.node_locations.get(node_id, set())
            other_locations = {loc for loc in locations if Path(loc).name != source_name}
            if other_locations:
                issues["duplicate_nodes"].append(f"{node_id} (在 {section_name}；另见 {', '.join(sorted(Path(loc).name for loc in other_locations))})")

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

    def _check_relations(self, relations: Dict, source_file: str) -> Dict:
        """检查关系质量"""
        issues = {
            "warnings": [],
            "missing_source_claim": []
        }

        if not relations:
            return issues

        source_name = Path(source_file).name

        for rel_id, rel_data in self._iter_collection_items(relations):
            locations = self.relation_locations.get(rel_id, set())
            other_locations = {loc for loc in locations if Path(loc).name != source_name}
            if other_locations:
                issues["warnings"].append(f"关系ID重复: {rel_id}（另见 {', '.join(sorted(Path(loc).name for loc in other_locations))}）")

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
                    for _, node_data in self._iter_collection_items(data[section]):
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
