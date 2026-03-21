#!/bin/bash
# seVen_Engine/Skills/docker_check.sh
echo "🐋 Checking AlArab Docker Empire..."
if ! command -v docker &> /dev/null
then
    echo "❌ Docker is not installed or not in PATH."
    exit 1
fi

docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo "✅ Docker Check Complete."
