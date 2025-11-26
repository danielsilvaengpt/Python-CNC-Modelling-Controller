import math
import os
import random
import meshio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Função para converter graus em radianos
def converterGrausParaRadianos(graus):
    radianos = (graus / 180) * math.pi
    return radianos


# Função para calcular o cosseno
def cosseno(rad):
    radianos = converterGrausParaRadianos(rad)
    return round(math.cos(radianos), 6)


# Função para calcular o seno
def seno(rad):
    radianos = converterGrausParaRadianos(rad)
    return round(math.sin(radianos), 6)


# Função para gerar as coordenadas dos pinos
def gerarCoordenadasPinos(x_max, y_max, diametro_pino, espacamento_pino, angulo, ax):
    valores_x = np.arange(0, x_max, espacamento_pino + diametro_pino)
    valores_y = np.arange(0, y_max, espacamento_pino + diametro_pino)

    xx, yy = np.meshgrid(valores_x, valores_y)

    raio = diametro_pino / 2

    cos_ = cosseno(angulo)
    distAngCos = (diametro_pino + espacamento_pino) * cos_

    sin_ = seno(angulo)
    distAngSin = (diametro_pino + espacamento_pino) * sin_
    distAngSinY = (diametro_pino + espacamento_pino) - distAngSin

    centros_iniciais = []
    for i in range(len(valores_y)):
        for j in range(len(valores_x)):
            centro_inicial_x = xx[i, j] + raio
            centro_inicial_y = yy[i, j] + raio
            if centro_inicial_x + raio < x_max and centro_inicial_y + raio < y_max:
                centros_iniciais.append((centro_inicial_x, centro_inicial_y))

    distancia_xy = centros_iniciais[-1]
    distancia_meio_x = (x_max - (distancia_xy[0] + raio)) / 2
    distancia_meio_y = (y_max - (distancia_xy[1] + raio)) / 2

    centros_finais = []
    dados = []
    n_pinos = 0
    for i in range(len(valores_y)):
        for j in range(len(valores_x)):
            centro_final_x = xx[i, j] + raio + distancia_meio_x
            centro_final_y = yy[i, j] + raio + distancia_meio_y
            if i % 2 != 0:
                centro_final_x += distAngCos
            if centro_final_x + raio < x_max and centro_final_y + raio < y_max:
                n_pinos += 1
                centros_finais.append((centro_final_x, centro_final_y))
                circulo = plt.Circle((centro_final_x, centro_final_y), raio, edgecolor='blue', facecolor='none')
                ax.add_patch(circulo)
                ax.plot(centro_final_x, centro_final_y, "ro", markersize=0.5)
                dados.append((centro_final_x, centro_final_y))

    ax.set_aspect('equal', 'box')
    ax.axhline(y=0, color="black", linestyle="--", linewidth=1)
    ax.axvline(x=0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_xlim(-1, x_max)
    ax.set_ylim(-1, y_max)
    ax.set_title('Modelo de Pinos 2D')
    ax.legend(['Nº Total de Pinos: {}'.format(n_pinos)], loc='upper right', fontsize=10, bbox_to_anchor=(1, 1.3),
              borderaxespad=0.1)

    print("\nNúmero Total de Pinos:", n_pinos)
    # Cálculo da área total do retângulo
    area_total = x_max * y_max

    # Cálculo da área de cada circunferência
    area_circunferencia = math.pi * (raio ** 2)

    # Cálculo da soma das áreas das circunferências
    area_total_circunferencias = area_circunferencia * len(centros_finais)

    # Cálculo da área fora das circunferências
    area_fora_circunferencias = area_total - area_total_circunferencias

    print("Área fora das circunferências:", area_fora_circunferencias)
    return dados


# Função para gerar as coordenadas dos pinos
def gerarCoordenadasPinosSemAX(x_max, y_max, diametro_pino, espacamento_pino, angulo):
    valores_x = np.arange(0, x_max, espacamento_pino + diametro_pino)
    valores_y = np.arange(0, y_max, espacamento_pino + diametro_pino)

    xx, yy = np.meshgrid(valores_x, valores_y)

    raio = diametro_pino / 2

    cos_ = cosseno(angulo)
    distAngCos = (diametro_pino + espacamento_pino) * cos_

    sin_ = seno(angulo)
    distAngSin = (diametro_pino + espacamento_pino) * sin_
    distAngSinY = (diametro_pino + espacamento_pino) - distAngSin

    centros_iniciais = []
    for i in range(len(valores_y)):
        for j in range(len(valores_x)):
            centro_inicial_x = xx[i, j] + raio
            centro_inicial_y = yy[i, j] + raio
            if centro_inicial_x + raio < x_max and centro_inicial_y + raio < y_max:
                centros_iniciais.append((centro_inicial_x, centro_inicial_y))

    distancia_xy = centros_iniciais[-1]
    distancia_meio_x = (x_max - (distancia_xy[0] + raio)) / 2
    distancia_meio_y = (y_max - (distancia_xy[1] + raio)) / 2

    centros_finais = []
    dados = []
    n_pinos = 0
    for i in range(len(valores_y)):
        for j in range(len(valores_x)):
            centro_final_x = xx[i, j] + raio + distancia_meio_x
            centro_final_y = yy[i, j] + raio + distancia_meio_y
            if i % 2 != 0:
                centro_final_x += distAngCos
            if centro_final_x + raio < x_max and centro_final_y + raio < y_max:
                n_pinos += 1
                centros_finais.append((centro_final_x, centro_final_y))
    # Cálculo da área total do retângulo
    area_total = x_max * y_max

    # Cálculo da área de cada circunferência
    area_circunferencia = math.pi * (raio ** 2)

    # Cálculo da soma das áreas das circunferências
    area_total_circunferencias = area_circunferencia * len(centros_finais)

    # Cálculo da área fora das circunferências
    area_fora_circunferencias = area_total - area_total_circunferencias

    print("Área fora das circunferências:", area_fora_circunferencias)
    return dados


# Função para ajustar as coordenadas Z dos pinos com base no modelo
def ajustarCoordenadasZ(dados, modelo_x, modelo_y, modelo_z):
    DistEuclidiana = []
    num_pontos_modelo = len(modelo_x)
    for i in range(len(dados)):
        x, y = dados[i]
        distancia_minima = float('inf')
        z_mais_proximo = 0
        for j in range(num_pontos_modelo):
            distancia = np.sqrt((x - modelo_x[j]) ** 2 + (y - modelo_y[j]) ** 2)
            if distancia < distancia_minima:
                distancia_minima = distancia
                z_mais_proximo = modelo_z[j]

        dados[i] = (x, y, z_mais_proximo)
        DistEuclidiana.append(distancia_minima)

    return dados, DistEuclidiana


# Função para plotar as coordenadas ajustadas dos pinos e o modelo
def plotarCoordenadasPinos(modelo_x, modelo_y, modelo_z, df, x_max, y_max, ax):
    ax.scatter(modelo_x, modelo_y, modelo_z, color='red', s=5)
    ax.scatter(df['X'], df['Y'], df['Z'], color='black', s=15)
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_title('Coordenadas do modelo 3d e pinos do molde')
    ax.legend(['Pontos do Modelo: {}'.format(len(modelo_x)), 'Nº de Pinos: {}'.format(len(df['X']))], loc='upper right',
              fontsize=10, bbox_to_anchor=(1.05, 1.0), borderaxespad=3)
    print("Número Total de Pontos do Modelo:", len(modelo_x))

    # Configurar cor de fundo e legendas em branco
    ax.set_facecolor('#151515')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(colors='white')

# Função para plotar as coordenadas ajustadas dos pinos e o modelo
def plotarPinos3D(df, x_max, y_max, ax):
    ax.scatter(df['X'], df['Y'], df['Z'], color='black', s=15)
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_title('Modelo 3D')
    ax.legend(['Nº de Pinos: {}'.format(len(df['X']))], loc='upper right',
              fontsize=10, bbox_to_anchor=(1.05, 1.5), borderaxespad=3)


# Função para ler o arquivo do modelo
def lerArquivoModelo(caminho_arquivo):
    mesh = meshio.read(caminho_arquivo)
    vertices = mesh.points
    modelo_x = vertices[:, 0].astype(int)
    modelo_y = vertices[:, 1].astype(int)
    modelo_z = vertices[:, 2].astype(float)
    return modelo_x, modelo_y, modelo_z


# Função para dimensionar e deslocar as coordenadas do modelo
def dimensionarDeslocarCoordenadasModelo(modelo_x, modelo_y, x_max, y_max, z_max, modelo_z):
    max_x = np.amax(modelo_x)
    max_y = np.amax(modelo_y)
    max_z = np.amax(modelo_z)

    modelo_x = (modelo_x / (max_x / x_max))
    modelo_y = (modelo_y / (max_y / y_max))

    if max_z > z_max:
        print("\nEscalado")
        modelo_z = (modelo_z / (max_z / z_max))
    else:
        print("")
        print("\nNao precisa de ser escalado")

    min_x = np.min(modelo_x)
    min_y = np.min(modelo_y)

    modelo_x = modelo_x - min_x
    modelo_y = modelo_y - min_y

    meio_x = x_max / 2
    meio_y = y_max / 2

    ponto_medio_x = np.mean(modelo_x)
    ponto_medio_y = np.mean(modelo_y)

    deslocamento_x = meio_x - ponto_medio_x
    deslocamento_y = meio_y - ponto_medio_y

    modelo_x = (modelo_x + deslocamento_x)
    modelo_y = (modelo_y + deslocamento_y)

    return modelo_x, modelo_y, modelo_z


# Função para criar um arquivo de texto e escrever as coordenadas dos pinos
def criarArquivoCoordenadasPinos(nome_arquivo, dados, modelo_zE):

    with open("Sistema_Visao.txt", "r") as fileSystemVision:
        LinhasSV = len(fileSystemVision.readline())

    if LinhasSV == 0:
        with open(nome_arquivo, 'w') as arquivo:
            for i, row in dados.iterrows():
                z_aleatorio = random.uniform(min(modelo_zE), max(modelo_zE))
                arquivo.write(f"{i} {z_aleatorio}\n")


# Função principal
def principal(x_max, y_max, diametro_pino, espacamento_pino, angulo, nome_arquivo, z_max):
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(131)

    coordenadas_pinos = gerarCoordenadasPinos(x_max, y_max, diametro_pino, espacamento_pino, angulo, ax1)

    modelo_x, modelo_y, modelo_z = lerArquivoModelo(nome_arquivo)

    modelo_x, modelo_y, modelo_zE = dimensionarDeslocarCoordenadasModelo(modelo_x, modelo_y, x_max, y_max, z_max, modelo_z)

    coordenadas_pinos, distanciaEuclidiana = ajustarCoordenadasZ(coordenadas_pinos, modelo_x, modelo_y, modelo_zE)

    df = pd.DataFrame(coordenadas_pinos, columns=['X', 'Y', 'Z'])
    df.index = df.index + 1
    print("\nCoordenadas dos pinos:")
    print(df)

    MinEuclidiano = min(distanciaEuclidiana)
    MaxEuclidiano = max(distanciaEuclidiana)
    MediaEuclidiana = sum(distanciaEuclidiana) / len(distanciaEuclidiana)

    print("\nMinimo Distancia Euclidiana:", MinEuclidiano)
    print("Maxima Distancia Euclidiana: ", MaxEuclidiano)
    print("Media Distancia Euclidiana: ", MediaEuclidiana, "\n")

    ax2 = fig.add_subplot(132, projection='3d')
    plotarCoordenadasPinos(modelo_x, modelo_y, modelo_zE, df, x_max, y_max, ax2)

    ax3 = fig.add_subplot(133, projection='3d')
    plotarPinos3D(df, x_max, y_max, ax3)

    # Chamada da função no final da função principal
    nome_arquivo = "Sistema_Visao.txt"  # Nome do arquivo a ser criado
    criarArquivoCoordenadasPinos(nome_arquivo, df, modelo_zE)

    plt.savefig('Modelo.png')

    return coordenadas_pinos , modelo_x , modelo_y , modelo_zE , x_max , y_max , df