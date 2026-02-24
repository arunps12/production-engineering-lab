"""
Exercise 2.C.8 — TCP Connection States
Guide: docs/curriculum/03-networking-debug-lab.md

Tasks:
1. Create connections and observe ESTABLISHED, TIME_WAIT states
2. Use ss -tn to see current connection states
"""

import socket
import time


def observe_connection_states():
    """Create a connection, close it, then inspect states with ss."""
    # TODO: Create a socket connection
    # TODO: Print instructions to run: ss -tn | grep <port>
    # TODO: Show ESTABLISHED state
    # TODO: Close connection and show TIME_WAIT state
    pass


if __name__ == "__main__":
    observe_connection_states()
