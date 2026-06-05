#!/usr/bin/env python3
"""
Intelligent Decision Engine - 智能决策引擎
构建完整攻击链，自主规划渗透测试路径
"""

import json
import logging
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("IntelligentDecisionEngine")


class TaskPhase(Enum):
    """任务阶段枚举"""
    RECONNAISSANCE = "reconnaissance"
    VULNERABILITY_DISCOVERY = "vulnerability_discovery"
    EXPLOITATION = "exploitation"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    POST_EXPLOITATION = "post_exploitation"
    REPORTING = "reporting"


@dataclass
class AttackStep:
    """攻击步骤"""
    phase: TaskPhase
    tool: str
    parameters: Dict[str, Any]
    description: str
    expected_result: str
    dependencies: List[str]
    priority: int = 5


@dataclass
class AttackChain:
    """完整攻击链"""
    target: str
    steps: List[AttackStep]
    start_time: datetime
    status: str = "planning"
    current_step: int = 0
    execution_results: List[Dict] = None

    def __post_init__(self):
        if self.execution_results is None:
            self.execution_results = []


class IntelligentDecisionEngine:
    """智能决策引擎 - 核心策略大脑"""

    def __init__(self):
        self.attack_patterns = self._load_attack_patterns()
        self.phase_transitions = self._define_phase_transitions()
        logger.info("🧠 智能决策引擎初始化完成")

    def _load_attack_patterns(self) -> Dict[str, Any]:
        """加载攻击模式库"""
        return {
            "web_application": {
                "phases": [
                    TaskPhase.RECONNAISSANCE,
                    TaskPhase.VULNERABILITY_DISCOVERY,
                    TaskPhase.EXPLOITATION,
                    TaskPhase.POST_EXPLOITATION,
                    TaskPhase.REPORTING
                ],
                "tool_recommendations": {
                    TaskPhase.RECONNAISSANCE: ["nmap", "gobuster", "httpx", "wafw00f"],
                    TaskPhase.VULNERABILITY_DISCOVERY: ["nuclei", "nikto", "sqlmap", "arjun"],
                    TaskPhase.EXPLOITATION: ["sqlmap", "metasploit", "hydra"],
                    TaskPhase.PRIVILEGE_ESCALATION: ["linpeas", "winpeas"],
                    TaskPhase.POST_EXPLOITATION: ["mimikatz", "bloodhound"],
                }
            },
            "network_infrastructure": {
                "phases": [
                    TaskPhase.RECONNAISSANCE,
                    TaskPhase.VULNERABILITY_DISCOVERY,
                    TaskPhase.EXPLOITATION,
                    TaskPhase.PRIVILEGE_ESCALATION,
                    TaskPhase.POST_EXPLOITATION,
                    TaskPhase.REPORTING
                ],
                "tool_recommendations": {
                    TaskPhase.RECONNAISSANCE: ["nmap", "masscan", "enum4linux-ng", "amass"],
                    TaskPhase.VULNERABILITY_DISCOVERY: ["nuclei", "openvas"],
                    TaskPhase.EXPLOITATION: ["metasploit", "hydra", "netexec"],
                }
            }
        }

    def _define_phase_transitions(self) -> Dict[TaskPhase, List[TaskPhase]]:
        """定义阶段转换规则"""
        return {
            TaskPhase.RECONNAISSANCE: [TaskPhase.VULNERABILITY_DISCOVERY],
            TaskPhase.VULNERABILITY_DISCOVERY: [TaskPhase.EXPLOITATION, TaskPhase.REPORTING],
            TaskPhase.EXPLOITATION: [TaskPhase.PRIVILEGE_ESCALATION, TaskPhase.POST_EXPLOITATION, TaskPhase.REPORTING],
            TaskPhase.PRIVILEGE_ESCALATION: [TaskPhase.POST_EXPLOITATION, TaskPhase.REPORTING],
            TaskPhase.POST_EXPLOITATION: [TaskPhase.REPORTING],
        }

    def analyze_target(self, target: str, target_type: str = "web_application") -> Dict[str, Any]:
        """分析目标并生成初步评估"""
        logger.info(f"🔍 开始分析目标: {target}")
        return {
            "target": target,
            "type": target_type,
            "recommended_pattern": self.attack_patterns.get(target_type, self.attack_patterns["web_application"]),
            "confidence": 0.8,
            "timestamp": datetime.now().isoformat()
        }

    def build_attack_chain(self, target: str, target_info: Dict[str, Any]) -> AttackChain:
        """构建完整攻击链"""
        logger.info(f"⚔️  为目标 {target} 构建攻击链")
        
        pattern = target_info.get("recommended_pattern", self.attack_patterns["web_application"])
        phases = pattern["phases"]
        tool_recs = pattern["tool_recommendations"]
        
        steps = []
        for phase in phases:
            if phase in tool_recs:
                for idx, tool in enumerate(tool_recs[phase]):
                    step = AttackStep(
                        phase=phase,
                        tool=tool,
                        parameters={"target": target},
                        description=f"{phase.value} 使用 {tool}",
                        expected_result=f"{tool} 执行结果",
                        dependencies=steps[-1].tool if steps else [],
                        priority=10 - idx
                    )
                    steps.append(step)
        
        return AttackChain(
            target=target,
            steps=steps,
            start_time=datetime.now()
        )

    def select_next_step(self, attack_chain: AttackChain, current_result: Dict[str, Any]) -> Optional[AttackStep]:
        """根据当前结果选择下一步"""
        if attack_chain.current_step >= len(attack_chain.steps):
            logger.info("✅ 攻击链已完成")
            return None
        
        next_step = attack_chain.steps[attack_chain.current_step]
        logger.info(f"➡️  下一步: {next_step.description}")
        return next_step

    def update_chain_based_on_result(self, attack_chain: AttackChain, step_result: Dict[str, Any]) -> AttackChain:
        """根据执行结果动态调整攻击链"""
        attack_chain.execution_results.append(step_result)
        
        if step_result.get("success"):
            logger.info("✅ 步骤执行成功，继续攻击链")
            attack_chain.current_step += 1
        else:
            logger.warning("❌ 步骤执行失败，评估替代方案")
            # 这里可以实现替代策略选择
            attack_chain.current_step += 1
        
        return attack_chain

    def evaluate_risk(self, attack_step: AttackStep) -> Dict[str, float]:
        """评估攻击步骤的风险"""
        risk_factors = {
            "noise_level": 0.3,
            "detection_chance": 0.2,
            "success_probability": 0.7
        }
        return risk_factors


