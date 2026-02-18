#!/usr/bin/env bash
# =============================================================================
# Section 1 — Linux Fundamentals: Advanced Debug Lab
# Guide: docs/curriculum/01-linux-fundamentals.md
# =============================================================================

# Exercise 1.D.1 — Debug: "Address Already in Use"
# TODO: Find the process using the port, kill it
# ss -tlnp | grep :8000
# kill <pid>


# Exercise 1.D.2 — Debug: "Permission Denied" on Script
# TODO: Check permissions, add execute bit
# ls -la script.sh
# chmod +x script.sh


# Exercise 1.D.3 — Debug: Orphaned Process Eating CPU
# TODO: Find with top/htop, identify parent, kill properly
# top -b -n 1 | head -20
# ps aux --sort=-%cpu | head -5


# Exercise 1.D.4 — Debug: Disk Full — Can't Write Logs
# TODO: Find large files, identify deleted-but-open files
# df -h
# find /var/log -size +100M -exec ls -lh {} \;
# lsof | grep deleted


# Exercise 1.D.5 — Debug: Shell Script Fails Silently
# TODO: Add set -euo pipefail, use bash -x for trace


# Exercise 1.D.6 — Debug: Wrong PATH Causes Wrong Python
# TODO: which python, echo $PATH, fix order


# Exercise 1.D.7 — Debug: Deleted File Still Consuming Disk
# TODO: lsof +L1, find processes holding deleted files


# Exercise 1.D.8 — Debug: Environment Variable Inheritance
# TODO: export vs no export, subshell behavior


# Exercise 1.D.9 — Debug: Script Works in Terminal but Fails in Cron
# TODO: Full paths in cron, source profile, set PATH


# Exercise 1.D.10 — Debug: SSH Connection Drops Kill Your Server
# TODO: nohup, tmux/screen, disown, systemd service
