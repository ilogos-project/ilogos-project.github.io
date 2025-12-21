#!/bin/bash
echo "🚀 快速启动 iLogos 平台"
echo "======================"

# 检查目录
if [ ! -d "code/website" ]; then
    echo "正在创建项目结构..."
    mkdir -p code/website
    mkdir -p data/corpus
    mkdir -p scripts
    
    # 创建最简单的网站
    cat > code/website/index.html << 'HTML_END'
<!DOCTYPE html>
<html>
<head>
    <title>iLogos Platform</title>
    <style>
        body { font-family: Arial; margin: 0; }
        .hero { background: #1a237e; color: white; padding: 100px 20px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>iLogos Platform</h1>
        <p>Ancient Language Big Data Platform</p>
    </div>
    <div class="container">
        <h2>快速开始成功！</h2>
        <p>你的 iLogos 平台已经设置完成。</p>
    </div>
</body>
</html>
HTML_END
fi

echo "✅ 项目已初始化"
echo ""
echo "📋 下一步："
echo "1. 启动网站: cd code/website && python3 -m http.server 8000"
echo "2. 访问: http://localhost:8000"
