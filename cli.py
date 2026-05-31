#!/usr/bin/env python3
"""
HexStrike AI - Pure Terminal CLI Tool
MIT License

Phase 2 Implementation: Core Functionality
- CLI Entry Point with argument parsing
- Configuration file support (~/.hexstrike/config.yaml)
- LLM API integration (OpenAI compatible, Ollama)
- Built-in MCP client that auto-launches HexStrike server
"""

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, List
import threading
import requests
import yaml

# ============================================================================
# LOGGING & CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class HexStrikeConfig:
    """Configuration dataclass for HexStrike CLI"""
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    ollama_base_url: str = "http://localhost:11434/v1"
    use_ollama: bool = False
    target: str = ""
    non_interactive: bool = False
    debug: bool = False
    server_port: int = 8888
    server_host: str = "127.0.0.1"
    output_format: str = "markdown"


class ConfigManager:
    """Manages configuration loading and saving"""
    
    CONFIG_DIR = Path.home() / ".hexstrike"
    CONFIG_FILE = CONFIG_DIR / "config.yaml"
    SESSION_DIR = CONFIG_DIR / "sessions"
    
    @classmethod
    def initialize(cls):
        """Initialize configuration directory structure"""
        cls.CONFIG_DIR.mkdir(exist_ok=True)
        cls.SESSION_DIR.mkdir(exist_ok=True)
        
        if not cls.CONFIG_FILE.exists():
            cls.create_default_config()
    
    @classmethod
    def create_default_config(cls):
        """Create default configuration file"""
        default_config = {
            "api": {
                "api_key": "",
                "base_url": "https://api.openai.com/v1",
                "model": "gpt-4o",
                "ollama": {
                    "enabled": False,
                    "base_url": "http://localhost:11434/v1",
                    "model": "llama3"
                }
            },
            "server": {
                "host": "127.0.0.1",
                "port": 8888
            },
            "cli": {
                "output_format": "markdown",
                "debug": False
            }
        }
        
        with open(cls.CONFIG_FILE, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        logger.info(f"Created default config at {cls.CONFIG_FILE}")
    
    @classmethod
    def load_config(cls) -> HexStrikeConfig:
        """Load configuration from file"""
        cls.initialize()
        
        config = HexStrikeConfig()
        
        try:
            with open(cls.CONFIG_FILE, 'r') as f:
                data = yaml.safe_load(f)
            
            if data:
                config.api_key = data.get("api", {}).get("api_key", "")
                config.base_url = data.get("api", {}).get("base_url", config.base_url)
                config.model = data.get("api", {}).get("model", config.model)
                config.use_ollama = data.get("api", {}).get("ollama", {}).get("enabled", False)
                if config.use_ollama:
                    config.ollama_base_url = data.get("api", {}).get("ollama", {}).get("base_url", config.ollama_base_url)
                    config.model = data.get("api", {}).get("ollama", {}).get("model", "llama3")
                config.server_host = data.get("server", {}).get("host", config.server_host)
                config.server_port = data.get("server", {}).get("port", config.server_port)
                config.output_format = data.get("cli", {}).get("output_format", config.output_format)
                config.debug = data.get("cli", {}).get("debug", config.debug)
        
        except Exception as e:
            logger.warning(f"Failed to load config: {e}, using defaults")
        
        return config
    
    @classmethod
    def save_config(cls, config: HexStrikeConfig):
        """Save configuration to file"""
        cls.initialize()
        
        data = {
            "api": {
                "api_key": config.api_key,
                "base_url": config.base_url,
                "model": config.model,
                "ollama": {
                    "enabled": config.use_ollama,
                    "base_url": config.ollama_base_url,
                    "model": config.model if config.use_ollama else "llama3"
                }
            },
            "server": {
                "host": config.server_host,
                "port": config.server_port
            },
            "cli": {
                "output_format": config.output_format,
                "debug": config.debug
            }
        }
        
        with open(cls.CONFIG_FILE, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)


# ============================================================================
# MODERN VISUAL ENGINE (Terminal UI)
# ============================================================================

class TerminalVisualEngine:
    """Beautiful terminal UI with colors"""
    
    COLORS = {
        'RED': '\033[38;5;196m',
        'GREEN': '\033[38;5;46m',
        'BLUE': '\033[38;5;51m',
        'YELLOW': '\033[38;5;226m',
        'PURPLE': '\033[38;5;129m',
        'ORANGE': '\033[38;5;208m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
        'SUCCESS': '\033[38;5;46m',
        'WARNING': '\033[38;5;208m',
        'ERROR': '\033[38;5;196m',
        'INFO': '\033[38;5;51m',
        'HIGHLIGHT': '\033[48;5;196m\033[38;5;15m'
    }
    
    @staticmethod
    def banner():
        """Display HexStrike banner"""
        b = TerminalVisualEngine.COLORS['BOLD']
        r = TerminalVisualEngine.COLORS['RED']
        res = TerminalVisualEngine.COLORS['RESET']
        return f"""
{b}{r}
██╗  ██╗███████╗██╗  ██╗███████╗████████╗██████╗ ██╗██╗  ██╗███████╗
██║  ██║██╔════╝╚██╗██╔╝██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝
███████║█████╗   ╚███╔╝ ███████╗   ██║   ██████╔╝██║█████╔╝ █████╗  
██╔══██║██╔══╝   ██╔██╗ ╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  
██║  ██║███████╗██╔╝ ██╗███████║   ██║   ██║  ██║██║██║  ██╗███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
{res}
{TerminalVisualEngine.COLORS['DIM']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{res}
  🚀 HexStrike AI - Pure Terminal CLI Tool
  ⚡ AI-Automated Penetration Testing
  🎯 v1.0 | Build: 2026-05-31
{TerminalVisualEngine.COLORS['DIM']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{res}
"""

    @staticmethod
    def status(message: str, status: str = "INFO"):
        """Display status message"""
        color_map = {
            "INFO": TerminalVisualEngine.COLORS['INFO'],
            "SUCCESS": TerminalVisualEngine.COLORS['SUCCESS'],
            "WARNING": TerminalVisualEngine.COLORS['WARNING'],
            "ERROR": TerminalVisualEngine.COLORS['ERROR']
        }
        color = color_map.get(status, TerminalVisualEngine.COLORS['INFO'])
        print(f"{color}[{status}]{TerminalVisualEngine.COLORS['RESET']} {message}")

    @staticmethod
    def highlight(text: str) -> str:
        """Highlight important text"""
        return f"{TerminalVisualEngine.COLORS['HIGHLIGHT']}{text}{TerminalVisualEngine.COLORS['RESET']}"


# ============================================================================
# LLM API CLIENT
# ============================================================================

class LLMClient:
    """LLM API client with OpenAI compatible and Ollama support"""
    
    def __init__(self, config: HexStrikeConfig):
        self.config = config
        self.session = requests.Session()
        self.conversation_history: List[Dict[str, str]] = []
    
    def _get_base_url(self) -> str:
        """Get appropriate base URL based on config"""
        if self.config.use_ollama:
            return self.config.ollama_base_url
        return self.config.base_url
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {"Content-Type": "application/json"}
        if self.config.api_key and not self.config.use_ollama:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers
    
    async def chat_completion(self, messages: List[Dict[str, str]], stream: bool = True) -> str:
        """
        Send chat completion request
        
        Args:
            messages: List of conversation messages
            stream: Whether to stream the response
        
        Returns:
            Full response text
        """
        url = f"{self._get_base_url()}/chat/completions"
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": 0.7,
            "stream": stream
        }
        
        if stream:
            return await self._stream_completion(url, payload)
        else:
            return await self._non_stream_completion(url, payload)
    
    async def _stream_completion(self, url: str, payload: Dict[str, Any]) -> str:
        """Handle streaming response"""
        full_response = []
        
        try:
            response = self.session.post(url, json=payload, headers=self._get_headers(), stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        data_str = line_text[6:]
                        if data_str.strip() == '[DONE]':
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data.get('choices', [{}])[0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                print(content, end='', flush=True)
                                full_response.append(content)
                        except json.JSONDecodeError:
                            pass
        
        except Exception as e:
            TerminalVisualEngine.status(f"LLM API error: {e}", "ERROR")
            return ""
        
        print()
        return ''.join(full_response)
    
    async def _non_stream_completion(self, url: str, payload: Dict[str, Any]) -> str:
        """Handle non-streaming response"""
        try:
            response = self.session.post(url, json=payload, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            return data.get('choices', [{}])[0].get('message', {}).get('content', '')
        except Exception as e:
            TerminalVisualEngine.status(f"LLM API error: {e}", "ERROR")
            return ""
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})


# ============================================================================
# MCP CLIENT & SERVER MANAGER
# ============================================================================

class MCPServerManager:
    """Manages launching and monitoring HexStrike MCP server"""
    
    def __init__(self, config: HexStrikeConfig):
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
    
    def start_server(self) -> bool:
        """Start HexStrike server in background"""
        if self.is_running:
            return True
        
        TerminalVisualEngine.status("Starting HexStrike MCP server...", "INFO")
        
        script_dir = Path(__file__).parent
        server_script = script_dir / "hexstrike_server.py"
        
        if not server_script.exists():
            TerminalVisualEngine.status("Server script not found!", "ERROR")
            return False
        
        try:
            cmd = [
                sys.executable,
                str(server_script),
                "--port", str(self.config.server_port),
                "--host", self.config.server_host
            ]
            
            if self.config.debug:
                cmd.append("--debug")
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(script_dir)
            )
            
            # Wait for server to start
            time.sleep(3)
            
            if self.process.poll() is None:
                self.is_running = True
                TerminalVisualEngine.status(f"Server started on {self.config.server_host}:{self.config.server_port}", "SUCCESS")
                return True
            else:
                stderr = self.process.stderr.read().decode() if self.process.stderr else ""
                TerminalVisualEngine.status(f"Server failed to start: {stderr}", "ERROR")
                return False
        
        except Exception as e:
            TerminalVisualEngine.status(f"Failed to start server: {e}", "ERROR")
            return False
    
    def stop_server(self):
        """Stop HexStrike server"""
        if self.process and self.is_running:
            TerminalVisualEngine.status("Stopping HexStrike server...", "INFO")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.is_running = False
    
    def check_health(self) -> bool:
        """Check if server is healthy"""
        try:
            url = f"http://{self.config.server_host}:{self.config.server_port}/health"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False


