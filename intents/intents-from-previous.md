# Intents From Previous Codebase

## Scope

This note captures high-level user intents inferred from the implemented repository behavior as of 2026-03-18. It is based on executable code, tests, and packaging metadata rather than roadmap text.

## Observed Product Purpose

The current codebase implements an experimental command-line tool for working with project scaffolds.

The code supports these core outcomes:

- discover scaffolds from configured filesystem roots
- generate a new project from a chosen scaffold
- inspect and initialize user and scaffold configuration
- iterate on scaffold development by regenerating a sample output on file changes

In practical terms, the tool is aimed at local developer workflows around project bootstrapping and scaffold maintenance.

## Primary User Intents

### 1. Bootstrap a new project quickly

User intent:
Create a new project directory from a reusable scaffold with Copier.

Evidence:

- [Project command](../creat/cmd/project.py)
- [Scaffold discovery](../creat/scaffolds.py)

### 2. Maintain a personal or team scaffold library

User intent:
Keep scaffolds in one or more local root directories and discover them by name.

Evidence:

- [User config model](../creat/configs.py)
- [Scaffold index builder](../creat/scaffolds.py)

### 3. Inspect and initialize configuration

User intent:
Print current config, understand defaults, and create a missing local scaffold config file.

Evidence:

- [Config commands](../creat/cmd/config.py)
- [Config models and JSON loading](../creat/configs.py)

### 4. Develop scaffolds iteratively

User intent:
Render a sample project, watch for template changes, recopy updates, and optionally run post-copy shell commands.

Evidence:

- [Sample command](../creat/cmd/sample.py)
- [Scaffold config sample runs](../creat/configs.py)
- [Directory context manager](../creat/processes.py)

## Likely User Personas

- Scaffold consumer: a developer creating a new project from an existing template.
- Scaffold maintainer: a developer iterating on a scaffold and validating generated output.
- Team or platform owner: a person curating a shared set of scaffolds under configured roots.

## Implemented User-Facing Flows

The current CLI exposes these verified flows:

- `creat list`
- `creat config user`
- `creat config scaffold [PATH] [--init]`
- `creat project <scaffold> <target> [--dry-run]`
- `creat sample <scaffold> [--sample-path PATH]`

## What The Current Code Does Not Clearly Indicate

- There is no evidence of a remote scaffold registry or network service.
- There is no interactive scaffold authoring wizard.
- There is no GUI or web interface.
- There is no implemented user-facing `IdSubs` feature; the only `IdSubs` code lives in [tests/test_idsubs.py](../tests/test_idsubs.py) and should be treated as test-only or exploratory.

## Confidence And Gaps

High confidence:

- local CLI scaffolding workflow
- Copier-backed project generation
- scaffold-maintainer sample loop

Lower confidence:

- target team size and long-term distribution model
- future scope beyond local filesystem workflows

Reason for lower confidence:

- [README.md](../README.md) and [pyproject.toml](../pyproject.toml) describe the project only as experimental

## Working Product Statement

A concise statement of present-day intent derived from code:

"creat is a local CLI for discovering project scaffolds, generating projects from them, and iterating on scaffold development through watched sample regeneration."
