#!/usr/bin/env python3
"""
分析 sci-logic-kb 知识库中的节点和关系统计
"""
import yaml
import os
import sys
from collections import defaultdict

def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def analyze_papers(papers_dir):
    total = {
        'entities': 0,
        'principles': 0,
        'methods': 0,
        'metrics': 0,
        'relations': 0,
        'files': 0
    }

    node_ids = defaultdict(list)  # id -> [file]
    relation_ids = defaultdict(list)

    for filename in os.listdir(papers_dir):
        if not filename.endswith('.yaml'):
            continue

        filepath = os.path.join(papers_dir, filename)
        try:
            data = load_yaml(filepath)
            total['files'] += 1

            # 统计节点
            for key in ['entities', 'principles', 'methods', 'metrics']:
                if key in data:
                    items = data[key]
                    if items is None:
                        continue
                    total[key] += len(items)
                    for item in items:
                        if 'id' in item:
                            node_ids[item['id']].append(filename)

            # 统计关系
            if 'relations' in data and data['relations']:
                rels = data['relations']
                total['relations'] += len(rels)
                for rel in rels:
                    if 'id' in rel:
                        relation_ids[rel['id']].append(filename)

        except Exception as e:
            print(f"警告: 解析 {filename} 时出错: {e}", file=sys.stderr)

    # 检查重复ID
    duplicate_nodes = {id: files for id, files in node_ids.items() if len(files) > 1}
    duplicate_relations = {id: files for id, files in relation_ids.items() if len(files) > 1}

    return total, node_ids, relation_ids, duplicate_nodes, duplicate_relations

def main():
    # Support both old and new directory structures
    papers_dir = 'topics/ultrastable-laser/papers'
    if not os.path.exists(papers_dir):
        papers_dir = 'papers'
    if not os.path.exists(papers_dir):
        print(f"错误: 目录 {papers_dir} 不存在")
        sys.exit(1)

    total, node_ids, relation_ids, dup_nodes, dup_rels = analyze_papers(papers_dir)

    print("=" * 60)
    print("sci-logic-kb 知识库统计报告")
    print("=" * 60)
    print(f"论文文件数: {total['files']}")
    print(f"实体节点 (ent.*): {total['entities']}")
    print(f"原理节点 (pri.*): {total['principles']}")
    print(f"方法节点 (meth.*): {total['methods']}")
    print(f"指标节点 (met.*): {total['metrics']}")
    print(f"关系边 (rel.*): {total['relations']}")
    print(f"唯一节点ID数: {len(node_ids)}")
    print(f"唯一关系ID数: {len(relation_ids)}")
    print()

    if dup_nodes:
        print("⚠️  重复的节点ID (跨文件定义):")
        for node_id, files in dup_nodes.items():
            print(f"  {node_id}: {', '.join(files)}")
    else:
        print("✅ 所有节点ID全局唯一")

    if dup_rels:
        print("⚠️  重复的关系ID:")
        for rel_id, files in dup_rels.items():
            print(f"  {rel_id}: {', '.join(files)}")
    else:
        print("✅ 所有关系ID全局唯一")

    # 按前缀分类统计节点
    prefix_counts = defaultdict(int)
    for node_id in node_ids.keys():
        if '.' in node_id:
            prefix = node_id.split('.')[0]
            prefix_counts[prefix] += 1

    print()
    print("节点类型分布:")
    for prefix in ['ent', 'pri', 'meth', 'met', 'src']:
        count = prefix_counts.get(prefix, 0)
        print(f"  {prefix}.*: {count}")

    # 检查是否有孤立的节点（无关系引用）
    # 简单检查：统计出现在关系 subject/object 中的节点
    referenced_nodes = set()
    # 需要重新遍历来收集引用信息
    for filename in os.listdir(papers_dir):
        if not filename.endswith('.yaml'):
            continue
        filepath = os.path.join(papers_dir, filename)
        try:
            data = load_yaml(filepath)
            if 'relations' in data and data['relations']:
                for rel in data['relations']:
                    if 'subject' in rel:
                        referenced_nodes.add(rel['subject'])
                    if 'object' in rel:
                        referenced_nodes.add(rel['object'])
        except:
            pass

    isolated = set(node_ids.keys()) - referenced_nodes
    if isolated:
        print(f"\n⚠️  有 {len(isolated)} 个节点未被任何关系引用（可能孤立）:")
        for node in sorted(isolated)[:10]:  # 只显示前10个
            print(f"  {node}")
        if len(isolated) > 10:
            print(f"  ... 还有 {len(isolated)-10} 个")
    else:
        print("\n✅ 所有节点都有至少一个关系引用")

    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()