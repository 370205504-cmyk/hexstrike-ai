# 🐉 Kali Linux 部署与使用教程

本教程将指导您在 Kali Linux 系统上部署和使用 HexStrike AI。

---

## 📋 目录

1. [系统要求](#系统要求)
2. [部署教程](#部署教程)
3. [配置教程](#配置教程)
4. [使用教程](#使用教程)
5. [常见问题](#常见问题)

---

## 系统要求

### 最低配置
- **操作系统**: Kali Linux 2025.04+
- **Python**: 3.8+
- **内存**: 4GB RAM
- **磁盘**: 10GB 可用空间
- **网络**: 可访问互联网

### 推荐配置
- **操作系统**: Kali Linux 2025.05+
- **Python**: 3.13
- **内存**: 8GB+ RAM
- **磁盘**: 20GB+ 可用空间
- **网络**: 双网卡（攻击 + 管理）

---

## 部署教程

### 方法一：从 GitHub 克隆（推荐）

#### 步骤 1：更新系统
```bash
sudo apt update
sudo apt upgrade -y
```

#### 步骤 2：安装基础依赖
```bash
sudo apt install -y python3 python3-venv python3-pip git
```

#### 步骤 3：克隆项目
```bash
cd ~
git clone https://github.com/370205504-cmyk/hexstrike-ai.git
cd hexstrike-ai
```

#### 步骤 4：创建虚拟环境
```bash
python3 -m venv hexstrike-dev
source hexstrike-dev/bin/activate
```

#### 步骤 5：安装 Python 依赖
```bash
pip3 install -r requirements.txt
```

#### 步骤 6：验证安装
```bash
# 查看帮助
python3 cli.py --help

# 测试组件
python3 test_cli.py
```

### 方法二：使用初始化脚本

项目提供了自动化初始化脚本：

```bash
cd ~/hexstrike-ai
chmod +x init_dev.sh
./init_dev.sh
```

---

## 配置教程

### 1. 创建配置目录

配置文件会自动创建在 `~/.hexstrike/` 目录下：

```bash
# 首次运行 CLI 会自动创建配置
python3 cli.py --help
```

### 2. 配置文件说明

配置文件位置：`~/.hexstrike/config.yaml`

#### 默认配置示例：
```yaml
api:
  api_key: ""                    # 您的 API Key
  base_url: "https://api.openai.com/v1"  # API 基础 URL
  model: "gpt-4o"                # 使用的模型
  ollama:
    enabled: false               # 是否启用 Ollama
    base_url: "http://localhost:11434/v1"
    model: "llama3"

server:
  host: "127.0.0.1"
  port: 8888

cli:
  output_format: "markdown"
  debug: false
```

### 3. 配置 OpenAI 兼容 API

#### 选项 A：使用 OpenAI
```bash
# 编辑配置文件
nano ~/.hexstrike/config.yaml
```

修改以下内容：
```yaml
api:
  api_key: "sk-您的OpenAI-API-Key"
  base_url: "https://api.openai.com/v1"
  model: "gpt-4o"
```

#### 选项 B：使用 DeepSeek
```yaml
api:
  api_key: "sk-您的DeepSeek-API-Key"
  base_url: "https://api.deepseek.com/v1"
  model: "deepseek-chat"
```

#### 选项 C：使用通义千问
```yaml
api:
  api_key: "sk-您的通义千问-API-Key"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  model: "qwen-plus"
```

### 4. 配置 Ollama 本地模型

#### 步骤 1：安装 Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### 步骤 2：启动 Ollama 服务
```bash
# 启动服务
systemctl start ollama
# 设置开机自启
systemctl enable ollama
```

#### 步骤 3：下载模型
```bash
ollama pull llama3
# 或使用其他模型
ollama pull qwen2
ollama pull mistral
```

#### 步骤 4：配置 HexStrike 使用 Ollama
```bash
# 编辑配置文件
nano ~/.hexstrike/config.yaml
```

修改以下内容：
```yaml
api:
  ollama:
    enabled: true
    base_url: "http://localhost:11434/v1"
    model: "llama3"
```

---

## 使用教程

### 一、CLI 工具使用

#### 1. 查看帮助
```bash
python3 cli.py --help
```

#### 2. 交互式模式（推荐新手）
```bash
python3 cli.py --target 192.168.1.100
```

#### 3. 全自动模式（非交互）
```bash
python3 cli.py --target 192.168.1.100 --non-interactive
```

#### 4. 使用 Ollama 本地模型
```bash
python3 cli.py --target 192.168.1.100 --ollama
```

#### 5. 列出可用工具
```bash
python3 cli.py --list-tools
```

#### 6. 调试模式
```bash
python3 cli.py --target 192.168.1.100 --debug
```

### 二、MCP 服务器使用

#### 1. 启动服务器
```bash
python3 hexstrike_server.py
```

#### 2. 调试模式启动
```bash
python3 hexstrike_server.py --debug
```

#### 3. 自定义端口
```bash
python3 hexstrike_server.py --port 8888
```

#### 4. 测试服务器健康状态
```bash
curl http://localhost:8888/health
```

### 三、实用示例

#### 示例 1：信息收集
```bash
# 交互式模式
python3 cli.py --target 192.168.1.100
# 然后选择"信息收集"选项
```

#### 示例 2：Web 应用测试
```bash
python3 cli.py --target http://example.com
# 选择"Web 应用安全测试"
```

#### 示例 3：漏洞扫描
```bash
python3 cli.py --target 192.168.1.100 --non-interactive
```

---

## 常见问题

### Q1: 提示找不到 Python 模块？
**A:** 确保已激活虚拟环境：
```bash
cd ~/hexstrike-ai
source hexstrike-dev/bin/activate
```

### Q2: 如何更新项目？
**A:**
```bash
cd ~/hexstrike-ai
git pull
source hexstrike-dev/bin/activate
pip3 install -r requirements.txt --upgrade
```

### Q3: Ollama 连接失败？
**A:** 检查 Ollama 服务状态：
```bash
systemctl status ollama
# 如果未启动，启动服务
systemctl start ollama
```

### Q4: 端口被占用？
**A:** 使用其他端口：
```bash
python3 hexstrike_server.py --port 9999
```

### Q5: 如何卸载？
**A:**
```bash
# 删除项目目录
rm -rf ~/hexstrike-ai
# 删除配置文件
rm -rf ~/.hexstrike
```

### Q6: 如何重置配置？
**A:**
```bash
rm -rf ~/.hexstrike
# 重新运行 CLI 会创建新配置
python3 cli.py --help
```

---

## 安全建议

1. **始终在授权环境使用** - 只能测试您拥有或获得授权的系统
2. **使用隔离环境** - 建议在虚拟机或专用测试环境运行
3. **监控活动** - 时刻关注 AI 智能体的操作
4. **备份重要数据** - 操作前备份重要数据
5. **遵守法律法规** - 遵守当地网络安全相关法律

---

## 📞 获取帮助

- 查看项目文档：`DEVELOPMENT.md`
- GitHub Issues：https://github.com/370205504-cmyk/hexstrike-ai/issues
- 查看配置说明：`GITHUB_SETUP.md`

---

## 🎉 下一步

完成部署后，您可以：

1. ✅ 阅读 `README.md` 了解项目
2. ✅ 尝试运行 `python3 test_cli.py` 测试组件
3. ✅ 使用 `python3 cli.py --help` 探索功能
4. ✅ 开始您的第一次渗透测试（在授权环境中！）

祝您使用愉快！🚀
