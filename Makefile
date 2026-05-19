# Makefile para o Simulador de Processador Simples (Python)

# Variáveis
PYTHON = python3
SCRIPT = simulador.py
ENTRADA = entrada.txt

.PHONY: all run clean help

# Alvo padrão: executa o simulador
all: run

# Executa o simulador garantindo que o arquivo de entrada exista
run:
	@if [ ! -f $(ENTRADA) ]; then \
		echo "Erro: O arquivo '$(ENTRADA)' não foi encontrado!"; \
		echo "Por favor, crie o arquivo '$(ENTRADA)' antes de rodar."; \
		exit 1; \
	fi
	@echo "Iniciando a simulação do processador..."
	$(PYTHON) $(SCRIPT)

# Limpa os arquivos de saída gerados pelo simulador
clean:
	@echo "Removendo arquivos de saída gerados..."
	rm -f unidade_controle.txt banco_registradores.txt memoria_ram.txt
	@echo "Limpeza concluída."

# Ajuda / Comandos disponíveis
help:
	@echo "Comandos disponíveis no Makefile:"
	@echo "  make run   - Executa o simulador (usa o arquivo $(ENTRADA))"
	@echo "  make clean - Remove os arquivos de saída gerados (.txt)"
	@echo "  make help  - Mostra esta mensagem de ajuda"