#!/usr/bin/env python3
"""
补全Zotero条目信息：
1. 通过DOI获取缺失的年份
2. 尝试为缺失DOI的条目查找DOI
"""

import sqlite3
import json
import re
import sys
import time
from urllib.request import urlopen, Request
from urllib.parse import quote, urlencode
from urllib.error import HTTPError, URLError

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

def fetch_doi_metadata(doi):
    """通过Crossref API获取DOI的元数据"""
    if not doi:
        return None

    try:
        url = f"https://api.crossref.org/works/{quote(doi)}"
        headers = {'User-Agent': 'ZoteroCleaner/1.0 (mailto:example@example.com)'}
        req = Request(url, headers=headers)

        with urlopen(req, timeout=10) as response:
            data = json.load(response)
            if data['status'] == 'ok':
                return data['message']
    except HTTPError as e:
        if e.code == 404:
            print(f"  DOI未找到: {doi}")
        else:
            print(f"  HTTP错误 {e.code} 获取DOI {doi}: {e.reason}")
    except Exception as e:
        print(f"  获取DOI {doi} 元数据失败: {e}")

    return None

def search_doi_by_title(title, author=None):
    """通过标题搜索DOI"""
    if not title or len(title) < 10:
        return None

    try:
        # Crossref搜索API
        query_params = {'query.bibliographic': title, 'rows': 1}
        if author:
            query_params['query.author'] = author

        url = f"https://api.crossref.org/works?{urlencode(query_params)}"
        headers = {'User-Agent': 'ZoteroCleaner/1.0 (mailto:example@example.com)'}
        req = Request(url, headers=headers)

        with urlopen(req, timeout=10) as response:
            data = json.load(response)
            if data['status'] == 'ok' and data['message']['total-results'] > 0:
                item = data['message']['items'][0]
                return item.get('DOI')
    except Exception as e:
        print(f"  搜索标题失败 '{title[:30]}...': {e}")

    return None

def extract_year_from_metadata(metadata):
    """从元数据中提取年份"""
    if not metadata:
        return None

    # 尝试从published字段提取
    published = metadata.get('published', {})
    if published.get('date-parts'):
        date_parts = published['date-parts'][0]
        if date_parts and len(date_parts) > 0:
            return str(date_parts[0])

    # 尝试其他字段
    year = metadata.get('published-year') or metadata.get('year') or metadata.get('issued-year')
    if year:
        return str(year)

    # 尝试从created字段提取
    created = metadata.get('created', {})
    if created.get('date-parts'):
        date_parts = created['date-parts'][0]
        if date_parts and len(date_parts) > 0:
            return str(date_parts[0])

    return None

def update_item_year(conn, item_id, year):
    """更新条目的年份"""
    cursor = conn.cursor()

    # 查找date字段的fieldID
    cursor.execute("SELECT fieldID FROM fields WHERE fieldName = 'date'")
    field_row = cursor.fetchone()
    if not field_row:
        print(f"  错误：未找到date字段")
        return False

    field_id = field_row['fieldID']

    # 检查是否已存在date字段
    cursor.execute("""
    SELECT id.valueID FROM itemData id
    WHERE id.itemID = ? AND id.fieldID = ?
    """, (item_id, field_id))

    value_row = cursor.fetchone()

    # 检查是否已存在相同值的记录
    cursor.execute("SELECT valueID FROM itemDataValues WHERE value = ?", (year,))
    existing_value_row = cursor.fetchone()

    if existing_value_row:
        # 重用现有的valueID
        value_id = existing_value_row['valueID']
        if value_row:
            # 更新现有关联
            cursor.execute("UPDATE itemData SET valueID = ? WHERE itemID = ? AND fieldID = ?",
                          (value_id, item_id, field_id))
        else:
            # 创建新关联
            cursor.execute("INSERT INTO itemData (itemID, fieldID, valueID) VALUES (?, ?, ?)",
                          (item_id, field_id, value_id))
    else:
        # 需要创建新值
        if value_row:
            value_id = value_row['valueID']
            cursor.execute("UPDATE itemDataValues SET value = ? WHERE valueID = ?", (year, value_id))
        else:
            # 插入新值
            cursor.execute("INSERT INTO itemDataValues (value) VALUES (?)", (year,))
            value_id = cursor.lastrowid
            cursor.execute("INSERT INTO itemData (itemID, fieldID, valueID) VALUES (?, ?, ?)",
                          (item_id, field_id, value_id))

    print(f"  更新条目 {item_id} 年份为: {year}")
    return True

def update_item_doi(conn, item_id, doi):
    """更新条目的DOI"""
    cursor = conn.cursor()

    # 查找DOI字段的fieldID
    cursor.execute("SELECT fieldID FROM fields WHERE fieldName = 'DOI'")
    field_row = cursor.fetchone()
    if not field_row:
        print(f"  错误：未找到DOI字段")
        return False

    field_id = field_row['fieldID']

    # 检查是否已存在DOI字段
    cursor.execute("""
    SELECT id.valueID FROM itemData id
    WHERE id.itemID = ? AND id.fieldID = ?
    """, (item_id, field_id))

    value_row = cursor.fetchone()

    # 检查是否已存在相同值的记录
    cursor.execute("SELECT valueID FROM itemDataValues WHERE value = ?", (doi,))
    existing_value_row = cursor.fetchone()

    if existing_value_row:
        # 重用现有的valueID
        value_id = existing_value_row['valueID']
        if value_row:
            # 更新现有关联
            cursor.execute("UPDATE itemData SET valueID = ? WHERE itemID = ? AND fieldID = ?",
                          (value_id, item_id, field_id))
        else:
            # 创建新关联
            cursor.execute("INSERT INTO itemData (itemID, fieldID, valueID) VALUES (?, ?, ?)",
                          (item_id, field_id, value_id))
    else:
        # 需要创建新值
        if value_row:
            value_id = value_row['valueID']
            cursor.execute("UPDATE itemDataValues SET value = ? WHERE valueID = ?", (doi, value_id))
        else:
            # 插入新值
            cursor.execute("INSERT INTO itemDataValues (value) VALUES (?)", (doi,))
            value_id = cursor.lastrowid
            cursor.execute("INSERT INTO itemData (itemID, fieldID, valueID) VALUES (?, ?, ?)",
                          (item_id, field_id, value_id))

    print(f"  更新条目 {item_id} DOI为: {doi}")
    return True

