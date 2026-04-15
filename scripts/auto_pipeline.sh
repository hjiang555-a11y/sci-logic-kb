#!/bin/bash
# 自动化论文处理流水线
# 从Zotero获取未处理论文，上传PDF到GitHub，分批处理，质量检查，清理PDF

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "========================================"
echo "自动化论文处理流水线"
echo "开始时间: $(date)"
echo "========================================"

# 配置
BATCH_SIZE=10
GITHUB_TOKEN="${GITHUB_TOKEN}"
ZOTERO_USER_ID="19944378"

# 检查环境
if [ -z "$GITHUB_TOKEN" ]; then
    echo "警告: GITHUB_TOKEN 未设置，跳过Issue创建"
    echo "请设置: export GITHUB_TOKEN=your_token"
fi

# 步骤1: 获取并上传未处理论文PDF
echo ""
echo "步骤1: 获取未处理论文PDF"
echo "----------------------------------------"

python3 scripts/batch_process_zotero.py --batch-size "$BATCH_SIZE"

echo ""
echo "步骤1完成"
echo "现在PDF文件已上传到仓库的pdfs/目录"
echo "GitHub Issue已创建触发处理"
echo ""
echo "等待GitHub Actions处理完成..."
echo "建议等待几分钟后再继续下一步"

# 询问是否继续
read -p "是否继续步骤2（质量检查）？[y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "暂停，稍后运行步骤2: scripts/batch_quality_check.py"
    exit 0
fi

# 步骤2: 质量检查
echo ""
echo "步骤2: 质量检查与整理"
echo "----------------------------------------"

# 运行质量检查
python3 scripts/batch_quality_check.py --count "$BATCH_SIZE" --mark-unverified --output "quality_report_$(date +%Y%m%d_%H%M%S).md"

echo ""
echo "质量检查完成"
echo "报告已生成"

# 步骤3: 清理已处理的PDF（可选）
echo ""
echo "步骤3: 清理PDF文件（可选）"
echo "----------------------------------------"

echo "注意: 为节省存储空间，可删除已处理的PDF文件"
echo "但请确保:"
echo "1. GitHub Actions已成功处理所有论文"
echo "2. 对应的YAML文件已生成在papers/目录"
echo "3. 需要保留PDF时可跳过此步骤"

read -p "是否删除pdfs/目录中的PDF文件？[y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "删除PDF文件..."
    rm -f pdfs/*.pdf
    echo "PDF文件已删除"

    # 从git中删除
    git rm pdfs/*.pdf 2>/dev/null || true
    git commit -m "cleanup: remove processed PDF files to save space" || true
    echo "PDF文件已从git记录中移除"
else
    echo "保留PDF文件"
fi

echo ""
echo "========================================"
echo "自动化流水线完成"
echo "完成时间: $(date)"
echo "========================================"
echo ""
echo "后续操作建议:"
echo "1. 检查GitHub仓库的Pull Requests"
echo "2. 审核质量检查报告"
echo "3. 验证新节点是否正确标注'未审核'"
echo "4. 根据需要进行手动调整"
echo ""
echo "要处理下一批论文，重新运行此脚本"