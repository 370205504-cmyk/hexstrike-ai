#!/usr/bin/env python3
"""
Langfuse Tracker - 决策追踪系统
使用 Langfuse 追踪所有决策过程，实现系统迭代优化
"""

import json
import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("LangfuseTracker")

# Try to import Langfuse - if not available, use local tracking
try:
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    logger.warning("Langfuse not available, using local tracking only")


class DecisionTrace:
    """决策追踪记录"""

    def __init__(self, task: str, context: Dict[str, Any]):
        self.trace_id = str(uuid.uuid4())
        self.task = task
        self.context = context
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.steps: List[Dict[str, Any]] = []
        self.result: Optional[Dict[str, Any]] = None
        self.status = "in_progress"

    def add_step(self, step_name: str, step_data: Dict[str, Any], step_type: str = "action"):
        """添加决策步骤"""
        self.steps.append({
            "step_name": step_name,
            "step_type": step_type,
            "data": step_data,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"📌 [{self.trace_id[:8]}] {step_name}")

    def complete(self, result: Dict[str, Any], success: bool = True):
        """完成追踪"""
        self.end_time = datetime.now()
        self.result = result
        self.status = "success" if success else "failure"
        duration = (self.end_time - self.start_time).total_seconds()
        logger.info(f"🏁 [{self.trace_id[:8]}] 完成，耗时 {duration:.2f}s")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "trace_id": self.trace_id,
            "task": self.task,
            "context": self.context,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else None,
            "steps": self.steps,
            "result": self.result,
            "status": self.status
        }


class LangfuseDecisionTracker:
    """决策追踪器"""

    def __init__(self, storage_dir: str = "~/.hexstrike/decision_traces", use_langfuse: bool = False):
        self.storage_dir = Path(storage_dir).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.traces_file = self.storage_dir / "traces.json"
        self.traces: List[DecisionTrace] = []
        self.current_trace: Optional[DecisionTrace] = None
        self.use_langfuse = use_langfuse and LANGFUSE_AVAILABLE
        self.langfuse_client = None

        if self.use_langfuse:
            try:
                self.langfuse_client = Langfuse()
                logger.info("📊 Langfuse 客户端初始化完成")
            except Exception as e:
                logger.warning(f"Langfuse 初始化失败: {e}，使用本地追踪")
                self.use_langfuse = False

        self._load_traces()
        logger.info(f"📋 决策追踪器初始化完成，已加载 {len(self.traces)} 条追踪记录")

    def _load_traces(self):
        """从磁盘加载追踪记录"""
        if self.traces_file.exists():
            try:
                with open(self.traces_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Note: We don't recreate full DecisionTrace objects, just keep as dicts for history
                    self.trace_history = data
            except Exception as e:
                logger.error(f"加载追踪记录失败: {e}")
                self.trace_history = []
        else:
            self.trace_history = []

    def _save_traces(self):
        """保存追踪记录到磁盘"""
        # Combine current traces with history
        all_traces = self.trace_history + [t.to_dict() for t in self.traces]
        
        # Keep last 1000 traces
        if len(all_traces) > 1000:
            all_traces = all_traces[-1000:]
        
        with open(self.traces_file, 'w', encoding='utf-8') as f:
            json.dump(all_traces, f, ensure_ascii=False, indent=2)

    def start_trace(self, task: str, context: Dict[str, Any]) -> str:
        """开始新的追踪"""
        self.current_trace = DecisionTrace(task, context)
        self.traces.append(self.current_trace)
        logger.info(f"🎯 开始追踪: {task} [ID: {self.current_trace.trace_id[:8]}]")
        return self.current_trace.trace_id

    def add_trace_step(self, step_name: str, step_data: Dict[str, Any], step_type: str = "action"):
        """添加追踪步骤"""
        if self.current_trace:
            self.current_trace.add_step(step_name, step_data, step_type)
            
            # Also log to Langfuse if available
            if self.use_langfuse and self.langfuse_client:
                try:
                    # This would call Langfuse's span creation in a real implementation
                    pass
                except Exception as e:
                    logger.warning(f"Langfuse 步骤记录失败: {e}")

    def end_trace(self, result: Dict[str, Any], success: bool = True) -> Dict[str, Any]:
        """结束追踪"""
        if self.current_trace:
            self.current_trace.complete(result, success)
            trace_dict = self.current_trace.to_dict()
            self._save_traces()
            
            # Log to Langfuse if available
            if self.use_langfuse and self.langfuse_client:
                try:
                    # This would call Langfuse's trace completion in a real implementation
                    pass
                except Exception as e:
                    logger.warning(f"Langfuse 追踪完成记录失败: {e}")
            
            self.current_trace = None
            return trace_dict
        return {}

    def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """获取追踪记录"""
        # Check current traces
        for trace in self.traces:
            if trace.trace_id == trace_id:
                return trace.to_dict()
        
        # Check history
        for trace in self.trace_history:
            if trace.get("trace_id") == trace_id:
                return trace
        
        return None

    def get_recent_traces(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取最近的追踪记录"""
        all_traces = self.trace_history + [t.to_dict() for t in self.traces]
        return all_traces[-limit:]

    def get_success_rate(self, task_type: Optional[str] = None) -> float:
        """获取成功率"""
        all_traces = self.trace_history + [t.to_dict() for t in self.traces]
        
        if task_type:
            filtered = [t for t in all_traces if t.get("task", "").startswith(task_type)]
        else:
            filtered = all_traces
        
        if not filtered:
            return 0.0
        
        successful = sum(1 for t in filtered if t.get("status") == "success")
        return successful / len(filtered)

    def get_analytics(self) -> Dict[str, Any]:
        """获取分析数据"""
        all_traces = self.trace_history + [t.to_dict() for t in self.traces]
        
        if not all_traces:
            return {"total_traces": 0}
        
        return {
            "total_traces": len(all_traces),
            "successful": sum(1 for t in all_traces if t.get("status") == "success"),
            "failed": sum(1 for t in all_traces if t.get("status") == "failure"),
            "success_rate": self.get_success_rate(),
            "avg_duration": sum(t.get("duration", 0) for t in all_traces if t.get("duration")) / len(all_traces)
        }

