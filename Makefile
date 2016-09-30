ifndef VIRTUAL_ENV
$(error You don't seem to be inside a virtualenv, please activate it and run this again)
endif

.PHONY: run

run:
	python main.py

.pip-tools-installed-flag:
	@echo "## Installing pip-tools"
	# https://pip.pypa.io/en/stable/user_guide/#only-if-needed-recursive-upgrade
	pip install --upgrade pip-tools
	touch .pip-tools-installed-flag

requirements.txt: requirements.in .pip-tools-installed-flag
	@echo "## Compiling requirements.txt"
	pip-compile --output-file requirements.txt requirements.in

.PHONY: pip-sync
pip-sync: requirements.txt
	@echo "## Syncing requirements.txt with virtualenv's installed packages"
	pip-sync
