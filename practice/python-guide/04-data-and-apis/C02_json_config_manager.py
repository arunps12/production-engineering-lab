"""
Exercise 4.C.2 — JSON Configuration Manager
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. Define default config as a dict
2. Implement deep_merge(base, overrides)
3. Implement validate_config(config) → list of errors
4. Load config with layered overrides: defaults → file → env vars
"""

import json
import os

DEFAULT_CONFIG = {
    "app": {"name": "my-service", "version": "0.1.0", "debug": False},
    "server": {"host": "0.0.0.0", "port": 8000, "workers": 1},
    "logging": {"level": "INFO", "format": "json"},
}


def deep_merge(base: dict, overrides: dict) -> dict:
    """Recursively merge two dicts. Overrides take precedence."""
    # TODO: Implement
    pass


def validate_config(config: dict) -> list:
    """Validate config and return list of error strings."""
    # TODO: Implement (check required fields, valid port range, etc.)
    pass


def load_config(config_path: str = None) -> dict:
    """Load config: defaults → file → env vars."""
    # TODO: Implement
    pass


# TODO: Test deep merge, validation, and loading
