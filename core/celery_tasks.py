#!/usr/bin/env python3
"""
Celery Async Tasks - 异步任务系统
将耗时工具调用放入后台，支持大规模并行扫描
"""

import logging
import subprocess
import time
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("CeleryTasks")

# Try to import Celery - if not available, use a mock implementation
try:
    from celery import Celery, shared_task
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    logger.warning("Celery not available, using mock async implementation")

    # Mock decorator and task class for when Celery isn't installed
    def shared_task(func):
        func.delay = lambda *args, **kwargs: MockAsyncResult(func(*args, **kwargs))
        func.apply_async = lambda *args, **kwargs: MockAsyncResult(func(*args, **kwargs))
        return func

    class MockAsyncResult:
        def __init__(self, result):
            self.result = result
            self.state = "SUCCESS"
            self._result = result

        def get(self, timeout=None):
            return self.result

        def ready(self):
            return True

        def successful(self):
            return True


# Task registry and status tracking
task_registry = {}
task_status = {}


class TaskStatus:
    """任务状态"""
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"


def register_task(task_name: str, task_func):
    """注册任务"""
    task_registry[task_name] = task_func
    logger.info(f"📋 注册任务: {task_name}")


@shared_task(bind=True, max_retries=3)
def execute_tool_task(self, tool: str, args: list, target: str, options: Optional[Dict] = None) -> Dict[str, Any]:
    """执行工具任务"""
    task_id = self.request.id if hasattr(self, 'request') else f"mock_{int(time.time())}"
    
    logger.info(f"🚀 开始执行任务 {task_id}: {tool} {' '.join(args)}")
    task_status[task_id] = {
        "status": TaskStatus.STARTED,
        "tool": tool,
        "target": target,
        "started_at": datetime.now().isoformat()
    }

    try:
        # Build command
        cmd = [tool] + args
        
        # Execute command
        start_time = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=options.get("timeout", 300) if options else 300
        )
        execution_time = time.time() - start_time

        output = result.stdout
        error_output = result.stderr
        success = result.returncode == 0

        task_result = {
            "task_id": task_id,
            "tool": tool,
            "target": target,
            "command": " ".join(cmd),
            "success": success,
            "return_code": result.returncode,
            "output": output,
            "error_output": error_output,
            "execution_time": execution_time,
            "started_at": task_status[task_id]["started_at"],
            "completed_at": datetime.now().isoformat()
        }

        if success:
            task_status[task_id]["status"] = TaskStatus.SUCCESS
            logger.info(f"✅ 任务 {task_id} 完成，耗时 {execution_time:.2f}s")
        else:
            task_status[task_id]["status"] = TaskStatus.FAILURE
            logger.warning(f"⚠️  任务 {task_id} 完成但返回非零退出码: {result.returncode}")

        return task_result

    except subprocess.TimeoutExpired as e:
        logger.error(f"⏱️  任务 {task_id} 超时")
        task_status[task_id]["status"] = TaskStatus.FAILURE
        if hasattr(self, 'retry'):
            raise self.retry(exc=e, countdown=2 ** self.request.retries)
        return {
            "task_id": task_id,
            "tool": tool,
            "target": target,
            "success": False,
            "error": "Timeout",
            "error_output": str(e)
        }

    except Exception as e:
        logger.error(f"❌ 任务 {task_id} 执行失败: {e}")
        task_status[task_id]["status"] = TaskStatus.FAILURE
        if hasattr(self, 'retry'):
            raise self.retry(exc=e, countdown=2 ** self.request.retries)
        return {
            "task_id": task_id,
            "tool": tool,
            "target": target,
            "success": False,
            "error": str(type(e).__name__),
            "error_output": str(e)
        }


@shared_task
def parallel_scan_task(targets: list, tool: str, base_args: list) -> Dict[str, Any]:
    """并行扫描任务"""
    logger.info(f"🔄 开始并行扫描 {len(targets)} 个目标")
    
    results = {}
    for target in targets:
        args = base_args + [target]
        result = execute_tool_task.delay(tool, args, target)
        results[target] = result

    # Wait for all results
    final_results = {}
    for target, async_result in results.items():
        try:
            final_results[target] = async_result.get(timeout=600)
        except Exception as e:
            final_results[target] = {"success": False, "error": str(e)}

    return {
        "total_targets": len(targets),
        "successful": sum(1 for r in final_results.values() if r.get("success")),
        "failed": sum(1 for r in final_results.values() if not r.get("success")),
        "results": final_results
    }


def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取任务状态"""
    return task_status.get(task_id)


def get_all_tasks() -> Dict[str, Dict[str, Any]]:
    """获取所有任务"""
    return task_status


class CeleryTaskManager:
    """Celery 任务管理器"""

    def __init__(self, broker_url: str = "redis://localhost:6379/0", backend_url: str = "redis://localhost:6379/1"):
        self.broker_url = broker_url
        self.backend_url = backend_url
        self.celery_app = None

        if CELERY_AVAILABLE:
            self._init_celery()
        else:
            logger.warning("Celery not available, using synchronous mode")

    def _init_celery(self):
        """初始化 Celery 应用"""
        self.celery_app = Celery(
            'hexstrike_tasks',
            broker=self.broker_url,
            backend=self.backend_url
        )
        logger.info("🐦 Celery 应用初始化完成")

    def submit_tool_task(self, tool: str, args: list, target: str, options: Optional[Dict] = None):
        """提交工具任务"""
        return execute_tool_task.delay(tool, args, target, options)

    def submit_parallel_scan(self, targets: list, tool: str, base_args: list):
        """提交并行扫描任务"""
        return parallel_scan_task.delay(targets, tool, base_args)

