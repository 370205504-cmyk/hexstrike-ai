#!/bin/bash

# HexStrike AI 开发环境初始化脚本
# 功能：设置git配置并准备首次提交

echo "========================================="
echo "HexStrike AI 开发环境设置"
echo "========================================="
echo ""

# 检查是否在正确的目录
if [ ! -d ".git" ]; then
    echo "错误：请在 hexstrike-ai 目录中运行此脚本"
    exit 1
fi

# 检查git状态
echo "1. 检查Git状态..."
git status
echo ""

# 检查虚拟环境
if [ ! -d "hexstrike-dev" ]; then
    echo "警告：虚拟环境不存在，正在创建..."
    python3 -m venv hexstrike-dev
    echo "虚拟环境已创建"
fi
echo ""

# 配置git用户信息（提示用户）
echo "2. Git配置"
read -p "请输入您的Git用户名: " git_username
read -p "请输入您的Git邮箱: " git_email

git config user.name "$git_username"
git config user.email "$git_email"
echo "Git用户信息已配置"
echo ""

# 添加.gitignore
echo "3. 配置Git忽略规则..."
if [ -f ".gitignore" ]; then
    echo ".gitignore 文件已存在"
else
    echo "创建 .gitignore 文件..."
    cat > .gitignore << 'EOF'
# Virtual environments
hexstrike-dev/
venv/
env/
.venv/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# MCP cache
.mcp/
EOF
fi
echo ""

# 添加所有更改
echo "4. 准备提交..."
git add .
git status
echo ""

# 询问是否现在提交
read -p "是否现在创建初始提交？(y/n): " confirm
if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    git commit -m "feat: 设置HexStrike AI开发环境
    
- 添加开发分支dev
- 配置虚拟环境hexstrike-dev
- 添加.gitignore规则
- 创建开发文档DEVELOPMENT.md
- 配置适合二次开发的Git工作流"
    echo ""
    echo "✅ 初始提交完成！"
    echo ""
    echo "查看提交历史："
    git log --oneline -1
else
    echo "未创建提交。您可以稍后手动提交。"
fi

echo ""
echo "========================================="
echo "设置完成！"
echo "========================================="
echo ""
echo "下一步："
echo "1. 激活虚拟环境: source hexstrike-dev/bin/activate"
echo "2. 查看开发文档: cat DEVELOPMENT.md"
echo "3. 开始开发工作"
echo "4. 推送代码: git push origin dev"
echo ""
