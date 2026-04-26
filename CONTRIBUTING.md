---

## 本地环境搭建

本地维护只需要 Python 3.10+ 和 `pyyaml`：

```bash
python -m pip install pyyaml
```

如需使用 Zotero / Obsidian / 本地 PDF 工作流，可复制环境变量模板：

```bash
cp .env.example .env
```

常用验证命令：

```bash
python scripts/lint.py --summary
python scripts/stats.py
python scripts/build_index.py
```

## 快速上手：单篇论文摄入 Checklist