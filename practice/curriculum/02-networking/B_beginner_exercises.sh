#!/usr/bin/env bash
# =============================================================================
# Section 2 — Networking: Beginner Exercises
# Guide: docs/curriculum/02-networking-debug-lab.md
# =============================================================================

# Exercise 2.B.1 — Discover Your Network Interfaces
# TODO: ip addr show, ifconfig, hostname -I


# Exercise 2.B.2 — Test DNS Resolution
# TODO: nslookup google.com, dig google.com, host google.com


# Exercise 2.B.3 — Check Network Connectivity
# TODO: ping -c 4 google.com, ping -c 4 8.8.8.8


# Exercise 2.B.4 — Explore Listening Ports
# TODO: ss -tlnp, netstat -tlnp


# Exercise 2.B.5 — Make HTTP Requests with curl
# TODO: curl -v https://httpbin.org/get
# TODO: curl -X POST https://httpbin.org/post -d '{"key":"value"}'


# Exercise 2.B.6 — TCP Connection Test with curl Timing
# TODO: curl -w "@curl-format.txt" -o /dev/null -s https://httpbin.org/get


# Exercise 2.B.7 — Simple TCP Server and Client
# See B07_tcp_server.py and B07_tcp_client.py


# Exercise 2.B.8 — Inspect /etc/hosts
# TODO: cat /etc/hosts, understand how local DNS override works


# Exercise 2.B.9 — Check Open Connections
# TODO: ss -tnp, lsof -i -n -P


# Exercise 2.B.10 — Download Files
# TODO: curl -O, wget, curl -L (follow redirects)
