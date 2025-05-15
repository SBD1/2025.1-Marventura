# Makefile

VENV=.venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip3
REQS=requisitos.txt

# Instala o ambiente virtual e dependências, se necessário
setup:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install -r $(REQS)

# Executa o jogo
start: setup
	@$(PYTHON) main.py
