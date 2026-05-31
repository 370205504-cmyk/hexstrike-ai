# 🚀 HexStrike AI 增强版 - 自动进化、自动升级、自我迭代、长记忆系统

## 📋 目录

1. [功能特性](#-功能特性)
2. [快速开始](#-快速开始)
3. [核心模块](#-核心模块)
4. [使用指南](#-使用指南)
5. [架构设计](#-架构设计)

---

## ✨ 功能特性

### 🧠 1. 长记忆系统 (LongTermMemory)
- **持久化存储**: 所有经验、成功案例、失败教训自动保存到磁盘
- **智能召回**: 根据任务关键词自动召回相关历史经验
- **分类管理**: 自动将经验分类为成功/失败，便于分析
- **知识点库**: 支持存储和检索关键知识点

### 🔄 2. 自动进化引擎 (AutoEvolutionEngine)
- **策略优化**: 根据成功率自动优化工具选择策略
- **参数调优**: 学习最佳参数组合
- **最佳实践**: 自动记录和应用最佳实践
- **成功率追踪**: 持续追踪工具使用成功率

### ⬆️ 3. 自动升级系统 (AutoUpgradeSystem)
- **版本检查**: 自动检查 GitHub 最新版本
- **一键升级**: 自动拉取代码和更新依赖
- **版本管理**: 自动记录和管理版本号

### 🔃 4. 自我迭代系统 (SelfIteration)
- **持续优化**: 每执行任务后自动优化
- **性能监控**: 实时监控成功率变化
- **策略进化**: 当性能下降时自动进化策略

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目（如果还没有克隆
git clone https://github.com/370205504-cmyk/hexstrike-ai
cd hexstrike-ai

# 激活虚拟环境
source hexstrike-dev/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 运行增强版 CLI

```bash
# 查看帮助
python cli_enhanced.py --help

# 查看状态
python cli_enhanced.py status

# 查看记忆
python cli_enhanced.py memory

# 执行任务
python cli_enhanced.py task --type reconnaissance --desc "扫描 192.168.1.100"

# 交互式模式
python cli_enhanced.py task

# 检查更新
python cli_enhanced.py check

# 执行升级
python cli_enhanced.py upgrade
```

---

## 📦 核心模块

### 🧠 LongTermMemory - 长记忆系统

```python
from hexstrike_enhanced import LongTermMemory

memory = LongTermMemory()

# 存储经验
experience = {
    "task_type": "reconnaissance",
    "content": "扫描 192.168.1.100",
    "tools_used": ["nmap", "gobuster"],
    "success": True,
    "importance": 7
}
memory.store_experience(experience)

# 召回相关经验
related = memory.recall("192.168.1.100")

# 获取成功/失败模式
successes = memory.get_success_patterns("reconnaissance")
failures = memory.get_failure_patterns("reconnaissance")
```

### 🔄 AutoEvolutionEngine - 自动进化引擎

```python
from hexstrike_enhanced import AutoEvolutionEngine, LongTermMemory

memory = LongTermMemory()
evolution = AutoEvolutionEngine(memory)

# 分析经验
evolution.analyze_experience(experience_id)

# 获取推荐工具
recommended = evolution.get_recommended_tools("reconnaissance")

# 进化策略
evolution.evolve_strategy("reconnaissance")
```

### ⬆️ AutoUpgradeSystem - 自动升级系统

```python
from hexstrike_enhanced import AutoUpgradeSystem

upgrader = AutoUpgradeSystem()

# 检查更新
has_update, message = upgrader.check_for_updates()

# 执行升级
success = upgrader.perform_upgrade()
```

### 🔃 SelfIteration - 自我迭代系统

```python
from hexstrike_enhanced import SelfIteration, LongTermMemory, AutoEvolutionEngine, AutoUpgradeSystem

iterator = SelfIteration(memory, evolution, upgrader)

# 执行迭代
iterator.iterate(feedback_experience)
```

---

## 💻 使用指南

### 基础使用示例

```python
from hexstrike_enhanced import EnhancedHexStrikeAgent

# 初始化增强版 Agent
agent = EnhancedHexStrikeAgent()

# 执行任务
task = {
    "type": "reconnaissance",
    "description": "对目标进行信息收集"
}
result = agent.execute_task(task)

# 查看状态
status = agent.get_status()
print(status)
```

### CLI 命令说明

| 命令 | 说明 |
|-----|------|
| `status` | 查看 Agent 状态（迭代次数、经验数等） |
| `memory` | 查看长期记忆系统 |
| `task` | 执行任务（可交互式/命令式） |
| `check` | 检查更新 |
| `upgrade` | 执行升级 |

---

## 🏗️ 架构设计

```
EnhancedHexStrikeAgent (主入口)
    │
    ├── LongTermMemory (长记忆系统)
    │   ├── experiences.json (经验库)
    │   ├── success_cases.json (成功案例)
    │   ├── failure_cases.json (失败教训)
    │   └── knowledge.json (知识点库)
    │
    ├── AutoEvolutionEngine (进化引擎)
    │   ├── 策略优化
    │   ├── 参数调优
    │   └── 最佳实践
    │
    ├── AutoUpgradeSystem (自动升级)
    │   ├── 版本检查
    │   ├── Git 更新
    │   └── 依赖升级
    │
    └── SelfIteration (自我迭代系统)
        ├── 持续优化
        ├── 性能监控
        └── 策略进化
```

---

## 📊 数据存储

所有数据存储在 `~/.hexstrike/` 目录：

```
~/.hexstrike/
├── config.yaml      # 配置文件
└── memory/         # 记忆系统
    ├── experiences.json   # 所有经验
    ├── success_cases.json
    ├── failure_cases.json
    └── knowledge.json
```

---

## 🎯 工作流程

1. **任务执行 → 2. **记忆召回** → 3. **工具推荐** → 4. **执行** → 5. **经验存储** → 6. **自我迭代** → 7. **策略进化**

---

## 🔒 安全提示

- 只在授权环境使用
- 建议在虚拟机或隔离环境运行
- 持续监控 Agent 行为
- 遵守当地法律法规

---

## 📚 进阶开发

### 扩展记忆系统

可以通过继承 `LongTermMemory` 类扩展功能：

```python
class AdvancedMemory(LongTermMemory):
    def recall_advanced(self, query, use_embeddings=True):
        # 更高级的召回方法
        pass
```

### 自定义进化策略

```python
class CustomEvolution(AutoEvolutionEngine):
    def custom_evolution_logic(self):
        # 自定义进化逻辑
        pass
```

---

## 📞 反馈与贡献

欢迎提交 Issue 和 PR！

---

## 📄 许可证

MIT License
