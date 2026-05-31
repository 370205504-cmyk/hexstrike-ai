#!/usr/bin/env python3
"""
测试增强版 HexStrike AI 功能
"""

print("="*60)
print("🧪 测试增强版 HexStrike AI")
print("="*60)

try:
    print("\n1. 测试导入模块...")
    from hexstrike_enhanced import (
        LongTermMemory,
        AutoEvolutionEngine,
        AutoUpgradeSystem,
        EnhancedHexStrikeAgent
    )
    print("✅ 导入成功！")

    print("\n2. 测试 LongTermMemory...")
    memory = LongTermMemory()
    print("✅ 记忆系统初始化成功！")

    print("\n3. 测试 EnhancedHexStrikeAgent...")
    agent = EnhancedHexStrikeAgent()
    print("✅ 增强版 Agent 初始化成功！")

    print("\n4. 测试执行任务...")
    result = agent.execute_task({
        'type': 'test',
        'description': '测试任务'
    })
    print(f"✅ 任务执行成功！结果: {result}")

    print("\n5. 显示 Agent 状态...")
    status = agent.get_status()
    print(f"   状态: {status}")

    print("\n" + "="*60)
    print("🎉 所有测试通过！")
    print("="*60)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
