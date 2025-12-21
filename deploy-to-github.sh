#!/bin/bash
echo "🚀 开始部署 iLogos 平台到 GitHub Pages..."
echo "========================================"

# 1. 检查GitHub配置
read -p "请输入你的GitHub用户名: " GITHUB_USER
read -p "请输入仓库名（推荐: ilogos-platform）: " REPO_NAME

if [ -z "$GITHUB_USER" ] || [ -z "$REPO_NAME" ]; then
    echo "❌ 需要提供GitHub信息"
    exit 1
fi

# 2. 设置远程仓库
echo "🌐 设置远程仓库..."
git remote remove origin 2>/dev/null
GITHUB_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
git remote add origin "$GITHUB_URL"

# 3. 推送到GitHub
echo "⬆️  推送到GitHub..."
if git push -u origin main 2>/dev/null; then
    echo "✅ 推送成功！"
else
    echo "⚠️  推送失败，可能仓库不存在"
    echo "请在GitHub上创建仓库: https://github.com/new"
    echo "仓库名: $REPO_NAME"
    echo "然后再次运行此脚本"
    exit 1
fi

# 4. 配置GitHub Pages
echo ""
echo "📋 下一步手动配置GitHub Pages："
echo "1. 访问 https://github.com/$GITHUB_USER/$REPO_NAME/settings/pages"
echo "2. 在 'Source' 部分选择 'main' 分支"
echo "3. 选择 '/ (root)' 文件夹"
echo "4. 点击 'Save'"
echo ""
echo "🌍 网站将在几分钟后上线："
echo "   https://$GITHUB_USER.github.io/$REPO_NAME/"
echo ""
echo "💡 提示：如果使用自定义域名，可在设置中添加"
