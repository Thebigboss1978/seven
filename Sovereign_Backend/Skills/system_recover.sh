#!/bin/bash
# seVen_Engine/Skills/system_recover.sh
echo "🔨 Initiating seVen SYSTEM RECOVERY..."
# 1. Kill any hung processes on our ports
lsof -ti:7778 | xargs kill -9 2>/dev/null
# 2. Cleanup Ollama
ollama gc
# 3. Restart the server in the background
cd /Users/macos/AlArab777/seVen_Engine
nohup python3 Engine/seVen_Core_Server.py > server.log 2>&1 &
echo "✅ System Restarted and Memory Purged. Tier 1 Active."