class MCPClient:
    """Lightweight MCP client for calling HexStrike tools"""
    
    def __init__(self, config: HexStrikeConfig):
        self.config = config
        self.base_url = f"http://{config.server_host}:{config.server_port}"
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a HexStrike tool
        
        Args:
            tool_name: Name of the tool to call
            params: Tool parameters
        
        Returns:
            Tool execution result
        """
        url = f"{self.base_url}/api/tools/{tool_name}"
        
        try:
            response = requests.post(url, json=params, timeout=300)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        try:
            response = requests.get(f"{self.base_url}/api/tools", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            TerminalVisualEngine.status(f"Failed to list tools: {e}", "ERROR")
            return []


# ============================================================================
# MAIN CLI APPLICATION
# ============================================================================

class HexStrikeCLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.llm_client = Optional[LLMClient]
        self.mcp_server = Optional[MCPServerManager]
        self.mcp_client = Optional[MCPClient]
    
    def parse_args(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="HexStrike AI - Pure Terminal Penetration Testing Tool"
        )
        
        parser.add_argument("--target", "-t", help="Target IP or hostname")
        parser.add_argument("--api-key", help="LLM API key")
        parser.add_argument("--model", help="LLM model name")
        parser.add_argument("--ollama", action="store_true", help="Use Ollama local model")
        parser.add_argument("--non-interactive", "-n", action="store_true", help="Run in non-interactive mode")
        parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
        parser.add_argument("--port", type=int, default=8888, help="Server port")
        parser.add_argument("--host", default="127.0.0.1", help="Server host")
        parser.add_argument("--config", help="Path to custom config file")
        parser.add_argument("--list-tools", action="store_true", help="List available tools")
        
        args = parser.parse_args()
        
        # Update config from command line
        if args.target:
            self.config.target = args.target
        if args.api_key:
            self.config.api_key = args.api_key
        if args.model:
            self.config.model = args.model
        if args.ollama:
            self.config.use_ollama = True
        if args.non_interactive:
            self.config.non_interactive = args.non_interactive
        if args.debug:
            self.config.debug = args.debug
        if args.port:
            self.config.server_port = args.port
        if args.host:
            self.config.server_host = args.host
        
        return args
    
    async def initialize(self):
        """Initialize all components"""
        self.llm_client = LLMClient(self.config)
        self.mcp_server = MCPServerManager(self.config)
        self.mcp_client = MCPClient(self.config)
    
    async def list_available_tools(self):
        """List all available HexStrike tools"""
        TerminalVisualEngine.status("Listing available tools...", "INFO")
        
        if not self.mcp_server.check_health():
            if not self.mcp_server.start_server():
                TerminalVisualEngine.status("Could not start server to list tools", "ERROR")
                return
        
        tools = await self.mcp_client.list_tools()
        
        print(f"\n{TerminalVisualEngine.COLORS['BOLD']}Available Tools ({len(tools)}):{TerminalVisualEngine.COLORS['RESET']}")
        print(TerminalVisualEngine.COLORS['DIM'] + "=" * 60 + TerminalVisualEngine.COLORS['RESET'])
        
        for i, tool in enumerate(tools, 1):
            name = tool.get("name", "Unknown")
            description = tool.get("description", "")
            print(f"{i}. {TerminalVisualEngine.COLORS['GREEN']}{name}{TerminalVisualEngine.COLORS['RESET']}")
            if description:
                print(f"   {TerminalVisualEngine.COLORS['DIM']}{description}{TerminalVisualEngine.COLORS['RESET']}")
            print()
    
    async def run_interactive_mode(self):
        """Run in interactive mode"""
        print(TerminalVisualEngine.banner())
        
        if not self.config.target:
            TerminalVisualEngine.status("Please specify a target with --target", "WARNING")
            self.config.target = input("Enter target IP/hostname: ").strip()
        
        if not self.config.api_key and not self.config.use_ollama:
            TerminalVisualEngine.status("API key not configured", "WARNING")
            key_input = input("Enter API key (leave blank for Ollama): ").strip()
            if key_input:
                self.config.api_key = key_input
            else:
                self.config.use_ollama = True
        
        # Start server
        if not self.mcp_server.start_server():
            return
        
        print(f"\n{TerminalVisualEngine.COLORS['BOLD']}🎯 Target: {TerminalVisualEngine.highlight(self.config.target)}{TerminalVisualEngine.COLORS['RESET']}")
        print(f"{TerminalVisualEngine.COLORS['DIM']}Type 'help' for commands, 'quit' to exit{TerminalVisualEngine.COLORS['RESET']}")
        print()
        
        # Initial scan prompt
        initial_prompt = f"""
