EXE.POETRY2 := $(shell which poetry2 poetry@2)
POETRY := $(EXE.POETRY2)
PIPX := pipx
VERSION := $(shell $(POETRY) version --short)
PRE_COMMIT := pre-commit
NAME := $(shell basename $(shell pwd))
WHEEL := $(NAME)-$(VERSION)-py3-none-any.whl
DISTDIR := dist
GIT := git

help::
	@echo 'Targets:'
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

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
	$(POETRY) build --no-interaction --format=wheel --output=$(DISTDIR)
	$(PIPX) install --force $(DISTDIR)/$(WHEEL)

local:: ## Install the local environment
	$(POETRY) sync --no-interaction
	$(PRE_COMMIT) install --install-hooks
	$(PRE_COMMIT) install --hook-type commit-msg

update:: ## Update the local environment
	$(POETRY) update --no-interaction
	$(PRE_COMMIT) autoupdate
	$(PRE_COMMIT) install --install-hooks

check:: ## Check the code
	$(POETRY) check
	$(POETRY) run ruff check creat tests
	$(POETRY) run mypy creat tests
	$(POETRY) run pytest -v --disable-warnings --maxfail=1

lock:: ## Lock the dependencies
	$(POETRY) lock
