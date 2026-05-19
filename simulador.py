# SIMULADOR DE PROCESSADOR SIMPLES

def inicializar_sistema():
    """Inicializa os componentes do hardware."""
    # Memória RAM com 32 posições (todas zeradas inicialmente)
    ram = [0] * 32
    
    # Banco de Registradores (R0, R1, R2, R3)
    registradores = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
    
    # Registradores de Controle
    pc = 0  
    ir = ""

    return ram, registradores, pc, ir

#Lê as instruções do arquivo de entrada.
def ler_arquivo_entrada(nome_arquivo="entrada.txt"):
    """Lê as instruções do arquivo de entrada (máximo 32 linhas)."""
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            # Lê as linhas, remove espaços em branco e ignora linhas vazias
            instrucoes = [linha.strip() for linha in f.readlines() if linha.strip()]
            return instrucoes[:32]  # Garante o limite máximo de 32 linhas
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        print("Crie um arquivo 'entrada.txt' na mesma pasta com as instruções.")
        return []

def salvar_resultados(pc, ir, registradores, ram):
    """Gera os três arquivos de saída com o estado FINAL da execução."""
    
    # 1. Unidade de Controle
    with open("unidade_controle.txt", "w", encoding="utf-8") as f:
        f.write(f"PC: {pc}\n")
        f.write(f"IR: {ir}\n")
        
    # 2. Banco de Registradores
    with open("banco_registradores.txt", "w", encoding="utf-8") as f:
        f.write(f"R0: {registradores['R0']}\n")
        f.write(f"R1: {registradores['R1']}\n")
        f.write(f"R2: {registradores['R2']}\n")
        f.write(f"R3: {registradores['R3']}\n")
        
    # 3. Memória RAM (32 linhas)
    with open("memoria_ram.txt", "w", encoding="utf-8") as f:
        for i in range(32):
            f.write(f"Posicao {i:02d}: {ram[i]}\n")

def simular_processador():
    # Inicializa o Hardware
    ram, registradores, pc, ir = inicializar_sistema()
    
    # Carrega o programa na memória de instruções (simulada aqui pela lista)
    programa = ler_arquivo_entrada()
    if not programa:
        return

    # Flags para controle da ALU (Unidade Lógica e Aritmética)
    alu_zero = False
    alu_negative = False
    
    rodando = True
    
    # Loop do Ciclo de Instrução
    while rodando and pc < len(programa):
        
        # 1. FETCH (Busca)
        ir = programa[pc]
        instrucao_atual = ir # Guarda para o log final
        pc += 1 # Avança o PC para a próxima instrução
        
        # 2. DECODE (Decodificação)
        partes = ir.split()
        opcode = partes[0].upper() # O comando (Ex: LOAD, ADD)
        
        # 3. EXECUTE (Execução)
        
        # --- Instruções de Movimentação de Dados ---
        if opcode == "LOAD":
            reg = partes[1].upper()
            mem = int(partes[2])
            registradores[reg] = ram[mem]
            
        elif opcode == "STORE":
            mem = int(partes[1])
            reg = partes[2].upper()
            ram[mem] = registradores[reg]
            
        elif opcode == "MOVE":
            reg1 = partes[1].upper()
            reg2 = partes[2].upper()
            registradores[reg1] = registradores[reg2]
            
        # --- Instruções Aritméticas e Lógicas ---
        elif opcode == "ADD":
            reg1 = partes[1].upper()
            reg2 = partes[2].upper()
            reg3 = partes[3].upper()
            resultado = registradores[reg2] + registradores[reg3]
            registradores[reg1] = resultado
            
            # Atualiza as flags da ALU
            alu_zero = (resultado == 0)
            alu_negative = (resultado < 0)
            
        elif opcode == "SUB":
            reg1 = partes[1].upper()
            reg2 = partes[2].upper()
            reg3 = partes[3].upper()
            resultado = registradores[reg2] - registradores[reg3]
            registradores[reg1] = resultado
            
            # Atualiza as flags da ALU
            alu_zero = (resultado == 0)
            alu_negative = (resultado < 0)
            
        elif opcode == "AND":
            reg1 = partes[1].upper()
            reg2 = partes[2].upper()
            reg3 = partes[3].upper()
            resultado = registradores[reg2] & registradores[reg3]
            registradores[reg1] = resultado
            
            alu_zero = (resultado == 0)
            alu_negative = (resultado < 0)
            
        elif opcode == "OR":
            reg1 = partes[1].upper()
            reg2 = partes[2].upper()
            reg3 = partes[3].upper()
            resultado = registradores[reg2] | registradores[reg3]
            registradores[reg1] = resultado
            
            alu_zero = (resultado == 0)
            alu_negative = (resultado < 0)
            
        # --- Instruções de Desvio (Branching) ---
        elif opcode == "BRANCH":
            mem = int(partes[1])
            pc = mem # Desvia o PC para a linha da memória especificada
            
        elif opcode == "BZERO":
            mem = int(partes[1])
            if alu_zero:
                pc = mem
                
        elif opcode == "BNEG":
            mem = int(partes[1])
            if alu_negative:
                pc = mem
                
        # --- Outras Instruções ---
        elif opcode == "NOP":
            pass # Não faz nada
            
        elif opcode == "HALT":
            rodando = False # Para a execução da máquina
            
        else:
            print(f"Instrução desconhecida encontrada: {opcode}")
            rodando = False

    # Grava o estado FINAL nos arquivos TXT exigidos
    salvar_resultados(pc, instrucao_atual, registradores, ram)
    print("Simulação concluída com sucesso! Arquivos de saída gerados.")

# Executa o simulador
if __name__ == "__main__":
    simular_processador()