class FailureRecoverySystem:
    """故障恢复系统 - 错误分类与恢复逻辑"""

    class ErrorCategory(Enum):
        """错误分类"""
        TOOL_NOT_FOUND = "tool_not_found"
        PERMISSION_DENIED = "permission_denied"
        NETWORK_ERROR = "network_error"
        TIMEOUT = "timeout"
        UNKNOWN_ERROR = "unknown_error"

    def __init__(self):
        self.recovery_strategies = {
            self.ErrorCategory.TOOL_NOT_FOUND: self._recover_tool_not_found,
            self.ErrorCategory.PERMISSION_DENIED: self._recover_permission_denied,
            self.ErrorCategory.NETWORK_ERROR: self._recover_network_error,
            self.ErrorCategory.TIMEOUT: self._recover_timeout,
            self.ErrorCategory.UNKNOWN_ERROR: self._recover_unknown_error,
        }
        self.error_history = []
        logger.info("🛡️  故障恢复系统初始化完成")

    def classify_error(self, error_message: str, error_output: str = "") -> ErrorCategory:
        """错误分类"""
        err_lower = error_message.lower() + " " + error_output.lower()
        
        if any(keyword in err_lower for keyword in ["command not found", "no such file", "not installed"]):
            return self.ErrorCategory.TOOL_NOT_FOUND
        elif any(keyword in err_lower for keyword in ["permission denied", "access denied", "forbidden"]):
            return self.ErrorCategory.PERMISSION_DENIED
        elif any(keyword in err_lower for keyword in ["connection refused", "network unreachable", "timeout"]):
            return self.ErrorCategory.NETWORK_ERROR
        elif any(keyword in err_lower for keyword in ["timed out", "timeout"]):
            return self.ErrorCategory.TIMEOUT
        else:
            return self.ErrorCategory.UNKNOWN_ERROR

    def attempt_recovery(self, error_category: ErrorCategory, context: Dict[str, Any]) -> Dict[str, Any]:
        """尝试恢复"""
        logger.info(f"🔧 尝试从 {error_category.value} 恢复...")
        strategy = self.recovery_strategies.get(error_category, self._recover_unknown_error)
        return strategy(context)

    def _recover_tool_not_found(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """工具未找到恢复策略"""
        tool = context.get("tool")
        alternatives = context.get("alternatives", [])
        return {
            "retry": False,
            "alternative_tools": alternatives,
            "suggestion": f"尝试安装 {tool} 或使用替代工具"
        }

    def _recover_permission_denied(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """权限拒绝恢复策略"""
        return {
            "retry": True,
            "elevate_privileges": True,
            "suggestion": "尝试提升权限或使用不同的方法"
        }

    def _recover_network_error(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """网络错误恢复策略"""
        return {
            "retry": True,
            "retry_count": 3,
            "delay_between_retries": 5,
            "suggestion": "等待网络恢复并重试"
        }

    def _recover_timeout(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """超时恢复策略"""
        return {
            "retry": True,
            "increase_timeout": True,
            "suggestion": "增加超时时间并重试"
        }

    def _recover_unknown_error(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """未知错误恢复策略"""
        return {
            "retry": True,
            "log_detailed": True,
            "suggestion": "记录详细日志并尝试不同方法"
        }

    def record_error(self, error_info: Dict[str, Any]):
        """记录错误历史"""
        error_info["timestamp"] = datetime.now().isoformat()
        self.error_history.append(error_info)
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-100:]

    def get_common_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取常见错误"""
        # 简单的频率统计
        from collections import Counter
        error_types = [e.get("category", "unknown") for e in self.error_history]
        return [{"type": t, "count": c} for t, c in Counter(error_types).most_common(limit)]

