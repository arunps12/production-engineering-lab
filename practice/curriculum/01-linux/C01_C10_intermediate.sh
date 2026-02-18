#!/usr/bin/env bash
# =============================================================================
# Section 1 — Linux Fundamentals: Intermediate Exercises (1-10)
# Guide: docs/curriculum/01-linux-fundamentals.md
# =============================================================================

# Exercise 1.C.1 — Process Tree Investigation
# TODO: pstree, ps --forest, /proc/<pid>/status


# Exercise 1.C.2 — Zombie Process Creation
# TODO: Create a zombie process with Python, observe with ps aux


# Exercise 1.C.3 — Signal Handling
# TODO: trap signals in a script, send signals with kill -SIGTERM


# Exercise 1.C.4 — File Descriptor Investigation
# TODO: ls -l /proc/self/fd, lsof -p <pid>


# Exercise 1.C.5 — Disk Space Forensics
# TODO: du -sh /var/*, find . -size +100M, df -h


# Exercise 1.C.6 — Log Analysis Pipeline
# TODO: cat /var/log/syslog | grep ERROR | awk '{print $5}' | sort | uniq -c | sort -rn


# Exercise 1.C.7 — Process Resource Limits
# TODO: ulimit -a, ulimit -n 1024


# Exercise 1.C.8 — Background Jobs and Job Control
# TODO: command &, jobs, fg, bg, Ctrl+Z, nohup


# Exercise 1.C.9 — Using screen or tmux
# TODO: tmux new -s session, tmux attach, tmux ls


# Exercise 1.C.10 — Cron Jobs
# TODO: crontab -e, crontab -l, * * * * * /path/to/script.sh
