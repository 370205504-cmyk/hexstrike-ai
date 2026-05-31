#!/usr/bin/env python3
"""
HexStrike AI 增强版 CLI - 带自动进化、自动升级、自我迭代、长记忆功能
"""

import argparse
import sys
import json
from pathlib import Path
from hexstrike_enhanced import (
    EnhancedHexStrikeAgent,
    LongTermMemory,
    AutoEvolutionEngine,
    AutoUpgradeSystem
)


def print_banner():
    """打印横幅"""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                     🚀 HEXSTRIKE AI 增强版                       ║
║          自动进化 | 自动升级 | 自我迭代 | 长记忆系统             ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


class EnhancedCLI:
    """增强版 CLI"""
    
    def __init__(self):
        self.agent = EnhancedHexStrikeAgent()
    
    def show_status(self):
        """显示 Agent 状态"""
        status = self.agent.get_status()
        print("\n" + "="*60)
        print("📊 AGENT 状态")
        print("="*60)
        print(f"迭代次数:        {status['iteration_count']}")
        print(f"总经验数:        {status['total_experiences']}")
        print(f"成功案例:        {status['success_cases']}")
        print(f"失败案例:        {status['failure_cases']}")
        print(f"当前版本:        {status['current_version']}")
        if status['last_iteration']:
            print(f"最后迭代:        {status['last_iteration']}")
        print("="*60 + "\n")
    
    def show_memory(self):
        """显示记忆内容"""
        print("\n" + "="*60)
        print("🧠 长期记忆系统")
        print("="*60)
        
        memory = self.agent.memory
        print(f"经验记录: {len(memory.memories['experiences'])} 条")
        print(f"成功案例: {len(memory.memories['success_cases'])} 条")
        print(f"失败案例: {len(memory.memories['failure_cases'])} 条")
        print(f"知识点:   {len(memory.memories['knowledge'])} 个")
        
        # 显示最近的经验
        if memory.memories['experiences']:
            print("\n📜 最近的经验:")
            recent = memory.memories['experiences'][-3:]
            for i, exp in enumerate(reversed(recent), 1):
                print(f"\n  {i}. [{exp['id']}] {exp.get('task_type', 'unknown')}")
                print(f"     内容: {exp.get('content', '')[:50]}...")
                print(f"     结果: {'✅ 成功' if exp.get('success') else '❌ 失败'}")
                print(f"     时间: {exp.get('timestamp', '')}")
        
        print("="*60 + "\n")
    
    def run_task(self, task_type: str, description: str):
        """执行任务"""
        print(f"\n🎯 执行任务: {description}")
        
        task = {
            "type": task_type,
            "description": description
        }
        
        result = self.agent.execute_task(task)
        
        print("\n📋 任务结果:")
        print(f"   成功: {'✅' if result.get('success') else '❌'}")
        print(f"   工具: {', '.join(result.get('tools_used', []))}")
        print(f"   方法: {result.get('approach', '')}")
        print(f"   输出: {result.get('output', '')}")
    
    def check_updates(self):
        """检查更新"""
        print("\n🔍 检查更新...")
        has_update, msg = self.agent.upgrader.check_for_updates()
        print(f"   {msg}")
        
        if has_update:
            print("\n💡 提示: 使用 --upgrade 命令进行升级")
    
    def perform_upgrade(self):
        """执行升级"""
        print("\n⬆️  开始升级...")
        success = self.agent.upgrader.perform_upgrade()
        
        if success:
            print("✅ 升级成功！")
        else:
            print("❌ 升级失败，请查看日志")
    
    def interactive_mode(self):
        """交互式模式"""
        print("\n" + "="*60)
        print("💬 交互式模式 (输入 'quit' 退出)")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n🎯 请描述任务: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                # 简单的任务类型判断
                task_type = "general"
                if "web" in user_input.lower() or "网站" in user_input:
                    task_type = "web_vulnerability_scan"
                elif "scan" in user_input.lower() or "扫描" in user_input:
                    task_type = "reconnaissance"
                elif "exploit" in user_input.lower() or "利用" in user_input:
                    task_type = "exploitation"
                
                self.run_task(task_type, user_input)
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 出错: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="HexStrike AI 增强版 - 自动进化、自动升级、自我迭代、长记忆系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s status              # 查看 Agent 状态
  %(prog)s memory              # 查看长期记忆
  %(prog)s task                # 执行任务（交互式）
  %(prog)s task --type reconnaissance --desc "扫描 192.168.1.100"
  %(prog)s check               # 检查更新
  %(prog)s upgrade             # 执行升级
  %(prog)s                     # 进入完整交互式模式
        """
    )
    
    subparsers = parser.add_subparsers(title="命令", dest="command")
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="查看 Agent 状态")
    
    # memory 命令
    memory_parser = subparsers.add_parser("memory", help="查看长期记忆")
    
    # task 命令
    task_parser = subparsers.add_parser("task", help="执行任务")
    task_parser.add_argument("--type", "-t", default="general", 
                          help="任务类型 (reconnaissance, web_vulnerability_scan, exploitation, etc.)")
    task_parser.add_argument("--desc", "-d", help="任务描述")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查更新")
    
    # upgrade 命令
    upgrade_parser = subparsers.add_parser("upgrade", help="执行升级")
    
    args = parser.parse_args()
    
    print_banner()
    
    cli = EnhancedCLI()
    
    if args.command == "status":
        cli.show_status()
    elif args.command == "memory":
        cli.show_memory()
    elif args.command == "task":
        if args.desc:
            cli.run_task(args.type, args.desc)
        else:
            cli.interactive_mode()
    elif args.command == "check":
        cli.check_updates()
    elif args.command == "upgrade":
        cli.perform_upgrade()
    else:
        # 默认进入交互式模式
        cli.interactive_mode()


if __name__ == "__main__":
    main()
