from graph import Graph
from PIL import Image
from os import listdir
from typing import Tuple, List
from os.path import isfile, join
from queue import PriorityQueue


class MovimentacaoEquipamento:
    
    def __init__(self):
        self.grafo = Graph()
        self.posicao_inicial = None
        self.posicoes_destino = []
        self.caminho = []

# Processa o arquivo bitmap e constrói o grafo
    def processar_bitmap(self, pasta: str) -> None:
        # Lista todos os arquivos na pasta
        arquivos = [f for f in listdir(pasta) if isfile(join(pasta, f))]

        # Determina o número de andares com base nos arquivos presentes
        num_andares = len(arquivos)

        for andar in range(num_andares):
            arquivo_bitmap = f"{pasta}/toy_{andar}.bmp"
            imagem = Image.open(arquivo_bitmap)
            largura, altura = imagem.size

            for i in range(altura):
                for j in range(largura):
                    cor_pixel = imagem.getpixel((j, i))

                    self.grafo.add_node((andar, i, j))

                    if cor_pixel == (255, 0, 0):  # Vermelho
                        self.posicao_inicial = (andar, i, j)

                    elif cor_pixel == (0, 255, 0):  # Verde
                        self.posicoes_destino.append((andar, i, j))

                    if cor_pixel != (0, 0, 0):
                        # Adiciona arestas com pesos considerando os diferentes tipos de pixel
                        if i > 0 and imagem.getpixel((j, i - 1)) != (0, 0, 0):
                            peso = 4 if cor_pixel == (128, 128, 128) else 2 if cor_pixel == (196, 196, 196) else 1
                            self.grafo.add_undirected_edge((andar, i, j), (andar, i - 1, j), peso)
                        if j > 0 and imagem.getpixel((j - 1, i)) != (0, 0, 0):
                            peso = 4 if cor_pixel == (128, 128, 128) else 2 if cor_pixel == (196, 196, 196) else 1
                            self.grafo.add_undirected_edge((andar, i, j), (andar, i, j - 1), peso)

                        if andar > 0 and imagem.getpixel((j, i)) != (0, 0, 0):
                            peso = 4 if cor_pixel == (128, 128, 128) else 2 if cor_pixel == (196, 196, 196) else 1
                            self.grafo.add_undirected_edge((andar, i, j), (andar - 1, i, j), peso)

            if andar < num_andares - 1:
                for i in range(altura):
                    for j in range(largura):
                        cor_pixel = imagem.getpixel((j, i))  # Adicione esta linha

                        if cor_pixel != (0, 0, 0):
                            peso = 4 if cor_pixel == (128, 128, 128) else 2 if cor_pixel == (196, 196, 196) else 1
                            self.grafo.add_undirected_edge((andar, i, j), (andar + 1, i, j), peso)

                            
    
    def encontrar_caminho(self) -> List[str]:
        # Utiliza o algoritmo de Dijkstra para encontrar o caminho mínimo
        distancias, predecessores = self.grafo.dijkstra(self.posicao_inicial)

        # Encontrar a posição de destino com menor distância
        posicao_destino = min(self.posicoes_destino, key=lambda destino: distancias[destino])

        # Reconstruir o caminho a partir dos predecessores
        caminho = self.reconstruir_caminho(predecessores, posicao_destino)

        return self.formatar_caminho(caminho)

    def reconstruir_caminho(self, visitados, destino) -> List:
        caminho = [destino]
        while destino in visitados and visitados[destino] is not None:
            destino = visitados[destino]
            caminho.insert(0, destino)
        return caminho

    # Trata os dados em sequências
    def formatar_caminho(self, caminho):
        caminho_formatado = ""
        ultimo_andar = None

        for no in caminho:
            andar, i, j = no

            if ultimo_andar is not None and andar != ultimo_andar:
                caminho_formatado += "ˆ"  # Caractere indicando mudança de andar

            caminho_formatado += "←" if j > 0 and (andar, i, j - 1) in caminho else "→"
            caminho_formatado += "↑" if i > 0 and (andar, i - 1, j) in caminho else "↓"

            ultimo_andar = andar

        return caminho_formatado

    def imprimir_caminho(self, caminho: List[str]) -> None:
        print("É possível deslocar o equipamento:")
        if len(caminho) == 1:
            print(caminho[0])
        else:
            print(" ".join(caminho))