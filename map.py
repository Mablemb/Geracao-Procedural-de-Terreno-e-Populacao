import random as rd
import numpy as np
import matplotlib.pyplot as plt

def map_propagate(map):
    
    """ Função para geração procedural que avança em 1 passo o mapa recebido.
    Usa a vizinhança de cada célula de map para gerar o valor da célula de
    next_map propagando-se.
    dos pontos de origem a cada iteração.

    Recebe: 
        map (2d array): matriz NxN contendo pontos que servirão de origem
        para a dispersão
    
    Retorna:
        next_map (2d array): mapa atualizado pelo algoritmo de propagação
    """
    next_map = np.zeros((len(map),len(map)))
    for i in range(2,len(next_map)-2):
        for j in range(2,len(next_map)-2):
            next_map[i][j] = (map[i+1][j] + map[i-1][j] + map[i][j+1] + map[i][j-1]
                              + map[i-1][j-1] + map[i-1][j+1] + map[i+1][j+1] + map[i+1][j-1])/8

    return next_map

def map_group(map, map_max):
    
    """ Agrupa as células utilizando intervalos de zero ao map_max como parâmetro.
    
    Recebe:
        map (2d array): mapa com valores dispersos
        map_max (float): maior valor em map

    Retorna:
        next_map (2d array): mapa com valores agrupados
    """
    
    next_map = np.zeros((len(map),len(map))) # Alocação de memória
    
    # Percorre o map e usa os valores de cada célula para atualizar o next_map
    for i in range(2,len(next_map)-2):
        for j in range(2,len(next_map)-2):
            
            # Decide o valor conforme o intervalo que se encaixa
            if map[i][j] >= map_max*(3/4):
                next_map[i][j] = 4
            elif map[i][j] >= map_max*(2/4):
                next_map[i][j] = 3
            elif map[i][j] >= map_max*(1/4):
                next_map[i][j] = 2
            elif map[i][j] >= map_max*(1/8):
                next_map[i][j] = 1
            else:
                next_map[i][j] = 0

    return next_map

def map_populate(map, pop_dens: int):
    
    """ Usa os valores de cada parte de map para gerar ou não um ponto em
    next_map

    Recebe:
        map (2d array): mapa com valores dispersos
        pop_dens (int): modificador de probabilidade da população de um ponto
        
    Returns:
        next_map (2d array): mapa com valores normalizados
    """
    next_map = np.zeros((len(map),len(map)))
    
    for i in range(2,len(next_map)-2):
        for j in range(2,len(next_map)-2):
            if map[i][j] != 0:
                chance = rd.randrange(0,100)
                viabilidade = pop_dens*map[i][j]
                
                next_map[i][j] = (1 if chance < viabilidade else 0)

    return next_map

map_size = 200
n_origins = 100
startValue = 100
nIterations = 100

print(f"Iniciando construção do mapa {map_size}x{map_size}, com {n_origins} origens e {nIterations} iterações.")

map_zero = np.zeros((map_size,map_size))

origins = list()

while len(origins) < n_origins*2:
    new_origin = rd.randint(2,map_size-2)
    if origins.count(new_origin) < 2:
        origins.append(new_origin)

for i in range(0, n_origins*2,2):
    map_zero[origins[i]][origins[i+1]] = startValue

print("MapaZero ok.")

map_result = map_propagate(map_zero)
for i in range(0,nIterations):
    map_result = map_propagate(map_result)
    if i%20 == 0:
        print(f"Progresso do mapa: {(i/nIterations)*100:.1f}%")
    
map_max = map_result.max(where=True)
print(map_max)
maxindex = np.unravel_index(map_result.argmax(), map_result.shape)
print(maxindex)

map_result2 = map_group(map_result, map_max)
print(f"Agrupando mapa...")

map_result3 = map_populate(map_result2,5)
print(f"Populando mapa 1...")

map_result4 = map_populate(map_result2,2)
print(f"Populando mapa 2...")

map_result5 = map_populate(map_result2,1)
print(f"Populando mapa 3...")

f, axarr = plt.subplots(2,2)
axarr[0,0].imshow(map_zero)
axarr[1,0].imshow(map_result)
axarr[0,1].imshow(map_result2)
axarr[1,1].imshow(map_result5)

plt.show()