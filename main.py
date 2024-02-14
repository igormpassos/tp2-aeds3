#Igor Marques Passos
#22.2.8118

from manipulaBMP import MovimentacaoEquipamento

# Função para interação com o usuário
def obter_pasta_bitmap():
    pasta = input("Informe a pasta contendo o(s) arquivo(s) bitmap: ")
    return pasta

# Função principal
def main():
    # Obtém a pasta contendo os arquivos bitmap
    pasta_bitmap = obter_pasta_bitmap()

    # Cria uma instância da classe MovimentacaoEquipamento
    movimentacao_equipamento = MovimentacaoEquipamento()

    # Processa os arquivos bitmap na pasta
    movimentacao_equipamento.processar_bitmap(pasta_bitmap)

    # Encontrar o caminho
    caminho = movimentacao_equipamento.encontrar_caminho()

    # Exibe o caminho ao usuário
    print("É possível deslocar o equipamento:")
    print(caminho)

    
main();