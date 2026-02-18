#!/usr/bin/env bash
# =============================================================================
# PART E — Production Simulation: Server Health Check System
# Guide: docs/curriculum/01-linux-fundamentals.md
#
# Build a health check script that monitors:
# 1. Disk usage (alert if > 80%)
# 2. Memory usage (alert if > 90%)
# 3. CPU load average
# 4. Key processes running (python, nginx, etc.)
# 5. Port availability (8000, 5432, etc.)
# =============================================================================

set -euo pipefail

LOG_FILE="/tmp/healthcheck.log"
ALERT_THRESHOLD_DISK=80
ALERT_THRESHOLD_MEM=90

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_disk() {
    # TODO: Check disk usage with df, alert if above threshold
    log "Checking disk usage..."
}

check_memory() {
    # TODO: Check memory with free -m, alert if above threshold
    log "Checking memory..."
}

check_cpu() {
    # TODO: Check load average with uptime
    log "Checking CPU load..."
}

check_processes() {
    # TODO: Check if key processes are running
    local processes=("python" "ssh")
    log "Checking processes..."
}

check_ports() {
    # TODO: Check if expected ports are listening
    local ports=(22 8000)
    log "Checking ports..."
}

main() {
    log "=== Health Check Started ==="
    check_disk
    check_memory
    check_cpu
    check_processes
    check_ports
    log "=== Health Check Complete ==="
}

main "$@"
