#!/usr/bin/env bash
# =============================================================================
# Section 2 — Networking: Advanced Debug Lab & Production Simulation
# Guide: docs/curriculum/02-networking-debug-lab.md
# =============================================================================

# Exercise 2.D.1 — Debug: "Connection Refused" on Working Service
# TODO: Check if service is running, check bind address, check port


# Exercise 2.D.2 — Debug: curl Inside Docker Container Fails
# TODO: Check Docker networking, DNS resolution inside container


# Exercise 2.D.3 — Debug: Intermittent "Connection Reset"
# TODO: Check server logs, connection limits, timeouts


# Exercise 2.D.4 — Debug: DNS Works but HTTPS Fails
# TODO: Check certificates, date/time, CA bundle


# Exercise 2.D.5 — Debug: TIME_WAIT Exhaustion
# TODO: ss -s, sysctl net.ipv4.tcp_tw_reuse


# Exercise 2.D.6 — Debug: Docker Port Mapping Not Working
# TODO: docker port, docker inspect, iptables


# Exercise 2.D.7 — Debug: Slow Response Times
# TODO: curl timing, traceroute, check DNS resolution time


# Exercise 2.D.8 — Full Network Diagnostic Script
# See D08_network_diagnostic.sh


# PART E — Multi-Service Communication Debugging
# TODO: Set up two services that talk to each other
# TODO: Debug when communication breaks