We are conducting a penetration test on {self.config.target}.
First, please perform comprehensive information gathering using appropriate tools.
"""
        
        self.llm_client.add_to_history("user", initial_prompt)
        
        while True:
            try:
                prompt = input(f"\n{TerminalVisualEngine.COLORS['BLUE']}▶{TerminalVisualEngine.COLORS['RESET']} ")
                
                if prompt.lower() in ['quit', 'exit', 'q']:
                    break
                elif prompt.lower() == 'help':
                    self.show_help()
                elif prompt.lower() == 'tools':
                    await self.list_available_tools()
                elif prompt.strip():
                    self.llm_client.add_to_history("user", prompt)
                    
                    # Get LLM response
                    response = await self.llm_client.chat_completion(self.llm_client.conversation_history)
                    self.llm_client.add_to_history("assistant", response)
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                TerminalVisualEngine.status(f"Error: {e}", "ERROR")
    
    async def run_non_interactive_mode(self):
        """Run in non-interactive (automatic) mode"""
        print(TerminalVisualEngine.banner())
        
        if not self.config.target:
            TerminalVisualEngine.status("Target required for non-interactive mode", "ERROR")
            return
        
        TerminalVisualEngine.status(f"Starting automatic penetration test on {self.config.target}", "INFO")
        
        if not self.mcp_server.start_server():
            return
        
        # TODO: Implement full non-interactive workflow
        TerminalVisualEngine.status("Non-interactive mode will be implemented in Phase 3", "WARNING")
        
        # For now, just show some info
        print(f"\n{TerminalVisualEngine.COLORS['BOLD']}📋 Target: {self.config.target}{TerminalVisualEngine.COLORS['RESET']}")
        print(f"{TerminalVisualEngine.COLORS['DIM']}Full automation coming soon!{TerminalVisualEngine.COLORS['RESET']}")
    
    def show_help(self):
        """Show help information"""
        help_text = f"""
{TerminalVisualEngine.COLORS['BOLD']}HexStrike CLI Commands:{TerminalVisualEngine.COLORS['RESET']}
  help              Show this help message
  tools             List available tools
  quit/exit/q       Exit the program
  <any prompt>      Ask AI to perform security tasks

{TerminalVisualEngine.COLORS['BOLD']}Command Line Arguments:{TerminalVisualEngine.COLORS['RESET']}
  --target TARGET   Target IP or hostname
  --api-key KEY     LLM API key
  --model MODEL     LLM model name
  --ollama          Use local Ollama model
  --non-interactive Automatic mode
  --debug           Enable debug output
  --list-tools      List available tools
  --config FILE     Custom config file
"""
        print(help_text)
    
    async def run(self):
        """Main run method"""
        args = self.parse_args()
        await self.initialize()
        
        if args.list_tools:
            await self.list_available_tools()
            return
        
        try:
            if self.config.non_interactive:
                await self.run_non_interactive_mode()
            else:
                await self.run_interactive_mode()
        finally:
            if self.mcp_server:
                self.mcp_server.stop_server()


def main():
    """Main entry point"""
    cli = HexStrikeCLI()
    asyncio.run(cli.run())


if __name__ == "__main__":
    main()
