#!/usr/bin/env bash
# =============================================================================
# Exercise 2.D.8 — Full Network Diagnostic Script
# Guide: docs/curriculum/02-networking-debug-lab.md
# =============================================================================

set -euo pipefail

TARGET=${1:-"google.com"}
PORT=${2:-443}

echo "=== Network Diagnostic for $TARGET:$PORT ==="

# TODO: 1. Check DNS resolution
# echo "--- DNS Resolution ---"
# dig +short "$TARGET"

# TODO: 2. Check connectivity
# echo "--- Ping ---"
# ping -c 3 "$TARGET"

# TODO: 3. Check port accessibility
# echo "--- Port Check ---"
# timeout 5 bash -c "echo >/dev/tcp/$TARGET/$PORT" 2>/dev/null && echo "Port $PORT: OPEN" || echo "Port $PORT: CLOSED"

# TODO: 4. Check HTTP response
# echo "--- HTTP Response ---"
# curl -s -o /dev/null -w "Status: %{http_code}\nTime: %{time_total}s\n" "https://$TARGET"

# TODO: 5. Check route
# echo "--- Traceroute ---"
# traceroute -m 10 "$TARGET" 2>/dev/null || echo "traceroute not available"

echo "=== Diagnostic Complete ==="
