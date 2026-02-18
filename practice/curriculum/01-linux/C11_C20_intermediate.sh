#!/usr/bin/env bash
# =============================================================================
# Section 1 — Linux Fundamentals: Intermediate Exercises (11-20)
# Guide: docs/curriculum/01-linux-fundamentals.md
# =============================================================================

# Exercise 1.C.11 — Networking File Transfer
# TODO: scp file.txt user@host:/path/, rsync -avz ./src/ user@host:/dest/


# Exercise 1.C.12 — System Service Management
# TODO: systemctl status, systemctl start/stop/restart, journalctl -u


# Exercise 1.C.13 — Inspecting Network Connections
# TODO: ss -tlnp, netstat -tlnp, lsof -i :8000


# Exercise 1.C.14 — Using sed for Stream Editing
# TODO: sed 's/old/new/g', sed -i, sed -n '5,10p'


# Exercise 1.C.15 — Process Monitoring with ps and top
# TODO: ps aux --sort=-%mem, top -b -n 1


# Exercise 1.C.16 — Writing a Bash Script with Error Handling
# See C16_error_handling_script.sh


# Exercise 1.C.17 — Here Documents and Here Strings
# TODO: cat <<EOF, command <<<string


# Exercise 1.C.18 — Using tee for Split Output
# TODO: command | tee output.log, command | tee -a append.log


# Exercise 1.C.19 — Conditional Execution Patterns
# TODO: cmd1 && cmd2, cmd1 || cmd2, if [[ ]]; then


# Exercise 1.C.20 — Comparing Files
# TODO: diff file1 file2, diff -u, vimdiff, comm
