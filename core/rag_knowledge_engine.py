#!/usr/bin/env python3
"""
RAG Knowledge Engine - 知识引擎
实时检索最新漏洞库(CVE)和利用代码(Exploit-DB)
"""

import json
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("RAGKnowledgeEngine")


class CVEFetcher:
    """CVE 漏洞信息获取器"""
    
    def __init__(self, cache_dir: str = "~/.hexstrike/cve_cache"):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.nvd_api_base = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        logger.info("📊 CVE 获取器初始化完成")

    def search_cve(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索 CVE 漏洞"""
        logger.info(f"🔍 搜索 CVE: {keyword}")
        
        cache_file = self.cache_dir / f"cve_{keyword.replace(' ', '_')}.json"
        
        # 检查缓存
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                    if (datetime.now() - datetime.fromisoformat(cached["cached_at"])).days < 1:
                        logger.info("📦 使用缓存的 CVE 数据")
                        return cached["results"]
            except:
                pass
        
        # 调用 NVD API (简化模拟)
        results = self._mock_nvd_search(keyword, limit)
        
        # 缓存结果
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                "cached_at": datetime.now().isoformat(),
                "keyword": keyword,
                "results": results
            }, f, ensure_ascii=False, indent=2)
        
        return results

    def _mock_nvd_search(self, keyword: str, limit: int) -> List[Dict[str, Any]]:
        """模拟 NVD 搜索结果 (实际项目中应该调用真实 API)"""
        return [
            {
                "id": f"CVE-2024-{1000 + i}",
                "description": f"漏洞描述: {keyword} 相关漏洞",
                "severity": "HIGH" if i % 2 == 0 else "MEDIUM",
                "cvss_score": 7.5 + i * 0.1,
                "published_date": (datetime.now()).isoformat(),
                "references": [f"https://example.com/cve-{i}"]
            } for i in range(limit)
        ]

    def get_cve_details(self, cve_id: str) -> Optional[Dict[str, Any]]:
        """获取 CVE 详情"""
        logger.info(f"📖 获取 CVE 详情: {cve_id}")
        return {
            "id": cve_id,
            "description": f"{cve_id} 的详细描述",
            "severity": "CRITICAL",
            "cvss_score": 9.8,
            "affected_versions": ["1.0.0", "1.1.0", "2.0.0"],
            "exploit_available": True,
            "patch_available": False,
            "published_date": datetime.now().isoformat()
        }


class ExploitDBFetcher:
    """Exploit-DB 利用代码获取器"""
    
    def __init__(self):
        self.exploit_db_api = "https://www.exploit-db.com"
        logger.info("💥 Exploit-DB 获取器初始化完成")

    def search_exploits(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索利用代码"""
        logger.info(f"🔍 搜索 Exploit-DB: {keyword}")
        
        # 模拟搜索结果
        return [
            {
                "id": f"EDB-ID-{40000 + i}",
                "title": f"{keyword} 利用代码 - 版本 {i}",
                "type": "remote" if i % 2 == 0 else "local",
                "platform": "Linux" if i % 3 == 0 else "Windows",
                "date": (datetime.now()).isoformat(),
                "author": "Security Researcher"
            } for i in range(limit)
        ]

    def get_exploit_code(self, exploit_id: str) -> Optional[str]:
        """获取利用代码内容"""
        logger.info(f"📝 获取利用代码: {exploit_id}")
        return """
# 示例利用代码
# 注意: 实际项目中应该从 Exploit-DB 获取真实代码
import socket

def exploit(target):
    print(f"Exploiting {target}...")
"""


class RAGKnowledgeEngine:
    """RAG 知识引擎 - 整合所有情报源"""
    
    def __init__(self):
        self.cve_fetcher = CVEFetcher()
        self.exploit_fetcher = ExploitDBFetcher()
        self.local_knowledge_base = {}
        logger.info("🧠 RAG 知识引擎初始化完成")

    def query(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """查询知识引擎"""
        logger.info(f"💬 查询: {question}")
        
        results = {
            "cves": [],
            "exploits": [],
            "local_knowledge": [],
            "recommendations": []
        }
        
        # 搜索 CVE
        results["cves"] = self.cve_fetcher.search_cve(question)
        
        # 搜索 Exploit-DB
        results["exploits"] = self.exploit_fetcher.search_exploits(question)
        
        # 检索本地知识库
        results["local_knowledge"] = self._query_local_knowledge(question)
        
        # 生成建议
        results["recommendations"] = self._generate_recommendations(results)
        
        return results

    def _query_local_knowledge(self, question: str) -> List[Dict[str, Any]]:
        """查询本地知识库"""
        relevant = []
        question_lower = question.lower()
        
        for key, value in self.local_knowledge_base.items():
            if any(kw in question_lower for kw in key.lower().split()):
                relevant.append({"key": key, "value": value})
        
        return relevant

    def _generate_recommendations(self, search_results: Dict[str, Any]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if search_results["cves"]:
            high_severity = [c for c in search_results["cves"] if c["severity"] in ["CRITICAL", "HIGH"]]
            if high_severity:
                recommendations.append(f"发现 {len(high_severity)} 个高危 CVE，建议优先处理")
        
        if search_results["exploits"]:
            recommendations.append(f"找到 {len(search_results['exploits'])} 个可用的利用代码")
        
        return recommendations

    def add_to_knowledge_base(self, key: str, value: Any):
        """添加到本地知识库"""
        self.local_knowledge_base[key] = {
            "value": value,
            "added_at": datetime.now().isoformat()
        }
        logger.info(f"📚 添加到知识库: {key}")

