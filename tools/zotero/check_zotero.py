#!/usr/bin/env python3
"""
检查Zotero数据库，识别重复论文并补全缺失信息
"""

import sqlite3
import sys
import re
from collections import defaultdict

# Zotero数据库路径
DB_PATH = "/mnt/d/Users/hjian/Zotero/zotero.sqlite"

def connect_db():
    """连接Zotero数据库"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"数据库连接失败: {e}")
        sys.exit(1)

def get_table_info(conn):
    """获取数据库表结构信息"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("数据库表:")
    for table in tables:
        print(f"  {table[0]}")
    return [t[0] for t in tables]

def query_items(conn):
    """查询所有论文条目"""
    cursor = conn.cursor()

    # 查询items表中类型为journalArticle的条目
    query = """
    SELECT
        i.itemID, i.key, i.itemTypeID, it.typeName,
        i.dateAdded, i.dateModified
    FROM items i
    JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
    WHERE it.typeName IN ('journalArticle', 'conferencePaper', 'thesis', 'bookSection', 'preprint')
    ORDER BY i.dateAdded DESC
    """

    cursor.execute(query)
    items = cursor.fetchall()
    print(f"找到 {len(items)} 个文献条目")
    return items

def get_item_details(conn, item_id):
    """获取条目的详细信息（标题、作者、DOI、年份等）"""
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

    details = {}
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
            # 公司/机构作者
            authors.append(author['lastName'] or '')
        else:
            # 个人作者
            name = ""
            if author['firstName']:
                name += author['firstName'] + " "
            if author['lastName']:
                name += author['lastName']
            authors.append(name.strip())

    if authors:
        details['authors'] = authors

    return details

def find_duplicates(items_details):
    """基于标题和DOI查找重复条目"""
    title_map = defaultdict(list)
    doi_map = defaultdict(list)

    for item_id, details in items_details.items():
        title = details.get('title', '').lower().strip()
        doi = details.get('DOI', '')

        if title:
            title_map[title].append(item_id)
        if doi:
            doi_map[doi.lower()].append(item_id)

    duplicates = []

    # 基于标题的重复
    for title, ids in title_map.items():
        if len(ids) > 1:
            duplicates.append(('title', title, ids))

    # 基于DOI的重复
    for doi, ids in doi_map.items():
        if len(ids) > 1:
            duplicates.append(('DOI', doi, ids))

    return duplicates

def print_item_details(details):
    """打印条目详情"""
    print(f"  标题: {details.get('title', 'N/A')}")
    print(f"  作者: {', '.join(details.get('authors', ['N/A']))}")
    print(f"  年份: {details.get('date', 'N/A')}")
    print(f"  期刊: {details.get('publicationTitle', 'N/A')}")
    print(f"  DOI: {details.get('DOI', 'N/A')}")
    print(f"  URL: {details.get('url', 'N/A')}")
    print(f"  卷: {details.get('volume', 'N/A')}")
    print(f"  期: {details.get('issue', 'N/A')}")
    print(f"  页码: {details.get('pages', 'N/A')}")

def main():
    print("=== Zotero数据库检查 ===")

    conn = connect_db()

    # 获取表信息
    tables = get_table_info(conn)

    # 查询所有论文条目
    items = query_items(conn)

    # 获取每个条目的详细信息
    items_details = {}
    print("\n=== 文献条目详情 ===")
    for item in items[:20]:  # 先看前20个
        item_id = item['itemID']
        key = item['key']
        type_name = item['typeName']

        print(f"\n[{key}] {type_name}:")
        details = get_item_details(conn, item_id)
        items_details[item_id] = details
        print_item_details(details)

    # 查找重复
    duplicates = find_duplicates(items_details)

    print("\n=== 重复条目 ===")
    if duplicates:
        for dup_type, value, ids in duplicates:
            print(f"\n基于{dup_type}的重复: {value}")
            for item_id in ids:
                details = items_details[item_id]
                print(f"  - 条目ID: {item_id}, 标题: {details.get('title', 'N/A')[:50]}...")
    else:
        print("未发现重复条目")

    # 检查缺失信息
    print("\n=== 缺失重要信息的条目 ===")
    missing_info = []
    for item_id, details in items_details.items():
        missing = []
        if 'title' not in details:
            missing.append('标题')
        if 'DOI' not in details:
            missing.append('DOI')
        if 'date' not in details:
            missing.append('年份')
        if 'authors' not in details:
            missing.append('作者')

        if missing:
            missing_info.append((item_id, details, missing))

    for item_id, details, missing in missing_info[:10]:  # 最多显示10个
        print(f"\n条目ID: {item_id}")
        print(f"  标题: {details.get('title', 'N/A')[:50]}...")
        print(f"  缺失: {', '.join(missing)}")

    # 与QUEUE.md对比
    print("\n=== 与QUEUE.md对比 ===")
    with open("/home/hjian/sci-logic-kb/QUEUE.md", "r", encoding="utf-8") as f:
        queue_content = f.read()

    # 提取QUEUE.md中的Zotero keys
    queue_keys = re.findall(r'`([A-Z0-9]{8})`', queue_content)
    print(f"QUEUE.md中包含 {len(queue_keys)} 个Zotero key")
    print(f"示例: {queue_keys[:5]}")

    # 检查哪些key在数据库中
    cursor = conn.cursor()
    found_keys = []
    missing_keys = []

    for key in queue_keys:
        cursor.execute("SELECT key FROM items WHERE key = ?", (key,))
        if cursor.fetchone():
            found_keys.append(key)
        else:
            missing_keys.append(key)

    print(f"\n数据库中存在的key: {len(found_keys)}/{len(queue_keys)}")
    print(f"数据库中缺失的key: {len(missing_keys)}/{len(queue_keys)}")
    if missing_keys:
        print(f"缺失的key: {missing_keys[:10]}")

    conn.close()

if __name__ == "__main__":
    main()