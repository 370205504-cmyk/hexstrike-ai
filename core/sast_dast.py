#!/usr/bin/env python3
"""
SAST/DAST - 代码与业务逻辑安全审计
引入 SAST/DAST 工具进行深层代码审计
"""

import logging
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger("SASTDAST")


class VulnerabilitySeverity(Enum):
    """漏洞严重程度"""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SASTAnalyzer:
    """静态应用安全测试分析器"""

    def __init__(self):
        self.supported_tools = ["semgrep", "bandit", "eslint", "pmd"]
        logger.info("🔬 SAST 分析器初始化完成")

    def scan_codebase(self, code_dir: str, language: str = "python") -> Dict[str, Any]:
        """扫描代码库"""
        logger.info(f"📁 扫描代码库: {code_dir} (语言: {language})")
        
        results = {
            "scan_type": "sast",
            "language": language,
            "target": code_dir,
            "vulnerabilities": [],
            "summary": {}
        }
        
        # 根据语言选择工具
        if language == "python":
            tool = "bandit"
        elif language in ["javascript", "typescript"]:
            tool = "eslint"
        else:
            tool = "semgrep"
        
        # 执行扫描（模拟）
        results["vulnerabilities"] = self._simulate_sast_scan(language)
        results["summary"] = self._summarize_vulnerabilities(results["vulnerabilities"])
        
        return results

    def _simulate_sast_scan(self, language: str) -> List[Dict[str, Any]]:
        """模拟 SAST 扫描结果"""
        vulnerabilities = [
            {
                "id": "SAST-001",
                "severity": VulnerabilitySeverity.HIGH.value,
                "title": "SQL Injection Vulnerability",
                "description": "User input directly concatenated into SQL query",
                "file": "src/auth.py",
                "line": 42,
                "recommendation": "Use parameterized queries"
            },
            {
                "id": "SAST-002",
                "severity": VulnerabilitySeverity.MEDIUM.value,
                "title": "Hardcoded API Key",
                "description": "API key found in source code",
                "file": "src/config.py",
                "line": 15,
                "recommendation": "Use environment variables"
            },
            {
                "id": "SAST-003",
                "severity": VulnerabilitySeverity.LOW.value,
                "title": "Weak Random Number Generator",
                "description": "Insecure random function used",
                "file": "src/utils.py",
                "line": 89,
                "recommendation": "Use secrets module"
            }
        ]
        return vulnerabilities

    def _summarize_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """统计漏洞"""
        summary = {
            "total": len(vulnerabilities),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "info")
            if severity in summary:
                summary[severity] += 1
        
        return summary


class DASTAnalyzer:
    """动态应用安全测试分析器"""

    def __init__(self):
        self.supported_tools = ["owasp-zap", "burpsuite", "nikto", "nuclei"]
        logger.info("🌐 DAST 分析器初始化完成")

    def scan_web_app(self, target_url: str, scan_type: str = "full") -> Dict[str, Any]:
        """扫描 Web 应用"""
        logger.info(f"🕸️  扫描 Web 应用: {target_url} (类型: {scan_type})")
        
        results = {
            "scan_type": "dast",
            "target": target_url,
            "scan_mode": scan_type,
            "vulnerabilities": [],
            "summary": {}
        }
        
        # 执行扫描（模拟）
        results["vulnerabilities"] = self._simulate_dast_scan(target_url)
        results["summary"] = self._summarize_vulnerabilities(results["vulnerabilities"])
        
        return results

    def _simulate_dast_scan(self, url: str) -> List[Dict[str, Any]]:
        """模拟 DAST 扫描结果"""
        vulnerabilities = [
            {
                "id": "DAST-001",
                "severity": VulnerabilitySeverity.CRITICAL.value,
                "title": "Remote Code Execution",
                "description": "Unauthenticated RCE via file upload",
                "endpoint": "/upload",
                "method": "POST",
                "recommendation": "Validate file types and sanitize"
            },
            {
                "id": "DAST-002",
                "severity": VulnerabilitySeverity.HIGH.value,
                "title": "Broken Authentication",
                "description": "JWT token not properly validated",
                "endpoint": "/api/v1/user",
                "method": "GET",
                "recommendation": "Implement proper JWT validation"
            },
            {
                "id": "DAST-003",
                "severity": VulnerabilitySeverity.MEDIUM.value,
                "title": "Cross-Site Scripting (XSS)",
                "description": "Reflected XSS in search parameter",
                "endpoint": "/search",
                "method": "GET",
                "recommendation": "Encode output and use CSP"
            },
            {
                "id": "DAST-004",
                "severity": VulnerabilitySeverity.LOW.value,
                "title": "Information Disclosure",
                "description": "Server version exposed in headers",
                "endpoint": "/",
                "method": "GET",
                "recommendation": "Remove version information"
            }
        ]
        return vulnerabilities

    def _summarize_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """统计漏洞"""
        summary = {
            "total": len(vulnerabilities),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "info")
            if severity in summary:
                summary[severity] += 1
        
        return summary


class LogicVulnerabilityAnalyzer:
    """业务逻辑漏洞分析器"""

    def __init__(self):
        logger.info("🧠 业务逻辑漏洞分析器初始化完成")

    def analyze_logic_flows(self, endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析业务逻辑流程"""
        logger.info("🔄 分析业务逻辑流程")
        
        issues = []
        
        # 检查越权访问
        for endpoint in endpoints:
            if not endpoint.get("requires_auth", False):
                issues.append({
                    "type": "missing_auth",
                    "severity": VulnerabilitySeverity.HIGH.value,
                    "endpoint": endpoint.get("url"),
                    "description": "Endpoint does not require authentication"
                })
            
            if endpoint.get("method") in ["POST", "PUT", "DELETE"]:
                if not endpoint.get("has_csrf", False):
                    issues.append({
                        "type": "missing_csrf",
                        "severity": VulnerabilitySeverity.MEDIUM.value,
                        "endpoint": endpoint.get("url"),
                        "description": "State-changing request without CSRF protection"
                    })
        
        return {
            "analysis_type": "logic",
            "total_endpoints": len(endpoints),
            "issues": issues,
            "summary": {
                "total_issues": len(issues),
                "critical": sum(1 for i in issues if i["severity"] == "critical"),
                "high": sum(1 for i in issues if i["severity"] == "high"),
                "medium": sum(1 for i in issues if i["severity"] == "medium"),
                "low": sum(1 for i in issues if i["severity"] == "low")
            }
        }

    def detect_idor_vulnerabilities(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """检测不安全的直接对象引用 (IDOR)"""
        logger.info("🔑 检测 IDOR 漏洞")
        
        vulnerabilities = []
        
        for test in test_cases:
            if test.get("authorized_user") and test.get("unauthorized_user"):
                if test.get("unauthorized_can_access", False):
                    vulnerabilities.append({
                        "type": "idor",
                        "severity": VulnerabilitySeverity.HIGH.value,
                        "resource": test.get("resource"),
                        "description": "Unauthorized user can access restricted resource"
                    })
        
        return vulnerabilities

