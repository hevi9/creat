# Removal From Previous Codebase

## Goal

- remove the old scaffold-based project creation code
- keep only the foundations needed for the new AI-agent-supported project creation system

## Keep

- the config system in [creat/configs.py](../creat/configs.py)
- the `creat/cmd/` package structure as a skeleton for future commands
- project metadata in [pyproject.toml](../pyproject.toml), migrated from Poetry workflows to uv

## Remove

- scaffold discovery and rendering code
- scaffold-specific command implementations
- scaffold-specific configuration models and fields
- scaffold-related tests
- scaffold-related documentation

## Status

Implemented in the repository on 2026-03-18.

The codebase now preserves configuration utilities and command-module placeholders while removing the old scaffold execution path.
