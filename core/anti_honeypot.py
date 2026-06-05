#!/usr/bin/env python3
"""
Anti-Honeypot - 蜜罐检测与对抗系统
对可疑 IP 进行交互延迟及响应模式分析
"""

import logging
import time
import random
from typing import Dict, List, Any, Optional
from enum import Enum

logger = logging.getLogger("AntiHoneypot")


class HoneypotIndicator(Enum):
    """蜜罐指标"""
    UNUSUAL_PORT = "unusual_port"
    UNREALISTIC_RESPONSE = "unrealistic_response"
    LOW_INTERACTION = "low_interaction"
    DELIBERATE_VULNERABILITIES = "deliberate_vulnerabilities"
    RAPID_RESPONSE = "rapid_response"
    STATIC_RESPONSE = "static_response"


class HoneypotRiskLevel(Enum):
    """风险等级"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AntiHoneypotSystem:
    """反蜜罐系统"""

    def __init__(self):
        self.suspicious_ips = set()
        self.analysis_history = {}
        logger.info("🕵️  反蜜罐系统初始化完成")

    def analyze_target(self, target: str, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析目标是否为蜜罐"""
        logger.info(f"🔍 分析目标: {target}")
        
        indicators = []
        score = 0
        
        # 分析响应延迟
        avg_delay = sum(r.get("delay", 0) for r in responses) / len(responses) if responses else 0
        if avg_delay < 0.01:
            indicators.append(HoneypotIndicator.RAPID_RESPONSE)
            score += 20
        
        # 分析响应一致性
        responses_content = [r.get("content", "") for r in responses]
        if len(set(responses_content)) == 1 and len(responses) > 1:
            indicators.append(HoneypotIndicator.STATIC_RESPONSE)
            score += 30
        
        # 分析交互水平
        interaction_level = self._assess_interaction_level(responses)
        if interaction_level < 0.3:
            indicators.append(HoneypotIndicator.LOW_INTERACTION)
            score += 40
        
        # 确定风险等级
        risk_level = self._calculate_risk_level(score)
        
        result = {
            "target": target,
            "risk_score": score,
            "risk_level": risk_level.value,
            "indicators": [i.value for i in indicators],
            "is_likely_honeypot": score >= 50,
            "analysis_timestamp": time.time()
        }
        
        self.analysis_history[target] = result
        
        if result["is_likely_honeypot"]:
            logger.warning(f"⚠️  检测到可能的蜜罐: {target} (分数: {score})")
            self.suspicious_ips.add(target)
        else:
            logger.info(f"✅ 目标 {target} 看起来是安全的 (分数: {score})")
        
        return result

    def _assess_interaction_level(self, responses: List[Dict[str, Any]]) -> float:
        """评估交互水平"""
        if not responses:
            return 0.0
        
        # 简单的交互评分逻辑
        score = 0.0
        for r in responses:
            # 响应长度
            if len(r.get("content", "")) > 100:
                score += 0.2
            # 变化的响应头
            if r.get("headers_changed", False):
                score += 0.2
            # 错误处理
            if "error" in r.get("content", "").lower():
                score += 0.1
        
        return min(1.0, score)

    def _calculate_risk_level(self, score: int) -> HoneypotRiskLevel:
        """计算风险等级"""
        if score < 10:
            return HoneypotRiskLevel.SAFE
        elif score < 30:
            return HoneypotRiskLevel.LOW
        elif score < 50:
            return HoneypotRiskLevel.MEDIUM
        elif score < 70:
            return HoneypotRiskLevel.HIGH
        else:
            return HoneypotRiskLevel.CRITICAL

    def add_interactive_delay(self, min_delay: float = 2.0, max_delay: float = 10.0):
        """添加交互延迟以避免被蜜罐检测"""
        delay = random.uniform(min_delay, max_delay)
        logger.info(f"⏱️  添加交互延迟: {delay:.2f}s")
        time.sleep(delay)

    def randomize_request_patterns(self, num_requests: int) -> List[float]:
        """随机化请求模式"""
        delays = []
        for _ in range(num_requests):
            delay = random.uniform(0.5, 5.0)
            delays.append(delay)
            logger.debug(f"计划请求延迟: {delay:.2f}s")
        return delays

    def get_suspicious_targets(self) -> List[str]:
        """获取可疑目标列表"""
        return list(self.suspicious_ips)

    def get_analysis_history(self, target: Optional[str] = None) -> Dict[str, Any]:
        """获取分析历史"""
        if target:
            return self.analysis_history.get(target, {})
        return self.analysis_history


class ResponseAnalyzer:
    """响应分析器"""

    def __init__(self):
        self.baseline_responses = {}

    def set_baseline(self, service: str, response: str):
        """设置基准响应"""
        self.baseline_responses[service] = response
        logger.info(f"📊 设置 {service} 的基准响应")

    def compare_to_baseline(self, service: str, response: str) -> Dict[str, Any]:
        """与基准响应比较"""
        if service not in self.baseline_responses:
            return {"match": False, "reason": "No baseline"}
        
        baseline = self.baseline_responses[service]
        similarity = self._calculate_similarity(baseline, response)
        
        return {
            "match": similarity > 0.9,
            "similarity": similarity,
            "is_suspicious": similarity > 0.95  # 完全一样可能是蜜罐
        }

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算字符串相似度"""
        if not str1 or not str2:
            return 0.0
        
        # 简单的相似度计算
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0

