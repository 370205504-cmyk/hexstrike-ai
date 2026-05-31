#!/usr/bin/env python3
"""
Quick Test Script for HexStrike CLI Components
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("HexStrike CLI - Quick Component Test")
print("=" * 60)

try:
    print("\n1. Testing imports...")
    from cli import ConfigManager, TerminalVisualEngine, HexStrikeConfig
    
    print("   ✅ Imports successful!")
    
    print("\n2. Testing config initialization...")
    ConfigManager.initialize()
    print("   ✅ Config initialized")
    
    config = ConfigManager.load_config()
    print(f"   ✅ Config loaded: model={config.model}, debug={config.debug}")
    
    print("\n3. Testing terminal UI...")
    print(TerminalVisualEngine.banner())
    TerminalVisualEngine.status("Test status message", "INFO")
    TerminalVisualEngine.status("Test success message", "SUCCESS")
    
    print("\n" + "=" * 60)
    print("✅ All components tested successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Run 'python cli.py --help' to see command line options")
    print("  - Check ~/.hexstrike/ for your configuration")
    print("  - Start coding the integration with HexStrike server!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
