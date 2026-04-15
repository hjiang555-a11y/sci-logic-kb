#!/usr/bin/env python3
"""
清理Zotero数据库：去除重复、补全缺失信息
"""

import sqlite3
import re
import sys
import json
from collections import defaultdict
from urllib.request import urlopen, Request
from urllib.parse import quote
from difflib import SequenceMatcher

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

def normalize_title(title):
    """规范化标题以便比较：小写、移除标点、移除常见词"""
    if not title:
        return ""

    # 转换为小写
    title = title.lower()

    # 移除标点符号
    title = re.sub(r'[^\w\s]', ' ', title)

    # 移除常见词（冠词、连接词等）
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    words = [word for word in title.split() if word not in stop_words]

    # 排序单词以处理词序差异（可选）
    # words.sort()

    return ' '.join(words)

def get_all_items(conn):
    """获取所有文献条目及其详细信息"""
    cursor = conn.cursor()

    # 查询所有文献条目
    query = """
    SELECT
        i.itemID, i.key, i.itemTypeID, it.typeName,
        i.dateAdded, i.dateModified
    FROM items i
    JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
    WHERE it.typeName IN ('journalArticle', 'conferencePaper', 'thesis', 'bookSection', 'preprint')
    ORDER BY i.itemID
    """

    cursor.execute(query)
    items = cursor.fetchall()

    # 获取字段映射
    cursor.execute("SELECT fieldID, fieldName FROM fields")
    field_map = {row['fieldID']: row['fieldName'] for row in cursor.fetchall()}

    items_details = {}
    for item in items:
        item_id = item['itemID']
        details = get_item_details(conn, item_id, field_map)
        items_details[item_id] = details

    return items_details

def get_item_details(conn, item_id, field_map):
    """获取条目的详细信息"""
    cursor = conn.cursor()

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

    # 获取附件信息（跳过，因为列名可能不同）
    # attachment_query = """
    # SELECT ia.key, ia.itemTypeID, iat.typeName, ia.dateAdded, ia.dateModified
    # FROM itemAttachments ia
    # JOIN itemTypes iat ON ia.itemTypeID = iat.itemTypeID
    # WHERE ia.parentItemID = ?
    # """
    # cursor.execute(attachment_query, (item_id,))
    # attachments = cursor.fetchall()
    # details['attachments'] = [dict(row) for row in attachments]
    details['attachments'] = []

    return details

def find_duplicates_advanced(items_details):
    """高级重复检测：基于标题相似性、DOI、作者+年份"""
    duplicates = []

    # 按规范化标题分组
    title_groups = defaultdict(list)
    for item_id, details in items_details.items():
        title = details.get('title', '')
        if title:
            norm_title = normalize_title(title)
            if norm_title:  # 忽略空标题
                title_groups[norm_title].append(item_id)

    # 按DOI分组
    doi_groups = defaultdict(list)
    for item_id, details in items_details.items():
        doi = details.get('DOI', '')
        if doi:
            doi_groups[doi.lower()].append(item_id)

    # 基于标题的重复
    for norm_title, ids in title_groups.items():
        if len(ids) > 1:
            # 检查标题相似性（防止误判）
            titles = [items_details[item_id].get('title', '') for item_id in ids]
            similar = True
            for i in range(len(titles)-1):
                ratio = SequenceMatcher(None, titles[i].lower(), titles[i+1].lower()).ratio()
                if ratio < 0.8:  # 相似度阈值
                    similar = False
                    break
            if similar:
                duplicates.append(('title', norm_title, ids, titles))

    # 基于DOI的重复
    for doi, ids in doi_groups.items():
        if len(ids) > 1:
            duplicates.append(('DOI', doi, ids, [items_details[item_id].get('title', '') for item_id in ids]))

    # 基于作者+年份的近似重复（无DOI情况）
    author_year_groups = defaultdict(list)
    for item_id, details in items_details.items():
        authors = tuple(details.get('authors', []))
        year = details.get('date', '')[:4] if details.get('date') else ''
        if authors and year:
            key = (tuple(authors), year)
            author_year_groups[key].append(item_id)

    for key, ids in author_year_groups.items():
        if len(ids) > 1:
            authors, year = key
            # 检查标题相似性
            titles = [items_details[item_id].get('title', '') for item_id in ids]
            similar_titles = all(
                SequenceMatcher(None, t1.lower(), t2.lower()).ratio() > 0.7
                for i, t1 in enumerate(titles) for j, t2 in enumerate(titles) if i < j
            )
            if similar_titles:
                duplicates.append(('author_year', f"{authors[:2]}... {year}", ids, titles))

    return duplicates

