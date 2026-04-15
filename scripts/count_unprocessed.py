#!/usr/bin/env python3
import re

with open('QUEUE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 匹配未处理论文
pattern = r'\[ \]\s*`([A-Z0-9]{8})`\s*\|\s*([^|]+)\s*\|\s*(.+)'
matches = re.findall(pattern, content)

print(f'未处理论文数量: {len(matches)}')

# 按类别分组
fiber_count = 0
fp_count = 0
other_count = 0

for zotero_key, author_year, title in matches:
    if 'fiber' in title.lower() or 'fiber' in author_year.lower():
        fiber_count += 1
    elif 'cavity' in title.lower() or 'fp' in title.lower():
        fp_count += 1
    else:
        other_count += 1

print(f'光纤相关: {fiber_count} 篇')
print(f'FP腔相关: {fp_count} 篇')
print(f'其他: {other_count} 篇')

# 显示前10篇
print('\n前10篇未处理论文:')
for i, (zotero_key, author_year, title) in enumerate(matches[:10], 1):
    print(f'{i}. {zotero_key} | {author_year} | {title[:60]}...')