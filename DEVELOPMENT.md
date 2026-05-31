# HexStrike AI 开发环境配置

## 环境信息
- **官方仓库**: https://github.com/0x4m4/hexstrike-ai
- **当前分支**: dev (二次开发专用)
- **Python版本**: 3.14
- **虚拟环境**: hexstrike-dev

## 快速开始

### 1. 激活虚拟环境
```bash
cd hexstrike-ai
source hexstrike-dev/bin/activate
```

### 2. 运行开发服务器
```bash
python3 hexstrike_server.py --debug --port 8888
```

### 3. 验证安装
```bash
python3 -c "import hexstrike; print('HexStrike AI loaded successfully!')"
```

## Git 工作流程

### 分支管理
- **master**: 官方稳定版本（只读）
- **dev**: 二次开发分支（您当前的分支）

### 提交代码
```bash
# 查看当前状态
git status

# 添加修改的文件
git add .

# 提交（替换为您的提交信息）
git commit -m "feat: 添加新功能"

# 推送到远程dev分支
git push origin dev
```

### 同步上游更新
```bash
# 添加上游仓库（如果还没有）
git remote add upstream https://github.com/0x4m4/hexstrike-ai.git

# 获取上游最新代码
git fetch upstream

# 合并上游更新到dev分支
git merge upstream/master
```

## 项目结构

```
hexstrike-ai/
├── hexstrike_server.py      # MCP服务主入口
├── hexstrike_mcp.py         # MCP协议实现
├── requirements.txt         # Python依赖列表
├── hexstrike-ai-mcp.json   # MCP配置文件
├── assets/                  # 静态资源
├── .gitignore              # Git忽略规则
└── hexstrike-dev/          # 虚拟环境（已创建）
```

## 二次开发建议

### 1. 添加新的CLI工具
在项目根目录创建 `cli.py` 文件：
```python
#!/usr/bin/env python3
import sys
from your_module import main

if __name__ == "__main__":
    main()
```

### 2. 添加新的Kali工具
参考 `tools/` 目录下的现有实现进行扩展。

### 3. 工具调用
使用 `ToolManager` 类统一管理所有工具调用。

## 依赖管理

### 安装新依赖
```bash
source hexstrike-dev/bin/activate
pip3 install <package_name>
pip3 freeze > requirements.txt
```

### 导出当前依赖
```bash
pip3 freeze > requirements.txt
```

## 常见问题

### Q: 虚拟环境无法激活
```bash
# 确保在正确的目录
cd hexstrike-ai
source hexstrike-dev/bin/activate
```

### Q: 依赖安装失败
```bash
# 升级pip
pip3 install --upgrade pip
# 重新安装依赖
pip3 install -r requirements.txt
```

### Q: 如何查看已安装的包
```bash
pip3 list
```

## 下一步

1. 查看 [README.md](README.md) 了解项目详情
2. 查看 `hexstrike_server.py` 了解服务架构
3. 开始您的二次开发工作！

## 许可证
本项目基于 MIT 许可证开源。详情请查看 [LICENSE](LICENSE) 文件。
