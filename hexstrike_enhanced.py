#!/usr/bin/env python3
"""
HexStrike AI 增强版 - 自动进化、自动升级、自我迭代、长记忆系统
"""

import os
import json
import time
import hashlib
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict
import yaml

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HexStrikeEnhanced")


class LongTermMemory:
    """长期记忆系统 - 存储历史经验、成功案例、失败教训"""
    
    def __init__(self, memory_dir: str = "~/.hexstrike/memory"):
        self.memory_dir = Path(memory_dir).expanduser()
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 不同类型的记忆
        self.experience_db = self.memory_dir / "experiences.json"
        self.success_db = self.memory_dir / "success_cases.json"
        self.failure_db = self.memory_dir / "failure_cases.json"
        self.knowledge_db = self.memory_dir / "knowledge.json"
        
        # 加载现有记忆
        self.memories = self._load_memories()
        
    def _load_memories(self) -> Dict[str, Any]:
        """加载所有记忆"""
        memories = {
            "experiences": [],
            "success_cases": [],
            "failure_cases": [],
            "knowledge": {},
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_recalls": 0,
                "total_stores": 0
            }
        }
        
        for db_name, db_path in [
            ("experiences", self.experience_db),
            ("success_cases", self.success_db),
            ("failure_cases", self.failure_db),
            ("knowledge", self.knowledge_db),
        ]:
            if db_path.exists():
                try:
                    with open(db_path, 'r', encoding='utf-8') as f:
                        if db_name == "knowledge":
                            memories[db_name] = json.load(f)
                        else:
                            memories[db_name] = json.load(f)
                except Exception as e:
                    logger.warning(f"加载 {db_name} 失败: {e}")
        
        return memories
    
    def _save_memories(self):
        """保存记忆到磁盘"""
        for db_name, db_path in [
            ("experiences", self.experience_db),
            ("success_cases", self.success_db),
            ("failure_cases", self.failure_db),
            ("knowledge", self.knowledge_db),
        ]:
            try:
                with open(db_path, 'w', encoding='utf-8') as f:
                    json.dump(self.memories[db_name], f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"保存 {db_name} 失败: {e}")
    
    def store_experience(self, experience: Dict[str, Any]) -> str:
        """存储一条经验"""
        experience["id"] = hashlib.md5(str(experience).encode()).hexdigest()[:12]
        experience["timestamp"] = datetime.now().isoformat()
        experience["importance"] = experience.get("importance", 5)
        
        self.memories["experiences"].append(experience)
        self.memories["metadata"]["total_stores"] += 1
        
        # 根据结果分类
        if experience.get("success"):
            self.memories["success_cases"].append(experience)
        else:
            self.memories["failure_cases"].append(experience)
        
        self._save_memories()
        return experience["id"]
    
    def recall(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """根据查询召回相关记忆（简单关键词匹配）"""
        self.memories["metadata"]["total_recalls"] += 1
        query_lower = query.lower()
        
        relevant = []
        for exp in reversed(self.memories["experiences"]):
            content = str(exp.get("content", "") + exp.get("description", "")).lower()
            if query_lower in content:
                relevant.append(exp)
                if len(relevant) >= limit:
                    break
        
        # 如果没找到足够的，返回最近的
        if len(relevant) < limit:
            recent = [e for e in reversed(self.memories["experiences"]) if e not in relevant]
            relevant.extend(recent[:limit - len(relevant)])
        
        return relevant
    
    def get_success_patterns(self, task_type: str) -> List[Dict[str, Any]]:
        """获取特定任务类型的成功模式"""
        return [
            case for case in self.memories["success_cases"]
            if case.get("task_type") == task_type
        ]
    
    def get_failure_patterns(self, task_type: str) -> List[Dict[str, Any]]:
        """获取特定任务类型的失败模式"""
        return [
            case for case in self.memories["failure_cases"]
            if case.get("task_type") == task_type
        ]
    
    def store_knowledge(self, key: str, value: Any):
        """存储知识点"""
        self.memories["knowledge"][key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        self._save_memories()
    
    def get_knowledge(self, key: str) -> Optional[Any]:
        """获取知识点"""
        if key in self.memories["knowledge"]:
            return self.memories["knowledge"][key]["value"]
        return None


class AutoEvolutionEngine:
    """自动进化引擎 - 根据经验优化策略和参数"""
    
    def __init__(self, memory: LongTermMemory):
        self.memory = memory
        self.strategies = self._init_strategies()
        self.performance_history = []
        
    def _init_strategies(self) -> Dict[str, Any]:
        """初始化策略"""
        return {
            "tool_selection": {
                "preference": {},
                "success_rate": {},
                "last_used": {}
            },
            "parameter_tuning": {
                "optimal_params": {}
            },
            "workflow_optimization": {
                "best_practices": []
            }
        }
    
    def analyze_experience(self, experience_id: str):
        """分析一条经验并学习"""
        experiences = [e for e in self.memory.memories["experiences"] if e["id"] == experience_id]
        if not experiences:
            return
        
        exp = experiences[0]
        
        # 更新工具偏好
        if "tools_used" in exp:
            for tool in exp["tools_used"]:
                if exp["success"]:
                    if tool not in self.strategies["tool_selection"]["preference"]:
                        self.strategies["tool_selection"]["preference"][tool] = 0
                    self.strategies["tool_selection"]["preference"][tool] += 1
                
                # 更新成功率
                total = self.strategies["tool_selection"]["success_rate"].get(tool, {"success": 0, "total": 0})
                total["total"] += 1
                if exp["success"]:
                    total["success"] += 1
                self.strategies["tool_selection"]["success_rate"][tool] = total
                self.strategies["tool_selection"]["last_used"][tool] = datetime.now().isoformat()
        
        # 如果成功，记录最佳实践
        if exp["success"] and "approach" in exp:
            self.strategies["workflow_optimization"]["best_practices"].append({
                "task_type": exp.get("task_type"),
                "approach": exp["approach"],
                "result": exp.get("result"),
                "timestamp": datetime.now().isoformat()
            })
        
        # 记录性能历史
        self.performance_history.append({
            "timestamp": datetime.now().isoformat(),
            "success": exp["success"],
            "duration": exp.get("duration", 0),
            "task_type": exp.get("task_type")
        })
    
    def get_recommended_tools(self, task_type: str) -> List[str]:
        """获取推荐的工具列表（基于成功率排序）"""
        tool_scores = {}
        for tool, stats in self.strategies["tool_selection"]["success_rate"].items():
            if stats["total"] > 0:
                success_rate = stats["success"] / stats["total"]
                # 考虑使用次数和成功率
                tool_scores[tool] = success_rate * min(stats["total"], 10)
        
        sorted_tools = sorted(tool_scores.items(), key=lambda x: x[1], reverse=True)
        return [tool for tool, score in sorted_tools]
    
    def get_optimized_parameters(self, tool: str) -> Dict[str, Any]:
        """获取优化后的参数"""
        return self.strategies["parameter_tuning"]["optimal_params"].get(tool, {})
    
    def evolve_strategy(self, task_type: str):
        """根据历史数据进化策略"""
        logger.info(f"正在进化 {task_type} 任务的策略...")
        
        # 获取成功和失败案例
        successes = self.memory.get_success_patterns(task_type)
        failures = self.memory.get_failure_patterns(task_type)
        
        if successes:
            # 分析成功案例的共同特征
            logger.info(f"分析了 {len(successes)} 个成功案例")
        
        if failures:
            # 分析失败原因
            logger.info(f"分析了 {len(failures)} 个失败案例，避免重蹈覆辙")


class AutoUpgradeSystem:
    """自动升级系统 - 检查更新、下载、安装"""
    
    def __init__(self, repo_url: str = "https://github.com/370205504-cmyk/hexstrike-ai"):
        self.repo_url = repo_url
        self.current_version = self._get_current_version()
        self.update_check_interval = timedelta(hours=24)
        self.last_check = None
        
    def _get_current_version(self) -> str:
        """获取当前版本"""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--always"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            return result.stdout.strip() or "v1.0.0"
        except:
            return "v1.0.0"
    
    def check_for_updates(self) -> Tuple[bool, str]:
        """检查是否有更新"""
        self.last_check = datetime.now()
        logger.info("检查更新...")
        
        try:
            # 检查本地 git 状态
            result = subprocess.run(
                ["git", "fetch", "origin"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            # 比较本地和远程
            result = subprocess.run(
                ["git", "status", "-uno"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            if "Your branch is behind" in result.stdout:
                return True, "发现新版本！"
            
            return False, "当前是最新版本"
        except Exception as e:
            logger.warning(f"检查更新失败: {e}")
            return False, f"检查失败: {e}"
    
    def perform_upgrade(self) -> bool:
        """执行升级"""
        logger.info("开始升级...")
        
        try:
            # 拉取更新
            result = subprocess.run(
                ["git", "pull", "origin", "main"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            if result.returncode == 0:
                logger.info("代码更新成功！")
                
                # 更新依赖
                logger.info("更新依赖...")
                subprocess.run(
                    ["pip", "install", "-r", "requirements.txt", "--upgrade"],
                    cwd=Path(__file__).parent
                )
                
                self.current_version = self._get_current_version()
                logger.info(f"升级完成！当前版本: {self.current_version}")
                return True
            else:
                logger.error(f"升级失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"升级出错: {e}")
            return False


class SelfIteration:
    """自我迭代系统 - 持续优化自身"""
    
    def __init__(
        self, 
        memory: LongTermMemory, 
        evolution: AutoEvolutionEngine, 
        upgrader: AutoUpgradeSystem
    ):
        self.memory = memory
        self.evolution = evolution
        self.upgrader = upgrader
        self.iteration_count = 0
        self.last_iteration = None
        
    def iterate(self, feedback: Optional[Dict[str, Any]] = None):
        """执行一次迭代"""
        self.iteration_count += 1
        self.last_iteration = datetime.now()
        
        logger.info(f"开始第 {self.iteration_count} 次自我迭代...")
        
        # 1. 进化策略
        if feedback:
            # 如果有反馈，先存储经验
            self.memory.store_experience(feedback)
        
        # 2. 分析最近的经验
        recent_exps = self.memory.memories["experiences"][-5:]
        for exp in recent_exps:
            self.evolution.analyze_experience(exp["id"])
        
        # 3. 检查更新（周期性）
        if (self.iteration_count % 10 == 0):  # 每10次迭代检查一次更新
            has_update, msg = self.upgrader.check_for_updates()
            if has_update:
                logger.info(msg)
                # 询问或自动升级（这里只是记录）
                self.memory.store_knowledge("pending_update", True)
        
        # 4. 优化自身
        self._optimize_self()
        
        logger.info(f"第 {self.iteration_count} 次迭代完成！")
    
    def _optimize_self(self):
        """优化自身（简单示例）"""
        # 分析性能历史
        if len(self.evolution.performance_history) > 10:
            recent = self.evolution.performance_history[-10:]
            success_rate = sum(1 for h in recent if h["success"]) / len(recent)
            logger.info(f"近期成功率: {success_rate:.1%}")
            
            # 如果成功率下降，触发策略进化
            if success_rate < 0.7:
                logger.warning("成功率下降，触发策略进化...")
                task_types = set(h["task_type"] for h in recent if h["task_type"])
                for task_type in task_types:
                    self.evolution.evolve_strategy(task_type)


class EnhancedHexStrikeAgent:
    """增强版 HexStrike Agent - 整合所有功能"""
    
    def __init__(self):
        # 初始化核心组件
        self.memory = LongTermMemory()
        self.evolution = AutoEvolutionEngine(self.memory)
        self.upgrader = AutoUpgradeSystem()
        self.self_iterator = SelfIteration(
            self.memory, 
            self.evolution, 
            self.upgrader
        )
        
        logger.info("🤖 增强版 HexStrike Agent 初始化完成！")
        logger.info(f"  - 已加载 {len(self.memory.memories['experiences'])} 条经验")
        logger.info(f"  - 当前版本: {self.upgrader.current_version}")
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务并记录经验"""
        start_time = time.time()
        
        logger.info(f"开始执行任务: {task.get('description', '未知任务')}")
        
        # 1. 召回相关记忆
        related_experiences = self.memory.recall(task.get("description", ""))
        if related_experiences:
            logger.info(f"召回了 {len(related_experiences)} 条相关经验")
        
        # 2. 获取推荐工具
        recommended_tools = self.evolution.get_recommended_tools(task.get("type"))
        if recommended_tools:
            logger.info(f"推荐工具: {recommended_tools[:3]}")
        
        # 3. 执行任务（这里是示例，实际会调用真实工具）
        result = self._simulate_task_execution(task)
        
        # 4. 计算持续时间
        duration = time.time() - start_time
        
        # 5. 存储经验
        experience = {
            "task_type": task.get("type"),
            "content": task.get("description", ""),
            "tools_used": result.get("tools_used", []),
            "approach": result.get("approach"),
            "result": str(result.get("output")),
            "success": result.get("success", False),
            "duration": duration,
            "importance": result.get("importance", 5)
        }
        
        exp_id = self.memory.store_experience(experience)
        logger.info(f"经验已存储 (ID: {exp_id})")
        
        # 6. 触发自我迭代
        self.self_iterator.iterate(experience)
        
        return result
    
    def _simulate_task_execution(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """模拟任务执行（示例）"""
        # 这里应该是真实的工具调用逻辑
        # 现在先返回模拟结果
        return {
            "success": True,
            "tools_used": ["nmap", "gobuster"],
            "approach": "标准信息收集流程",
            "output": "发现开放端口 80, 443",
            "importance": 7
        }
    
    def get_status(self) -> Dict[str, Any]:
        """获取 Agent 状态"""
        return {
            "iteration_count": self.self_iterator.iteration_count,
            "total_experiences": len(self.memory.memories["experiences"]),
            "success_cases": len(self.memory.memories["success_cases"]),
            "failure_cases": len(self.memory.memories["failure_cases"]),
            "current_version": self.upgrader.current_version,
            "last_iteration": self.self_iterator.last_iteration.isoformat() if self.self_iterator.last_iteration else None
        }


def main():
    """主函数示例"""
    agent = EnhancedHexStrikeAgent()
    
    # 示例：执行几个任务
    tasks = [
        {
            "type": "reconnaissance",
            "description": "对 192.168.1.100 进行信息收集"
        },
        {
            "type": "web_vulnerability_scan",
            "description": "扫描 http://example.com 的 Web 漏洞"
        }
    ]
    
    for task in tasks:
        result = agent.execute_task(task)
        print(f"\n任务结果: {result}")
    
    # 查看状态
    status = agent.get_status()
    print(f"\nAgent 状态: {json.dumps(status, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
