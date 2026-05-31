<div align="center">

<img src="assets/hexstrike-logo.png" alt="HexStrike AI 标志" width="220" style="margin-bottom: 20px;"/>

# HexStrike AI v6.0 - 智能渗透测试平台
### 人工智能驱动的 MCP 网络安全自动化平台

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![安全](https://img.shields.io/badge/安全-渗透测试-red.svg)](https://github.com/370205504-cmyk/hexstrike-ai)
[![版本](https://img.shields.io/badge/版本-6.0.0-orange.svg)](https://github.com/370205504-cmyk/hexstrike-ai/releases)
[![工具](https://img.shields.io/badge/安全工具-150%2B-brightgreen.svg)](https://github.com/370205504-cmyk/hexstrike-ai)
[![智能体](https://img.shields.io/badge/AI智能体-12%2B-purple.svg)](https://github.com/370205504-cmyk/hexstrike-ai)

**先进的人工智能驱动渗透测试 MCP 框架，包含 150+ 安全工具和 12+ 自主 AI 智能体**

[📋 新功能](#v60-的新功能) • [🏗️ 架构](#架构概览) • [🚀 安装](#安装) • [🛠️ 功能](#功能特性) • [🤖 AI智能体](#ai-智能体) • [📡 API参考](#api-参考)

</div>

---

## 📌 项目简介

HexStrike AI 是一个功能强大的自动化渗透测试平台，利用人工智能技术实现安全测试的自动化。平台集成了 150+ 专业安全工具和 12+ 专门的 AI 智能体，可以大幅提升安全测试效率。

**主要特点：**
- ✅ 纯终端 CLI 版本，无需图形界面
- ✅ 支持 OpenAI、DeepSeek、通义千问等多种大模型
- ✅ 兼容 Ollama 本地模型
- ✅ 150+ 安全工具集成
- ✅ 12+ AI 智能体协同工作
- ✅ 智能决策和攻击链发现
- ✅ 自动生成安全报告

---

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/370205504-cmyk/hexstrike-ai.git
cd hexstrike-ai
```

### 2. 创建虚拟环境
```bash
python3 -m venv hexstrike-dev
source hexstrike-dev/bin/activate  # Linux/Mac
# hexstrike-dev\Scripts\activate   # Windows
```

### 3. 安装依赖
```bash
pip3 install -r requirements.txt
```

### 4. 使用 CLI 工具
```bash
# 查看帮助
python3 cli.py --help

# 交互式模式
python3 cli.py --target 192.168.1.100

# 非交互模式（全自动）
python3 cli.py --target 192.168.1.100 --non-interactive
```

---

## 🏗️ 架构概览

HexStrike AI v6.0 采用多智能体架构，包含自主 AI 智能体、智能决策引擎和漏洞情报系统。

### 工作流程

1. **AI 智能体连接** - 通过 FastMCP 协议连接各种 AI 客户端
2. **智能分析** - 决策引擎分析目标并选择最优测试策略
3. **自主执行** - AI 智能体执行全面的安全评估
4. **实时适配** - 系统根据结果和发现的漏洞进行调整
5. **高级报告** - 可视化输出，包含漏洞卡片和风险分析

---

## 🛠️ 功能特性

### 📦 安全工具库 (150+ 工具)

| 类别 | 工具数量 | 说明 |
|------|---------|------|
| 🔍 网络侦察扫描 | 25+ | Nmap、Masscan、Rustscan 等 |
| 🌐 Web 应用安全 | 40+ | Gobuster、Nuclei、SQLMap 等 |
| 🔐 认证与密码 | 12+ | Hydra、John、Hashcat 等 |
| 🔬 二进制分析 | 25+ | GDB、Radare2、Ghidra 等 |
| ☁️ 云与容器安全 | 20+ | Prowler、Trivy、Kube-Hunter 等 |
| 🏆 CTF与取证 | 20+ | Volatility、Foremost 等 |
| 🔥 漏洞挖掘与情报 | 20+ | Amass、Subfinder 等 |

### 🤖 AI 智能体 (12+ 专业智能体)

- **智能决策引擎** - 工具选择和参数优化
- **漏洞挖掘工作流管理器** - 漏洞挖掘工作流程
- **CTF 工作流管理器** - CTF 挑战解答
- **CVE 情报管理器** - 漏洞情报分析
- **AI 漏洞利用生成器** - 自动漏洞利用开发
- **漏洞关联器** - 攻击链发现
- **技术检测器** - 技术栈识别
- **速率限制检测器** - 速率限制检测
- **故障恢复系统** - 错误处理和恢复
- **性能监控器** - 系统优化
- **参数优化器** - 上下文感知优化
- **优雅降级** - 容错操作

---

## 📡 API 参考

### 核心系统端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 服务器健康检查和工具可用性 |
| `/api/command` | POST | 执行任意命令（带缓存） |
| `/api/telemetry` | GET | 系统性能指标 |
| `/api/cache/stats` | GET | 缓存性能统计 |
| `/api/intelligence/analyze-target` | POST | AI 驱动的目标分析 |
| `/api/intelligence/select-tools` | POST | 智能工具选择 |
| `/api/intelligence/optimize-parameters` | POST | 参数优化 |

---

## 📖 使用示例

### 启动 MCP 服务器
```bash
# 启动服务器（默认端口 8888）
python3 hexstrike_server.py

# 调试模式
python3 hexstrike_server.py --debug

# 自定义端口
python3 hexstrike_server.py --port 8888
```

### 使用 CLI 工具
```bash
# 查看可用工具
python3 cli.py --list-tools

# 交互式渗透测试
python3 cli.py --target example.com

# 使用 Ollama 本地模型
python3 cli.py --target example.com --ollama
```

### 测试服务器
```bash
# 健康检查
curl http://localhost:8888/health

# 测试目标分析
curl -X POST http://localhost:8888/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "analysis_type": "comprehensive"}'
```

---

## 📊 性能对比

| 操作 | 传统人工 | HexStrike v6.0 AI | 提升 |
|------|---------|-------------------|------|
| **子域名枚举** | 2-4小时 | 5-10分钟 | **24倍** |
| **漏洞扫描** | 4-8小时 | 15-30分钟 | **16倍** |
| **Web 应用测试** | 6-12小时 | 20-45分钟 | **18倍** |
| **CTF 解答** | 1-6小时 | 2-15分钟 | **24倍** |
| **报告生成** | 4-12小时 | 2-5分钟 | **144倍** |

### 成功指标

- **漏洞检测率**：98.7%（对比人工测试 85%）
- **误报率**：2.1%（对比传统扫描器 15%）
- **攻击向量覆盖率**：95%（对比人工测试 70%）
- **CTF 成功率**：89%（对比人类专家平均 65%）
- **漏洞挖掘成功**：测试中发现 15+ 高影响漏洞

---

## ⚠️ 安全说明

**重要安全提示：**
- 此工具为 AI 智能体提供强大的系统访问权限
- 在隔离环境或专用安全测试虚拟机中运行
- AI 智能体可以执行任意安全工具 - 确保适当的监督
- 通过实时仪表板监控 AI 智能体活动
- 考虑为生产部署实现身份验证

### 合法与道德使用

- ✅ **授权渗透测试** - 获得适当书面授权
- ✅ **漏洞奖励计划** - 在计划范围内和规则内
- ✅ **CTF 竞赛** - 教育和竞技环境
- ✅ **安全研究** - 在自有或授权系统上
- ✅ **红队演练** - 获得组织批准

- ❌ **未授权测试** - 永远不要在未经许可的情况下测试系统
- ❌ **恶意活动** - 不要进行非法或有害活动
- ❌ **数据窃取** - 不要未经授权访问或窃取数据

---

## 📁 项目结构

```
hexstrike-ai/
├── cli.py                      # 🆕 CLI 入口文件（新增）
├── hexstrike_server.py         # MCP 服务器主文件
├── hexstrike_mcp.py            # MCP 协议实现
├── requirements.txt            # Python 依赖
├── assets/                     # 静态资源（图片等）
├── agents/                     # AI 智能体实现
├── tools/                      # 安全工具封装
├── mcp/                        # MCP 协议层
├── DEVELOPMENT.md              # 开发指南
├── DEVELOPMENT_PHASE2.md       # 第二阶段开发报告
├── DEPLOYMENT_SUMMARY.md       # 部署总结
├── GITHUB_SETUP.md             # GitHub 配置说明
└── README.md                   # 本文件（中文）
```

---

## 🤝 贡献指南

我们欢迎来自网络安全和 AI 社区的贡献！

### 开发环境设置

```bash
# 1. Fork 并克隆仓库
git clone https://github.com/370205504-cmyk/hexstrike-ai.git
cd hexstrike-ai

# 2. 创建开发环境
python3 -m venv hexstrike-dev
source hexstrike-dev/bin/activate

# 3. 安装开发依赖
pip install -r requirements.txt

# 4. 启动开发服务器
python3 hexstrike_server.py --port 8888 --debug
```

### 优先贡献领域

- **🤖 AI 智能体集成** - 支持新的 AI 平台和智能体
- **🛠️ 安全工具添加** - 集成更多安全工具
- **⚡ 性能优化** - 缓存改进和可扩展性增强
- **📖 文档** - AI 使用示例和集成指南
- **🧪 测试框架** - AI 智能体交互的自动化测试

---

## 📄 许可证

MIT 许可证 - 详见 LICENSE 文件。

---

## 🌟 项目统计

- **150+ 安全工具** - 全面的安全测试武器库
- **12+ AI 智能体** - 自主决策和工作流管理
- **4000+ 漏洞模板** - Nuclei 集成，覆盖广泛
- **35+ 攻击类别** - 从 Web 应用到云基础设施
- **实时处理** - 智能缓存，亚秒级响应
- **99.9% 正常运行时间** - 容错架构，优雅降级

---

<div align="center">

## 🚀 准备好改变您的 AI 智能体了吗？

**[⭐ 给本仓库加星](https://github.com/370205504-cmyk/hexstrike-ai)** • **[🍴 Fork 并贡献](https://github.com/370205504-cmyk/hexstrike-ai/fork)**

---

**由网络安全社区用 ❤️ 打造，致力于 AI 驱动的安全自动化**

*HexStrike AI v6.0 - 人工智能与网络安全卓越的交汇点*

</div>
