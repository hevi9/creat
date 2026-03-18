UV := uv
PIPX := pipx
VERSION := $(shell sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml | head -n 1)
PRE_COMMIT := pre-commit
NAME := $(shell basename $(shell pwd))
WHEEL := $(NAME)-$(VERSION)-py3-none-any.whl
DISTDIR := dist
GIT := git
UV_ACTIVE_FLAG := $(if $(VIRTUAL_ENV),--active,)

help::
	@echo 'Targets:'
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

requires::
	which $(UV)

pull:: ## Pull the git repository
	$(GIT) pull
	$(GIT) pull --recurse-submodules
	$(GIT) pull --tags

check-clean-workspace:: ## Check the workspace
	$(GIT) diff --exit-code
	$(GIT) diff --cached --exit-code
	$(GIT) diff --submodule=log --exit-code

push:: check-clean-workspace check ## Push the repository
	$(GIT) push
	$(GIT) push --recurse-submodules check
	$(GIT) push --tags

clean:: ## Clean the repository
	rm -rf .venv .doit.db dist

deploy-user:: check ## Deploy the user
	$(UV) build --wheel --out-dir=$(DISTDIR)
	$(PIPX) install --force $(DISTDIR)/$(WHEEL)

local:: requires ## Install the local environment
	# Keep console scripts visible when the caller already activated a venv.
	$(UV) sync $(UV_ACTIVE_FLAG) --group dev
	$(PRE_COMMIT) install --install-hooks
	$(PRE_COMMIT) install --hook-type commit-msg

update:: ## Update the local environment
	# Keep console scripts visible when the caller already activated a venv.
	$(UV) sync $(UV_ACTIVE_FLAG) --group dev --upgrade
	$(PRE_COMMIT) autoupdate
	$(PRE_COMMIT) install --install-hooks

check:: ## Check the code
	$(UV) run ruff check creat tests
	$(UV) run mypy creat tests
	$(UV) run pytest -v --disable-warnings --maxfail=1

lock:: ## Lock the dependencies
	$(UV) lock
