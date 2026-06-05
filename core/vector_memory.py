#!/usr/bin/env python3
"""
Vector Memory - 向量记忆系统
使用向量数据库存储历史扫描结果和攻击链
"""

import json
import logging
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("VectorMemory")

# Try to import vector DB libraries
try:
    import numpy as np
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    logger.warning("NumPy not available, using simple memory implementation")


class MemoryItem:
    """记忆项"""

    def __init__(self, content: str, metadata: Dict[str, Any], embedding: Optional[List[float]] = None):
        self.id = hashlib.md5(content.encode()).hexdigest()[:12]
        self.content = content
        self.metadata = metadata
        self.embedding = embedding
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
            "embedding": self.embedding,
            "timestamp": self.timestamp
        }


class VectorMemoryStore:
    """向量记忆存储"""

    def __init__(self, storage_dir: str = "~/.hexstrike/vector_memory"):
        self.storage_dir = Path(storage_dir).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.storage_dir / "memory_store.json"
        self.memories: List[MemoryItem] = []
        self._load_memories()
        logger.info(f"🧠 向量记忆系统初始化完成，已加载 {len(self.memories)} 条记忆")

    def _load_memories(self):
        """从磁盘加载记忆"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item_data in data:
                        item = MemoryItem(
                            content=item_data["content"],
                            metadata=item_data["metadata"],
                            embedding=item_data.get("embedding")
                        )
                        item.id = item_data["id"]
                        item.timestamp = item_data["timestamp"]
                        self.memories.append(item)
            except Exception as e:
                logger.error(f"加载记忆失败: {e}")

    def _save_memories(self):
        """保存记忆到磁盘"""
        data = [item.to_dict() for item in self.memories]
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_memory(self, content: str, metadata: Dict[str, Any], embedding: Optional[List[float]] = None) -> str:
        """添加记忆"""
        item = MemoryItem(content, metadata, embedding)
        self.memories.append(item)
        self._save_memories()
        logger.info(f"📝 添加记忆: {item.id}")
        return item.id

    def search_memories(self, query: str, top_k: int = 5, filter_metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """搜索记忆"""
        logger.info(f"🔍 搜索记忆: {query}")
        
        # Simple keyword-based search (fallback if vector search not available)
        query_lower = query.lower()
        results = []
        
        for item in reversed(self.memories):  # Newest first
            # Apply metadata filter
            if filter_metadata:
                match = True
                for key, value in filter_metadata.items():
                    if item.metadata.get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            # Simple relevance score
            relevance = 0
            content_lower = item.content.lower()
            if query_lower in content_lower:
                relevance += 10
            for keyword in query_lower.split():
                if keyword in content_lower:
                    relevance += 1
            
            if relevance > 0:
                results.append({
                    "id": item.id,
                    "content": item.content,
                    "metadata": item.metadata,
                    "relevance": relevance,
                    "timestamp": item.timestamp
                })
        
        # Sort by relevance and limit
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:top_k]

    def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取记忆"""
        for item in self.memories:
            if item.id == memory_id:
                return item.to_dict()
        return None

    def get_memories_by_metadata(self, metadata_filter: Dict[str, Any]) -> List[Dict[str, Any]]:
        """根据元数据获取记忆"""
        results = []
        for item in self.memories:
            match = True
            for key, value in metadata_filter.items():
                if item.metadata.get(key) != value:
                    match = False
                    break
            if match:
                results.append(item.to_dict())
        return results

    def store_scan_result(self, target: str, tool: str, result: Dict[str, Any]):
        """存储扫描结果"""
        content = json.dumps(result, ensure_ascii=False)
        metadata = {
            "type": "scan_result",
            "target": target,
            "tool": tool,
            "success": result.get("success", False)
        }
        return self.add_memory(content, metadata)

    def store_attack_chain(self, target: str, attack_chain: Dict[str, Any]):
        """存储攻击链"""
        content = json.dumps(attack_chain, ensure_ascii=False)
        metadata = {
            "type": "attack_chain",
            "target": target,
            "status": attack_chain.get("status", "planned")
        }
        return self.add_memory(content, metadata)

    def get_relevant_experiences(self, target: str, task_type: str) -> List[Dict[str, Any]]:
        """获取相关经验"""
        filter_meta = {"type": "scan_result", "target": target}
        results = self.get_memories_by_metadata(filter_meta)
        
        if not results:
            # If no exact match, search by target and task type
            results = self.search_memories(f"{target} {task_type}", top_k=10)
        
        return results

    def clear_old_memories(self, days: int = 30):
        """清除旧记忆"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_iso = cutoff.isoformat()
        
        old_count = len(self.memories)
        self.memories = [
            item for item in self.memories
            if item.timestamp >= cutoff_iso
        ]
        removed = old_count - len(self.memories)
        
        if removed > 0:
            self._save_memories()
            logger.info(f"🗑️  清除了 {removed} 条旧记忆")


class SimpleEmbeddingGenerator:
    """简单的嵌入生成器（模拟）"""

    def generate_embedding(self, text: str) -> List[float]:
        """生成文本嵌入（模拟）"""
        # Simple hash-based embedding for demonstration
        import hashlib
        import struct
        
        hash_bytes = hashlib.sha256(text.encode()).digest()
        embedding = []
        for i in range(0, 32, 4):
            val = struct.unpack('f', hash_bytes[i:i+4])[0]
            embedding.append(val % 1.0)
        
        # Normalize
        norm = sum(x**2 for x in embedding)**0.5 or 1
        return [x / norm for x in embedding]