def find_missing_info(items_details):
    """查找缺失重要信息的条目"""
    missing_info = []
    for item_id, details in items_details.items():
        missing = []
        if 'title' not in details or not details['title']:
            missing.append('标题')
        if 'DOI' not in details or not details['DOI']:
            missing.append('DOI')
        if 'date' not in details or not details['date']:
            missing.append('年份')
        if 'authors' not in details or not details['authors']:
            missing.append('作者')

        if missing:
            missing_info.append((item_id, details, missing))

    return missing_info

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
    except Exception as e:
        print(f"获取DOI {doi} 元数据失败: {e}")

    return None

def extract_year_from_date(date_str):
    """从日期字符串中提取年份"""
    if not date_str:
        return None

    # 尝试匹配年份（4位数字）
    match = re.search(r'\b(\d{4})\b', date_str)
    if match:
        return match.group(1)

    return None

def main():
    print("=== Zotero数据库清理工具 ===")
    print("1. 检测重复条目")
    print("2. 查找缺失信息")
    print("3. 尝试补全缺失信息")
    print()

    conn = connect_db()

    print("正在读取数据库...")
    items_details = get_all_items(conn)
    print(f"共读取 {len(items_details)} 个文献条目")

    print("\n=== 高级重复检测 ===")
    duplicates = find_duplicates_advanced(items_details)

    if duplicates:
        print(f"发现 {len(duplicates)} 组重复条目:")
        for dup_type, value, ids, titles in duplicates:
            print(f"\n基于{dup_type}的重复: {value[:50]}...")
            for i, item_id in enumerate(ids):
                title = titles[i][:60] + "..." if len(titles[i]) > 60 else titles[i]
                print(f"  [{i+1}] 条目ID: {item_id}, 标题: {title}")
    else:
        print("未发现重复条目")

    print("\n=== 缺失重要信息的条目 ===")
    missing_info = find_missing_info(items_details)

    if missing_info:
        print(f"发现 {len(missing_info)} 个条目缺失重要信息:")

        # 分类缺失信息
        missing_all = []  # 完全缺失（标题、DOI、年份、作者都没有）
        missing_partial = []  # 部分缺失

        for item_id, details, missing in missing_info:
            if len(missing) == 4:  # 全部缺失
                missing_all.append((item_id, details, missing))
            else:
                missing_partial.append((item_id, details, missing))

        if missing_all:
            print(f"\n完全缺失信息的条目 ({len(missing_all)} 个):")
            for item_id, details, missing in missing_all[:10]:  # 最多显示10个
                print(f"  条目ID: {item_id}, 缺失: {', '.join(missing)}")
                if 'attachments' in details and details['attachments']:
                    print(f"    有 {len(details['attachments'])} 个附件")

        if missing_partial:
            print(f"\n部分缺失信息的条目 ({len(missing_partial)} 个):")
            for item_id, details, missing in missing_partial[:10]:  # 最多显示10个
                title = details.get('title', 'N/A')[:50]
                print(f"  条目ID: {item_id}, 标题: {title}...")
                print(f"    缺失: {', '.join(missing)}")
                if 'DOI' in details and details['DOI'] and 'date' not in details:
                    print(f"    DOI: {details['DOI']} (可尝试获取年份)")
    else:
        print("所有条目信息完整")

    # 尝试通过DOI补全年份信息
    print("\n=== 尝试通过DOI补全年份信息 ===")
    doi_to_fetch = []
    for item_id, details, missing in missing_partial:
        if 'date' in missing and 'DOI' in details and details['DOI']:
            doi_to_fetch.append((item_id, details['DOI']))

    if doi_to_fetch:
        print(f"发现 {len(doi_to_fetch)} 个有DOI但缺少年份的条目")
        print("正在从Crossref API获取年份信息...")

        for i, (item_id, doi) in enumerate(doi_to_fetch[:5]):  # 限制前5个
            print(f"  [{i+1}] DOI: {doi}")
            metadata = fetch_doi_metadata(doi)
            if metadata:
                published = metadata.get('published', {})
                year = None

                # 尝试从不同字段提取年份
                if published.get('date-parts'):
                    date_parts = published['date-parts'][0]
                    if date_parts and len(date_parts) > 0:
                        year = str(date_parts[0])

                if not year:
                    year = metadata.get('published-year') or metadata.get('year')

                if year:
                    print(f"     找到年份: {year}")
                    # 这里可以添加更新数据库的代码
                else:
                    print(f"     未找到年份信息")
            else:
                print(f"     获取元数据失败")
    else:
        print("没有需要补全年份的条目")

    conn.close()

    print("\n=== 建议操作 ===")
    if duplicates:
        print("1. 手动检查重复条目并删除重复项")

    if missing_all:
        print(f"2. 检查 {len(missing_all)} 个完全缺失信息的条目，如果无用可删除")

    if doi_to_fetch:
        print(f"3. 为 {len(doi_to_fetch)} 个条目补全年份信息")

    print("\n注意：直接操作数据库有风险，建议先导出备份")

if __name__ == "__main__":
    main()