def complete_missing_years(conn):
    """为有DOI但缺少年份的条目补全年份"""
    print("=== 补全缺失年份 ===")

    cursor = conn.cursor()

    # 查找有DOI但无年份的条目
    query = """
    SELECT DISTINCT i.itemID, i.key
    FROM items i
    JOIN itemData id ON i.itemID = id.itemID
    JOIN itemDataValues idv ON id.valueID = idv.valueID
    JOIN fields f ON id.fieldID = f.fieldID
    WHERE f.fieldName = 'DOI'
    AND idv.value IS NOT NULL AND idv.value != ''
    AND i.itemID NOT IN (
        SELECT id2.itemID
        FROM itemData id2
        JOIN itemDataValues idv2 ON id2.valueID = idv2.valueID
        JOIN fields f2 ON id2.fieldID = f2.fieldID
        WHERE f2.fieldName = 'date'
        AND idv2.value IS NOT NULL AND idv2.value != ''
    )
    """
    cursor.execute(query)
    missing_year_items = cursor.fetchall()

    print(f"发现 {len(missing_year_items)} 个有DOI但缺少年份的条目")

    updated_count = 0
    for row in missing_year_items:
        item_id = row['itemID']
        key = row['key']

        # 获取DOI
        cursor.execute("""
        SELECT idv.value
        FROM itemData id
        JOIN itemDataValues idv ON id.valueID = idv.valueID
        JOIN fields f ON id.fieldID = f.fieldID
        WHERE f.fieldName = 'DOI' AND id.itemID = ?
        """, (item_id,))
        doi_row = cursor.fetchone()
        if not doi_row:
            continue

        doi = doi_row['value']
        print(f"  条目ID: {item_id}, Key: {key}, DOI: {doi}")

        # 获取元数据
        metadata = fetch_doi_metadata(doi)
        if metadata:
            year = extract_year_from_metadata(metadata)
            if year:
                if update_item_year(conn, item_id, year):
                    updated_count += 1
            else:
                print(f"    未找到年份信息")
        else:
            print(f"    获取元数据失败")

        # 避免请求过快
        time.sleep(0.5)

    conn.commit()
    print(f"已更新 {updated_count} 个条目的年份")
    return updated_count

def complete_missing_dois(conn, limit=10):
    """为缺失DOI的条目尝试查找DOI"""
    print("\n=== 尝试查找缺失DOI ===")

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
    AND LENGTH(idv.value) > 10  -- 标题长度足够
    AND i.itemID NOT IN (
        SELECT id2.itemID
        FROM itemData id2
        JOIN itemDataValues idv2 ON id2.valueID = idv2.valueID
        JOIN fields f2 ON id2.fieldID = f2.fieldID
        WHERE f2.fieldName = 'DOI'
        AND idv2.value IS NOT NULL AND idv2.value != ''
    )
    LIMIT ?
    """
    cursor.execute(query, (limit,))
    missing_doi_items = cursor.fetchall()

    print(f"尝试为 {len(missing_doi_items)} 个条目查找DOI")

    updated_count = 0
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
        if not title_row:
            continue

        title = title_row['value']

        # 获取作者（可选）
        authors = []
        cursor.execute("""
        SELECT ia.firstName, ia.lastName, ia.fieldMode
        FROM itemCreators ic
        JOIN creators ia ON ic.creatorID = ia.creatorID
        WHERE ic.itemID = ?
        ORDER BY ic.orderIndex
        LIMIT 1
        """, (item_id,))
        author_row = cursor.fetchone()
        if author_row:
            if author_row['fieldMode'] == 1:
                authors.append(author_row['lastName'] or '')
            else:
                name = ""
                if author_row['firstName']:
                    name += author_row['firstName'] + " "
                if author_row['lastName']:
                    name += author_row['lastName']
                authors.append(name.strip())

        author_str = authors[0] if authors else None

        print(f"  条目ID: {item_id}, Key: {key}")
        print(f"    标题: {title[:60]}...")

        # 搜索DOI
        doi = search_doi_by_title(title, author_str)
        if doi:
            print(f"    找到DOI: {doi}")
            if update_item_doi(conn, item_id, doi):
                updated_count += 1
        else:
            print(f"    未找到DOI")

        # 避免请求过快
        time.sleep(1)

    conn.commit()
    print(f"已更新 {updated_count} 个条目的DOI")
    return updated_count

def main():
    print("=== 补全Zotero条目信息 ===")

    conn = connect_db()

    try:
        # 1. 补全缺失年份
        years_updated = complete_missing_years(conn)

        # 2. 尝试查找缺失DOI（限制数量）
        dois_updated = complete_missing_dois(conn, limit=30)

        print("\n=== 完成 ===")
        print(f"补全年份: {years_updated} 个条目")
        print(f"补全DOI: {dois_updated} 个条目")

    except Exception as e:
        print(f"补全信息过程中出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()