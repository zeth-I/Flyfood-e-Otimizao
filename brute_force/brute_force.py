import time

# Recebe dois números no modelo de plano cartesiano | Exemplo: 4 5 (4x5)
dimensoes_matriz = input("Dimensões da matriz: ").split() 

# Determinar listas para serem usadas mais na frente
matriz = []
locais = []
route = []
best_route = []
comp = []

# Função para definir o melhor caminho
def melhor_caminho(comb, coords, empty):
    short_route = 0
    i = 0
    j = 0
    temp = 0
    for c in range(0,len(comb)):
        for d in range(0,len(comb[c])-1):
            while (coords[i][0] != comb[c][d]):
                i += 1
            while (coords[j][0] != comb[c][d+1]):
                j += 1
            a = coords[i][1]
            b = coords[j][1]
            x = coords[i][2]
            y = coords[j][2]
            temp = temp + (abs(a-b) + abs(x-y))
            i = j = 0
        if(short_route == 0):
            empty = comb[c]
            short_route = temp
        elif(temp < short_route):
            short_route = temp
            empty = comb[c]
        temp = 0
    print(empty, len(comb))

# Função para gerar permutações
def permutacoes(lista, r = None):
    t = tuple(lista)
    n = len(t)
    r = n if r is None else r
    if r > n:
        return
    tabela = list(range(n))
    rotacao = list(range(n, n-r, -1))

    yield tuple(t[i] for i in tabela[:r])
    while n:
        for i in reversed(range(r)):
            rotacao[i] -= 1
            if rotacao[i] == 0:
                tabela[i:] = tabela[i+1:] + tabela[i:i+1]
                rotacao[i] = n - i
            else:
                j = rotacao[i]
                tabela[i], tabela[-j] = tabela[-j], tabela[i]
                yield tuple(t[i] for i in tabela[:r])
                break
        else:
            return

for c in range(0, int(dimensoes_matriz[0])):
    matriz.append([])
    for d in range(0,int(dimensoes_matriz[1])):
        matriz[c].append(0)
while True:
    pontos = [str(i) for i in input("Pontos(Modelo: Ponto Linha Coluna): ").split()]
    # Entrada de letra e posição de X e Y dentro da matriz PONTO lINHA COLUNA

    if pontos:
        nome = pontos[0].upper()
        locais.append(nome)
        x = int(pontos[1])
        y = int(pontos[2])
        matriz[x-1][y-1] = nome
    else:
        break

# print(matriz) # Para visualizar a matriz

start = str(input("Ponto de partida: ")).upper()
locais.remove(start)

inicio = time.time()
arranjo = list(permutacoes(locais, len(locais)))

for item in arranjo:
    best_route.append(list(item))

for item in best_route:
    item.append(start)
    item.insert(0,start)

for c in range(0,len(matriz)):
    for d in range(0,len(matriz[c])):
        for e in range(0,len(best_route)):
            for f in range(0,len(best_route[e])):
                if len(route) == 0:
                    if matriz[c][d] == best_route[e][f]:
                        route.append([matriz[c][d],c+1,d+1])
                else:
                    if (matriz[c][d] == best_route[e][f]) and ([matriz[c][d],c+1,d+1] not in route):
                        route.append([matriz[c][d],c+1,d+1])
                        
melhor_caminho(best_route, route, comp)
fim = time.time()
print("O tempo de execução:", (fim-inicio))