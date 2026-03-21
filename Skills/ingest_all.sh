#!/bin/bash
# seVen_Engine/Skills/ingest_all.sh
echo "🌊 Triggering Universal Knowledge Ingestion..."
# This script sends a POST request to our own API to force a sync
curl -X POST http://127.0.0.1:7778/api/sync
echo "✅ Ingestion sequence completed."
