#!/usr/bin/env python3
"""
Multi-Model Collaboration - 多模型协同系统
不同专精的 AI 模型协同决策
"""

import json
import logging
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("MultiModelCollaboration")


class AgentSpecialty(Enum):
    """智能体专长"""
    RECONNAISSANCE = "reconnaissance"
    VULNERABILITY_ANALYSIS = "vulnerability_analysis"
    EXPLOITATION = "exploitation"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    POST_EXPLOITATION = "post_exploitation"
    REFEREE = "referee"


@dataclass
class AgentOpinion:
    """智能体意见"""
    agent_name: str
    specialty: AgentSpecialty
    recommendation: str
    confidence: float
    reasoning: str
    timestamp: datetime


@dataclass
class FinalDecision:
    """最终决策"""
    task: str
    chosen_approach: str
    supporting_opinions: List[AgentOpinion]
    referee_justification: str
    timestamp: datetime


class BaseSpecializedAgent:
    """基础专业化智能体"""

    def __init__(self, name: str, specialty: AgentSpecialty):
        self.name = name
        self.specialty = specialty
        logger.info(f"🤖 初始化智能体: {name} ({specialty.value})")

    def analyze(self, task: str, context: Dict[str, Any]) -> AgentOpinion:
        """分析任务并给出意见"""
        raise NotImplementedError("子类必须实现此方法")


class ReconnaissanceAgent(BaseSpecializedAgent):
    """侦察智能体"""

    def __init__(self):
        super().__init__("ReconExpert", AgentSpecialty.RECONNAISSANCE)

    def analyze(self, task: str, context: Dict[str, Any]) -> AgentOpinion:
        target = context.get("target", "unknown")
        return AgentOpinion(
            agent_name=self.name,
            specialty=self.specialty,
            recommendation=f"建议使用 nmap 进行端口扫描，然后用 gobuster 枚举目录",
            confidence=0.9,
            reasoning=f"目标 {target} 需要全面的信息收集",
            timestamp=datetime.now()
        )


class VulnerabilityAnalysisAgent(BaseSpecializedAgent):
    """漏洞分析智能体"""

    def __init__(self):
        super().__init__("VulnAnalyzer", AgentSpecialty.VULNERABILITY_ANALYSIS)

    def analyze(self, task: str, context: Dict[str, Any]) -> AgentOpinion:
        return AgentOpinion(
            agent_name=self.name,
            specialty=self.specialty,
            recommendation="建议使用 Nuclei 扫描常见漏洞，然后用 SQLMap 测试 SQL 注入",
            confidence=0.85,
            reasoning="基于目标架构，Web 漏洞可能性较高",
            timestamp=datetime.now()
        )


class ExploitationAgent(BaseSpecializedAgent):
    """漏洞利用智能体"""

    def __init__(self):
        super().__init__("ExploitMaster", AgentSpecialty.EXPLOITATION)

    def analyze(self, task: str, context: Dict[str, Any]) -> AgentOpinion:
        return AgentOpinion(
            agent_name=self.name,
            specialty=self.specialty,
            recommendation="使用 Metasploit 框架或自定义利用代码",
            confidence=0.8,
            reasoning="需要根据具体漏洞选择合适的利用方式",
            timestamp=datetime.now()
        )


class RefereeAgent(BaseSpecializedAgent):
    """仲裁智能体"""

    def __init__(self):
        super().__init__("Referee", AgentSpecialty.REFEREE)

    def resolve(self, opinions: List[AgentOpinion], task: str) -> FinalDecision:
        """仲裁并做出最终决策"""
        logger.info(f"⚖️  仲裁智能体正在评估 {len(opinions)} 个意见")
        
        # 简单的加权决策策略
        sorted_opinions = sorted(opinions, key=lambda x: x.confidence, reverse=True)
        best_opinion = sorted_opinions[0]
        
        return FinalDecision(
            task=task,
            chosen_approach=best_opinion.recommendation,
            supporting_opinions=sorted_opinions[:3],
            referee_justification=f"基于置信度选择 {best_opinion.agent_name} 的方案，置信度 {best_opinion.confidence:.2f}",
            timestamp=datetime.now()
        )


class MultiModelCollaborationSystem:
    """多模型协同系统"""

    def __init__(self):
        self.agents = [
            ReconnaissanceAgent(),
            VulnerabilityAnalysisAgent(),
            ExploitationAgent()
        ]
        self.referee = RefereeAgent()
        logger.info("🤝 多模型协同系统初始化完成")

    def collaborate(self, task: str, context: Dict[str, Any]) -> FinalDecision:
        """协同决策"""
        logger.info(f"🎯 开始协同决策: {task}")
        
        # 收集所有智能体的意见
        opinions = []
        for agent in self.agents:
            try:
                opinion = agent.analyze(task, context)
                opinions.append(opinion)
                logger.info(f"📝 {agent.name}: {opinion.recommendation} (置信度: {opinion.confidence:.2f})")
            except Exception as e:
                logger.error(f"❌ 智能体 {agent.name} 分析失败: {e}")
        
        # 仲裁智能体做出最终决策
        final_decision = self.referee.resolve(opinions, task)
        
        logger.info(f"✅ 最终决策: {final_decision.chosen_approach}")
        return final_decision

    def get_all_agent_status(self) -> List[Dict[str, Any]]:
        """获取所有智能体状态"""
        return [
            {
                "name": agent.name,
                "specialty": agent.specialty.value,
                "status": "active"
            } for agent in self.agents
        ] + [
            {
                "name": self.referee.name,
                "specialty": self.referee.specialty.value,
                "status": "active",
                "role": "referee"
            }
        ]

