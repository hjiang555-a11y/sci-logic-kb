#!/usr/bin/env python3
"""
执行Zotero数据库清理：
1. 删除完全损坏的条目
2. 合并重复条目
3. 尝试为缺失DOI的条目查找DOI（占位符，实际需要网络搜索）
"""

import sqlite3
import re
import sys
import json
from collections import defaultdict
from urllib.request import urlopen, Request
from urllib.parse import quote
from difflib import SequenceMatcher

DB_PATH = "/mnt/d/Users/hjian/Zotero/zotero.sqlite"

def connect_db():
    """连接Zotero数据库"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # 启用外键约束
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"数据库连接失败: {e}")
        sys.exit(1)

def get_queue_keys():
    """从QUEUE.md获取Zotero keys"""
    try:
        with open("/home/hjian/sci-logic-kb/QUEUE.md", "r", encoding="utf-8") as f:
            content = f.read()
        keys = re.findall(r'`([A-Z0-9]{8})`', content)
        return set(keys)
    except Exception as e:
        print(f"读取QUEUE.md失败: {e}")
        return set()

def get_item_key(conn, item_id):
    """根据itemID获取条目的key"""
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM items WHERE itemID = ?", (item_id,))
    row = cursor.fetchone()
    return row['key'] if row else None

def get_item_details(conn, item_id):
    """获取条目的详细信息"""
    cursor = conn.cursor()

    # 获取字段映射
    cursor.execute("SELECT fieldID, fieldName FROM fields")
    field_map = {row['fieldID']: row['fieldName'] for row in cursor.fetchall()}

    # 查询条目的数据
    query = """
    SELECT id.fieldID, idv.value
    FROM itemData id
    LEFT JOIN itemDataValues idv ON id.valueID = idv.valueID
    WHERE id.itemID = ?
    """
    cursor.execute(query, (item_id,))
    data = cursor.fetchall()

    details = {'itemID': item_id}
    for row in data:
        field_id = row['fieldID']
        value = row['value']
        if value:
            field_name = field_map.get(field_id, f"field_{field_id}")
            details[field_name] = value

    # 获取作者信息
    authors = []
    author_query = """
    SELECT ia.firstName, ia.lastName, ia.fieldMode
    FROM itemCreators ic
    JOIN creators ia ON ic.creatorID = ia.creatorID
    WHERE ic.itemID = ?
    ORDER BY ic.orderIndex
    """
    cursor.execute(author_query, (item_id,))
    author_rows = cursor.fetchall()
    for author in author_rows:
        if author['fieldMode'] == 1:
            authors.append(author['lastName'] or '')
        else:
            name = ""
            if author['firstName']:
                name += author['firstName'] + " "
            if author['lastName']:
                name += author['lastName']
            authors.append(name.strip())

    if authors:
        details['authors'] = authors

    # 获取附件数量
    attachment_query = """
    SELECT COUNT(*) as count FROM itemAttachments WHERE parentItemID = ?
    """
    cursor.execute(attachment_query, (item_id,))
    attachments_count = cursor.fetchone()['count']
    details['attachments_count'] = attachments_count

    # 获取条目的key
    details['key'] = get_item_key(conn, item_id)

    return details

def normalize_title(title):
    """规范化标题以便比较"""
    if not title:
        return ""
    title = title.lower()
    title = re.sub(r'[^\w\s]', ' ', title)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    words = [word for word in title.split() if word not in stop_words]
    return ' '.join(words)

def find_duplicates(conn):
    """查找所有重复条目"""
    cursor = conn.cursor()

    # 获取所有文献条目
    query = """
    SELECT i.itemID, i.key, it.typeName
    FROM items i
    JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
    WHERE it.typeName IN ('journalArticle', 'conferencePaper', 'thesis', 'bookSection', 'preprint')
    """
    cursor.execute(query)
    items = cursor.fetchall()

    # 获取每个条目的详细信息
    items_details = {}
    for item in items:
        item_id = item['itemID']
        details = get_item_details(conn, item_id)
        items_details[item_id] = details

    # 按规范化标题分组
    title_groups = defaultdict(list)
    for item_id, details in items_details.items():
        title = details.get('title', '')
        if title:
            norm_title = normalize_title(title)
            if norm_title:
                title_groups[norm_title].append(item_id)

    # 按DOI分组
    doi_groups = defaultdict(list)
    for item_id, details in items_details.items():
        doi = details.get('DOI', '')
        if doi:
            doi_groups[doi.lower()].append(item_id)

    # 收集重复组
    duplicate_groups = []

    # 基于标题的重复
    for norm_title, ids in title_groups.items():
        if len(ids) > 1:
            # 检查标题相似性
            titles = [items_details[item_id].get('title', '') for item_id in ids]
            similar = True
            for i in range(len(titles)-1):
                ratio = SequenceMatcher(None, titles[i].lower(), titles[i+1].lower()).ratio()
                if ratio < 0.8:
                    similar = False
                    break
            if similar:
                duplicate_groups.append(ids)

    # 基于DOI的重复
    for doi, ids in doi_groups.items():
        if len(ids) > 1:
            # 确保这组不在已添加的组中
            ids_set = set(ids)
            already_included = False
            for existing_group in duplicate_groups:
                if ids_set.issubset(set(existing_group)):
                    already_included = True
                    break
            if not already_included:
                duplicate_groups.append(ids)

    # 去重：移除包含关系的组
    final_groups = []
    for i, group1 in enumerate(duplicate_groups):
        subset = False
        for j, group2 in enumerate(duplicate_groups):
            if i != j and set(group1).issubset(set(group2)):
                subset = True
                break
        if not subset:
            final_groups.append(group1)

    return final_groups, items_details

def score_item(details, queue_keys):
    """为条目评分，分数越高越应该保留"""
    score = 0

    # 检查是否在QUEUE.md中
    if details.get('key') in queue_keys:
        score += 1000

    # 信息完整性
    if details.get('title'):
        score += 100
    if details.get('DOI'):
        score += 80
    if details.get('date'):
        score += 60
    if details.get('authors'):
        score += 40

    # 附件数量
    score += details.get('attachments_count', 0) * 20

    # 字段数量（粗略估计完整性）
    field_count = len([k for k in details.keys() if k not in ['itemID', 'key', 'attachments_count', 'authors']])
    score += field_count * 5

    return score

def delete_item(conn, item_id):
    """删除条目及其相关数据"""
    cursor = conn.cursor()

    print(f"  删除条目 {item_id}...")

    try:
        # 先删除itemData（通过valueID引用itemDataValues）
        cursor.execute("DELETE FROM itemData WHERE itemID = ?", (item_id,))

        # 删除itemCreators
        cursor.execute("DELETE FROM itemCreators WHERE itemID = ?", (item_id,))

        # 删除itemTags
        cursor.execute("DELETE FROM itemTags WHERE itemID = ?", (item_id,))

        # 删除itemNotes
        cursor.execute("DELETE FROM itemNotes WHERE itemID = ?", (item_id,))

        # 删除itemAttachments（级联删除？先手动删除）
        cursor.execute("DELETE FROM itemAttachments WHERE parentItemID = ?", (item_id,))

        # 删除items表中的条目
        cursor.execute("DELETE FROM items WHERE itemID = ?", (item_id,))

        # 注意：itemDataValues可能被其他条目共享，不应删除
        # creators表可能被其他条目共享，不应删除

        return True
    except sqlite3.Error as e:
        print(f"  删除条目 {item_id} 失败: {e}")
        return False

def delete_corrupted_items(conn):
    """删除完全损坏的条目（无标题、DOI、年份、作者）"""
    cursor = conn.cursor()

    print("=== 删除损坏条目 ===")

    # 查找损坏条目
    query = """
    SELECT i.itemID
    FROM items i
    JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
    WHERE it.typeName IN ('journalArticle', 'conferencePaper', 'thesis', 'bookSection', 'preprint')
    AND i.itemID NOT IN (
        SELECT id.itemID
        FROM itemData id
        JOIN itemDataValues idv ON id.valueID = idv.valueID
        JOIN fields f ON id.fieldID = f.fieldID
        WHERE f.fieldName IN ('title', 'DOI', 'date')
        AND idv.value IS NOT NULL AND idv.value != ''
    )
    AND i.itemID NOT IN (
        SELECT ic.itemID FROM itemCreators ic
    )
    """
    cursor.execute(query)
    corrupted_items = cursor.fetchall()

    print(f"找到 {len(corrupted_items)} 个损坏条目")

    deleted_count = 0
    for row in corrupted_items:
        item_id = row['itemID']

        # 获取条目的key
        key = get_item_key(conn, item_id)
        print(f"  条目ID: {item_id}, Key: {key}")

        # 检查是否有附件
        cursor.execute("SELECT COUNT(*) as count FROM itemAttachments WHERE parentItemID = ?", (item_id,))
        attachments_count = cursor.fetchone()['count']

        if attachments_count == 0:
            if delete_item(conn, item_id):
                deleted_count += 1
        else:
            print(f"  警告：条目 {item_id} 有 {attachments_count} 个附件，跳过删除")

    conn.commit()
    print(f"已删除 {deleted_count} 个损坏条目")
    return deleted_count

def merge_duplicates(conn, queue_keys):
    """合并重复条目"""
    print("\n=== 合并重复条目 ===")

    duplicate_groups, items_details = find_duplicates(conn)
    print(f"发现 {len(duplicate_groups)} 组重复条目")

    deleted_count = 0
    for group_idx, group in enumerate(duplicate_groups, 1):
        print(f"\n处理第 {group_idx} 组: {group}")

        # 为组内每个条目评分
        scored_items = []
        for item_id in group:
            details = items_details.get(item_id)
            if details:
                score = score_item(details, queue_keys)
                scored_items.append((item_id, score, details))

        # 按分数排序，分数最高的保留
        scored_items.sort(key=lambda x: x[1], reverse=True)

        print(f"  评分结果:")
        for i, (item_id, score, details) in enumerate(scored_items):
            title = details.get('title', 'N/A')[:40]
            doi = details.get('DOI', 'N/A')
            in_queue = "✓" if details.get('key') in queue_keys else "✗"
            print(f"    [{i+1}] 条目ID: {item_id}, 分数: {score}, 标题: {title}..., DOI: {doi}, 在队列中: {in_queue}")

        # 保留分数最高的，删除其他的
        if len(scored_items) > 1:
            keep_item_id = scored_items[0][0]
            print(f"  保留条目: {keep_item_id}")

            for item_id, score, details in scored_items[1:]:
                # 再次确认不要删除在队列中的条目
                if details.get('key') in queue_keys:
                    print(f"  警告：条目 {item_id} 在队列中，跳过删除")
                    continue

                if delete_item(conn, item_id):
                    deleted_count += 1

    conn.commit()
    print(f"\n已删除 {deleted_count} 个重复条目")
    return deleted_count

def try_find_missing_dois(conn):
    """尝试为缺失DOI的条目查找DOI（占位符）"""
    print("\n=== 查找缺失DOI ===")
    print("注意：此功能需要实现网络搜索，目前仅为占位符")

    cursor = conn.cursor()

    # 查找有标题但无DOI的条目
    query = """
    SELECT DISTINCT i.itemID, i.key
    FROM items i
    JOIN itemData id ON i.itemID = id.itemID
    JOIN itemDataValues idv ON id.valueID = idv.valueID
    JOIN fields f ON id.fieldID = f.fieldID
    WHERE f.fieldName = 'title'
    AND idv.value IS NOT NULL AND idv.value != ''
    AND i.itemID NOT IN (
        SELECT id2.itemID
        FROM itemData id2
        JOIN itemDataValues idv2 ON id2.valueID = idv2.valueID
        JOIN fields f2 ON id2.fieldID = f2.fieldID
        WHERE f2.fieldName = 'DOI'
        AND idv2.value IS NOT NULL AND idv2.value != ''
    )
    LIMIT 10
    """
    cursor.execute(query)
    missing_doi_items = cursor.fetchall()

    print(f"发现 {len(missing_doi_items)} 个有标题但无DOI的条目（显示前10个）")

    for row in missing_doi_items:
        item_id = row['itemID']
        key = row['key']

        # 获取标题
        cursor.execute("""
        SELECT idv.value
        FROM itemData id
        JOIN itemDataValues idv ON id.valueID = idv.valueID
        JOIN fields f ON id.fieldID = f.fieldID
        WHERE f.fieldName = 'title' AND id.itemID = ?
        """, (item_id,))
        title_row = cursor.fetchone()
        title = title_row['value'] if title_row else 'N/A'

        print(f"  条目ID: {item_id}, Key: {key}")
        print(f"    标题: {title[:60]}...")
        print(f"    建议：可通过Crossref API或Google Scholar搜索DOI")

    return len(missing_doi_items)

def main():
    print("=== 执行Zotero数据库清理 ===")
    print("注意：此操作将修改数据库，请确保已备份")

    # 获取QUEUE.md中的keys
    queue_keys = get_queue_keys()
    print(f"QUEUE.md中有 {len(queue_keys)} 个条目")

    conn = connect_db()

    try:
        # 1. 删除损坏条目
        deleted_corrupted = delete_corrupted_items(conn)

        # 2. 合并重复条目
        deleted_duplicates = merge_duplicates(conn, queue_keys)

        # 3. 尝试查找缺失DOI（占位符）
        missing_doi_count = try_find_missing_dois(conn)

        print("\n=== 清理完成 ===")
        print(f"删除损坏条目: {deleted_corrupted}")
        print(f"删除重复条目: {deleted_duplicates}")
        print(f"需要查找DOI的条目: {missing_doi_count}")

        # 验证清理后数据库状态
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM items")
        total_items = cursor.fetchone()['count']
        print(f"数据库当前总条目数: {total_items}")

    except Exception as e:
        print(f"清理过程中出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()