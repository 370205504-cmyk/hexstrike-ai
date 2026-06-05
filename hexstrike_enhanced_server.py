#!/usr/bin/env python3
"""
HexStrike AI v7.0 - Enhanced Penetration Testing Framework
Integrating:
  - Intelligent Decision Engine
  - RAG Knowledge Engine
  - Multi-Model Collaboration
  - Celery Async Tasks
  - Vector Memory Store
  - Decision Tracking
  - BOAZ Evasion Framework
  - Anti-Honeypot System
  - SAST/DAST Analyzers
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all our new components
from core.intelligent_decision_engine import (
    IntelligentDecisionEngine,
    FailureRecoverySystem,
    TaskPhase
)
from core.rag_knowledge_engine import RAGKnowledgeEngine
from core.multi_model_collaboration import MultiModelCollaborationSystem
from core.celery_tasks import (
    CeleryTaskManager,
    execute_tool_task,
    get_task_status,
    get_all_tasks
)
from core.vector_memory import VectorMemoryStore
from core.langfuse_tracker import LangfuseDecisionTracker
from core.boaz_enhanced import BOAZEnhancedFramework, PayloadGenerator
from core.anti_honeypot import AntiHoneypotSystem
from core.sast_dast import SASTAnalyzer, DASTAnalyzer, LogicVulnerabilityAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('hexstrike_enhanced.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Configuration
API_HOST = os.environ.get('HEXSTRIKE_HOST', '127.0.0.1')
API_PORT = int(os.environ.get('HEXSTRIKE_PORT', 8888))

# Initialize all our components
class HexStrikeEnhancedCore:
    """Core class that integrates all enhanced components"""
    
    def __init__(self):
        logger.info("🚀 Initializing HexStrike AI v7.0 Enhanced Core...")
        
        # Initialize core components
        self.decision_engine = IntelligentDecisionEngine()
        self.failure_recovery = FailureRecoverySystem()
        self.knowledge_engine = RAGKnowledgeEngine()
        self.multi_model = MultiModelCollaborationSystem()
        
        # Initialize architecture components
        self.task_manager = CeleryTaskManager()
        self.vector_memory = VectorMemoryStore()
        self.tracker = LangfuseDecisionTracker()
        
        # Initialize offensive techniques
        self.boaz = BOAZEnhancedFramework()
        self.payload_gen = PayloadGenerator()
        self.anti_honeypot = AntiHoneypotSystem()
        self.sast = SASTAnalyzer()
        self.dast = DASTAnalyzer()
        self.logic_analyzer = LogicVulnerabilityAnalyzer()
        
        logger.info("✅ All components initialized successfully!")

# Initialize the core
hexstrike_core = HexStrikeEnhancedCore()

# ============================================================================
# API Routes
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": "7.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "decision_engine": "active",
            "knowledge_engine": "active",
            "multi_model": "active",
            "vector_memory": "active",
            "boaz_framework": "active"
        }
    })

# ============================================================================
# AI Brain Endpoints
# ============================================================================

@app.route('/api/v1/analyze-target', methods=['POST'])
def analyze_target():
    """Analyze a target using the Intelligent Decision Engine"""
    data = request.json
    target = data.get('target')
    target_type = data.get('target_type', 'web_application')
    
    if not target:
        return jsonify({"error": "Target is required"}), 400
    
    try:
        # Start tracking
        trace_id = hexstrike_core.tracker.start_trace(
            "analyze_target",
            {"target": target, "target_type": target_type}
        )
        
        # Analyze target
        target_info = hexstrike_core.decision_engine.analyze_target(target, target_type)
        hexstrike_core.tracker.add_trace_step("analyze", {"target_info": target_info})
        
        # Build attack chain
        attack_chain = hexstrike_core.decision_engine.build_attack_chain(target, target_info)
        hexstrike_core.tracker.add_trace_step("build_chain", {"steps_count": len(attack_chain.steps)})
        
        # Store in memory
        hexstrike_core.vector_memory.store_attack_chain(target, {
            "target_info": target_info,
            "steps": [
                {
                    "phase": step.phase.value,
                    "tool": step.tool,
                    "parameters": step.parameters,
                    "priority": step.priority
                }
                for step in attack_chain.steps
            ]
        })
        
        # Complete tracking
        result = {
            "target_info": target_info,
            "attack_chain": [
                {
                    "phase": step.phase.value,
                    "tool": step.tool,
                    "description": step.description,
                    "parameters": step.parameters
                }
                for step in attack_chain.steps
            ]
        }
        hexstrike_core.tracker.end_trace(result, True)
        
        return jsonify({
            "trace_id": trace_id,
            "status": "success",
            "result": result
        })
    except Exception as e:
        logger.error(f"Error analyzing target: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/knowledge-query', methods=['POST'])
def knowledge_query():
    """Query the RAG Knowledge Engine"""
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        results = hexstrike_core.knowledge_engine.query(query)
        return jsonify({
            "status": "success",
            "query": query,
            "results": results
        })
    except Exception as e:
        logger.error(f"Error querying knowledge engine: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/multi-model-collaborate', methods=['POST'])
def multi_model_collaborate():
    """Get collaborative decision from multi-model system"""
    data = request.json
    task = data.get('task')
    context = data.get('context', {})
    
    if not task:
        return jsonify({"error": "Task is required"}), 400
    
    try:
        decision = hexstrike_core.multi_model.collaborate(task, context)
        return jsonify({
            "status": "success",
            "decision": {
                "chosen_approach": decision.chosen_approach,
                "referee_justification": decision.referee_justification,
                "supporting_opinions": [
                    {
                        "agent": op.agent_name,
                        "specialty": op.specialty.value,
                        "recommendation": op.recommendation,
                        "confidence": op.confidence
                    }
                    for op in decision.supporting_opinions
                ]
            }
        })
    except Exception as e:
        logger.error(f"Error in multi-model collaboration: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# Async Task Endpoints
# ============================================================================

@app.route('/api/v1/execute-tool', methods=['POST'])
def execute_tool():
    """Execute a tool asynchronously"""
    data = request.json
    tool = data.get('tool')
    args = data.get('args', [])
    target = data.get('target', '')
    options = data.get('options', {})
    
    if not tool:
        return jsonify({"error": "Tool is required"}), 400
    
    try:
        # Submit the task
        task_result = hexstrike_core.task_manager.submit_tool_task(tool, args, target, options)
        
        # Get task ID (handle both Celery and mock)
        task_id = None
        if hasattr(task_result, 'id'):
            task_id = task_result.id
        elif hasattr(task_result, 'task_id'):
            task_id = task_result.task_id
        else:
            task_id = f"task_{int(datetime.now().timestamp())}"
        
        return jsonify({
            "status": "submitted",
            "task_id": task_id,
            "tool": tool,
            "target": target
        })
    except Exception as e:
        logger.error(f"Error submitting tool task: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/task-status/<task_id>', methods=['GET'])
def get_task_status_endpoint(task_id):
    """Get the status of a task"""
    try:
        status = get_task_status(task_id)
        return jsonify({
            "task_id": task_id,
            "status": status
        })
    except Exception as e:
        logger.error(f"Error getting task status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/tasks', methods=['GET'])
def get_all_tasks_endpoint():
    """Get all tasks"""
    try:
        tasks = get_all_tasks()
        return jsonify({
            "total_tasks": len(tasks),
            "tasks": tasks
        })
    except Exception as e:
        logger.error(f"Error getting all tasks: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# Memory Endpoints
# ============================================================================

@app.route('/api/v1/memory/scan-result', methods=['POST'])
def store_scan_result():
    """Store a scan result in vector memory"""
    data = request.json
    target = data.get('target')
    tool = data.get('tool')
    result = data.get('result')
    
    if not target or not tool or not result:
        return jsonify({"error": "Target, tool, and result are required"}), 400
    
    try:
        memory_id = hexstrike_core.vector_memory.store_scan_result(target, tool, result)
        return jsonify({
            "status": "success",
            "memory_id": memory_id
        })
    except Exception as e:
        logger.error(f"Error storing scan result: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/memory/search', methods=['POST'])
def search_memory():
    """Search memory for relevant information"""
    data = request.json
    query = data.get('query')
    top_k = data.get('top_k', 5)
    filter_meta = data.get('filter', None)
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        results = hexstrike_core.vector_memory.search_memories(query, top_k, filter_meta)
        return jsonify({
            "status": "success",
            "query": query,
            "count": len(results),
            "results": results
        })
    except Exception as e:
        logger.error(f"Error searching memory: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# Offensive Techniques Endpoints
# ============================================================================

@app.route('/api/v1/boaz/generate-payload', methods=['POST'])
def generate_payload():
    """Generate an evasive payload using BOAZ"""
    data = request.json
    lhost = data.get('lhost', '127.0.0.1')
    lport = data.get('lport', 4444)
    payload_type = data.get('payload_type', 'reverse_tcp')
    target_edr = data.get('target_edr', 'generic')
    
    try:
        base_payload = hexstrike_core.payload_gen.generate_metasploit_payload(
            lhost, lport, payload_type
        )
        
        boaz_result = hexstrike_core.boaz.ai_driven_payload_generation(
            {"risk_score": 0.7},
            base_payload
        )
        
        return jsonify({
            "status": "success",
            "payload": boaz_result
        })
    except Exception as e:
        logger.error(f"Error generating payload: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/anti-honeypot/analyze', methods=['POST'])
def analyze_honeypot():
    """Analyze if a target is a honeypot"""
    data = request.json
    target = data.get('target')
    responses = data.get('responses', [])
    
    if not target:
        return jsonify({"error": "Target is required"}), 400
    
    try:
        result = hexstrike_core.anti_honeypot.analyze_target(target, responses)
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        logger.error(f"Error analyzing honeypot: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/sast/scan', methods=['POST'])
def sast_scan():
    """Run SAST scan on code directory"""
    data = request.json
    code_dir = data.get('code_dir')
    language = data.get('language', 'python')
    
    if not code_dir:
        return jsonify({"error": "Code directory is required"}), 400
    
    try:
        results = hexstrike_core.sast.scan_codebase(code_dir, language)
        return jsonify({
            "status": "success",
            "results": results
        })
    except Exception as e:
        logger.error(f"Error running SAST scan: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/dast/scan', methods=['POST'])
def dast_scan():
    """Run DAST scan on web application"""
    data = request.json
    target_url = data.get('target_url')
    scan_type = data.get('scan_type', 'full')
    
    if not target_url:
        return jsonify({"error": "Target URL is required"}), 400
    
    try:
        results = hexstrike_core.dast.scan_web_app(target_url, scan_type)
        return jsonify({
            "status": "success",
            "results": results
        })
    except Exception as e:
        logger.error(f"Error running DAST scan: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='HexStrike AI v7.0 Enhanced Server')
    parser.add_argument('--host', default=API_HOST, help='Server host')
    parser.add_argument('--port', type=int, default=API_PORT, help='Server port')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    
    args = parser.parse_args()
    
    # Print welcome banner
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║  🚀 HEXSTRIKE AI v7.0 - ENHANCED PENETRATION TESTING FRAMEWORK  ║
╠═══════════════════════════════════════════════════════════════╣
║  ✅ Intelligent Decision Engine                                 ║
║  ✅ RAG Knowledge Engine                                        ║
║  ✅ Multi-Model Collaboration                                   ║
║  ✅ Async Task Processing                                       ║
║  ✅ Vector Memory Store                                         ║
║  ✅ BOAZ Evasion Framework                                      ║
║  ✅ Anti-Honeypot System                                        ║
║  ✅ SAST/DAST Analyzers                                         ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    
    logger.info(f"Starting HexStrike AI v7.0 Enhanced Server on {args.host}:{args.port}")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
